from stellar_base.builder import Builder

alice_secret = 'SCB6JIZUC3RDHLRGFRTISOUYATKEE63EP7MCHNZNXQMQGZSLZ5CNRTKK'
bob_address = 'GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH'

builder = Builder(secret=alice_secret, horizon_uri='https://horizon.stellar.org', network='PUBLIC')
builder.add_text_memo("Hello, Stellar!").append_payment_op(
    destination=bob_address, amount='12.25', asset_code='XLM')
builder.sign()
response = builder.submit()
print(response)
