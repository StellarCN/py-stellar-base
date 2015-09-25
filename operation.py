# coding:utf-8
from .stellarxdr import StellarXDR_pack as xdr
from .keypair import KeyPair


class Operation(object):

    @staticmethod
    def createAccount(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []

        destination = KeyPair.fromAddress(opts.get('destination')).accountId()
        startingBalance = opts.startingBalance # int64

        createAccountOp = xdr.types.CreateAccountOp(destination, startingBalance)
        body = xdr.nullclass()
        body.type = xdr.const.CREATE_ACCOUNT
        body.createAccountOp = createAccountOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def payment(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        destination = KeyPair.fromAddress(opts.get('destination')).accountId()
        asset = opts.get('asset').toXdrObject()
        amount = opts.get('amount')

        paymentOp = xdr.types.PaymentOp(destination, asset, amount)
        body = xdr.nullclass()
        body.type =xdr.const.PAYMENT
        body.paymentOp = paymentOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def pathPayment(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        destination = KeyPair.fromAddress(opts.destination).accountId()
        sendAsset = opts.get('sendAsset').toXdrObject()
        sendMax = opts.get('sendMax')
        destAsset = opts.get('destAsset').toXdrObject()
        destAmount = opts.get('destAmount')
        try:
            path = opts.get('path')
        except KeyError:
            path = None

        pathPayment = xdr.types.PathPaymentOp(sendAsset, sendMax, destination, 
                                              destAsset, destAmount, path)
        body = xdr.nullclass()
        body.type = xdr.const.PATH_PAYMENT
        body.pathPayment = pathPayment
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def changeTrust(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        line = opts.get('asset').toXdrObject()
        try:
            limit = opts.get('limit')
        except:
            limit = "9223372036854775807"
        limit = int(limit)

        changeTrustOP = xdr.types.ChangeTrustOp(line, limit)
        body = xdr.nullclass()
        body.type = xdr.const.CHANGE_TRUST
        body.changeTrustOP = changeTrustOP
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def allowTrust(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        trustor = KeyPair.fromAddress(opts.get('trustor')).accountId()
        assetCode = opts.get('assetCode')
        length = len(assetCode)
        assert length <=12
        padLength = 4 - length if length <= 4 else 12 - length
        assetCode = assetCode + '\x00' * padLength

        asset  = xdr.nullclass()
        if length == 4:
            asset.type = xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            asset.assetCode4 = assetCode
        else:
            asset.type = xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            asset.assetCode12 = assetCode
        authorize = opts.get('authorize')

        allowTrustOp = xdr.types.AllowTrustOp(trustor, asset, authorize)
        body = xdr.nullclass()
        body.type = xdr.const.ALLOW_TRUST
        body.changeTrustOP = allowTrustOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def setOptions(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        try:
            inflationDest = KeyPair.fromAddress(opts.get('inflationDest')).accountId()
        except KeyError:
            inflationDest = None

        clearFlags = opts.get('clearFlags') or None
        setFlags = opts.get('setFlags') or None
        masterWeight = opts.get('masterWeight') or None
        lowThreshold = opts.get('lowThreshold') or None
        medThreshold = opts.get('medThreshold') or None
        highThreshold = opts.get('highThreshold') or None
        homeDomain = opts.get('homeDomain') or None

        try:
            signer = xdr.types.Signer(KeyPair.fromAddress(opts.get('signer').address).accountId(),
                                       weight=opts.get('signer').weight)
        except KeyError:
            signer = None

        setOptionsOp = xdr.types.SetOptionsOp(inflationDest, clearFlags, setFlags,
                                              masterWeight, lowThreshold, medThreshold,
                                              highThreshold, homeDomain, signer)
        body = xdr.nullclass()
        body.type = xdr.const.SET_OPTIONS
        body.setOptionsOp = setOptionsOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def manageOffer(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        selling = opts.get('selling').toXdrObject()
        buying = opts.get('buying').toXdrObject()
        amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        price = xdr.types.Price(n=None, d=None)
        offerId = opts.get('offerId')

        manageOfferOp = xdr.types.ManageOfferOp(selling, buying, amount, price, offerId)
        body = xdr.nullclass()
        body.type = xdr.const.MANAGE_OFFER
        body.changeTrustOP = manageOfferOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def createPassiveOffer(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        selling = opts.get('selling').toXdrObject()
        buying = opts.get('buying').toXdrObject()
        amount = opts.get('amount')
        # TODO
        # approx = best_r(opts.price)
        price = xdr.types.Price(n=None,d=None)

        createPassiveOfferOp = xdr.types.CreatePassiveOfferOp(selling, buying, amount, price)
        body = xdr.nullclass()
        body.type = xdr.const.CREATE_PASSIVE_OFFER
        body.createPassiveOfferOp = createPassiveOfferOp
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def accountMerge(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []
        destination = KeyPair.fromAddress(opts.get('destination')).accountId()

        body = xdr.nullclass()
        body.type = xdr.const.ACCOUNT_MERGE
        body.accountMerge = destination
        return xdr.types.Operation(sourceAccount, body)

    @staticmethod
    def inflation(opts):
        try:
            sourceAccount = [KeyPair.fromAddress(opts.get('source')).accountId()]
        except:
            sourceAccount = []

        body = xdr.nullclass()
        body.type = xdr.const.INFLATION
        return xdr.types.Operation(sourceAccount, body)


