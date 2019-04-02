import asyncio

from stellar_base.async_support.address import Address

address = 'GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A'
horizon = 'https://horizon.stellar.org'
cursor = 'now'  # or load where you left off

address = Address(address=address, horizon_uri=horizon)


def payment_handler(response):
    print(response)


async def print_payments():
    async for event in await address.payments(sse=True):
        payment_handler(event)


loop = asyncio.get_event_loop()
loop.run_until_complete(print_payments())
loop.close()
