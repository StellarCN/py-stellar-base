"""
SEP: 0011
Title: Txrep: human-readable low-level representation of Stellar transactions
Author: David Mazières
Status: Active
Created: 2018-08-31
"""

import json
from decimal import Decimal
from enum import Enum
from typing import List, Union, Optional, Dict

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..exceptions import ValueError as SdkValueError
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
    """Generate a human-readable format for Stellar transactions.

    MuxAccount is currently not supported.

    Txrep is a human-readable representation of Stellar transactions that functions like an assembly language for XDR.

    See `SEP-0011 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0011.md>`_


    :param transaction_envelope: Transaction envelope object.
    :return: A human-readable format for Stellar transactions.
    """

    is_fee_bump = isinstance(transaction_envelope, FeeBumpTransactionEnvelope)
    tx_type = _EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP.value
    if not is_fee_bump:
        assert isinstance(transaction_envelope, TransactionEnvelope)
        if transaction_envelope.transaction.v1:
            tx_type = _EnvelopeType.ENVELOPE_TYPE_TX.value
        else:
            tx_type = _EnvelopeType.ENVELOPE_TYPE_TX_V0.value

    prefix = "feeBump.tx.innerTx.tx." if is_fee_bump else "tx."

    transaction = transaction_envelope.transaction
    if is_fee_bump:
        assert isinstance(transaction_envelope, FeeBumpTransactionEnvelope)
        fee_bump_transaction_envelope = transaction_envelope
        fee_bump_transaction = fee_bump_transaction_envelope.transaction
        transaction_envelope = fee_bump_transaction.inner_transaction_envelope
        transaction = transaction_envelope.transaction

    lines: List[str] = []

    _add_line("type", tx_type, lines)
    if is_fee_bump:
        assert isinstance(fee_bump_transaction, FeeBumpTransaction)
        assert isinstance(transaction, Transaction)
        _add_line(
            "feeBump.tx.feeSource", fee_bump_transaction.fee_source.public_key, lines
        )
        _add_line(
            "feeBump.tx.fee",
            fee_bump_transaction.base_fee * (len(transaction.operations) + 1),
            lines,
        )
        _add_line(
            "feeBump.tx.innerTx.type", _EnvelopeType.ENVELOPE_TYPE_TX.value, lines
        )
    assert isinstance(transaction, Transaction)
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


# Setting to ignore pass in .coveragerc will cause this function to not be counted by pytest.
def from_txrep(
    txrep: str, network_passphrase: str
) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
    """Parse txrep and generate transaction envelope object.

    MuxAccount is currently not supported.

    Txrep is a human-readable representation of Stellar transactions that functions like an assembly language for XDR.

    See `SEP-0011 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0011.md>`_

    :param txrep: a human-readable format for Stellar transactions.
    :param network_passphrase: The network to connect, you do not need to set this value at this
        time, it is reserved for future use.
    :return: A human-readable format for Stellar transactions.
    """
    raw_data_map = _get_raw_data_map(txrep)
    tx_type = _EnvelopeType(_get_value(raw_data_map, "type"))
    is_fee_bump = True if tx_type == _EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP else False

    prefix = "feeBump.tx.innerTx.tx." if is_fee_bump else "tx."

    source = _get_value(raw_data_map, f"{prefix}sourceAccount")
    fee = _get_int_value(raw_data_map, f"{prefix}fee")
    sequence = _get_int_value(raw_data_map, f"{prefix}seqNum")
    time_bounds = _get_time_bounds(raw_data_map, prefix)
    memo = _get_memo(raw_data_map, prefix)
    operations = _get_operations(raw_data_map, prefix)

    prefix = "feeBump.tx.innerTx." if is_fee_bump else ""
    transaction_signatures = _get_signatures(raw_data_map, prefix)

    v1 = (
        False
        if not is_fee_bump and tx_type == _EnvelopeType.ENVELOPE_TYPE_TX_V0
        else True
    )
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
        network_passphrase=network_passphrase,
    )

    if is_fee_bump:
        fee_bump_fee_source = _get_value(raw_data_map, "feeBump.tx.feeSource")
        fee_bump_fee = _get_int_value(raw_data_map, "feeBump.tx.fee")
        fee_bump_base_fee = int(fee_bump_fee / (len(operations) + 1))

        fee_bump_transaction_signatures = _get_signatures(raw_data_map, "feeBump.")

        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_bump_fee_source,
            base_fee=fee_bump_base_fee,
            inner_transaction_envelope=transaction_envelope,
        )
        fee_bump_transaction_envelope = FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction,
            signatures=fee_bump_transaction_signatures,
            network_passphrase=network_passphrase,
        )
        return fee_bump_transaction_envelope
    return transaction_envelope


def _get_operations(raw_data_map: Dict[str, str], prefix: str) -> List[Operation]:
    operations = []
    operation_length = _get_int_value(raw_data_map, f"{prefix}operations.len")
    for i in range(operation_length):
        operation = _get_operation(i, raw_data_map, prefix)
        operations.append(operation)
    return operations


def _get_raw_data_map(txrep: str) -> Dict[str, str]:
    lines = txrep.strip().split("\n")
    raw_data_map = {}
    for line in lines:
        if line.startswith(":") or len(line.strip()) == 0:
            # remove full-line comment and blank line
            continue
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = _remove_comment(parts[1])
            raw_data_map[key] = value
    return raw_data_map


def _get_time_bounds(raw_data_map: Dict[str, str], prefix: str) -> Optional[TimeBounds]:
    time_bounds_present = _get_bool_value(raw_data_map, f"{prefix}timeBounds._present")
    time_bounds = None
    if time_bounds_present:
        min_time = _get_int_value(raw_data_map, f"{prefix}timeBounds.minTime")
        max_time = _get_int_value(raw_data_map, f"{prefix}timeBounds.maxTime")
        time_bounds = TimeBounds(min_time=min_time, max_time=max_time)
    return time_bounds


def _get_memo(raw_data_map: Dict[str, str], prefix: str) -> Memo:
    memo_type = _get_value(raw_data_map, f"{prefix}memo.type")
    if memo_type == "MEMO_TEXT":
        return TextMemo(_get_bytes_value(raw_data_map, f"{prefix}memo.text"))
    elif memo_type == "MEMO_ID":
        return IdMemo(_get_int_value(raw_data_map, f"{prefix}memo.id"))
    elif memo_type == "MEMO_HASH":
        return HashMemo(_get_bytes_value(raw_data_map, f"{prefix}memo.hash"))
    elif memo_type == "MEMO_RETURN":
        return ReturnHashMemo(_get_bytes_value(raw_data_map, f"{prefix}memo.retHash"))
    elif memo_type == "MEMO_NONE":
        return NoneMemo()
    else:
        raise SdkValueError(
            f"`{memo_type}` is not a valid memo type, expected one of `MEMO_TEXT`, `MEMO_ID`, "
            f"`MEMO_HASH`, `MEMO_RETURN`, `MEMO_NONE`."
        )


def _remove_comment(value: str) -> str:
    value = value.strip()
    if len(value) == 0:
        return value
    if value[0] == '"':
        return _remove_string_value_comment(value)
    return _remove_non_string_value_comment(value)


def _remove_non_string_value_comment(value: str) -> str:
    parts = value.split(" ")
    return parts[0]


def _remove_string_value_comment(value: str) -> str:
    v = '"'
    in_escape_sequence = False
    for char in value[1:]:
        if in_escape_sequence:
            if char == "n":
                v += "\n"
            else:
                v += char
            in_escape_sequence = False
        elif char == "\\":
            in_escape_sequence = True
        elif char == '"':
            v += char
            break
        else:
            v += char
    return v


def _get_signature(
    index: int, raw_data_map: Dict[str, str], prefix: str
) -> stellar_xdr.DecoratedSignature:
    hint = _get_bytes_value(raw_data_map, f"{prefix}signatures[{index}].hint")
    signature = _get_bytes_value(raw_data_map, f"{prefix}signatures[{index}].signature")
    return stellar_xdr.DecoratedSignature(
        stellar_xdr.SignatureHint(hint), stellar_xdr.Signature(signature)
    )


def _get_signatures(
    raw_data_map: Dict[str, str], prefix: str
) -> List[stellar_xdr.DecoratedSignature]:
    signatures: List[stellar_xdr.DecoratedSignature] = []
    signature_length = _get_int_value(raw_data_map, f"{prefix}signatures.len")
    for i in range(signature_length):
        signature = _get_signature(i, raw_data_map, prefix)
        signatures.append(signature)
    return signatures


def _get_operation(index, raw_data_map, tx_prefix):
    prefix = f"{tx_prefix}operations[{index}].body."
    source_account_id = None
    if _get_bool_value(
        raw_data_map, f"{tx_prefix}operations[{index}].sourceAccount._present"
    ):
        source_account_id = _get_value(
            raw_data_map, f"{tx_prefix}operations[{index}].sourceAccount"
        )
    operation_type = _get_value(raw_data_map, f"{prefix}type")
    if operation_type == AccountMerge.TYPE.name:
        return _get_account_merge_op(source_account_id, tx_prefix, raw_data_map, index)
    elif operation_type == AllowTrust.TYPE.name:
        operation_prefix = prefix + "allowTrustOp."
        return _get_allow_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == BumpSequence.TYPE.name:
        operation_prefix = prefix + "bumpSequenceOp."
        return _get_bump_sequence_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == ChangeTrust.TYPE.name:
        operation_prefix = prefix + "changeTrustOp."
        return _get_change_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == CreateAccount.TYPE.name:
        operation_prefix = prefix + "createAccountOp."
        return _get_create_account_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == CreatePassiveSellOffer.TYPE.name:
        operation_prefix = prefix + "createPassiveSellOfferOp."
        return _get_create_passive_sell_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == Inflation.TYPE.name:
        return _get_inflation_op(source_account_id)
    elif operation_type == ManageBuyOffer.TYPE.name:
        operation_prefix = prefix + "manageBuyOfferOp."
        return _get_manage_buy_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == ManageData.TYPE.name:
        operation_prefix = prefix + "manageDataOp."
        return _get_manage_data_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == ManageSellOffer.TYPE.name:
        operation_prefix = prefix + "manageSellOfferOp."
        return _get_manage_sell_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == PathPaymentStrictReceive.TYPE.name:
        operation_prefix = prefix + "pathPaymentStrictReceiveOp."
        return _get_path_payment_strict_receive_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == PathPaymentStrictSend.TYPE.name:
        operation_prefix = prefix + "pathPaymentStrictSendOp."
        return _get_path_payment_strict_send_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == Payment.TYPE.name:
        operation_prefix = prefix + "paymentOp."
        return _get_payment_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == SetOptions.TYPE.name:
        operation_prefix = prefix + "setOptionsOp."
        return _get_set_options_op(source_account_id, operation_prefix, raw_data_map)
    else:
        raise SdkValueError(
            f"This operation has not been implemented yet, "
            f"operation type: {operation_type}."
        )


def _get_set_options_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> SetOptions:
    inflation_dest = None
    clear_flags = None
    set_flags = None
    master_weight = None
    low_threshold = None
    med_threshold = None
    high_threshold = None
    signer = None
    home_domain = None
    if _get_bool_value(raw_data_map, f"{operation_prefix}inflationDest._present"):
        inflation_dest = _get_value(raw_data_map, f"{operation_prefix}inflationDest")
    if _get_bool_value(raw_data_map, f"{operation_prefix}clearFlags._present"):
        clear_flags = _get_int_value(raw_data_map, f"{operation_prefix}clearFlags")
    if _get_bool_value(raw_data_map, f"{operation_prefix}setFlags._present"):
        set_flags = _get_int_value(raw_data_map, f"{operation_prefix}setFlags")
    if _get_bool_value(raw_data_map, f"{operation_prefix}masterWeight._present"):
        master_weight = _get_int_value(raw_data_map, f"{operation_prefix}masterWeight")
    if _get_bool_value(raw_data_map, f"{operation_prefix}lowThreshold._present"):
        low_threshold = _get_int_value(raw_data_map, f"{operation_prefix}lowThreshold")
    if _get_bool_value(raw_data_map, f"{operation_prefix}medThreshold._present"):
        med_threshold = _get_int_value(raw_data_map, f"{operation_prefix}medThreshold")
    if _get_bool_value(raw_data_map, f"{operation_prefix}highThreshold._present"):
        high_threshold = _get_int_value(
            raw_data_map, f"{operation_prefix}highThreshold"
        )
    if _get_bool_value(raw_data_map, f"{operation_prefix}signer._present"):
        weight = _get_int_value(raw_data_map, f"{operation_prefix}signer.weight")
        key = _get_value(raw_data_map, f"{operation_prefix}signer.key")
        if key.startswith("G"):
            signer = Signer.ed25519_public_key(key, weight)
        elif key.startswith("X"):
            sha256_hash = StrKey.decode_sha256_hash(key)
            signer = Signer.sha256_hash(sha256_hash, weight)
        elif key.startswith("T"):
            pre_auth_tx_hash = StrKey.decode_pre_auth_tx(key)
            signer = Signer.pre_auth_tx(pre_auth_tx_hash, weight)
        else:
            raise SdkValueError("Signer key should start with `G`, `X` or `T`.")

    if _get_bool_value(raw_data_map, f"{operation_prefix}homeDomain._present"):
        home_domain = _get_string_value(raw_data_map, f"{operation_prefix}homeDomain")

    return SetOptions(
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


def _get_path_payment_strict_receive_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> PathPaymentStrictReceive:
    send_asset = _get_asset(raw_data_map, f"{operation_prefix}sendAsset")
    send_max = _get_amount_value(raw_data_map, f"{operation_prefix}sendMax")
    destination = _get_value(raw_data_map, f"{operation_prefix}destination")
    dest_asset = _get_asset(raw_data_map, f"{operation_prefix}destAsset")
    dest_amount = _get_amount_value(raw_data_map, f"{operation_prefix}destAmount")
    path_length = _get_int_value(raw_data_map, f"{operation_prefix}path.len")
    path = []
    for i in range(path_length):
        asset = _get_asset(raw_data_map, f"{operation_prefix}path[{i}]")
        path.append(asset)
    return PathPaymentStrictReceive(
        destination=destination,
        send_asset=send_asset,
        send_max=send_max,
        dest_asset=dest_asset,
        dest_amount=dest_amount,
        path=path,
        source=source,
    )


def _get_path_payment_strict_send_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> PathPaymentStrictSend:
    send_asset = _get_asset(raw_data_map, f"{operation_prefix}sendAsset")
    send_amount = _get_amount_value(raw_data_map, f"{operation_prefix}sendAmount")
    destination = _get_value(raw_data_map, f"{operation_prefix}destination")
    dest_asset = _get_asset(raw_data_map, f"{operation_prefix}destAsset")
    dest_min = _get_amount_value(raw_data_map, f"{operation_prefix}destMin")
    path_length = _get_int_value(raw_data_map, f"{operation_prefix}path.len")
    path = []
    for i in range(path_length):
        asset = _get_asset(raw_data_map, f"{operation_prefix}path[{i}]")
        path.append(asset)
    return PathPaymentStrictSend(
        destination=destination,
        send_asset=send_asset,
        send_amount=send_amount,
        dest_asset=dest_asset,
        dest_min=dest_min,
        path=path,
        source=source,
    )


def _get_create_passive_sell_offer_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> CreatePassiveSellOffer:
    selling = _get_asset(raw_data_map, f"{operation_prefix}selling")
    buying = _get_asset(raw_data_map, f"{operation_prefix}buying")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    price_n = _get_int_value(raw_data_map, f"{operation_prefix}price.n")
    price_d = _get_int_value(raw_data_map, f"{operation_prefix}price.d")
    price = Price(n=price_n, d=price_d)
    return CreatePassiveSellOffer(
        selling=selling, buying=buying, amount=amount, price=price, source=source
    )


def _get_manage_buy_offer_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ManageBuyOffer:
    selling = _get_asset(raw_data_map, f"{operation_prefix}selling")
    buying = _get_asset(raw_data_map, f"{operation_prefix}buying")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}buyAmount")
    offer_id = _get_int_value(raw_data_map, f"{operation_prefix}offerID")
    price_n = _get_int_value(raw_data_map, f"{operation_prefix}price.n")
    price_d = _get_int_value(raw_data_map, f"{operation_prefix}price.d")
    price = Price(n=price_n, d=price_d)
    return ManageBuyOffer(
        selling=selling,
        buying=buying,
        amount=amount,
        price=price,
        offer_id=offer_id,
        source=source,
    )


def _get_manage_sell_offer_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ManageSellOffer:
    selling = _get_asset(raw_data_map, f"{operation_prefix}selling")
    buying = _get_asset(raw_data_map, f"{operation_prefix}buying")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    offer_id = _get_int_value(raw_data_map, f"{operation_prefix}offerID")
    price_n = _get_int_value(raw_data_map, f"{operation_prefix}price.n")
    price_d = _get_int_value(raw_data_map, f"{operation_prefix}price.d")
    price = Price(n=price_n, d=price_d)
    return ManageSellOffer(
        selling=selling,
        buying=buying,
        amount=amount,
        price=price,
        offer_id=offer_id,
        source=source,
    )


def _get_payment_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> Payment:
    destination = _get_value(raw_data_map, f"{operation_prefix}destination")
    asset = _get_asset(raw_data_map, f"{operation_prefix}asset")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    return Payment(destination=destination, asset=asset, amount=amount, source=source)


def _get_manage_data_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ManageData:
    data_name = _get_string_value(raw_data_map, f"{operation_prefix}dataName")
    data_value = None
    if _get_bool_value(raw_data_map, f"{operation_prefix}dataValue._present"):
        data_value = _get_bytes_value(raw_data_map, f"{operation_prefix}dataValue")
    return ManageData(data_name=data_name, data_value=data_value, source=source)


def _get_bump_sequence_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> BumpSequence:
    bump_to = _get_int_value(raw_data_map, f"{operation_prefix}bumpTo")
    return BumpSequence(bump_to=bump_to, source=source)


def _get_allow_trust_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> AllowTrust:
    trustor = _get_value(raw_data_map, f"{operation_prefix}trustor")
    asset_code = _get_value(raw_data_map, f"{operation_prefix}asset")
    authorize = _get_bool_value(raw_data_map, f"{operation_prefix}authorize")
    return AllowTrust(
        trustor=trustor, asset_code=asset_code, authorize=authorize, source=source
    )


def _get_change_trust_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ChangeTrust:
    line = _get_asset(raw_data_map, f"{operation_prefix}line")
    limit = _get_amount_value(raw_data_map, f"{operation_prefix}limit")
    return ChangeTrust(asset=line, limit=limit, source=source)


def _get_inflation_op(source: str) -> Inflation:
    return Inflation(source=source)


def _get_account_merge_op(
    source: str, transaction_prefix: str, raw_data_map: Dict[str, str], index: int
) -> AccountMerge:
    destination = _get_value(
        raw_data_map, f"{transaction_prefix}operations[{index}].body.destination"
    )
    return AccountMerge(destination=destination, source=source)


def _get_create_account_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> CreateAccount:
    destination = _get_value(raw_data_map, f"{operation_prefix}destination")
    starting_balance = _get_amount_value(
        raw_data_map, f"{operation_prefix}startingBalance"
    )
    return CreateAccount(
        destination=destination, starting_balance=starting_balance, source=source
    )


def _get_asset(raw_data_map: Dict[str, str], key: str) -> Asset:
    return _decode_asset(_get_value(raw_data_map, key))


def _get_amount_value(raw_data_map: Dict[str, str], key: str) -> str:
    value = _get_int_value(raw_data_map, key)
    return Operation.from_xdr_amount(value)


def _get_int_value(raw_data_map: Dict[str, str], key: str) -> int:
    value = _get_value(raw_data_map, key)
    try:
        return int(value)
    except ValueError as e:
        raise SdkValueError(f"Failed to convert `{value}` to int type.") from e


def _get_bool_value(raw_data_map: Dict[str, str], key: str) -> bool:
    value = _get_value(raw_data_map, key)
    if value == _true:
        return True
    elif value == _false:
        return False
    else:
        raise SdkValueError(f"Failed to convert `{value}` to bool type.")


def _get_bytes_value(raw_data_map: Dict[str, str], key: str) -> bytes:
    value = _get_value(raw_data_map, key)
    if value[0] == '"':
        # for text memo.
        return _get_string_value(raw_data_map, key).encode()
    try:
        return bytes.fromhex(value)
    except ValueError as e:
        raise SdkValueError(f"Failed to convert `{value}` to bytes type.") from e


def _get_string_value(raw_data_map: Dict[str, str], key: str) -> str:
    value = _get_value(raw_data_map, key)
    if len(value) == 0:
        return value
    return value[1:-1]


def _get_value(raw_data_map: Dict[str, str], key: str) -> str:
    try:
        return raw_data_map[key]
    except KeyError as e:
        raise SdkValueError(f"`{key}` is missing from txrep.") from e


def _decode_asset(asset: str) -> Asset:
    # native (or any string up to 12 characters not containing an unescaped colon) for the native asset
    if ":" not in asset and len(asset) <= 12:
        return Asset.native()
    parts = asset.split(":")
    if len(parts) != 2:
        raise SdkValueError("Failed to decode asset string.")
    return Asset(parts[0], parts[1])


def _add_line(key: str, value: Union[str, int], lines: List[str]) -> None:
    lines.append(f"{key}: {value}")


def _add_time_bounds(time_bounds: Optional[TimeBounds], prefix: str, lines: List[str]) -> None:
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


def _add_operations(operations: List[Operation], prefix: str, lines: List[str]) -> None:
    _add_line(f"{prefix}operations.len", len(operations), lines)
    for index, operation in enumerate(operations):
        _add_operation(index, operation, prefix, lines)


def _add_operation(
    index: int, operation: Operation, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}operations[{index}]."
    operation_type = operation.TYPE

    def add_operation_line(key: str, value: Union[str, int]) -> None:
        _add_line(f"{prefix}{key}", value, lines)

    if operation.source is not None:
        add_operation_line("sourceAccount._present", _true)
        add_operation_line("sourceAccount", operation.source)
    else:
        add_operation_line("sourceAccount._present", _false)
    add_operation_line("body.type", operation_type.name)

    def add_body_line(
        key: str, value: Union[str, int, None], optional: bool = False
    ) -> None:
        operation_type = operation.TYPE
        key = f"body.{_to_camel_case(operation_type.name)}Op.{key}"
        if optional:
            present = True if value is not None else False
            add_operation_line(f"{key}._present", _true if present else _false)
            if present:
                assert value is not None
                add_operation_line(key, value)
        else:
            assert value is not None
            add_operation_line(key, value)

    def add_signer(signer: Optional[Signer]) -> None:
        add_body_line("signer._present", _false if signer is None else _true)
        if signer is None:
            return
        if (
            signer.signer_key.signer_key.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519
        ):
            assert signer.signer_key.signer_key.ed25519 is not None
            add_body_line(
                "signer.key",
                StrKey.encode_ed25519_public_key(
                    signer.signer_key.signer_key.ed25519.uint256
                ),
            )
        if (
            signer.signer_key.signer_key.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
        ):
            assert signer.signer_key.signer_key.pre_auth_tx is not None
            add_body_line(
                "signer.key",
                StrKey.encode_pre_auth_tx(
                    signer.signer_key.signer_key.pre_auth_tx.uint256
                ),
            )
        if (
            signer.signer_key.signer_key.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X
        ):
            assert signer.signer_key.signer_key.hash_x is not None
            add_body_line(
                "signer.key",
                StrKey.encode_sha256_hash(signer.signer_key.signer_key.hash_x.uint256),
            )
        add_body_line("signer.weight", signer.weight)

    def add_price(price: Union[Price, str, Decimal]) -> None:
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
    elif isinstance(operation, Inflation):
        pass
    else:
        raise SdkValueError(
            f"This operation has not been implemented yet, "
            f"operation type: {operation}."
        )


def _add_signatures(
    signatures: List[stellar_xdr.DecoratedSignature], prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}signatures.len", len(signatures), lines)
    for index, signature in enumerate(signatures):
        _add_signature(index, signature, prefix, lines)


def _add_signature(
    index: int, signature: stellar_xdr.DecoratedSignature, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}signatures[{index}]."
    _add_line(f"{prefix}hint", _to_opaque(signature.hint.signature_hint), lines)
    _add_line(f"{prefix}signature", _to_opaque(signature.signature.signature), lines)


def _to_asset(asset: Asset) -> str:
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


def _to_string(value: Union[str, bytes]) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    # We are not following the standard here, it needs more discussion.
    try:
        value = value.decode("utf-8")
    except UnicodeDecodeError:
        assert isinstance(value, bytes)
        return _to_opaque(value)
    return json.dumps(value)


def _to_opaque(value: Union[bytes]) -> str:
    return value.hex()
