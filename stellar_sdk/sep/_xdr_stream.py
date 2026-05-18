from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Protocol, TypeVar

from xdrlib3 import ConversionError, Packer, Unpacker

from .. import xdr as stellar_xdr
from .exceptions import InvalidWasmError

__all__ = [
    "parse_sc_meta_entries",
    "parse_sc_spec_entries",
    "parse_sc_env_meta_entries",
    "serialize_sc_meta_entries",
    "serialize_sc_spec_entries",
    "serialize_sc_env_meta_entries",
]


class _XdrPackable(Protocol):
    def pack(self, packer: Packer) -> None: ...


_XdrEntry = TypeVar("_XdrEntry", bound=_XdrPackable)


def parse_sc_meta_entries(data: bytes) -> tuple[stellar_xdr.SCMetaEntry, ...]:
    """Parse a SEP-46 stream of ``SCMetaEntry`` values."""
    return _parse_xdr_stream(data, stellar_xdr.SCMetaEntry.unpack, "SCMetaEntry")


def parse_sc_spec_entries(data: bytes) -> tuple[stellar_xdr.SCSpecEntry, ...]:
    """Parse a SEP-48 stream of ``SCSpecEntry`` values."""
    return _parse_xdr_stream(data, stellar_xdr.SCSpecEntry.unpack, "SCSpecEntry")


def parse_sc_env_meta_entries(data: bytes) -> tuple[stellar_xdr.SCEnvMetaEntry, ...]:
    """Parse a stream of ``SCEnvMetaEntry`` values."""
    return _parse_xdr_stream(data, stellar_xdr.SCEnvMetaEntry.unpack, "SCEnvMetaEntry")


def serialize_sc_meta_entries(
    entries: Iterable[stellar_xdr.SCMetaEntry],
) -> bytes:
    """Serialize ``SCMetaEntry`` values as an unframed XDR stream."""
    return _serialize_xdr_stream(entries)


def serialize_sc_spec_entries(
    entries: Iterable[stellar_xdr.SCSpecEntry],
) -> bytes:
    """Serialize ``SCSpecEntry`` values as an unframed XDR stream."""
    return _serialize_xdr_stream(entries)


def serialize_sc_env_meta_entries(
    entries: Iterable[stellar_xdr.SCEnvMetaEntry],
) -> bytes:
    """Serialize ``SCEnvMetaEntry`` values as an unframed XDR stream."""
    return _serialize_xdr_stream(entries)


def _parse_xdr_stream(
    data: bytes,
    unpack_entry: Callable[[Unpacker], _XdrEntry],
    entry_name: str,
) -> tuple[_XdrEntry, ...]:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    unpacker = Unpacker(data)
    entries: list[_XdrEntry] = []
    while unpacker.get_position() < len(data):
        before = unpacker.get_position()
        try:
            entry = unpack_entry(unpacker)
        except (EOFError, ValueError, ConversionError) as exc:
            raise InvalidWasmError(f"Invalid XDR stream for {entry_name}.") from exc
        after = unpacker.get_position()
        if after <= before:
            raise InvalidWasmError(
                f"Invalid XDR stream for {entry_name}: decoder made no progress."
            )
        entries.append(entry)

    if unpacker.get_position() != len(data):
        raise InvalidWasmError(f"Invalid XDR stream for {entry_name}: trailing bytes.")
    return tuple(entries)


def _serialize_xdr_stream(entries: Iterable[_XdrPackable]) -> bytes:
    packer = Packer()
    for entry in entries:
        entry.pack(packer)
    return packer.get_buffer()
