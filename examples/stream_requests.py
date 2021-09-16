"""
See: https://stellar-sdk.readthedocs.io/en/latest/querying_horizon.html#streaming-requests
"""
from stellar_sdk import Server
from e_utils import read_key


func_key = read_key()

server = Server(horizon_url="https://horizon-testnet.stellar.org")
account_id = func_key['destination_acct_0']
last_cursor = "now"  # or load where you left off


def tx_handler(tx_response):
    print(tx_response)


for tx in server.transactions().for_account(account_id).cursor(last_cursor).stream():
    tx_handler(tx)
