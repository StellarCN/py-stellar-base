"""
See: https://stellar-sdk.readthedocs.io/en/latest/asynchronous.html
"""
import asyncio

from stellar_sdk import AiohttpClient, ServerAsync

HORIZON_URL = "https://horizon.stellar.org"


async def payments():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for payment in server.payments().cursor(cursor="now").stream():
            print(f"Payment: {payment}")


async def effects():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for effect in server.effects().cursor(cursor="now").stream():
            print(f"Effect: {effect}")


async def operations():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for operation in server.operations().cursor(cursor="now").stream():
            print(f"Operation: {operation}")


async def transactions():
    async with ServerAsync(HORIZON_URL, AiohttpClient()) as server:
        async for transaction in server.transactions().cursor(cursor="now").stream():
            print(f"Transaction: {transaction}")


async def listen():
    await asyncio.gather(payments(), effects(), operations(), transactions())


if __name__ == "__main__":
    asyncio.run(listen())
