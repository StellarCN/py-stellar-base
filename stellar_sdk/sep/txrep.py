"""
SEP: 0011
Title: Txrep: human-readable low-level representation of Stellar transactions
Author: David Mazières
Status: Active
Created: 2018-08-31
Updated: 2021-10-09
Version: 1.1.0
"""

import re
from typing import Any, Final

from .. import xdr as stellar_xdr
from ..fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from ..network import Network
from ..transaction_envelope import TransactionEnvelope
from ._txrep_lines import (
    ALPHANUM4,
    NATIVE,
    POOL_SHARE,
    ZERO_ACCOUNT,
    TxrepReader,
    TxrepWriter,
    asset_kind,
    index,
    join,
    read_account,
    read_code,
    read_pool_share,
    split_asset,
    write_account,
    write_code,
    write_pool_share,
)
from ._txrep_schema import SCHEMA
from .exceptions import InvalidTxrepError

__all__ = ["from_txrep", "to_txrep"]

# Txrep names a value by the XDR names of the fields and union arms that lead to it,
# which only the XDR definitions have, so `_txrep_schema.py` keeps those of a
# transaction envelope. Most types are written field by field; the rules below are
# where SEP-11 says otherwise.

# SEP-11 writes the native asset as XLM on the public network, TestXLM on the test
# network, and native elsewhere.
_NATIVE_ASSETS: Final = {
    Network.PUBLIC_NETWORK_PASSPHRASE: "XLM",
    Network.TESTNET_NETWORK_PASSPHRASE: "TestXLM",
}
# Written as a strkey, as SEP-51 writes them too.
_STRKEYS: Final = frozenset({"PublicKey", "MuxedAccount", "SignerKey"})
# Written as `native` or `CODE:ISSUER`, and whether each has the arm of a liquidity
# pool's shares, written as `ID:lp`.
_ASSETS: Final = {"Asset": False, "TrustLineAsset": True}
# Written as `CODE:ISSUER` wherever else they appear. The trailing NULs of a code are
# left out down to this many bytes, so that a short AlphaNum12 code reads as one.
_ALPHANUMS: Final = {"AlphaNum4": 0, "AlphaNum12": 5}
# The asset of AllowTrustOp, written as its code alone.
_ASSET_CODE: Final = "AssetCode"
# Seconds since the epoch, written with the date as a comment.
_TIME_POINT: Final = "TimePoint"
# The source account of a TransactionV0 is 32 bytes, written as an account under the
# name it had before protocol 13.
_ACCOUNTS: Final = {("TransactionV0", "sourceAccountEd25519"): "sourceAccount"}
# Stroops, written with the amount as a comment.
_AMOUNTS: Final = frozenset(
    {
        ("CreateAccountOp", "startingBalance"),
        ("PaymentOp", "amount"),
        ("PathPaymentStrictReceiveOp", "sendMax"),
        ("PathPaymentStrictReceiveOp", "destAmount"),
        ("PathPaymentStrictSendOp", "sendAmount"),
        ("PathPaymentStrictSendOp", "destMin"),
        ("ManageSellOfferOp", "amount"),
        ("ManageBuyOfferOp", "buyAmount"),
        ("CreatePassiveSellOfferOp", "amount"),
        ("ChangeTrustOp", "limit"),
        ("CreateClaimableBalanceOp", "amount"),
        ("ClawbackOp", "amount"),
        ("LiquidityPoolDepositOp", "maxAmountA"),
        ("LiquidityPoolDepositOp", "maxAmountB"),
        ("LiquidityPoolWithdrawOp", "amount"),
        ("LiquidityPoolWithdrawOp", "minAmountA"),
        ("LiquidityPoolWithdrawOp", "minAmountB"),
    }
)
# The union arms holding these have their fields written as the union's own:
# `tx.fee`, not `v1.tx.fee`.
_INLINED: Final = re.compile(r"TransactionV[0-9]+Envelope")
_ENVELOPE: Final = ("ref", "TransactionEnvelope")


def to_txrep(
    transaction_envelope: TransactionEnvelope | FeeBumpTransactionEnvelope,
) -> str:
    """Write a transaction as txrep, a form people can read before they sign.

    Txrep is one `field: value` line per field of the transaction envelope's XDR,
    such as `tx.operations[0].body.paymentOp.amount: 10000000 (1)`.

    See `SEP-0011 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0011.md>`_
    for the format.

    :param transaction_envelope: The transaction envelope.
    :return: The txrep, one line per field.
    """
    native = _NATIVE_ASSETS.get(transaction_envelope.network_passphrase, "native")
    writer = TxrepWriter(native)
    _write(writer, _ENVELOPE, transaction_envelope.to_xdr_object(), "")
    return writer.text()


def from_txrep(
    txrep: str, network_passphrase: str
) -> TransactionEnvelope | FeeBumpTransactionEnvelope:
    """Read a transaction from txrep.

    Fields may come in any order, and the last line of a field counts. A field left
    out is zero, false or empty, and an optional value left out is there if any of
    its fields is given, as SEP-11 says. Integers may be hex (`0x10`) or octal
    (`010`), and enums `Type#Number`. A line that the transaction doesn't use, such
    as a misspelled field or one of a union arm that isn't selected, is an error.

    :param txrep: The txrep, one `field: value` line per field.
    :param network_passphrase: The network of the transaction.
    :return: A :class:`TransactionEnvelope`, or a :class:`FeeBumpTransactionEnvelope`.
    :raises: :exc:`InvalidTxrepError <stellar_sdk.sep.exceptions.InvalidTxrepError>`:
        if the text is not valid txrep of a transaction envelope; the message names
        the line.
    :raises: :exc:`ValueError`: if the SDK rejects the transaction the text holds,
        as :meth:`TransactionEnvelope.from_xdr` does, such as time bounds that end
        before they start. :exc:`InvalidTxrepError` is a :exc:`ValueError` too.
    """
    reader = TxrepReader(txrep)
    # Reading a deep value, such as nested claim predicates, recurses, and so does
    # the SDK converting it.
    try:
        envelope = _read(reader, _ENVELOPE, "")
        reader.finish()
        if isinstance(envelope, stellar_xdr.TransactionEnvelope.TxFeeBump):
            return FeeBumpTransactionEnvelope.from_xdr_object(
                envelope, network_passphrase
            )
        return TransactionEnvelope.from_xdr_object(envelope, network_passphrase)
    except RecursionError:
        msg = "the txrep is nested too deeply"
        raise InvalidTxrepError(msg) from None


# --- Writing ------------------------------------------------------------------------


def _write(
    w: TxrepWriter, t: tuple[Any, ...], value: Any, path: str, *, amount: bool = False
) -> None:
    """Write a value of the type `t`; `amount` adds the comment of an amount."""
    match t:
        case ("ref", name):
            _write_definition(w, name, value, path, amount=amount)
        case ("bool",):
            w.boolean(path, value)
        case ("int",) | ("uint",) | ("hyper",) | ("uhyper",):
            if amount:
                w.amount(path, value)
            else:
                w.integer(path, value)
        case ("opaque", _):
            w.opaque(path, value)
        case ("var_opaque", _):
            w.var_opaque(path, value)
        case ("string", _):
            w.string(path, value)
        case ("optional", element):
            w.present(path, value)
            if value is not None:
                _write(w, element, value, path)
        case ("var_array", element, _):
            w.length(path, len(value))
            for i, item in enumerate(value):
                _write(w, element, item, index(path, i))
        case _:
            raise AssertionError(t)


def _write_definition(
    w: TxrepWriter, name: str, value: Any, path: str, *, amount: bool
) -> None:
    d = SCHEMA[name]
    if d[0] == "typedef":
        if name == _TIME_POINT:
            w.time_point(path, value)
        else:
            _write(w, d[1], value, path, amount=amount)
    elif d[0] == "enum":
        w.enum(path, value)
    elif name in _STRKEYS:
        w.line(path, value.to_json_value())
    elif name in _ASSETS:
        w.line(path, _asset_text(value, w.native))
    elif name in _ALPHANUMS:
        w.line(path, _alphanum_text(value, _ALPHANUMS[name]))
    elif name == _ASSET_CODE:
        w.line(path, _asset_code_text(value))
    elif d[0] == "struct":
        for field, attribute, t in d[2]:
            renamed = _ACCOUNTS.get((name, field))
            if renamed is not None:
                w.line(join(path, renamed), write_account(getattr(value, attribute)))
            else:
                at = join(path, field)
                is_amount = (name, field) in _AMOUNTS
                _write(w, t, getattr(value, attribute), at, amount=is_amount)
    else:
        _, _, switch, switch_attribute, switch_type, arms = d
        discriminant = getattr(value, switch_attribute)
        _write(w, switch_type, discriminant, join(path, switch))
        _, arm, attribute, t = arms[discriminant]
        if t is not None:
            at = path if _inlined(t) else join(path, arm)
            _write(w, t, getattr(value, attribute), at)


def _asset_text(asset: Any, native: str) -> str:
    """An Asset or a TrustLineAsset as `native`, `CODE:ISSUER` or `ID:lp`."""
    match asset.type:
        case stellar_xdr.AssetType.ASSET_TYPE_NATIVE:
            return native
        case stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            return _alphanum_text(asset.alpha_num4, _ALPHANUMS["AlphaNum4"])
        case stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            return _alphanum_text(asset.alpha_num12, _ALPHANUMS["AlphaNum12"])
        case _:
            return write_pool_share(asset.liquidity_pool_id)


def _alphanum_text(alphanum: Any, keep: int) -> str:
    """An AlphaNum4 or an AlphaNum12 as `CODE:ISSUER`."""
    code = write_code(alphanum.asset_code, keep)
    return f"{code}:{alphanum.issuer.to_json_value()}"


def _asset_code_text(asset_code: Any) -> str:
    if asset_code.type == stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
        return write_code(asset_code.asset_code4, _ALPHANUMS["AlphaNum4"])
    return write_code(asset_code.asset_code12, _ALPHANUMS["AlphaNum12"])


# --- Reading ------------------------------------------------------------------------


def _read(r: TxrepReader, t: tuple[Any, ...], path: str) -> Any:
    """Read a value of the type `t`."""
    match t:
        case ("ref", name):
            return _read_definition(r, name, path)
        case ("bool",):
            return r.boolean(path)
        case ("int",):
            return r.int32(path)
        case ("uint",):
            return r.uint32(path)
        case ("hyper",):
            return r.int64(path)
        case ("uhyper",):
            return r.uint64(path)
        case ("opaque", size):
            return r.opaque(path, size)
        case ("var_opaque", max_size):
            return r.var_opaque(path, max_size)
        case ("string", max_size):
            return r.string(path, max_size)
        case ("optional", element):
            return _read(r, element, path) if r.present(path) else None
        case ("var_array", element, max_count):
            count = r.length(path, max_count)
            return [_read(r, element, index(path, i)) for i in range(count)]
        case _:
            raise AssertionError(t)


def _read_definition(r: TxrepReader, name: str, path: str) -> Any:
    d = SCHEMA[name]
    if d[0] == "typedef":
        return _read(r, d[1], path)
    if d[0] == "enum":
        return r.enum(path, getattr(stellar_xdr, d[1]), name)
    if name in _STRKEYS:
        return r.parse(path, getattr(stellar_xdr, d[1]).from_json_value, ZERO_ACCOUNT)
    if name in _ASSETS:
        return r.parse(path, lambda text: _read_asset(name, text), "native")
    if name in _ALPHANUMS:
        default = f":{ZERO_ACCOUNT}"
        return r.parse(path, lambda text: _read_alphanum(name, text), default)
    if name == _ASSET_CODE:
        # Left out, it has no value to read as: the union has no arm for 0, the
        # native asset.
        return r.parse(path, _read_asset_code, None)
    if d[0] == "struct":
        values = {}
        for field, attribute, t in d[2]:
            renamed = _ACCOUNTS.get((name, field))
            if renamed is not None:
                at = join(path, renamed)
                values[attribute] = r.parse(at, read_account, ZERO_ACCOUNT)
            else:
                values[attribute] = _read(r, t, join(path, field))
        return getattr(stellar_xdr, d[1])(**values)
    _, namespace, switch, _, switch_type, arms = d
    at = join(path, switch)
    discriminant = _read(r, switch_type, at)
    arm_class, arm, _, t = r.arm(arms, discriminant, at, name)
    cls = getattr(getattr(stellar_xdr, namespace), arm_class)
    if t is None:
        return cls()
    return cls(_read(r, t, path if _inlined(t) else join(path, arm)))


def _read_asset(name: str, text: str) -> Any:
    """An Asset or a TrustLineAsset from `native`, `CODE:ISSUER` or `ID:lp`."""
    union = getattr(stellar_xdr, name)
    kind = asset_kind(text, pool_share=_ASSETS[name])
    if kind == NATIVE:
        return union.Native()
    if kind == POOL_SHARE:
        return union.PoolShare(read_pool_share(text))
    if kind == ALPHANUM4:
        return union.CreditAlphaNum4(_read_alphanum("AlphaNum4", text))
    return union.CreditAlphaNum12(_read_alphanum("AlphaNum12", text))


def _read_alphanum(name: str, text: str) -> Any:
    """An AlphaNum4 or an AlphaNum12 from `CODE:ISSUER`."""
    code, issuer = split_asset(text)
    size = 4 if name == "AlphaNum4" else 12
    asset_code = read_code(code, size).ljust(size, b"\0")
    return getattr(stellar_xdr, name)(
        asset_code, stellar_xdr.PublicKey.from_json_value(issuer)
    )


def _read_asset_code(text: str) -> Any:
    code = read_code(text, 12)
    if len(code) <= ALPHANUM4:
        return stellar_xdr.AssetCode.CreditAlphaNum4(code.ljust(4, b"\0"))
    return stellar_xdr.AssetCode.CreditAlphaNum12(code.ljust(12, b"\0"))


def _inlined(t: tuple[Any, ...]) -> bool:
    """Whether a union arm holding `t` has its fields written as the union's own."""
    return t[0] == "ref" and _INLINED.fullmatch(t[1]) is not None
