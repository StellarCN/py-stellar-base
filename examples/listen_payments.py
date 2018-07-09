from stellar_base.address import Address

address = 'GBVFCKIISDBSN5NSSTMVMLMWRR5ZP2DSUBIISG5JFW6YIQC5HO5JC6YS'
horizon = 'https://horizon-testnet.stellar.org'
cursor = 0  # or load where you left off

addr = Address(address=address, horizon=horizon)


def paymentHandler(response):
    print(response)


payments = addr.payments(sse=True, cursor=cursor)
for payment in payments:
    paymentHandler(payment)
