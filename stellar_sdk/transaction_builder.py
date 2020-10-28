import time
import warnings
from decimal import Decimal
from typing import List, Union, Optional

from .signer_key import SignerKey
from .account import Account
from .asset import Asset
from .exceptions import ValueError
from .fee_bump_transaction import FeeBumpTransaction
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .keypair import Keypair
from .memo import *
from .network import Network
from .operation import *
from .price import Price
from .signer import Signer
from .time_bounds import TimeBounds
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .utils import hex_to_bytes
from .xdr import Xdr

__all__ = ["TransactionBuilder"]


class TransactionBuilder:
    """Transaction builder helps constructs a new :class:`TransactionEnvelope
    <stellar_sdk.transaction_envelope.TransactionEnvelope>` using the given
    :class:`Account <stellar_sdk.account.Account>` as the transaction's "source account". The transaction will use
    the current sequence number of the given account as its sequence number and increment the given account's
    sequence number by one. The given source account must include a private key for signing the transaction or
    an error will be thrown.

    Be careful about **unsubmitted transactions**! When you build a transaction, stellar-sdk automatically
    increments the source account's sequence number. If you end up not submitting this transaction and submitting
    another one instead, it'll fail due to the sequence number being wrong. So if you decide not to use a built
    transaction, make sure to update the source account's sequence number with :meth:`stellar_sdk.Server.load_account`
    before creating another transaction.

    :param source_account: The source account for this transaction.
    :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        Defaults to **Test SDF Network ; September 2015**.
    :param base_fee: Base fee in stroops. The network base fee is obtained by default from the latest ledger.
        Transaction fee is equal to base fee times number of operations in this transaction.
    :param v1: When this value is set to True, V1 transactions will be generated,
        otherwise V0 transactions will be generated.
        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_ for more information.
    """

    # TODO: add an example
    def __init__(
        self,
        source_account: Account,
        network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee: int = 100,
        v1: bool = True,
    ):
        self.source_account: Account = source_account
        self.base_fee: int = base_fee
        self.network_passphrase: str = network_passphrase
        self.operations: List[Operation] = []
        self.time_bounds: Optional[TimeBounds] = None
        self.memo: Memo = NoneMemo()
        self.v1: bool = v1

    def build(self) -> TransactionEnvelope:
        """This will build the transaction envelope.
        It will also increment the source account's sequence number by 1.

        :return: The transaction envelope.
        """
        source = self.source_account.account_id
        sequence = self.source_account.sequence + 1
        transaction = Transaction(
            source=source,
            sequence=sequence,
            fee=self.base_fee * len(self.operations),
            operations=self.operations,
            memo=self.memo,
            time_bounds=self.time_bounds,
            v1=self.v1,
        )
        transaction_envelope = TransactionEnvelope(
            transaction=transaction, network_passphrase=self.network_passphrase
        )
        self.source_account.increment_sequence_number()
        return transaction_envelope

    @staticmethod
    def build_fee_bump_transaction(
        fee_source: Union[Keypair, str],
        base_fee: int,
        inner_transaction_envelope: TransactionEnvelope,
        network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
    ) -> "FeeBumpTransactionEnvelope":
        """Create a
        :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
        object.

        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_ for more information.

        :param fee_source: The account paying for the transaction.
        :param base_fee: The max fee willing to pay per operation in inner transaction (**in stroops**).
        :param inner_transaction_envelope: The TransactionEnvelope to be bumped by the fee bump transaction.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: a :class:`TransactionBuilder <stellar_sdk.transaction_envelope.TransactionBuilder>` via the XDR object.
        """
        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_source,
            base_fee=base_fee,
            inner_transaction_envelope=inner_transaction_envelope,
        )
        transaction_envelope = FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction, network_passphrase=network_passphrase,
        )
        return transaction_envelope

    @staticmethod
    def from_xdr(
        xdr: str, network_passphrase: str
    ) -> Union["TransactionBuilder", FeeBumpTransactionEnvelope]:
        """Create a :class:`TransactionBuilder
        <stellar_sdk.transaction_envelope.TransactionBuilder>` or
        :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
        via an XDR object.

        In addition, if xdr is not of
        :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`,
        it sets the fields of this builder (the transaction envelope,
        transaction, operations, source, etc.) to all of the fields in the
        provided XDR transaction envelope, but the signature will not be added to it.

        :param xdr: The XDR object representing the transaction envelope to
            which this builder is setting its state to.
        :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        :return: a :class:`TransactionBuilder <stellar_sdk.transaction_envelope.TransactionBuilder>` or
            :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
            via the XDR object.
        """
        xdr_object = Xdr.types.TransactionEnvelope.from_xdr(xdr)
        te_type = xdr_object.type
        if te_type == Xdr.const.ENVELOPE_TYPE_TX_FEE_BUMP:
            return FeeBumpTransactionEnvelope.from_xdr_object(
                xdr_object, network_passphrase
            )
        transaction_envelope = TransactionEnvelope.from_xdr(
            xdr=xdr, network_passphrase=network_passphrase
        )

        source_account = Account(
            transaction_envelope.transaction.source.public_key,
            transaction_envelope.transaction.sequence - 1,
        )
        transaction_builder = TransactionBuilder(
            source_account=source_account,
            network_passphrase=network_passphrase,
            base_fee=int(
                transaction_envelope.transaction.fee
                / len(transaction_envelope.transaction.operations)
            ),
            v1=transaction_envelope.transaction.v1,
        )
        transaction_builder.time_bounds = transaction_envelope.transaction.time_bounds
        transaction_builder.operations = transaction_envelope.transaction.operations
        transaction_builder.memo = transaction_envelope.transaction.memo
        return transaction_builder

    def add_time_bounds(self, min_time: int, max_time: int) -> "TransactionBuilder":
        """Add a time bound to this transaction.

        Add a UNIX timestamp, determined by ledger time, of a lower and
        upper bound of when this transaction will be valid. If a transaction is
        submitted too early or too late, it will fail to make it into the
        transaction set. maxTime equal 0 means that it's not set.

        :param min_time: the UNIX timestamp (in seconds)
        :param max_time: the UNIX timestamp (in seconds)
        :return: This builder instance.

        """
        self.time_bounds = TimeBounds(min_time, max_time)
        return self

    def set_timeout(self, timeout: int) -> "TransactionBuilder":
        """Set timeout for the transaction, actually set a TimeBounds.

        :param timeout: timeout in second.
        :return: This builder instance.
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`: if time_bound is already set.
        """
        if self.time_bounds:
            raise ValueError(
                "TimeBounds has been already set - setting timeout would overwrite it."
            )
        timeout_timestamp = int(time.time()) + timeout
        self.time_bounds = TimeBounds(min_time=0, max_time=timeout_timestamp)
        return self

    def add_memo(self, memo: Memo) -> "TransactionBuilder":
        """Set the memo for the transaction build by this :class:`Builder`.

        :param memo: A memo to add to this transaction.
        :return: This builder instance.

        """
        self.memo = memo
        return self

    def add_text_memo(self, memo_text: Union[str, bytes]) -> "TransactionBuilder":
        """Set the memo for the transaction to a new :class:`TextMemo
        <stellar_sdk.memo.TextMemo>`.

        :param memo_text: The text for the memo to add.
        :return: This builder instance.
        :raises: :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
            if ``memo_text`` is not a valid text memo.
        """
        memo = TextMemo(memo_text)
        return self.add_memo(memo)

    def add_id_memo(self, memo_id: int) -> "TransactionBuilder":
        """Set the memo for the transaction to a new :class:`IdMemo
        <stellar_sdk.memo.IdMemo>`.

        :param memo_id: A 64 bit unsigned integer to set as the memo.
        :return: This builder instance.
        :raises:
            :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
            if ``memo_id`` is not a valid id memo.

        """
        memo = IdMemo(memo_id)
        return self.add_memo(memo)

    def add_hash_memo(self, memo_hash: Union[bytes, str]) -> "TransactionBuilder":
        """Set the memo for the transaction to a new :class:`HashMemo
        <stellar_sdk.memo.HashMemo>`.

        :param memo_hash: A 32 byte hash or hex encoded string to use as the memo.
        :return: This builder instance.
        :raises:
            :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
            if ``memo_hash`` is not a valid hash memo.
        """
        memo = HashMemo(hex_to_bytes(memo_hash))
        return self.add_memo(memo)

    def add_return_hash_memo(
        self, memo_return: Union[bytes, str]
    ) -> "TransactionBuilder":
        """Set the memo for the transaction to a new :class:`RetHashMemo
        <stellar_sdk.memo.ReturnHashMemo>`.

        :param memo_return: A 32 byte hash or hex encoded string intended to be interpreted as
            the hash of the transaction the sender is refunding.
        :return: This builder instance.
        :raises:
            :exc:`MemoInvalidException <stellar_sdk.exceptions.MemoInvalidException>`:
            if ``memo_return`` is not a valid return hash memo.
        """
        memo = ReturnHashMemo(hex_to_bytes(memo_return))
        return self.add_memo(memo)

    def append_operation(self, operation: Operation) -> "TransactionBuilder":
        """Add an operation to the builder instance

        :param operation: an operation
        :return: This builder instance.
        """
        # TODO: LOG HERE
        self.operations.append(operation)
        return self

    def append_create_account_op(
        self,
        destination: str,
        starting_balance: Union[str, Decimal],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`CreateAccount
        <stellar_sdk.operation.CreateAccount>` operation to the list of
        operations.

        :param destination: Account address that is created and funded.
        :param starting_balance: Amount of XLM to send to the newly created
            account. This XLM comes from the source account.
        :param source: The source address to deduct funds from to fund the
            new account.
        :return: This builder instance.

        """
        op = CreateAccount(destination, starting_balance, source)
        return self.append_operation(op)

    def append_change_trust_op(
        self,
        asset_code: str,
        asset_issuer: str,
        limit: Union[str, Decimal] = None,
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ChangeTrust <stellar_sdk.operation.ChangeTrust>`
        operation to the list of operations.

        :param asset_issuer: The issuer address for the asset.
        :param asset_code: The asset code for the asset.
        :param limit: The limit of the new trustline.
        :param source: The source address to add the trustline to.
        :return: This builder instance.

        """
        asset = Asset(asset_code, asset_issuer)
        op = ChangeTrust(asset, limit, source)
        return self.append_operation(op)

    def append_payment_op(
        self,
        destination: str,
        amount: Union[str, Decimal],
        asset_code: str = "XLM",
        asset_issuer: Optional[str] = None,
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`Payment <stellar_sdk.operation.Payment>` operation
        to the list of operations.

        :param destination: Account address that receives the payment.
        :param amount: The amount of the currency to send in the payment.
        :param asset_code: The asset code for the asset to send.
        :param asset_issuer: The address of the issuer of the asset.
        :param source: The source address of the payment.
        :return: This builder instance.

        """
        asset = Asset(code=asset_code, issuer=asset_issuer)
        op = Payment(destination, asset, amount, source)
        return self.append_operation(op)

    def append_path_payment_op(
        self,
        destination: str,
        send_code: str,
        send_issuer: Optional[str],
        send_max: Union[str, Decimal],
        dest_code: str,
        dest_issuer: Optional[str],
        dest_amount: Union[str, Decimal],
        path: List[Asset],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`PathPayment <stellar_sdk.operation.PathPayment>`
        operation to the list of operations.

        :param destination: The destination address (Account ID) for the
            payment.
        :param send_code: The asset code for the source asset deducted from
            the source account.
        :param send_issuer: The address of the issuer of the source asset.
        :param send_max: The maximum amount of send asset to deduct
            (excluding fees).
        :param dest_code: The asset code for the final destination asset
            sent to the recipient.
        :param dest_issuer: Account address that receives the payment.
        :param dest_amount: The amount of destination asset the destination
            account receives.
        :param path: A list of Asset objects to use as the path.
        :param source: The source address of the path payment.
        :return: This builder instance.

        """

        warnings.warn(
            "Will be removed in version v3.0.0, "
            "use stellar_sdk.transaction_builder.append_path_payment_strict_receive_op",
            DeprecationWarning,
        )

        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for asset in path:
            assets.append(asset)
        op = PathPayment(
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=assets,
            source=source,
        )
        return self.append_operation(op)

    def append_path_payment_strict_receive_op(
        self,
        destination: str,
        send_code: str,
        send_issuer: Optional[str],
        send_max: Union[str, Decimal],
        dest_code: str,
        dest_issuer: Optional[str],
        dest_amount: Union[str, Decimal],
        path: List[Asset],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`PathPaymentStrictReceive <stellar_sdk.operation.PathPaymentStrictReceive>`
        operation to the list of operations.

        :param destination: The destination address (Account ID) for the
            payment.
        :param send_code: The asset code for the source asset deducted from
            the source account.
        :param send_issuer: The address of the issuer of the source asset.
        :param send_max: The maximum amount of send asset to deduct
            (excluding fees).
        :param dest_code: The asset code for the final destination asset
            sent to the recipient.
        :param dest_issuer: Account address that receives the payment.
        :param dest_amount: The amount of destination asset the destination
            account receives.
        :param path: A list of Asset objects to use as the path.
        :param source: The source address of the path payment.
        :return: This builder instance.

        """

        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for asset in path:
            assets.append(asset)
        op = PathPaymentStrictReceive(
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=assets,
            source=source,
        )
        return self.append_operation(op)

    def append_path_payment_strict_send_op(
        self,
        destination: str,
        send_code: str,
        send_issuer: Optional[str],
        send_amount: Union[str, Decimal],
        dest_code: str,
        dest_issuer: Optional[str],
        dest_min: Union[str, Decimal],
        path: List[Asset],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`PathPaymentStrictSend <stellar_sdk.operation.PathPaymentStrictSend>`
        operation to the list of operations.

        :param destination: The destination address (Account ID) for the
            payment.
        :param send_code: The asset code for the source asset deducted from
            the source account.
        :param send_issuer: The address of the issuer of the source asset.
        :param send_amount: Amount of send_asset to send.
        :param dest_code: The asset code for the final destination asset
            sent to the recipient.
        :param dest_issuer: Account address that receives the payment.
        :param dest_min: The minimum amount of dest_asset to be received.
        :param path: A list of Asset objects to use as the path.
        :param source: The source address of the path payment.
        :return: This builder instance.

        """

        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for asset in path:
            assets.append(asset)
        op = PathPaymentStrictSend(
            destination=destination,
            send_asset=send_asset,
            send_amount=send_amount,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=assets,
            source=source,
        )
        return self.append_operation(op)

    def append_allow_trust_op(
        self,
        trustor: str,
        asset_code: str,
        authorize: Union[TrustLineEntryFlag, bool],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append an :class:`AllowTrust <stellar_sdk.operation.AllowTrust>`
        operation to the list of operations.

        :param trustor: The account of the recipient of the trustline.
        :param asset_code:  The asset of the trustline the source account
            is authorizing. For example, if an anchor wants to allow another
            account to hold its USD credit, the type is USD:anchor.
        :param authorize: `True` to authorize the line, `False` to deauthorize，if you need further control,
            you can also use :class:`stellar_sdk.operation.allow_trust.TrustLineEntryFlag`.
        :param source: The source address that is establishing the trust in
            the allow trust operation.
        :return: This builder instance.

        """
        op = AllowTrust(trustor, asset_code, authorize, source)
        return self.append_operation(op)

    def append_set_options_op(
        self,
        inflation_dest: str = None,
        clear_flags: Union[int, Flag] = None,
        set_flags: Union[int, Flag] = None,
        master_weight: int = None,
        low_threshold: int = None,
        med_threshold: int = None,
        high_threshold: int = None,
        home_domain: str = None,
        signer: Signer = None,
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`SetOptions <stellar_sdk.operation.SetOptions>`
        operation to the list of operations.

        :param inflation_dest: Account of the inflation destination.
        :param clear_flags: Indicates which flags to clear. For details about the flags,
            please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`__.
            The `bit mask <https://en.wikipedia.org/wiki/Bit_field>`_ integer subtracts from the existing flags of the account.
            This allows for setting specific bits without knowledge of existing flags, you can also use
            :class:`stellar_sdk.operation.set_options.Flag`
            - AUTHORIZATION_REQUIRED = 1
            - AUTHORIZATION_REVOCABLE = 2
            - AUTHORIZATION_IMMUTABLE = 4
        :param set_flags: Indicates which flags to set. For details about the flags,
            please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`__.
            The bit mask integer adds onto the existing flags of the account.
            This allows for setting specific bits without knowledge of existing flags, you can also use
            :class:`stellar_sdk.operation.set_options.Flag`
            - AUTHORIZATION_REQUIRED = 1
            - AUTHORIZATION_REVOCABLE = 2
            - AUTHORIZATION_IMMUTABLE = 4
        :param master_weight: A number from 0-255 (inclusive) representing the weight of the master key.
            If the weight of the master key is updated to 0, it is effectively disabled.
        :param low_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a low threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param med_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a medium threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param high_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a high threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
        :param home_domain: sets the home domain used for
            reverse `federation <https://www.stellar.org/developers/guides/concepts/federation.html>`_ lookup.
        :param signer: Add, update, or remove a signer from the account.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.

        """
        op = SetOptions(
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            signer=signer,
            home_domain=home_domain,
            source=source,
        )
        return self.append_operation(op)

    def append_ed25519_public_key_signer(
        self, account_id: str, weight: int, source: str = None
    ) -> "TransactionBuilder":
        """Add a ed25519 public key signer to an account.

        Add a ed25519 public key signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param account_id: The account id of the new ed25519_public_key signer.
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.

        """
        signer = Signer.ed25519_public_key(account_id=account_id, weight=weight)
        return self.append_set_options_op(signer=signer, source=source)

    def append_hashx_signer(
        self, sha256_hash: Union[bytes, str], weight: int, source: str = None,
    ) -> "TransactionBuilder":
        """Add a sha256 hash(HashX) signer to an account.

        Add a HashX signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param sha256_hash: The address of the new sha256 hash(hashX) signer,
            a 32 byte hash or hex encoded string.
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.

        """
        signer = Signer.sha256_hash(
            sha256_hash=hex_to_bytes(sha256_hash), weight=weight
        )
        return self.append_set_options_op(signer=signer, source=source)

    def append_pre_auth_tx_signer(
        self, pre_auth_tx_hash: Union[str, bytes], weight: int, source=None
    ) -> "TransactionBuilder":
        """Add a PreAuthTx signer to an account.

        Add a PreAuthTx signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param pre_auth_tx_hash: The address of the new preAuthTx signer - obtained by calling ``hash`` on
            the :class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`,
            a 32 byte hash or hex encoded string.
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.

        """
        signer = Signer.pre_auth_tx(
            pre_auth_tx_hash=hex_to_bytes(pre_auth_tx_hash), weight=weight
        )
        return self.append_set_options_op(signer=signer, source=source)

    def append_manage_buy_offer_op(
        self,
        selling_code: str,
        selling_issuer: Optional[str],
        buying_code: str,
        buying_issuer: Optional[str],
        amount: Union[str, Decimal],
        price: Union[str, Decimal, Price],
        offer_id: int = 0,
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageBuyOffer <stellar_sdk.operation.ManageBuyOffer>`
        operation to the list of operations.

        :param selling_code: The asset code for the asset the offer creator
            is selling.
        :param selling_issuer: The issuing address for the asset the offer
            creator is selling.
        :param buying_code: The asset code for the asset the offer creator
            is buying.
        :param buying_issuer: The issuing address for the asset the offer
            creator is buying.
        :param amount: Amount being bought. if set to. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of thing being bought in terms of what you are selling.
        :param offer_id: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param source: The source address that is managing a buying offer on
            Stellar's distributed exchange.
        :return: This builder instance.

        """
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)
        op = ManageBuyOffer(
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
            source=source,
        )
        return self.append_operation(op)

    def append_manage_sell_offer_op(
        self,
        selling_code: str,
        selling_issuer: Optional[str],
        buying_code: str,
        buying_issuer: Optional[str],
        amount: Union[str, Decimal],
        price: Union[str, Price, Decimal],
        offer_id: int = 0,
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageSellOffer <stellar_sdk.operation.ManageSellOffer>`
        operation to the list of operations.

        :param selling_code: The asset code for the asset the offer creator
            is selling.
        :param selling_issuer: The issuing address for the asset the offer
            creator is selling.
        :param buying_code: The asset code for the asset the offer creator
            is buying.
        :param buying_issuer: The issuing address for the asset the offer
            creator is buying.
        :param amount: Amount of the asset being sold. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of 1 unit of selling in terms of buying.
        :param offer_id: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param source: The source address that is managing an offer on
            Stellar's distributed exchange.
        :return: This builder instance.

        """
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)
        op = ManageSellOffer(
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
            source=source,
        )
        return self.append_operation(op)

    def append_create_passive_sell_offer_op(
        self,
        selling_code: str,
        selling_issuer: Optional[str],
        buying_code: str,
        buying_issuer: Optional[str],
        amount: Union[str, Decimal],
        price: Union[str, Price, Decimal],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`CreatePassiveSellOffer
        <stellar_sdk.operation.CreatePassiveSellOffer>` operation to the list of
        operations.

        :param selling_code: The asset code for the asset the offer creator
            is selling.
        :param selling_issuer: The issuing address for the asset the offer
            creator is selling.
        :param buying_code: The asset code for the asset the offer creator
            is buying.
        :param buying_issuer: The issuing address for the asset the offer
            creator is buying.
        :param amount: Amount of the asset being sold. Set to 0 if you want
            to delete an existing offer.
        :param price: Price of 1 unit of selling in terms of buying.
        :param source: The source address that is creating a passive offer
            on Stellar's distributed exchange.
        :return: This builder instance.

        """

        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)
        op = CreatePassiveSellOffer(selling, buying, amount, price, source)
        return self.append_operation(op)

    def append_account_merge_op(
        self, destination: str, source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`AccountMerge
        <stellar_sdk.operation.AccountMerge>` operation to the list of
        operations.

        :param destination: The ID of the offer. 0 for new offer. Set to
            existing offer ID to update or delete.
        :param source: The source address that is being merged into the
            destination account.
        :return: This builder instance.

        """
        op = AccountMerge(destination, source)
        return self.append_operation(op)

    def append_inflation_op(self, source: str = None) -> "TransactionBuilder":
        """Append a :class:`Inflation
        <stellar_sdk.operation.Inflation>` operation to the list of
        operations.

        :param source: The source address that is running the inflation
            operation.
        :return: This builder instance.

        """
        op = Inflation(source)
        return self.append_operation(op)

    def append_manage_data_op(
        self, data_name: str, data_value: Union[str, bytes, None], source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageData <stellar_sdk.operation.ManageData>`
        operation to the list of operations.

        :param data_name: String up to 64 bytes long. If this is a new Name
            it will add the given name/value pair to the account. If this Name
            is already present then the associated value will be modified.
        :param data_value: If not present then the existing
            Name will be deleted. If present then this value will be set in the
            DataEntry. Up to 64 bytes long.
        :param source: The source account on which data is being managed.
            operation.
        :return: This builder instance.

        """
        op = ManageData(data_name, data_value, source)
        return self.append_operation(op)

    def append_bump_sequence_op(
        self, bump_to: int, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`BumpSequence <stellar_sdk.operation.BumpSequence>`
        operation to the list of operations.

        :param bump_to: Sequence number to bump to.
        :param source: The source address that is running the inflation operation.
        :return: This builder instance.

        """
        op = BumpSequence(bump_to, source)
        return self.append_operation(op)

    def append_create_claimable_balance_op(
        self,
        asset: Asset,
        amount: Union[str, Decimal],
        claimants: List[Claimant],
        source: str = None,
    ) -> "TransactionBuilder":
        """Append a :class:`CreateClaimableBalance <stellar_sdk.operation.CreateClaimableBalance>`
        operation to the list of operations.

        :param asset: The asset for the claimable balance.
        :param amount: the amount of the asset.
        :param claimants: A list of Claimants.
        :param source: The source account (defaults to transaction source).
        """
        op = CreateClaimableBalance(asset, amount, claimants, source)
        return self.append_operation(op)

    def append_claim_claimable_balance_op(
        self, balance_id: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`ClaimClaimableBalance <stellar_sdk.operation.ClaimClaimableBalance>`
        operation to the list of operations.

        :param balance_id: The claimable balance id to be claimed.
        :param source: The source account (defaults to transaction source).
        """
        op = ClaimClaimableBalance(balance_id, source)
        return self.append_operation(op)

    def append_begin_sponsoring_future_reserves_op(
        self, sponsored_id: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`BeginSponsoringFutureReserves <stellar_sdk.operation.BeginSponsoringFutureReserves>`
        operation to the list of operations.

        :param sponsored_id: The sponsored account id.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = BeginSponsoringFutureReserves(sponsored_id, source)
        return self.append_operation(op)

    def append_end_sponsoring_future_reserves_op(
        self, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>`
        operation to the list of operations.

        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = EndSponsoringFutureReserves(source)
        return self.append_operation(op)

    def append_revoke_account_sponsorship_op(
        self, account_id: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for an account to the list of operations.

        :param account_id: The sponsored account ID.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_account_sponsorship(account_id, source)
        return self.append_operation(op)

    def append_revoke_trustline_sponsorship_op(
        self, account_id: str, asset: Asset, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a trustline to the list of operations.

        :param account_id: The account ID which owns the trustline.
        :param asset: The asset in the trustline.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        return self.append_operation(op)

    def append_revoke_offer_sponsorship_op(
        self, seller_id: str, offer_id: int, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for an offer to the list of operations.

        :param seller_id: The account ID which created the offer.
        :param offer_id: The offer ID.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)
        return self.append_operation(op)

    def append_revoke_data_sponsorship_op(
        self, account_id: str, data_name: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a data entry to the list of operations.

        :param account_id: The account ID which owns the data entry.
        :param data_name: The name of the data entry
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)
        return self.append_operation(op)

    def append_revoke_claimable_balance_sponsorship_op(
        self, claimable_balance_id: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a claimable to the list of operations.

        :param claimable_balance_id: The sponsored claimable balance ID.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_claimable_balance_sponsorship(
            claimable_balance_id, source
        )
        return self.append_operation(op)

    def append_revoke_ed25519_public_key_signer_sponsorship_op(
        self, account_id: str, signer_key: str, source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a ed25519_public_key signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the ed25519_public_key signer.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        signer_key = SignerKey.ed25519_public_key(signer_key)
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        return self.append_operation(op)

    def append_revoke_hashx_signer_sponsorship_op(
        self, account_id: str, signer_key: Union[bytes, str], source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a hashx signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the hashx signer.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        signer_key = SignerKey.sha256_hash(hex_to_bytes(signer_key))
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        return self.append_operation(op)

    def append_revoke_pre_auth_tx_signer_sponsorship_op(
        self, account_id: str, signer_key: Union[bytes, str], source: str = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>` operation
        for a pre_auth_tx signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the pre_auth_tx signer.
        :param source: The source account (defaults to transaction source).
        :return: This builder instance.
        """
        signer_key = SignerKey.pre_auth_tx(hex_to_bytes(signer_key))
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        return self.append_operation(op)
