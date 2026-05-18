from __future__ import annotations

import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep._wasm import (
    CONTRACT_ENV_META_SECTION_NAME,
    CONTRACT_META_SECTION_NAME,
    CONTRACT_SPEC_SECTION_NAME,
)
from stellar_sdk.sep._xdr_stream import serialize_sc_meta_entries
from stellar_sdk.sep.contract_info import ContractInfo
from stellar_sdk.sep.contract_spec import ContractSpec
from stellar_sdk.sep.exceptions import InvalidWasmError

from .contract_introspection_helpers import (
    custom_section,
    meta_entry,
    serialize_entries,
    wasm,
)


def test_contract_info_reads_env_meta():
    env_entry = stellar_xdr.SCEnvMetaEntry(
        stellar_xdr.SCEnvMetaKind.SC_ENV_META_KIND_INTERFACE_VERSION,
        interface_version=stellar_xdr.SCEnvMetaEntryInterfaceVersion(
            protocol=stellar_xdr.Uint32(23),
            pre_release=stellar_xdr.Uint32(0),
        ),
    )
    module = wasm(
        custom_section(
            CONTRACT_META_SECTION_NAME,
            serialize_sc_meta_entries([meta_entry("name", "demo")]),
        ),
        custom_section(
            CONTRACT_ENV_META_SECTION_NAME,
            serialize_entries([env_entry]),
        ),
    )

    info = ContractInfo.from_wasm(module)
    assert info.meta.items() == (("name", "demo"),)
    assert len(info.spec) == 0
    assert info.env_meta == (env_entry,)


def test_contract_info_without_env_meta_uses_empty_tuple():
    module = wasm(
        custom_section(
            CONTRACT_META_SECTION_NAME,
            serialize_sc_meta_entries([meta_entry("name", "demo")]),
        )
    )

    info = ContractInfo.from_wasm(module)
    assert info.meta.items() == (("name", "demo"),)
    assert len(info.spec) == 0
    assert info.env_meta == ()
    assert info == ContractInfo(info.meta, info.spec)
    assert repr(info).startswith("<ContractInfo [meta=")
    with pytest.raises(TypeError, match="unhashable"):
        hash(info)
    with pytest.raises(AttributeError):
        setattr(info, "meta", info.meta)
    with pytest.raises(AttributeError):
        setattr(info, "spec", ContractSpec())
    with pytest.raises(AttributeError):
        setattr(info, "env_meta", ())


def test_contract_info_from_wasm_file(tmp_path):
    path = tmp_path / "contract.wasm"
    path.write_bytes(wasm())

    info = ContractInfo.from_wasm_file(path)

    assert len(info.meta) == 0
    assert len(info.spec) == 0
    assert info.env_meta == ()


def test_contract_info_rejects_multiple_spec_sections():
    module = wasm(
        custom_section(CONTRACT_SPEC_SECTION_NAME, b""),
        custom_section(CONTRACT_SPEC_SECTION_NAME, b""),
    )

    with pytest.raises(InvalidWasmError, match="expected at most one"):
        ContractInfo.from_wasm(module)
