from stellar_sdk import Server

server = Server(horizon_url="https://horizon-testnet.stellar.org")

# get a list of transactions that occurred in ledger 1400
transactions = server.transactions().for_ledger(1400).call()
print(transactions)

# get a list of transactions submitted by a particular account
transactions = server.transactions() \
    .for_account(account_id="GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW") \
    .call()
print(transactions)
