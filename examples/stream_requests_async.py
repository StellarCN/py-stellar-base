import asyncio

from stellar_sdk import AiohttpClient, Server

HORIZON_URL = "https://horizon.stellar.org"


async def payments():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        async for payment in server.payments().cursor(cursor="now").stream():
            print(f"Payment: {payment}")


async def effects():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        async for effect in server.effects().cursor(cursor="now").stream():
            print(f"Effect: {effect}")


async def operations():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        async for operation in server.operations().cursor(cursor="now").stream():
            print(f"Operation: {operation}")


async def transactions():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        async for transaction in server.transactions().cursor(cursor="now").stream():
            print(f"Transaction: {transaction}")


async def listen():
    await asyncio.gather(
        payments(),
        effects(),
        operations(),
        transactions()
    )


if __name__ == '__main__':
    asyncio.run(listen())
