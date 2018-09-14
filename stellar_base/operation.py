# -*- coding: utf-8 -*-

import base64
from decimal import Context, Decimal, Inexact

from .asset import Asset
from .stellarxdr import Xdr
from .utils import (
    account_xdr_object, best_rational_approximation as best_r, decode_check,
    division, encode_check, signer_key_xdr_object)
from .exceptions import DecodeError, XdrLengthError

ONE = Decimal(10 ** 7)

# TODO: We should really consider not taking a dictionary of opts here, and
# instead should craft each operation's arguments to reasonable defaults and
# expectations of required arguments. It makes documentation better, as well
# as inspection of the method # definition. There's no reason that dictionary
# unpacking can't be used to facilitate easy dict -> kwargs conversion on the
# init statements.


class Operation(object):
    """The :class:`Operation` object, which represents an operation on
    Stellar's network.

    An operation is an individual command that mutates Stellar's ledger. It is
    typically rolled up into a transaction (a transaction is a list of
    operations with additional metadata).

    Operations are executed on behalf of the source account specified in the
    transaction, unless there is an override defined for the operation.

    For more on operations, see `Stellar's documentation on operations
    <https://www.stellar.org/developers/guides/concepts/operations.html>`_ as
    well as `Stellar's List of Operations
    <https://www.stellar.org/developers/guides/concepts/list-of-operations.html>`_,
    which includes information such as the security necessary for a given
    operation, as well as information about when validity checks occur on the
    network.

    The :class:`Operation` class is typically not used, but rather one of its
    subclasses is typically included in transactions.

    :param dict opts: A dict of options for creating this :class:`Operation`.
        By default, this only pulls out the source account via opts.source.

    """

    def __init__(self, opts):
        # FIXME: Use a better exception.
        assert type(opts) is dict

        self.source = opts.get('source')
        self.body = Xdr.nullclass()

    def __eq__(self, other):
        return self.xdr() == other.xdr()

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`Operation`.

        """
        try:
            source_account = [account_xdr_object(self.source)]
        except TypeError:
            source_account = []
        return Xdr.types.Operation(source_account, self.body)

    def xdr(self):
        """Packs and base64 encodes this :class:`Operation` as an XDR string.

        """
        op = Xdr.StellarXDRPacker()
        op.pack_Operation(self.to_xdr_object())
        return base64.b64encode(op.get_buffer())

    @staticmethod
    def to_xdr_amount(value):
        """Converts an amount to the appropriate value to send over the network
        as a part of an XDR object.

        Each asset amount is encoded as a signed 64-bit integer in the XDR
        structures. An asset amount unit (that which is seen by end users) is
        scaled down by a factor of ten million (10,000,000) to arrive at the
        native 64-bit integer representation. For example, the integer amount
        value 25,123,456 equals 2.5123456 units of the asset. This scaling
        allows for seven decimal places of precision in human-friendly amount
        units.

        This static method correctly multiplies the value by the scaling factor
        in order to come to the integer value used in XDR structures.

        See `Stellar's documentation on Asset Precision
        <https://www.stellar.org/developers/guides/concepts/assets.html#amount-precision-and-representation>`_
        for more information.

        :param str value: The amount to convert to an integer for XDR
            serialization.

        """
        if not isinstance(value, str):
            # FIXME: Raise better exception
            raise Exception("value must be a string")

        # throw exception if value * ONE has decimal places (it can't be
        # represented as int64)
        return int((Decimal(value) * ONE).to_integral_exact(
            context=Context(traps=[Inexact])))

    @staticmethod
    def from_xdr_amount(value):
        """Converts an amount from an XDR object into its appropriate integer
        representation.

        Each asset amount is encoded as a signed 64-bit integer in the XDR
        structures. An asset amount unit (that which is seen by end users) is
        scaled down by a factor of ten million (10,000,000) to arrive at the
        native 64-bit integer representation. For example, the integer amount
        value 25,123,456 equals 2.5123456 units of the asset. This scaling
        allows for seven decimal places of precision in human-friendly amount
        units.

        This static method correctly divides the value by the scaling factor in
        order to get the proper units of the asset.

        See `Stellar's documentation on Asset Precision
        <https://www.stellar.org/developers/guides/concepts/assets.html#amount-precision-and-representation>`_
        for more information.

        :param int value: The amount to convert to a string from an XDR int64
            amount.

        """
        return str(Decimal(value) / ONE)

    @classmethod
    def from_xdr(cls, xdr):
        """Create the appropriate :class:`Operation` subclass from the XDR
        structure.

        Decode an XDR base64 encoded string and create the appropriate
        :class:`Operation` object.

        :param str xdr: The XDR object to create an :class:`Operation` (or
            subclass) instance from.

        """
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
    """The :class:`CreateAccount` object, which represents a Create Account
    operation on Stellar's network.

    This operation creates and funds a new account with the specified starting
    balance.

    Threshold: Medium

    :param dict opts: A dict of options for creating this
        :class:`CreateAccount`. This class pulls a 'source', 'destination', and
        'starting_balance' via opts.

    """
    def __init__(self, opts):
        super(CreateAccount, self).__init__(opts)
        self.destination = opts.get('destination')
        self.starting_balance = opts.get('starting_balance')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`CreateAccount`.

        """
        destination = account_xdr_object(self.destination)

        create_account_op = Xdr.types.CreateAccountOp(
            destination, Operation.to_xdr_amount(self.starting_balance))
        self.body.type = Xdr.const.CREATE_ACCOUNT
        self.body.createAccountOp = create_account_op
        return super(CreateAccount, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`CreateAccount` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check(
            'account',
            op_xdr_object.body.createAccountOp.destination.ed25519).decode()
        starting_balance = Operation.from_xdr_amount(
            op_xdr_object.body.createAccountOp.startingBalance)

        return cls({
            'source': source,
            'destination': destination,
            'starting_balance': starting_balance,
        })


class Payment(Operation):
    """The :class:`Payment` object, which represents a Payment operation on
    Stellar's network.

    Sends an amount in a specific asset to a destination account.

    Threshold: Medium

    :param dict opts: A dict of options for creating this :class:`Payment`.
        This class pulls a 'source', 'destination', 'asset', and 'amount' via
        opts.

    """
    def __init__(self, opts):
        super(Payment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.asset = opts.get('asset')
        self.amount = opts.get('amount')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`Payment`.

        """
        asset = self.asset.to_xdr_object()
        destination = account_xdr_object(self.destination)

        amount = Operation.to_xdr_amount(self.amount)

        payment_op = Xdr.types.PaymentOp(destination, asset, amount)
        self.body.type = Xdr.const.PAYMENT
        self.body.paymentOp = payment_op
        return super(Payment, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`Payment` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check(
            'account',
            op_xdr_object.body.paymentOp.destination.ed25519).decode()
        asset = Asset.from_xdr_object(op_xdr_object.body.paymentOp.asset)
        amount = Operation.from_xdr_amount(op_xdr_object.body.paymentOp.amount)

        return cls({
            'source': source,
            'destination': destination,
            'asset': asset,
            'amount': amount,
        })


class PathPayment(Operation):
    """The :class:`PathPayment` object, which represents a PathPayment
    operation on Stellar's network.

    Sends an amount in a specific asset to a destination account through a path
    of offers. This allows the asset sent (e.g., 450 XLM) to be different from
    the asset received (e.g, 6 BTC).

    Threshold: Medium

    :param dict opts: A dict of options for creating this :class:`PathPayment`.
        This class pulls a 'source', 'destination', 'send_asset', 'send_max',
        'dest_asset', 'dest_amount', and 'path' via opts.

    """
    def __init__(self, opts):
        super(PathPayment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.send_asset = opts.get('send_asset')
        self.send_max = opts.get('send_max')
        self.dest_asset = opts.get('dest_asset')
        self.dest_amount = opts.get('dest_amount')
        self.path = opts.get('path')  # a list of paths/assets

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`PathPayment`.

        """
        destination = account_xdr_object(self.destination)
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment = Xdr.types.PathPaymentOp(
            send_asset, Operation.to_xdr_amount(self.send_max), destination,
            dest_asset, Operation.to_xdr_amount(self.dest_amount), path)
        self.body.type = Xdr.const.PATH_PAYMENT
        self.body.pathPaymentOp = path_payment
        return super(PathPayment, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`PathPayment` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check(
            'account',
            op_xdr_object.body.pathPaymentOp.destination.ed25519).decode()
        send_asset = Asset.from_xdr_object(
            op_xdr_object.body.pathPaymentOp.sendAsset)
        dest_asset = Asset.from_xdr_object(
            op_xdr_object.body.pathPaymentOp.destAsset)
        send_max = Operation.from_xdr_amount(
            op_xdr_object.body.pathPaymentOp.sendMax)
        dest_amount = Operation.from_xdr_amount(
            op_xdr_object.body.pathPaymentOp.destAmount)

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
    """The :class:`ChangeTrust` object, which represents a ChangeTrust
    operation on Stellar's network.

    Creates, updates, or deletes a trustline. For more on trustlines, please
    refer to the `assets documentation
    <https://www.stellar.org/developers/guides/concepts/assets.html>_`.

    Threshold: Medium

    :param dict opts: A dict of options for creating this :class:`ChangeTrust`.
        This class pulls a 'source', 'asset', and optionally a 'limit' via
        opts.

    """
    def __init__(self, opts):
        super(ChangeTrust, self).__init__(opts)
        self.line = opts.get('asset')
        if opts.get('limit') is not None:
            self.limit = opts.get('limit')
        else:
            self.limit = "922337203685.4775807"

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`ChangeTrust`.

        """
        line = self.line.to_xdr_object()
        limit = Operation.to_xdr_amount(self.limit)

        change_trust_op = Xdr.types.ChangeTrustOp(line, limit)
        self.body.type = Xdr.const.CHANGE_TRUST
        self.body.changeTrustOp = change_trust_op
        return super(ChangeTrust, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`ChangeTrust` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        line = Asset.from_xdr_object(op_xdr_object.body.changeTrustOp.line)
        limit = Operation.from_xdr_amount(
            op_xdr_object.body.changeTrustOp.limit)

        return cls({
            'source': source,
            'asset': line,
            'limit': limit
        })


class AllowTrust(Operation):
    """The :class:`AllowTrust` object, which represents a AllowTrust operation
    on Stellar's network.

    Updates the authorized flag of an existing trustline. This can only be
    called by the issuer of a trustline’s `asset
    <https://www.stellar.org/developers/guides/concepts/assets.html>`_.

    The issuer can only clear the authorized flag if the issuer has the
    AUTH_REVOCABLE_FLAG set. Otherwise, the issuer can only set the authorized
    flag.

    Threshold: Low

    :param dict opts: A dict of options for creating this :class:`AllowTrust`.
        This class pulls a 'source', 'trustor', 'asset_code', and 'authorize'
        via opts.

    """
    def __init__(self, opts):
        super(AllowTrust, self).__init__(opts)
        self.trustor = opts.get('trustor')
        self.asset_code = opts.get('asset_code')
        self.authorize = opts.get('authorize')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`AllowTrust`.

        """
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
        """Creates a :class:`AllowTrust` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()
        trustor = encode_check(
            'account',
            op_xdr_object.body.allowTrustOp.trustor.ed25519).decode()
        authorize = op_xdr_object.body.allowTrustOp.authorize

        asset_type = op_xdr_object.body.allowTrustOp.asset.type
        if asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            asset_code = (
                op_xdr_object.body.allowTrustOp.asset.assetCode4.decode())
        elif asset_type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12:
            asset_code = (
                op_xdr_object.body.allowTrustOp.asset.assetCode12.decode())
        else:
            # FIXME: Raise a better exception
            raise Exception

        return cls({
            'source': source,
            'trustor': trustor,
            'authorize': authorize,
            'asset_code': asset_code
        })


class SetOptions(Operation):
    """The :class:`SetOptions` object, which represents a SetOptions operation
    on Stellar's network.

    This operation sets the options for an account.

    For more information on the signing options, please refer to the `multi-sig
    doc <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.

    When updating signers or other thresholds, the threshold of this operation
    is high.

    Threshold: Medium or High

    :param dict opts: A dict of options for creating this :class:`SetOptions`.
        This class pulls several of the following depending on the option: a
        'source', 'inflation_dest', 'clear_flags', 'set_flags',
        'master_weight', 'low_threshold', 'med_threshold', 'high_threshold',
        'home_domain', 'signer_address', 'signer_type', 'signer_weight' via
        opts.

    """
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

        # FIXME: Clean up boolean logic - make these conditions more linear
        # (some of them depend on booleans already checked in earlier
        # statements)
        if self.signer_address is not None and self.signer_type is None:
            try:
                decode_check('account', self.signer_address)
            except DecodeError:
                raise Exception(
                    'Must be a valid strkey if not give signer_type')
            self.signer_type = 'ed25519PublicKey'

        signer_is_invalid_type = (
            self.signer_type is not None and
            self.signer_type not in ('ed25519PublicKey', 'hashX', 'preAuthTx'))

        if signer_is_invalid_type:
            # FIXME: Throw better exception
            raise Exception('invalid signer type.')

        signer_addr_has_valid_len = (
            self.signer_address is not None and len(self.signer_address) == 32)

        if (self.signer_type in ('hashX', 'preAuthTx')
                and not signer_addr_has_valid_len):
            # FIXME: Throw better exception
            raise Exception('hashX or preAuthTx Signer must be 32 bytes')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`SetOptions`.

        """
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

        req_signer_fields = (
            self.signer_address, self.signer_type, self.signer_weight)

        if all(signer_field is not None for signer_field in req_signer_fields):
            signer = [
                Xdr.types.Signer(
                    signer_key_xdr_object(
                        self.signer_type, self.signer_address),
                    self.signer_weight)
            ]
        else:
            signer = []

        set_options_op = Xdr.types.SetOptionsOp(
            inflation_dest, self.clear_flags, self.set_flags,
            self.master_weight, self.low_threshold, self.med_threshold,
            self.high_threshold, self.home_domain, signer)
        self.body.type = Xdr.const.SET_OPTIONS
        self.body.setOptionsOp = set_options_op
        return super(SetOptions, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`SetOptions` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        if not op_xdr_object.body.setOptionsOp.inflationDest:
            inflation_dest = None
        else:
            inflation_dest = encode_check(
                'account',
                op_xdr_object.body.setOptionsOp.inflationDest[0].ed25519).decode()

        clear_flags = op_xdr_object.body.setOptionsOp.clearFlags  # list
        set_flags = op_xdr_object.body.setOptionsOp.setFlags
        master_weight = op_xdr_object.body.setOptionsOp.masterWeight
        low_threshold = op_xdr_object.body.setOptionsOp.lowThreshold
        med_threshold = op_xdr_object.body.setOptionsOp.medThreshold
        high_threshold = op_xdr_object.body.setOptionsOp.highThreshold
        home_domain = op_xdr_object.body.setOptionsOp.homeDomain

        if op_xdr_object.body.setOptionsOp.signer:
            key = op_xdr_object.body.setOptionsOp.signer[0].key
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
            'signer_type': signer_type,
            'signer_weight': signer_weight
        })


class ManageOffer(Operation):
    """The :class:`ManageOffer` object, which represents a ManageOffer
    operation on Stellar's network.

    Creates, updates, or deletes an offer.

    If you want to create a new offer set Offer ID to 0.

    If you want to update an existing offer set Offer ID to existing offer ID.

    If you want to delete an existing offer set Offer ID to existing offer ID
    and set Amount to 0.

    Threshold: Medium

    :param dict opts: A dict of options for creating this :class:`ManageOffer`.
        This class pulls several of the following from opts: 'source',
        'selling', 'buying', 'amount', 'price', 'offer_id'.

    """
    def __init__(self, opts):
        super(ManageOffer, self).__init__(opts)
        self.selling = opts.get('selling')  # Asset
        self.buying = opts.get('buying')  # Asset
        self.amount = opts.get('amount')
        self.price = opts.get('price')
        self.offer_id = opts.get('offer_id', 0)

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`ManageOffer`.

        """
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = best_r(self.price)
        price = Xdr.types.Price(price['n'], price['d'])

        amount = Operation.to_xdr_amount(self.amount)

        manage_offer_op = Xdr.types.ManageOfferOp(
            selling, buying, amount, price, self.offer_id)
        self.body.type = Xdr.const.MANAGE_OFFER
        self.body.manageOfferOp = manage_offer_op
        return super(ManageOffer, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`ManageOffer` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        selling = Asset.from_xdr_object(
            op_xdr_object.body.manageOfferOp.selling)
        buying = Asset.from_xdr_object(op_xdr_object.body.manageOfferOp.buying)
        amount = Operation.from_xdr_amount(
            op_xdr_object.body.manageOfferOp.amount)

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
    """The :class:`CreatePassiveOffer` object, which represents a
    CreatePassiveOffer operation on Stellar's network.

    A passive offer is an offer that does not act on and take a reverse offer
    of equal price. Instead, they only take offers of lesser price. For
    example, if an offer exists to buy 5 BTC for 30 XLM, and you make a passive
    offer to buy 30 XLM for 5 BTC, your passive offer does not take the first
    offer.

    Note that regular offers made later than your passive offer can act on and
    take your passive offer, even if the regular offer is of the same price as
    your passive offer.

    Passive offers allow market makers to have zero spread. If you want to
    trade EUR for USD at 1:1 price and USD for EUR also at 1:1, you can create
    two passive offers so the two offers don’t immediately act on each other.

    Once the passive offer is created, you can manage it like any other offer
    using the manage offer operation - see :class:`ManageOffer` for more
    details.

    :param dict opts: A dict of options for creating this
        :class:`CreatePassiveOffer`.  This class pulls several of the following
        from opts: 'source', 'selling', 'buying', 'amount', 'price'.

    """
    def __init__(self, opts):
        super(CreatePassiveOffer, self).__init__(opts)
        self.selling = opts.get('selling')
        self.buying = opts.get('buying')
        self.amount = opts.get('amount')
        self.price = opts.get('price')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`CreatePassiveOffer`.

        """
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        # FIXME: This assume that self.price is always an integer, however it
        # could be a tuple/dict of a numerator and denominator. This should do
        # type checking (similar to the JS library).
        price = best_r(self.price)
        price = Xdr.types.Price(price['n'], price['d'])

        amount = Operation.to_xdr_amount(self.amount)

        create_passive_offer_op = Xdr.types.CreatePassiveOfferOp(
            selling, buying, amount, price)
        self.body.type = Xdr.const.CREATE_PASSIVE_OFFER
        self.body.createPassiveOfferOp = create_passive_offer_op
        return super(CreatePassiveOffer, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`CreatePassiveOffer` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        selling = Asset.from_xdr_object(
            op_xdr_object.body.createPassiveOfferOp.selling)
        buying = Asset.from_xdr_object(
            op_xdr_object.body.createPassiveOfferOp.buying)
        amount = Operation.from_xdr_amount(
            op_xdr_object.body.createPassiveOfferOp.amount)

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
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    :param dict opts: A dict of options for creating this
        :class:`AccountMerge`.  This class pulls several of the following from
        opts: 'source', 'destination'

    """
    def __init__(self, opts):
        super(AccountMerge, self).__init__(opts)
        self.destination = opts.get('destination')

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`AccountMerge`.

        """
        destination = account_xdr_object(self.destination)

        self.body.type = Xdr.const.ACCOUNT_MERGE
        self.body.destination = destination
        return super(AccountMerge, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        destination = encode_check(
            'account', op_xdr_object.body.destination.ed25519).decode()

        return cls({
            'source': source,
            'destination': destination
        })


class Inflation(Operation):
    """The :class:`Inflation` object, which represents a
    Inflation operation on Stellar's network.

    This operation runs inflation.

    Threshold: Low

    :param dict opts: A dict of options for creating this
        :class:`Inflation`.  This class pulls several of the following from
        opts: 'source'.

    """
    def __init__(self, opts):
        super(Inflation, self).__init__(opts)

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`Inflation`.

        """
        self.body.type = Xdr.const.INFLATION
        return super(Inflation, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`Inflation` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()
        return cls({'source': source})


class ManageData(Operation):
    """The :class:`ManageData` object, which represents a
    ManageData operation on Stellar's network.

    Allows you to set,modify or delete a Data Entry (name/value pair) that is
    attached to a particular account. An account can have an arbitrary amount
    of DataEntries attached to it. Each DataEntry increases the minimum balance
    needed to be held by the account.

    DataEntries can be used for application specific things. They are not used
    by the core Stellar protocol.

    Threshold: Medium

    :param dict opts: A dict of options for creating this :class:`ManageData`.
        This class pulls several of the following from opts: 'source',
        'data_name', 'data_value'.

    """
    def __init__(self, opts):
        super(ManageData, self).__init__(opts)
        self.data_name = opts.get('data_name')
        self.data_value = opts.get('data_value')

        valid_data_name_len = len(self.data_name) <= 64
        valid_data_val_len = (
            self.data_value is None or len(self.data_value) <= 64)

        if not valid_data_name_len or not valid_data_val_len:
            raise XdrLengthError(
                "Data or value should be <= 64 bytes (ascii encoded).")

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`ManageData`.

        """
        data_name = bytearray(self.data_name, encoding='utf-8')

        if self.data_value is not None:
            if isinstance(self.data_value, bytes):
                data_value = [bytearray(self.data_value)]
            else:
                data_value = [bytearray(self.data_value, 'utf-8')]
        else:
            data_value = []
        manage_data_op = Xdr.types.ManageDataOp(data_name, data_value)
        self.body.type = Xdr.const.MANAGE_DATA
        self.body.manageDataOp = manage_data_op
        return super(ManageData, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`ManageData` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        data_name = op_xdr_object.body.manageDataOp.dataName.decode()

        if op_xdr_object.body.manageDataOp.dataValue:
            data_value = op_xdr_object.body.manageDataOp.dataValue[0]
        else:
            data_value = None
        return cls({
            'source': source,
            'data_name': data_name,
            'data_value': data_value
        })
