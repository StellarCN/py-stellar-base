from __future__ import annotations

from collections.abc import Iterator

from .exceptions import InvalidWasmError

CONTRACT_META_SECTION_NAME = "contractmetav0"
CONTRACT_SPEC_SECTION_NAME = "contractspecv0"
CONTRACT_ENV_META_SECTION_NAME = "contractenvmetav0"

__all__ = [
    "CONTRACT_ENV_META_SECTION_NAME",
    "CONTRACT_META_SECTION_NAME",
    "CONTRACT_SPEC_SECTION_NAME",
    "get_wasm_custom_sections",
    "iter_wasm_custom_sections",
]

_WASM_MAGIC = b"\x00asm"
_WASM_VERSION_1 = b"\x01\x00\x00\x00"
_CUSTOM_SECTION_ID = 0
_MAX_LEB128_U32_BYTES = 5


def iter_wasm_custom_sections(
    wasm: bytes, name: str | None = None
) -> Iterator[tuple[str, bytes]]:
    """Iterate Wasm custom sections in module order.

    :param wasm: The raw Wasm module bytes.
    :param name: Optional custom section name filter.
    :return: An iterator of ``(section_name, section_payload)`` tuples.
    :raises InvalidWasmError: If the Wasm module or custom section framing is invalid.
    """
    if not isinstance(wasm, bytes):
        raise TypeError("wasm must be bytes")
    if len(wasm) < 8:
        raise InvalidWasmError("Invalid Wasm module: header is too short.")
    if wasm[:4] != _WASM_MAGIC:
        raise InvalidWasmError("Invalid Wasm module: bad magic header.")
    if wasm[4:8] != _WASM_VERSION_1:
        raise InvalidWasmError("Invalid Wasm module: unsupported version.")

    offset = 8
    wasm_len = len(wasm)
    while offset < wasm_len:
        section_id = wasm[offset]
        offset += 1

        section_size, offset = _read_u32_leb128(wasm, offset)
        section_end = offset + section_size
        if section_end > wasm_len:
            raise InvalidWasmError("Invalid Wasm module: section extends past EOF.")

        if section_id == _CUSTOM_SECTION_ID:
            section_name, payload_offset = _read_name(wasm, offset, section_end)
            if name is None or section_name == name:
                yield section_name, wasm[payload_offset:section_end]

        offset = section_end

    if offset != wasm_len:
        raise InvalidWasmError("Invalid Wasm module: trailing bytes after sections.")


def get_wasm_custom_sections(wasm: bytes, name: str) -> tuple[bytes, ...]:
    """Return all custom section payloads with the given name."""
    return tuple(data for _, data in iter_wasm_custom_sections(wasm, name))


def _read_name(data: bytes, offset: int, limit: int) -> tuple[str, int]:
    name_len, offset = _read_u32_leb128(data, offset, limit)
    name_end = offset + name_len
    if name_end > limit:
        raise InvalidWasmError("Invalid Wasm custom section: name extends past EOF.")
    try:
        name = data[offset:name_end].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidWasmError(
            "Invalid Wasm custom section: name is not UTF-8."
        ) from exc
    return name, name_end


def _read_u32_leb128(
    data: bytes, offset: int, limit: int | None = None
) -> tuple[int, int]:
    if limit is None:
        limit = len(data)

    result = 0
    shift = 0
    for _ in range(_MAX_LEB128_U32_BYTES):
        if offset >= limit:
            raise InvalidWasmError("Invalid Wasm module: truncated LEB128 value.")
        byte = data[offset]
        offset += 1

        result |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            if result > 0xFFFFFFFF:
                raise InvalidWasmError("Invalid Wasm module: LEB128 value exceeds u32.")
            return result, offset
        shift += 7

    raise InvalidWasmError("Invalid Wasm module: LEB128 value is too long.")
