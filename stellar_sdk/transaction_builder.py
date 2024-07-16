import binascii
import math
import os
import time
import warnings
from decimal import Decimal
from typing import List, Optional, Sequence, Union

from . import StrKey
from . import xdr as stellar_xdr
from .account import Account
from .address import Address
from .asset import Asset
from .fee_bump_transaction import FeeBumpTransaction
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .keypair import Keypair
from .ledger_bounds import LedgerBounds
from .liquidity_pool_asset import LiquidityPoolAsset
from .liquidity_pool_id import LiquidityPoolId
from .memo import *
from .muxed_account import MuxedAccount
from .network import Network
from .operation import *
from .preconditions import Preconditions
from .price import Price
from .signer import Signer
from .signer_key import SignedPayloadSigner, SignerKey
from .soroban_data_builder import SorobanDataBuilder
from .time_bounds import TimeBounds
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope
from .utils import hex_to_bytes, is_valid_hash

__all__ = ["TransactionBuilder"]

MIN_BASE_FEE = 100


class TransactionBuilder:
    """Transaction builder helps constructs a new :class:`TransactionEnvelope
    <stellar_sdk.transaction_envelope.TransactionEnvelope>` using the given
    :class:`Account <stellar_sdk.account.Account>` as the transaction's "source account". The transaction will use
    the current sequence number of the given account as its sequence number and increment the given account's
    sequence number by one.

    Operations can be added to the transaction via their corresponding builder
    methods, and each returns the :class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
    object, so they can be chained together. After adding the desired operations, call
    the :func:`build` method on the TransactionBuilder to return a fully constructed
    :class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>` that can be signed.

    Be careful about **unsubmitted transactions**! When you build a transaction, stellar-sdk automatically
    increments the source account's sequence number. If you end up not submitting this transaction and submitting
    another one instead, it'll fail due to the sequence number being wrong. So if you decide not to use a built
    transaction, make sure to update the source account's sequence number
    with :func:`stellar_sdk.server.Server.load_account` or :func:`stellar_sdk.server_async.ServerAsync.load_account`
    before creating another transaction.

    The following code example creates a new transaction with :class:`CreateAccount <stellar_sdk.operation.CreateAccount>`
    and :class:`Payment <stellar_sdk.operation.Payment>` operations. The Transaction's source account(alice) first
    funds `bob`, then sends a payment to `bob`. The built transaction is then signed by `alice_keypair`::

        # Alice funds Bob with 5 XLM and then pays Bob 10.25 XLM
        from stellar_sdk import Server, Asset, Keypair, TransactionBuilder, Network

        alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
        bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"

        server = Server("https://horizon-testnet.stellar.org")
        alice_account = server.load_account(alice_keypair.public_key)
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        base_fee = 100
        transaction = (
            TransactionBuilder(
                source_account=alice_account,
                network_passphrase=network_passphrase,
                base_fee=base_fee,
            )
                .add_text_memo("Hello, Stellar!")
                .append_create_account_op(bob_address, "5")
                .append_payment_op(bob_address, Asset.native(), "10.25")
                .set_timeout(30)
                .build()
        )
        transaction.sign(alice_keypair)
        response = server.submit_transaction(transaction)
        print(response)

    :param source_account: The source account for this transaction.
    :param network_passphrase: The network to connect to for verifying and retrieving additional attributes from.
        Defaults to ``Test SDF Network ; September 2015``.
    :param base_fee: Max fee you're willing to pay per operation in this transaction (**in stroops**).
    :param v1: When this value is set to True, V1 transactions will be generated,
        otherwise V0 transactions will be generated.
        See `CAP-0015 <https://github.com/stellar/stellar-protocol/blob/master/core/cap-0015.md>`_ for more information.
    """

    def __init__(
        self,
        source_account: Account,
        network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee: int = MIN_BASE_FEE,
        v1: bool = True,
    ):
        self.source_account: Account = source_account
        self.base_fee: int = base_fee
        self.network_passphrase: str = network_passphrase
        self.operations: List[Operation] = []
        self.time_bounds: Optional[TimeBounds] = None
        self.ledger_bounds: Optional[LedgerBounds] = None
        self.min_sequence_number: Optional[int] = None
        self.min_sequence_age: Optional[int] = None
        self.min_sequence_ledger_gap: Optional[int] = None
        self.extra_signers: List[SignerKey] = []
        self.memo: Memo = NoneMemo()
        self.v1: bool = v1

        self.soroban_data: Optional[stellar_xdr.SorobanTransactionData] = None

    def build(self) -> TransactionEnvelope:
        """This will build the transaction envelope.
        It will also increment the source account's sequence number by 1.

        :return: New transaction envelope.
        """
        if self.time_bounds is None:
            warnings.warn(
                "It looks like you haven't set a TimeBounds for the transaction, "
                "we strongly recommend that you set it. "
                "You can learn why you should set it up through this link: "
                "https://www.stellar.org/developers-blog/transaction-submission-timeouts-and-dynamic-fees-faq"
            )

        source = self.source_account.account
        sequence = self.source_account.sequence + 1
        preconditions = Preconditions(
            time_bounds=self.time_bounds,
            ledger_bounds=self.ledger_bounds,
            min_sequence_number=self.min_sequence_number,
            min_sequence_age=self.min_sequence_age,
            min_sequence_ledger_gap=self.min_sequence_ledger_gap,
            extra_signers=self.extra_signers,
        )
        fee = self.base_fee * len(self.operations)
        if self.soroban_data:
            fee += self.soroban_data.resource_fee.int64
        transaction = Transaction(
            source=source,
            sequence=sequence,
            fee=fee,
            operations=self.operations,
            memo=self.memo,
            preconditions=preconditions,
            soroban_data=self.soroban_data,
            v1=self.v1,
        )
        transaction_envelope = TransactionEnvelope(
            transaction=transaction, network_passphrase=self.network_passphrase
        )
        self.source_account.increment_sequence_number()
        return transaction_envelope

    @staticmethod
    def build_fee_bump_transaction(
        fee_source: Union[MuxedAccount, Keypair, str],
        base_fee: int,
        inner_transaction_envelope: TransactionEnvelope,
        network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
    ) -> FeeBumpTransactionEnvelope:
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

        if base_fee < MIN_BASE_FEE:
            raise ValueError(
                f"Invalid `base_fee`, it should be at least {MIN_BASE_FEE} stroops."
            )

        soroban_resource_fee = 0
        if inner_transaction_envelope.transaction.soroban_data:
            soroban_resource_fee = (
                inner_transaction_envelope.transaction.soroban_data.resource_fee.int64
            )

        inner_include_fee = (
            inner_transaction_envelope.transaction.fee - soroban_resource_fee
        )  # dont include soroban resource fee
        inner_base_fee = math.ceil(
            inner_include_fee / len(inner_transaction_envelope.transaction.operations)
        )

        if base_fee < inner_base_fee:
            raise ValueError(
                f"Invalid `base_fee`, it should be at least {inner_base_fee} stroops."
            )

        fee = base_fee * (len(inner_transaction_envelope.transaction.operations) + 1)
        fee += soroban_resource_fee

        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_source,
            fee=fee,
            inner_transaction_envelope=inner_transaction_envelope,
        )
        transaction_envelope = FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction,
            network_passphrase=network_passphrase,
        )
        return transaction_envelope

    @staticmethod
    def from_xdr(
        xdr: str, network_passphrase: str
    ) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
        """When you are not sure whether your XDR belongs to
        :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
        or :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`,
        you can use this function.

        An example::

            from stellar_sdk import Network, TransactionBuilder

            xdr = "AAAAAgAAAADHJNEDn33/C1uDkDfzDfKVq/4XE9IxDfGiLCfoV7riZQAAA+gCI4TVABpRPgAAAAAAAAAAAAAAAQAAAAAAAAADAAAAAUxpcmEAAAAAabIaDgm0ypyJpsVfEjZw2mO3Enq4Q4t5URKfWtqukSUAAAABVVNEAAAAAADophqGHmCvYPgHc+BjRuXHLL5Z3K3aN2CNWO9CUR2f3AAAAAAAAAAAE8G9mAADcH8AAAAAMYdBWgAAAAAAAAABV7riZQAAAEARGCGwYk/kEB2Z4UL20y536evnwmmSc4c2FnxlvUcPZl5jgWHcNwY8LTpFhdrUN9TZWciCRp/JCZYa0SJh8cYB"
            te = TransactionBuilder.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
            print(te)

        :param xdr: Transaction envelope XDR
        :param network_passphrase: The network to connect to for verifying and retrieving
            additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
        :raises: :exc:`ValueError <stellar_sdk.exceptions.ValueError>` - XDR is neither :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
            nor :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
        """
        if FeeBumpTransactionEnvelope.is_fee_bump_transaction_envelope(xdr):
            return FeeBumpTransactionEnvelope.from_xdr(xdr, network_passphrase)
        return TransactionEnvelope.from_xdr(xdr, network_passphrase)

    def add_time_bounds(self, min_time: int, max_time: int) -> "TransactionBuilder":
        """Sets a timeout precondition on the transaction.

        Because of the distributed nature of the Stellar network it is possible
        that the status of your transaction will be determined after a long time
        if the network is highly congested. If you want to be sure to receive the
        status of the transaction within a given period you should set
        the :class:`TimeBounds` with `max_time` on the transaction (this is
        what :func:`set_timeout` does internally).

        Please note that Horizon may still return **504 Gateway Timeout**
        error, even for short timeouts. In such case you need to resubmit the same
        transaction again without making any changes to receive a status. This
        method is using the machine system time (UTC), make sure it is set
        correctly.

        Add a UNIX timestamp, determined by ledger time, of a lower and
        upper bound of when this transaction will be valid. If a transaction is
        submitted too early or too late, it will fail to make it into the
        transaction set. `max_time` equal ``0`` means that it's not set.

        :param min_time: the UNIX timestamp (in seconds)
        :param max_time: the UNIX timestamp (in seconds)
        :return: This builder instance.

        """
        self.time_bounds = TimeBounds(min_time, max_time)
        return self

    def set_timeout(self, timeout: int) -> "TransactionBuilder":
        """Set timeout for the transaction, actually set a :class:`TimeBounds`.

        :param timeout: timeout in second.
        :return: This builder instance.
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`: if `time_bound` is already set.
        """
        if self.time_bounds:
            raise ValueError(
                "TimeBounds has been already set - setting timeout would overwrite it."
            )
        timeout_timestamp = int(time.time()) + timeout
        self.time_bounds = TimeBounds(min_time=0, max_time=timeout_timestamp)
        return self

    def set_ledger_bounds(
        self, min_ledger: int, max_ledger: int
    ) -> "TransactionBuilder":
        """If you want to prepare a transaction which will only
        be valid within some range of ledgers, you can set a `ledger_bounds` precondition.
        Internally this will set the :class:`LedgerBounds` preconditions.

        :param min_ledger: The minimum ledger this transaction is valid at, or after.
            Cannot be negative. If the value is ``0``, the transaction is valid immediately.
        :param max_ledger: The maximum ledger this transaction is valid before.
            Cannot be negative. If the value is ``0``, the transaction is valid indefinitely.
        :return: This builder instance.
        """
        self.ledger_bounds = LedgerBounds(min_ledger, max_ledger)
        return self

    def set_min_sequence_number(self, min_sequence_number: int) -> "TransactionBuilder":
        """If you want to prepare a transaction which will be valid only while the account sequence number is
        **min_sequence_number <= source_account_sequence_number < tx.sequence**.

        Note that after execution the account's sequence number is always raised to `tx.sequence`.
        Internally this will set the `min_sequence_number` precondition.

        :param min_sequence_number: The minimum source account sequence
            number this transaction is valid for. If the value is ``None``
            the transaction is valid when **source account's sequence number == tx.sequence - 1**.
        :return: This builder instance.
        """
        self.min_sequence_number = min_sequence_number
        return self

    def set_min_sequence_age(self, min_sequence_age: int) -> "TransactionBuilder":
        """For the transaction to be valid, the current ledger time must be
        at least `min_sequence_age` greater than source account's `sequence_time`.
        Internally this will set the `min_sequence_age` precondition.

        :param min_sequence_age: The minimum amount of time between
            source account sequence time and the ledger time when this transaction
            will become valid. If the value is ``0`` or ``None``, the transaction is unrestricted
            by the account sequence age. Cannot be negative.
        :return: This builder instance.
        """
        self.min_sequence_age = min_sequence_age
        return self

    def set_min_sequence_ledger_gap(
        self, min_sequence_ledger_gap: int
    ) -> "TransactionBuilder":
        """For the transaction to be valid, the current ledger number must be at least
        `min_sequence_ledger_gap` greater than source account's ledger sequence.
        Internally this will set the `min_sequence_ledger_gap` precondition.

        :param min_sequence_ledger_gap: The minimum number of ledgers between source account
            sequence and the ledger number when this transaction will become valid.
            If the value is ``0`` or ``None``, the transaction is unrestricted by the account sequence
            ledger. Cannot be negative.
        :return: This builder instance.
        """
        self.min_sequence_ledger_gap = min_sequence_ledger_gap
        return self

    def set_soroban_data(
        self, soroban_data: Union[stellar_xdr.SorobanTransactionData, str]
    ) -> "TransactionBuilder":
        """Set the SorobanTransactionData. For non-contract(non-Soroban) transactions, this setting has no effect.

        In the case of Soroban transactions, set to an instance of
        SorobanTransactionData. This can typically be obtained from the simulation
        response based on a transaction with a InvokeHostFunctionOp.
        It provides necessary resource estimations for contract invocation.

        :param soroban_data: The SorobanTransactionData as XDR object or base64 encoded string.
        :return: This builder instance.
        """
        self.soroban_data = SorobanDataBuilder.from_xdr(soroban_data).build()
        return self

    def add_extra_signer(
        self, signer_key: Union[SignerKey, SignedPayloadSigner, str]
    ) -> "TransactionBuilder":
        """For the transaction to be valid, there must be a signature corresponding to every
        Signer in this array, even if the signature is not otherwise required by
        the source account or operations.
        Internally this will set the :class:`SignerKey` precondition.

        :param signer_key: The signer key
        :return: This builder instance.
        """
        if isinstance(signer_key, str):
            signer_key = SignerKey.from_encoded_signer_key(signer_key)
        if isinstance(signer_key, SignedPayloadSigner):
            signer_key = SignerKey.ed25519_signed_payload(signer_key)
        self.extra_signers.append(signer_key)
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
            if `memo_text` is not a valid text memo.
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
            if `memo_id` is not a valid id memo.

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
            if `memo_hash` is not a valid hash memo.
        """
        memo = HashMemo(memo_hash)
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
            if `memo_return` is not a valid return hash memo.
        """
        memo = ReturnHashMemo(memo_return)
        return self.add_memo(memo)

    def append_operation(self, operation: Operation) -> "TransactionBuilder":
        """Add an operation to the builder instance

        :param operation: an operation
        :return: This builder instance.
        """
        self.operations.append(operation)
        return self

    def append_create_account_op(
        self,
        destination: str,
        starting_balance: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
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
        asset: Union[Asset, LiquidityPoolAsset],
        limit: Union[str, Decimal] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ChangeTrust <stellar_sdk.operation.ChangeTrust>`
        operation to the list of operations.

        :param asset: The asset for the trust line.
        :param limit: The limit for the asset, defaults to max int64(``922337203685.4775807``).
            If the limit is set to ``"0"`` it deletes the trustline.
        :param source: The source address to add the trustline to.
        :return: This builder instance.
        """

        op = ChangeTrust(asset, limit, source)
        return self.append_operation(op)

    def append_payment_op(
        self,
        destination: Union[MuxedAccount, str],
        asset: Asset,
        amount: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`Payment <stellar_sdk.operation.Payment>` operation
        to the list of operations.

        :param destination: The destination account ID.
        :param asset: The asset to send.
        :param amount: The amount to send.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """

        op = Payment(destination, asset, amount, source)
        return self.append_operation(op)

    def append_path_payment_strict_receive_op(
        self,
        destination: Union[MuxedAccount, str],
        send_asset: Asset,
        send_max: Union[str, Decimal],
        dest_asset: Asset,
        dest_amount: Union[str, Decimal],
        path: Sequence[Asset],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`PathPaymentStrictReceive <stellar_sdk.operation.PathPaymentStrictReceive>`
        operation to the list of operations.

        :param destination: The destination account to send to.
        :param send_asset: The `asset` to pay with.
        :param send_max: The maximum amount of `send_asset` to send.
        :param dest_asset: The asset the `destination` will receive.
        :param dest_amount: The amount the `destination` receives.
        :param path: A list of Asset objects to use as the path.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """

        op = PathPaymentStrictReceive(
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path,
            source=source,
        )
        return self.append_operation(op)

    def append_path_payment_strict_send_op(
        self,
        destination: Union[MuxedAccount, str],
        send_asset: Asset,
        send_amount: Union[str, Decimal],
        dest_asset: Asset,
        dest_min: Union[str, Decimal],
        path: Sequence[Asset],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`PathPaymentStrictSend <stellar_sdk.operation.PathPaymentStrictSend>`
        operation to the list of operations.

        :param destination: The destination account to send to.
        :param send_asset: The `asset` to pay with.
        :param send_amount: Amount of `send_asset` to send.
        :param dest_asset: The asset the `destination` will receive.
        :param dest_min: The minimum amount of `dest_asset` to be received.
        :param path: A list of Asset objects to use as the path.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = PathPaymentStrictSend(
            destination=destination,
            send_asset=send_asset,
            send_amount=send_amount,
            dest_asset=dest_asset,
            dest_min=dest_min,
            path=path,
            source=source,
        )
        return self.append_operation(op)

    def append_allow_trust_op(
        self,
        trustor: str,
        asset_code: str,
        authorize: Union[TrustLineEntryFlag, bool],
        source: Optional[Union[MuxedAccount, str]] = None,
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
        warnings.warn(
            "Use `stellar_sdk.transaction_builder.TransactionBuilder.append_set_trust_line_flags_op` instead.",
            DeprecationWarning,
        )
        op = AllowTrust(trustor, asset_code, authorize, source)
        return self.append_operation(op)

    def append_set_options_op(
        self,
        inflation_dest: str = None,
        clear_flags: Union[int, AuthorizationFlag] = None,
        set_flags: Union[int, AuthorizationFlag] = None,
        master_weight: int = None,
        low_threshold: int = None,
        med_threshold: int = None,
        high_threshold: int = None,
        home_domain: str = None,
        signer: Signer = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`SetOptions <stellar_sdk.operation.SetOptions>`
        operation to the list of operations.

        :param inflation_dest: Account of the inflation destination.
        :param clear_flags: Indicates which flags to clear. For details about the flags,
            please refer to the `Control Access to an Asset - Flag <https://developers.stellar.org/docs/issuing-assets/control-asset-access/#flags>`__.
            The `bit mask <https://en.wikipedia.org/wiki/Bit_field>`_ integer subtracts from the existing flags of the account.
            This allows for setting specific bits without knowledge of existing flags, you can also use
            :class:`stellar_sdk.operation.set_options.AuthorizationFlag`

            * AUTHORIZATION_REQUIRED = 1
            * AUTHORIZATION_REVOCABLE = 2
            * AUTHORIZATION_IMMUTABLE = 4
            * AUTHORIZATION_CLAWBACK_ENABLED = 8

        :param set_flags: Indicates which flags to set. For details about the flags,
            please refer to the `Control Access to an Asset - Flag <https://developers.stellar.org/docs/issuing-assets/control-asset-access/#flags>`__.
            The bit mask integer adds onto the existing flags of the account.
            This allows for setting specific bits without knowledge of existing flags, you can also use
            :class:`stellar_sdk.operation.set_options.AuthorizationFlag`

            * AUTHORIZATION_REQUIRED = 1
            * AUTHORIZATION_REVOCABLE = 2
            * AUTHORIZATION_IMMUTABLE = 4
            * AUTHORIZATION_CLAWBACK_ENABLED = 8

        :param master_weight: A number from 0-255 (inclusive) representing the weight of the master key.
            If the weight of the master key is updated to 0, it is effectively disabled.
        :param low_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a low threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
        :param med_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a medium threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
        :param high_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
            operations it performs that have `a high threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
        :param home_domain: sets the home domain used for
            reverse `federation <https://developers.stellar.org/docs/glossary/federation/>`_ lookup.
        :param signer: Add, update, or remove a signer from the account.
        :param source: The source account for the operation. Defaults to the transaction's source account.
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
        self,
        account_id: str,
        weight: int,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Add a ed25519 public key signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param account_id: The account id of the new ed25519_public_key signer.
            (ex. ``"GDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH2354AD"``)
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.
        """
        signer = Signer.ed25519_public_key(account_id=account_id, weight=weight)
        return self.append_set_options_op(signer=signer, source=source)

    def append_hashx_signer(
        self,
        sha256_hash: Union[bytes, str],
        weight: int,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Add a sha256 hash(HashX) signer to an account via a :class:`SetOptions
        <stellar_sdk.operation.SetOptions` operation. This is a helper
        function for :meth:`append_set_options_op`.

        :param sha256_hash: The address of the new sha256 hash(hashX) signer,
            a 32 byte hash, hex encoded string or encode strkey.
            (ex. ``"XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL"``,
            ``"da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"`` or bytes)
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.
        """
        if isinstance(sha256_hash, str) and is_valid_hash(sha256_hash):
            sha256_hash = hex_to_bytes(sha256_hash)
        signer = Signer.sha256_hash(sha256_hash=sha256_hash, weight=weight)
        return self.append_set_options_op(signer=signer, source=source)

    def append_pre_auth_tx_signer(
        self, pre_auth_tx_hash: Union[str, bytes], weight: int, source=None
    ) -> "TransactionBuilder":
        """Add a PreAuthTx signer to an account via a :class:`SetOptions <stellar_sdk.operation.SetOptions` operation.
        This is a helper function for :meth:`append_set_options_op`.

        :param pre_auth_tx_hash: The address of the new preAuthTx signer - obtained by calling `hash` on
            the :class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`,
            a 32 byte hash, hex encoded string or encode strkey.
            (ex. ``"TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS"``,
            ``"da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"`` or bytes)
        :param weight: The weight of the new signer.
        :param source: The source account that is adding a signer to its
            list of signers.
        :return: This builder instance.
        """
        if isinstance(pre_auth_tx_hash, str) and is_valid_hash(pre_auth_tx_hash):
            pre_auth_tx_hash = hex_to_bytes(pre_auth_tx_hash)
        signer = Signer.pre_auth_tx(pre_auth_tx_hash=pre_auth_tx_hash, weight=weight)
        return self.append_set_options_op(signer=signer, source=source)

    def append_manage_buy_offer_op(
        self,
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        offer_id: int = 0,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageBuyOffer <stellar_sdk.operation.ManageBuyOffer>`
        operation to the list of operations.

        :param selling: What you're selling.
        :param buying: What you're buying.
        :param amount: Amount being bought. if set to ``0``, delete the offer.
        :param price: Price of thing being bought in terms of what you are selling.
        :param offer_id: If ``0``, will create a new offer (default). Otherwise,
            edits an existing offer.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """

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
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        offer_id: int = 0,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageSellOffer <stellar_sdk.operation.ManageSellOffer>`
        operation to the list of operations.

        :param selling: What you're selling.
        :param buying: What you're buying.
        :param amount: The total amount you're selling. If ``0``, deletes the offer.
        :param price: Price of 1 unit of `selling` in terms of `buying`.
        :param offer_id: If ``0``, will create a new offer (default). Otherwise,
            edits an existing offer.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """

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
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`CreatePassiveSellOffer
        <stellar_sdk.operation.CreatePassiveSellOffer>` operation to the list of
        operations.

        :param selling: What you're selling.
        :param buying: What you're buying.
        :param amount: The total amount you're selling.
        :param price: Price of 1 unit of `selling` in terms of `buying`.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """

        op = CreatePassiveSellOffer(selling, buying, amount, price, source)
        return self.append_operation(op)

    def append_account_merge_op(
        self,
        destination: Union[MuxedAccount, str],
        source: Optional[Union[MuxedAccount, str]] = None,
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

    def append_inflation_op(
        self, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
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
        self,
        data_name: str,
        data_value: Union[str, bytes, None],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`ManageData <stellar_sdk.operation.ManageData>`
        operation to the list of operations.

        :param data_name: If this is a new Name
            it will add the given name/value pair to the account. If this Name
            is already present then the associated value will be modified. Up to 64 bytes long.
        :param data_value: If not present then the existing `data_name` will be deleted.
            If present then this value will be set in the DataEntry. Up to 64 bytes long.
        :param source: The source account on which data is being managed.
            operation.
        :return: This builder instance.

        """
        op = ManageData(data_name, data_value, source)
        return self.append_operation(op)

    def append_bump_sequence_op(
        self, bump_to: int, source: Optional[Union[MuxedAccount, str]] = None
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
        claimants: Sequence[Claimant],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`CreateClaimableBalance <stellar_sdk.operation.CreateClaimableBalance>`
        operation to the list of operations.

        :param asset: The asset for the claimable balance.
        :param amount: the amount of the asset.
        :param claimants: A list of Claimants.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        """
        op = CreateClaimableBalance(asset, amount, claimants, source)
        return self.append_operation(op)

    def append_claim_claimable_balance_op(
        self, balance_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append a :class:`ClaimClaimableBalance <stellar_sdk.operation.ClaimClaimableBalance>`
        operation to the list of operations.

        :param balance_id: The claimable balance id to be claimed.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        """
        op = ClaimClaimableBalance(balance_id, source)
        return self.append_operation(op)

    def append_begin_sponsoring_future_reserves_op(
        self, sponsored_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append a :class:`BeginSponsoringFutureReserves <stellar_sdk.operation.BeginSponsoringFutureReserves>`
        operation to the list of operations.

        :param sponsored_id: The sponsored account id.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = BeginSponsoringFutureReserves(sponsored_id, source)
        return self.append_operation(op)

    def append_end_sponsoring_future_reserves_op(
        self, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append a :class:`EndSponsoringFutureReserves <stellar_sdk.operation.EndSponsoringFutureReserves>`
        operation to the list of operations.

        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = EndSponsoringFutureReserves(source)
        return self.append_operation(op)

    def append_revoke_account_sponsorship_op(
        self, account_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for an account to the list of operations.

        :param account_id: The sponsored account ID.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_account_sponsorship(account_id, source)
        return self.append_operation(op)

    def append_revoke_trustline_sponsorship_op(
        self,
        account_id: str,
        asset: Union[Asset, LiquidityPoolId],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a trustline to the list of operations.

        :param account_id: The account ID which owns the trustline.
        :param asset: The asset in the trustline.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        return self.append_operation(op)

    def append_revoke_offer_sponsorship_op(
        self,
        seller_id: str,
        offer_id: int,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for an offer to the list of operations.

        :param seller_id: The account ID which created the offer.
        :param offer_id: The offer ID.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)
        return self.append_operation(op)

    def append_revoke_data_sponsorship_op(
        self,
        account_id: str,
        data_name: str,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a data entry to the list of operations.

        :param account_id: The account ID which owns the data entry.
        :param data_name: The name of the data entry
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)
        return self.append_operation(op)

    def append_revoke_claimable_balance_sponsorship_op(
        self,
        claimable_balance_id: str,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a claimable to the list of operations.

        :param claimable_balance_id: The sponsored claimable balance ID.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_claimable_balance_sponsorship(
            claimable_balance_id, source
        )
        return self.append_operation(op)

    def append_revoke_liquidity_pool_sponsorship_op(
        self,
        liquidity_pool_id: str,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a claimable to the list of operations.

        :param liquidity_pool_id: The sponsored liquidity pool ID in hex string.
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        op = RevokeSponsorship.revoke_liquidity_pool_sponsorship(
            liquidity_pool_id, source
        )
        return self.append_operation(op)

    def append_revoke_ed25519_public_key_signer_sponsorship_op(
        self,
        account_id: str,
        signer_key: str,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for an ed25519_public_key signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the ed25519_public_key signer.
            (ex. ``"GDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH2354AD"``)
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        key = SignerKey.ed25519_public_key(signer_key)
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, key, source)
        return self.append_operation(op)

    def append_revoke_hashx_signer_sponsorship_op(
        self,
        account_id: str,
        signer_key: Union[bytes, str],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a hashx signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the hashx signer.
            (ex. ``"XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL"``,
            ``"da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"`` or bytes)
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        if isinstance(signer_key, str) and is_valid_hash(signer_key):
            signer_key = hex_to_bytes(signer_key)
        key = SignerKey.sha256_hash(signer_key)
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, key, source)
        return self.append_operation(op)

    def append_revoke_pre_auth_tx_signer_sponsorship_op(
        self,
        account_id: str,
        signer_key: Union[bytes, str],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append a :class:`RevokeSponsorship <stellar_sdk.operation.RevokeSponsorship>` operation
        for a pre_auth_tx signer to the list of operations.

        :param account_id: The account ID where the signer sponsorship is being removed from.
        :param signer_key: The account id of the pre_auth_tx signer.
            (ex. ``"TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS"``,
            ``"da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"`` or bytes)
        :param source: The source account for the operation. Defaults to the transaction's source account.
        :return: This builder instance.
        """
        if isinstance(signer_key, str) and is_valid_hash(signer_key):
            signer_key = hex_to_bytes(signer_key)
        key = SignerKey.pre_auth_tx(signer_key)
        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, key, source)
        return self.append_operation(op)

    def append_clawback_op(
        self,
        asset: Asset,
        from_: Union[MuxedAccount, str],
        amount: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`Clawback <stellar_sdk.operation.Clawback>`
        operation to the list of operations.

        :param asset: The asset being clawed back.
        :param from_: The public key of the account to claw back from.
        :param amount: The amount of the asset to claw back.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        """
        op = Clawback(asset, from_, amount, source)
        return self.append_operation(op)

    def append_clawback_claimable_balance_op(
        self, balance_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append an :class:`ClawbackClaimableBalance <stellar_sdk.operation.ClawbackClaimableBalance>`
        operation to the list of operations.

        :param balance_id: The claimable balance ID to be clawed back.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = ClawbackClaimableBalance(balance_id, source)
        return self.append_operation(op)

    def append_set_trust_line_flags_op(
        self,
        trustor: str,
        asset: Asset,
        clear_flags: TrustLineFlags = None,
        set_flags: TrustLineFlags = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`SetTrustLineFlags <stellar_sdk.operation.SetTrustLineFlags>`
        operation to the list of operations.

        :param trustor: The account whose trustline this is.
        :param asset: The asset on the trustline.
        :param clear_flags: The flags to clear.
        :param set_flags: The flags to set.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        return self.append_operation(op)

    def append_liquidity_pool_deposit_op(
        self,
        liquidity_pool_id: str,
        max_amount_a: Union[str, Decimal],
        max_amount_b: Union[str, Decimal],
        min_price: Union[str, Decimal, Price],
        max_price: Union[str, Decimal, Price],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`LiquidityPoolDeposit <stellar_sdk.operation.LiquidityPoolDeposit>`
        operation to the list of operations.

        :param liquidity_pool_id: The liquidity pool ID.
        :param max_amount_a: Maximum amount of first asset to deposit.
        :param max_amount_b: Maximum amount of second asset to deposit.
        :param min_price: Minimum deposit_a/deposit_b price.
        :param max_price: Maximum deposit_a/deposit_b price.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = LiquidityPoolDeposit(
            liquidity_pool_id, max_amount_a, max_amount_b, min_price, max_price, source
        )
        return self.append_operation(op)

    def append_liquidity_pool_withdraw_op(
        self,
        liquidity_pool_id: str,
        amount: Union[str, Decimal],
        min_amount_a: Union[str, Decimal],
        min_amount_b: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`LiquidityPoolWithdraw <stellar_sdk.operation.LiquidityPoolWithdraw>`
        operation to the list of operations.

        :param liquidity_pool_id: The liquidity pool ID.
        :param amount: Amount of pool shares to withdraw.
        :param min_amount_a: Minimum amount of first asset to withdraw.
        :param min_amount_b: Minimum amount of second asset to withdraw.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = LiquidityPoolWithdraw(
            liquidity_pool_id, amount, min_amount_a, min_amount_b, source
        )
        return self.append_operation(op)

    def append_invoke_contract_function_op(
        self,
        contract_id: str,
        function_name: str,
        parameters: Sequence[stellar_xdr.SCVal] = None,
        auth: Sequence[stellar_xdr.SorobanAuthorizationEntry] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` operation to the list of operations.

        You can use this method to invoke a contract function.

        :param contract_id: The ID of the contract to invoke.
        :param function_name: The name of the function to invoke.
        :param parameters: The parameters to pass to the method.
        :param auth: The authorizations required to execute the host function.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        if not StrKey.is_valid_contract(contract_id):
            raise ValueError("`contract_id` is invalid.")

        if parameters is None:
            parameters = []

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT,
            invoke_contract=stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(
                    sc_symbol=function_name.encode("utf-8")
                ),
                args=list(parameters),
            ),
        )
        op = InvokeHostFunction(host_function=host_function, auth=auth, source=source)
        return self.append_operation(op)

    def append_upload_contract_wasm_op(
        self,
        contract: Union[bytes, str],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` operation to the list of operations.

        You can use this method to install a contract code,
        and then use :func:`append_create_contract_op` to create a contract.

        :param contract: The contract code to install, path to a file or bytes.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """

        if isinstance(contract, str):
            with open(contract, "rb") as f:
                contract = f.read()

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM,
            wasm=contract,
        )
        op = InvokeHostFunction(host_function=host_function, auth=[], source=source)
        return self.append_operation(op)

    def append_create_contract_op(
        self,
        wasm_id: Union[bytes, str],
        address: Union[str, Address],
        salt: Optional[bytes] = None,
        auth: Sequence[stellar_xdr.SorobanAuthorizationEntry] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` operation to the list of operations.

        You can use this method to create a contract.

        :param wasm_id: The ID of the contract code to install.
        :param address: The address using to derive the contract ID.
        :param salt: The 32-byte salt to use to derive the contract ID.
        :param auth: The authorizations required to execute the host function.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        if isinstance(wasm_id, str):
            wasm_id = binascii.unhexlify(wasm_id)

        if salt is None:
            salt = os.urandom(32)
        else:
            if len(salt) != 32:
                raise ValueError("`salt` must be 32 bytes long")

        if isinstance(address, str):
            address = Address(address)

        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                from_address=stellar_xdr.ContractIDPreimageFromAddress(
                    address=address.to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(salt),
                ),
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
                stellar_xdr.Hash(wasm_id),
            ),
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )

        op = InvokeHostFunction(host_function=host_function, auth=auth, source=source)
        return self.append_operation(op)

    def append_create_stellar_asset_contract_from_asset_op(
        self,
        asset: Asset,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` operation to the list of operations.

        You can use this method to deploy a contract that wraps a classic asset.

        :param asset: The asset to wrap.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        asset_param = asset.to_xdr_object()

        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET,
                from_asset=asset_param,
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
            ),
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )

        op = InvokeHostFunction(host_function=host_function, auth=[], source=source)
        return self.append_operation(op)

    def append_create_stellar_asset_contract_from_address_op(
        self,
        address: Union[str, Address],
        salt: Optional[bytes] = None,
        auth: Sequence[stellar_xdr.SorobanAuthorizationEntry] = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> "TransactionBuilder":
        """Append an :class:`InvokeHostFunction <stellar_sdk.operation.InvokeHostFunction>` operation to the list of operations.

        You can use this method to create a new Soroban token contract.

        I do not recommend using this method, please check
        `the documentation <https://soroban.stellar.org/docs/learn/faq#should-i-issue-my-token-as-a-stellar-asset-or-a-custom-soroban-token>`__ for more information.

        :param address: The address using to derive the contract ID.
        :param salt: The 32-byte salt to use to derive the contract ID.
        :param auth: The authorizations required to execute the host function.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        if salt is None:
            salt = os.urandom(32)
        else:
            if len(salt) != 32:
                raise ValueError("`salt` must be 32 bytes long")

        if isinstance(address, str):
            address = Address(address)

        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                from_address=stellar_xdr.ContractIDPreimageFromAddress(
                    address=address.to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(salt),
                ),
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
            ),
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )

        op = InvokeHostFunction(host_function=host_function, auth=auth, source=source)
        return self.append_operation(op)

    def append_extend_footprint_ttl_op(
        self, extend_to: int, source: Optional[Union[MuxedAccount, str]] = None
    ) -> "TransactionBuilder":
        """Append an :class:`ExtendFootprintTTL <stellar_sdk.operation.ExtendFootprintTTL>` operation to the list of operations.

        :param extend_to: The number of ledgers past the LCL (last closed ledger)
            by which to extend the validity of the ledger keys in this transaction.
        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = ExtendFootprintTTL(extend_to=extend_to, source=source)
        return self.append_operation(op)

    def append_restore_footprint_op(
        self, source: Optional[Union[MuxedAccount, str]] = None
    ):
        """Append an :class:`RestoreFootprint <stellar_sdk.operation.RestoreFootprint>` operation to the list of operations.

        :param source: The source account for the operation. Defaults to the
            transaction's source account.
        :return: This builder instance.
        """
        op = RestoreFootprint(source)
        return self.append_operation(op)

    def __repr__(self):
        return (
            f"<TransactionBuilder [source_account={self.source_account}, "
            f"base_fee={self.base_fee}, network_passphrase={self.network_passphrase}, "
            f"operations={self.operations}, memo={self.memo}, "
            f"time_bounds={self.time_bounds}, "
            f"ledger_bounds={self.ledger_bounds}, "
            f"min_sequence_number={self.min_sequence_number}, "
            f"min_sequence_age={self.min_sequence_age}, "
            f"min_sequence_ledger_gap={self.min_sequence_ledger_gap}, "
            f"extra_signers={self.extra_signers}, "
            f"soroban_data={self.soroban_data}, "
            f"v1={self.v1}]>"
        )
