.. _api:

*****************
API Documentation
*****************


.. module:: stellar_sdk


Account
^^^^^^^^

.. autoclass:: stellar_sdk.account.Account
   :members:
   :inherited-members:

Asset
^^^^^

.. autoclass:: stellar_sdk.asset.Asset
   :members:
   :inherited-members:

Keypair
^^^^^^^

.. autoclass:: stellar_sdk.keypair.Keypair
   :members:
   :inherited-members:

Memo
^^^^

Memo
----

.. autoclass:: stellar_sdk.memo.Memo
   :members:

NoneMemo
--------
.. autoclass:: stellar_sdk.memo.NoneMemo
   :members:

TextMemo
--------
.. autoclass:: stellar_sdk.memo.TextMemo
   :members:

IdMemo
------
.. autoclass:: stellar_sdk.memo.IdMemo
   :members:

HashMemo
--------
.. autoclass:: stellar_sdk.memo.HashMemo
   :members:

ReturnHashMemo
--------------
.. autoclass:: stellar_sdk.memo.ReturnHashMemo
   :members:

Network
^^^^^^^

.. autoclass:: stellar_sdk.network.Network
   :members:
   :inherited-members:

Operation
^^^^^^^^^

Operation
---------
.. autoclass:: stellar_sdk.operation.Operation
   :members:
   :inherited-members:

AccountMerge
------------
.. autoclass:: stellar_sdk.operation.AccountMerge
   :members: to_xdr_object, from_xdr_object

AllowTrust
----------
.. autoclass:: stellar_sdk.operation.AllowTrust
   :members: to_xdr_object, from_xdr_object

BumpSequence
------------
.. autoclass:: stellar_sdk.operation.BumpSequence
   :members: to_xdr_object, from_xdr_object

ChangeTrust
-----------
.. autoclass:: stellar_sdk.operation.ChangeTrust
   :members: to_xdr_object, from_xdr_object

CreateAccount
-------------
.. autoclass:: stellar_sdk.operation.CreateAccount
   :members: to_xdr_object, from_xdr_object

CreatePassiveSellOffer
----------------------
.. autoclass:: stellar_sdk.operation.CreatePassiveSellOffer
   :members: to_xdr_object, from_xdr_object

Inflation
---------
.. autoclass:: stellar_sdk.operation.Inflation
   :members: to_xdr_object, from_xdr_object

ManageBuyOffer
--------------
.. autoclass:: stellar_sdk.operation.ManageBuyOffer
   :members: to_xdr_object, from_xdr_object

ManageData
----------
.. autoclass:: stellar_sdk.operation.ManageData
   :members: to_xdr_object, from_xdr_object

ManageSellOffer
---------------
.. autoclass:: stellar_sdk.operation.ManageSellOffer
   :members: to_xdr_object, from_xdr_object

PathPayment
-----------
.. autoclass:: stellar_sdk.operation.PathPayment
   :members: to_xdr_object, from_xdr_object

Payment
-------
.. autoclass:: stellar_sdk.operation.Payment
   :members: to_xdr_object, from_xdr_object

SetOptions
----------
.. autoclass:: stellar_sdk.operation.SetOptions
   :members: to_xdr_object, from_xdr_object

Price
^^^^^

.. autoclass:: stellar_sdk.price.Price
   :members:
   :inherited-members:

Signer
^^^^^^^^^^

.. autoclass:: stellar_sdk.signer.Signer
   :members:
   :inherited-members:

TimeBounds
^^^^^^^^^^

.. autoclass:: stellar_sdk.time_bounds.TimeBounds
   :members:
   :inherited-members: