.. _snippets:

********
Snippets
********

Random Key Generation
---------------------
.. code-block:: python

   from stellar_base.keypair import Keypair
   kp = Keypair.random()


Multiple Key Generation
-----------------------
.. code-block:: python

  from stellar_base.utils import StellarMnemonic
  from stellar_base.keypair import Keypair
  sm = StellarMnemonic()
  secret_phrase = sm.generate()
  kp0 = Keypair.deterministic(secret_phrase, index=0)
  kp1 = Keypair.deterministic(secret_phrase, index=1)
  kp2 = Keypair.deterministic(secret_phrase, index=2)


Create Account
--------------
.. code-block:: python

   from stellar_base.builder import Builder
   alice_seed = 'SB4675LMYLBWMKENDBAO6ZTVPLI6AISE3VZZDZASUFWW2T4MEGKX7NEI'
   bob_address = 'GCRNOBFLTGLGSYOWCYINZA7JAAAZ5CXMSNM7QUYFYOHHIEZY4R6665MA'
   builder = Builder(secret=alice_seed, horizon='https://horizon-testnet.stellar.org')
   builder.append_create_account_op(destination=bob_address, starting_balance=2)
   builder.sign()
   builder.submit()


Payment
-------
.. code-block:: python

   from stellar_base.builder import Builder
   alice_seed = 'SB4675LMYLBWMKENDBAO6ZTVPLI6AISE3VZZDZASUFWW2T4MEGKX7NEI'
   bob_address = 'GCRNOBFLTGLGSYOWCYINZA7JAAAZ5CXMSNM7QUYFYOHHIEZY4R6665MA'
   builder = Builder(secret=alice_seed, horizon='https://horizon-testnet.stellar.org') \
             .append_payment_op(destination=bob_address, amount=100, asset_code='XLM', asset_issuer=None) \
             .add_text_memo("Hey, Stellar!")
   builder.sign()
   builder.submit()


Create Offer
------------
.. code-block:: python

   from stellar_base.builder import Builder
   alice_seed = 'SB4675LMYLBWMKENDBAO6ZTVPLI6AISE3VZZDZASUFWW2T4MEGKX7NEI'
   bob_address = 'GCRNOBFLTGLGSYOWCYINZA7JAAAZ5CXMSNM7QUYFYOHHIEZY4R6665MA'
   selling_code = 'XLM'
   selling_issuer = None
   buying_code = 'XCN'
   buying_issuer = 'GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY'
   price = 5.5
   amount = 12.5
   builder = Builder(secret=alice_seed, horizon='https://horizon-testnet.stellar.org') \
             .append_manage_offer_op(selling_code, selling_issuer, buying_code, \
              buying_issuer, amount, price)
   builder.sign()
   builder.submit()
