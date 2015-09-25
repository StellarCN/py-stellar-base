# coding:utf-8
from .stellarxdr import StellarXDR_pack as Xdr
from .keypair import KeyPair


class Operation(object):

    @staticmethod
    def create_account(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []

        destination = KeyPair.from_address(opts.get('destination')).account_id()
        starting_balance = opts.startingBalance  # int64

        create_account_op = Xdr.types.CreateAccountOp(destination, starting_balance)
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_ACCOUNT
        body.createAccountOp = create_account_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def payment(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        destination = KeyPair.from_address(opts.get('destination')).account_id()
        asset = opts.get('asset').to_xdr_object()
        amount = opts.get('amount')

        payment_op = Xdr.types.PaymentOp(destination, asset, amount)
        body = Xdr.nullclass()
        body.type = Xdr.const.PAYMENT
        body.paymentOp = payment_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def path_payment(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        destination = KeyPair.from_address(opts.destination).account_id()
        send_asset = opts.get('send_asset').to_xdr_object()
        send_max = opts.get('send_max')
        dest_asset = opts.get('dest_asset').to_xdr_object()
        dest_amount = opts.get('dest_amount')
        try:
            path = opts.get('path')
        except KeyError:
            path = None

        path_payment = Xdr.types.PathPaymentOp(send_asset, send_max, destination,
                                               dest_asset, dest_amount, path)
        body = Xdr.nullclass()
        body.type = Xdr.const.PATH_PAYMENT
        body.pathPayment = path_payment
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def change_trust(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        line = opts.get('asset').to_xdr_object()
        try:
            limit = int(opts.get('limit'))
        except TypeError:
            limit = 9223372036854775807
        limit = int(limit)

        change_trust_op = Xdr.types.ChangeTrustOp(line, limit)
        body = Xdr.nullclass()
        body.type = Xdr.const.CHANGE_TRUST
        body.changeTrustOP = change_trust_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def allow_trust(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        trustor = KeyPair.from_address(opts.get('trustor')).account_id()
        asset_code = opts.get('asset_code')
        length = len(asset_code)
        assert length <= 12
        pad_length = 4 - length if length <= 4 else 12 - length
        asset_code += '\x00' * pad_length

        asset = Xdr.nullclass()
        if length == 4:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            asset.assetCode4 = asset_code
        else:
            asset.type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            asset.assetCode12 = asset_code
        authorize = opts.get('authorize')

        allow_trust_op = Xdr.types.AllowTrustOp(trustor, asset, authorize)
        body = Xdr.nullclass()
        body.type = Xdr.const.ALLOW_TRUST
        body.changeTrustOP = allow_trust_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def set_options(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        try:
            inflation_dest = KeyPair.from_address(opts.get('inflationDest')).account_id()
        except KeyError:
            inflation_dest = None

        clear_flags = opts.get('clear_flags') or None
        set_flags = opts.get('set_flags') or None
        master_weight = opts.get('master_weight') or None
        low_threshold = opts.get('lowThreshold') or None
        med_threshold = opts.get('medThreshold') or None
        high_threshold = opts.get('high_threshold') or None
        home_domain = opts.get('home_domain') or None

        try:
            signer = Xdr.types.Signer(KeyPair.from_address(opts.get('signer').address).account_id(),
                                      weight=opts.get('signer').weight)
        except KeyError:
            signer = None

        set_options_op = Xdr.types.SetOptionsOp(inflation_dest, clear_flags, set_flags,
                                                master_weight, low_threshold, med_threshold,
                                                high_threshold, home_domain, signer)
        body = Xdr.nullclass()
        body.type = Xdr.const.SET_OPTIONS
        body.setOptionsOp = set_options_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def manage_offer(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        selling = opts.get('selling').to_xdr_object()
        buying = opts.get('buying').to_xdr_object()
        amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        price = Xdr.types.Price(n=None, d=None)
        offer_id = opts.get('offerId')

        manage_offer_op = Xdr.types.ManageOfferOp(selling, buying, amount, price, offer_id)
        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_OFFER
        body.changeTrustOP = manage_offer_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def create_passive_offer(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        selling = opts.get('selling').to_xdr_object()
        buying = opts.get('buying').to_xdr_object()
        amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        price = Xdr.types.Price(n=None, d=None)

        create_passive_offer_op = Xdr.types.CreatePassiveOfferOp(selling, buying, amount, price)
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_PASSIVE_OFFER
        body.createPassiveOfferOp = create_passive_offer_op
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def account_merge(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []
        destination = KeyPair.from_address(opts.get('destination')).account_id()

        body = Xdr.nullclass()
        body.type = Xdr.const.ACCOUNT_MERGE
        body.accountMerge = destination
        return Xdr.types.Operation(source_account, body)

    @staticmethod
    def inflation(opts):
        try:
            source_account = [KeyPair.from_address(opts.get('source')).account_id()]
        except TypeError:
            source_account = []

        body = Xdr.nullclass()
        body.type = Xdr.const.INFLATION
        return Xdr.types.Operation(source_account, body)
