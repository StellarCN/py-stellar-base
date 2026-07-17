import pytest

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
