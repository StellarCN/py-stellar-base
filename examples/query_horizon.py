from stellar_sdk import Server

server = Server(horizon_url="https://horizon.stellar.org")

# get a list of transactions that occurred in ledger 29576671
transactions = server.transactions().for_ledger(29576671).call()
# You can use raw data or parsed data to get a better development experience.
# print(transactions.raw_data)
print(transactions.parse_data())

# get a list of transactions submitted by a particular account
transactions = (
    server.transactions()
    .for_account(account_id="GDZP7ZPAR4UBJIZH5EGAKJADTKX3LIXKBIPZFFN54XHB6XBAK4QBOHRE")
    .call()
)
# You can use raw data or parsed data to get a better development experience.
# print(transactions.raw_data)
print(transactions.parse_data())
