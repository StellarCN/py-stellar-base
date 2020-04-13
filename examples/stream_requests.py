from stellar_sdk import Server

server = Server(horizon_url="https://horizon-testnet.stellar.org")
account_id = "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"
last_cursor = "now"  # or load where you left off


def tx_handler(tx_response):
    # You can use raw data or parsed data to get a better development experience.
    # print(tx_response.raw_data)
    print(tx_response.parse_data())


for tx in server.transactions().for_account(account_id).cursor(last_cursor).stream():
    tx_handler(tx)
