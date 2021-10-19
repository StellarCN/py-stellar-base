import pytest

from stellar_sdk.client.aiohttp_client import AiohttpClient
from stellar_sdk.sep.exceptions import StellarTomlNotFoundError
from stellar_sdk.sep.stellar_toml import fetch_stellar_toml, fetch_stellar_toml_async


@pytest.mark.slow
class TestStellarToml:
    def test_get_success_sync(self):
        toml = fetch_stellar_toml("overcat.me", None)
        assert toml.get("FEDERATION_SERVER") == "https://federation.overcat.workers.dev"

    @pytest.mark.asyncio
    async def test_get_success_async(self):
        client = AiohttpClient()
        toml = await fetch_stellar_toml_async("overcat.me", client)
        assert toml.get("FEDERATION_SERVER") == "https://federation.overcat.workers.dev"

    def test_get_success_http(self):
        toml = fetch_stellar_toml("overcat.me", None, True)
        assert toml.get("FEDERATION_SERVER") == "https://federation.overcat.workers.dev"

    def test_get_not_found(self):
        with pytest.raises(StellarTomlNotFoundError):
            fetch_stellar_toml("httpbin.overcat.me")
