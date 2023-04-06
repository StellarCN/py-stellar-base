import binascii

import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban import SorobanServer
from stellar_sdk.soroban.soroban_rpc import *

RPC_SERVER = "https://rpc-futurenet.stellar.org:443/"


# TODO: We need automated contract generation and submission
@pytest.mark.skip(
    reason="TODO: We need automated contract generation and submission"
)
class TestSorobanServer:
    def test_get_health(self):
        with SorobanServer(RPC_SERVER) as server:
            response = server.get_health()
            expected_resp = GetHealthResponse(status="healthy")
            assert response == expected_resp

    def test_get_events(self):
        start_ledger = 90000
        end_ledger = 90300
        with SorobanServer(RPC_SERVER) as server:
            response = server.get_events(start_ledger, end_ledger)
            assert isinstance(response, GetEventsResponse)
            assert len(response.events) > 1

    def test_get_network(self):
        with SorobanServer(RPC_SERVER) as server:
            response = server.get_network()
            assert isinstance(response, GetNetworkResponse)
            assert response.friendbot_url == "https://friendbot-futurenet.stellar.org/"
            assert response.passphrase == "Test SDF Future Network ; October 2022"
            assert response.protocol_version >= 20

    def test_get_ledger_entry(self):
        contract_id = "2e0ab0e99241f96f1b4514589d501996b8b36af5021556ddef9bc3a8ab69c0c4"
        ledger_key = stellar_xdr.LedgerKey.from_contract_data(
            stellar_xdr.LedgerKeyContractData(
                contract_id=stellar_xdr.Hash(binascii.unhexlify(contract_id)),
                key=stellar_xdr.SCVal.from_scv_symbol(
                    stellar_xdr.SCSymbol("COUNTER".encode("utf-8"))
                ),
            )
        )
        with SorobanServer(RPC_SERVER) as server:
            response = server.get_ledger_entry(ledger_key)
            assert isinstance(response, GetLedgerEntryResponse)

    def test_get_transaction(self):
        tx_id = "d45558a5e00781c676098e8a339c0f7e997239ba8a38d4b7dfb1af7266f827a2"
        with SorobanServer(RPC_SERVER) as server:
            response = server.get_transaction(tx_id)
            assert isinstance(response, GetTransactionResponse)
            assert response.status == GetTransactionStatus.SUCCESS

    def test_simulate_transaction(self):
        xdr = "AAAAAgAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JAAAAGQAABt3AAAAAwAAAAAAAAAAAAAAAQAAAAAAAAAYAAAAAAAAAAIAAAAEAAAAAQAAAAYAAAAgLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAAFAAAACWluY3JlbWVudAAAAAAAAAIAAAAGLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAADAAAAAwAAAAdhzePVa/b9zS2vgzgjO4T/UT45VAsuLjoTRFAB3ze3lwAAAAEAAAAGLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAAFAAAAB0NPVU5URVIAAAAAAAAAAAAAAAAB4P10JAAAAECa3YcH7yRCNKEhnPaJDvPXwEQx5p9x6/WeNlRG4ulVAFrrjtgX7+vJm1G5z+DJQgj7iC0aly0dsuqyuPKn1oYK"
        with SorobanServer(RPC_SERVER) as server:
            response = server.simulate_transaction(xdr)
            assert isinstance(response, SimulateTransactionResponse)

    def test_send_transaction(self):
        xdr = "AAAAAgAAAADBPp7TMinJylnn+6dQXJACNc15LF+aJ2Py1BaR4P10JAAAAGQAABt3AAAAAwAAAAAAAAAAAAAAAQAAAAAAAAAYAAAAAAAAAAIAAAAEAAAAAQAAAAYAAAAgLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAAFAAAACWluY3JlbWVudAAAAAAAAAIAAAAGLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAADAAAAAwAAAAdhzePVa/b9zS2vgzgjO4T/UT45VAsuLjoTRFAB3ze3lwAAAAEAAAAGLgqw6ZJB+W8bRRRYnVAZlrizavUCFVbd75vDqKtpwMQAAAAFAAAAB0NPVU5URVIAAAAAAAAAAAAAAAAB4P10JAAAAECa3YcH7yRCNKEhnPaJDvPXwEQx5p9x6/WeNlRG4ulVAFrrjtgX7+vJm1G5z+DJQgj7iC0aly0dsuqyuPKn1oYK"
        tx_id = "d45558a5e00781c676098e8a339c0f7e997239ba8a38d4b7dfb1af7266f827a2"

        with SorobanServer(RPC_SERVER) as server:
            response = server.send_transaction(xdr)
            assert isinstance(response, SendTransactionResponse)
            assert response.hash == tx_id
