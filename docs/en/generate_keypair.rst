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

You can also create a randomly generated keypair:

.. code-block:: python
   :linenos:

   from stellar_sdk import Keypair

   keypair = Keypair.random()
   print("Public Key: " + keypair.public_key)
   print("Secret Seed: " + keypair.secret)