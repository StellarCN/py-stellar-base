.. _quick_start:

***********
Quick Start
***********

Stellar Guides
==============

At the absolute basics, you'll want to read up on `Stellar's Documentation
Guides <https://www.stellar.org/developers/guides/>`_, as it contains a lot of
information on the concepts used below (Transactions, Payments, Operations,
KeyPairs, etc.).

Alright, let's get started!
===========================

First, you'll want to create a Stellar key pair. There are 2 methods for
generating a key pair:

Random Key Generation
---------------------

Simply use :meth:`Keypair.random <stellar_base.keypair.Keypair.random>` to
generate the object like so:

.. code-block:: python

   from stellar_base.keypair import Keypair
   kp = Keypair.random()

Deterministic generation
------------------------

Or, generate the key pair is deterministically from a mnemonic string, also
known as "seed phrase". This can be useful for backing up the passphrase on
paper and using it later, or by making it easier to memorize than the secret
seed.

First you'll need to generate a mnemonic string:

.. code-block:: python

   from stellar_base.utils import StellarMnemonic
   # Here we use Chinese, but English is the default language.
   sm = StellarMnemonic("chinese")
   secret_phrase = sm.generate()


You can also use your own mnemonic string instead of a generated one. Once
you've created your secret phrase, you should either write your phrase down or
memorize it. You should not share your mnemonic string with anyone.

From here, we use :meth:`Keypair.deterministic
<stellar_base.keypair.Keypair.deterministic>` to generate the keypair from
your secret phrase:

.. code-block:: python

   kp = Keypair.deterministic(secret_phrase, lang='chinese')

You can even create multiple key pairs from the same phrase, using a different
index with each call. For example:

.. code-block:: python

   kp1 = Keypair.deterministic(secret_phrase, lang='chinese', index=1)
   kp2 = Keypair.deterministic(secret_phrase, lang='chinese', index=2)

From the generated :class:`Keypair <stellar_base.keypair.Keypair>` object, you
can easily access your public and private key.

.. code-block:: python

   publickey = kp.address().decode()
   seed = kp.seed().decode()

Your master public key is also your account address. If someone needs to send
you a transaction, you should share your public key with them. However, your
secret seed should always remain locally on your computer, and it should never
be transmitted over the internet.

If you ever forget or lose the public key, you can regenerate the key pair from
the your secret seed:

.. code-block:: python

   from stellar_base.keypair import Keypair
   kp = Keypair.from_seed(seed)

Both the public key and the secret seed can be regenerated via the secret
phrase if you used on.

.. code-block:: python

   from stellar_base.keypair import Keypair
   seed_phrase = '...' # the word sequence that you wrote down or memorized
   kp = Keypair.deterministic(seed_phrase, lang='chinese')

However, if you used a random generator, it is important to never lose your
seed - otherwise you won't be able to send transactions, and many other
operations!

Here is a sample key pair in Stellar Development Foundation's (SDF) TESTNET;
let's use them in the following steps:

.. code-block:: python

   publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
   seed = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'


Create An Account
=================
Now, in order to create an account, you need to run a :class:`CreateAccount
<stellar_base.operation.CreateAccount>` operation with your new account ID.
Due to `Stellar's account minimums
<https://www.stellar.org/developers/guides/concepts/fees.html#minimum-account-balance>`_,
you'll need to transfer the minimum account balance from another account with
the create account operation. As of this writing, minimum balance is ``1 XLM (2
x 0.5 Base Reserve)``, and is subject to change.


Using The SDF Testnet
---------------------
If you want to play in the Stellar test network, you can ask our `Friendbot
<https://www.stellar.org/developers/guides/get-started/create-account.html>`_
to create an account for you as shown below:

.. code-block:: python

   import requests
   publickey = kp.address().decode()
   url = 'https://friendbot.stellar.org'
   r = requests.get(url, params={'addr': publickey})

Using The Stellar Live Network
------------------------------
On the other hand, if you would like to create an account on the live network,
you should buy some Stellar Lumens from an exchange. When you withdraw the
Lumens into your new account, the exchange will automatically create the
account for you. However, if you want to create an account from another
account of your own, here's an example of how to do so:


.. code-block:: python

   from stellar_base.keypair import Keypair
   from stellar_base.operation import CreateAccount, Payment
   from stellar_base.transaction import Transaction
   from stellar_base.transaction_envelope import TransactionEnvelope as Te
   from stellar_base.memo import TextMemo
   from stellar_base.horizon import horizon_livenet

   # This creates a new Horizon Livenet instance
   horizon = horizon_livenet()

   # This is the seed (the StrKey representation of the secret seed that
   # generates your private key from your original account that is funding the
   # new account in the create account operation. You'll need the seed in order
   # to sign off on the transaction. This is the source account.
   old_account_seed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
   old_account_keypair = Keypair.from_seed(old_account_seed)

   # This is the new account ID (the StrKey representation of your newly
   # created public key). This is the destination account.
   new_account_addr = "GABRGTDZEDCQ5W663U2EI5KWRSU3EAWJCSI57H7XAMUO5BQRIGNNZGTY"

   amount = '1' # Your new account minimum balance (in XLM) to transfer over
   # create the CreateAccount operation
   op = CreateAccount(
       destination=new_account_addr,
       starting_balance=amount
   )
   # create a memo
   memo = TextMemo('Hello, StellarCN!')

   # Get the current sequence of the source account by contacting Horizon. You
   # should also check the response for errors!
   # Python 3
   sequence = horizon.account(old_account_keypair.address().decode()).get('sequence')
   # Python 2
   # sequence = horizon.account(old_account_keypair.address()).get('sequence')

   # Create a transaction with our single create account operation, with the
   # default fee of 100 stroops as of this writing (0.00001 XLM)
   tx = Transaction(
       source=old_account_keypair.address().decode(),
       sequence=sequence,
       memo=memo,
       operations=[
           op,
       ],
   )
   # Build a transaction envelope, ready to be signed.
   envelope = Te(tx=tx, network_id="PUBLIC")

   # Sign the transaction envelope with the source keypair
   envelope.sign(old_account_keypair)

   # Submit the transaction to Horizon
   te_xdr = envelope.xdr()
   response = horizon.submit(te_xdr)

Make sure to look at the response body carefully, as it can be an error or a
successful response.

Looking up Account Details on Horizon
=====================================

Basic Information
-----------------
Once you have the account, you might want to look up its information from
Horizon to verify the network knows about your new account:

.. code-block:: python

   from stellar_base.address import Address
   publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
   address = Address(address=publickey) # See signature for additional args
   address.get() # Get the latest information from Horizon

You can now retrieve information for the account's

    * Sequence Number
    * Balances
    * Paging Token
    * Thresholds
    * Flags
    * Signers
    * Data

Like so:

.. code-block:: python

   print('Balances: {}'.format(address.balances))
   print('Sequence Number: {}'.format(address.sequence))
   print('Flags: {}'.format(address.flags))
   print('Signers: {}'.format(address.signers))
   print('Data: {}'.format(address.data))


Most Recent Payments
--------------------
We can check the most recent payments by:

.. code-block:: python

   payments = address.payments()

Like many Horizon endpoints, payments is `paginated
<https://www.stellar.org/developers/horizon/reference/paging.html>`_. You can
get different payments by using the following query parameters: limit, order,
and cursor.

So if you need to check payments after a specific cursor, try:

.. code-block:: python

   address.payments(cursor='4225135422738433', limit=20, order='asc')

You can also use `server sent events
<https://www.stellar.org/developers/horizon/reference/responses.html#streaming>`_
if you want to by passing in sse=True on methods that have sse in their
signature.

.. code-block:: python

   address.payments(sse=True)

Other Account Attributes
------------------------
Just like payments, there are plenty of other account attributes you can look
up via Horizon:

.. code-block:: python

   address.transactions()
   address.effects()
   address.offers()
   address.operations()

Look at the `Horizon API reference
<https://www.stellar.org/developers/horizon/reference/index.html>`_ for which
endpoints support SSE.

Building A Transaction
======================

When we created an account, we already created a transaction.
We can build a transaction with a :class:`Builder
<stellar_base.builder.Builder>`, or with a :class:`Transaction
<stellar_base.transaction.Transaction>` object by itself. We recommend you use
the builder, as it handles a lot of the details for you, and you can focus on
the important parameters in each method's signature.

Using a Builder
---------------

Let's send Bob a payment that we owe him. We'd go about this in the following
way:

.. code-block:: python

   from stellar_base.builder import Builder
   seed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
   builder = Builder(secret=seed)
   # builder = Builder(secret=seed, network='public') for LIVENET

   bob_address = 'GABRGTDZEDCQ5W663U2EI5KWRSU3EAWJCSI57H7XAMUO5BQRIGNNZGTY'
   builder.append_payment_op(bob_address, '100', 'XLM')
   builder.add_text_memo('For beers') # string length <= 28 bytes
   builder.sign()

   # Uses an internal horizon instance to submit over the network
   builder.submit()

Or if you want to pay him with CNY:

.. code-block:: python

   # This is a stellar issuing account ID for an anchor that issues CNY
   CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
   builder.append_payment_op(bob_address, '10', 'CNY', CNY_ISSUER)
   builder.add_text_memo('For beers') # string length <= 28 bytes
   builder.sign()

   # Uses an internal horizon instance to submit over the network
   builder.submit()

And that's it!

Sometimes, we work with multi-signature transactions that require your
signature in addition to the the account that originally sealed the transaction
in an envelope. Typically you'll get an XDR string that you need to sign. To do
this, you use :meth:`import_from_xdr
<stellar_base.builder.Builder.import_from_xdr>` to import it into your builder.

.. code-block:: python

   # This is the transaction that you need to add your signature to
   xdr_string = 'AAAAAAMTTHkgxQ7b3t00RHVWjKmyAskUkd+f9wMo7oYRQZrcAAAAZAAAAIHlSBzvAAAAAAAAAAAAAAABAAAAAAAAAAoAAAAFaGVsbG8AAAAAAAABAAAAB3N0ZWxsYXIAAAAAAAAAAAA='
   builder = Builder(secret=seed)
   builder.import_from_xdr(xdr_string)
   builder.sign()
   xdr_string = builder.gen_xdr()

From here you can pass along your XDR string to anyone else who needs to sign
it, or you can submit it via `builder.submit()` if you're the last to sign.

Using a Transaction Object
--------------------------

Here is a full example of how to make a Transaction from scratch. As you can
see, it requires a lot more imports and knowledge of internal objects, but it
gives you the most flexibility before submitting your transaction over the
wire.

In this example, Alice is sending Bob 100 CNY.

.. code-block:: python

   from stellar_base.keypair import Keypair
   from stellar_base.asset import Asset
   from stellar_base.operation import Payment
   from stellar_base.transaction import Transaction
   from stellar_base.transaction_envelope import TransactionEnvelope as Te
   from stellar_base.memo import TextMemo
   from stellar_base.horizon import horizon_testnet, horizon_livenet

   # Generate Alice's Keypair for ultimately signing and setting as the source
   alice_seed = 'SAZJ3EDATROKTNNN4WZBZPRC34AN5WR43VEHAFKT5D66UEZTKDNKUHOK'
   alice_kp = Keypair.from_seed(alice_seed)

   # Bob's address, for the destination
   bob_address = 'GDLP3SP4WP72L4BAJWZUDZ6SAYE4NAWILT5WQDS7RWC4XCUNUQDRB2A4'

   # The CNY Issuer's address
   CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'

   horizon = horizon_testnet()
   # horizon = horizon_livenet() for LIVENET

   # create op
   amount = '100'
   asset = Asset('CNY', CNY_ISSUER)
   op = Payment(
       # Source is also inferred from the transaction source, so it's optional.
       source=alice_kp.address().decode(),
       destination=bob_address,
       asset=asset,
       amount=amount
   )
   # create a memo
   msg = TextMemo('For beers yesterday!')

   # Get the current sequence of Alice
   # Python 3
   sequence = horizon.account(alice_kp.address().decode('utf-8')).get('sequence')
   # Python 2
   # sequence = horizon.account(alice_kp.address()).get('sequence')

   # Construct a transaction
   tx = Transaction(
       source=alice_kp.address().decode(),
       sequence=sequence,
       # time_bounds = {'minTime': 1531000000, 'maxTime': 1531234600},
       memo=msg,
       fee=100, # Can specify a fee or use the default by not specifying it
       operations=[
           op,
       ],
   )



   # Build transaction envelope
   envelope = Te(tx=tx, network_id="TESTNET") # or 'PUBLIC'

   # Sign the envelope
   envelope.sign(alice_kp)

   # Submit the transaction to Horizon!
   xdr = envelope.xdr()
   response = horizon.submit(xdr)

What's Next
===========

From here, we recommend you explore our :ref:`api`. In there you'll find out
more about the various objects that represent concepts in Stellar, as well as
some of the additional helper classes and functions that exist.

Happy Coding!
