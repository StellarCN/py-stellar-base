.. _api:

API Documentation
=================

.. module:: stellar_base

Asset
-----

.. autoclass:: stellar_base.asset.Asset
   :members:

Keypair
-------

.. autoclass:: stellar_base.keypair.Keypair
   :members:

Memo
----

.. autoclass:: stellar_base.memo.Memo
   :members:

.. autoclass:: stellar_base.memo.NoneMemo
   :members:
   :inherited-members:

.. autoclass:: stellar_base.memo.TextMemo
   :members:
   :inherited-members:

.. autoclass:: stellar_base.memo.IdMemo
   :members:
   :inherited-members:

.. autoclass:: stellar_base.memo.HashMemo
   :members:
   :inherited-members:

.. autoclass:: stellar_base.memo.RetHashMemo
   :members:
   :inherited-members:

Operation
---------

.. autoclass:: stellar_base.operation.Operation
   :members:
   :inherited-members:

Transaction
-----------

.. autoclass:: stellar_base.transaction.Transaction
   :members:
   :inherited-members:

List of Operations
------------------

Create Account
^^^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.CreateAccount
   :members:

Payment
^^^^^^^

.. autoclass:: stellar_base.operation.Payment
   :members:

Path Payment
^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.PathPayment
   :members:

Manage Offer
^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.ManageOffer
   :members:

Create Passive Offer
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.CreatePassiveOffer
   :members:

Set Options
^^^^^^^^^^^

.. autoclass:: stellar_base.operation.SetOptions
   :members:

Change Trust
^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.ChangeTrust
   :members:

Allow Trust
^^^^^^^^^^^

.. autoclass:: stellar_base.operation.AllowTrust
   :members:

Account Merge
^^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.AccountMerge
   :members:

Inflation
^^^^^^^^^

.. autoclass:: stellar_base.operation.Inflation
   :members:

Manage Data
^^^^^^^^^^^

.. autoclass:: stellar_base.operation.ManageData
   :members:
