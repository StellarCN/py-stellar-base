"""
See: https://stellar-sdk.readthedocs.io/en/latest/querying_horizon.html#building-requests
"""
from stellar_sdk import Server

server = Server(horizon_url="https://horizon.stellar.org")
account = "GB6NVEN5HSUBKMYCE5ZOWSK5K23TBWRUQLZY3KNMXUZ3AQ2ESC4MY4AQ"

# get a list of transactions that occurred in ledger 1400
transactions = server.transactions().for_ledger(1400).call()
print(transactions)

# get a list of transactions submitted by a particular account
transactions = server.transactions().for_account(account_id=account).call()
print(transactions)

# The following example will show you how to handle paging
print(f"Gets all payment operations associated with {account}.")
payments_records = []
payments_call_builder = (
    server.payments().for_account(account).order(desc=False).limit(10)
)  # limit can be set to a maximum of 200
payments_records += payments_call_builder.call()["_embedded"]["records"]
page_count = 0
while page_records := payments_call_builder.next()["_embedded"]["records"]:
    payments_records += page_records
    print(f"Page {page_count} fetched")
    print(f"data: {page_records}")
    page_count += 1
print(f"Payments count: {len(payments_records)}")
