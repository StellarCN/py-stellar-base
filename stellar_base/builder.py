# coding: utf-8
import binascii
import warnings

from .asset import Asset
from .horizon import HORIZON_LIVE, HORIZON_TEST
from .horizon import Horizon
from .keypair import Keypair
from . import memo
from .network import NETWORKS, Network
from . import operation
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope as Te
from .exceptions import SignatureExistError
from .federation import federation, FederationError


class Builder(object):
    """The :class:`Builder` object, which uses the builder pattern to create
    a list of operations in a :class:`Transaction`, ultimately to be submitted
    as a :class:`TransactionEnvelope` to the network via Horizon (see
    :class:`Horizon`).

    :param str secret: The base32 secret seed for the source address.
    :param str address: The base32 source address.
    :param str horizon_uri: The horizon instance to use for submitting the created
        transaction.
    :param str network: The network string that describes which version of
        Horizon to use, either the live net ('PUBLIC') or the test net
        ('TESTNET'). Defaults to TESTNET if an instance of Horizon has not been
        passed to the horizon param.
    :param sequence: The sequence number to use for submitting this
        transaction with (must be the *current* sequence number of the source
        account)
    :type sequence: int, str
    :param int fee: The network base fee is currently set to
        100 stroops (0.00001 lumens). Transaction fee is equal to base fee
        times number of operations in this transaction.
    """

    def __init__(self,
                 secret=None,
                 address=None,
                 horizon_uri=None,
                 network=None,
                 sequence=None,
                 fee=100):
        if secret:
            self.key_pair = Keypair.from_seed(secret)
            self.address = self.key_pair.address().decode()
        else:
            self.key_pair = None
            self.address = None

        if address is None and secret is None:
            raise Exception('No Stellar address afforded.')
        if address is not None and secret is None:
            self.address = Keypair.from_address(address).address().decode()
            self.key_pair = None

        if network is None:
            self.network = 'TESTNET'
        elif network.upper() in NETWORKS:
            self.network = network.upper()
        else:
            self.network = network

        if horizon_uri:
            self.horizon = Horizon(horizon_uri)
        elif self.network == 'PUBLIC':
            self.horizon = Horizon(HORIZON_LIVE)
        else:
            self.horizon = Horizon(HORIZON_TEST)

        if sequence:
            self.sequence = int(sequence)
        elif self.address:
            self.sequence = self.get_sequence()
        else:
            self.sequence = None
        self.ops = []
        self.time_bounds = None
        self.memo = memo.NoneMemo()
        self.fee = fee
        self.tx = None
        self.te = None

    def append_op(self, operation):
        """Append an :class:`Operation <stellar_base.operation.Operation>` to
        the list of operations.

        Add the operation specified if it doesn't already exist in the list of
        operations of this :class:`Builder` instance.

        :param operation: The operation to append to the list of operations.
        :type operation: :class:`Operation`
        :return: This builder instance.

        """
        if operation not in self.ops:
            self.ops.append(operation)
        return self

    def append_create_account_op(self,
                                 destination,
                                 starting_balance,
                                 source=None):
        """Append a :class:`CreateAccount
        <stellar_base.operation.CreateAccount>` operation to the list of
        operations.

        :param str destination: Account address that is created and funded.
        :param str starting_balance: Amount of XLM to send to the newly created
            account. This XLM comes from the source account.
        :param str source: The source address to deduct funds from to fund the
            new account.
        :return: This builder instance.

        """
        op = operation.CreateAccount(destination, starting_balance, source)
        return self.append_op(op)

    def append_trust_op(self, destination, code, limit=None, source=None):
        """append_trust_op will be deprecated in the future, use append_change_trust_op instead.
        Append a :class:`ChangeTrust <stellar_base.operation.ChangeTrust>`
        operation to the list of operations.

        :param str destination: The issuer address for the asset.
        :param str code: The asset code for the asset.
        :param str limit: The limit of the new trustline.
        :param str source: The source address to add the trustline to.
        :return: This builder instance.

        """
        warnings.warn(
            "append_trust_op will be deprecated in the future, use append_change_trust_op instead.",
            PendingDeprecationWarning
        )

        return self.append_change_trust_op(asset_code=code, asset_issuer=destination, limit=limit, source=source)

    def append_change_trust_op(self, asset_code, asset_issuer, limit=None, source=None):
        """Append a :class:`ChangeTrust <stellar_base.operation.ChangeTrust>`
        operation to the list of operations.

        :param str asset_issuer: The issuer address for the asset.
        :param str asset_code: The asset code for the asset.
        :param str limit: The limit of the new trustline.
        :param str source: The source address to add the trustline to.
        :return: This builder instance.

        """
        asset = Asset(asset_code, asset_issuer)
        op = operation.ChangeTrust(asset, limit, source)
        return self.append_op(op)

    def append_payment_op(self,
                          destination,
                          amount,
                          asset_code='XLM',
                          asset_issuer=None,
                          source=None):
        """Append a :class:`Payment <stellar_base.operation.Payment>` operation
        to the list of operations.

        :param str destination: Account address that receives the payment.
        :param str amount: The amount of the currency to send in the payment.
        :param str asset_code: The asset code for the asset to send.
        :param asset_issuer: The address of the issuer of the asset.
        :type asset_issuer: str, None
        :param str source: The source address of the payment.
        :return: This builder instance.

        """
        asset = Asset(code=asset_code, issuer=asset_issuer)
        op = operation.Payment(destination, asset, amount, source)
        return self.append_op(op)

    def append_path_payment_op(self,
                               destination,
                               send_code,
                               send_issuer,
                               send_max,
                               dest_code,
                               dest_issuer,
                               dest_amount,
                               path,
                               source=None):
        """Append a :class:`PathPayment <stellar_base.operation.PathPayment>`
        operation to the list of operations.

        :param str destination: The destination address (Account ID) for the
            payment.
        :param str send_code: The asset code for the source asset deducted from
            the source account.
        :param send_issuer: The address of the issuer of the source asset.
        :type send_issuer: str, None
        :param str send_max: The maximum amount of send asset to deduct
            (excluding fees).
        :param str dest_code: The asset code for the final destination asset
            sent to the recipient.
        :param dest_issuer: Account address that receives the payment.
        :type dest_issuer: str, None
        :param str dest_amount: The amount of destination asset the destination
            account receives.
        :param list path: A list of asset tuples, each tuple containing a
            (asset_code, asset_issuer) for each asset in the path. For the native
            asset, `None` is used for the asset_issuer.
        :param str source: The source address of the path payment.
        :return: This builder instance.

        """
        # path: a list of asset tuple which contains asset_code and asset_issuer,
        # [(asset_code, asset_issuer), (asset_code, asset_issuer)] for native asset you can deliver
        # ('XLM', None)
        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for p in path:
            assets.append(Asset(p[0], p[1]))
        op = operation.PathPayment(destination, send_asset, send_max,
                                   dest_asset, dest_amount, assets, source)
        return self.append_op(op)

    def append_allow_trust_op(self,
                              trustor,
                              asset_code,
                              authorize,
                              source=None):
        """Append an :class:`AllowTrust <stellar_base.operation.AllowTrust>`
        operation to the list of operations.

        :param str trustor: The account of the recipient of the trustline.
        :param str asset_code:  The asset of the trustline the source account
            is authorizing. For example, if an anchor wants to allow another
            account to hold its USD credit, the type is USD:anchor.
        :param bool authorize: Flag indicating whether the trustline is
            authorized.
        :param str source: The source address that is establishing the trust in
            the allow trust operation.
        :return: This builder instance.

        """
        op = operation.AllowTrust(trustor, asset_code, authorize, source)
        return self.append_op(op)

    def append_set_options_op(self,
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
        """Append a :class:`SetOptions <stellar_base.operation.SetOptions>`
        operation to the list of operations.

        .. _Accounts:
            https://www.stellar.org/developers/guides/concepts/accounts.html

        :param str inflation_dest: The address in which to send inflation to on
            an :class:`Inflation <stellar_base.operation.Inflation>` operation.
        :param int clear_flags: Indicates which flags to clear. For details
            about the flags, please refer to Stellar's documentation on
            `Accounts`_. The bit mask integer subtracts from the existing flags
            of the account. This allows for setting specific bits without
            knowledge of existing flags.
        :param int set_flags: Indicates which flags to set. For details about
            the flags, please refer to Stellar's documentation on `Accounts`_.
            The bit mask integer adds onto the existing flags of the account.
            This allows for setting specific bits without knowledge of existing
            flags.
        :param int master_weight: Weight of the master key. This account may
            also add other keys with which to sign transactions using the
            signer param.
        :param int low_threshold: A number from 0-255 representing the
            threshold this account sets on all operations it performs that have
            a `low threshold
            <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param int med_threshold: A number from 0-255 representing the
            threshold this account sets on all operations it performs that have
            a `medium threshold
            <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param int high_threshold: A number from 0-255 representing the
            threshold this account sets on all operations it performs that have
            a `high threshold
            <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param str home_domain: Sets the home domain of an account. See
            Stellar's documentation on `Federation
            <https://www.stellar.org/developers/guides/concepts/federation.html>`_.
        :param signer_address: The address of the new signer to add to the
            source account.
        :type signer_address: str, bytes
        :param str signer_type: The type of signer to add to the account. Must
            be in ('ed25519PublicKey', 'hashX', 'preAuthTx'). See Stellar's
            documentation for `Multi-Sign
            <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_
            for more information.
        :param int signer_weight: The weight of the signer. If the weight is 0,
            the signer will be deleted.
        :param str source: The source address for which options are being set.
        :return: This builder instance.

        """

        op = operation.SetOptions(inflation_dest, clear_flags, set_flags,
                                  master_weight, low_threshold, med_threshold,
                                  high_threshold, home_domain, signer_address,
                                  signer_type, signer_weight, source)
        return self.append_op(op)

    def append_hashx_signer(self, hashx, signer_weight, source=None):
        """Add a HashX signer to an account.

        Add a HashX signer to an account via a :class:`SetOptions
        <stellar_base.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param hashx: The address of the new hashX signer.
        :type hashx: str, bytes
        :param int signer_weight: The weight of the new signer.
        :param str source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.

        """
        return self.append_set_options_op(
            signer_address=hashx,
            signer_type='hashX',
            signer_weight=signer_weight,
            source=source)

    def append_pre_auth_tx_signer(self,
                                  pre_auth_tx,
                                  signer_weight,
                                  source=None):
        """Add a PreAuthTx signer to an account.

        Add a PreAuthTx signer to an account via a :class:`SetOptions
        <stellar_base.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param pre_auth_tx: The address of the new preAuthTx signer - obtained by calling `hash_meta` on the TransactionEnvelope.
        :type pre_auth_tx: str, bytes
        :param int signer_weight: The weight of the new signer.
        :param str source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.

        """
        return self.append_set_options_op(
            signer_address=pre_auth_tx,
            signer_type='preAuthTx',
            signer_weight=signer_weight,
            source=source)

    def append_manage_offer_op(self,
                               selling_code,
                               selling_issuer,
                               buying_code,
                               buying_issuer,
                               amount,
                               price,
                               offer_id=0,
                               source=None):
        """Append a :class:`ManageOffer <stellar_base.operation.ManageOffer>`
        operation to the list of operations.

        :param str selling_code: The asset code for the asset the offer creator
            is selling.
        :param selling_issuer: The issuing address for the asset the offer
            creator is selling.
        :type selling_issuer: str, None
        :param str buying_code: The asset code for the asset the offer creator
            is buying.
        :param buying_issuer: The issuing address for the asset the offer
            creator is selling.
        :type buying_issuer: str, None
        :param str amount: Amount of the asset being sold. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of 1 unit of selling in terms of buying. You can pass
            in a number as a string or a dict like `{n: numerator, d: denominator}`
        :type price: str, dict
        :param int offer_id: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param str source: The source address that is managing an offer on
            Stellar's distributed exchange.
        :return: This builder instance.

        """
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)
        op = operation.ManageOffer(selling, buying, amount, price, offer_id,
                                   source)
        return self.append_op(op)

    def append_create_passive_offer_op(self,
                                       selling_code,
                                       selling_issuer,
                                       buying_code,
                                       buying_issuer,
                                       amount,
                                       price,
                                       source=None):
        """Append a :class:`CreatePassiveOffer
        <stellar_base.operation.CreatePassiveOffer>` operation to the list of
        operations.

        :param str selling_code: The asset code for the asset the offer creator
            is selling.
        :param selling_issuer: The issuing address for the asset the offer
            creator is selling.
        :type selling_issuer: str, None
        :param str buying_code: The asset code for the asset the offer creator
            is buying.
        :param buying_issuer: The issuing address for the asset the offer
            creator is selling.
        :type buying_issuer: str, None
        :param str amount: Amount of the asset being sold. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of 1 unit of selling in terms of buying. You can pass
            in a number as a string or a dict like `{n: numerator, d: denominator}`
        :type price: str, dict
        :param str source: The source address that is creating a passive offer
            on Stellar's distributed exchange.
        :return: This builder instance.

        """
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)
        op = operation.CreatePassiveOffer(selling, buying, amount, price,
                                          source)
        return self.append_op(op)

    def append_account_merge_op(self, destination, source=None):
        """Append a :class:`AccountMerge
        <stellar_base.operation.AccountMerge>` operation to the list of
        operations.

        :param str destination: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param str source: The source address that is being merged into the
            destination account.
        :return: This builder instance.

        """
        op = operation.AccountMerge(destination, source)
        return self.append_op(op)

    def append_inflation_op(self, source=None):
        """Append a :class:`Inflation
        <stellar_base.operation.Inflation>` operation to the list of
        operations.

        :param str source: The source address that is running the inflation
            operation.
        :return: This builder instance.

        """
        op = operation.Inflation(source)
        return self.append_op(op)

    def append_manage_data_op(self, data_name, data_value, source=None):
        """Append a :class:`ManageData <stellar_base.operation.ManageData>`
        operation to the list of operations.

        :param str data_name: String up to 64 bytes long. If this is a new Name
            it will add the given name/value pair to the account. If this Name
            is already present then the associated value will be modified.
        :param data_value: If not present then the existing
            Name will be deleted. If present then this value will be set in the
            DataEntry. Up to 64 bytes long.
        :type data_value: str, bytes, None
        :param str source: The source account on which data is being managed.
            operation.
        :return: This builder instance.

        """
        op = operation.ManageData(data_name, data_value, source)
        return self.append_op(op)

    def append_bump_sequence_op(self, bump_to, source=None):
        """Append a :class:`BumpSequence <stellar_base.operation.BumpSequence>`
        operation to the list of operations.

        Only available in protocol version 10 and above

        :param int bump_to: Sequence number to bump to.
        :param str source: The source address that is running the inflation
            operation.
        :return: This builder instance.

        """
        op = operation.BumpSequence(bump_to, source)
        return self.append_op(op)

    def add_memo(self, memo):
        """Set the memo for the transaction build by this :class:`Builder`.

        :param memo: A memo to add to this transaction.
        :type memo: :class:`Memo <stellar_base.memo.Memo>`
        :return: This builder instance.

        """
        self.memo = memo
        return self

    def add_text_memo(self, memo_text):
        """Set the memo for the transaction to a new :class:`TextMemo
        <stellar_base.memo.TextMemo>`.

        :param str memo_text: The text for the memo to add.
        :return: This builder instance.

        """
        memo_text = memo.TextMemo(memo_text)
        return self.add_memo(memo_text)

    def add_id_memo(self, memo_id):
        """Set the memo for the transaction to a new :class:`IdMemo
        <stellar_base.memo.IdMemo>`.

        :param int memo_id: A 64 bit unsigned integer to set as the memo.
        :return: This builder instance.

        """
        memo_id = memo.IdMemo(memo_id)
        return self.add_memo(memo_id)

    def add_hash_memo(self, memo_hash):
        """Set the memo for the transaction to a new :class:`HashMemo
        <stellar_base.memo.HashMemo>`.

        :param memo_hash: A 32 byte hash or hex encoded string to use as the memo.
        :type memo_hash: bytes, str
        :return: This builder instance.

        """
        memo_hash = memo.HashMemo(memo_hash)
        return self.add_memo(memo_hash)

    def add_ret_hash_memo(self, memo_return):
        """Set the memo for the transaction to a new :class:`RetHashMemo
        <stellar_base.memo.RetHashMemo>`.

        :param bytes memo_return: A 32 byte hash or hex encoded string intended to be interpreted as
            the hash of the transaction the sender is refunding.
        :type memo_return: bytes, str
        :return: This builder instance.

        """
        memo_return = memo.RetHashMemo(memo_return)
        return self.add_memo(memo_return)

    def add_time_bounds(self, time_bounds):
        """Add a time bound to this transaction.

        Add a UNIX timestamp, determined by ledger time, of a lower and
        upper bound of when this transaction will be valid. If a transaction is
        submitted too early or too late, it will fail to make it into the
        transaction set. maxTime equal 0 means that it's not set.

        :param dict time_bounds: A dict that contains a minTime and maxTime attribute
            (`{'minTime': 1534392138, 'maxTime': 1534392238}`) representing the
            lower and upper bound of when a given transaction will be valid.
        :return: This builder instance.

        """
        self.time_bounds = time_bounds
        return self

    def federation_payment(self,
                           fed_address,
                           amount,
                           asset_code='XLM',
                           asset_issuer=None,
                           source=None,
                           allow_http=False):
        """Append a :class:`Payment <stellar_base.operation.Payment>` operation
        to the list of operations using federation on the destination address.

        Translates the destination stellar address to an account ID via
        :func:`federation <stellar_base.federation.federation>`, before
        creating a new payment operation via :meth:`append_payment_op`.

        :param str fed_address: A Stellar Address that needs to be translated
            into a valid account ID via federation.
        :param str amount: The amount of the currency to send in the payment.
        :param str asset_code: The asset code for the asset to send.
        :param str asset_issuer: The address of the issuer of the asset.
        :param str source: The source address of the payment.
        :param bool allow_http: When set to `True`, connections to insecure http protocol federation servers
            will be allowed. Must be set to `False` in production. Default: `False`.
        :return: This builder instance.

        """
        fed_info = federation(
            address_or_id=fed_address, fed_type='name', allow_http=allow_http)
        if not fed_info:
            raise FederationError(
                'Cannot determine Stellar Address to Account ID translation '
                'via Federation server')
        self.append_payment_op(fed_info['account_id'], amount, asset_code,
                               asset_issuer, source)
        memo_type = fed_info.get('memo_type')
        if memo_type is not None and memo_type in ('text', 'id', 'hash'):
            getattr(self, 'add_' + memo_type + '_memo')(fed_info['memo'])

    def gen_tx(self):
        """Generate a :class:`Transaction
        <stellar_base.transaction.Transaction>` object from the list of
        operations contained within this object.

        :return: A transaction representing all of the operations that have
            been appended to this builder.
        :rtype: :class:`Transaction <stellar_base.transaction.Transaction>`

        """
        if not self.address:
            raise Exception('Transaction does not have any source address')
        if not self.sequence:
            raise Exception('No sequence is present, maybe not funded?')
        tx = Transaction(
            source=self.address,
            sequence=self.sequence,
            time_bounds=self.time_bounds,
            memo=self.memo,
            fee=self.fee * len(self.ops),
            operations=self.ops)
        self.tx = tx
        return tx

    def gen_te(self):
        """Generate a :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>` around the
        generated Transaction via the list of operations in this instance.

        :return: A transaction envelope ready to send over the network.
        :rtype: :class:`TransactionEnvelope
            <stellar_base.transaction_envelope.TransactionEnvelope>`

        """
        if self.tx is None:
            self.gen_tx()
        te = Te(self.tx, network_id=self.network)
        if self.te:
            te.signatures = self.te.signatures
        self.te = te
        return te

    def gen_xdr(self):
        """Create an XDR object around a newly generated
        :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>`.

        :return: An XDR object representing a newly created transaction
            envelope ready to send over the network.

        """
        if self.tx is None:
            self.gen_te()
        return self.te.xdr()

    def gen_compliance_xdr(self):
        """Create an XDR object representing this builder's transaction to be
        sent over via the Compliance protocol (notably, with a sequence number
        of 0).

        Intentionally, the XDR object is returned without any signatures on the
        transaction.

        See `Stellar's documentation on its Compliance Protocol
        <https://www.stellar.org/developers/guides/compliance-protocol.html>`_
        for more information.

        """
        sequence = self.sequence
        self.sequence = -1
        tx_xdr = self.gen_tx().xdr()
        self.sequence = sequence
        return tx_xdr

    def hash(self):
        """Return a hash for this transaction.

        :return: A hash for this transaction.
        :rtype: bytes
        """
        return self.gen_te().hash_meta()

    def hash_hex(self):
        """Return a hex encoded hash for this transaction.

        :return: A hex encoded hash for this transaction.
        :rtype: str
        """
        return binascii.hexlify(self.hash()).decode()

    def import_from_xdr(self, xdr):
        """Create a :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>` via an XDR
        object.

        In addition, sets the fields of this builder (the transaction envelope,
        transaction, operations, source, etc.) to all of the fields in the
        provided XDR transaction envelope.

        :param xdr: The XDR object representing the transaction envelope to
            which this builder is setting its state to.
        :type xdr: bytes, str

        """
        te = Te.from_xdr(xdr)
        if self.network.upper() in NETWORKS:
            te.network_id = Network(NETWORKS[self.network]).network_id()
        else:
            te.network_id = Network(self.network).network_id()
        self.te = te
        self.tx = te.tx  # with a different source or not .
        self.ops = te.tx.operations
        self.address = te.tx.source
        self.sequence = te.tx.sequence - 1
        time_bounds_in_xdr = te.tx.time_bounds
        if time_bounds_in_xdr:
            self.time_bounds = {
                'maxTime': time_bounds_in_xdr[0].maxTime,
                'minTime': time_bounds_in_xdr[0].minTime
            }
        else:
            self.time_bounds = None
        self.memo = te.tx.memo
        return self

    def sign(self, secret=None):
        """Sign the generated :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>` from the list
        of this builder's operations.

        :param str secret: The secret seed to use if a key pair or secret was
            not provided when this class was originaly instantiated, or if
            another key is being utilized to sign the transaction envelope.

        """
        key_pair = self.key_pair if not secret else Keypair.from_seed(secret)

        self.gen_te()

        try:
            self.te.sign(key_pair)
        except SignatureExistError:
            raise

    def sign_preimage(self, preimage):
        """Sign the generated transaction envelope using a Hash(x) signature.

        :param preimage: The value to be hashed and used as a signer on the
            transaction envelope.
        :type preimage: str, bytes

        """
        if self.te is None:
            self.gen_te()
        try:
            self.te.sign_hashX(preimage)
        except SignatureExistError:
            raise

    def submit(self):
        """Submit the generated XDR object of the built transaction envelope to
        Horizon.

        Sends the generated transaction envelope over the wire via this
        builder's :class:`Horizon <stellar_base.horizon.Horizon>` instance.
        Note that you'll typically want to sign the transaction before
        submitting via the sign methods.

        :returns: A dict representing the JSON response from Horizon.

        """
        return self.horizon.submit(self.gen_xdr())

    def next_builder(self):
        """Create a new builder based off of this one with its sequence number
        incremented.

        :return: A new Builder instance
        :rtype: :class:`Builder`

        """
        sequence = self.sequence + 1
        next_builder = Builder(
            horizon_uri=self.horizon.horizon_uri,
            address=self.address,
            network=self.network,
            sequence=sequence,
            fee=self.fee)
        next_builder.key_pair = self.key_pair
        return next_builder

    def get_sequence(self):
        """Get the sequence number for a given account via Horizon.

        :return: The current sequence number for a given account
        :rtype: int
        """
        if not self.address:
            raise ValueError('No address provided')

        address = self.horizon.account(self.address)
        return int(address.get('sequence'))