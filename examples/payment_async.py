import asyncio

from stellar_base.async_support.builder import Builder


async def payment():
    alice_secret = 'SBSDC63JU5NAXX6BA5A2YXJPPDW7FNEPGSP2DO6NM7T7JQHH2MTNYY2R'
    bob_address = 'GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH'
    builder = Builder(secret=alice_secret, horizon_uri='https://h.fchain.io')
    builder.add_text_memo("Hello, Stellar!").append_payment_op(
        destination=bob_address, amount='12.25', asset_code='XLM')
    await builder.sign()
    response = await builder.submit()
    print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(payment())
loop.close()