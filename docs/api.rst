.. _api:

*****************
API Documentation
*****************


Classes
=======

.. module:: stellar_base

Address
-------

.. autoclass:: stellar_base.address.Address
   :members:
   :inherited-members:

Asset
-----

.. autoclass:: stellar_base.asset.Asset
   :members:
   :inherited-members:

Builder
-------

.. autoclass:: stellar_base.builder.Builder
   :members:
   :inherited-members:

Keypair
-------

.. autoclass:: stellar_base.keypair.Keypair
   :members:
   :inherited-members:

Memo
----

.. autoclass:: stellar_base.memo.Memo
   :members:

.. autoclass:: stellar_base.memo.NoneMemo
   :members:

.. autoclass:: stellar_base.memo.TextMemo
   :members:

.. autoclass:: stellar_base.memo.IdMemo
   :members:

.. autoclass:: stellar_base.memo.HashMemo
   :members:

.. autoclass:: stellar_base.memo.RetHashMemo
   :members:

Network
-------

.. automodule:: stellar_base.network
   :members:

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

TransactionEnvelope
-------------------

.. autoclass:: stellar_base.transaction_envelope.TransactionEnvelope
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

Bump Sequence
^^^^^^^^^^^^^

.. autoclass:: stellar_base.operation.BumpSequence
   :members:

List of Exceptions
------------------

StellarError
^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.StellarError
   :members:

BadSignatureError
^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.BadSignatureError
   :members:

AssetCodeInvalidError
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.AssetCodeInvalidError
   :members:

StellarAddressInvalidError
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.StellarAddressInvalidError
   :members:


StellarSecretInvalidError
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.StellarSecretInvalidError
   :members:

NoStellarSecretOrAddressError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.NoStellarSecretOrAddressError
   :members:

SequenceError
^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.SequenceError
   :members:

ConfigurationError
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.ConfigurationError
   :members:

NoApproximationError
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.NoApproximationError
   :members:

HorizonError
^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.HorizonError
   :members:

HorizonRequestError
^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.HorizonRequestError
   :members:


SignatureExistError
^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.SignatureExistError
   :members:

DecodeError
^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.DecodeError
   :members:

NotValidParamError
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.NotValidParamError
   :members:

MnemonicError
^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.MnemonicError
   :members:

MissingSigningKeyError
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_base.exceptions.MissingSigningKeyError
   :members:

FederationError
^^^^^^^^^^^^^^^
.. autoclass:: stellar_base.exceptions.FederationError
   :members:


Federation
==========

.. automodule:: stellar_base.federation
   :members:

Horizon
=======

.. autoclass:: stellar_base.horizon.Horizon
   :members:
   :inherited-members:

.. autofunction:: stellar_base.horizon.horizon_testnet

.. autofunction:: stellar_base.horizon.horizon_livenet
