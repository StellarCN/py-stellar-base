from types import SimpleNamespace
from typing import Any, cast

import pytest

from stellar_sdk import (
    Account,
    Address,
    Keypair,
    Network,
    TransactionBuilder,
    scval,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.contract import (
    AssembledTransaction,
    AssembledTransactionAsync,
)
from stellar_sdk.contract import assembled_transaction as assembled_transaction_module
from stellar_sdk.contract import (
    assembled_transaction_async as assembled_transaction_async_module,
)
from stellar_sdk.contract.exceptions import (
    NeedsMoreSignaturesError,
    NeedsPreparationError,
)
from stellar_sdk.operation import InvokeHostFunction

_MUXED_ACCOUNT_ID = (
    "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
)
_CLAIMABLE_BALANCE_ID = "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"


def _sample_invocation(
    contract_id: str = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK",
) -> stellar_xdr.SorobanAuthorizedInvocation:
    return stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(b"increment"),
                args=[],
            ),
        ),
        sub_invocations=[],
    )


def _sample_auth_entry(address: str) -> stellar_xdr.SorobanAuthorizationEntry:
    return stellar_xdr.SorobanAuthorizationEntry(
        credentials=stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(address).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        ),
        root_invocation=_sample_invocation(),
    )


class _FakeSorobanServer:
    def __init__(self, restore_preambles: list[Any] | None = None) -> None:
        self.simulated_transactions: list[Any] = []
        self.restore_preambles = restore_preambles or []

    def get_latest_ledger(self) -> SimpleNamespace:
        return SimpleNamespace(sequence=100)

    def simulate_transaction(self, transaction) -> SimpleNamespace:
        self.simulated_transactions.append(transaction)
        restore_preamble = (
            self.restore_preambles.pop(0) if self.restore_preambles else None
        )
        return SimpleNamespace(
            error=None, restore_preamble=restore_preamble, latest_ledger=101
        )


class _FakeSorobanServerAsync:
    def __init__(self, restore_preambles: list[Any] | None = None) -> None:
        self.simulated_transactions: list[Any] = []
        self.restore_preambles = restore_preambles or []

    async def get_latest_ledger(self) -> SimpleNamespace:
        return SimpleNamespace(sequence=100)

    async def simulate_transaction(self, transaction) -> SimpleNamespace:
        self.simulated_transactions.append(transaction)
        restore_preamble = (
            self.restore_preambles.pop(0) if self.restore_preambles else None
        )
        return SimpleNamespace(
            error=None, restore_preamble=restore_preamble, latest_ledger=101
        )


def _assembled_with_auth(address: str, server=None):
    source = Keypair.random()
    server = cast(Any, server or _FakeSorobanServer())
    builder = (
        TransactionBuilder(
            Account(source.public_key, 1),
            Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        .set_timeout(300)
        .append_invoke_contract_function_op(
            contract_id="CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK",
            function_name="increment",
            parameters=[],
            auth=[_sample_auth_entry(address)],
        )
    )
    assembled: AssembledTransaction[Any] = AssembledTransaction(builder, server, source)
    assembled.built_transaction = builder.build()
    cast(Any, assembled).simulation = SimpleNamespace(
        latest_ledger=100, restore_preamble=None
    )
    return assembled, source, server


def _assembled_async_with_auth(address: str, server=None):
    source = Keypair.random()
    server = cast(Any, server or _FakeSorobanServerAsync())
    builder = (
        TransactionBuilder(
            Account(source.public_key, 1),
            Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        .set_timeout(300)
        .append_invoke_contract_function_op(
            contract_id="CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK",
            function_name="increment",
            parameters=[],
            auth=[_sample_auth_entry(address)],
        )
    )
    assembled: AssembledTransactionAsync[Any] = AssembledTransactionAsync(
        builder, server, source
    )
    assembled.built_transaction = builder.build()
    cast(Any, assembled).simulation = SimpleNamespace(
        latest_ledger=100, restore_preamble=None
    )
    return assembled, source, server


def test_authorize_contract_address_requires_preparation():
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    assembled, _, _ = _assembled_with_auth(contract_id)
    seen_preimages: list[stellar_xdr.HashIDPreimage] = []

    assembled.authorize(
        address=contract_id,
        signer=lambda preimage: seen_preimages.append(preimage)
        or scval.to_bytes(b"sig"),
        valid_for_ledger_count=20,
    )

    assert assembled._needs_preparation is True
    assert len(seen_preimages) == 1
    assert seen_preimages[0].soroban_authorization is not None
    assert (
        seen_preimages[0].soroban_authorization.signature_expiration_ledger.uint32
        == 120
    )
    with pytest.raises(NeedsPreparationError, match="Authorization entries"):
        assembled.sign(force=True)
    with pytest.raises(NeedsPreparationError, match="Authorization entries"):
        assembled.to_xdr()


def test_sign_auth_entries_rejects_non_account_contract_address():
    assembled, _, _ = _assembled_with_auth(Keypair.random().public_key)

    with pytest.raises(ValueError, match=r"classic account .* contract"):
        assembled.sign_auth_entries(
            Keypair.random(),
            _MUXED_ACCOUNT_ID,
            654656,
        )


@pytest.mark.asyncio
async def test_async_sign_auth_entries_rejects_non_account_contract_address():
    assembled, _, _ = _assembled_async_with_auth(Keypair.random().public_key)

    with pytest.raises(ValueError, match=r"classic account .* contract"):
        await assembled.sign_auth_entries(
            Keypair.random(),
            Address(_CLAIMABLE_BALANCE_ID),
            654656,
        )


def test_sign_requires_unsigned_contract_account_auth_entry():
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    assembled, _, _ = _assembled_with_auth(contract_id)

    with pytest.raises(NeedsMoreSignaturesError, match=contract_id):
        assembled.sign(transaction_signer=Keypair.random(), force=True)


def test_async_sign_requires_unsigned_contract_account_auth_entry():
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    assembled, _, _ = _assembled_async_with_auth(contract_id)

    with pytest.raises(NeedsMoreSignaturesError, match=contract_id):
        assembled.sign(transaction_signer=Keypair.random(), force=True)


def test_sign_and_submit_auto_prepares_contract_address_auth(monkeypatch):
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    server = _FakeSorobanServer()
    assembled, _, _ = _assembled_with_auth(contract_id, server)

    assembled.authorize(
        address=contract_id,
        signer=lambda _: scval.to_bytes(b"sig"),
        valid_until_ledger_sequence=120,
    )

    def fake_assemble(transaction, simulation):
        return transaction

    monkeypatch.setattr(
        assembled_transaction_module, "_assemble_transaction", fake_assemble
    )
    monkeypatch.setattr(AssembledTransaction, "submit", lambda self: scval.to_void())

    assert assembled.sign_and_submit(force=True) == scval.to_void()
    assert len(server.simulated_transactions) == 1
    op = server.simulated_transactions[0].transaction.operations[0]
    assert op.auth[0].credentials.address is not None
    assert (
        op.auth[0].credentials.address.signature.type != stellar_xdr.SCValType.SCV_VOID
    )
    assert assembled._needs_preparation is False


def test_keypair_account_auth_does_not_prepare_again(monkeypatch):
    auth_signer = Keypair.random()
    server = _FakeSorobanServer()
    assembled, _, _ = _assembled_with_auth(auth_signer.public_key, server)

    assembled.sign_auth_entries(auth_signer, valid_until_ledger_sequence=120)

    monkeypatch.setattr(AssembledTransaction, "submit", lambda self: scval.to_void())

    assert assembled._needs_preparation is False
    assert assembled.sign_and_submit(force=True) == scval.to_void()
    assert server.simulated_transactions == []


def test_prepare_restores_footprint_after_contract_address_auth(monkeypatch):
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    restore_preamble = object()
    server = _FakeSorobanServer([restore_preamble])
    assembled, _, _ = _assembled_with_auth(contract_id, server)
    restored = []

    assembled.authorize(
        address=contract_id,
        signer=lambda _: scval.to_bytes(b"sig"),
        valid_until_ledger_sequence=120,
    )

    def fake_assemble(transaction, simulation):
        return transaction

    monkeypatch.setattr(
        assembled_transaction_module, "_assemble_transaction", fake_assemble
    )
    monkeypatch.setattr(
        assembled,
        "_is_current_simulation_read_call",
        lambda: False,
    )
    monkeypatch.setattr(
        assembled,
        "restore_footprint",
        lambda preamble: restored.append(preamble),
    )

    assert assembled.prepare() is assembled
    assert restored == [restore_preamble]
    assert len(server.simulated_transactions) == 2
    assert assembled._needs_preparation is False


def test_authorize_rejects_conflicting_expiration_options():
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    assembled, _, _ = _assembled_with_auth(contract_id)

    with pytest.raises(ValueError, match="mutually exclusive"):
        assembled.authorize(
            address=contract_id,
            signer=lambda _: scval.to_bytes(b"sig"),
            valid_until_ledger_sequence=120,
            valid_for_ledger_count=20,
        )


def test_authorize_accepts_keypair_as_first_argument():
    auth_signer = Keypair.random()
    assembled, _, _ = _assembled_with_auth(auth_signer.public_key)

    assembled.authorize(auth_signer, valid_until_ledger_sequence=120)

    assert assembled.built_transaction is not None
    op = assembled.built_transaction.transaction.operations[0]
    assert isinstance(op, InvokeHostFunction)
    assert op.auth[0].credentials.address is not None
    assert (
        op.auth[0].credentials.address.signature.type != stellar_xdr.SCValType.SCV_VOID
    )
    assert assembled._needs_preparation is False


@pytest.mark.asyncio
async def test_async_sign_and_submit_auto_prepares_contract_address_auth(monkeypatch):
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    server = _FakeSorobanServerAsync()
    assembled, _, _ = _assembled_async_with_auth(contract_id, server)

    await assembled.authorize(
        address=contract_id,
        signer=lambda _: scval.to_bytes(b"sig"),
        valid_until_ledger_sequence=120,
    )

    def fake_assemble(transaction, simulation):
        return transaction

    async def fake_submit(self):
        return scval.to_void()

    monkeypatch.setattr(
        assembled_transaction_async_module,
        "_assemble_transaction",
        fake_assemble,
    )
    monkeypatch.setattr(AssembledTransactionAsync, "submit", fake_submit)

    assert await assembled.sign_and_submit(force=True) == scval.to_void()
    assert len(server.simulated_transactions) == 1
    assert assembled._needs_preparation is False


@pytest.mark.asyncio
async def test_async_prepare_restores_footprint_after_contract_address_auth(
    monkeypatch,
):
    contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
    restore_preamble = object()
    server = _FakeSorobanServerAsync([restore_preamble])
    assembled, _, _ = _assembled_async_with_auth(contract_id, server)
    restored = []

    await assembled.authorize(
        address=contract_id,
        signer=lambda _: scval.to_bytes(b"sig"),
        valid_until_ledger_sequence=120,
    )

    def fake_assemble(transaction, simulation):
        return transaction

    async def fake_restore_footprint(preamble):
        restored.append(preamble)

    monkeypatch.setattr(
        assembled_transaction_async_module,
        "_assemble_transaction",
        fake_assemble,
    )
    monkeypatch.setattr(
        assembled,
        "_is_current_simulation_read_call",
        lambda: False,
    )
    monkeypatch.setattr(assembled, "restore_footprint", fake_restore_footprint)

    assert await assembled.prepare() is assembled
    assert restored == [restore_preamble]
    assert len(server.simulated_transactions) == 2
    assert assembled._needs_preparation is False
