from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from .. import xdr as stellar_xdr
from ._wasm import CONTRACT_META_SECTION_NAME, get_wasm_custom_sections
from ._xdr_stream import parse_sc_meta_entries, serialize_sc_meta_entries
from .exceptions import InvalidWasmError

__all__ = ["ContractMeta"]


class ContractMeta:
    """The :class:`ContractMeta` object, which represents SEP-46 contract
    metadata.

    ``entries`` are normalized to a tuple in entry order.

    :param entries: The raw SEP-46 metadata XDR entries.
    """

    __slots__ = ("entries",)

    def __init__(self, entries: tuple[stellar_xdr.SCMetaEntry, ...] = ()) -> None:
        self.entries = tuple(entries)

    @classmethod
    def from_wasm(cls, wasm: bytes) -> "ContractMeta":
        """Creates a :class:`ContractMeta` object from contract Wasm bytes.

        :param wasm: The contract Wasm bytes.
        :return: A :class:`ContractMeta` object.
        :raises InvalidWasmError: If the Wasm module or metadata section cannot be decoded.
        """
        entries: list[stellar_xdr.SCMetaEntry] = []
        for section in get_wasm_custom_sections(wasm, CONTRACT_META_SECTION_NAME):
            entries.extend(parse_sc_meta_entries(section))
        return cls(tuple(entries))

    @classmethod
    def from_wasm_file(cls, path: str | os.PathLike[str]) -> "ContractMeta":
        """Creates a :class:`ContractMeta` object from a contract Wasm file.

        :param path: The path to the contract Wasm file.
        :return: A :class:`ContractMeta` object.
        :raises InvalidWasmError: If the Wasm module or metadata section cannot be decoded.
        """
        return cls.from_wasm(Path(path).read_bytes())

    @classmethod
    def from_xdr_bytes(cls, data: bytes) -> "ContractMeta":
        """Creates a :class:`ContractMeta` object from SEP-46 XDR stream bytes.

        :param data: The XDR stream bytes.
        :return: A :class:`ContractMeta` object.
        :raises InvalidWasmError: If the XDR stream cannot be decoded.
        """
        return cls(parse_sc_meta_entries(data))

    def to_xdr_bytes(self) -> bytes:
        """Serializes the metadata entries as SEP-46 XDR stream bytes.

        :return: The XDR stream bytes.
        """
        return serialize_sc_meta_entries(self.entries)

    def items(self) -> tuple[tuple[str, str], ...]:
        """Returns ``SC_META_V0`` key/value pairs in entry order.

        :return: The decoded key/value pairs.
        :raises InvalidWasmError: If a key or value is not UTF-8.
        """
        items: list[tuple[str, str]] = []
        for entry in self.entries:
            if entry.kind != stellar_xdr.SCMetaKind.SC_META_V0 or entry.v0 is None:
                continue
            items.append(
                (_decode_meta_string(entry.v0.key), _decode_meta_string(entry.v0.val))
            )
        return tuple(items)

    def get(self, key: str, default: str | None = None) -> str | None:
        """Returns the first ``SC_META_V0`` value for ``key``.

        :param key: The metadata key.
        :param default: The default value returned when the key is not present.
        :return: The metadata value or ``default``.
        :raises InvalidWasmError: If a key or value is not UTF-8.
        """
        for item_key, item_value in self.items():
            if item_key == key:
                return item_value
        return default

    def get_all(self, key: str) -> tuple[str, ...]:
        """Returns all ``SC_META_V0`` values for ``key`` in entry order.

        :param key: The metadata key.
        :return: All metadata values for the key.
        :raises InvalidWasmError: If a key or value is not UTF-8.
        """
        return tuple(
            item_value for item_key, item_value in self.items() if item_key == key
        )

    def supported_seps(self, strict: bool = False) -> tuple[int, ...]:
        """Returns SEP-47 SEP identifiers from ``sep`` meta entries.

        Values are returned in first-seen order with duplicates removed. Invalid
        identifiers are skipped by default and raise ``ValueError`` when
        ``strict`` is true.

        :param strict: Whether to reject invalid SEP identifiers.
        :return: SEP identifiers declared by the contract.
        :raises ValueError: If ``strict`` is true and an identifier is invalid.
        :raises InvalidWasmError: If a key or value is not UTF-8.
        """
        seen: set[int] = set()
        supported: list[int] = []
        for value in self.get_all("sep"):
            for part in value.split(","):
                sep = part.strip()
                if not sep:
                    if strict:
                        raise ValueError("Invalid SEP identifier: empty value.")
                    continue
                if not sep.isdecimal():
                    if strict:
                        raise ValueError(f"Invalid SEP identifier: {sep!r}.")
                    continue
                sep_number = int(sep)
                if sep_number not in seen:
                    seen.add(sep_number)
                    supported.append(sep_number)
        return tuple(supported)

    def implements_sep(self, sep: int) -> bool:
        """Returns whether the contract declares support for ``sep`` via SEP-47.

        :param sep: The SEP number.
        :return: ``True`` if the contract declares support for the SEP.
        """
        if not isinstance(sep, int):
            raise TypeError("sep must be int")
        return sep in self.supported_seps()

    def __iter__(self) -> Iterator[stellar_xdr.SCMetaEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, key: object) -> bool:
        """Returns whether an ``SC_META_V0`` entry exists for ``key``."""
        if not isinstance(key, str):
            return False
        return any(item_key == key for item_key, _ in self.items())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContractMeta):
            return NotImplemented
        return self.entries == other.entries

    def __repr__(self) -> str:
        return f"<ContractMeta [entries={self.entries}]>"


def _decode_meta_string(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidWasmError("Contract meta contains a non-UTF-8 string.") from exc
