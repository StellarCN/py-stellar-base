# -*- coding: utf-8 -*-

import base64
import decimal
from decimal import Context, Decimal, Inexact

from .asset import Asset
from .stellarxdr import Xdr
from .utils import (account_xdr_object, best_rational_approximation as best_r,
                    division, encode_check, signer_key_xdr_object,
                    is_valid_address, convert_hex_to_bytes)
from .exceptions import StellarAddressInvalidError, NotValidParamError

ONE = Decimal(10 ** 7)


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

    :param str source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    def __init__(self, source=None):
        self.source = source
        self.body = Xdr.nullclass()

    def __eq__(self, other):
        return self.xdr() == other.xdr()

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`Operation`.

        """
        try:
            source_account = [account_xdr_object(self.source)]
        except StellarAddressInvalidError:
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
            raise NotValidParamError("Value of type '{}' must be of type String, but got {}".format(value, type(value)))

        # throw exception if value * ONE has decimal places (it can't be
        # represented as int64)
        try:
            amount = int((Decimal(value) * ONE).to_integral_exact(context=Context(traps=[Inexact])))
        except decimal.Inexact:
            raise NotValidParamError("Value of '{}' must have at most 7 digits after the decimal.".format(value))
        except decimal.InvalidOperation:
            raise NotValidParamError("Value of '{}' must represent a positive number.".format(value))
        return amount

    @staticmethod
    def to_xdr_price(price):
        if isinstance(price, dict):
            if not ('n' in price and 'd' in price):
                raise NotValidParamError(
                    "You need pass `price` params as `str` or `{'n': numerator, 'd': denominator}`"
                )
        else:
            price = best_r(price)
        return price

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
    def type_code(cls):
        pass

    @classmethod
    def from_xdr_object(cls, operation):
        for sub_cls in cls.__subclasses__():
            if sub_cls.type_code() == operation.type:
                return sub_cls.from_xdr_object(operation)
        raise NotImplementedError("Operation of type={} is not implemented"
                                  ".".format(operation.type))

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
        return cls.from_xdr_object(op)


class CreateAccount(Operation):
    """The :class:`CreateAccount` object, which represents a Create Account
    operation on Stellar's network.

    This operation creates and funds a new account with the specified starting
    balance.

    Threshold: Medium

    :param str destination: Destination account ID to create an account for.
    :param str starting_balance: Amount in XLM the account should be
        funded for. Must be greater than the [reserve balance amount]
        (https://www.stellar.org/developers/learn/concepts/fees.html).
    :param str source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.CREATE_ACCOUNT

    def __init__(self, destination, starting_balance, source=None):
        super(CreateAccount, self).__init__(source)
        self.destination = destination
        self.starting_balance = starting_balance

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

        return cls(
            source=source,
            destination=destination,
            starting_balance=starting_balance,
        )


class Payment(Operation):
    """The :class:`Payment` object, which represents a Payment operation on
    Stellar's network.

    Sends an amount in a specific asset to a destination account.

    Threshold: Medium

    :param str destination: The destination account ID.
    :param Asset asset: The asset to send.
    :param str amount: The amount to send.
    :param str source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.PAYMENT

    def __init__(self, destination, asset, amount, source=None):
        super(Payment, self).__init__(source)
        self.destination = destination
        self.asset = asset
        self.amount = amount

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

        return cls(
            source=source,
            destination=destination,
            asset=asset,
            amount=amount,
        )


class PathPayment(Operation):
    """The :class:`PathPayment` object, which represents a PathPayment
    operation on Stellar's network.

    Sends an amount in a specific asset to a destination account through a path
    of offers. This allows the asset sent (e.g., 450 XLM) to be different from
    the asset received (e.g, 6 BTC).

    Threshold: Medium

    :param str destination: The destination account to send to.
    :param Asset send_asset: The asset to pay with.
    :param str send_max: The maximum amount of send_asset to send.
    :param Asset dest_asset: The asset the destination will receive.
    :param str dest_amount: The amount the destination receives.
    :param list path: A list of Asset objects to use as the path.
    :param str source: The source account for the payment. Defaults to the
        transaction's source account.
    """

    @classmethod
    def type_code(cls):
        return Xdr.const.PATH_PAYMENT

    def __init__(self,
                 destination,
                 send_asset,
                 send_max,
                 dest_asset,
                 dest_amount,
                 path,
                 source=None):
        super(PathPayment, self).__init__(source)
        self.destination = destination
        self.send_asset = send_asset
        self.send_max = send_max
        self.dest_asset = dest_asset
        self.dest_amount = dest_amount
        self.path = path  # a list of paths/assets

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

        return cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path)


class ChangeTrust(Operation):
    """The :class:`ChangeTrust` object, which represents a ChangeTrust
    operation on Stellar's network.

    Creates, updates, or deletes a trustline. For more on trustlines, please
    refer to the `assets documentation
    <https://www.stellar.org/developers/guides/concepts/assets.html>_`.

    Threshold: Medium

    :param Asset asset: The asset for the trust line.
    :param str limit: The limit for the asset, defaults to max int64.
        If the limit is set to "0" it deletes the trustline.
    :param str source: The source account (defaults to transaction source).

    """
    default_limit = "922337203685.4775807"

    @classmethod
    def type_code(cls):
        return Xdr.const.CHANGE_TRUST

    def __init__(self, asset, limit=None, source=None):
        super(ChangeTrust, self).__init__(source)
        self.line = asset
        self.limit = limit or self.default_limit

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

        return cls(source=source, asset=line, limit=limit)


class AllowTrust(Operation):
    """The :class:`AllowTrust` object, which represents a AllowTrust operation
    on Stellar's network.

    Updates the authorized flag of an existing trustline. This can only be
    called by the issuer of a trustline's `asset
    <https://www.stellar.org/developers/guides/concepts/assets.html>`_.

    The issuer can only clear the authorized flag if the issuer has the
    AUTH_REVOCABLE_FLAG set. Otherwise, the issuer can only set the authorized
    flag.

    Threshold: Low

    :param str trustor: The trusting account (the one being authorized)
    :param str asset_code: The asset code being authorized.
    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.ALLOW_TRUST

    def __init__(self, trustor, asset_code, authorize, source=None):
        super(AllowTrust, self).__init__(source)
        self.trustor = trustor
        self.asset_code = asset_code
        self.authorize = authorize

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
            raise NotImplementedError(
                "Operation of asset_type={} is not implemented"
                ".".format(asset_type.type))

        return cls(
            source=source,
            trustor=trustor,
            authorize=authorize,
            asset_code=asset_code)


class SetOptions(Operation):
    """The :class:`SetOptions` object, which represents a SetOptions operation
    on Stellar's network.

    This operation sets the options for an account.

    For more information on the signing options, please refer to the `multi-sig
    doc <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.

    When updating signers or other thresholds, the threshold of this operation
    is high.

    Threshold: Medium or High

    :param str inflation_dest: Set this account ID as the account's inflation destination.
    :param int clear_flags: Bitmap integer for which account flags to clear.
    :param int set_flags: Bitmap integer for which account flags to set.
    :param int master_weight: The master key weight.
    :param int low_threshold: The sum weight for the low threshold.
    :param int med_threshold: The sum weight for the medium threshold.
    :param int high_threshold: The sum weight for the high threshold.
    :param str home_domain: sets the home domain used for reverse federation lookup.
    :param signer_address: signer
    :type signer_address: str, bytes
    :param str signer_type: The type of signer, it should be 'ed25519PublicKey',
        'hashX' or 'preAuthTx'
    :param int signer_weight: The weight of the new signer (0 to delete or 1-255)
    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.SET_OPTIONS

    def __init__(self,
                 inflation_dest=None,
                 clear_flags=None,
                 set_flags=None,
                 master_weight=None,
                 low_threshold=None,
                 med_threshold=None,
                 high_threshold=None,
                 home_domain=None,
                 signer_address=None,
                 signer_type=None,
                 signer_weight=None,
                 source=None):
        super(SetOptions, self).__init__(source)
        self.inflation_dest = inflation_dest
        self.clear_flags = clear_flags
        self.set_flags = set_flags
        self.master_weight = master_weight
        self.low_threshold = low_threshold
        self.med_threshold = med_threshold
        self.high_threshold = high_threshold
        if isinstance(home_domain, str):
            self.home_domain = bytearray(home_domain, encoding='utf-8')
        else:
            self.home_domain = home_domain
        self.signer_address = signer_address
        self.signer_type = signer_type
        self.signer_weight = signer_weight

        if self.signer_address is not None and self.signer_type is None:
            try:
                is_valid_address(self.signer_address)
            except StellarAddressInvalidError:
                raise StellarAddressInvalidError('Must be a valid stellar address if not give signer_type')
            self.signer_type = 'ed25519PublicKey'

        signer_is_invalid_type = (
                self.signer_type is not None and
                self.signer_type not in ('ed25519PublicKey', 'hashX', 'preAuthTx'))

        if signer_is_invalid_type:
            raise NotValidParamError('Invalid signer type, sign_type should '
                                     'be ed25519PublicKey, hashX or preAuthTx')

        if self.signer_type in ('hashX', 'preAuthTx'):
            self.signer_address = convert_hex_to_bytes(self.signer_address)

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

        req_signer_fields = (self.signer_address, self.signer_type,
                             self.signer_weight)

        if all(signer_field is not None for signer_field in req_signer_fields):
            signer = [
                Xdr.types.Signer(
                    signer_key_xdr_object(self.signer_type,
                                          self.signer_address),
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
                'account', op_xdr_object.body.setOptionsOp.inflationDest[0]
                    .ed25519).decode()

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

        return cls(
            source=source,
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            signer_address=signer_address,
            signer_type=signer_type,
            signer_weight=signer_weight)


class ManageOffer(Operation):
    """The :class:`ManageOffer` object, which represents a ManageOffer
    operation on Stellar's network.

    Creates, updates, or deletes an offer.

    If you want to create a new offer set Offer ID to 0.

    If you want to update an existing offer set Offer ID to existing offer ID.

    If you want to delete an existing offer set Offer ID to existing offer ID
    and set Amount to 0.

    Threshold: Medium

    :param Asset selling: What you're selling.
    :param Asset buying: What you're buying.
    :param str amount: The total amount you're selling. If 0,
        deletes the offer.
    :param price: Price of 1 unit of `selling` in
        terms of `buying`.
    :type price: str, dict
    :param int offer_id: If `0`, will create a new offer (default). Otherwise,
        edits an existing offer.
    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.MANAGE_OFFER

    def __init__(self, selling, buying, amount, price, offer_id=0,
                 source=None):
        super(ManageOffer, self).__init__(source)
        self.selling = selling  # Asset
        self.buying = buying  # Asset
        self.amount = amount
        self.price = price
        self.offer_id = offer_id

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`ManageOffer`.

        """
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = Operation.to_xdr_price(self.price)
        price = Xdr.types.Price(price['n'], price['d'])

        amount = Operation.to_xdr_amount(self.amount)

        manage_offer_op = Xdr.types.ManageOfferOp(selling, buying, amount,
                                                  price, self.offer_id)
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

        return cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id)


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
    two passive offers so the two offers don't immediately act on each other.

    Once the passive offer is created, you can manage it like any other offer
    using the manage offer operation - see :class:`ManageOffer` for more
    details.

    :param Asset selling: What you're selling.
    :param Asset buying: What you're buying.
    :param str amount: The total amount you're selling. If 0,
        deletes the offer.
    :param price: Price of 1 unit of `selling` in
        terms of `buying`.
    :type price: str, dict
    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.CREATE_PASSIVE_OFFER

    def __init__(self, selling, buying, amount, price, source=None):
        super(CreatePassiveOffer, self).__init__(source)
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`CreatePassiveOffer`.

        """
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        price = Operation.to_xdr_price(self.price)
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
        return cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price)


class AccountMerge(Operation):
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    :param str destination: Destination to merge the source account into.
    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.ACCOUNT_MERGE

    def __init__(self, destination, source=None):
        super(AccountMerge, self).__init__(source)
        self.destination = destination

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

        return cls(source=source, destination=destination)


class Inflation(Operation):
    """The :class:`Inflation` object, which represents a
    Inflation operation on Stellar's network.

    This operation runs inflation.

    Threshold: Low

    :param str source: The source account (defaults to transaction source).

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.INFLATION

    def __init__(self, source=None):
        super(Inflation, self).__init__(source)

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
        return cls(source=source)


class ManageData(Operation):
    """The :class:`ManageData` object, which represents a
    ManageData operation on Stellar's network.

    Allows you to set, modify or delete a Data Entry (name/value pair) that is
    attached to a particular account. An account can have an arbitrary amount
    of DataEntries attached to it. Each DataEntry increases the minimum balance
    needed to be held by the account.

    DataEntries can be used for application specific things. They are not used
    by the core Stellar protocol.

    Threshold: Medium

    :param str data_name: The name of the data entry.
    :param data_value: The value of the data entry.
    :type data_value: str, bytes, None
    :param str source: The optional source account.

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.MANAGE_DATA

    def __init__(self, data_name, data_value, source=None):
        super(ManageData, self).__init__(source)
        self.data_name = data_name
        self.data_value = data_value

        valid_data_name_len = len(self.data_name) <= 64
        valid_data_val_len = (self.data_value is None
                              or len(self.data_value) <= 64)

        if not valid_data_name_len or not valid_data_val_len:
            raise NotValidParamError(
                "Data and value should be <= 64 bytes (ascii encoded).")

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
        return cls(source=source, data_name=data_name, data_value=data_value)


class BumpSequence(Operation):
    """The :class:`BumpSequence` object, which represents a
    BumpSequence operation on Stellar's network.

    Only available in protocol version 10 and above

    Bump sequence allows to bump forward the sequence number of the source account of the
    operation, allowing to invalidate any transactions with a smaller sequence number.
    If the specified bumpTo sequence number is greater than the source account’s sequence number,
    the account’s sequence number is updated with that value, otherwise it’s not modified.

    Threshold: Low

    :param int bump_to: Sequence number to bump to.
    :param str source: The optional source account.

    """

    @classmethod
    def type_code(cls):
        return Xdr.const.BUMP_SEQUENCE

    def __init__(self, bump_to, source=None):
        super(BumpSequence, self).__init__(source)
        self.bump_to = bump_to

    def to_xdr_object(self):
        """Creates an XDR Operation object that represents this
        :class:`BumpSequence`.

        """
        bump_sequence_op = Xdr.types.BumpSequenceOp(self.bump_to)
        self.body.type = Xdr.const.BUMP_SEQUENCE
        self.body.bumpSequenceOp = bump_sequence_op
        return super(BumpSequence, self).to_xdr_object()

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        """Creates a :class:`BumpSequence` object from an XDR Operation
        object.

        """
        if not op_xdr_object.sourceAccount:
            source = None
        else:
            source = encode_check(
                'account', op_xdr_object.sourceAccount[0].ed25519).decode()

        bump_to = op_xdr_object.body.bumpSequenceOp.bumpTo
        return cls(source=source, bump_to=bump_to)
