"""
SEP: 0011
Title: Txrep: human-readable low-level representation of Stellar transactions
Author: David Mazières
Status: Active
Created: 2018-08-31
"""
import json
from decimal import Decimal
from typing import List, Union, Optional

from ..asset import Asset
from ..memo import *
from ..network import Network
from ..operation import *
from ..price import Price
from ..signer import Signer
from ..strkey import StrKey
from ..time_bounds import TimeBounds
from ..transaction_envelope import TransactionEnvelope
from ..xdr import Xdr
from ..xdr.StellarXDR_const import OperationType

__all__ = ["to_txrep"]

true = "true"
false = "false"


def to_txrep(
    transaction_envelope: Union[TransactionEnvelope, str],
    network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
) -> str:
    """Txrep is a human-readable representation of Stellar transactions that functions like an assembly language for XDR.

    :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object
        or base64 encoded xdr
    :param network_passphrase: The network to connect, you do not need to set this value at this
        time, it is reserved for future use.
    :return: A human-readable format for Stellar transactions.
    """
    if isinstance(transaction_envelope, str):
        transaction_envelope = TransactionEnvelope.from_xdr(
            xdr=transaction_envelope, network_passphrase=network_passphrase
        )

    lines = []
    transaction = transaction_envelope.transaction
    __add_line("tx.sourceAccount", transaction.source.public_key, lines)
    __add_line("tx.fee", transaction.fee, lines)
    __add_line("tx.seqNum", transaction.sequence, lines)
    __add_time_bounds(transaction.time_bounds, lines)
    __add_memo(transaction.memo, lines)
    __add_operations(transaction.operations, lines)
    __add_line("tx.ext.v", 0, lines)
    __add_signatures(transaction_envelope.signatures, lines)
    return "\n".join(lines)


def __add_line(key: str, value: Union[str, int], lines: List[str]) -> None:
    lines.append("{}: {}".format(key, value))


def __add_time_bounds(time_bounds: TimeBounds, lines: List[str]) -> None:
    if time_bounds is None:
        __add_line("tx.timeBounds._present", false, lines)
    else:
        __add_line("tx.timeBounds._present", true, lines)
        __add_line("tx.timeBounds.minTime", time_bounds.min_time, lines)
        __add_line("tx.timeBounds.maxTime", time_bounds.max_time, lines)


def __add_memo(memo: Memo, lines: List[str]) -> None:
    if isinstance(memo, NoneMemo):
        __add_line("tx.memo.type", "MEMO_NONE", lines)
    if isinstance(memo, TextMemo):
        __add_line("tx.memo.type", "MEMO_TEXT", lines)
        # I don't think we should decode it.
        __add_line("tx.memo.text", __to_string(memo.memo_text), lines)
    if isinstance(memo, IdMemo):
        __add_line("tx.memo.type", "MEMO_ID", lines)
        __add_line("tx.memo.id", memo.memo_id, lines)
    if isinstance(memo, HashMemo):
        __add_line("tx.memo.type", "MEMO_HASH", lines)
        __add_line("tx.memo.hash", __to_opaque(memo.memo_hash), lines)
    if isinstance(memo, ReturnHashMemo):
        __add_line("tx.memo.type", "MEMO_RETURN", lines)
        __add_line("tx.memo.retHash", __to_opaque(memo.memo_return), lines)


def __add_operations(operations: List[Operation], lines: List[str]) -> None:
    __add_line("tx.operations.len", len(operations), lines)
    for index, operation in enumerate(operations):
        __add_operation(index, operation, lines)


def __add_operation(index: int, operation: Operation, lines: List[str]) -> None:
    prefix = "tx.operations[{}]".format(index)
    operation_type = OperationType[operation.type_code()]

    def add_operation_line(key: str, value: Union[str, int]) -> None:
        __add_line("{}.{}".format(prefix, key), value, lines)

    if operation.source is not None:
        add_operation_line("sourceAccount._present", true)
        add_operation_line("sourceAccount", operation.source)
    else:
        add_operation_line("sourceAccount._present", false)
    add_operation_line("body.type", operation_type)

    def add_body_line(
        key: str, value: Union[str, int, None], optional: bool = False
    ) -> None:
        operation_type = OperationType[operation.type_code()]
        key = "body.{}Op.{}".format(__to_camel_case(operation_type), key)
        if optional:
            present = True if value is not None else False
            add_operation_line("{}._present".format(key), true if present else false)
            if present:
                add_operation_line(key, value)
        else:
            add_operation_line(key, value)

    def add_signer(signer: Signer) -> None:
        if signer is None:
            return
        add_body_line("signer._present", false if signer is None else true)
        if signer.signer_key.type == Xdr.const.SIGNER_KEY_TYPE_ED25519:
            add_body_line(
                "signer.key",
                StrKey.encode_ed25519_public_key(signer.signer_key.ed25519),
            )
        if signer.signer_key.type == Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX:
            add_body_line(
                "signer.key", StrKey.encode_pre_auth_tx(signer.signer_key.preAuthTx)
            )
        if signer.signer_key.type == Xdr.const.SIGNER_KEY_TYPE_HASH_X:
            add_body_line(
                "signer.key", StrKey.encode_sha256_hash(signer.signer_key.hashX)
            )
        add_body_line("signer.weight", signer.weight)

    def add_price(price: Union[Price, str, None]) -> None:
        price = __to_price(price)
        add_body_line("price.n", price.n)
        add_body_line("price.d", price.d)

    def add_home_domain(home_domain: Optional[str]) -> None:
        if home_domain is None:
            add_body_line("homeDomain", None, True)
        else:
            add_body_line("homeDomain", __to_string(home_domain), True)

    if isinstance(operation, CreateAccount):
        add_body_line("destination", operation.destination)
        add_body_line("startingBalance", __to_amount(operation.starting_balance))
    elif isinstance(operation, Payment):
        add_body_line("destination", operation.destination)
        add_body_line("asset", __to_asset(operation.asset))
        add_body_line("amount", __to_amount(operation.amount))
    elif isinstance(operation, PathPaymentStrictReceive):
        add_body_line("sendAsset", __to_asset(operation.send_asset))
        add_body_line("sendMax", __to_amount(operation.send_max))
        add_body_line("destination", operation.destination)
        add_body_line("destAsset", __to_asset(operation.dest_asset))
        add_body_line("destAmount", __to_amount(operation.dest_amount))
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line("path[{}]".format(index), __to_asset(asset))
    elif isinstance(operation, ManageSellOffer):
        add_body_line("selling", __to_asset(operation.selling))
        add_body_line("buying", __to_asset(operation.buying))
        add_body_line("amount", __to_amount(operation.amount))
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, CreatePassiveSellOffer):
        add_body_line("selling", __to_asset(operation.selling))
        add_body_line("buying", __to_asset(operation.buying))
        add_body_line("amount", __to_amount(operation.amount))
        add_price(operation.price)
    elif isinstance(operation, SetOptions):
        add_body_line("inflationDest", operation.inflation_dest, True)
        add_body_line("clearFlags", operation.clear_flags, True)
        add_body_line("setFlags", operation.set_flags, True)
        add_body_line("masterWeight", operation.master_weight, True)
        add_body_line("lowThreshold", operation.low_threshold, True)
        add_body_line("medThreshold", operation.med_threshold, True)
        add_body_line("highThreshold", operation.high_threshold, True)
        add_home_domain(operation.home_domain)
        add_signer(operation.signer)
    elif isinstance(operation, ChangeTrust):
        add_body_line("line", __to_asset(operation.asset))
        add_body_line("limit", __to_amount(operation.limit))
    elif isinstance(operation, AllowTrust):
        add_body_line("trustor", operation.trustor)
        add_body_line("asset", operation.asset_code)
        add_body_line("authorize", true if operation.authorize else false)
    elif isinstance(operation, AccountMerge):
        # AccountMerge does not include 'accountMergeOp' prefix
        # see https://github.com/StellarCN/py-stellar-base/blob/master/.xdr/Stellar-transaction.x#L282
        add_operation_line("body.destination", operation.destination)
    elif isinstance(operation, ManageData):
        add_body_line("dataName", __to_string(operation.data_name))
        if operation.data_value is None:
            add_body_line("dataValue._present", false)
        else:
            add_body_line("dataValue._present", true)
            add_body_line("dataValue", __to_opaque(operation.data_value))
    elif isinstance(operation, BumpSequence):
        add_body_line("bumpTo", operation.bump_to)
    elif isinstance(operation, ManageBuyOffer):
        add_body_line("selling", __to_asset(operation.selling))
        add_body_line("buying", __to_asset(operation.buying))
        add_body_line("buyAmount", __to_amount(operation.amount))
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, PathPaymentStrictSend):
        add_body_line("sendAsset", __to_asset(operation.send_asset))
        add_body_line("sendAmount", __to_amount(operation.send_amount))
        add_body_line("destination", operation.destination)
        add_body_line("destAsset", __to_asset(operation.dest_asset))
        add_body_line("destMin", __to_amount(operation.dest_min))
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line("path[{}]".format(index), __to_asset(asset))
    else:
        raise NotImplementedError(
            "This operation has not been implemented yet, "
            "operation type: {}.".format(operation)
        )


def __add_signatures(
    signatures: List[Xdr.types.DecoratedSignature], lines: List[str]
) -> None:
    __add_line("signatures.len", len(signatures), lines)
    for index, signature in enumerate(signatures):
        __add_signature(index, signature, lines)


def __add_signature(
    index: int, signature: Xdr.types.DecoratedSignature, lines: List[str]
) -> None:
    prefix = "signatures[{}]".format(index)
    __add_line("{}.hint".format(prefix), __to_opaque(signature.hint), lines)
    __add_line("{}.signature".format(prefix), __to_opaque(signature.signature), lines)


def __to_asset(asset: Asset):
    if asset.is_native():
        return "native"
    return "{}:{}".format(asset.code, asset.issuer)


def __to_amount(amount: Union[Decimal, str]) -> int:
    return Operation.to_xdr_amount(amount)


def __to_price(price: Union[Price, str, Decimal]) -> Price:
    if isinstance(price, Price):
        price_fraction = price
    else:
        price_fraction = Price.from_raw_price(price)
    return price_fraction


def __to_camel_case(snake_str: str) -> str:
    components = snake_str.lower().split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def __to_string(value: Union[str, bytes]):
    if isinstance(value, str):
        return json.dumps(value)
    # We are not following the standard here, it needs more discussion.
    try:
        value = value.decode("utf-8")
    except UnicodeDecodeError:
        return __to_opaque(value)
    return json.dumps(value)


def __to_opaque(value: Union[bytes]):
    return value.hex()
