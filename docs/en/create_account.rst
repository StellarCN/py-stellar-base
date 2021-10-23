.. _create_account:


**************
Create Account
**************

Now, in order to create an account, you need to run a :py:class:`CreateAccount
<stellar_sdk.operation.CreateAccount>` operation with your new account ID.
Due to `Stellar's minimum account balance
<https://developers.stellar.org/docs/glossary/minimum-balance/>`_,
you'll need to transfer the minimum account balance from another account with
the create account operation. As of this writing, minimum balance is **1 XLM (2
x 0.5 Base Reserve)**, and is subject to change.

Using The SDF Testnet
=====================
If you want to play in the Stellar test network, you can ask our `Friendbot
<https://developers.stellar.org/docs/tutorials/create-account/>`_
to create an account for you as shown below:

.. literalinclude:: ../../examples/create_account_friendbot.py
   :language: python
   :linenos:

Using The Stellar Live Network
==============================
On the other hand, if you would like to create an account on the live network,
you should buy some Stellar Lumens from an exchange. When you withdraw the
Lumens into your new account, the exchange will automatically create the
account for you. However, if you want to create an account from another
account of your own, here's an example of how to do so:


.. literalinclude:: ../../examples/create_account.py
   :language: python
   :linenos:


Note: To avoid risks, TESTNET is used in the example above. In order to use the
Stellar Live Network you will have to change the network passphrase to
Network.PUBLIC_NETWORK_PASSPHRASE and the server URL to point to
https://horizon.stellar.org too.
