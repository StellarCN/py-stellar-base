import copy

import pytest
import requests_mock

from stellar_sdk import Account, Keypair, Network, TransactionBuilder, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address
from stellar_sdk.base_soroban_server import ResourceLeeway
from stellar_sdk.exceptions import (
    AccountNotFoundException,
    PrepareTransactionException,
    SorobanRpcErrorResponse,
)
from stellar_sdk.soroban_rpc import *
from stellar_sdk.soroban_server import SorobanServer

PRC_URL = "https://example.com/soroban_rpc"


class TestSorobanServer:
    def test_load_account(self):
        result = {
            "entries": [
                {
                    "key": "AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JA==",
                    "xdr": "AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JAAAABdIcDhpAAADHAAAAAwAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAABfI8AAAAAZMK3qQ==",
                    "lastModifiedLedgerSeq": "97423",
                    "liveUntilLedgerSeq": "97999",
                }
            ],
            "latestLedger": "108023",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "ecb18f82ec12484190673502d0486b98",
            "result": result,
        }
        account_id = "GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54"
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).load_account(account_id) == Account(
                account_id, 3418793967628
            )

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLedgerEntries"
        assert request_data["params"] == {
            "keys": ["AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JA=="]
        }

    def test_load_account_not_found_raise(self):
        result = {"entries": None, "latestLedger": "108023"}
        data = {
            "jsonrpc": "2.0",
            "id": "ecb18f82ec12484190673502d0486b98",
            "result": result,
        }
        account_id = "GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54"
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            with pytest.raises(
                AccountNotFoundException,
                match=f"Account not found, account_id: {account_id}",
            ):
                SorobanServer(PRC_URL).load_account(account_id)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLedgerEntries"
        assert request_data["params"] == {
            "keys": ["AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JA=="]
        }

    def test_get_health(self):
        result = {
            "status": "healthy",
            "latestLedger": 50000,
            "oldestLedger": 1,
            "ledgerRetentionWindow": 10000,
        }
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(
                PRC_URL
            ).get_health() == GetHealthResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getHealth"
        assert request_data["params"] is None

    def test_get_network(self):
        result = {
            "friendbotUrl": "http://localhost:8000/friendbot",
            "passphrase": "Standalone Network ; February 2017",
            "protocolVersion": "20",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }
        Response[GetNetworkResponse].model_validate(data)
        GetNetworkResponse.model_validate(result)

        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(
                PRC_URL
            ).get_network() == GetNetworkResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getNetwork"
        assert request_data["params"] is None

    def test_get_contract_data(self):
        result = {
            "entries": [
                {
                    "key": "AAAABgAAAAFbihjlAiytnchoNOQZzgshTg9sfCxcBnTGO2xwtRu0awAAABQAAAAB",
                    "xdr": "AAAABgAAAAAAAAABW4oY5QIsrZ3IaDTkGc4LIU4PbHwsXAZ0xjtscLUbtGsAAAAUAAAAAQAAABMAAAAAJEKO7o0EZBi/DpFId2xLI1yGppi+ADrnh9IIE/CfJEcAAAAA",
                    "lastModifiedLedgerSeq": "11715",
                    "liveUntilLedgerSeq": "17882",
                }
            ],
            "latestLedger": "12551",
        }

        data = {
            "jsonrpc": "2.0",
            "id": "839c6c921d40456db5ba8a1c4e1a0e70",
            "result": result,
        }
        contract_id = "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY"
        key = stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert (
                SorobanServer(PRC_URL).get_contract_data(contract_id, key)
                == GetLedgerEntriesResponse.model_validate(result).entries[0]
            )

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLedgerEntries"
        assert key == stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE
        )
        assert request_data["params"] == {
            "keys": ["AAAABgAAAAFbihjlAiytnchoNOQZzgshTg9sfCxcBnTGO2xwtRu0awAAABQAAAAB"]
        }

    def test_get_contract_data_not_found(self):
        result = {"entries": None, "latestLedger": "296"}
        data = {
            "jsonrpc": "2.0",
            "id": "839c6c921d40456db5ba8a1c4e1a0e70",
            "result": result,
        }
        contract_id = "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY"
        key = stellar_xdr.SCVal(stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE)
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).get_contract_data(contract_id, key) is None

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLedgerEntries"
        assert key == stellar_xdr.SCVal(
            stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE
        )
        assert request_data["params"] == {
            "keys": ["AAAABgAAAAFbihjlAiytnchoNOQZzgshTg9sfCxcBnTGO2xwtRu0awAAABQAAAAB"]
        }

    def test_get_ledger_entries(self):
        result = {
            "entries": [
                {
                    "key": "AAAAAAAAAACynni6I2ACEzWuORVM1b2y0k1ZDni0W6JlC/Ad/mfCSg==",
                    "xdr": "AAAAAAAAAACynni6I2ACEzWuORVM1b2y0k1ZDni0W6JlC/Ad/mfCSgAAABdIdugAAAAAnwAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAA",
                    "lastModifiedLedgerSeq": "159",
                    "liveUntilLedgerSeq": "288",
                },
                {
                    "key": "AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JA==",
                    "xdr": "AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JAAAABdIcmH6AAAAoQAAAAgAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAAHAkAAAAAZMPQ0g==",
                    "lastModifiedLedgerSeq": "7177",
                    "liveUntilLedgerSeq": "8392",
                },
            ],
            "latestLedger": "7943",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "0ce70038b1804b3c93ca7abc137f3061",
            "result": result,
        }

        account_id0 = "GCZJ46F2ENQAEEZVVY4RKTGVXWZNETKZBZ4LIW5CMUF7AHP6M7BEV464"
        key0 = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.ACCOUNT,
            account=stellar_xdr.LedgerKeyAccount(
                account_id=Keypair.from_public_key(account_id0).xdr_account_id(),
            ),
        )
        account_id1 = "GDAT5HWTGIU4TSSZ4752OUC4SABDLTLZFRPZUJ3D6LKBNEPA7V2CIG54"
        key1 = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.ACCOUNT,
            account=stellar_xdr.LedgerKeyAccount(
                account_id=Keypair.from_public_key(account_id1).xdr_account_id(),
            ),
        )
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).get_ledger_entries(
                [key0, key1]
            ) == GetLedgerEntriesResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLedgerEntries"
        assert request_data["params"] == {
            "keys": [
                "AAAAAAAAAACynni6I2ACEzWuORVM1b2y0k1ZDni0W6JlC/Ad/mfCSg==",
                "AAAAAAAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JA==",
            ]
        }

    def test_get_transaction(self):
        result = {
            "status": "SUCCESS",
            "latestLedger": "79289",
            "latestLedgerCloseTime": "1690387240",
            "oldestLedger": "77850",
            "oldestLedgerCloseTime": "1690379694",
            "applicationOrder": 1,
            "envelopeXdr": "AAAAAgAAAADTYKIzfa0ubKp7qjOcF+ZO8sjQutzo1iHuDh8esi9q+wABNjQAATW1AAAAAQAAAAAAAAAAAAAAAQAAAAAAAAAYAAAAAAAAAAIAAAASAAAAAb3H+V1yFoNDBpje4rchxeaR7/hRNS2CAT2Dh6A8z6xrAAAADwAAAARuYW1lAAAAAAAAAAEAAAAAAAAAAwAAAAYAAAABvcf5XXIWg0MGmN7ityHF5pHv+FE1LYIBPYOHoDzPrGsAAAAPAAAACE1FVEFEQVRBAAAAAQAAAAAAAAAGAAAAAb3H+V1yFoNDBpje4rchxeaR7/hRNS2CAT2Dh6A8z6xrAAAAFAAAAAEAAAAAAAAAB++FkDTZODW0rvolF6AuIZf4w7+GQd8RofaH8u2pM+UPAAAAAAAAAAAAUrutAAAiqAAAAAAAAADIAAAAAAAAACgAAAABsi9q+wAAAEDgHR/5rU+bsXD/oPUFodyEgXFNbDm5T2+M1GarZXy+d+tZ757PBL9ysK41F1hUYz3p5CA7Urlpe3fnNjYcu1EM",
            "resultXdr": "AAAAAAABNCwAAAAAAAAAAQAAAAAAAAAYAAAAAJhEDjNV0Jj46jrxCj87qJ6JaYKJN4c+p5tvapkLwrn8AAAAAA==",
            "resultMetaXdr": "AAAAAwAAAAAAAAACAAAAAwABNbYAAAAAAAAAANNgojN9rS5sqnuqM5wX5k7yyNC63OjWIe4OHx6yL2r7AAAAF0h1s9QAATW1AAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQABNbYAAAAAAAAAANNgojN9rS5sqnuqM5wX5k7yyNC63OjWIe4OHx6yL2r7AAAAF0h1s9QAATW1AAAAAQAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAMAAAAAAAE1tgAAAABkwUMZAAAAAAAAAAEAAAAAAAAAAgAAAAMAATW2AAAAAAAAAADTYKIzfa0ubKp7qjOcF+ZO8sjQutzo1iHuDh8esi9q+wAAABdIdbPUAAE1tQAAAAEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAABNbYAAAAAZMFDGQAAAAAAAAABAAE1tgAAAAAAAAAA02CiM32tLmyqe6oznBfmTvLI0Lrc6NYh7g4fHrIvavsAAAAXSHWz/AABNbUAAAABAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAwAAAAAAATW2AAAAAGTBQxkAAAAAAAAAAQAAAAAAAAAAAAAADgAAAAZUb2tlbkEAAAAAAAIAAAABAAAAAAAAAAAAAAACAAAAAAAAAAMAAAAPAAAAB2ZuX2NhbGwAAAAADQAAACC9x/ldchaDQwaY3uK3IcXmke/4UTUtggE9g4egPM+sawAAAA8AAAAEbmFtZQAAAAEAAAABAAAAAAAAAAG9x/ldchaDQwaY3uK3IcXmke/4UTUtggE9g4egPM+sawAAAAIAAAAAAAAAAgAAAA8AAAAJZm5fcmV0dXJuAAAAAAAADwAAAARuYW1lAAAADgAAAAZUb2tlbkEAAA==",
            "ledger": "79286",
            "createdAt": "1690387225",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }
        tx_hash = "06dd9ee70bf93bbfe219e2b31363ab5a0361cc6285328592e4d3d1fed4c9025c"
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).get_transaction(
                tx_hash
            ) == GetTransactionResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getTransaction"
        assert request_data["params"] == {"hash": tx_hash}

    def test_get_events(self):
        result = {
            "events": [
                {
                    "type": "contract",
                    "ledger": "12739",
                    "ledgerClosedAt": "2023-09-16T06:23:57Z",
                    "contractId": "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY",
                    "id": "0000054713588387840-0000000000",
                    "pagingToken": "0000054713588387840-0000000000",
                    "topic": [
                        "AAAADwAAAAdDT1VOVEVSAA==",
                        "AAAADwAAAAlpbmNyZW1lbnQAAAA=",
                    ],
                    "value": "AAAAAwAAAAE=",
                    "inSuccessfulContractCall": True,
                    "txHash": "db86e94aa98b7d38213c041ebbb727fbaabf0b7c435de594f36c2d51fc61926d",
                },
                {
                    "type": "contract",
                    "ledger": "12747",
                    "ledgerClosedAt": "2023-09-16T06:24:05Z",
                    "contractId": "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY",
                    "id": "0000054747948126208-0000000000",
                    "pagingToken": "0000054747948126208-0000000000",
                    "topic": [
                        "AAAADwAAAAdDT1VOVEVSAA==",
                        "AAAADwAAAAlpbmNyZW1lbnQAAAA=",
                    ],
                    "value": "AAAAAwAAAAI=",
                    "inSuccessfulContractCall": True,
                    "txHash": "db86e94aa98b7d38213c041ebbb727fbaabf0b7c435de594f36c2d51fc61926d",
                },
            ],
            "latestLedger": "187",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }

        start_ledger = 100
        filters = [
            EventFilter(
                event_type=EventFilterType.CONTRACT,
                contract_ids=[
                    "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY"
                ],
                topics=[
                    ["AAAADwAAAAdDT1VOVEVSAA==", "AAAADwAAAAlpbmNyZW1lbnQAAAA="],
                ],
            )
        ]
        GetEventsResponse.model_validate(result)
        cursor = "0000054713588387839-0000000000"
        limit = 10
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).get_events(
                start_ledger, filters, cursor, limit
            ) == GetEventsResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getEvents"
        assert request_data["params"] == {
            "filters": [
                {
                    "contractIds": [
                        "CBNYUGHFAIWK3HOINA2OIGOOBMQU4D3MPQWFYBTUYY5WY4FVDO2GWXUY"
                    ],
                    "topics": [
                        ["AAAADwAAAAdDT1VOVEVSAA==", "AAAADwAAAAlpbmNyZW1lbnQAAAA="]
                    ],
                    "type": "contract",
                }
            ],
            "pagination": {"cursor": "0000054713588387839-0000000000", "limit": 10},
            "startLedger": 100,
        }

    def test_get_latest_ledger(self):
        result = {
            "id": "e73d7654b72daa637f396669182c6072549736a9e3b6fcb8e685adb61f8c910a",
            "protocolVersion": "20",
            "sequence": 24170,
        }
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(
                PRC_URL
            ).get_latest_ledger() == GetLatestLedgerResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getLatestLedger"
        assert request_data["params"] is None

    def test_get_fee_stats(self):
        result = {
            "sorobanInclusionFee": {
                "max": "210",
                "min": "100",
                "mode": "100",
                "p10": "100",
                "p20": "100",
                "p30": "100",
                "p40": "100",
                "p50": "100",
                "p60": "100",
                "p70": "100",
                "p80": "100",
                "p90": "120",
                "p95": "190",
                "p99": "200",
                "transactionCount": "10",
                "ledgerCount": 50,
            },
            "inclusionFee": {
                "max": "100",
                "min": "100",
                "mode": "100",
                "p10": "100",
                "p20": "100",
                "p30": "100",
                "p40": "100",
                "p50": "100",
                "p60": "100",
                "p70": "100",
                "p80": "100",
                "p90": "100",
                "p95": "100",
                "p99": "100",
                "transactionCount": "7",
                "ledgerCount": 10,
            },
            "latestLedger": 4519945,
        }

        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(
                PRC_URL
            ).get_fee_stats() == GetFeeStatsResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getFeeStats"
        assert request_data["params"] is None

    def test_get_transactions(self):
        result = {
            "transactions": [
                {
                    "status": "FAILED",
                    "applicationOrder": 1,
                    "feeBump": False,
                    "envelopeXdr": "AAAAAgAAAACDz21Q3CTITlGqRus3/96/05EDivbtfJncNQKt64BTbAAAASwAAKkyAAXlMwAAAAEAAAAAAAAAAAAAAABmWeASAAAAAQAAABR3YWxsZXQ6MTcxMjkwNjMzNjUxMAAAAAEAAAABAAAAAIPPbVDcJMhOUapG6zf/3r/TkQOK9u18mdw1Aq3rgFNsAAAAAQAAAABwOSvou8mtwTtCkysVioO35TSgyRir2+WGqO8FShG/GAAAAAFVQUgAAAAAAO371tlrHUfK+AvmQvHje1jSUrvJb3y3wrJ7EplQeqTkAAAAAAX14QAAAAAAAAAAAeuAU2wAAABAn+6A+xXvMasptAm9BEJwf5Y9CLLQtV44TsNqS8ocPmn4n8Rtyb09SBiFoMv8isYgeQU5nAHsIwBNbEKCerusAQ==",
                    "resultXdr": "AAAAAAAAAGT/////AAAAAQAAAAAAAAAB////+gAAAAA=",
                    "resultMetaXdr": "AAAAAwAAAAAAAAACAAAAAwAc0RsAAAAAAAAAAIPPbVDcJMhOUapG6zf/3r/TkQOK9u18mdw1Aq3rgFNsAAAAF0YpYBQAAKkyAAXlMgAAAAsAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAMAAAAAABzRGgAAAABmWd/VAAAAAAAAAAEAHNEbAAAAAAAAAACDz21Q3CTITlGqRus3/96/05EDivbtfJncNQKt64BTbAAAABdGKWAUAACpMgAF5TMAAAALAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAc0RsAAAAAZlnf2gAAAAAAAAAAAAAAAAAAAAA=",
                    "ledger": 1888539,
                    "createdAt": 1717166042,
                },
                {
                    "status": "SUCCESS",
                    "applicationOrder": 2,
                    "feeBump": False,
                    "envelopeXdr": "AAAAAgAAAAC4EZup+ewCs/doS3hKbeAa4EviBHqAFYM09oHuLtqrGAAPQkAAGgQZAAAANgAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAABB90WssODNIgi6BHveqzxTRmIpvAFRyVNM+Hm2GVuCcAAAAAAAAAAAq6aHAHZ2sd9aPbRsskrlXMLWIwqs4Sv2Bk+VwuIR+9wAAABdIdugAAAAAAAAAAAIu2qsYAAAAQERzKOqYYiPXNwsiL8ADAG/f45RBssmf3umGzw4qKkLGlObuPdX0buWmTGrhI13SG38F2V8Mp9DI+eDkcCjMSAOGVuCcAAAAQHnm0o/r+Gsl+6oqBgSbqoSY37gflvQB3zZRghuir0N75UVerd0Q50yG5Zfu08i2crhx6uk+5HYTl8/Sa7uZ+Qc=",
                    "resultXdr": "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAA=",
                    "resultMetaXdr": "AAAAAwAAAAAAAAACAAAAAwAc0RsAAAAAAAAAALgRm6n57AKz92hLeEpt4BrgS+IEeoAVgzT2ge4u2qsYAAAAADwzS2gAGgQZAAAANQAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAMAAAAAABzPVAAAAABmWdZ2AAAAAAAAAAEAHNEbAAAAAAAAAAC4EZup+ewCs/doS3hKbeAa4EviBHqAFYM09oHuLtqrGAAAAAA8M0toABoEGQAAADYAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAc0RsAAAAAZlnf2gAAAAAAAAABAAAAAwAAAAMAHNEaAAAAAAAAAAAQfdFrLDgzSIIugR73qs8U0ZiKbwBUclTTPh5thlbgnABZJUSd0V2hAAAAawAAAlEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAaBGEAAAAAZkspCwAAAAAAAAABABzRGwAAAAAAAAAAEH3Rayw4M0iCLoEe96rPFNGYim8AVHJU0z4ebYZW4JwAWSUtVVp1oQAAAGsAAAJRAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAwAAAAAAGgRhAAAAAGZLKQsAAAAAAAAAAAAc0RsAAAAAAAAAACrpocAdnax31o9tGyySuVcwtYjCqzhK/YGT5XC4hH73AAAAF0h26AAAHNEbAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                    "ledger": 1888539,
                    "createdAt": 1717166042,
                },
                {
                    "status": "SUCCESS",
                    "applicationOrder": 3,
                    "feeBump": False,
                    "envelopeXdr": "AAAAAgAAAACwtG/IRC5DZE1UdekijEsoQEPM/uOwZ3iY/Y8UZ3b9xAAPQkAAGgRHAAAANgAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAABB90WssODNIgi6BHveqzxTRmIpvAFRyVNM+Hm2GVuCcAAAAAAAAAADgdupKeB04lazKXCOb+E1JfxaM3tI4Xsb/qDa1MWOvXgAAABdIdugAAAAAAAAAAAJndv3EAAAAQKcTimw6KKcM0AeCMxXJcEK/hS9ROoj/qpMFppGNAr4W3ifSOSTGAFbA+cIVHmaV4p7xGcR+9JnUN1YjamvJZwSGVuCcAAAAQK9Cp775JbnYA793SXkkWWbmvnEFTiDPiFyTHxTphCwBDB1zqkXqGG6Q5O3dAyqkNJvj1XNRDsmY4pKV41qijQU=",
                    "resultXdr": "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAA=",
                    "resultMetaXdr": "AAAAAwAAAAAAAAACAAAAAwAc0RsAAAAAAAAAALC0b8hELkNkTVR16SKMSyhAQ8z+47BneJj9jxRndv3EAAAAADwzS2gAGgRHAAAANQAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAMAAAAAABzPVAAAAABmWdZ2AAAAAAAAAAEAHNEbAAAAAAAAAACwtG/IRC5DZE1UdekijEsoQEPM/uOwZ3iY/Y8UZ3b9xAAAAAA8M0toABoERwAAADYAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAc0RsAAAAAZlnf2gAAAAAAAAABAAAAAwAAAAMAHNEbAAAAAAAAAAAQfdFrLDgzSIIugR73qs8U0ZiKbwBUclTTPh5thlbgnABZJS1VWnWhAAAAawAAAlEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAaBGEAAAAAZkspCwAAAAAAAAABABzRGwAAAAAAAAAAEH3Rayw4M0iCLoEe96rPFNGYim8AVHJU0z4ebYZW4JwAWSUWDOONoQAAAGsAAAJRAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAwAAAAAAGgRhAAAAAGZLKQsAAAAAAAAAAAAc0RsAAAAAAAAAAOB26kp4HTiVrMpcI5v4TUl/Foze0jhexv+oNrUxY69eAAAAF0h26AAAHNEbAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                    "ledger": 1888539,
                    "createdAt": 1717166042,
                },
                {
                    "status": "SUCCESS",
                    "applicationOrder": 4,
                    "feeBump": False,
                    "envelopeXdr": "AAAAAgAAAACxMt2gKYOehEoVbmh9vfvZ4mVzXFSNTbAU5S4a8zorrAA4wrwAHLqRAAAADAAAAAAAAAAAAAAAAQAAAAAAAAAYAAAAAQAAAAAAAAAAAAAAALEy3aApg56EShVuaH29+9niZXNcVI1NsBTlLhrzOiusz3K+BVgRzXig/Bhz1TL5Qy+Ibv6cDvCfdaAtBMMFPcYAAAAAHXUVmJM11pdJSKKV52UJrVYlvxaPLmmg17nMe0HGy0MAAAABAAAAAAAAAAEAAAAAAAAAAAAAAACxMt2gKYOehEoVbmh9vfvZ4mVzXFSNTbAU5S4a8zorrM9yvgVYEc14oPwYc9Uy+UMviG7+nA7wn3WgLQTDBT3GAAAAAB11FZiTNdaXSUiiledlCa1WJb8Wjy5poNe5zHtBxstDAAAAAAAAAAEAAAAAAAAAAQAAAAcddRWYkzXWl0lIopXnZQmtViW/Fo8uaaDXucx7QcbLQwAAAAEAAAAGAAAAAbolCtTsMrJvK0M2SaskFsaMajj3iAZbXxELZHwDyE5dAAAAFAAAAAEABf2jAAAd1AAAAGgAAAAAADjCWAAAAAHzOiusAAAAQM+qaiMKxMoCVNjdRIh3X9CSxkjAm0BpXYDB9Fd+DS0guYKiY3TMaVe243UB008iBn5ynQv724rReXlg7iFqXQA=",
                    "resultXdr": "AAAAAAAw3cUAAAAAAAAAAQAAAAAAAAAYAAAAAKg/pGuhtOG27rIpG8xhUIp46CStGWOcsGlNsTQv44UOAAAAAA==",
                    "resultMetaXdr": "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",
                    "diagnosticEventsXdr": [
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAACnJlYWRfZW50cnkAAAAAAAUAAAAAAAAAAg==",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAC3dyaXRlX2VudHJ5AAAAAAUAAAAAAAAAAQ==",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAEGxlZGdlcl9yZWFkX2J5dGUAAAAFAAAAAAAAHdQ=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAEWxlZGdlcl93cml0ZV9ieXRlAAAAAAAABQAAAAAAAABo",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAADXJlYWRfa2V5X2J5dGUAAAAAAAAFAAAAAAAAAFQ=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAADndyaXRlX2tleV9ieXRlAAAAAAAFAAAAAAAAAAA=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAADnJlYWRfZGF0YV9ieXRlAAAAAAAFAAAAAAAAAAA=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAD3dyaXRlX2RhdGFfYnl0ZQAAAAAFAAAAAAAAAGg=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAADnJlYWRfY29kZV9ieXRlAAAAAAAFAAAAAAAAHdQ=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAD3dyaXRlX2NvZGVfYnl0ZQAAAAAFAAAAAAAAAAA=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAACmVtaXRfZXZlbnQAAAAAAAUAAAAAAAAAAA==",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAD2VtaXRfZXZlbnRfYnl0ZQAAAAAFAAAAAAAAAAA=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAACGNwdV9pbnNuAAAABQAAAAAABTO4",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAACG1lbV9ieXRlAAAABQAAAAAAAPkD",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAEWludm9rZV90aW1lX25zZWNzAAAAAAAABQAAAAAAAmiz",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAD21heF9yd19rZXlfYnl0ZQAAAAAFAAAAAAAAADA=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAEG1heF9yd19kYXRhX2J5dGUAAAAFAAAAAAAAAGg=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAEG1heF9yd19jb2RlX2J5dGUAAAAFAAAAAAAAHdQ=",
                        "AAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAADwAAAAxjb3JlX21ldHJpY3MAAAAPAAAAE21heF9lbWl0X2V2ZW50X2J5dGUAAAAABQAAAAAAAAAA",
                    ],
                    "ledger": 1888539,
                    "createdAt": 1717166042,
                },
                {
                    "status": "FAILED",
                    "applicationOrder": 1,
                    "feeBump": False,
                    "envelopeXdr": "AAAAAgAAAAAxLMEcxmfUgNzL687Js4sX/jmFQDqTo1Lj4KDoC1PeSQAehIAAAAIJAAtMUQAAAAEAAAAAAAAAAAAAAABmWeAVAAAAAQAAAAlwc3BiOjMyMTcAAAAAAAACAAAAAQAAAACKlutUN5GT3UOoE2BUkNtJEwoipGOinBFsQtXgpIZMxQAAAAEAAAAA433o+yremWU3t88cKpfpHR+JMFR44JHzmBGni6hqCEYAAAACQVRVQUgAAAAAAAAAAAAAAGfK1mN4mg51jbX6by6TWghGynQ463doEDgzriqZo9bzAAAAAAaOd4AAAAABAAAAAIqW61Q3kZPdQ6gTYFSQ20kTCiKkY6KcEWxC1eCkhkzFAAAAAQAAAADjfej7Kt6ZZTe3zxwql+kdH4kwVHjgkfOYEaeLqGoIRgAAAAJBVFVTRAAAAAAAAAAAAAAAZ8rWY3iaDnWNtfpvLpNaCEbKdDjrd2gQODOuKpmj1vMAAAAAADh1IAAAAAAAAAACC1PeSQAAAEBoad/kqj/4Sqq5tC6HyeMm5LJKM1VqKRGZc3e4uvA3ITThwn2nNMRJRegdQrLrPBTSgw51nY8npilXVIds7I0OpIZMxQAAAEDTZNaLjIDMWPDdCxa1ZB28vUxTcS/0xykOFTI/JAz096vX6Y7wI0QvnbPM7KCoL0cJAciD+pJxNqXQ2Aff1hoO",
                    "resultXdr": "AAAAAAAAAMj/////AAAAAgAAAAAAAAAB////+wAAAAAAAAAB////+wAAAAA=",
                    "resultMetaXdr": "AAAAAwAAAAAAAAACAAAAAwAc0RwAAAAAAAAAADEswRzGZ9SA3Mvrzsmzixf+OYVAOpOjUuPgoOgLU95JAAAAFxzxIbUAAAIJAAtMUAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAMAAAAAABzRGgAAAABmWd/VAAAAAAAAAAEAHNEcAAAAAAAAAAAxLMEcxmfUgNzL687Js4sX/jmFQDqTo1Lj4KDoC1PeSQAAABcc8SG1AAACCQALTFEAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAADAAAAAAAc0RwAAAAAZlnf3wAAAAAAAAAAAAAAAAAAAAA=",
                    "ledger": 1888540,
                    "createdAt": 1717166047,
                },
            ],
            "latestLedger": 1888542,
            "latestLedgerCloseTimestamp": 1717166057,
            "oldestLedger": 1871263,
            "oldestLedgerCloseTimestamp": 1717075350,
            "cursor": "8111217537191937",
        }

        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "result": result,
        }

        start_ledger = 1888539
        GetTransactionsResponse.model_validate(result)
        limit = 5
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).get_transactions(
                start_ledger, None, limit
            ) == GetTransactionsResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "getTransactions"
        assert request_data["params"] == {
            "startLedger": 1888539,
            "pagination": {"cursor": None, "limit": 5},
        }

    def test_simulate_transaction(self):
        result = {
            "transactionData": "AAAAAAAAAAIAAAAGAAAAAcWLK/vE8FTnMk9r8gytPgJuQbutGm0gw9fUkY3tFlQRAAAAFAAAAAEAAAAAAAAAB300Hyg0HZG+Qie3zvsxLvugrNtFqd3AIntWy9bg2YvZAAAAAAAAAAEAAAAGAAAAAcWLK/vE8FTnMk9r8gytPgJuQbutGm0gw9fUkY3tFlQRAAAAEAAAAAEAAAACAAAADwAAAAdDb3VudGVyAAAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAQAAAAAAFcLDAAAF8AAAAQgAAAMcAAAAAAAAAJw=",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                "AAAAAQAAAAAAAAABxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
            ],
            "minResourceFee": "58595",
            "results": [
                {
                    "auth": [
                        "AAAAAAAAAAAAAAABxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
                    ],
                    "xdr": "AAAAAwAAABQ=",
                }
            ],
            "cost": {"cpuInsns": "1240100", "memBytes": "161637"},
            "stateChanges": [
                {
                    "type": "created",
                    "key": "AAAAAAAAAABuaCbVXZ2DlXWarV6UxwbW3GNJgpn3ASChIFp5bxSIWg==",
                    "before": None,
                    "after": "AAAAZAAAAAAAAAAAbmgm1V2dg5V1mq1elMcG1txjSYKZ9wEgoSBaeW8UiFoAAAAAAAAAZAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                }
            ],
            "latestLedger": "1479",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "e1fabdcdf0244a2a9adfab94d7748b6c",
            "result": result,
        }
        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).simulate_transaction(
                transaction
            ) == SimulateTransactionResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "simulateTransaction"
        assert request_data["params"] == {
            "transaction": transaction.to_xdr(),
            "resourceConfig": None,
        }

    def test_simulate_transaction_with_addl_resources(self):
        result = {
            "transactionData": "AAAAAAAAAAIAAAAGAAAAAcWLK/vE8FTnMk9r8gytPgJuQbutGm0gw9fUkY3tFlQRAAAAFAAAAAEAAAAAAAAAB300Hyg0HZG+Qie3zvsxLvugrNtFqd3AIntWy9bg2YvZAAAAAAAAAAEAAAAGAAAAAcWLK/vE8FTnMk9r8gytPgJuQbutGm0gw9fUkY3tFlQRAAAAEAAAAAEAAAACAAAADwAAAAdDb3VudGVyAAAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAQAAAAAAFcLDAAAF8AAAAQgAAAMcAAAAAAAAAJw=",
            "events": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                "AAAAAQAAAAAAAAABxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
            ],
            "minResourceFee": "58595",
            "results": [
                {
                    "auth": [
                        "AAAAAAAAAAAAAAABxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
                    ],
                    "xdr": "AAAAAwAAABQ=",
                }
            ],
            "cost": {"cpuInsns": "1240100", "memBytes": "161637"},
            "latestLedger": "1479",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "e1fabdcdf0244a2a9adfab94d7748b6c",
            "result": result,
        }
        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).simulate_transaction(
                transaction, ResourceLeeway(1000000)
            ) == SimulateTransactionResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "simulateTransaction"
        assert request_data["params"] == {
            "transaction": transaction.to_xdr(),
            "resourceConfig": {"instructionLeeway": 1000000},
        }

    def test_prepare_transaction_without_auth_and_soroban_data(self):
        data = {
            "jsonrpc": "2.0",
            "id": "7a469b9d6ed4444893491be530862ce3",
            "result": {
                "transactionData": "AAAAAAAAAAIAAAAGAAAAAem354u9STQWq5b3Ed1j9tOemvL7xV0NPwhn4gXg0AP8AAAAFAAAAAEAAAAH8dTe2OoI0BnhlDbH0fWvXmvprkBvBAgKIcL9busuuMEAAAABAAAABgAAAAHpt+eLvUk0FquW9xHdY/bTnpry+8VdDT8IZ+IF4NAD/AAAABAAAAABAAAAAgAAAA8AAAAHQ291bnRlcgAAAAASAAAAAAAAAABYt8SiyPKXqo89JHEoH9/M7K/kjlZjMT7BjhKnPsqYoQAAAAEAHifGAAAFlAAAAIgAAAAAAAAAAg==",
                "minResourceFee": "58181",
                "events": [
                    "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAg6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                    "AAAAAQAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
                ],
                "results": [
                    {
                        "auth": [
                            "AAAAAAAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
                        ],
                        "xdr": "AAAAAwAAABQ=",
                    }
                ],
                "cost": {"cpuInsns": "1646885", "memBytes": "1296481"},
                "latestLedger": "14245",
            },
        }

        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            new_transaction = SorobanServer(PRC_URL).prepare_transaction(transaction)
        expected_transaction = copy.deepcopy(transaction)
        expected_transaction.transaction.fee += int(data["result"]["minResourceFee"])
        expected_transaction.transaction.soroban_data = (
            stellar_xdr.SorobanTransactionData.from_xdr(
                data["result"]["transactionData"]
            )
        )
        op = expected_transaction.transaction.operations[0]
        op.auth = [
            stellar_xdr.SorobanAuthorizationEntry.from_xdr(xdr)
            for xdr in data["result"]["results"][0]["auth"]
        ]
        assert new_transaction == expected_transaction

    def test_prepare_transaction_with_soroban_data(self):
        data = {
            "jsonrpc": "2.0",
            "id": "7a469b9d6ed4444893491be530862ce3",
            "result": {
                "transactionData": "AAAAAAAAAAEAAAAGAAAAAdeSi3LCcDzP6vfrn/TvTVBKVai5efybRQ6iyEK00c5hAAAAFAAAAAEAAAACAAAAAAAAAABPFZKkWLE8Tlrm5Jx81FUrXpm6EhpW/s8TXPUyf0D5PgAAAAAAAAAAbjEdZhNooxW4Z5oCpgPDCmGnVRwOxutuDO14EQ4kFmoAA3kUAAACGAAAASAAAAAAAAG4Sw==",
                "minResourceFee": "112715",
                "events": [
                    "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAg6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                    "AAAAAQAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
                ],
                "results": [
                    {
                        "auth": [
                            "AAAAAAAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
                        ],
                        "xdr": "AAAAAwAAABQ=",
                    }
                ],
                "cost": {"cpuInsns": "1646885", "memBytes": "1296481"},
                "latestLedger": "14245",
            },
        }

        soroban_data = stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(50000),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                read_bytes=stellar_xdr.Uint32(2),
                write_bytes=stellar_xdr.Uint32(3),
                instructions=stellar_xdr.Uint32(4),
            ),
        )  # soroban_data will be overwritten by the response
        transaction = _build_soroban_transaction(soroban_data, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            new_transaction = SorobanServer(PRC_URL).prepare_transaction(transaction)
        expected_transaction = copy.deepcopy(transaction)
        expected_transaction.transaction.fee = 50000 + int(
            data["result"]["minResourceFee"]
        )  # 50000 is base fee
        expected_transaction.transaction.soroban_data = (
            stellar_xdr.SorobanTransactionData.from_xdr(
                data["result"]["transactionData"]
            )
        )
        op = expected_transaction.transaction.operations[0]
        op.auth = [
            stellar_xdr.SorobanAuthorizationEntry.from_xdr(xdr)
            for xdr in data["result"]["results"][0]["auth"]
        ]
        assert new_transaction == expected_transaction

    def test_prepare_transaction_with_auth(self):
        data = {
            "jsonrpc": "2.0",
            "id": "7a469b9d6ed4444893491be530862ce3",
            "result": {
                "transactionData": "AAAAAAAAAAIAAAAGAAAAAem354u9STQWq5b3Ed1j9tOemvL7xV0NPwhn4gXg0AP8AAAAFAAAAAEAAAAH8dTe2OoI0BnhlDbH0fWvXmvprkBvBAgKIcL9busuuMEAAAABAAAABgAAAAHpt+eLvUk0FquW9xHdY/bTnpry+8VdDT8IZ+IF4NAD/AAAABAAAAABAAAAAgAAAA8AAAAHQ291bnRlcgAAAAASAAAAAAAAAABYt8SiyPKXqo89JHEoH9/M7K/kjlZjMT7BjhKnPsqYoQAAAAEAHifGAAAFlAAAAIgAAAAAAAAAAg==",
                "minResourceFee": "58181",
                "events": [
                    "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAg6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                    "AAAAAQAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
                ],
                "results": [
                    {
                        "auth": [
                            "AAAAAAAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
                        ],
                        "xdr": "AAAAAwAAABQ=",
                    }
                ],
                "cost": {"cpuInsns": "1646885", "memBytes": "1296481"},
                "latestLedger": "14245",
            },
        }

        auth = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
            ),
            root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                function=stellar_xdr.SorobanAuthorizedFunction(
                    type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                    contract_fn=stellar_xdr.InvokeContractArgs(
                        contract_address=Address(
                            "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                        ).to_xdr_sc_address(),
                        function_name=stellar_xdr.SCSymbol(b"increment"),
                        args=[],
                    ),
                ),
                sub_invocations=[],
            ),
        )

        transaction = _build_soroban_transaction(None, [auth])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            new_transaction = SorobanServer(PRC_URL).prepare_transaction(transaction)
        expected_transaction = copy.deepcopy(transaction)
        expected_transaction.transaction.fee += int(data["result"]["minResourceFee"])
        expected_transaction.transaction.soroban_data = (
            stellar_xdr.SorobanTransactionData.from_xdr(
                data["result"]["transactionData"]
            )
        )
        op = expected_transaction.transaction.operations[0]
        op.auth = [auth]
        assert new_transaction == expected_transaction

    def test_prepare_transaction_error_resp_prepare_transaction_exception_raise(self):
        data = {
            "jsonrpc": "2.0",
            "id": "7b6ada2bdec04ee28147d1557aadc3cf",
            "result": {
                "error": 'HostError: Error(WasmVm, MissingValue)\n\nEvent log (newest first):\n   0: [Diagnostic Event] contract:607682f2477a6be8cdf0fdf32be13d5f25a686cc094fd93d5aa3d7b68232d0c0, topics:[error, Error(WasmVm, MissingValue)], data:["invoking unknown export", increment]\n   1: [Diagnostic Event] topics:[fn_call, Bytes(607682f2477a6be8cdf0fdf32be13d5f25a686cc094fd93d5aa3d7b68232d0c0), increment], data:[Address(Account(58b7c4a2c8f297aa8f3d2471281fdfccecafe48e5663313ec18e12a73eca98a1)), 10]\n\nBacktrace (newest first):\n   0: soroban_env_host::vm::Vm::invoke_function_raw\n   1: soroban_env_host::host::frame::<impl soroban_env_host::host::Host>::call_n_internal\n   2: soroban_env_host::host::frame::<impl soroban_env_host::host::Host>::invoke_function\n   3: preflight::preflight_invoke_hf_op::{{closure}}\n   4: preflight::catch_preflight_panic\n   5: _cgo_a3255893d7fd_Cfunc_preflight_invoke_hf_op\n             at /tmp/go-build/cgo-gcc-prolog:99:11\n   6: runtime.asmcgocall\n             at ./runtime/asm_amd64.s:848\n\n',
                "transactionData": None,
                "events": None,
                "minResourceFee": "0",
                "cost": {"cpuInsns": "0", "memBytes": "0"},
                "latestLedger": "898",
            },
        }
        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            with pytest.raises(
                PrepareTransactionException,
                match="Simulation transaction failed, the response contains error information.",
            ) as e:
                SorobanServer(PRC_URL).prepare_transaction(transaction)
            assert (
                e.value.simulate_transaction_response
                == SimulateTransactionResponse.model_validate(data["result"])
            )

    def test_prepare_transaction_invalid_results_value_raise(
        self,
    ):
        # this error should not happen
        data = {
            "jsonrpc": "2.0",
            "id": "7a469b9d6ed4444893491be530862ce3",
            "result": {
                "transactionData": "AAAAAAAAAAIAAAAGAAAAAem354u9STQWq5b3Ed1j9tOemvL7xV0NPwhn4gXg0AP8AAAAFAAAAAEAAAAH8dTe2OoI0BnhlDbH0fWvXmvprkBvBAgKIcL9busuuMEAAAABAAAABgAAAAHpt+eLvUk0FquW9xHdY/bTnpry+8VdDT8IZ+IF4NAD/AAAABAAAAABAAAAAgAAAA8AAAAHQ291bnRlcgAAAAASAAAAAAAAAABYt8SiyPKXqo89JHEoH9/M7K/kjlZjMT7BjhKnPsqYoQAAAAEAHifGAAAFlAAAAIgAAAAAAAAAAg==",
                "minResourceFee": "58181",
                "events": [
                    "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAg6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAAPAAAACWluY3JlbWVudAAAAAAAABAAAAABAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAo=",
                    "AAAAAQAAAAAAAAAB6bfni71JNBarlvcR3WP2056a8vvFXQ0/CGfiBeDQA/wAAAACAAAAAAAAAAIAAAAPAAAACWZuX3JldHVybgAAAAAAAA8AAAAJaW5jcmVtZW50AAAAAAAAAwAAABQ=",
                ],
                "results": [],
                "cost": {"cpuInsns": "1646885", "memBytes": "1296481"},
                "latestLedger": "14245",
            },
        }
        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            with pytest.raises(
                ValueError,
                match="Simulation results invalid",
            ) as e:
                SorobanServer(PRC_URL).prepare_transaction(transaction)

    def test_send_transaction(self):
        result = {
            "status": "PENDING",
            "hash": "64977cc4bb7f8bf75bdc47570548a994667899d3319b72f95cb2a64e567ad52c",
            "latestLedger": "1479",
            "latestLedgerCloseTime": "1690594566",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "688dfcf3bcd04f52af4866e98dffe387",
            "result": result,
        }

        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).send_transaction(
                transaction
            ) == SendTransactionResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "sendTransaction"
        assert request_data["params"] == {"transaction": transaction.to_xdr()}
        assert result["hash"] == transaction.hash_hex()

    def test_send_transaction_error(self):
        result = {
            "status": "ERROR",
            "errorResultXdr": "AAAAAAAAf67////6AAAAAA==",
            "diagnosticEventsXdr": [
                "AAAAAQAAAAAAAAAAAAAAAgAAAAAAAAADAAAADwAAAAdmbl9jYWxsAAAAAA0AAAAgr/p6gt6h8MrmSw+WNJnu3+sCP9dHXx7jR8IH0sG6Cy0AAAAPAAAABWhlbGxvAAAAAAAADwAAAAVBbG9oYQAAAA=="
            ],
            "hash": "64977cc4bb7f8bf75bdc47570548a994667899d3319b72f95cb2a64e567ad52c",
            "latestLedger": "1479",
            "latestLedgerCloseTime": "1690594566",
        }
        data = {
            "jsonrpc": "2.0",
            "id": "688dfcf3bcd04f52af4866e98dffe387",
            "result": result,
        }

        transaction = _build_soroban_transaction(None, [])
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            assert SorobanServer(PRC_URL).send_transaction(
                transaction
            ) == SendTransactionResponse.model_validate(result)

        request_data = m.last_request.json()
        assert len(request_data["id"]) == 32
        assert request_data["jsonrpc"] == "2.0"
        assert request_data["method"] == "sendTransaction"
        assert request_data["params"] == {"transaction": transaction.to_xdr()}
        assert result["hash"] == transaction.hash_hex()

    def test_soroban_rpc_error_response_raise(self):
        data = {
            "jsonrpc": "2.0",
            "id": "198cb1a8-9104-4446-a269-88bf000c2721",
            "error": {
                "code": -32601,
                "message": "method not found",
                "data": "mockTest",
            },
        }
        with requests_mock.Mocker() as m:
            m.post(PRC_URL, json=data)
            with pytest.raises(SorobanRpcErrorResponse) as e:
                SorobanServer(PRC_URL).get_health()
            assert e.value.code == -32601
            assert e.value.message == "method not found"
            assert e.value.data == "mockTest"


def _build_soroban_transaction(
    soroban_data: Optional[stellar_xdr.SorobanTransactionData],
    auth: List[stellar_xdr.SorobanAuthorizationEntry],
):
    contract_id = (
        "CDU3PZ4LXVETIFVLS33RDXLD63JZ5GXS7PCV2DJ7BBT6EBPA2AB7YR5H"  # auth contract
    )

    tx_submitter_kp = Keypair.from_secret(
        "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
    )
    op_invoker_kp = Keypair.from_secret(
        "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
    )
    source = Account(tx_submitter_kp.public_key, 3053721747476)
    tx_builder = (
        TransactionBuilder(
            source_account=source,
            network_passphrase=Network.STANDALONE_NETWORK_PASSPHRASE,
            base_fee=50000,
        )
        .add_time_bounds(0, 0)
        .append_invoke_contract_function_op(
            contract_id=contract_id,
            function_name="increment",
            parameters=[
                scval.to_address(op_invoker_kp.public_key),
                scval.to_uint32(10),
            ],
            auth=auth,
            source=op_invoker_kp.public_key,
        )
    )
    if soroban_data:
        tx_builder.set_soroban_data(soroban_data)
    return tx_builder.build()
