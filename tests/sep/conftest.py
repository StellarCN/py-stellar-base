from collections.abc import AsyncGenerator

import pytest

from stellar_sdk.client.aiohttp_client import AiohttpClient

FROZEN_TIME = 1_700_000_000


class _FrozenTime:
    """Stand-in for the ``time`` module exposing a constant ``time()``."""

    def __init__(self, now: float) -> None:
        self._now = now

    def time(self) -> float:
        return self._now


class _FixedEntropy:
    """Stand-in for the ``os`` module exposing a deterministic ``urandom()``."""

    @staticmethod
    def urandom(n: int) -> bytes:
        return bytes(i % 256 for i in range(n))


@pytest.fixture
def frozen_web_auth(monkeypatch: pytest.MonkeyPatch) -> int:
    """Freeze time and nonce entropy inside the SEP-10/SEP-45 modules.

    Only the module-level ``time``/``os`` bindings of the web-authentication
    modules are patched — the global modules stay untouched. Challenge
    building and verification then share one frozen clock, so tests can
    assert exact time bounds and nonces.
    """
    import stellar_sdk.sep.stellar_soroban_web_authentication as sep45
    import stellar_sdk.sep.stellar_web_authentication as sep10

    monkeypatch.setattr(sep10, "time", _FrozenTime(FROZEN_TIME))
    monkeypatch.setattr(sep10, "os", _FixedEntropy())
    monkeypatch.setattr(sep45, "os", _FixedEntropy())
    return FROZEN_TIME


@pytest.fixture
async def close_internal_aiohttp_clients(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[None, None]:
    """Close the ``AiohttpClient`` instances the SDK creates when ``client=None``.

    ``federation``/``stellar_toml`` build an ``AiohttpClient`` internally and
    never close it, leaking the underlying aiohttp session ("Unclosed client
    session" warnings). Patching the modules' ``AiohttpClient`` binding to a
    tracking factory keeps the default-client code path covered while still
    closing every session at teardown.
    """
    import stellar_sdk.sep.federation as federation
    import stellar_sdk.sep.stellar_toml as stellar_toml

    created: list[AiohttpClient] = []

    def _tracking_factory() -> AiohttpClient:
        client = AiohttpClient()
        created.append(client)
        return client

    monkeypatch.setattr(federation, "AiohttpClient", _tracking_factory)
    monkeypatch.setattr(stellar_toml, "AiohttpClient", _tracking_factory)
    yield
    for client in created:
        await client.close()
