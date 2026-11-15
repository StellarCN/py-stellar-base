from __future__ import annotations

from collections.abc import Iterable

from .. import xdr as stellar_xdr
from .exceptions import InvalidWasmError

__all__ = [
    "parse_sc_env_meta_entries",
    "parse_sc_meta_entries",
    "parse_sc_spec_entries",
    "serialize_sc_env_meta_entries",
    "serialize_sc_meta_entries",
    "serialize_sc_spec_entries",
]


def parse_sc_meta_entries(data: bytes) -> tuple[stellar_xdr.SCMetaEntry.Any, ...]:
    """Parse a SEP-46 stream of ``SCMetaEntry`` values."""
    try:
        return tuple(stellar_xdr.decode_stream(stellar_xdr.SCMetaEntry, data))
    except stellar_xdr.XdrError as exc:
        raise InvalidWasmError("Invalid XDR stream for SCMetaEntry.") from exc


def parse_sc_spec_entries(data: bytes) -> tuple[stellar_xdr.SCSpecEntry.Any, ...]:
    """Parse a SEP-48 stream of ``SCSpecEntry`` values."""
    try:
        return tuple(stellar_xdr.decode_stream(stellar_xdr.SCSpecEntry, data))
    except stellar_xdr.XdrError as exc:
        raise InvalidWasmError("Invalid XDR stream for SCSpecEntry.") from exc


def parse_sc_env_meta_entries(
    data: bytes,
) -> tuple[stellar_xdr.SCEnvMetaEntry.Any, ...]:
    """Parse a stream of ``SCEnvMetaEntry`` values."""
    try:
        return tuple(stellar_xdr.decode_stream(stellar_xdr.SCEnvMetaEntry, data))
    except stellar_xdr.XdrError as exc:
        raise InvalidWasmError("Invalid XDR stream for SCEnvMetaEntry.") from exc


def serialize_sc_meta_entries(
    entries: Iterable[stellar_xdr.SCMetaEntry.Any],
) -> bytes:
    """Serialize ``SCMetaEntry`` values as an unframed XDR stream."""
    return stellar_xdr.encode_stream(entries)


def serialize_sc_spec_entries(
    entries: Iterable[stellar_xdr.SCSpecEntry.Any],
) -> bytes:
    """Serialize ``SCSpecEntry`` values as an unframed XDR stream."""
    return stellar_xdr.encode_stream(entries)


def serialize_sc_env_meta_entries(
    entries: Iterable[stellar_xdr.SCEnvMetaEntry.Any],
) -> bytes:
    """Serialize ``SCEnvMetaEntry`` values as an unframed XDR stream."""
    return stellar_xdr.encode_stream(entries)
