.. _api:

*****************
API 文档
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

Call Builder
^^^^^^^^^^^^

BaseCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.BaseCallBuilder
   :members:
   :inherited-members:

AccountsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.AccountsCallBuilder
   :members:
   :inherited-members:

AssetsCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.AssetsCallBuilder
   :members:
   :inherited-members:

EffectsCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.EffectsCallBuilder
   :members:
   :inherited-members:

FeeStatsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.FeeStatsCallBuilder
   :members:
   :inherited-members:

LedgersCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.LedgersCallBuilder
   :members:
   :inherited-members:

OffersCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.OffersCallBuilder
   :members:
   :inherited-members:

OperationsCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.OperationsCallBuilder
   :members:
   :inherited-members:

OrderbookCallBuilder
--------------------
.. autoclass:: stellar_sdk.call_builder.OrderbookCallBuilder
   :members:
   :inherited-members:

PathsCallBuilder
----------------
.. autoclass:: stellar_sdk.call_builder.PathsCallBuilder
   :members:
   :inherited-members:

PaymentsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.PaymentsCallBuilder
   :members:
   :inherited-members:

RootCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.RootCallBuilder
   :members:
   :inherited-members:

StrictReceivePathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.StrictReceivePathsCallBuilder
   :members:
   :inherited-members:

StrictSendPathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.StrictSendPathsCallBuilder
   :members:
   :inherited-members:

TradeAggregationsCallBuilder
----------------------------
.. autoclass:: stellar_sdk.call_builder.TradeAggregationsCallBuilder
   :members:
   :inherited-members:

TradesCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.TradesCallBuilder
   :members:
   :inherited-members:

TransactionsCallBuilder
-----------------------
.. autoclass:: stellar_sdk.call_builder.TransactionsCallBuilder
   :members:
   :inherited-members:

Client
^^^^^^

BaseAsyncClient
---------------

.. autoclass:: stellar_sdk.client.base_async_client.BaseAsyncClient
   :members:

BaseSyncClient
---------------

.. autoclass:: stellar_sdk.client.base_sync_client.BaseSyncClient
   :members:

AiohttpClient
--------------

.. autoclass:: stellar_sdk.client.aiohttp_client.AiohttpClient
   :members:

RequestsClient
--------------

.. autoclass:: stellar_sdk.client.requests_client.RequestsClient
   :members:

SimpleRequestsClient
--------------------

.. autoclass:: stellar_sdk.client.simple_requests_client.SimpleRequestsClient
   :members:

Response
--------

.. autoclass:: stellar_sdk.client.response.Response
   :members:



Exceptions
^^^^^^^^^^

SdkError
--------

.. autoclass:: stellar_sdk.exceptions.SdkError
   :members:

ValueError
----------

.. autoclass:: stellar_sdk.exceptions.ValueError
   :members:

TypeError
---------

.. autoclass:: stellar_sdk.exceptions.TypeError
   :members:

BadSignatureError
-----------------

.. autoclass:: stellar_sdk.exceptions.BadSignatureError
   :members:

Ed25519PublicKeyInvalidError
----------------------------

.. autoclass:: stellar_sdk.exceptions.Ed25519PublicKeyInvalidError
   :members:

Ed25519SecretSeedInvalidError
-----------------------------

.. autoclass:: stellar_sdk.exceptions.Ed25519SecretSeedInvalidError
   :members:

MissingEd25519SecretSeedError
-----------------------------

.. autoclass:: stellar_sdk.exceptions.MissingEd25519SecretSeedError
   :members:

MemoInvalidException
--------------------

.. autoclass:: stellar_sdk.exceptions.MemoInvalidException
   :members:

AssetCodeInvalidError
---------------------

.. autoclass:: stellar_sdk.exceptions.AssetCodeInvalidError
   :members:

AssetIssuerInvalidError
-----------------------

.. autoclass:: stellar_sdk.exceptions.AssetIssuerInvalidError
   :members:

NoApproximationError
--------------------

.. autoclass:: stellar_sdk.exceptions.NoApproximationError
   :members:

SignatureExistError
-------------------

.. autoclass:: stellar_sdk.exceptions.SignatureExistError
   :members:

BaseRequestError
----------------

.. autoclass:: stellar_sdk.exceptions.BaseRequestError
   :members:

ConnectionError
---------------

.. autoclass:: stellar_sdk.exceptions.ConnectionError
   :members:

BaseHorizonError
----------------

.. autoclass:: stellar_sdk.exceptions.BaseHorizonError
   :members:

NotFoundError
-------------

.. autoclass:: stellar_sdk.exceptions.NotFoundError
   :members:

BadRequestError
---------------

.. autoclass:: stellar_sdk.exceptions.BadRequestError
   :members:

BadResponseError
----------------

.. autoclass:: stellar_sdk.exceptions.BadResponseError
   :members:

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

.. _operation_list_archor:

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

PathPaymentStrictReceive
------------------------
.. autoclass:: stellar_sdk.operation.PathPaymentStrictReceive
   :members: to_xdr_object, from_xdr_object

PathPaymentStrictSend
---------------------
.. autoclass:: stellar_sdk.operation.PathPaymentStrictSend
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

Server
^^^^^^

.. autoclass:: stellar_sdk.server.Server
   :members:
   :inherited-members:

Signer
^^^^^^

.. autoclass:: stellar_sdk.signer.Signer
   :members:
   :inherited-members:

TimeBounds
^^^^^^^^^^

.. autoclass:: stellar_sdk.time_bounds.TimeBounds
   :members:
   :inherited-members:

Transaction
^^^^^^^^^^^

.. autoclass:: stellar_sdk.transaction.Transaction
   :members:

TransactionEnvelope
^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.transaction_envelope.TransactionEnvelope
   :members:

TransactionBuilder
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.transaction_builder.TransactionBuilder
   :members:

Stellar Ecosystem Proposals
^^^^^^^^^^^^^^^^^^^^^^^^^^^
SEP 0001: stellar.toml
----------------------
.. autofunction:: stellar_sdk.sep.stellar_toml.fetch_stellar_toml

SEP 0002: Federation protocol
----------------------
.. autofunction:: stellar_sdk.sep.federation.resolve_stellar_address
.. autofunction:: stellar_sdk.sep.federation.resolve_account_id
.. autoclass:: stellar_sdk.sep.federation.FederationRecord
   :members:

SEP 0005: Key Derivation Methods for Stellar Accounts
-----------------------------------------------------
.. autoclass:: stellar_sdk.sep.mnemonic.StellarMnemonic
   :members:
.. autoclass:: stellar_sdk.sep.mnemonic.Language
   :members:
   :undoc-members:

SEP 0010: Stellar Web Authentication
------------------------------------
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction

Exceptions
----------
.. autoclass:: stellar_sdk.sep.exceptions.StellarTomlNotFoundError
.. autoclass:: stellar_sdk.sep.exceptions.InvalidSep10ChallengeError
