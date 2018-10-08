# You may get a warning that the connection failed, but don't panic,
# the program will always try to reconnect.
# see: https://github.com/StellarCN/py-stellar-base/issues/152
from stellar_base.address import Address

address = 'GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A'
horizon = 'https://horizon.stellar.org'
cursor = 'now'  # or load where you left off

address = Address(address=address, horizon_uri=horizon)


def payment_handler(response):
    print(response.data)


payments = address.payments(sse=True, cursor=cursor)
for payment in payments:
    payment_handler(payment)