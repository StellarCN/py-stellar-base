from __future__ import annotations

from types import SimpleNamespace

import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep._wasm import CONTRACT_META_SECTION_NAME
from stellar_sdk.sep._xdr_stream import serialize_sc_meta_entries
from stellar_sdk.sep.contract_meta import ContractMeta
from stellar_sdk.sep.exceptions import InvalidWasmError

from .contract_introspection_helpers import custom_section, meta_entry, wasm


def test_contract_meta_from_wasm_merges_sections_in_order():
    meta_a = meta_entry("sep", "0041,40")
    meta_b = meta_entry("sep", "48")
    module = wasm(
        custom_section(CONTRACT_META_SECTION_NAME, serialize_sc_meta_entries([meta_a])),
        custom_section("unrelated", b"ignored"),
        custom_section(CONTRACT_META_SECTION_NAME, serialize_sc_meta_entries([meta_b])),
    )

    meta = ContractMeta.from_wasm(module)
    assert len(meta) == 2
    assert "sep" in meta
    assert meta.items() == (("sep", "0041,40"), ("sep", "48"))
    assert meta.get("sep") == "0041,40"
    assert meta.get_all("sep") == ("0041,40", "48")


def test_contract_meta_from_xdr_bytes_round_trip():
    entries = (meta_entry("key", "value"), meta_entry("other", "value"))
    data = serialize_sc_meta_entries(entries)

    meta = ContractMeta.from_xdr_bytes(data)
    assert meta.entries == entries
    assert meta.to_xdr_bytes() == data
    assert tuple(meta) == entries


def test_contract_meta_from_wasm_file(tmp_path):
    module = wasm()
    path = tmp_path / "contract.wasm"
    path.write_bytes(module)

    assert ContractMeta.from_wasm_file(path).entries == ()


def test_contract_meta_supported_seps():
    meta = ContractMeta((meta_entry("sep", "0041,40"), meta_entry("sep", "48")))

    assert meta.supported_seps() == (41, 40, 48)
    assert meta.implements_sep(41)


def test_contract_meta_supported_seps_strict_validation():
    meta = ContractMeta((meta_entry("sep", "41,bad"),))

    assert meta.supported_seps() == (41,)
    with pytest.raises(ValueError, match="Invalid SEP identifier"):
        meta.supported_seps(strict=True)
    with pytest.raises(TypeError, match="sep must be int"):
        meta.implements_sep("41")  # type: ignore[arg-type]

    meta = ContractMeta((meta_entry("sep", "41,,48"),))
    assert meta.supported_seps() == (41, 48)
    with pytest.raises(ValueError, match="empty value"):
        meta.supported_seps(strict=True)


def test_contract_meta_value_semantics_and_decode_errors():
    meta = ContractMeta((meta_entry("key", "value"),))
    assert meta == ContractMeta.from_xdr_bytes(meta.to_xdr_bytes())
    assert repr(meta).startswith("<ContractMeta [entries=")
    assert meta.get("missing", "default") == "default"
    assert 123 not in meta
    with pytest.raises(TypeError, match="unhashable"):
        hash(meta)
    with pytest.raises(AttributeError):
        setattr(meta, "entries", ())  # noqa: B010

    invalid = ContractMeta(
        (
            stellar_xdr.SCMetaEntry(
                stellar_xdr.SCMetaKind.SC_META_V0,
                v0=stellar_xdr.SCMetaV0(b"key", b"\xff"),
            ),
        )
    )
    with pytest.raises(InvalidWasmError, match="non-UTF-8"):
        invalid.items()

    meta = ContractMeta((SimpleNamespace(kind=object(), v0=None),))  # type: ignore[arg-type]
    assert meta.items() == ()
