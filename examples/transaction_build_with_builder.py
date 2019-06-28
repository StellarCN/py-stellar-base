from stellar_base.builder import Builder

alice_seed = 'SBUORYV26AZ3ULEEC5FQ4NKPVRO7MBAWTW26YKCDPPKFGMK7WAYNX4UN'
bob_address = 'GBZF7GQJXXHD3OL3B5IOUICFDYIATZZ3F3XQ7SOQ5PXLVQMDSOI5ACEE'

horizon_uri = 'https://horizon-testnet.stellar.org'  # testnet horizon
# horizon_uri = 'https://horizon-testnet.stellar.org' # public horizon
network = 'TESTNET'  # for test network
# network = 'PUBLIC' # for public network

builder = Builder(secret=alice_seed, horizon_uri=horizon_uri, network=network) \
    .add_text_memo("Buy yourself a beer!") \
    .append_payment_op(destination=bob_address, asset_code='XLM', amount='10.5') \
    .append_set_options_op(home_domain='fed.network')

builder.sign()  # signed by alice
response = builder.submit()  # send it to horizon
print(response)
