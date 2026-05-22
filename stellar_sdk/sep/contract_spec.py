from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from .. import xdr as stellar_xdr
from ._wasm import CONTRACT_SPEC_SECTION_NAME, get_wasm_custom_sections
from ._xdr_stream import parse_sc_spec_entries, serialize_sc_spec_entries
from .exceptions import InvalidWasmError

__all__ = ["ContractSpec"]


class ContractSpec:
    """The :class:`ContractSpec` object, which represents a SEP-48 contract
    interface specification.

    ``entries`` are normalized to a read-only tuple in entry order.

    :param entries: The raw SEP-48 specification XDR entries.
    """

    __slots__ = ("_entries",)

    def __init__(self, entries: tuple[stellar_xdr.SCSpecEntry, ...] = ()) -> None:
        self._entries = tuple(entries)

    @property
    def entries(self) -> tuple[stellar_xdr.SCSpecEntry, ...]:
        """Returns the raw SEP-48 specification XDR entries."""
        return self._entries

    @classmethod
    def from_wasm(cls, wasm: bytes) -> ContractSpec:
        """Creates a :class:`ContractSpec` object from contract Wasm bytes.

        :param wasm: The contract Wasm bytes.
        :return: A :class:`ContractSpec` object.
        :raises InvalidWasmError: If the Wasm module or specification section cannot be decoded.
        """
        sections = get_wasm_custom_sections(wasm, CONTRACT_SPEC_SECTION_NAME)
        if len(sections) > 1:
            raise InvalidWasmError(
                f"Invalid Wasm module: expected at most one {CONTRACT_SPEC_SECTION_NAME!r} section."
            )
        if not sections:
            return cls()
        return cls(parse_sc_spec_entries(sections[0]))

    @classmethod
    def from_wasm_file(cls, path: str | os.PathLike[str]) -> ContractSpec:
        """Creates a :class:`ContractSpec` object from a contract Wasm file.

        :param path: The path to the contract Wasm file.
        :return: A :class:`ContractSpec` object.
        :raises InvalidWasmError: If the Wasm module or specification section cannot be decoded.
        """
        return cls.from_wasm(Path(path).read_bytes())

    @classmethod
    def from_xdr_bytes(cls, data: bytes) -> ContractSpec:
        """Creates a :class:`ContractSpec` object from SEP-48 XDR stream bytes.

        :param data: The XDR stream bytes.
        :return: A :class:`ContractSpec` object.
        :raises InvalidWasmError: If the XDR stream cannot be decoded.
        """
        return cls(parse_sc_spec_entries(data))

    def to_xdr_bytes(self) -> bytes:
        """Serializes the specification entries as SEP-48 XDR stream bytes.

        :return: The XDR stream bytes.
        """
        return serialize_sc_spec_entries(self.entries)

    @property
    def functions(self) -> tuple[stellar_xdr.SCSpecFunctionV0, ...]:
        """Returns all function entries."""
        return tuple(
            entry.function_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0
            and entry.function_v0 is not None
        )

    @property
    def events(self) -> tuple[stellar_xdr.SCSpecEventV0, ...]:
        """Returns all event entries."""
        return tuple(
            entry.event_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_EVENT_V0
            and entry.event_v0 is not None
        )

    @property
    def structs(self) -> tuple[stellar_xdr.SCSpecUDTStructV0, ...]:
        """Returns all struct entries."""
        return tuple(
            entry.udt_struct_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0
            and entry.udt_struct_v0 is not None
        )

    @property
    def unions(self) -> tuple[stellar_xdr.SCSpecUDTUnionV0, ...]:
        """Returns all union entries."""
        return tuple(
            entry.udt_union_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0
            and entry.udt_union_v0 is not None
        )

    @property
    def enums(self) -> tuple[stellar_xdr.SCSpecUDTEnumV0, ...]:
        """Returns all enum entries."""
        return tuple(
            entry.udt_enum_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0
            and entry.udt_enum_v0 is not None
        )

    @property
    def error_enums(self) -> tuple[stellar_xdr.SCSpecUDTErrorEnumV0, ...]:
        """Returns all error enum entries."""
        return tuple(
            entry.udt_error_enum_v0
            for entry in self.entries
            if entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0
            and entry.udt_error_enum_v0 is not None
        )

    def get_function(self, name: str) -> stellar_xdr.SCSpecFunctionV0 | None:
        """Returns a function by name.

        :param name: The function name.
        :return: The function entry if present.
        :raises InvalidWasmError: If a function name is not UTF-8.
        """
        for function in self.functions:
            if _decode_symbol(function.name) == name:
                return function
        return None

    def get_event(self, name: str) -> stellar_xdr.SCSpecEventV0 | None:
        """Returns an event by name.

        :param name: The event name.
        :return: The event entry if present.
        :raises InvalidWasmError: If an event name is not UTF-8.
        """
        for event in self.events:
            if _decode_symbol(event.name) == name:
                return event
        return None

    def get_udt(self, name: str) -> stellar_xdr.SCSpecEntry | None:
        """Returns a user-defined type by name.

        :param name: The type name.
        :return: The user-defined type entry if present.
        :raises InvalidWasmError: If a type name is not UTF-8.
        """
        for entry in self.entries:
            udt_name = _get_udt_name(entry)
            if udt_name == name:
                return entry
        return None

    def __iter__(self) -> Iterator[stellar_xdr.SCSpecEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContractSpec):
            return NotImplemented
        return self.entries == other.entries

    def __repr__(self) -> str:
        return f"<ContractSpec [entries={self.entries}]>"


def _decode_symbol(symbol: stellar_xdr.SCSymbol) -> str:
    try:
        return symbol.sc_symbol.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidWasmError("Contract spec contains a non-UTF-8 symbol.") from exc


def _decode_string(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidWasmError("Contract spec contains a non-UTF-8 string.") from exc


def _get_udt_name(entry: stellar_xdr.SCSpecEntry) -> str | None:
    if (
        entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0
        and entry.udt_struct_v0 is not None
    ):
        return _decode_string(entry.udt_struct_v0.name)
    if (
        entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0
        and entry.udt_union_v0 is not None
    ):
        return _decode_string(entry.udt_union_v0.name)
    if (
        entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0
        and entry.udt_enum_v0 is not None
    ):
        return _decode_string(entry.udt_enum_v0.name)
    if (
        entry.kind == stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0
        and entry.udt_error_enum_v0 is not None
    ):
        return _decode_string(entry.udt_error_enum_v0.name)
    return None
