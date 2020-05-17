import asyncio
import logging

from stellar_sdk import AiohttpClient, Server
from stellar_sdk.exceptions import StreamClientError

HORIZON_URL = "https://horizon.stellar.org"

async def transactions():
    async with Server(HORIZON_URL, AiohttpClient()) as server:
        cursor = "now"
        while True:
            try:
                async for transaction in server.transactions().cursor(cursor).stream():
                    print(f"Transaction: {transaction}")
            except StreamClientError as e:
                logging.error(f'An error({e}) was encountered while reading the SSE message, which was caused by {e.__cause__}.')
                cursor = e.current_cursor


if __name__ == '__main__':
    asyncio.run(transactions())
