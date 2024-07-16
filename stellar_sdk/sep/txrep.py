"""
SEP: 0011
Title: Txrep: human-readable low-level representation of Stellar transactions
Author: David Mazières
Status: Active
Created: 2018-08-31
"""

import json
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Sequence, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..decorated_signature import DecoratedSignature
from ..fee_bump_transaction import FeeBumpTransaction
from ..fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from ..ledger_bounds import LedgerBounds
from ..liquidity_pool_asset import LiquidityPoolAsset
from ..liquidity_pool_id import LiquidityPoolId
from ..memo import *
from ..muxed_account import MuxedAccount
from ..operation import *
from ..operation.create_claimable_balance import ClaimPredicateType
from ..operation.revoke_sponsorship import RevokeSponsorshipType
from ..preconditions import Preconditions
from ..price import Price
from ..signer import Signer
from ..signer_key import SignerKey, SignerKeyType
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
            "feeBump.tx.feeSource",
            _to_muxed_account(fee_bump_transaction.fee_source),
            lines,
            comment=_to_muxed_account_comment(fee_bump_transaction.fee_source),
        )
        _add_line(
            "feeBump.tx.fee",
            fee_bump_transaction.fee,
            lines,
        )
        _add_line(
            "feeBump.tx.innerTx.type", _EnvelopeType.ENVELOPE_TYPE_TX.value, lines
        )
    assert isinstance(transaction, Transaction)
    _add_line(
        f"{prefix}sourceAccount",
        _to_muxed_account(transaction.source),
        lines,
        comment=_to_muxed_account_comment(transaction.source),
    )
    _add_line(f"{prefix}fee", transaction.fee, lines)
    _add_line(f"{prefix}seqNum", transaction.sequence, lines)
    _add_preconditions(transaction.preconditions, f"{prefix}cond.", lines)
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
    preconditions = _get_preconditions(raw_data_map, f"{prefix}cond.")
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
        preconditions=preconditions,
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

        fee_bump_transaction_signatures = _get_signatures(raw_data_map, "feeBump.")

        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_bump_fee_source,
            fee=fee_bump_fee,
            inner_transaction_envelope=transaction_envelope,
        )
        fee_bump_transaction_envelope = FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction,
            signatures=fee_bump_transaction_signatures,
            network_passphrase=network_passphrase,
        )
        return fee_bump_transaction_envelope
    return transaction_envelope


def _to_muxed_account(account: MuxedAccount) -> str:
    if account.account_muxed_id is None:
        return account.account_id
    assert account.account_muxed is not None
    return account.account_muxed


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


def _get_preconditions(raw_data_map: Dict[str, str], prefix: str) -> Preconditions:
    preconditions_type = _get_value(raw_data_map, f"{prefix}type")
    if preconditions_type == stellar_xdr.PreconditionType.PRECOND_TIME.name:
        time_bounds = _get_time_bounds(raw_data_map, prefix)
        return Preconditions(time_bounds=time_bounds)
    elif preconditions_type == stellar_xdr.PreconditionType.PRECOND_V2.name:
        time_bounds_optional = _get_time_bounds_optional(raw_data_map, prefix)
        ledger_bounds = _get_ledger_bounds_optional(raw_data_map, prefix)
        min_sequence_number_present = _get_bool_value(
            raw_data_map, f"{prefix}minSeqNum._present"
        )
        min_sequence_number = None
        if min_sequence_number_present:
            min_sequence_number = _get_int_value(raw_data_map, f"{prefix}minSeqNum")
        min_seq_age = _get_int_value(raw_data_map, f"{prefix}minSeqAge")
        min_sequence_ledger_gap = _get_int_value(
            raw_data_map, f"{prefix}minSeqLedgerGap"
        )
        extra_signers = _get_extra_signers(raw_data_map, f"{prefix}extraSigners")
        return Preconditions(
            time_bounds_optional,
            ledger_bounds,
            min_sequence_number,
            min_seq_age,
            min_sequence_ledger_gap,
            extra_signers,
        )
    elif preconditions_type == stellar_xdr.PreconditionType.PRECOND_NONE.name:
        return Preconditions()
    else:
        raise ValueError(
            f"This preconditions type has not been implemented yet, "
            f"preconditions type: {preconditions_type}."
        )


def _get_signer_key(raw_data_map: Dict[str, str], prefix: str) -> SignerKey:
    signer_key_type = _get_value(raw_data_map, f"{prefix}.type")
    if signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519.name:
        key = _get_value(raw_data_map, f"{prefix}.ed25519")
    elif signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X.name:
        key = _get_value(raw_data_map, f"{prefix}.hashX")
    elif signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX.name:
        key = _get_value(raw_data_map, f"{prefix}.preAuthTx")
    elif signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD.name:
        key = _get_value(raw_data_map, f"{prefix}.ed25519SignedPayload")
    else:
        raise ValueError(
            f"This signer key type has not been implemented yet, "
            f"signer key type: {signer_key_type}."
        )
    return SignerKey.from_encoded_signer_key(key)


def _get_extra_signers(raw_data_map: Dict[str, str], prefix: str) -> List[SignerKey]:
    extra_signers = []
    extra_signers_length = _get_int_value(raw_data_map, f"{prefix}.len")
    for i in range(extra_signers_length):
        key = _get_signer_key(raw_data_map, f"{prefix}[{i}]")
        extra_signers.append(key)
    return extra_signers


def _get_time_bounds_optional(
    raw_data_map: Dict[str, str], prefix: str
) -> Optional[TimeBounds]:
    time_bounds_present = _get_bool_value(raw_data_map, f"{prefix}timeBounds._present")
    time_bounds = None
    if time_bounds_present:
        time_bounds = _get_time_bounds(raw_data_map, prefix)
    return time_bounds


def _get_time_bounds(raw_data_map: Dict[str, str], prefix: str) -> TimeBounds:
    min_time = _get_int_value(raw_data_map, f"{prefix}timeBounds.minTime")
    max_time = _get_int_value(raw_data_map, f"{prefix}timeBounds.maxTime")
    return TimeBounds(min_time=min_time, max_time=max_time)


def _get_ledger_bounds_optional(
    raw_data_map: Dict[str, str], prefix: str
) -> Optional[LedgerBounds]:
    ledger_bounds_present = _get_bool_value(
        raw_data_map, f"{prefix}ledgerBounds._present"
    )
    ledger_bounds = None
    if ledger_bounds_present:
        ledger_bounds = _get_ledger_bounds(raw_data_map, prefix)
    return ledger_bounds


def _get_ledger_bounds(raw_data_map: Dict[str, str], prefix: str) -> LedgerBounds:
    min_ledger = _get_int_value(raw_data_map, f"{prefix}ledgerBounds.minLedger")
    max_ledger = _get_int_value(raw_data_map, f"{prefix}ledgerBounds.maxLedger")
    return LedgerBounds(min_ledger=min_ledger, max_ledger=max_ledger)


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
        raise ValueError(
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
) -> DecoratedSignature:
    hint = _get_bytes_value(raw_data_map, f"{prefix}signatures[{index}].hint")
    signature = _get_bytes_value(raw_data_map, f"{prefix}signatures[{index}].signature")
    return DecoratedSignature(hint, signature)


def _get_signatures(
    raw_data_map: Dict[str, str], prefix: str
) -> List[DecoratedSignature]:
    signatures: List[DecoratedSignature] = []
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
    if operation_type == _to_caps_with_under(AccountMerge.__name__):
        return _get_account_merge_op(source_account_id, tx_prefix, raw_data_map, index)
    elif operation_type == _to_caps_with_under(AllowTrust.__name__):
        operation_prefix = prefix + "allowTrustOp."
        return _get_allow_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(BeginSponsoringFutureReserves.__name__):
        operation_prefix = prefix + "beginSponsoringFutureReservesOp."
        return _get_begin_sponsoring_future_reserves_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(BumpSequence.__name__):
        operation_prefix = prefix + "bumpSequenceOp."
        return _get_bump_sequence_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(ChangeTrust.__name__):
        operation_prefix = prefix + "changeTrustOp."
        return _get_change_trust_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(ClaimClaimableBalance.__name__):
        operation_prefix = prefix + "claimClaimableBalanceOp."
        return _get_claim_claimable_balance_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(Clawback.__name__):
        operation_prefix = prefix + "clawbackOp."
        return _get_clawback_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(ClawbackClaimableBalance.__name__):
        operation_prefix = prefix + "clawbackClaimableBalanceOp."
        return _get_clawback_claimable_balance_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(CreateAccount.__name__):
        operation_prefix = prefix + "createAccountOp."
        return _get_create_account_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(CreateClaimableBalance.__name__):
        operation_prefix = prefix + "createClaimableBalanceOp."
        return _get_create_claimable_balance_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(CreatePassiveSellOffer.__name__):
        operation_prefix = prefix + "createPassiveSellOfferOp."
        return _get_create_passive_sell_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(EndSponsoringFutureReserves.__name__):
        return _get_end_sponsoring_future_reserves_op(source_account_id)
    elif operation_type == _to_caps_with_under(Inflation.__name__):
        return _get_inflation_op(source_account_id)
    elif operation_type == _to_caps_with_under(ManageBuyOffer.__name__):
        operation_prefix = prefix + "manageBuyOfferOp."
        return _get_manage_buy_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(ManageData.__name__):
        operation_prefix = prefix + "manageDataOp."
        return _get_manage_data_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(ManageSellOffer.__name__):
        operation_prefix = prefix + "manageSellOfferOp."
        return _get_manage_sell_offer_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(PathPaymentStrictReceive.__name__):
        operation_prefix = prefix + "pathPaymentStrictReceiveOp."
        return _get_path_payment_strict_receive_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(PathPaymentStrictSend.__name__):
        operation_prefix = prefix + "pathPaymentStrictSendOp."
        return _get_path_payment_strict_send_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(Payment.__name__):
        operation_prefix = prefix + "paymentOp."
        return _get_payment_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(RevokeSponsorship.__name__):
        operation_prefix = prefix + "revokeSponsorshipOp."
        return _get_revoke_sponsorship_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(SetOptions.__name__):
        operation_prefix = prefix + "setOptionsOp."
        return _get_set_options_op(source_account_id, operation_prefix, raw_data_map)
    elif operation_type == _to_caps_with_under(SetTrustLineFlags.__name__):
        operation_prefix = prefix + "setTrustLineFlagsOp."
        return _get_set_trust_line_flags_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(LiquidityPoolDeposit.__name__):
        operation_prefix = prefix + "liquidityPoolDepositOp."
        return _get_liquidity_pool_deposit_op(
            source_account_id, operation_prefix, raw_data_map
        )
    elif operation_type == _to_caps_with_under(LiquidityPoolWithdraw.__name__):
        operation_prefix = prefix + "liquidityPoolWithdrawOp."
        return _get_liquidity_pool_withdraw_op(
            source_account_id, operation_prefix, raw_data_map
        )
    else:
        raise ValueError(
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
            raise ValueError("Signer key should start with `G`, `X` or `T`.")

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
    # Keep compatibility
    line_type = raw_data_map.get(f"{operation_prefix}line.type", None)
    if line_type == stellar_xdr.AssetType.ASSET_TYPE_POOL_SHARE.name:
        asset_a = _get_asset(
            raw_data_map, f"{operation_prefix}line.liquidityPool.constantProduct.assetA"
        )
        asset_b = _get_asset(
            raw_data_map, f"{operation_prefix}line.liquidityPool.constantProduct.assetB"
        )
        fee = _get_int_value(
            raw_data_map, f"{operation_prefix}line.liquidityPool.constantProduct.fee"
        )
        line: Union[Asset, LiquidityPoolAsset] = LiquidityPoolAsset(
            asset_a, asset_b, fee
        )
    else:
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


def _get_begin_sponsoring_future_reserves_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> BeginSponsoringFutureReserves:
    sponsored_id = _get_value(raw_data_map, f"{operation_prefix}sponsoredID")
    return BeginSponsoringFutureReserves(sponsored_id=sponsored_id, source=source)


def _get_claim_claimable_balance_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ClaimClaimableBalance:
    balance_id = _get_value(raw_data_map, f"{operation_prefix}balanceID")
    return ClaimClaimableBalance(balance_id=balance_id, source=source)


def _get_clawback_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> Clawback:
    asset = _get_asset(raw_data_map, f"{operation_prefix}asset")
    from_ = _get_value(raw_data_map, f"{operation_prefix}from")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    return Clawback(asset=asset, from_=from_, amount=amount, source=source)


def _get_clawback_claimable_balance_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> ClawbackClaimableBalance:
    balance_id = _get_value(raw_data_map, f"{operation_prefix}balanceID")
    return ClawbackClaimableBalance(balance_id=balance_id, source=source)


def _get_create_claimable_balance_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
):
    def parse_claimant_predicate(
        prefix: str, raw_data_map: Dict[str, str]
    ) -> ClaimPredicate:
        claimant_predicate_type = _get_value(raw_data_map, f"{prefix}.type")
        if claimant_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_AND.name:
            left = parse_claimant_predicate(f"{prefix}.andPredicates[0]", raw_data_map)
            right = parse_claimant_predicate(f"{prefix}.andPredicates[1]", raw_data_map)
            return ClaimPredicate.predicate_and(left, right)
        elif claimant_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_OR.name:
            left = parse_claimant_predicate(f"{prefix}.orPredicates[0]", raw_data_map)
            right = parse_claimant_predicate(f"{prefix}.orPredicates[1]", raw_data_map)
            return ClaimPredicate.predicate_or(left, right)
        elif claimant_predicate_type == ClaimPredicateType.CLAIM_PREDICATE_NOT.name:
            predicate = parse_claimant_predicate(f"{prefix}.notPredicate", raw_data_map)
            return ClaimPredicate.predicate_not(predicate)
        elif (
            claimant_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME.name
        ):
            before_absolute_time = _get_int_value(raw_data_map, f"{prefix}.absBefore")
            return ClaimPredicate.predicate_before_absolute_time(before_absolute_time)
        elif (
            claimant_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME.name
        ):
            before_relative_time = _get_int_value(raw_data_map, f"{prefix}.relBefore")
            return ClaimPredicate.predicate_before_relative_time(before_relative_time)
        else:
            raise ValueError(
                f"This claim predicate type has not been implemented yet, "
                f"claim predicate type: {claimant_predicate_type}."
            )

    asset = _get_asset(raw_data_map, f"{operation_prefix}asset")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    claimants: List[Claimant] = []
    claimants_len = _get_int_value(raw_data_map, f"{operation_prefix}claimants.len")

    for index in range(claimants_len):
        destination = _get_value(
            raw_data_map, f"{operation_prefix}claimants[{index}].v0.destination"
        )
        claimant_predicate = parse_claimant_predicate(
            f"{operation_prefix}claimants[{index}].v0.predicate", raw_data_map
        )
        claimant = Claimant(destination=destination, predicate=claimant_predicate)
        claimants.append(claimant)
    return CreateClaimableBalance(
        asset=asset, amount=amount, claimants=claimants, source=source
    )


def _get_end_sponsoring_future_reserves_op(source: str) -> EndSponsoringFutureReserves:
    return EndSponsoringFutureReserves(source=source)


def _get_revoke_sponsorship_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> RevokeSponsorship:
    revoke_sponsorship_type = _get_value(raw_data_map, f"{operation_prefix}type")
    if (
        revoke_sponsorship_type
        == stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name
    ):
        ledger_entry_type = _get_value(
            raw_data_map, f"{operation_prefix}ledgerKey.type"
        )
        if ledger_entry_type == stellar_xdr.LedgerEntryType.ACCOUNT.name:
            account = _get_value(raw_data_map, f"{operation_prefix}ledgerKey.account")
            return RevokeSponsorship.revoke_account_sponsorship(
                account_id=account, source=source
            )
        elif ledger_entry_type == stellar_xdr.LedgerEntryType.TRUSTLINE.name:
            account = _get_value(
                raw_data_map, f"{operation_prefix}ledgerKey.trustLine.accountID"
            )
            asset = _get_asset(
                raw_data_map, f"{operation_prefix}ledgerKey.trustLine.asset"
            )
            return RevokeSponsorship.revoke_trustline_sponsorship(
                account_id=account, asset=asset, source=source
            )
        elif ledger_entry_type == stellar_xdr.LedgerEntryType.OFFER.name:
            sell_id = _get_value(
                raw_data_map, f"{operation_prefix}ledgerKey.offer.sellerID"
            )
            offer_id = _get_int_value(
                raw_data_map, f"{operation_prefix}ledgerKey.offer.offerID"
            )
            return RevokeSponsorship.revoke_offer_sponsorship(
                seller_id=sell_id, offer_id=offer_id, source=source
            )
        elif ledger_entry_type == stellar_xdr.LedgerEntryType.DATA.name:
            account_id = _get_value(
                raw_data_map, f"{operation_prefix}ledgerKey.data.accountID"
            )
            data_name = _get_value(
                raw_data_map, f"{operation_prefix}ledgerKey.data.dataName"
            )
            return RevokeSponsorship.revoke_data_sponsorship(
                account_id=account_id, data_name=data_name, source=source
            )
        elif ledger_entry_type == stellar_xdr.LedgerEntryType.CLAIMABLE_BALANCE.name:
            claimable_balance_id = _get_value(
                raw_data_map, f"{operation_prefix}ledgerKey.claimableBalance.balanceID"
            )
            return RevokeSponsorship.revoke_claimable_balance_sponsorship(
                claimable_balance_id=claimable_balance_id, source=source
            )
        elif ledger_entry_type == stellar_xdr.LedgerEntryType.LIQUIDITY_POOL.name:
            liquidity_pool_id = _get_value(
                raw_data_map,
                f"{operation_prefix}ledgerKey.liquidityPool.liquidityPoolID",
            )
            return RevokeSponsorship.revoke_liquidity_pool_sponsorship(
                liquidity_pool_id=liquidity_pool_id, source=source
            )
        else:
            raise ValueError(
                f"This ledger entry type has not been implemented yet, "
                f"ledger entry type: {ledger_entry_type}."
            )
    elif (
        revoke_sponsorship_type
        == stellar_xdr.RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER.name
    ):
        signer_key_type = _get_value(
            raw_data_map, f"{operation_prefix}signer.signerKey.type"
        )
        account_id = _get_value(raw_data_map, f"{operation_prefix}signer.accountID")
        if (
            signer_key_type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX.name
        ):
            key = _get_value(
                raw_data_map, f"{operation_prefix}signer.signerKey.preAuthTx"
            )
            signer_key = SignerKey.pre_auth_tx(StrKey.decode_pre_auth_tx(key))
        elif signer_key_type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519.name:
            key = _get_value(
                raw_data_map, f"{operation_prefix}signer.signerKey.ed25519"
            )
            signer_key = SignerKey.ed25519_public_key(key)
        elif signer_key_type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X.name:
            key = _get_value(raw_data_map, f"{operation_prefix}signer.signerKey.hashX")
            signer_key = SignerKey.sha256_hash(StrKey.decode_sha256_hash(key))
        else:
            raise ValueError(
                f"This signer key type has not been implemented yet, "
                f"signer key type: {signer_key_type}."
            )
        return RevokeSponsorship.revoke_signer_sponsorship(
            account_id=account_id, signer_key=signer_key, source=source
        )
    else:
        raise ValueError(
            f"This revoke sponsorship type has not been implemented yet, "
            f"revoke sponsorship type: {revoke_sponsorship_type}."
        )


def _get_set_trust_line_flags_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
) -> SetTrustLineFlags:
    trustor = _get_value(raw_data_map, f"{operation_prefix}trustor")
    asset = _get_asset(raw_data_map, f"{operation_prefix}asset")
    clear_flags_raw = _get_int_value(raw_data_map, f"{operation_prefix}clearFlags")
    set_flags_raw = _get_int_value(raw_data_map, f"{operation_prefix}setFlags")
    if clear_flags_raw == 0:
        clear_flags = None
    else:
        clear_flags = TrustLineFlags(clear_flags_raw)
    if set_flags_raw == 0:
        set_flags = None
    else:
        set_flags = TrustLineFlags(set_flags_raw)
    return SetTrustLineFlags(
        trustor=trustor,
        asset=asset,
        clear_flags=clear_flags,
        set_flags=set_flags,
        source=source,
    )


def _get_liquidity_pool_deposit_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
):
    liquidity_pool_id = _get_value(raw_data_map, f"{operation_prefix}liquidityPoolID")
    max_amount_a = _get_amount_value(raw_data_map, f"{operation_prefix}maxAmountA")
    max_amount_b = _get_amount_value(raw_data_map, f"{operation_prefix}maxAmountB")
    min_price_n = _get_int_value(raw_data_map, f"{operation_prefix}minPrice.n")
    min_price_d = _get_int_value(raw_data_map, f"{operation_prefix}minPrice.d")
    min_price = Price(min_price_n, min_price_d)
    max_price_n = _get_int_value(raw_data_map, f"{operation_prefix}maxPrice.n")
    max_price_d = _get_int_value(raw_data_map, f"{operation_prefix}maxPrice.d")
    max_price = Price(max_price_n, max_price_d)
    return LiquidityPoolDeposit(
        liquidity_pool_id=liquidity_pool_id,
        max_amount_a=max_amount_a,
        max_amount_b=max_amount_b,
        min_price=min_price,
        max_price=max_price,
        source=source,
    )


def _get_liquidity_pool_withdraw_op(
    source: str, operation_prefix: str, raw_data_map: Dict[str, str]
):
    liquidity_pool_id = _get_value(raw_data_map, f"{operation_prefix}liquidityPoolID")
    amount = _get_amount_value(raw_data_map, f"{operation_prefix}amount")
    min_amount_a = _get_amount_value(raw_data_map, f"{operation_prefix}minAmountA")
    min_amount_b = _get_amount_value(raw_data_map, f"{operation_prefix}minAmountB")
    return LiquidityPoolWithdraw(
        liquidity_pool_id=liquidity_pool_id,
        amount=amount,
        min_amount_a=min_amount_a,
        min_amount_b=min_amount_b,
        source=source,
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
        raise ValueError(f"Failed to convert `{value}` to int type.") from e


def _get_bool_value(raw_data_map: Dict[str, str], key: str) -> bool:
    value = _get_value(raw_data_map, key)
    if value == _true:
        return True
    elif value == _false:
        return False
    else:
        raise ValueError(f"Failed to convert `{value}` to bool type.")


def _get_bytes_value(raw_data_map: Dict[str, str], key: str) -> bytes:
    value = _get_value(raw_data_map, key)
    if value[0] == '"':
        # for text memo.
        return _get_string_value(raw_data_map, key).encode()
    try:
        return bytes.fromhex(value)
    except ValueError as e:
        raise ValueError(f"Failed to convert `{value}` to bytes type.") from e


def _get_string_value(raw_data_map: Dict[str, str], key: str) -> str:
    value = _get_value(raw_data_map, key)
    if len(value) == 0:
        return value
    return value[1:-1]


def _get_value(raw_data_map: Dict[str, str], key: str) -> str:
    try:
        return raw_data_map[key]
    except KeyError as e:
        raise ValueError(f"`{key}` is missing from txrep.") from e


def _decode_asset(asset: str) -> Asset:
    # native (or any string up to 12 characters not containing an unescaped colon) for the native asset
    if ":" not in asset and len(asset) <= 12:
        return Asset.native()
    parts = asset.split(":")
    if len(parts) != 2:
        raise ValueError("Failed to decode asset string.")
    return Asset(parts[0], parts[1])


def _add_line(
    key: str,
    value: Union[str, int],
    lines: List[str],
    comment: Union[str, int, Decimal] = None,
) -> None:
    lines.append(f"{key}: {value}{' (' + str(comment) + ')' if comment else ''}")


def _add_preconditions(
    cond: Optional[Preconditions], prefix: str, lines: List[str]
) -> None:
    if cond is None:
        cond_xdr = stellar_xdr.Preconditions(stellar_xdr.PreconditionType.PRECOND_NONE)
    else:
        cond_xdr = cond.to_xdr_object()
    _add_line(f"{prefix}type", cond_xdr.type.name, lines)
    if cond_xdr.type == stellar_xdr.PreconditionType.PRECOND_TIME:
        assert cond is not None
        assert cond.time_bounds is not None
        _add_time_bounds(cond.time_bounds, prefix, lines)
    elif cond_xdr.type == stellar_xdr.PreconditionType.PRECOND_V2:
        assert cond is not None
        _add_time_bounds_optional(cond.time_bounds, prefix, lines)
        _add_ledger_bounds_optional(cond.ledger_bounds, prefix, lines)
        if cond.min_sequence_number is None:
            _add_line(f"{prefix}minSeqNum._present", _false, lines)
        else:
            _add_line(f"{prefix}minSeqNum._present", _true, lines)
            _add_line(f"{prefix}minSeqNum", cond.min_sequence_number, lines)
        _add_line(f"{prefix}minSeqAge", cond.min_sequence_age or 0, lines)
        _add_line(f"{prefix}minSeqLedgerGap", cond.min_sequence_ledger_gap or 0, lines)
        _add_extra_signers(f"{prefix}extraSigners", cond.extra_signers, lines)
    elif cond_xdr.type == stellar_xdr.PreconditionType.PRECOND_NONE:
        pass
    else:
        raise ValueError(
            f"This preconditions type has not been implemented yet, "
            f"preconditions type: {cond_xdr.type}."
        )


def _add_signer_key(prefix: str, signer_key: SignerKey, lines: List[str]) -> None:
    _add_line(f"{prefix}.type", signer_key.signer_key_type.name, lines)
    key = signer_key.encoded_signer_key
    if signer_key.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_ED25519:
        _add_line(f"{prefix}.ed25519", key, lines)
    elif signer_key.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
        _add_line(f"{prefix}.hashX", key, lines)
    elif signer_key.signer_key_type == SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX:
        _add_line(f"{prefix}.preAuthTx", key, lines)
    elif (
        signer_key.signer_key_type
        == SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
    ):
        _add_line(f"{prefix}.ed25519SignedPayload", key, lines)
    else:
        raise ValueError(
            f"This signer key type has not been implemented yet, "
            f"signer key type: {signer_key.signer_key_type}."
        )


def _add_extra_signers(
    prefix: str, extra_signers: Optional[Sequence[SignerKey]], lines: List[str]
) -> None:
    if extra_signers is None:
        extra_signers = []
    _add_line(f"{prefix}.len", len(extra_signers), lines)
    for index, extra_signer in enumerate(extra_signers):
        _add_signer_key(f"{prefix}[{index}]", extra_signer, lines)


def _add_time_bounds_optional(
    time_bounds: Optional[TimeBounds], prefix: str, lines: List[str]
) -> None:
    if time_bounds is None:
        _add_line(f"{prefix}timeBounds._present", _false, lines)
    else:
        _add_line(f"{prefix}timeBounds._present", _true, lines)
        _add_time_bounds(time_bounds, prefix, lines)


def _add_time_bounds(time_bounds: TimeBounds, prefix: str, lines: List[str]) -> None:
    _add_line(
        f"{prefix}timeBounds.minTime",
        time_bounds.min_time,
        lines,
        _to_readable_utc_time_comment(time_bounds.min_time),
    )
    _add_line(
        f"{prefix}timeBounds.maxTime",
        time_bounds.max_time,
        lines,
        _to_readable_utc_time_comment(time_bounds.max_time),
    )


def _add_ledger_bounds_optional(
    ledger_bounds: Optional[LedgerBounds], prefix: str, lines: List[str]
) -> None:
    if ledger_bounds is None:
        _add_line(f"{prefix}ledgerBounds._present", _false, lines)
    else:
        _add_line(f"{prefix}ledgerBounds._present", _true, lines)
        _add_ledger_bounds(ledger_bounds, prefix, lines)


def _add_ledger_bounds(
    ledger_bounds: LedgerBounds, prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}ledgerBounds.minLedger", ledger_bounds.min_ledger, lines, None)
    _add_line(f"{prefix}ledgerBounds.maxLedger", ledger_bounds.max_ledger, lines, None)


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
    operations: Sequence[Operation], prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}operations.len", len(operations), lines)
    for index, operation in enumerate(operations):
        _add_operation(index, operation, prefix, lines)


def _add_operation(
    index: int, operation: Operation, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}operations[{index}]."
    operation_type = operation.__class__.__name__

    def add_operation_line(
        key: str, value: Union[str, int], comment: Union[str, int, Decimal] = None
    ) -> None:
        _add_line(f"{prefix}{key}", value, lines, comment)

    if operation.source is not None:
        add_operation_line("sourceAccount._present", _true)
        add_operation_line(
            "sourceAccount",
            _to_muxed_account(operation.source),
            comment=_to_muxed_account_comment(operation.source),
        )
    else:
        add_operation_line("sourceAccount._present", _false)

    add_operation_line("body.type", _to_caps_with_under(operation_type))

    def add_body_line(
        key: str,
        value: Union[str, int, None],
        optional: bool = False,
        comment: Union[str, int, Decimal] = None,
    ) -> None:
        operation_type = operation.__class__.__name__
        key = f"body.{_to_camel_case(operation_type)}Op.{key}"
        if optional:
            present = True if value is not None else False
            add_operation_line(f"{key}._present", _true if present else _false)
            if present:
                assert value is not None
                add_operation_line(key, value, comment=comment)
        else:
            assert value is not None
            add_operation_line(key, value, comment=comment)

    def add_signer(signer: Optional[Signer]) -> None:
        add_body_line("signer._present", _false if signer is None else _true)
        if signer is None:
            return
        add_body_line("signer.key", signer.signer_key.encoded_signer_key)
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

    def add_claim_predicate(prefix: str, claimant_predicate: ClaimPredicate):
        add_body_line(f"{prefix}.type", claimant_predicate.claim_predicate_type.name)
        if (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_UNCONDITIONAL
        ):
            pass
        elif (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_NOT
        ):
            assert claimant_predicate.not_predicate is not None
            add_claim_predicate(
                f"{prefix}.notPredicate", claimant_predicate.not_predicate
            )
        elif (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_AND
        ):
            add_body_line(f"{prefix}.andPredicates.len", 2)
            assert claimant_predicate.and_predicates is not None
            add_claim_predicate(
                f"{prefix}.andPredicates[0]", claimant_predicate.and_predicates.left
            )
            add_claim_predicate(
                f"{prefix}.andPredicates[1]", claimant_predicate.and_predicates.right
            )
        elif (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_OR
        ):
            add_body_line(f"{prefix}.orPredicates.len", 2)
            assert claimant_predicate.or_predicates is not None
            add_claim_predicate(
                f"{prefix}.orPredicates[0]", claimant_predicate.or_predicates.left
            )
            add_claim_predicate(
                f"{prefix}.orPredicates[1]", claimant_predicate.or_predicates.right
            )
        elif (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_ABSOLUTE_TIME
        ):
            assert claimant_predicate.abs_before is not None
            add_body_line(
                f"{prefix}.absBefore",
                claimant_predicate.abs_before,
                comment=_to_readable_utc_time_comment(claimant_predicate.abs_before),
            )
        elif (
            claimant_predicate.claim_predicate_type
            == ClaimPredicateType.CLAIM_PREDICATE_BEFORE_RELATIVE_TIME
        ):
            assert claimant_predicate.rel_before is not None
            add_body_line(
                f"{prefix}.relBefore",
                claimant_predicate.rel_before,
                comment=_to_readable_utc_time_comment(claimant_predicate.rel_before),
            )
        else:
            raise ValueError(
                f"This claim predicate type has not been implemented yet, "
                f"claim predicate type: {claimant_predicate.claim_predicate_type}."
            )

    if isinstance(operation, CreateAccount):
        add_body_line("destination", operation.destination)
        add_body_line(
            "startingBalance",
            _to_amount(operation.starting_balance),
            comment=operation.starting_balance,
        )
    elif isinstance(operation, Payment):
        add_body_line(
            "destination",
            _to_muxed_account(operation.destination),
            comment=_to_muxed_account_comment(operation.destination),
        )
        add_body_line("asset", _to_asset(operation.asset))
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
    elif isinstance(operation, PathPaymentStrictReceive):
        add_body_line("sendAsset", _to_asset(operation.send_asset))
        add_body_line(
            "sendMax", _to_amount(operation.send_max), comment=operation.send_max
        )
        add_body_line(
            "destination",
            _to_muxed_account(operation.destination),
            comment=_to_muxed_account_comment(operation.destination),
        )
        add_body_line("destAsset", _to_asset(operation.dest_asset))
        add_body_line(
            "destAmount",
            _to_amount(operation.dest_amount),
            comment=operation.dest_amount,
        )
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line(f"path[{index}]", _to_asset(asset))
    elif isinstance(operation, ManageSellOffer):
        add_body_line("selling", _to_asset(operation.selling))
        add_body_line("buying", _to_asset(operation.buying))
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, CreatePassiveSellOffer):
        add_body_line("selling", _to_asset(operation.selling))
        add_body_line("buying", _to_asset(operation.buying))
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
        add_price(operation.price)
    elif isinstance(operation, SetOptions):
        add_body_line("inflationDest", operation.inflation_dest, True)
        add_body_line(
            "clearFlags",
            operation.clear_flags.value if operation.clear_flags else None,
            True,
        )
        add_body_line(
            "setFlags", operation.set_flags.value if operation.set_flags else None, True
        )
        add_body_line("masterWeight", operation.master_weight, True)
        add_body_line("lowThreshold", operation.low_threshold, True)
        add_body_line("medThreshold", operation.med_threshold, True)
        add_body_line("highThreshold", operation.high_threshold, True)
        add_home_domain(operation.home_domain)
        add_signer(operation.signer)
    elif isinstance(operation, ChangeTrust):
        asset_xdr = operation.asset.to_change_trust_asset_xdr_object()
        add_body_line("line.type", asset_xdr.type.name)
        if asset_xdr.type == stellar_xdr.AssetType.ASSET_TYPE_POOL_SHARE:
            assert isinstance(operation.asset, LiquidityPoolAsset)
            add_body_line(
                "line.liquidityPool.constantProduct.assetA",
                _to_asset(operation.asset.asset_a),
            )
            add_body_line(
                "line.liquidityPool.constantProduct.assetB",
                _to_asset(operation.asset.asset_b),
            )
            add_body_line("line.liquidityPool.constantProduct.fee", operation.asset.fee)
        else:
            assert isinstance(operation.asset, Asset)
            add_body_line("line", _to_asset(operation.asset))
        add_body_line("limit", _to_amount(operation.limit), comment=operation.limit)
    elif isinstance(operation, AllowTrust):
        add_body_line("trustor", operation.trustor)
        add_body_line("asset", operation.asset_code)
        add_body_line("authorize", _true if operation.authorize else _false)
    elif isinstance(operation, AccountMerge):
        # AccountMerge does not include 'accountMergeOp' prefix
        # see https://github.com/StellarCN/py-stellar-base/blob/master/.xdr/Stellar-transaction.x#L282
        add_operation_line(
            "body.destination",
            _to_muxed_account(operation.destination),
            comment=_to_muxed_account_comment(operation.destination),
        )
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
        add_body_line(
            "buyAmount", _to_amount(operation.amount), comment=operation.amount
        )
        add_price(operation.price)
        add_body_line("offerID", operation.offer_id)
    elif isinstance(operation, PathPaymentStrictSend):
        add_body_line("sendAsset", _to_asset(operation.send_asset))
        add_body_line(
            "sendAmount",
            _to_amount(operation.send_amount),
            comment=operation.send_amount,
        )
        add_body_line(
            "destination",
            _to_muxed_account(operation.destination),
            comment=_to_muxed_account_comment(operation.destination),
        )
        add_body_line("destAsset", _to_asset(operation.dest_asset))
        add_body_line(
            "destMin", _to_amount(operation.dest_min), comment=operation.dest_min
        )
        add_body_line("path.len", len(operation.path))
        for index, asset in enumerate(operation.path):
            add_body_line(f"path[{index}]", _to_asset(asset))
    elif isinstance(operation, Inflation):
        # no body
        pass
    elif isinstance(operation, CreateClaimableBalance):
        add_body_line("asset", _to_asset(operation.asset))
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
        add_body_line("claimants.len", len(operation.claimants))
        for index, claimant in enumerate(operation.claimants):
            # current CLAIMANT_TYPE is CLAIMANT_TYPE_V0
            add_body_line(
                f"claimants[{index}].type",
                stellar_xdr.ClaimantType.CLAIMANT_TYPE_V0.name,
            )
            add_body_line(f"claimants[{index}].v0.destination", claimant.destination)
            add_claim_predicate(f"claimants[{index}].v0.predicate", claimant.predicate)
    elif isinstance(operation, ClaimClaimableBalance):
        add_body_line("balanceID", operation.balance_id)
    elif isinstance(operation, BeginSponsoringFutureReserves):
        add_body_line("sponsoredID", operation.sponsored_id)
    elif isinstance(operation, EndSponsoringFutureReserves):
        # no body
        pass
    elif isinstance(operation, RevokeSponsorship):
        if operation.revoke_sponsorship_type == RevokeSponsorshipType.ACCOUNT:
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line("ledgerKey.type", stellar_xdr.LedgerEntryType.ACCOUNT.name)
            add_body_line("ledgerKey.account", operation.account_id)
        elif operation.revoke_sponsorship_type == RevokeSponsorshipType.TRUSTLINE:
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line("ledgerKey.type", stellar_xdr.LedgerEntryType.TRUSTLINE.name)
            assert operation.trustline is not None
            add_body_line(
                "ledgerKey.trustLine.accountID", operation.trustline.account_id
            )
            add_body_line(
                "ledgerKey.trustLine.asset", _to_asset(operation.trustline.asset)
            )
        elif operation.revoke_sponsorship_type == RevokeSponsorshipType.OFFER:
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line("ledgerKey.type", stellar_xdr.LedgerEntryType.OFFER.name)
            assert operation.offer is not None
            add_body_line("ledgerKey.offer.sellerID", operation.offer.seller_id)
            add_body_line("ledgerKey.offer.offerID", operation.offer.offer_id)
        elif operation.revoke_sponsorship_type == RevokeSponsorshipType.DATA:
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line("ledgerKey.type", stellar_xdr.LedgerEntryType.DATA.name)
            assert operation.data is not None
            add_body_line("ledgerKey.data.accountID", operation.data.account_id)
            add_body_line("ledgerKey.data.dataName", operation.data.data_name)
        elif (
            operation.revoke_sponsorship_type == RevokeSponsorshipType.CLAIMABLE_BALANCE
        ):
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line(
                "ledgerKey.type", stellar_xdr.LedgerEntryType.CLAIMABLE_BALANCE.name
            )
            add_body_line(
                "ledgerKey.claimableBalance.balanceID", operation.claimable_balance_id
            )
        elif operation.revoke_sponsorship_type == RevokeSponsorshipType.LIQUIDITY_POOL:
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_LEDGER_ENTRY.name,
            )
            add_body_line(
                "ledgerKey.type", stellar_xdr.LedgerEntryType.LIQUIDITY_POOL.name
            )
            add_body_line(
                "ledgerKey.liquidityPool.liquidityPoolID", operation.liquidity_pool_id
            )
        elif operation.revoke_sponsorship_type == RevokeSponsorshipType.SIGNER:
            assert operation.signer is not None
            add_body_line(
                "type",
                stellar_xdr.revoke_sponsorship_type.RevokeSponsorshipType.REVOKE_SPONSORSHIP_SIGNER.name,
            )
            add_body_line("signer.accountID", operation.signer.account_id)
            signer_key_xdr = operation.signer.signer_key.to_xdr_object()
            add_body_line(
                "signer.signerKey.type",
                signer_key_xdr.type.name,
            )
            key = operation.signer.signer_key.encoded_signer_key
            if signer_key_xdr.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X:
                add_body_line("signer.signerKey.hashX", key)
            elif (
                signer_key_xdr.type == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519
            ):
                add_body_line("signer.signerKey.ed25519", key)
            elif (
                signer_key_xdr.type
                == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
            ):
                add_body_line("signer.signerKey.preAuthTx", key)
            else:
                raise ValueError(
                    f"This signer key type has not been implemented yet, "
                    f"signer key type: {signer_key_xdr.type}."
                )
        else:
            raise ValueError(
                f"This revoke sponsorship type has not been implemented yet, "
                f"revoke sponsorship type: {operation.revoke_sponsorship_type}."
            )
    elif isinstance(operation, Clawback):
        add_body_line("asset", _to_asset(operation.asset))
        add_body_line(
            "from",
            _to_muxed_account(operation.from_),
            comment=_to_muxed_account_comment(operation.from_),
        )
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
    elif isinstance(operation, ClawbackClaimableBalance):
        add_body_line("balanceID", operation.balance_id)
    elif isinstance(operation, SetTrustLineFlags):
        add_body_line("trustor", operation.trustor)
        add_body_line("asset", _to_asset(operation.asset))
        if operation.clear_flags is None:
            add_body_line("clearFlags", 0)
        else:
            add_body_line("clearFlags", operation.clear_flags.value)
        if operation.set_flags is None:
            add_body_line("setFlags", 0)
        else:
            add_body_line("setFlags", operation.set_flags.value)
    elif isinstance(operation, LiquidityPoolDeposit):
        add_body_line("liquidityPoolID", operation.liquidity_pool_id)
        add_body_line(
            "maxAmountA",
            _to_amount(operation.max_amount_a),
            comment=operation.max_amount_a,
        )
        add_body_line(
            "maxAmountB",
            _to_amount(operation.max_amount_b),
            comment=operation.max_amount_b,
        )
        add_body_line("minPrice.n", operation.min_price.n)
        add_body_line("minPrice.d", operation.min_price.d)
        add_body_line("maxPrice.n", operation.max_price.n)
        add_body_line("maxPrice.d", operation.max_price.d)
    elif isinstance(operation, LiquidityPoolWithdraw):
        add_body_line("liquidityPoolID", operation.liquidity_pool_id)
        add_body_line("amount", _to_amount(operation.amount), comment=operation.amount)
        add_body_line(
            "minAmountA",
            _to_amount(operation.min_amount_a),
            comment=operation.min_amount_a,
        )
        add_body_line(
            "minAmountB",
            _to_amount(operation.min_amount_b),
            comment=operation.min_amount_b,
        )
    else:
        raise ValueError(
            f"This operation has not been implemented yet, "
            f"operation type: {operation}."
        )


def _add_signatures(
    signatures: Sequence[DecoratedSignature], prefix: str, lines: List[str]
) -> None:
    _add_line(f"{prefix}signatures.len", len(signatures), lines)
    for index, signature in enumerate(signatures):
        _add_signature(index, signature, prefix, lines)


def _add_signature(
    index: int, signature: DecoratedSignature, prefix: str, lines: List[str]
) -> None:
    prefix = f"{prefix}signatures[{index}]."
    _add_line(f"{prefix}hint", _to_opaque(signature.signature_hint), lines)
    _add_line(f"{prefix}signature", _to_opaque(signature.signature), lines)


def _to_asset(asset: Union[Asset, LiquidityPoolAsset, LiquidityPoolId]) -> str:
    if not isinstance(asset, Asset):
        raise ValueError("Unexpected asset type.")
    if asset.is_native():
        return "native"
    return f"{asset.code}:{asset.issuer}"


def _to_readable_utc_time_comment(timestamp: int) -> str:
    utc_time = datetime.utcfromtimestamp(timestamp)
    return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")


def _to_muxed_account_comment(account: MuxedAccount) -> Optional[str]:
    if account.account_muxed_id is None:
        return None
    return (
        f"accountID: {account.account_id}, accountMuxedID: {account.account_muxed_id}"
    )


def _to_amount(amount: Union[Decimal, str]) -> int:
    return Operation.to_xdr_amount(amount)


def _to_price(price: Union[Price, str, Decimal]) -> Price:
    if isinstance(price, Price):
        price_fraction = price
    else:
        price_fraction = Price.from_raw_price(price)
    return price_fraction


def _to_camel_case(cap_words: str) -> str:
    return cap_words[0].lower() + cap_words[1:]


def _to_caps_with_under(word):
    return "".join(["_" + c if c.isupper() else c for c in word]).lstrip("_").upper()


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


def _to_opaque(value: bytes) -> str:
    return value.hex()
