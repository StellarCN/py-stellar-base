from stellar_base.builder import Builder

alice_seed = 'SB4675LMYLBWMKENDBAO6ZTVPLI6AISE3VZZDZASUFWW2T4MEGKX7NEI'
bob_address = 'GCRNOBFLTGLGSYOWCYINZA7JAAAZ5CXMSNM7QUYFYOHHIEZY4R6665MA'

selling_code = 'XLM'
selling_issuer = None

buying_code = 'XCN'
buying_issuer = 'GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY'

price = '5.5'  # or price = {'n': 55, 'd': 10}
amount = '12.5'

builder = Builder(secret=alice_seed, horizon_uri='https://horizon-testnet.stellar.org') \
             .append_manage_offer_op(selling_code, selling_issuer, buying_code, \
              buying_issuer, amount, price)

builder.sign()
builder.submit()