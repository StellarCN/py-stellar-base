from __future__ import annotations

from types import MethodType, SimpleNamespace
from typing import Any, ClassVar, Generic, TypeVar

import pytest

from stellar_sdk import Network, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.contract import contract_client, contract_client_async
from stellar_sdk.contract.contract_client import ContractClient
from stellar_sdk.contract.contract_client_async import ContractClientAsync
from stellar_sdk.operation import InvokeHostFunction
from stellar_sdk.soroban_server import SorobanServer
from stellar_sdk.soroban_server_async import SorobanServerAsync
from tests.helpers import deterministic_keypair

OWNER = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
CONTRACT_ID = "CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABSC4"
SOURCE_KP = deterministic_keypair("external-ref-source")
SALT = b"\x07" * 32

T = TypeVar("T")


class _FakeAssembledTransaction(Generic[T]):
    """Stands in for AssembledTransaction so no RPC round trip is needed.

    Everything the client hands the constructor is captured, and
    ``sign_and_submit`` runs the client's own ``parse_result_xdr_fn`` over a real
    result :class:`SCVal`, so the returned contract ID exercises that wiring
    instead of being echoed back from here.
    """

    captured: ClassVar[dict[str, Any]] = {}

    def __init__(self, builder, soroban_server, signer, parse_result_xdr_fn, timeout):
        captured = type(self).captured
        captured["builder"] = builder
        captured["server"] = soroban_server
        captured["signer"] = signer
        captured["parse_result_xdr_fn"] = parse_result_xdr_fn
        captured["submit_timeout"] = timeout

    def _submit(self, force: bool):
        captured = type(self).captured
        captured["force"] = force
        return captured["parse_result_xdr_fn"](scval.to_address(CONTRACT_ID))

    def simulate(self, restore: bool = True):
        type(self).captured["restore"] = restore
        return self

    def sign_and_submit(self, force: bool = False):
        return self._submit(force)


class _FakeAssembledTransactionAsync(_FakeAssembledTransaction[T]):
    async def simulate(self, restore: bool = True):  # type: ignore[override]
        type(self).captured["restore"] = restore
        return self

    async def sign_and_submit(self, force: bool = False):  # type: ignore[override]
        return self._submit(force)


def _external_ref_of(
    captured: dict[str, Any],
) -> stellar_xdr.ContractExecutableExternalRef:
    envelope = captured["builder"].build()
    op = envelope.transaction.operations[0]
    assert isinstance(op, InvokeHostFunction)
    create_contract = op.host_function.create_contract_v2
    assert create_contract is not None
    assert (
        create_contract.executable.type
        == stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_EXTERNAL_REF
    )
    external_ref = create_contract.executable.external_ref
    assert external_ref is not None
    return external_ref


def test_create_contract_from_external_ref(monkeypatch):
    captured: dict[str, Any] = {}
    monkeypatch.setattr(_FakeAssembledTransaction, "captured", captured)
    monkeypatch.setattr(
        contract_client, "AssembledTransaction", _FakeAssembledTransaction
    )
    server = SorobanServer("https://example.com")
    monkeypatch.setattr(
        server,
        "get_network",
        MethodType(
            lambda self: SimpleNamespace(passphrase=Network.TESTNET_NETWORK_PASSPHRASE),
            server,
        ),
    )

    contract_id = ContractClient.create_contract_from_external_ref(
        OWNER,
        "v1",
        SOURCE_KP.public_key,
        SOURCE_KP,
        server,
        salt=SALT,
        submit_timeout=77,
        restore=False,
    )

    # The ID came back through the client's own result parser, not from the fake.
    assert contract_id == CONTRACT_ID
    assert captured["server"] is server
    assert captured["signer"] is SOURCE_KP
    assert captured["submit_timeout"] == 77
    assert captured["restore"] is False
    assert captured["force"] is True
    external_ref = _external_ref_of(captured)
    assert external_ref.executable_owner == Address(OWNER).to_xdr_sc_address()
    assert external_ref.tag.sc_string == b"v1"


async def test_create_contract_from_external_ref_async(monkeypatch):
    captured: dict[str, Any] = {}
    monkeypatch.setattr(_FakeAssembledTransactionAsync, "captured", captured)
    monkeypatch.setattr(
        contract_client_async,
        "AssembledTransactionAsync",
        _FakeAssembledTransactionAsync,
    )
    server = SorobanServerAsync("https://example.com")

    async def get_network(self):
        return SimpleNamespace(passphrase=Network.TESTNET_NETWORK_PASSPHRASE)

    monkeypatch.setattr(server, "get_network", MethodType(get_network, server))

    contract_id = await ContractClientAsync.create_contract_from_external_ref(
        OWNER,
        b"\xff\xfe",
        SOURCE_KP.public_key,
        SOURCE_KP,
        server,
        salt=SALT,
        submit_timeout=77,
        restore=False,
    )

    # The ID came back through the client's own result parser, not from the fake.
    assert contract_id == CONTRACT_ID
    assert captured["server"] is server
    assert captured["signer"] is SOURCE_KP
    assert captured["submit_timeout"] == 77
    assert captured["restore"] is False
    assert captured["force"] is True
    external_ref = _external_ref_of(captured)
    assert external_ref.executable_owner == Address(OWNER).to_xdr_sc_address()
    assert external_ref.tag.sc_string == b"\xff\xfe"


def test_create_contract_from_external_ref_rejects_non_contract_owner(monkeypatch):
    monkeypatch.setattr(
        contract_client, "AssembledTransaction", _FakeAssembledTransaction
    )
    server = SorobanServer("https://example.com")

    with pytest.raises(ValueError, match="must be a contract address"):
        ContractClient.create_contract_from_external_ref(
            SOURCE_KP.public_key,
            "v1",
            SOURCE_KP.public_key,
            SOURCE_KP,
            server,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        )
