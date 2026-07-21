import pytest

from stellar_sdk import Address, Network
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.sep.stellar_soroban_web_authentication import (
    read_challenge_authorization_entries,
)
from tests.sep.soroban_web_authentication.helpers import (
    CLIENT_CONTRACT_ACCOUNT,
    CLIENT_DOMAIN,
    CLIENT_DOMAIN_ACCOUNT,
    HOME_DOMAIN,
    NETWORK_PASSPHRASE,
    SERVER_ACCOUNT,
    SERVER_SECRET,
    WEB_AUTH_CONTRACT,
    WEB_AUTH_DOMAIN,
    _build_entries,
    build_args,
    build_root_invocation,
)


async def test_build_challenge_authorization_entries(soroban_server, rpc_mock):
    mock_data = {
        "jsonrpc": "2.0",
        "id": "53c6af73bcb24cbab1120229a99612de",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAchrQAAAEgAAAA4AAAAAAAB619",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABANkhXTlJkSzVlSXZpTDlCajhDS2IxSzludXRvaklPdGpKYUpyTmVCYkNyNHpmbEt5YVVSNkN1Vi9LeExheWcyNgAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQ==",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "503165",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5zA2vAnNXt3SAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQDZIV05SZEs1ZUl2aUw5Qmo4Q0tiMUs5bnV0b2pJT3RqSmFKck5lQmJDcjR6ZmxLeWFVUjZDdVYvS3hMYXlnMjYAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51a8Dqi/xldiQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTM3nBT/87UYoQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEA2SFdOUmRLNWVJdmlMOUJqOENLYjFLOW51dG9qSU90akphSnJOZUJiQ3I0emZsS3lhVVI2Q3VWL0t4TGF5ZzI2AAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldRAAAAAA==",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVN5wU//O1GKEAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABU3nBT/87UYoQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVWvA6ov8ZXYkAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVa8Dqi/xldiQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABUwNrwJzV7d0gAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFTA2vAnNXt3SAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82106,
        },
    }

    rpc_mock.expect_response(mock_data)
    challenge_authorization_entries = await _build_entries(
        soroban_server=soroban_server,
        web_auth_contract=WEB_AUTH_CONTRACT,
        server_secret=SERVER_SECRET,
        client_account_id=CLIENT_CONTRACT_ACCOUNT,
        home_domain=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        client_domain=CLIENT_DOMAIN,
        client_domain_account=CLIENT_DOMAIN_ACCOUNT,
    )
    parsed = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_authorization_entries,
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )
    assert parsed.server_account_id == SERVER_ACCOUNT
    assert parsed.client_account_id == CLIENT_CONTRACT_ACCOUNT
    assert parsed.web_auth_contract == WEB_AUTH_CONTRACT
    assert parsed.matched_home_domain == HOME_DOMAIN
    assert parsed.web_auth_domain == WEB_AUTH_DOMAIN
    assert parsed.client_domain == CLIENT_DOMAIN
    assert parsed.client_domain_account == CLIENT_DOMAIN_ACCOUNT


async def test_build_challenge_authorization_entries_without_client_domain(
    soroban_server, rpc_mock
):
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f53108eae14c4279bbcc70a35dbaf935",
        "result": {
            "transactionData": "AAAAAAAAAAUAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABQAAAABAAAABgAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAABQAAAABAAAAByPTTS0KMcIYyML+YoUrcuG3q/jycm6359M+5okxqJVpAAAAB5p4YLtYmQSjnl08+eGabtklZz1wWphX7PKPXmxGR6x2AAAAAgAAAAYAAAAAAAAAAKTYiozxBkVKQYNQ5/vOahmvFqLD9mPgw+NjsauF9vudAAAAFS97Xent/lbsAAAAAAAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAVVVn5OpqSJQ0AAAAAABJbHwAAAJAAAACUAAAAAAAFPG4=",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAUAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAEBaRjhHTDNPbWQxd2ErQittMHRoTlJmQ0F5UHJ3N24vWkRBdVMzMTVUc1V5dWhNMkNHNXNTOTFPOW5pYWhNMm5YAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "343150",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG51VZ+TqakiUNAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAFAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAABAWkY4R0wzT21kMXdhK0IrbTB0aE5SZkNBeVBydzduL1pEQXVTMzE1VHNVeXVoTTJDRzVzUzkxTzluaWFoTTJuWAAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50ve13p7f5W7AAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABQAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAAQFpGOEdMM09tZDF3YStCK20wdGhOUmZDQXlQcnc3bi9aREF1UzMxNVRzVXl1aE0yQ0c1c1M5MU85bmlhaE0yblgAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVL3td6e3+VuwAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABUve13p7f5W7AAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABVVWfk6mpIlDQAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFVVZ+TqakiUNAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82338,
        },
    }

    rpc_mock.expect_response(mock_data)
    challenge_authorization_entries = await _build_entries(
        soroban_server=soroban_server,
        web_auth_contract=WEB_AUTH_CONTRACT,
        server_secret=SERVER_SECRET,
        client_account_id=CLIENT_CONTRACT_ACCOUNT,
        home_domain=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    )
    parsed = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_authorization_entries,
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )
    assert parsed.client_domain is None
    assert parsed.client_domain_account is None


async def test_build_challenge_authorization_entries_with_custom_nonce(
    soroban_server, rpc_mock
):
    """Test building challenge authorization entries without client domain."""

    mock_data = {
        "jsonrpc": "2.0",
        "id": "f05db92980a84271b4c354858ff2e48a",
        "result": {
            "transactionData": "AAAAAAAAAAYAAAAAAAAAAAsFgywxsz4qQ0GCRAuou6p/ImgqqQ7mY7P2yFlmqm0zAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAAAYAAAABaCSw4cnhsl4aWyRa5pYTz/CKYsGdDy0Idp1Kqpu4xucAAAAUAAAAAQAAAAYAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAUAAAAAQAAAAcj000tCjHCGMjC/mKFK3Lht6v48nJut+fTPuaJMaiVaQAAAAeaeGC7WJkEo55dPPnhmm7ZJWc9cFqYV+zyj15sRkesdgAAAAMAAAAGAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAAGAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAAGAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAcUkgAAAEgAAAA4AAAAAAAB58w",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAAPAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAARAAAAAQAAAAcAAAAPAAAAB2FjY291bnQAAAAADgAAADhDQlVDSk1IQlpIUTNFWFEyTE1TRlZaVVdDUEg3QkNUQ1lHT1E2TElJTzJPVVZLVTNYRERPTzJITgAAAA8AAAANY2xpZW50X2RvbWFpbgAAAAAAAA4AAAASY2xpZW50LmV4YW1wbGUuY29tAAAAAAAPAAAAFWNsaWVudF9kb21haW5fYWNjb3VudAAAAAAAAA4AAAA4R0FGUUxBWk1HR1pUNEtTRElHQkVJQzVJWE9WSDZJVElGS1VRNVpURFdQM01RV0xHVkpXVEgzVFgAAAAPAAAAC2hvbWVfZG9tYWluAAAAAA4AAAALZXhhbXBsZS5jb20AAAAADwAAAAVub25jZQAAAAAAAA4AAAAMcmFuZG9tLW5vbmNlAAAADwAAAA93ZWJfYXV0aF9kb21haW4AAAAADgAAABBhdXRoLmV4YW1wbGUuY29tAAAADwAAABd3ZWJfYXV0aF9kb21haW5fYWNjb3VudAAAAAAOAAAAOEdDU05SQ1VNNkVERUtTU0JRTklPUDY2T05JTTI2RlZDWVAzR0hZR0Q0TlIzREs0RjYzNVozMldR",
                "AAAAAQAAAAAAAAABpZYrQtB/Sr9w4mNly2nH8h5ic4ytC5rQrLXLbe/N3UMAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAPd2ViX2F1dGhfdmVyaWZ5AAAAAAE=",
            ],
            "minResourceFee": "499504",
            "results": [
                {
                    "auth": [
                        "AAAAAQAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG53QGGU1aROPYAAAAAAAAAAEAAAAAAAAAAaWWK0LQf0q/cOJjZctpx/IeYnOMrQua0Ky1y23vzd1DAAAAD3dlYl9hdXRoX3ZlcmlmeQAAAAABAAAAEQAAAAEAAAAHAAAADwAAAAdhY2NvdW50AAAAAA4AAAA4Q0JVQ0pNSEJaSFEzRVhRMkxNU0ZWWlVXQ1BIN0JDVENZR09RNkxJSU8yT1VWS1UzWERET08ySE4AAAAPAAAADWNsaWVudF9kb21haW4AAAAAAAAOAAAAEmNsaWVudC5leGFtcGxlLmNvbQAAAAAADwAAABVjbGllbnRfZG9tYWluX2FjY291bnQAAAAAAAAOAAAAOEdBRlFMQVpNR0daVDRLU0RJR0JFSUM1SVhPVkg2SVRJRktVUTVaVERXUDNNUVdMR1ZKV1RIM1RYAAAADwAAAAtob21lX2RvbWFpbgAAAAAOAAAAC2V4YW1wbGUuY29tAAAAAA8AAAAFbm9uY2UAAAAAAAAOAAAADHJhbmRvbS1ub25jZQAAAA8AAAAPd2ViX2F1dGhfZG9tYWluAAAAAA4AAAAQYXV0aC5leGFtcGxlLmNvbQAAAA8AAAAXd2ViX2F1dGhfZG9tYWluX2FjY291bnQAAAAADgAAADhHQ1NOUkNVTTZFREVLU1NCUU5JT1A2Nk9OSU0yNkZWQ1lQM0dIWUdENE5SM0RLNEY2MzVaMzJXUQAAAAA=",
                        "AAAAAQAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+51Jb8lh07WXnQAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                        "AAAAAQAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTN8DiMs4x5wIwAAAAAAAAABAAAAAAAAAAGllitC0H9Kv3DiY2XLacfyHmJzjK0LmtCstctt783dQwAAAA93ZWJfYXV0aF92ZXJpZnkAAAAAAQAAABEAAAABAAAABwAAAA8AAAAHYWNjb3VudAAAAAAOAAAAOENCVUNKTUhCWkhRM0VYUTJMTVNGVlpVV0NQSDdCQ1RDWUdPUTZMSUlPMk9VVktVM1hERE9PMkhOAAAADwAAAA1jbGllbnRfZG9tYWluAAAAAAAADgAAABJjbGllbnQuZXhhbXBsZS5jb20AAAAAAA8AAAAVY2xpZW50X2RvbWFpbl9hY2NvdW50AAAAAAAADgAAADhHQUZRTEFaTUdHWlQ0S1NESUdCRUlDNUlYT1ZINklUSUZLVVE1WlREV1AzTVFXTEdWSldUSDNUWAAAAA8AAAALaG9tZV9kb21haW4AAAAADgAAAAtleGFtcGxlLmNvbQAAAAAPAAAABW5vbmNlAAAAAAAADgAAAAxyYW5kb20tbm9uY2UAAAAPAAAAD3dlYl9hdXRoX2RvbWFpbgAAAAAOAAAAEGF1dGguZXhhbXBsZS5jb20AAAAPAAAAF3dlYl9hdXRoX2RvbWFpbl9hY2NvdW50AAAAAA4AAAA4R0NTTlJDVU02RURFS1NTQlFOSU9QNjZPTklNMjZGVkNZUDNHSFlHRDROUjNESzRGNjM1WjMyV1EAAAAA",
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAACwWDLDGzPipDQYJEC6i7qn8iaCqpDuZjs/bIWWaqbTMAAAAVfA4jLOMecCMAAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAAALBYMsMbM+KkNBgkQLqLuqfyJoKqkO5mOz9shZZqptMwAAABV8DiMs4x5wIwAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAAAAAAApNiKjPEGRUpBg1Dn+85qGa8WosP2Y+DD42Oxq4X2+50AAAAVSW/JYdO1l50AAAAA",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAAAAAACk2IqM8QZFSkGDUOf7zmoZrxaiw/Zj4MPjY7Grhfb7nQAAABVJb8lh07WXnQAAAAAAAAABAAAAAA==",
                },
                {
                    "type": "created",
                    "key": "AAAABgAAAAFoJLDhyeGyXhpbJFrmlhPP8IpiwZ0PLQh2nUqqm7jG5wAAABV0BhlNWkTj2AAAAAA=",
                    "before": None,
                    "after": "AAAAAAAAAAYAAAAAAAAAAWgksOHJ4bJeGlskWuaWE8/wimLBnQ8tCHadSqqbuMbnAAAAFXQGGU1aROPYAAAAAAAAAAEAAAAA",
                },
            ],
            "latestLedger": 82359,
        },
    }

    nonce = "random-nonce"
    rpc_mock.expect_response(mock_data)
    challenge_authorization_entries = await _build_entries(
        soroban_server=soroban_server,
        web_auth_contract=WEB_AUTH_CONTRACT,
        server_secret=SERVER_SECRET,
        client_account_id=CLIENT_CONTRACT_ACCOUNT,
        home_domain=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        client_domain=CLIENT_DOMAIN,
        client_domain_account=CLIENT_DOMAIN_ACCOUNT,
        nonce=nonce,
    )
    parsed = read_challenge_authorization_entries(
        challenge_authorization_entries=challenge_authorization_entries,
        server_account_id=SERVER_ACCOUNT,
        home_domains=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        web_auth_contract=WEB_AUTH_CONTRACT,
    )
    assert parsed.nonce == nonce


async def test_build_challenge_authorization_entries_client_domain_without_account(
    soroban_server, rpc_mock
):
    """Test that build_challenge_authorization_entries raises error when client_domain is provided without client_domain_account."""
    with pytest.raises(
        ValueError,
        match=r"client_domain and client_domain_account must both be provided or both be None.",
    ):
        await _build_entries(
            soroban_server=soroban_server,
            web_auth_contract=WEB_AUTH_CONTRACT,
            server_secret=SERVER_SECRET,
            client_account_id=CLIENT_CONTRACT_ACCOUNT,
            home_domain=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            network_passphrase=NETWORK_PASSPHRASE,
            client_domain=CLIENT_DOMAIN,
            client_domain_account=None,
        )


async def test_build_challenge_authorization_entries_client_domain_account_without_domain(
    soroban_server, rpc_mock
):
    """Test that build_challenge_authorization_entries raises error when client_domain_account is provided without client_domain."""
    with pytest.raises(
        ValueError,
        match=r"client_domain and client_domain_account must both be provided or both be None.",
    ):
        await _build_entries(
            soroban_server=soroban_server,
            web_auth_contract=WEB_AUTH_CONTRACT,
            server_secret=SERVER_SECRET,
            client_account_id=CLIENT_CONTRACT_ACCOUNT,
            home_domain=HOME_DOMAIN,
            web_auth_domain=WEB_AUTH_DOMAIN,
            network_passphrase=NETWORK_PASSPHRASE,
            client_domain=None,
            client_domain_account=CLIENT_DOMAIN_ACCOUNT,
        )


async def test_build_challenge_signs_v2_entries(soroban_server, rpc_mock):
    """build_challenge signs server entries that use ADDRESS_V2 credentials."""

    def unsigned_v2_entry(address: str) -> stellar_xdr.SorobanAuthorizationEntry:
        return stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
                address_v2=stellar_xdr.SorobanAddressCredentials(
                    address=Address(address).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(1),
                    signature_expiration_ledger=stellar_xdr.Uint32(0),
                    signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
                ),
            ),
            root_invocation=build_root_invocation(
                args=build_args(client_domain=None, client_domain_account=None)
            ),
        )

    mock_data = {
        "jsonrpc": "2.0",
        "id": "e1f7a93268e44a0ba2b6e0c6a3155e60",
        "result": {
            "results": [
                {
                    "auth": [
                        unsigned_v2_entry(CLIENT_CONTRACT_ACCOUNT).to_xdr(),
                        unsigned_v2_entry(SERVER_ACCOUNT).to_xdr(),
                    ],
                    "xdr": "AAAAAQ==",
                }
            ],
            "latestLedger": 82106,
        },
    }

    rpc_mock.expect_response(mock_data)
    challenge = await _build_entries(
        soroban_server=soroban_server,
        web_auth_contract=WEB_AUTH_CONTRACT,
        server_secret=SERVER_SECRET,
        client_account_id=CLIENT_CONTRACT_ACCOUNT,
        home_domain=HOME_DOMAIN,
        web_auth_domain=WEB_AUTH_DOMAIN,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    )

    entries = stellar_xdr.SorobanAuthorizationEntries.from_xdr(
        challenge
    ).soroban_authorization_entries
    assert len(entries) == 2
    client_entry, server_entry = entries
    assert client_entry.credentials.address_v2 is not None
    assert (
        client_entry.credentials.address_v2.signature.type
        == stellar_xdr.SCValType.SCV_VOID
    )
    assert server_entry.credentials.address_v2 is not None
    assert (
        server_entry.credentials.address_v2.signature.type
        == stellar_xdr.SCValType.SCV_VEC
    )
    assert server_entry.credentials.address_v2.signature_expiration_ledger == (
        stellar_xdr.Uint32(82106 + 180)
    )
