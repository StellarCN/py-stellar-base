from __future__ import annotations

from types import MethodType, SimpleNamespace

import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.exceptions import (
    ContractCodeNotFoundError,
    ContractInstanceNotFoundError,
    ContractWasmRetrievalError,
    SACHasNoWasmError,
)
from stellar_sdk.soroban_server import SorobanServer
from stellar_sdk.soroban_server_async import SorobanServerAsync

CONTRACT_ID = "CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABSC4"


def test_get_contract_wasm_by_hash(monkeypatch):
    wasm_hash = b"\x01" * 32
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServer("https://example.com")

    def get_ledger_entries(self, keys):
        assert keys[0].contract_code is not None
        assert keys[0].contract_code.hash.hash == wasm_hash
        return SimpleNamespace(
            entries=[SimpleNamespace(xdr=_contract_code_xdr(wasm_hash, wasm))]
        )

    monkeypatch.setattr(
        server, "get_ledger_entries", MethodType(get_ledger_entries, server)
    )

    assert server.get_contract_wasm_by_hash(wasm_hash) == wasm


@pytest.mark.asyncio
async def test_get_contract_wasm_by_hash_async(monkeypatch):
    wasm_hash = b"\x01" * 32
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServerAsync("https://example.com")

    async def get_ledger_entries(self, keys):
        assert keys[0].contract_code is not None
        assert keys[0].contract_code.hash.hash == wasm_hash
        return SimpleNamespace(
            entries=[SimpleNamespace(xdr=_contract_code_xdr(wasm_hash, wasm))]
        )

    monkeypatch.setattr(
        server, "get_ledger_entries", MethodType(get_ledger_entries, server)
    )

    assert await server.get_contract_wasm_by_hash(wasm_hash) == wasm


def test_get_contract_wasm_by_hash_validates_hash():
    server = SorobanServer("https://example.com")

    with pytest.raises(ValueError, match="32 bytes"):
        server.get_contract_wasm_by_hash(b"\x01")
    with pytest.raises(ValueError, match="all zero"):
        server.get_contract_wasm_by_hash(b"\x00" * 32)
    with pytest.raises(TypeError, match="bytes"):
        server.get_contract_wasm_by_hash("01" * 32)  # type: ignore[arg-type]


def test_get_contract_wasm_handles_sac(monkeypatch):
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(lambda self, contract_id: _sac_instance(), server),
    )

    with pytest.raises(SACHasNoWasmError):
        server.get_contract_wasm(CONTRACT_ID)


@pytest.mark.asyncio
async def test_get_contract_wasm_handles_sac_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")

    async def get_contract_instance(self, contract_id):
        return _sac_instance()

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(get_contract_instance, server),
    )

    with pytest.raises(SACHasNoWasmError):
        await server.get_contract_wasm(CONTRACT_ID)


def test_get_contract_wasm_uses_instance_hash(monkeypatch):
    wasm_hash = b"\x02" * 32
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(lambda self, contract_id: _wasm_instance(wasm_hash), server),
    )
    monkeypatch.setattr(
        server,
        "get_contract_wasm_by_hash",
        MethodType(lambda self, hash: wasm if hash == wasm_hash else b"", server),
    )

    assert server.get_contract_wasm(CONTRACT_ID) == wasm


@pytest.mark.asyncio
async def test_get_contract_wasm_uses_instance_hash_async(monkeypatch):
    wasm_hash = b"\x02" * 32
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServerAsync("https://example.com")

    async def get_contract_instance(self, contract_id):
        return _wasm_instance(wasm_hash)

    async def get_contract_wasm_by_hash(self, hash):
        return wasm if hash == wasm_hash else b""

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(get_contract_instance, server),
    )
    monkeypatch.setattr(
        server,
        "get_contract_wasm_by_hash",
        MethodType(get_contract_wasm_by_hash, server),
    )

    assert await server.get_contract_wasm(CONTRACT_ID) == wasm


def test_get_contract_wasm_rejects_missing_hash(monkeypatch):
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(lambda self, contract_id: _wasm_instance(None), server),
    )

    with pytest.raises(ContractWasmRetrievalError, match="missing its Wasm hash"):
        server.get_contract_wasm(CONTRACT_ID)


def test_get_contract_wasm_rejects_unknown_executable_kind(monkeypatch):
    server = SorobanServer("https://example.com")
    instance = stellar_xdr.SCContractInstance(
        executable=stellar_xdr.ContractExecutable(999),  # type: ignore[arg-type]
        storage=None,
    )

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(lambda self, contract_id: instance, server),
    )

    with pytest.raises(ContractWasmRetrievalError, match="unsupported executable"):
        server.get_contract_wasm(CONTRACT_ID)


@pytest.mark.asyncio
async def test_get_contract_wasm_rejects_missing_hash_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")

    async def get_contract_instance(self, contract_id):
        return _wasm_instance(None)

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(get_contract_instance, server),
    )

    with pytest.raises(ContractWasmRetrievalError, match="missing its Wasm hash"):
        await server.get_contract_wasm(CONTRACT_ID)


@pytest.mark.asyncio
async def test_get_contract_wasm_rejects_unknown_executable_kind_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")
    instance = stellar_xdr.SCContractInstance(
        executable=stellar_xdr.ContractExecutable(999),  # type: ignore[arg-type]
        storage=None,
    )

    async def get_contract_instance(self, contract_id):
        return instance

    monkeypatch.setattr(
        server,
        "_get_contract_instance",
        MethodType(get_contract_instance, server),
    )

    with pytest.raises(ContractWasmRetrievalError, match="unsupported executable"):
        await server.get_contract_wasm(CONTRACT_ID)


def test_get_contract_wasm_by_hash_missing_code(monkeypatch):
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(lambda self, keys: SimpleNamespace(entries=None), server),
    )

    with pytest.raises(ContractCodeNotFoundError, match="not found or is archived"):
        server.get_contract_wasm_by_hash(b"\x01" * 32)


@pytest.mark.asyncio
async def test_get_contract_wasm_by_hash_missing_code_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")

    async def get_ledger_entries(self, keys):
        return SimpleNamespace(entries=None)

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(get_ledger_entries, server),
    )

    with pytest.raises(ContractCodeNotFoundError, match="not found or is archived"):
        await server.get_contract_wasm_by_hash(b"\x01" * 32)


def test_get_contract_wasm_by_hash_rejects_non_code_entry(monkeypatch):
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(
            lambda self, keys: SimpleNamespace(
                entries=[
                    SimpleNamespace(
                        xdr=_contract_data_xdr(
                            CONTRACT_ID,
                            stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_VOID),
                        )
                    )
                ]
            ),
            server,
        ),
    )

    with pytest.raises(
        ContractWasmRetrievalError, match="did not contain contract code"
    ):
        server.get_contract_wasm_by_hash(b"\x01" * 32)


@pytest.mark.asyncio
async def test_get_contract_wasm_by_hash_rejects_non_code_entry_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")

    async def get_ledger_entries(self, keys):
        return SimpleNamespace(
            entries=[
                SimpleNamespace(
                    xdr=_contract_data_xdr(
                        CONTRACT_ID,
                        stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_VOID),
                    )
                )
            ]
        )

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(get_ledger_entries, server),
    )

    with pytest.raises(
        ContractWasmRetrievalError, match="did not contain contract code"
    ):
        await server.get_contract_wasm_by_hash(b"\x01" * 32)


def test_get_contract_helpers_parse_wasm(monkeypatch):
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "get_contract_wasm",
        MethodType(lambda self, contract_id: wasm, server),
    )

    assert len(server.get_contract_meta(CONTRACT_ID)) == 0
    assert len(server.get_contract_spec(CONTRACT_ID)) == 0
    assert len(server.get_contract_info(CONTRACT_ID).spec) == 0


@pytest.mark.asyncio
async def test_get_contract_helpers_parse_wasm_async(monkeypatch):
    wasm = b"\x00asm\x01\x00\x00\x00"
    server = SorobanServerAsync("https://example.com")

    async def get_contract_wasm(self, contract_id):
        return wasm

    monkeypatch.setattr(
        server,
        "get_contract_wasm",
        MethodType(get_contract_wasm, server),
    )

    assert len(await server.get_contract_meta(CONTRACT_ID)) == 0
    assert len(await server.get_contract_spec(CONTRACT_ID)) == 0
    assert len((await server.get_contract_info(CONTRACT_ID)).spec) == 0


def test_get_contract_instance_errors(monkeypatch):
    server = SorobanServer("https://example.com")

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(lambda self, keys: SimpleNamespace(entries=[]), server),
    )
    with pytest.raises(ContractInstanceNotFoundError):
        server._get_contract_instance(CONTRACT_ID)

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(
            lambda self, keys: SimpleNamespace(
                entries=[SimpleNamespace(xdr=_contract_code_xdr(b"\x01" * 32, b""))]
            ),
            server,
        ),
    )
    with pytest.raises(ContractWasmRetrievalError, match="contract data"):
        server._get_contract_instance(CONTRACT_ID)

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(
            lambda self, keys: SimpleNamespace(
                entries=[
                    SimpleNamespace(
                        xdr=_contract_data_xdr(
                            CONTRACT_ID,
                            stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_VOID),
                        )
                    )
                ]
            ),
            server,
        ),
    )
    with pytest.raises(ContractWasmRetrievalError, match="contract instance"):
        server._get_contract_instance(CONTRACT_ID)


@pytest.mark.asyncio
async def test_get_contract_instance_errors_async(monkeypatch):
    server = SorobanServerAsync("https://example.com")

    async def get_no_entries(self, keys):
        return SimpleNamespace(entries=[])

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(get_no_entries, server),
    )
    with pytest.raises(ContractInstanceNotFoundError):
        await server._get_contract_instance(CONTRACT_ID)

    async def get_code_entry(self, keys):
        return SimpleNamespace(
            entries=[SimpleNamespace(xdr=_contract_code_xdr(b"\x01" * 32, b""))]
        )

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(get_code_entry, server),
    )
    with pytest.raises(ContractWasmRetrievalError, match="contract data"):
        await server._get_contract_instance(CONTRACT_ID)

    async def get_non_instance_data(self, keys):
        return SimpleNamespace(
            entries=[
                SimpleNamespace(
                    xdr=_contract_data_xdr(
                        CONTRACT_ID,
                        stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_VOID),
                    )
                )
            ]
        )

    monkeypatch.setattr(
        server,
        "get_ledger_entries",
        MethodType(get_non_instance_data, server),
    )
    with pytest.raises(ContractWasmRetrievalError, match="contract instance"):
        await server._get_contract_instance(CONTRACT_ID)


def _contract_code_xdr(wasm_hash: bytes, code: bytes) -> str:
    return stellar_xdr.LedgerEntryData(
        stellar_xdr.LedgerEntryType.CONTRACT_CODE,
        contract_code=stellar_xdr.ContractCodeEntry(
            ext=stellar_xdr.ContractCodeEntryExt(0),
            hash=stellar_xdr.Hash(wasm_hash),
            code=code,
        ),
    ).to_xdr()


def _contract_data_xdr(contract_id: str, val: stellar_xdr.SCVal) -> str:
    return stellar_xdr.LedgerEntryData(
        stellar_xdr.LedgerEntryType.CONTRACT_DATA,
        contract_data=stellar_xdr.ContractDataEntry(
            ext=stellar_xdr.ExtensionPoint(0),
            contract=Address(contract_id).to_xdr_sc_address(),
            key=stellar_xdr.SCVal(
                stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE
            ),
            durability=stellar_xdr.ContractDataDurability.PERSISTENT,
            val=val,
        ),
    ).to_xdr()


def _wasm_instance(wasm_hash: bytes | None) -> stellar_xdr.SCContractInstance:
    return stellar_xdr.SCContractInstance(
        executable=stellar_xdr.ContractExecutable(
            stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
            wasm_hash=stellar_xdr.Hash(wasm_hash) if wasm_hash is not None else None,
        ),
        storage=None,
    )


def _sac_instance() -> stellar_xdr.SCContractInstance:
    return stellar_xdr.SCContractInstance(
        executable=stellar_xdr.ContractExecutable(
            stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET
        ),
        storage=None,
    )
