# coding: utf-8
import base64
from decimal import *

from .asset import Asset
from .stellarxdr import Xdr
from .utils import account_xdr_object, signer_key_xdr_object, encode_check, best_rational_approximation as best_r, \
    division
from .utils import XdrLengthError

ONE = Decimal(10 ** 7)


class Operation(object):
    """what we can do in stellar network.
        follow the specific . the source can be none.
    """

    def __init__(self, opts):
        assert type(opts) is dict

        self.source = opts.get('source')
        self.body = Xdr.nullclass()

    def __eq__(self, other):
        return self.xdr() == other.xdr()

    def to_xdr_object(self):
        try:
            source_account = [account_xdr_object(self.source)]
        except TypeError:
            source_account = []
        return Xdr.types.Operation(source_account, self.body)

    def xdr(self):
        op = Xdr.StellarXDRPacker()
        op.pack_Operation(self.to_xdr_object())
        return base64.b64encode(op.get_buffer())

    @staticmethod
    def to_xdr_amount(value):
        if not isinstance(value, str):
            raise Exception("value must be a string")

        # throw exception if value * ONE has decimal places (it can't be represented as int64)
        return int((Decimal(value) * ONE).to_integral_exact(context=Context(traps=[Inexact])))

    @staticmethod
    def from_xdr_amount(value):
        return str(Decimal(value) / ONE)

    @classmethod
    def from_xdr(cls, xdr):
        xdr_decode = base64.b64decode(xdr)
        op = Xdr.StellarXDRUnpacker(xdr_decode)
        op = op.unpack_Operation()
        if op.type == Xdr.const.CREATE_ACCOUNT:
            return CreateAccount.from_xdr_object(op)
        elif op.type == Xdr.const.PAYMENT:
            return Payment.from_xdr_object(op)
        elif op.type == Xdr.const.PATH_PAYMENT:
            return PathPayment.from_xdr_object(op)
        elif op.type == Xdr.const.CHANGE_TRUST:
            return ChangeTrust.from_xdr_object(op)
        elif op.type == Xdr.const.ALLOW_TRUST:
            return AllowTrust.from_xdr_object(op)
        elif op.type == Xdr.const.SET_OPTIONS:
            return SetOptions.from_xdr_object(op)
        elif op.type == Xdr.const.MANAGE_OFFER:
            return ManageOffer.from_xdr_object(op)
        elif op.type == Xdr.const.CREATE_PASSIVE_OFFER:
            return CreatePassiveOffer.from_xdr_object(op)
        elif op.type == Xdr.const.ACCOUNT_MERGE:
            return AccountMerge.from_xdr_object(op)
        elif op.type == Xdr.const.INFLATION:
            return Inflation.from_xdr_object(op)
        elif op.type == Xdr.const.MANAGE_DATA:
            return ManageData.from_xdr_object(op)


class CreateAccount(Operation):
    def __init__(self, opts):
        super(CreateAccount, self).__init__(opts)
        self.destination = opts.get('destination')
        self.starting_balance = opts.get('starting_balance')

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)

        create_account_op = Xdr.types.CreateAccountOp(destination, Operation.to_xdr_amount(self.starting_balance))
        self.body.type = Xdr.const.CREATE_ACCOUNT
        self.body.createAccountOp = create_account_op
        return super(CreateAccount, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check('account', op_xdr_object.body.createAccountOp.destination.ed25519).decode()
        starting_balance = Operation.from_xdr_amount(op_xdr_object.body.createAccountOp.startingBalance)

        return cls({
            'source': source,
            'destination': destination,
            'starting_balance': starting_balance,
        })


class Payment(Operation):
    def __init__(self, opts):
        super(Payment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.asset = opts.get('asset')
        self.amount = opts.get('amount')

    def to_xdr_object(self):
        asset = self.asset.to_xdr_object()
        destination = account_xdr_object(self.destination)

        amount = Operation.to_xdr_amount(self.amount)

        payment_op = Xdr.types.PaymentOp(destination, asset, amount)
        self.body.type = Xdr.const.PAYMENT
        self.body.paymentOp = payment_op
        return super(Payment, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check('account', op_xdr_object.body.paymentOp.destination.ed25519).decode()
        asset = Asset.from_xdr_object(op_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(op_xdr_object.body.paymentOp.amount)

        return cls({
            'source': source,
            'destination': destination,
            'asset': asset,
            'amount': amount,
        })


class PathPayment(Operation):
    def __init__(self, opts):
        super(PathPayment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.send_asset = opts.get('send_asset')
        self.send_max = opts.get('send_max')
        self.dest_asset = opts.get('dest_asset')
        self.dest_amount = opts.get('dest_amount')
        self.path = opts.get('path')  # a list of paths/assets

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()

        path_payment = Xdr.types.PathPaymentOp(send_asset, Operation.to_xdr_amount(self.send_max), destination,
                                               dest_asset, Operation.to_xdr_amount(self.dest_amount), self.path)
        self.body.type = Xdr.const.PATH_PAYMENT
        self.body.pathPaymentOp = path_payment
        return super(PathPayment, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check('account', op_xdr_object.body.pathPaymentOp.destination.ed25519).decode()
        send_asset = Asset.from_xdr_object(op_xdr_object.body.pathPaymentOp.sendAsset)
        dest_asset = Asset.from_xdr_object(op_xdr_object.body.pathPaymentOp.destAsset)
        send_max = Operation.from_xdr_amount(op_xdr_object.body.pathPaymentOp.sendMax)
        dest_amount = Operation.from_xdr_amount(op_xdr_object.body.pathPaymentOp.destAmount)

        path = []
        if op_xdr_object.body.pathPaymentOp.path:
            for x in op_xdr_object.body.pathPaymentOp.path:
                path.append(Asset.from_xdr_object(x))

        return cls({
            'source': source,
            'destination': destination,
            'send_asset': send_asset,
            'send_max': send_max,
            'dest_asset': dest_asset,
            'dest_amount': dest_amount,
            'path': path
        })


class ChangeTrust(Operation):
    def __init__(self, opts):
        super(ChangeTrust, self).__init__(opts)
        self.line = opts.get('asset')
        if opts.get('limit') is not None:
            self.limit = opts.get('limit')
        else:
            self.limit = "922337203685.4775807"

    def to_xdr_object(self):
        line = self.line.to_xdr_object()
        limit = Operation.to_xdr_amount(self.limit)

        change_trust_op = Xdr.types.ChangeTrustOp(line, limit)
        self.body.type = Xdr.const.CHANGE_TRUST
        self.body.changeTrustOp = change_trust_op
        return super(ChangeTrust, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        line = Asset.from_xdr_object(op_xdr_object.body.changeTrustOp.line)
        print(line)
        limit = Operation.from_xdr_amount(op_xdr_object.body.changeTrustOp.limit)

        return cls({
            'source': source,
            'asset': line,
            'limit': limit
        })


class AllowTrust(Operation):
    def __init__(self, opts):
        super(AllowTrust, self).__init__(opts)
        self.trustor = opts.get('trustor')
        self.asset_code = opts.get('asset_code')
        self.authorize = opts.get('authorize')

    def to_xdr_object(self):
        trustor = account_xdr_object(self.trustor)
        length = len(self.asset_code)
        assert length <= 12
        pad_length = 4 - length if length <= 4 else 12 - length
        # asset_code = self.asset_code + '\x00' * pad_length
        # asset_code = bytearray(asset_code, encoding='utf-8')
        asset_code = bytearray(self.asset_code, 'ascii') + b'\x00' * pad_length
        asset = Xdr.nullclass()
        if len(asset_code) == 4:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            asset.assetCode4 = asset_code
        else:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            asset.assetCode12 = asset_code

        allow_trust_op = Xdr.types.AllowTrustOp(trustor, asset, self.authorize)
        self.body.type = Xdr.const.ALLOW_TRUST
        self.body.allowTrustOp = allow_trust_op
        return super(AllowTrust, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()
        trustor = encode_check('account', op_xdr_object.body.allowTrustOp.trustor.ed25519).decode()
        authorize = op_xdr_object.body.allowTrustOp.authorize

        asset_type = op_xdr_object.body.allowTrustOp.asset.type
        if asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code = op_xdr_object.body.allowTrustOp.asset.assetCode4.decode()
        elif asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code = op_xdr_object.body.allowTrustOp.asset.assetCode12.decode()
        else:
            raise Exception

        return cls({
            'source': source,
            'trustor': trustor,
            'authorize': authorize,
            'asset_code': asset_code
        })


class SetOptions(Operation):
    def __init__(self, opts):
        super(SetOptions, self).__init__(opts)
        self.inflation_dest = opts.get('inflation_dest')
        self.clear_flags = opts.get('clear_flags')
        self.set_flags = opts.get('set_flags')
        self.master_weight = opts.get('master_weight')
        self.low_threshold = opts.get('low_threshold')
        self.med_threshold = opts.get('med_threshold')
        self.high_threshold = opts.get('high_threshold')
        self.home_domain = opts.get('home_domain')

        self.signer_address = opts.get('signer_address')
        self.signer_type = opts.get('signer_type')
        self.signer_weight = opts.get('signer_weight')

        if self.signer_address is not None and self.signer_type is None:
            try:
                decode_check('account', self.signer_address)
            except DecodeError:
                raise Exception('must be a valid strkey if not give signer_type')
            self.signer_type = 'ed25519PublicKey'

        if self.signer_type in ('hashX', 'preAuthTx') and \
                (self.signer_address is None or len(self.signer_address) != 32):
            raise Exception('hashX or preAuthTx Signer must be 32 bytes')

        if self.signer_type is not None and self.signer_type not in ('ed25519PublicKey', 'hashX', 'preAuthTx'):
            raise Exception('invalid signer type.')

    def to_xdr_object(self):
        def assert_option_array(x):
            if x is None:
                return []
            if not isinstance(x, list):
                return [x]
            return x

        if self.inflation_dest is not None:
            inflation_dest = [account_xdr_object(self.inflation_dest)]
        else:
            inflation_dest = []

        self.clear_flags = assert_option_array(self.clear_flags)
        self.set_flags = assert_option_array(self.set_flags)
        self.master_weight = assert_option_array(self.master_weight)
        self.low_threshold = assert_option_array(self.low_threshold)
        self.med_threshold = assert_option_array(self.med_threshold)
        self.high_threshold = assert_option_array(self.high_threshold)
        self.home_domain = assert_option_array(self.home_domain)

        if self.signer_address is not None and \
                self.signer_type is not None and \
                self.signer_weight is not None:
            signer = [
                Xdr.types.Signer(signer_key_xdr_object(self.signer_type, self.signer_address), self.signer_weight)]
        else:
            signer = []

        set_options_op = Xdr.types.SetOptionsOp(inflation_dest, self.clear_flags, self.set_flags,
                                                self.master_weight, self.low_threshold, self.med_threshold,
                                                self.high_threshold, self.home_domain, signer)
        self.body.type = Xdr.const.SET_OPTIONS
        self.body.setOptionsOp = set_options_op
        return super(SetOptions, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        if not op_xdr_object.body.setOptionsOp.inflationDest:
            inflation_dest = None
        else:
            inflation_dest = encode_check('account', op_xdr_object.body.setOptionsOp.inflationDest[0].ed25519).decode()

        clear_flags = op_xdr_object.body.setOptionsOp.clearFlags  # list
        set_flags = op_xdr_object.body.setOptionsOp.setFlags
        master_weight = op_xdr_object.body.setOptionsOp.masterWeight
        low_threshold = op_xdr_object.body.setOptionsOp.lowThreshold
        med_threshold = op_xdr_object.body.setOptionsOp.medThreshold
        high_threshold = op_xdr_object.body.setOptionsOp.highThreshold
        home_domain = op_xdr_object.body.setOptionsOp.homeDomain

        if op_xdr_object.body.setOptionsOp.signer:
            key = op_xdr_object.body.setOptionOp.signer[0].key
            if key.type == Xdr.const.SIGNER_KEY_TYPE_ED25519:
                signer_address = encode_check('account', key.ed25519).decode()
                signer_type = 'ed25519PublicKey'
            if key.type == Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX:
                signer_address = key.preAuthTx
                signer_type = 'preAuthTx'
            if key.type == Xdr.const.SIGNER_KEY_TYPE_HASH_X:
                signer_address = key.hashX
                signer_type = 'hashX'

            signer_weight = op_xdr_object.body.setOptionsOp.signer[0].weight
        else:
            signer_address = None
            signer_type = None
            signer_weight = None

        return cls({
            'source': source,
            'inflation_dest': inflation_dest,
            'clear_flags': clear_flags,
            'set_flags': set_flags,
            'master_weight': master_weight,
            'low_threshold': low_threshold,
            'med_threshold': med_threshold,
            'high_threshold': high_threshold,
            'home_domain': home_domain,
            'signer_address': signer_address,
            'Signer_type': signer_type,
            'signer_weight': signer_weight
        })


class ManageOffer(Operation):
    def __init__(self, opts):
        super(ManageOffer, self).__init__(opts)
        self.selling = opts.get('selling')  # Asset
        self.buying = opts.get('buying')  # Asset
        self.amount = opts.get('amount')
        self.price = opts.get('price')
        self.offer_id = opts.get('offer_id', 0)

    def to_xdr_object(self):
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = best_r(self.price)
        price = Xdr.types.Price(price['n'], price['d'])

        amount = Operation.to_xdr_amount(self.amount)

        manage_offer_op = Xdr.types.ManageOfferOp(selling, buying, amount, price, self.offer_id)
        self.body.type = Xdr.const.MANAGE_OFFER
        self.body.manageOfferOp = manage_offer_op
        return super(ManageOffer, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        selling = Asset.from_xdr_object(op_xdr_object.body.manageOfferOp.selling)
        buying = Asset.from_xdr_object(op_xdr_object.body.manageOfferOp.buying)
        amount = Operation.from_xdr_amount(op_xdr_object.body.manageOfferOp.amount)

        n = op_xdr_object.body.manageOfferOp.price.n
        d = op_xdr_object.body.manageOfferOp.price.d
        price = division(n, d)
        offer_id = op_xdr_object.body.manageOfferOp.offerID

        return cls({
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': amount,
            'price': price,
            'offer_id': offer_id
        })


class CreatePassiveOffer(Operation):
    def __init__(self, opts):
        super(CreatePassiveOffer, self).__init__(opts)
        self.selling = opts.get('selling')
        self.buying = opts.get('buying')
        self.amount = opts.get('amount')
        self.price = opts.get('price')

    def to_xdr_object(self):
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        price = best_r(self.price)
        price = Xdr.types.Price(price['n'], price['d'])

        amount = Operation.to_xdr_amount(self.amount)

        create_passive_offer_op = Xdr.types.CreatePassiveOfferOp(selling, buying, amount, price)
        self.body.type = Xdr.const.CREATE_PASSIVE_OFFER
        self.body.createPassiveOfferOp = create_passive_offer_op
        return super(CreatePassiveOffer, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        selling = Asset.from_xdr_object(op_xdr_object.body.createPassiveOfferOp.selling)
        buying = Asset.from_xdr_object(op_xdr_object.body.createPassiveOfferOp.buying)
        amount = Operation.from_xdr_amount(op_xdr_object.body.createPassiveOfferOp.amount)

        n = op_xdr_object.body.createPassiveOfferOp.price.n
        d = op_xdr_object.body.createPassiveOfferOp.price.d
        price = division(n, d)
        return cls({
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': amount,
            'price': price
        })


class AccountMerge(Operation):
    def __init__(self, opts):
        super(AccountMerge, self).__init__(opts)
        self.destination = opts.get('destination')

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)

        self.body.type = Xdr.const.ACCOUNT_MERGE
        self.body.destination = destination
        return super(AccountMerge, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check('account', op_xdr_object.body.destination.ed25519).decode()

        return cls({
            'source': source,
            'destination': destination
        })


class Inflation(Operation):
    def __init__(self, opts):
        super(Inflation, self).__init__(opts)

    def to_xdr_object(self):
        self.body.type = Xdr.const.INFLATION
        return super(Inflation, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()
        return cls({'source': source})


class ManageData(Operation):
    def __init__(self, opts):
        super(ManageData, self).__init__(opts)
        self.data_name = opts.get('data_name')
        self.data_value = opts.get('data_value')
        if len(self.data_name) > 64 or (self.data_value is not None and len(self.data_value) > 64):
            raise XdrLengthError("Data or value should be <= 64 bytes (ascii encoded). ")

    def to_xdr_object(self):
        data_name = bytearray(self.data_name, encoding='utf-8')

        if self.data_value is not None:
            data_value = [bytearray(self.data_value, 'utf-8')]
        else:
            data_value = []
        manage_data_op = Xdr.types.ManageDataOp(data_name, data_value)
        self.body.type = Xdr.const.MANAGE_DATA
        self.body.manageDataOp = manage_data_op
        return super(ManageData, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check('account', op_xdr_object.sourceAccount[0].ed25519).decode()

        data_name = op_xdr_object.body.manageDataOp.dataName.decode()

        if op_xdr_object.body.manageDataOp.dataValue:
            data_value = op_xdr_object.body.manageDataOp.dataValue[0].decode()
        else:
            data_value = None
        return cls({
            'source': source,
            'data_name': data_name,
            'data_value': data_value
        })
