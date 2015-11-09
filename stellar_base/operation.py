# coding:utf-8
from .stellarxdr import StellarXDR_pack as Xdr
from .utils import account_xdr_object


class Operation(object):
    """follow the specific . the source can be none.
    """

    def __init__(self, opts):
        assert type(opts) is dict

        self.source = opts.get('source')
        self.body = Xdr.nullclass

    def to_xdr_object(self):
        try:
            source_account = [account_xdr_object(self.source)]
        except TypeError:
            source_account = []
        return Xdr.types.Operation(source_account, self.body)


class CreateAccount(Operation):
    def __init__(self, opts):
        super(CreateAccount, self).__init__(opts)
        self.destination = opts.get('destination')
        self.starting_balance = opts.get('starting_balance')

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)

        create_account_op = Xdr.types.CreateAccountOp(destination, self.starting_balance)
        self.body.type = Xdr.const.CREATE_ACCOUNT
        self.body.createAccountOp = create_account_op
        return super(CreateAccount, self).to_xdr_object()


class Payment(Operation):
    def __init__(self, opts):
        super(Payment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.asset = opts.get('asset')
        self.amount = opts.get('amount')

    def to_xdr_object(self):
        asset = self.asset.to_xdr_object()
        destination = account_xdr_object(self.destination)

        payment_op = Xdr.types.PaymentOp(destination, asset, self.amount)
        self.body.type = Xdr.const.PAYMENT
        self.body.paymentOp = payment_op
        return super(Payment, self).to_xdr_object()


class PathPayment(Operation):
    def __init__(self, opts):
        super(PathPayment, self).__init__(opts)
        self.destination = opts.get('destination')
        self.send_asset = opts.get('send_asset')
        self.send_max = opts.get('send_max')
        self.dest_asset = opts.get('dest_asset')
        self.dest_amount = opts.get('dest_amount')
        self.path = opts.get('path')

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()

        path_payment = Xdr.types.PathPaymentOp(send_asset, self.send_max, destination,
                                               dest_asset, self.dest_amount, self.path)
        self.body.type = Xdr.const.PATH_PAYMENT
        self.body.pathPayment = path_payment
        return super(PathPayment, self).to_xdr_object()


class ChangeTrust(Operation):
    def __init__(self, opts):
        super(ChangeTrust, self).__init__(opts)
        self.line = opts.get('asset')
        try:
            self.limit = int(opts.get('limit'))
        except TypeError:
            self.limit = 9223372036854775807

    def to_xdr_object(self):
        line = self.line.to_xdr_object()

        change_trust_op = Xdr.types.ChangeTrustOp(line, self.limit)
        self.body.type = Xdr.const.CHANGE_TRUST
        self.body.changeTrustOp = change_trust_op
        return super(ChangeTrust, self).to_xdr_object()


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
        asset_code = self.asset_code + '\x00' * pad_length
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


class SetOptions(Operation):
    def __init__(self, opts):
        super(SetOptions, self).__init__(opts)
        self.inflation_dest = opts.get('inflation_dest') or None
        self.clear_flags = opts.get('clear_flags') or None
        self.set_flags = opts.get('set_flags') or None
        self.master_weight = opts.get('master_weight') or None
        self.low_threshold = opts.get('low_threshold') or None
        self.med_threshold = opts.get('med_threshold') or None
        self.high_threshold = opts.get('high_threshold') or None
        self.home_domain = opts.get('home_domain') or None
        try:
            self.signer_address = opts['signer_address']
            self.signer_weight = opts['signer_weight']
        except KeyError:
            self.signer_address = None

    def to_xdr_object(self):
        if self.inflation_dest is not None:
            inflation_dest = account_xdr_object(self.inflation_dest)
        else:
            inflation_dest = None
        if self.signer_address is not None:
            signer = Xdr.types.Signer(account_xdr_object(self.signer_address), self.signer_weight)
        else:
            signer = None

        set_options_op = Xdr.types.SetOptionsOp(inflation_dest, self.clear_flags, self.set_flags,
                                                self.master_weight, self.low_threshold, self.med_threshold,
                                                self.high_threshold, self.home_domain, signer)
        self.body.type = Xdr.const.SET_OPTIONS
        self.body.setOptionsOp = set_options_op
        return super(SetOptions, self).to_xdr_object()


class ManageOffer(Operation):
    def __init__(self, opts):
        super(ManageOffer, self).__init__(opts)
        self.selling = opts.get('selling')
        self.buying = opts.get('buying')
        self.amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        self.price = dict(n=None, d=None)
        self.offer_id = opts.get('offerId')

    def to_xdr_object(self):
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = Xdr.types.Price(n=self.price['n'], d=self.price['d'])

        manage_offer_op = Xdr.types.ManageOfferOp(selling, buying, self.amount, price, self.offer_id)
        self.body.type = Xdr.const.MANAGE_OFFER
        self.body.changeTrustOP = manage_offer_op
        return super(ManageOffer, self).to_xdr_object()


class CreatePassiveOffer(Operation):
    def __init__(self, opts):
        super(CreatePassiveOffer, self).__init__(opts)
        self.selling = opts.get('selling')
        self.buying = opts.get('buying')
        self.amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        self.price = dict(n=None, d=None)

    def to_xdr_object(self):
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = Xdr.types.Price(self.price['n'], self.price['d'])

        create_passive_offer_op = Xdr.types.CreatePassiveOfferOp(selling, buying, self.amount, price)
        self.body.type = Xdr.const.CREATE_PASSIVE_OFFER
        self.body.createPassiveOfferOp = create_passive_offer_op
        return super(CreatePassiveOffer, self).to_xdr_object()


class AccountMerge(Operation):
    def __init__(self, opts):
        super(AccountMerge, self).__init__(opts)
        self.destination = opts.get('destination')

    def to_xdr_object(self):
        destination = account_xdr_object(self.destination)

        self.body.type = Xdr.const.ACCOUNT_MERGE
        self.body.accountMerge = destination
        return super(AccountMerge, self).to_xdr_object()


class Inflation(Operation):
    def __init__(self, opts):
        super(Inflation, self).__init__(opts)

    def to_xdr_object(self):
        self.body.type = Xdr.const.INFLATION
        return super(Inflation, self).to_xdr_object()
