"""
SEP: 0011
Title: Txrep: human-readable low-level representation of Stellar transactions
Author: David Mazières
Status: Active
Created: 2018-08-31

TODO: v0 and v1
"""
import json
from decimal import Decimal
from enum import Enum
from typing import List, Union, Optional, Dict

from ..asset import Asset
from ..exceptions import ValueError
from ..fee_bump_transaction import FeeBumpTransaction
from ..fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from ..memo import *
from ..operation import *
from ..price import Price
from ..signer import Signer
from ..strkey import StrKey
from ..time_bounds import TimeBounds
from ..transaction import Transaction
from ..transaction_envelope import TransactionEnvelope
from ..xdr import Xdr
from ..xdr.StellarXDR_const import OperationType

__all__ = ["to_txrep", "from_txrep"]

_true = "true"
_false = "false"


class _EnvelopeType(Enum):
    ENVELOPE_TYPE_TX_V0 = "ENVELOPE_TYPE_TX_V0"
    ENVELOPE_TYPE_TX = "ENVELOPE_TYPE_TX"
    ENVELOPE_TYPE_TX_FEE_BUMP = "ENVELOPE_TYPE_TX_FEE_BUMP"


def to_txrep(
        transaction_envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
) -> str:
    """Txrep is a human-readable representation of Stellar transactions that functions like an assembly language for XDR.

    :param transaction_envelope: :class:`stellar_sdk.transaction_envelope.TransactionEnvelope` object.
    :return: A human-readable format for Stellar transactions.
    """

    is_fee_bump = isinstance(transaction_envelope, FeeBumpTransactionEnvelope)
    tx_type = _EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP.value
    if not is_fee_bump:
        if transaction_envelope.transaction.v1:
            tx_type = _EnvelopeType.ENVELOPE_TYPE_TX.value
        else:
            tx_type = _EnvelopeType.ENVELOPE_TYPE_TX_V0.value

    prefix = "feeBump.tx.innerTx.tx." if is_fee_bump else "tx."

    transaction = transaction_envelope.transaction
    if is_fee_bump:
        fee_bump_transaction_envelope = transaction_envelope
        fee_bump_transaction = fee_bump_transaction_envelope.transaction
        transaction_envelope = fee_bump_transaction.inner_transaction_envelope
        transaction = transaction_envelope.transaction

    lines = []

    _add_line("type", tx_type, lines)
    if is_fee_bump:
        _add_line(
            "feeBump.tx.feeSource", fee_bump_transaction.fee_source.public_key, lines
        )
        _add_line(
            "feeBump.tx.fee",
            fee_bump_transaction.base_fee * (len(transaction.operations) + 1),
            lines,
        )
        _tx_type = _EnvelopeType.ENVELOPE_TYPE_TX.value if transaction.v1 else _EnvelopeType.ENVELOPE_TYPE_TX_V0.value
        _add_line("feeBump.tx.innerTx.type", _tx_type, lines)

    _add_line(f"{prefix}sourceAccount", transaction.source.public_key, lines)
    _add_line(f"{prefix}fee", transaction.fee, lines)
    _add_line(f"{prefix}seqNum", transaction.sequence, lines)
    _add_time_bounds(transaction.time_bounds, prefix, lines)
    _add_memo(transaction.memo, prefix, lines)
    _add_operations(transaction.operations, prefix, lines)
    _add_line(f"{prefix}ext.v", 0, lines)
    _add_signatures(
        transaction_envelope.signatures,
        "feeBump.tx.innerTx." if is_fee_bump else "",
        lines,
    )
    if is_fee_bump:
        _add_line("feeBump.tx.ext.v", 0, lines)
        _add_signatures(fee_bump_transaction_envelope.signatures, "feeBump.", lines)
    return "\n".join(lines)


def from_txrep(txrep: str, network_passphrase: str) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
    lines = txrep.strip().split("\n")
    raw_data_map = {}
    for line in lines:
        if line.startswith(":") or len(line.strip()) == 0:
            # remove comment line and blank line
            continue
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = remove_comment(parts[1])
            raw_data_map[key] = value

    tx_type = _EnvelopeType(get_value(raw_data_map, 'type'))
    is_fee_bump = True if tx_type == _EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP else False

    prefix = 'feeBump.tx.innerTx.tx.' if is_fee_bump else 'tx.'
    source = get_value(raw_data_map, f'{prefix}sourceAccount')
    fee = get_int_value(raw_data_map, f"{prefix}fee")
    sequence = get_int_value(raw_data_map, f'{prefix}seqNum')
    # Timebounds
    time_bounds_present = get_bool_value(raw_data_map, f'{prefix}timeBounds._present')
    time_bounds = None
    if time_bounds_present:
        min_time = get_int_value(raw_data_map, f'{prefix}timeBounds.minTime')
        max_time = get_int_value(raw_data_map, f'{prefix}timeBounds.maxTime')
        time_bounds = TimeBounds(min_time=min_time, max_time=max_time)
    # Memo
    memo_type = get_value(raw_data_map, f'{prefix}memo.type')
    if memo_type == 'MEMO_TEXT':
        memo = TextMemo(get_bytes_value(raw_data_map, f'{prefix}memo.text'))
    elif memo_type == 'MEMO_ID':
        memo = IdMemo(get_int_value(raw_data_map, f'{prefix}memo.id'))
    elif memo_type == 'MEMO_HASH':
        memo = HashMemo(get_bytes_value(raw_data_map, f'{prefix}memo.hash'))
    elif memo_type == 'MEMO_RETURN':
        memo = ReturnHashMemo(get_bytes_value(raw_data_map, f'{prefix}memo.retHash'))
    elif memo_type == 'MEMO_NONE':
        memo = NoneMemo()
    else:
        raise ValueError()

    # Operations
    operations = []
    operation_length = get_int_value(raw_data_map, f'{prefix}operations.len')
    for i in range(operation_length):
        operation = get_operation(i, raw_data_map, prefix)
        operations.append(operation)

    # Signatures
    transaction_signatures: List[Xdr.types.DecoratedSignature] = []
    prefix = 'feeBump.tx.innerTx.' if is_fee_bump else ""
    signature_length = get_int_value(raw_data_map, f'{prefix}signatures.len')
    for i in range(signature_length):
        signature = get_signature(i, raw_data_map, prefix)
        transaction_signatures.append(signature)

    v1 = True
    if is_fee_bump:
        inner_tx_type = get_value(raw_data_map, 'feeBump.tx.innerTx.type')
        if _EnvelopeType(inner_tx_type) == _EnvelopeType.ENVELOPE_TYPE_TX_V0:
            v1 = False
    else:
        v1 = tx_type == _EnvelopeType.ENVELOPE_TYPE_TX

    transaction = Transaction(
        source=source,
        sequence=sequence,
        fee=fee,
        operations=operations,
        memo=memo,
        time_bounds=time_bounds,
        v1=v1,
    )
    transaction_envelope = TransactionEnvelope(
        transaction=transaction,
        signatures=transaction_signatures,
        network_passphrase=network_passphrase
    )

    if is_fee_bump:
        fee_bump_fee_source = get_value(raw_data_map, 'feeBump.tx.feeSource')
        fee_bump_fee = get_int_value(raw_data_map, 'feeBump.tx.fee')
        fee_bump_base_fee = int(fee_bump_fee / (len(operations) + 1))
        # fee bump transaction signatures
        fee_bump_signature_length = get_int_value(raw_data_map, 'feeBump.signatures.len')
        fee_bump_transaction_signatures: List[Xdr.types.DecoratedSignature] = []
        for i in range(fee_bump_signature_length):
            signature = get_signature(i, raw_data_map, 'feeBump.')
            fee_bump_transaction_signatures.append(signature)
        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_bump_fee_source,
            base_fee=fee_bump_base_fee,
            inner_transaction_envelope=transaction_envelope
        )
        fee_bump_transaction_envelope = FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction,
            signatures=fee_bump_transaction_signatures,
            network_passphrase=network_passphrase)
        return fee_bump_transaction_envelope
    return transaction_envelope


def remove_comment(value: str) -> str:
    value = value.strip()
    if len(value) == 0:
        return value
    if value[0] == '"':
        return remove_string_value_comment(value)
    return remove_non_string_value_comment(value)


def remove_non_string_value_comment(value: str) -> str:
    parts = value.split(" ")
    return parts[0]


def remove_string_value_comment(value: str) -> str:
    v = ""
    in_escape_sequence = False
    for char in value[1:]:
        if in_escape_sequence:
            if char == 'n':
                v += '\n'
            else:
                v += char
            in_escape_sequence = False
        elif char == '\\':
            in_escape_sequence = True
        elif char == '"':
            v += char
            break
        else:
            v += char
    return v


def get_signature(index: int, raw_data_map: Dict[str, str], prefix: str) -> Xdr.types.DecoratedSignature:
    hint = get_bytes_value(raw_data_map, f'{prefix}signatures[{index}].hint')
    signature = get_bytes_value(raw_data_map, f'{prefix}signatures[{index}].signature')
    return Xdr.types.DecoratedSignature(hint, signature)


def get_operation(index, raw_data_map, tx_prefix):
    prefix = f'{tx_prefix}operations[{index}].body.'
    source_account_id = None
    if get_bool_value(raw_data_map, f'{tx_prefix}operations[{index}].sourceAccount._present'):
        source_account_id = get_value(raw_data_map, f'{tx_prefix}operations[{index}].sourceAccount')
    operation_type = get_value(raw_data_map, f'{prefix}type')
    if operation_type == OperationType[AccountMerge.type_code()]:
        return get_account_merge_op(source_account_id, tx_prefix, raw_data_map, index)
    elif operation_type == OperationType[AllowTrust.type_code()]:
        operation_prefix = prefix + 'allowTrustOp.'
        return get_allow_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[BumpSequence.type_code()]:
        operation_prefix = prefix + 'bumpSequenceOp.'
        return get_bump_sequence_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[ChangeTrust.type_code()]:
        operation_prefix = prefix + 'changeTrustOp.'
        return get_change_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[CreateAccount.type_code()]:
        operation_prefix = prefix + 'createAccountOp.'
        return get_create_account_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[CreatePassiveSellOffer.type_code()]:
        operation_prefix = prefix + 'createPassiveSellOfferOp.'
        return get_create_passive_sell_offer_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[Inflation.type_code()]:
        return get_inflation_op(source_account_id)
    elif operation_type == OperationType[ManageBuyOffer.type_code()]:
        operation_prefix = prefix + 'manageBuyOfferOp.'
        return get_manage_buy_offer_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[ManageData.type_code()]:
        operation_prefix = prefix + 'manageDataOp.'
        return get_manage_data_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[ManageSellOffer.type_code()]:
        operation_prefix = prefix + 'manageSellOfferOp.'
        return get_manage_sell_offer_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[PathPaymentStrictReceive.type_code()]:
        operation_prefix = prefix + 'pathPaymentStrictReceiveOp.'
        return get_path_payment_strict_receive_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[PathPaymentStrictSend.type_code()]:
        operation_prefix = prefix + 'pathPaymentStrictSendOp.'
        return get_path_payment_strict_send_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[Payment.type_code()]:
        operation_prefix = prefix + 'paymentOp.'
        return get_payment_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == OperationType[SetOptions.type_code()]:
        operation_prefix = prefix + 'setOptionsOp.'
        return get_set_options_op(source_account_id, operation_prefix, raw_data_map)
    else:
        raise ValueError


def get_set_options_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> SetOptions:
    inflation_dest = None
    clear_flags = None
    set_flags = None
    master_weight = None
    low_threshold = None
    med_threshold = None
    high_threshold = None
    signer = None
    home_domain = None
    if get_bool_value(raw_data_map, f'{operation_prefix}.inflationDest._present'):
        inflation_dest = get_value(raw_data_map, f'{operation_prefix}.inflationDest')
    if get_bool_value(raw_data_map, f'{operation_prefix}.clearFlags._present'):
        clear_flags = get_int_value(raw_data_map, f'{operation_prefix}.clearFlags')
    if get_bool_value(raw_data_map, f'{operation_prefix}.setFlags._present'):
        set_flags = get_int_value(raw_data_map, f'{operation_prefix}.setFlags')
    if get_bool_value(raw_data_map, f'{operation_prefix}.masterWeight._present'):
        master_weight = get_int_value(raw_data_map, f'{operation_prefix}.masterWeight')
    if get_bool_value(raw_data_map, f'{operation_prefix}.lowThreshold._present'):
        low_threshold = get_int_value(raw_data_map, f'{operation_prefix}.lowThreshold')
    if get_bool_value(raw_data_map, f'{operation_prefix}.medThreshold._present'):
        med_threshold = get_int_value(raw_data_map, f'{operation_prefix}.medThreshold')
    if get_bool_value(raw_data_map, f'{operation_prefix}.highThreshold._present'):
        high_threshold = get_int_value(raw_data_map, f'{operation_prefix}.highThreshold')
    if get_bool_value(raw_data_map, f'{operation_prefix}.signer._present'):
        weight = get_int_value(raw_data_map, f'{operation_prefix}.signer.weight')
        key = get_value(raw_data_map, f'{operation_prefix}.signer.key')
        if key.startswith("G"):
            signer = Signer.ed25519_public_key(key, weight)
        elif key.startswith("X"):
            key = StrKey.decode_sha256_hash(key)
            signer = Signer.sha256_hash(key, weight)
        elif key.startswith("T"):
            key = StrKey.decode_pre_auth_tx(key)
            signer = Signer.pre_auth_tx(key, weight)
        else:
            raise ValueError

    if get_bool_value(raw_data_map, f'{operation_prefix}.homeDomain._present'):
        home_domain = get_bytes_value(raw_data_map, f'{operation_prefix}.homeDomain')

    return SetOptions(inflation_dest=inflation_dest, clear_flags=clear_flags, set_flags=set_flags,
                      master_weight=master_weight,
                      low_threshold=low_threshold, med_threshold=med_threshold, high_threshold=high_threshold,
                      signer=signer,
                      home_domain=home_domain, source=source)


def get_path_payment_strict_receive_op(source: str, operation_prefix: str,
                                       raw_data_map: Dict[str, str]) -> PathPaymentStrictReceive:
    send_asset = get_asset(raw_data_map, f'{operation_prefix}.sendAsset')
    send_max = get_amount_value(raw_data_map, f'{operation_prefix}.sendMax')
    destination = get_value(raw_data_map, f'{operation_prefix}.destination')
    dest_asset = get_asset(raw_data_map, f'{operation_prefix}.destAsset')
    dest_amount = get_amount_value(raw_data_map, f'{operation_prefix}.destAmount')
    path_length = get_int_value(raw_data_map, f'{operation_prefix}.path.len')
    path = []
    for i in range(path_length):
        asset = get_asset(raw_data_map, f'{operation_prefix}.path[{i}]')
        path.append(asset)
    return PathPaymentStrictReceive(destination=destination, send_asset=send_asset, send_max=send_max,
                                    dest_asset=dest_asset,
                                    dest_amount=dest_amount, path=path, source=source)


def get_path_payment_strict_send_op(source: str, operation_prefix: str,
                                    raw_data_map: Dict[str, str]) -> PathPaymentStrictSend:
    send_asset = get_asset(raw_data_map, f'{operation_prefix}.sendAsset')
    send_amount = get_amount_value(raw_data_map, f'{operation_prefix}.sendAmount')
    destination = get_value(raw_data_map, f'{operation_prefix}.destination')
    dest_asset = get_asset(raw_data_map, f'{operation_prefix}.destAsset')
    dest_min = get_amount_value(raw_data_map, f'{operation_prefix}.destMin')
    path_length = get_int_value(raw_data_map, f'{operation_prefix}.path.len')
    path = []
    for i in range(path_length):
        asset = get_asset(raw_data_map, f'{operation_prefix}.path[{i}]')
        path.append(asset)
    return PathPaymentStrictSend(destination=destination, send_asset=send_asset, send_amount=send_amount,
                                 dest_asset=dest_asset,
                                 dest_min=dest_min, path=path, source=source)


def get_create_passive_sell_offer_op(source: str, operation_prefix: str,
                                     raw_data_map: Dict[str, str]) -> CreatePassiveSellOffer:
    selling = get_asset(raw_data_map, f'{operation_prefix}.selling')
    buying = get_asset(raw_data_map, f'{operation_prefix}.buying')
    amount = get_amount_value(raw_data_map, f'{operation_prefix}.buyAmount')
    price_n = get_int_value(raw_data_map, f'{operation_prefix}.price.n')
    price_d = get_int_value(raw_data_map, f'{operation_prefix}.price.d')
    price = Price(n=price_n, d=price_d)
    return CreatePassiveSellOffer(selling=selling, buying=buying, amount=amount, price=price, source=source)


def get_manage_buy_offer_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> ManageBuyOffer:
    selling = get_asset(raw_data_map, f'{operation_prefix}.selling')
    buying = get_asset(raw_data_map, f'{operation_prefix}.buying')
    amount = get_amount_value(raw_data_map, f'{operation_prefix}.buyAmount')
    offer_id = get_int_value(raw_data_map, f'{operation_prefix}.offerID')
    price_n = get_int_value(raw_data_map, f'{operation_prefix}.price.n')
    price_d = get_int_value(raw_data_map, f'{operation_prefix}.price.d')
    price = Price(n=price_n, d=price_d)
    return ManageBuyOffer(selling=selling, buying=buying, amount=amount, price=price, offer_id=offer_id, source=source)


def get_manage_sell_offer_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> ManageSellOffer:
    selling = get_asset(raw_data_map, f'{operation_prefix}.selling')
    buying = get_asset(raw_data_map, f'{operation_prefix}.buying')
    amount = get_amount_value(raw_data_map, f'{operation_prefix}.amount')
    offer_id = get_int_value(raw_data_map, f'{operation_prefix}.offerID')
    price_n = get_int_value(raw_data_map, f'{operation_prefix}.price.n')
    price_d = get_int_value(raw_data_map, f'{operation_prefix}.price.d')
    price = Price(n=price_n, d=price_d)
    return ManageSellOffer(selling=selling, buying=buying, amount=amount, price=price, offer_id=offer_id, source=source)


def get_payment_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> Payment:
    destination = get_value(raw_data_map, f'{operation_prefix}destination')
    asset = get_asset(raw_data_map, f'{operation_prefix}asset')
    amount = get_amount_value(raw_data_map, f'{operation_prefix}amount')
    return Payment(destination=destination, asset=asset, amount=amount, source=source)


def decode_asset(asset: str) -> Asset:
    # native (or any string up to 12 characters not containing an unescaped colon) for the native asset
    if ":" not in asset and len(asset) <= 12:
        return Asset.native()
    parts = asset.split(":")
    if len(parts) != 2:
        raise ValueError()
    return Asset(parts[0], parts[1])


def get_manage_data_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> ManageData:
    data_name = get_value(raw_data_map, f'{operation_prefix}.dataName')
    data_value = None
    if get_bool_value(raw_data_map, f'{operation_prefix}.dataValue._present'):
        data_value = get_bytes_value(raw_data_map, f'{operation_prefix}.dataValue')
    return ManageData(data_name=data_name, data_value=data_value, source=source)


def get_bump_sequence_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> BumpSequence:
    bump_to = get_int_value(raw_data_map, f'{operation_prefix}.bumpTo')
    return BumpSequence(bump_to=bump_to, source=source)


def get_allow_trust_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> AllowTrust:
    trustor = get_value(raw_data_map, f'{operation_prefix}.trustor')
    asset_code = get_value(raw_data_map, f'{operation_prefix}.asset')
    authorize = get_bool_value(raw_data_map, f'{operation_prefix}.authorize')
    return AllowTrust(trustor=trustor, asset_code=asset_code, authorize=authorize, source=source)


def get_change_trust_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> ChangeTrust:
    line = get_asset(raw_data_map, f'{operation_prefix}.line')
    limit = get_amount_value(raw_data_map, f'{operation_prefix}.limit')
    return ChangeTrust(asset=line, limit=limit, source=source)


def get_inflation_op(source: str) -> Inflation:
    return Inflation(source=source)


def get_account_merge_op(source: str, transaction_prefix: str, raw_data_map: Dict[str, str],
                         index: int) -> AccountMerge:
    destination = get_value(raw_data_map, f'{transaction_prefix}operations[{index}].body.destination')
    return AccountMerge(destination=destination, source=source)


def get_create_account_op(source: str, operation_prefix: str, raw_data_map: Dict[str, str]) -> CreateAccount:
    destination = get_value(raw_data_map, f'{operation_prefix}.destination')
    starting_balance = get_amount_value(raw_data_map, f'{operation_prefix}.startingBalance')
    return CreateAccount(destination=destination, starting_balance=starting_balance, source=source)


def get_asset(raw_data_map: Dict[str, str], key: str) -> Asset:
    return decode_asset(get_value(raw_data_map, key))


def get_amount_value(raw_data_map: Dict[str, str], key: str) -> str:
    value = get_int_value(raw_data_map, key)
    return Operation.from_xdr_amount(value)


def get_int_value(raw_data_map: Dict[str, str], key: str) -> int:
    value = get_value(raw_data_map, key)
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Failed to convert `{value}` to int type.") from e


def get_bool_value(raw_data_map: Dict[str, str], key: str) -> bool:
    value = get_value(raw_data_map, key)
    if value == _true:
        return True
    elif value == _false:
        return False
    else:
        raise ValueError(f"Failed to convert `{value}` to bool type.")


def get_bytes_value(raw_data_map: Dict[str, str], key: str) -> bytes:
    value = get_value(raw_data_map, key)
    if value[0] == '"':
        # for text memo.
        return get_string_value(raw_data_map, key).encode()
    try:
        return bytes.fromhex(value)
    except ValueError as e:
        raise ValueError(f"Failed to convert `{value}` to bytes type.") from e


def get_string_value(raw_data_map: Dict[str, str], key: str) -> str:
    value = get_value(raw_data_map, key)
    if len(value) == 0:
        return value
    return value[1:-1]


def get_value(raw_data_map: Dict[str, str], key: str) -> str:
    try:
        return raw_data_map[key]
    except KeyError as e:
        raise ValueError(f"`{key}` is missing from txrep.") from e


def _add_line(key: str, value: Union[str, int], lines: List[str]) -> None:
    lines.append(f"{key}: {value}")


def _add_time_bounds(time_bounds: TimeBounds, prefix: str, lines: List[str]) -> None:
    if time_bounds is None:
        _add_line(f"{prefix}timeBounds._present", _false, lines)
    else:
        _add_line(f"{prefix}timeBounds._present", _true, lines)
        _add_line(f"{prefix}timeBounds.minTime", time_bounds.min_time, lines)
        _add_line(f"{prefix}timeBounds.maxTime", time_bounds.max_time, lines)


def _add_memo(memo: Memo, prefix: str, lines: List[str]) -> None:
    if isinstance(memo, NoneMemo):
        _add_line(f"{prefix}memo.type", "MEMO_NONE", lines)
    if isinstance(memo, TextMemo):
        _add_line(f"{prefix}memo.type", "MEMO_TEXT", lines)
        # I don't think we should decode it.
        _add_line(f"{prefix}memo.text", _to_string(memo.memo_text), lines)
    if isinstance(memo, IdMemo):
        _add_line(f"{prefix}memo.type", "MEMO_ID", lines)
        _add_line(f"{prefix}memo.id", memo.memo_id, lines)
    if isinstance(memo, HashMemo):
        _add_line(f"{prefix}memo.type", "MEMO_HASH", lines)
        _add_line(f"{prefix}memo.hash", _to_opaque(memo.memo_hash), lines)
    if isinstance(memo, ReturnHashMemo):
        _add_line(f"{prefix}memo.type", "MEMO_RETURN", lines)
        _add_line(f"{prefix}memo.retHash", _to_opaque(memo.memo_return), lines)


def _add_operations(
        operations: List[Operation], prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}operations.len", len(operations), lines)
    for index, operation in enumerate(operations):
        _add_operation(index, operation, prefix, lines)


def _add_operation(
        index: int, operation: Operation, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}operations[{index}]."
    operation_type = OperationType[operation.type_code()]

    def add_operation_line(key: str, value: Union[str, int]) -> None:
        _add_line(f"{prefix}{key}", value, lines)

    if operation.source is not None:
        add_operation_line("sourceAccount._present", _true)
        add_operation_line("sourceAccount", operation.source)
    else:
        add_operation_line("sourceAccount._present", _false)
    add_operation_line("body.type", operation_type)

    def add_body_line(
            key: str, value: Union[str, int, None], optional: bool = False
    ) -> None:
        operation_type = OperationType[operation.type_code()]
        key = f"body.{_to_camel_case(operation_type)}Op.{key}"
        if optional:
            present = True if value is not None else False
            add_operation_line(f"{key}._present", _true if present else _false)
            if present:
                add_operation_line(key, value)
        else:
            add_operation_line(key, value)

    def add_signer(signer: Signer) -> None:
        if signer is None:
            return
        add_body_line("signer._present", _false if signer is None else _true)
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
        price = _to_price(price)
        add_body_line("price.n", price.n)
        add_body_line("price.d", price.d)

    def add_home_domain(home_domain: Optional[str]) -> None:
        if home_domain is None:
            add_body_line("homeDomain", None, True)
        else:
            add_body_line("homeDomain", _to_string(home_domain), True)

    if isinstance(operation, CreateAccount):
        add_body_line("destination", operation.destination)
        add_body_line("startingBalance", _to_amount(operation.starting_balance))
    elif isinstance(operation, Payment):
        add_body_line("destination", operation.destination)
        add_body_line("asset", _to_asset(operation.asset))
        add_body_line("amount", _to_amount(operation.amount))
    elif isinstance(operation, PathPaymentStrictReceive):
        add_body_line("sendAsset", _to_asset(operation.send_asset))
        add_body_line("sendMax", _to_amount(operation.send_max))
        add_body_line("destination", operation.destination)
        add_body_line("destAsset", _to_asset(operation.dest_asset))
        add_body_line("destAmount", _to_amount(operation.dest_amount))
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line(f"path[{index}]", _to_asset(asset))
    elif isinstance(operation, ManageSellOffer):
        add_body_line("selling", _to_asset(operation.selling))
        add_body_line("buying", _to_asset(operation.buying))
        add_body_line("amount", _to_amount(operation.amount))
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, CreatePassiveSellOffer):
        add_body_line("selling", _to_asset(operation.selling))
        add_body_line("buying", _to_asset(operation.buying))
        add_body_line("amount", _to_amount(operation.amount))
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
        add_body_line("line", _to_asset(operation.asset))
        add_body_line("limit", _to_amount(operation.limit))
    elif isinstance(operation, AllowTrust):
        add_body_line("trustor", operation.trustor)
        add_body_line("asset", operation.asset_code)
        add_body_line("authorize", _true if operation.authorize else _false)
    elif isinstance(operation, AccountMerge):
        # AccountMerge does not include 'accountMergeOp' prefix
        # see https://github.com/StellarCN/py-stellar-base/blob/master/.xdr/Stellar-transaction.x#L282
        add_operation_line("body.destination", operation.destination)
    elif isinstance(operation, ManageData):
        add_body_line("dataName", _to_string(operation.data_name))
        if operation.data_value is None:
            add_body_line("dataValue._present", _false)
        else:
            add_body_line("dataValue._present", _true)
            add_body_line("dataValue", _to_opaque(operation.data_value))
    elif isinstance(operation, BumpSequence):
        add_body_line("bumpTo", operation.bump_to)
    elif isinstance(operation, ManageBuyOffer):
        add_body_line("selling", _to_asset(operation.selling))
        add_body_line("buying", _to_asset(operation.buying))
        add_body_line("buyAmount", _to_amount(operation.amount))
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, PathPaymentStrictSend):
        add_body_line("sendAsset", _to_asset(operation.send_asset))
        add_body_line("sendAmount", _to_amount(operation.send_amount))
        add_body_line("destination", operation.destination)
        add_body_line("destAsset", _to_asset(operation.dest_asset))
        add_body_line("destMin", _to_amount(operation.dest_min))
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line(f"path[{index}]", _to_asset(asset))
    else:
        raise NotImplementedError(
            f"This operation has not been implemented yet, "
            f"operation type: {operation}."
        )


def _add_signatures(
        signatures: List[Xdr.types.DecoratedSignature], prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}signatures.len", len(signatures), lines)
    for index, signature in enumerate(signatures):
        _add_signature(index, signature, prefix, lines)


def _add_signature(
        index: int, signature: Xdr.types.DecoratedSignature, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}signatures[{index}]."
    _add_line(f"{prefix}hint", _to_opaque(signature.hint), lines)
    _add_line(f"{prefix}signature", _to_opaque(signature.signature), lines)


def _to_asset(asset: Asset):
    if asset.is_native():
        return "native"
    return f"{asset.code}:{asset.issuer}"


def _to_amount(amount: Union[Decimal, str]) -> int:
    return Operation.to_xdr_amount(amount)


def _to_price(price: Union[Price, str, Decimal]) -> Price:
    if isinstance(price, Price):
        price_fraction = price
    else:
        price_fraction = Price.from_raw_price(price)
    return price_fraction


def _to_camel_case(snake_str: str) -> str:
    components = snake_str.lower().split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def _to_string(value: Union[str, bytes]):
    if isinstance(value, str):
        return json.dumps(value)
    # We are not following the standard here, it needs more discussion.
    try:
        value = value.decode("utf-8")
    except UnicodeDecodeError:
        return _to_opaque(value)
    return json.dumps(value)


def _to_opaque(value: Union[bytes]):
    return value.hex()
