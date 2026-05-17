from __future__ import annotations

import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep._wasm import CONTRACT_SPEC_SECTION_NAME
from stellar_sdk.sep._xdr_stream import (
    parse_sc_spec_entries,
    serialize_sc_spec_entries,
)
from stellar_sdk.sep.contract_spec import ContractSpec
from stellar_sdk.sep.exceptions import InvalidWasmError

from .contract_introspection_helpers import custom_section, wasm


def test_contract_spec_classifies_and_finds_entries():
    function = stellar_xdr.SCSpecFunctionV0(
        doc=b"",
        name=stellar_xdr.SCSymbol(b"hello"),
        inputs=[],
        outputs=[],
    )
    struct = stellar_xdr.SCSpecUDTStructV0(
        doc=b"",
        lib=b"",
        name=b"MyStruct",
        fields=[],
    )
    event = stellar_xdr.SCSpecEventV0(
        doc=b"",
        lib=b"",
        name=stellar_xdr.SCSymbol(b"transfer"),
        prefix_topics=[],
        params=[],
        data_format=stellar_xdr.SCSpecEventDataFormat.SC_SPEC_EVENT_DATA_FORMAT_MAP,
    )
    union = stellar_xdr.SCSpecUDTUnionV0(
        doc=b"",
        lib=b"",
        name=b"MyUnion",
        cases=[],
    )
    enum = stellar_xdr.SCSpecUDTEnumV0(
        doc=b"",
        lib=b"",
        name=b"MyEnum",
        cases=[],
    )
    error_enum = stellar_xdr.SCSpecUDTErrorEnumV0(
        doc=b"",
        lib=b"",
        name=b"MyError",
        cases=[],
    )
    entries = (
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0,
            function_v0=function,
        ),
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0,
            udt_struct_v0=struct,
        ),
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_EVENT_V0,
            event_v0=event,
        ),
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0,
            udt_union_v0=union,
        ),
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0,
            udt_enum_v0=enum,
        ),
        stellar_xdr.SCSpecEntry(
            stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0,
            udt_error_enum_v0=error_enum,
        ),
    )
    module = wasm(
        custom_section(CONTRACT_SPEC_SECTION_NAME, serialize_sc_spec_entries(entries))
    )

    spec = ContractSpec.from_wasm(module)
    assert tuple(spec) == entries
    assert spec == ContractSpec.from_xdr_bytes(spec.to_xdr_bytes())
    assert repr(spec).startswith("<ContractSpec [entries=")
    with pytest.raises(TypeError, match="unhashable"):
        hash(spec)
    assert spec.to_xdr_bytes() == serialize_sc_spec_entries(entries)
    assert spec.functions == (function,)
    assert spec.structs == (struct,)
    assert spec.events == (event,)
    assert spec.unions == (union,)
    assert spec.enums == (enum,)
    assert spec.error_enums == (error_enum,)
    assert spec.get_function("hello") == function
    assert spec.get_udt("MyStruct") == entries[1]
    assert spec.get_udt("MyUnion") == entries[3]
    assert spec.get_udt("MyEnum") == entries[4]
    assert spec.get_udt("MyError") == entries[5]
    assert spec.get_event("transfer") == event
    assert spec.get_function("missing") is None
    assert spec.get_event("missing") is None
    assert spec.get_udt("missing") is None
    assert parse_sc_spec_entries(spec.to_xdr_bytes()) == entries
    with pytest.raises(AttributeError):
        setattr(spec, "entries", ())


def test_contract_spec_empty_and_from_wasm_file(tmp_path):
    module = wasm()
    path = tmp_path / "contract.wasm"
    path.write_bytes(module)

    assert len(ContractSpec.from_wasm(module)) == 0
    assert len(ContractSpec.from_wasm_file(path)) == 0


def test_contract_spec_lookup_decode_errors():
    function = stellar_xdr.SCSpecFunctionV0(
        doc=b"",
        name=stellar_xdr.SCSymbol(b"\xff"),
        inputs=[],
        outputs=[],
    )
    spec = ContractSpec(
        (
            stellar_xdr.SCSpecEntry(
                stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0,
                function_v0=function,
            ),
        )
    )

    with pytest.raises(InvalidWasmError, match="non-UTF-8"):
        spec.get_function("invalid")

    invalid_udt = ContractSpec(
        (
            stellar_xdr.SCSpecEntry(
                stellar_xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0,
                udt_struct_v0=stellar_xdr.SCSpecUDTStructV0(
                    doc=b"",
                    lib=b"",
                    name=b"\xff",
                    fields=[],
                ),
            ),
        )
    )
    with pytest.raises(InvalidWasmError, match="non-UTF-8"):
        invalid_udt.get_udt("invalid")


def test_contract_spec_rejects_multiple_sections():
    module = wasm(
        custom_section(CONTRACT_SPEC_SECTION_NAME, b""),
        custom_section(CONTRACT_SPEC_SECTION_NAME, b""),
    )

    with pytest.raises(InvalidWasmError, match="expected at most one"):
        ContractSpec.from_wasm(module)
