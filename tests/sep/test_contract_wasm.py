from __future__ import annotations

import pytest

from stellar_sdk.sep._wasm import (
    CONTRACT_META_SECTION_NAME,
    _read_u32_leb128,
    get_wasm_custom_sections,
    iter_wasm_custom_sections,
)
from stellar_sdk.sep._xdr_stream import serialize_sc_meta_entries
from stellar_sdk.sep.exceptions import InvalidWasmError

from .contract_introspection_helpers import custom_section, meta_entry, wasm


def test_wasm_custom_sections_are_returned_in_order():
    meta_a = meta_entry("sep", "0041,40")
    meta_b = meta_entry("sep", "48")
    payload_a = serialize_sc_meta_entries([meta_a])
    payload_b = serialize_sc_meta_entries([meta_b])
    module = wasm(
        custom_section(CONTRACT_META_SECTION_NAME, payload_a),
        custom_section("unrelated", b"ignored"),
        custom_section(CONTRACT_META_SECTION_NAME, payload_b),
    )

    assert get_wasm_custom_sections(module, CONTRACT_META_SECTION_NAME) == (
        payload_a,
        payload_b,
    )
    assert tuple(iter_wasm_custom_sections(module, "unrelated")) == (
        ("unrelated", b"ignored"),
    )


def test_invalid_wasm_framing():
    with pytest.raises(TypeError, match="wasm must be bytes"):
        tuple(iter_wasm_custom_sections("not bytes"))  # type: ignore[arg-type]

    with pytest.raises(InvalidWasmError, match="header is too short"):
        tuple(iter_wasm_custom_sections(b"\x00asm"))

    with pytest.raises(InvalidWasmError, match="bad magic"):
        tuple(iter_wasm_custom_sections(b"not wasm"))

    with pytest.raises(InvalidWasmError, match="unsupported version"):
        tuple(iter_wasm_custom_sections(b"\x00asm\x02\x00\x00\x00"))

    # Section size says 2 bytes, but only one byte is present.
    malformed = b"\x00asm\x01\x00\x00\x00" + b"\x00\x02\x00"
    with pytest.raises(InvalidWasmError, match="section extends past EOF"):
        tuple(iter_wasm_custom_sections(malformed))

    # Custom section name length says 2 bytes, but only one byte is present.
    malformed = b"\x00asm\x01\x00\x00\x00" + b"\x00\x02\x02a"
    with pytest.raises(InvalidWasmError, match="name extends past EOF"):
        tuple(iter_wasm_custom_sections(malformed))

    malformed = b"\x00asm\x01\x00\x00\x00" + b"\x00\x02\x01\xff"
    with pytest.raises(InvalidWasmError, match="name is not UTF-8"):
        tuple(iter_wasm_custom_sections(malformed))

    malformed = b"\x00asm\x01\x00\x00\x00" + b"\x00\x80"
    with pytest.raises(InvalidWasmError, match="truncated LEB128"):
        tuple(iter_wasm_custom_sections(malformed))

    malformed = b"\x00asm\x01\x00\x00\x00" + b"\x00\x80\x80\x80\x80\x80\x00"
    with pytest.raises(InvalidWasmError, match="too long"):
        tuple(iter_wasm_custom_sections(malformed))

    with pytest.raises(InvalidWasmError, match="exceeds u32"):
        _read_u32_leb128(b"\xff\xff\xff\xff\x1f", 0)


def test_wasm_custom_section_with_multibyte_lengths():
    name = "a" * 130
    payload = b"payload"
    module = wasm(custom_section(name, payload))

    assert get_wasm_custom_sections(module, name) == (payload,)
