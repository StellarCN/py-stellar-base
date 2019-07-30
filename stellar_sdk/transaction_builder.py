import time

from .account import Account
from .asset import Asset
from .keypair import Keypair
from .memo import *
from .network import Network, TESTNET_NETWORK_PASSPHRASE
from .operation import *
from .time_bounds import TimeBounds
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope


class TransactionBuilder:
    def __init__(self,
                 source_account: Account,
                 network_passphrase: str = TESTNET_NETWORK_PASSPHRASE,
                 base_fee: int = 100):
        self.source_account = source_account
        self.base_fee = base_fee
        self.network = Network(network_passphrase)
        self.operations = []
        self.time_bounds = None
        self.memo = NoneMemo()

    def build(self) -> TransactionEnvelope:
        source = Keypair.from_public_key(self.source_account.account_id)
        sequence = self.source_account.sequence + 1
        transaction = Transaction(source=source,
                                  sequence=sequence,
                                  fee=self.base_fee * len(self.operations),
                                  operations=self.operations,
                                  memo=self.memo,
                                  time_bounds=self.time_bounds)
        transaction_envelope = TransactionEnvelope(transaction=transaction, network=self.network)
        self.source_account.increment_sequence_number()
        return transaction_envelope

    @classmethod
    def from_xdr(cls, xdr, network_id) -> TransactionEnvelope:
        """Create a :class:`TransactionEnvelope
        <stellar_sdk.transaction_envelope.TransactionEnvelope>` via an XDR
        object.

        In addition, sets the fields of this builder (the transaction envelope,
        transaction, operations, source, etc.) to all of the fields in the
        provided XDR transaction envelope.

        :param xdr: The XDR object representing the transaction envelope to
            which this builder is setting its state to.
        :param network_id:
        """
        return TransactionEnvelope.from_xdr(xdr=xdr, network=Network(network_id))

    def add_time_bounds(self, min_time, max_time) -> 'TransactionBuilder':
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
        self.time_bounds = TimeBounds(min_time, max_time)
        return self

    def set_timeout(self, timeout: int) -> 'TransactionBuilder':
        if self.time_bounds:
            raise ValueError("TimeBounds has been already set - setting timeout would overwrite it.")
        timeout_timestamp = int(time.time()) + timeout
        self.time_bounds = TimeBounds(min_time=0, max_time=timeout_timestamp)
        return self

    def add_memo(self, memo):
        """Set the memo for the transaction build by this :class:`Builder`.

        :param memo: A memo to add to this transaction.
        :type memo: :class:`Memo <stellar_sdk.memo.Memo>`
        :return: This builder instance.

        """
        self.memo = memo
        return self

    def add_text_memo(self, memo_text):
        """Set the memo for the transaction to a new :class:`TextMemo
        <stellar_sdk.memo.TextMemo>`.

        :param memo_text: The text for the memo to add.
        :type memo_text: str, bytes
        :return: This builder instance.

        """
        memo_text = TextMemo(memo_text)
        return self.add_memo(memo_text)

    def add_id_memo(self, memo_id):
        """Set the memo for the transaction to a new :class:`IdMemo
        <stellar_sdk.memo.IdMemo>`.

        :param int memo_id: A 64 bit unsigned integer to set as the memo.
        :return: This builder instance.

        """
        memo_id = IdMemo(memo_id)
        return self.add_memo(memo_id)

    def add_hash_memo(self, memo_hash):
        """Set the memo for the transaction to a new :class:`HashMemo
        <stellar_sdk.memo.HashMemo>`.

        :param memo_hash: A 32 byte hash or hex encoded string to use as the memo.
        :type memo_hash: bytes, str
        :return: This builder instance.

        """
        memo_hash = HashMemo(memo_hash)
        return self.add_memo(memo_hash)

    def add_return_hash_memo(self, memo_return_hash):
        """Set the memo for the transaction to a new :class:`RetHashMemo
        <stellar_sdk.memo.ReturnHashMemo>`.

        :param bytes memo_return: A 32 byte hash or hex encoded string intended to be interpreted as
            the hash of the transaction the sender is refunding.
        :type memo_return: bytes, str
        :return: This builder instance.

        """
        memo_return = ReturnHashMemo(memo_return_hash)
        return self.add_memo(memo_return)

    def append_operation(self, operation) -> 'TransactionBuilder':
        # TODO: LOG HERE
        self.operations.append(operation)
        return self

    def append_create_account_op(self,
                                 destination: str,
                                 starting_balance: str,
                                 source: str = None) -> 'TransactionBuilder':
        """Append a :class:`CreateAccount
        <stellar_sdk.operation.CreateAccount>` operation to the list of
        operations.

        :param str destination: Account address that is created and funded.
        :param str starting_balance: Amount of XLM to send to the newly created
            account. This XLM comes from the source account.
        :param str source: The source address to deduct funds from to fund the
            new account.
        :return: This builder instance.

        """
        op = CreateAccount(destination, starting_balance, source)
        return self.append_operation(op)

    def append_change_trust_op(self, asset_code, asset_issuer, limit=None, source=None):
        """Append a :class:`ChangeTrust <stellar_sdk.operation.ChangeTrust>`
        operation to the list of operations.

        :param str asset_issuer: The issuer address for the asset.
        :param str asset_code: The asset code for the asset.
        :param str limit: The limit of the new trustline.
        :param str source: The source address to add the trustline to.
        :return: This builder instance.

        """
        asset = Asset(asset_code, asset_issuer)
        op = ChangeTrust(asset, limit, source)
        return self.append_operation(op)

    def append_payment_op(self,
                          destination,
                          amount,
                          asset_code='XLM',
                          asset_issuer=None,
                          source=None):
        """Append a :class:`Payment <stellar_sdk.operation.Payment>` operation
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
        op = Payment(destination, asset, amount, source)
        return self.append_operation(op)

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
        """Append a :class:`PathPayment <stellar_sdk.operation.PathPayment>`
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
        op = PathPayment(destination, send_asset, send_max,
                         dest_asset, dest_amount, assets, source)
        return self.append_operation(op)

    def append_allow_trust_op(self,
                              trustor,
                              asset_code,
                              authorize,
                              source=None):
        """Append an :class:`AllowTrust <stellar_sdk.operation.AllowTrust>`
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
        op = AllowTrust(trustor, asset_code, authorize, source)
        return self.append_operation(op)

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
        """Append a :class:`SetOptions <stellar_sdk.operation.SetOptions>`
        operation to the list of operations.

        .. _Accounts:
            https://www.stellar.org/developers/guides/concepts/accounts.html

        :param str inflation_dest: The address in which to send inflation to on
            an :class:`Inflation <stellar_sdk.operation.Inflation>` operation.
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

        op = SetOptions(inflation_dest, clear_flags, set_flags,
                        master_weight, low_threshold, med_threshold,
                        high_threshold, home_domain, signer_address,
                        signer_type, signer_weight, source)
        return self.append_operation(op)

    def append_hashx_signer(self, hashx, signer_weight, source=None):
        """Add a HashX signer to an account.

        Add a HashX signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
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
        <stellar_sdk.operation.SetOptions` operation. This is a helper
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

    def append_manage_buy_offer_op(self,
                                   selling_code,
                                   selling_issuer,
                                   buying_code,
                                   buying_issuer,
                                   amount,
                                   price,
                                   offer_id=0,
                                   source=None):
        """Append a :class:`ManageBuyOffer <stellar_sdk.operation.ManageBuyOffer>`
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
        :param str amount: Amount being bought. if set to. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of thing being bought in terms of what you are selling. You can pass
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
        op = ManageBuyOffer(selling, buying, amount, price, offer_id,
                            source)
        return self.append_operation(op)

    def append_manage_sell_offer_op(self,
                                    selling_code,
                                    selling_issuer,
                                    buying_code,
                                    buying_issuer,
                                    amount,
                                    price,
                                    offer_id=0,
                                    source=None):
        """Append a :class:`ManageSellOffer <stellar_sdk.operation.ManageSellOffer>`
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
        op = ManageSellOffer(selling, buying, amount, price, offer_id,
                             source)
        return self.append_operation(op)

    def append_create_passive_sell_offer_op(self,
                                            selling_code,
                                            selling_issuer,
                                            buying_code,
                                            buying_issuer,
                                            amount,
                                            price,
                                            source=None):
        """Append a :class:`CreatePassiveSellOffer
        <stellar_sdk.operation.CreatePassiveSellOffer>` operation to the list of
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
        op = CreatePassiveSellOffer(selling, buying, amount, price,
                                    source)
        return self.append_operation(op)

    def append_account_merge_op(self, destination, source=None):
        """Append a :class:`AccountMerge
        <stellar_sdk.operation.AccountMerge>` operation to the list of
        operations.

        :param str destination: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param str source: The source address that is being merged into the
            destination account.
        :return: This builder instance.

        """
        op = AccountMerge(destination, source)
        return self.append_operation(op)

    def append_inflation_op(self, source=None):
        """Append a :class:`Inflation
        <stellar_sdk.operation.Inflation>` operation to the list of
        operations.

        :param str source: The source address that is running the inflation
            operation.
        :return: This builder instance.

        """
        op = Inflation(source)
        return self.append_operation(op)

    def append_manage_data_op(self, data_name, data_value, source=None):
        """Append a :class:`ManageData <stellar_sdk.operation.ManageData>`
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
        op = ManageData(data_name, data_value, source)
        return self.append_operation(op)

    def append_bump_sequence_op(self, bump_to, source=None):
        """Append a :class:`BumpSequence <stellar_sdk.operation.BumpSequence>`
        operation to the list of operations.

        Only available in protocol version 10 and above

        :param int bump_to: Sequence number to bump to.
        :param str source: The source address that is running the inflation
            operation.
        :return: This builder instance.

        """
        op = BumpSequence(bump_to, source)
        return self.append_operation(op)
