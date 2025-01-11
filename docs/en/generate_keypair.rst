.. _generate_keypair:


****************
Generate Keypair
****************

The :py:class:`Keypair <stellar_sdk.keypair.Keypair>` object represents a key pair used to
sign transactions in a Stellar network. The :py:class:`Keypair <stellar_sdk.keypair.Keypair>`
object can contain both a public and a private key, or only a public key.

If a :py:class:`Keypair <stellar_sdk.keypair.Keypair>` object does not contain a private
key it can't be used to sign transactions. The most convenient method of
creating a new keypair is by passing the account's secret seed:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   secret = "SBK2VIYYSVG76E7VC3QHYARNFLY2EAQXDHRC7BMXBBGIFG74ARPRMNQM"
   keypair = Keypair.from_secret(secret)

   # GDHMW6QZOL73SHKG2JA3YHXFDHM46SS5ZRWEYF5BCYHX2C5TVO6KZBYL
   public_key = keypair.public_key

   can_sign = keypair.can_sign()  # True


You can create a keypair from public key, but its function is limited:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   public_key = "GDHMW6QZOL73SHKG2JA3YHXFDHM46SS5ZRWEYF5BCYHX2C5TVO6KZBYL"
   keypair = Keypair.from_public_key(public_key)
   can_sign = keypair.can_sign()  # False

You can create a randomly generated keypair:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   keypair = Keypair.random()
   print("Public Key: " + keypair.public_key)
   print("Secret Seed: " + keypair.secret)

Vou can also generate a mnemonic phrase and later use it to generate a keypair:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   mnemonic_phrase = Keypair.generate_mnemonic_phrase()
   print(f"Mnemonic phrase: {mnemonic_phrase}")
   keypair = Keypair.from_mnemonic_phrase(mnemonic_phrase)
   print(f"Public Key: {keypair.public_key}")
   print(f"Secret Seed: {keypair.secret}")

Lastly, you can also use the Shamir secret sharing method to split a mnemonic
phrase into multiple phrases. In the following example, we need exactly 2
phrases in order to reconstruct the secret:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   mnemonic_phrases = Keypair.generate_shamir_mnemonic_phrases(member_threshold=2, member_count=3)
   print(f"Mnemonic phrases: {mnemonic_phrases}")
   keypair = Keypair.from_shamir_mnemonic_phrases(mnemonic_phrases[:2])  # any combinations
   print(f"Public Key: {keypair.public_key}")
   print(f"Secret Seed: {keypair.secret}")

If you want to convert an existing mnemonic phrase to Shamir, you need to get
the corresponding entropy. You can use these lower level functions:

.. code-block:: python
   :linenos:

   import shamir_mnemonic
   from stellar_sdk.sep.mnemonic import StellarMnemonic

   seed_raw = StellarMnemonic("english").to_entropy(mnemonic)
   mnemonic_phrases = shamir_mnemonic.generate_mnemonics(
       group_threshold=1,
       groups=[(2, 3)],
       master_secret=seed_raw,
       passphrase=passphrase.encode(),
   )[0]
   print(f"Mnemonic phrases: {mnemonic_phrases}")
