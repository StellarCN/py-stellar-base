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

AccountsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.AccountsCallBuilder
   :members:
   :inherited-members:

AssetsCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.AssetsCallBuilder
   :members:
   :inherited-members:

ClaimableBalancesCallBuilder
----------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.ClaimableBalancesCallBuilder
   :members:
   :inherited-members:

DataCallBuilder
---------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.DataCallBuilder
   :members:
   :inherited-members:

EffectsCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.EffectsCallBuilder
   :members:
   :inherited-members:

FeeStatsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.FeeStatsCallBuilder
   :members:
   :inherited-members:

LedgersCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.LedgersCallBuilder
   :members:
   :inherited-members:

LiquidityPoolsBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.LiquidityPoolsBuilder
   :members:
   :inherited-members:

OffersCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.OffersCallBuilder
   :members:
   :inherited-members:

OperationsCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.OperationsCallBuilder
   :members:
   :inherited-members:

OrderbookCallBuilder
--------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.OrderbookCallBuilder
   :members:
   :inherited-members:

PaymentsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.PaymentsCallBuilder
   :members:
   :inherited-members:

RootCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.RootCallBuilder
   :members:
   :inherited-members:

StrictReceivePathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.StrictReceivePathsCallBuilder
   :members:
   :inherited-members:

StrictSendPathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.StrictSendPathsCallBuilder
   :members:
   :inherited-members:

TradeAggregationsCallBuilder
----------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.TradeAggregationsCallBuilder
   :members:
   :inherited-members:

TradesCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.TradesCallBuilder
   :members:
   :inherited-members:

TransactionsCallBuilder
-----------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_sync.TransactionsCallBuilder
   :members:
   :inherited-members:

Call Builder Async
^^^^^^^^^^^^^^^^^^

AccountsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.AccountsCallBuilder
   :members:
   :inherited-members:

AssetsCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.AssetsCallBuilder
   :members:
   :inherited-members:

ClaimableBalancesCallBuilder
----------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.ClaimableBalancesCallBuilder
   :members:
   :inherited-members:

DataCallBuilder
---------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.DataCallBuilder
   :members:
   :inherited-members:

EffectsCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.EffectsCallBuilder
   :members:
   :inherited-members:

FeeStatsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.FeeStatsCallBuilder
   :members:
   :inherited-members:

LedgersCallBuilder
------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.LedgersCallBuilder
   :members:
   :inherited-members:

LiquidityPoolsBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.LiquidityPoolsBuilder
   :members:
   :inherited-members:

OffersCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.OffersCallBuilder
   :members:
   :inherited-members:

OperationsCallBuilder
---------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.OperationsCallBuilder
   :members:
   :inherited-members:

OrderbookCallBuilder
--------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.OrderbookCallBuilder
   :members:
   :inherited-members:

PaymentsCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.PaymentsCallBuilder
   :members:
   :inherited-members:

RootCallBuilder
-------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.RootCallBuilder
   :members:
   :inherited-members:

StrictReceivePathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.StrictReceivePathsCallBuilder
   :members:
   :inherited-members:

StrictSendPathsCallBuilder
------------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.StrictSendPathsCallBuilder
   :members:
   :inherited-members:

TradeAggregationsCallBuilder
----------------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.TradeAggregationsCallBuilder
   :members:
   :inherited-members:

TradesCallBuilder
-----------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.TradesCallBuilder
   :members:
   :inherited-members:

TransactionsCallBuilder
-----------------------
.. autoclass:: stellar_sdk.call_builder.call_builder_async.TransactionsCallBuilder
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

FeatureNotEnabledError
----------------------

.. autoclass:: stellar_sdk.exceptions.FeatureNotEnabledError
   :members:

Keypair
^^^^^^^

.. autoclass:: stellar_sdk.keypair.Keypair
   :members:
   :inherited-members:

LiquidityPoolAsset
^^^^^^^^^^^^^^^^^^
.. autodata:: stellar_sdk.liquidity_pool_asset.LIQUIDITY_POOL_FEE_V18
.. autoclass:: stellar_sdk.liquidity_pool_asset.LiquidityPoolAsset
   :members:

LiquidityPoolId
^^^^^^^^^^^^^^^
.. autoclass:: stellar_sdk.liquidity_pool_id.LiquidityPoolId
   :members:

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

MuxedAccount
^^^^^^^^^^^^

.. autoclass:: stellar_sdk.muxed_account.MuxedAccount
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

.. autoclass:: stellar_sdk.operation.allow_trust.TrustLineEntryFlag
   :members:

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

LiquidityPoolDeposit
--------------------
.. autoclass:: stellar_sdk.operation.LiquidityPoolDeposit
   :members: to_xdr_object, from_xdr_object

LiquidityPoolWithdraw
---------------------
.. autoclass:: stellar_sdk.operation.LiquidityPoolWithdraw
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

.. autoclass:: stellar_sdk.operation.set_options.AuthorizationFlag
   :members:

CreateClaimableBalance
----------------------
.. autoclass:: stellar_sdk.operation.CreateClaimableBalance
   :members: to_xdr_object, from_xdr_object

.. autoclass:: stellar_sdk.operation.Claimant
   :members:

.. autoclass:: stellar_sdk.operation.ClaimPredicate
   :members:

.. autoclass:: stellar_sdk.operation.create_claimable_balance.ClaimPredicateType
   :members:

.. autoclass:: stellar_sdk.operation.create_claimable_balance.ClaimPredicateGroup
   :members:

ClaimClaimableBalance
---------------------
.. autoclass:: stellar_sdk.operation.ClaimClaimableBalance
   :members: to_xdr_object, from_xdr_object

BeginSponsoringFutureReserves
-----------------------------
.. autoclass:: stellar_sdk.operation.BeginSponsoringFutureReserves
   :members: to_xdr_object, from_xdr_object

EndSponsoringFutureReserves
---------------------------
.. autoclass:: stellar_sdk.operation.EndSponsoringFutureReserves
   :members: to_xdr_object, from_xdr_object

RevokeSponsorship
-----------------
.. autoclass:: stellar_sdk.operation.RevokeSponsorship
   :members: to_xdr_object, from_xdr_object

.. autoclass:: stellar_sdk.operation.revoke_sponsorship.RevokeSponsorshipType
   :members:

.. autoclass:: stellar_sdk.operation.revoke_sponsorship.TrustLine
   :members:

.. autoclass:: stellar_sdk.operation.revoke_sponsorship.Offer
   :members:

.. autoclass:: stellar_sdk.operation.revoke_sponsorship.Data
   :members:

.. autoclass:: stellar_sdk.operation.revoke_sponsorship.Signer
   :members:

Clawback
--------
.. autoclass:: stellar_sdk.operation.Clawback
   :members: to_xdr_object, from_xdr_object

ClawbackClaimableBalance
------------------------
.. autoclass:: stellar_sdk.operation.ClawbackClaimableBalance
   :members: to_xdr_object, from_xdr_object

SetTrustLineFlags
-----------------
.. autoclass:: stellar_sdk.operation.SetTrustLineFlags
   :members: to_xdr_object, from_xdr_object

.. autoclass:: stellar_sdk.operation.set_trust_line_flags.TrustLineFlags
   :members:

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

ServerAsync
^^^^^^^^^^^

.. autoclass:: stellar_sdk.server_async.ServerAsync
   :members:
   :inherited-members:

Signer
^^^^^^

.. autoclass:: stellar_sdk.signer.Signer
   :members:
   :inherited-members:

SignerKey
^^^^^^^^^

.. autoclass:: stellar_sdk.signer_key.SignerKey
   :members:
   :inherited-members:

.. autoclass:: stellar_sdk.signer_key.SignerKeyType
   :members:

StrKey
^^^^^^

.. autoclass:: stellar_sdk.strkey.StrKey
   :members:
   :inherited-members:

TimeBounds
^^^^^^^^^^

.. autoclass:: stellar_sdk.time_bounds.TimeBounds
   :members:
   :inherited-members:

DecoratedSignature
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.decorated_signature.DecoratedSignature
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
   :inherited-members:

FeeBumpTransaction
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.fee_bump_transaction.FeeBumpTransaction
   :members:
   :inherited-members:

FeeBumpTransactionEnvelope
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope
   :members:
   :inherited-members:

TransactionBuilder
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.transaction_builder.TransactionBuilder
   :members:

Helpers
^^^^^^^
.. autofunction:: stellar_sdk.helpers.parse_transaction_envelope_from_xdr

XDR Utils
^^^^^^^^^
.. autofunction:: stellar_sdk.xdr.utils.from_xdr_amount
.. autofunction:: stellar_sdk.xdr.utils.to_xdr_amount

Stellar Ecosystem Proposals
^^^^^^^^^^^^^^^^^^^^^^^^^^^
SEP 0001: stellar.toml
----------------------
.. autofunction:: stellar_sdk.sep.stellar_toml.fetch_stellar_toml
.. autofunction:: stellar_sdk.sep.stellar_toml.fetch_stellar_toml_async

SEP 0002: Federation protocol
-----------------------------
.. autofunction:: stellar_sdk.sep.federation.resolve_stellar_address
.. autofunction:: stellar_sdk.sep.federation.resolve_stellar_address_async
.. autofunction:: stellar_sdk.sep.federation.resolve_account_id_async
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

SEP 0007: URI Scheme to facilitate delegated signing
-----------------------------------------------------
.. autoclass:: stellar_sdk.sep.stellar_uri.PayStellarUri
   :members:
   :inherited-members:
.. autoclass:: stellar_sdk.sep.stellar_uri.TransactionStellarUri
   :members:
   :inherited-members:
.. autoclass:: stellar_sdk.sep.stellar_uri.Replacement
   :members:
   :inherited-members:

SEP 0010: Stellar Web Authentication
------------------------------------
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers
.. autofunction:: stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction
.. autoclass:: stellar_sdk.sep.stellar_web_authentication.ChallengeTransaction
   :members:

SEP 0011: Txrep: human-readable low-level representation of Stellar transactions
---------------------------------------------------------------------------------
.. autofunction:: stellar_sdk.sep.txrep.to_txrep
.. autofunction:: stellar_sdk.sep.txrep.from_txrep

Exceptions
----------
.. autoclass:: stellar_sdk.sep.exceptions.StellarTomlNotFoundError
.. autoclass:: stellar_sdk.sep.exceptions.InvalidFederationAddress
.. autoclass:: stellar_sdk.sep.exceptions.FederationServerNotFoundError
.. autoclass:: stellar_sdk.sep.exceptions.BadFederationResponseError
.. autoclass:: stellar_sdk.sep.exceptions.InvalidSep10ChallengeError
.. autoclass:: stellar_sdk.sep.exceptions.AccountRequiresMemoError

.. _stellar_sdk_xdr:

stellar_sdk.xdr
^^^^^^^^^^^^^^^

AccountEntry
------------
.. autoclass:: stellar_sdk.xdr.account_entry.AccountEntry

AccountEntryExt
---------------
.. autoclass:: stellar_sdk.xdr.account_entry_ext.AccountEntryExt

AccountEntryExtensionV1
-----------------------
.. autoclass:: stellar_sdk.xdr.account_entry_extension_v1.AccountEntryExtensionV1

AccountEntryExtensionV1Ext
--------------------------
.. autoclass:: stellar_sdk.xdr.account_entry_extension_v1_ext.AccountEntryExtensionV1Ext

AccountEntryExtensionV2
-----------------------
.. autoclass:: stellar_sdk.xdr.account_entry_extension_v2.AccountEntryExtensionV2

AccountEntryExtensionV2Ext
--------------------------
.. autoclass:: stellar_sdk.xdr.account_entry_extension_v2_ext.AccountEntryExtensionV2Ext

AccountFlags
------------
.. autoclass:: stellar_sdk.xdr.account_flags.AccountFlags

AccountID
---------
.. autoclass:: stellar_sdk.xdr.account_id.AccountID

AccountMergeResult
------------------
.. autoclass:: stellar_sdk.xdr.account_merge_result.AccountMergeResult

AccountMergeResultCode
----------------------
.. autoclass:: stellar_sdk.xdr.account_merge_result_code.AccountMergeResultCode

AllowTrustOp
------------
.. autoclass:: stellar_sdk.xdr.allow_trust_op.AllowTrustOp

AllowTrustResult
----------------
.. autoclass:: stellar_sdk.xdr.allow_trust_result.AllowTrustResult

AllowTrustResultCode
--------------------
.. autoclass:: stellar_sdk.xdr.allow_trust_result_code.AllowTrustResultCode

AlphaNum12
----------
.. autoclass:: stellar_sdk.xdr.alpha_num12.AlphaNum12

AlphaNum4
---------
.. autoclass:: stellar_sdk.xdr.alpha_num4.AlphaNum4

Asset
-----
.. autoclass:: stellar_sdk.xdr.asset.Asset

AssetCode
---------
.. autoclass:: stellar_sdk.xdr.asset_code.AssetCode

AssetCode12
-----------
.. autoclass:: stellar_sdk.xdr.asset_code12.AssetCode12

AssetCode4
----------
.. autoclass:: stellar_sdk.xdr.asset_code4.AssetCode4

AssetType
---------
.. autoclass:: stellar_sdk.xdr.asset_type.AssetType

Auth
----
.. autoclass:: stellar_sdk.xdr.auth.Auth

AuthCert
--------
.. autoclass:: stellar_sdk.xdr.auth_cert.AuthCert

AuthenticatedMessage
--------------------
.. autoclass:: stellar_sdk.xdr.authenticated_message.AuthenticatedMessage

AuthenticatedMessageV0
----------------------
.. autoclass:: stellar_sdk.xdr.authenticated_message_v0.AuthenticatedMessageV0

BeginSponsoringFutureReservesOp
-------------------------------
.. autoclass:: stellar_sdk.xdr.begin_sponsoring_future_reserves_op.BeginSponsoringFutureReservesOp

BeginSponsoringFutureReservesResult
-----------------------------------
.. autoclass:: stellar_sdk.xdr.begin_sponsoring_future_reserves_result.BeginSponsoringFutureReservesResult

BeginSponsoringFutureReservesResultCode
---------------------------------------
.. autoclass:: stellar_sdk.xdr.begin_sponsoring_future_reserves_result_code.BeginSponsoringFutureReservesResultCode

Boolean
-------
.. autoclass:: stellar_sdk.xdr.base.Boolean

BucketEntry
-----------
.. autoclass:: stellar_sdk.xdr.bucket_entry.BucketEntry

BucketEntryType
---------------
.. autoclass:: stellar_sdk.xdr.bucket_entry_type.BucketEntryType

BucketMetadata
--------------
.. autoclass:: stellar_sdk.xdr.bucket_metadata.BucketMetadata

BucketMetadataExt
-----------------
.. autoclass:: stellar_sdk.xdr.bucket_metadata_ext.BucketMetadataExt

BumpSequenceOp
--------------
.. autoclass:: stellar_sdk.xdr.bump_sequence_op.BumpSequenceOp

BumpSequenceResult
------------------
.. autoclass:: stellar_sdk.xdr.bump_sequence_result.BumpSequenceResult

BumpSequenceResultCode
----------------------
.. autoclass:: stellar_sdk.xdr.bump_sequence_result_code.BumpSequenceResultCode

ChangeTrustAsset
----------------
.. autoclass:: stellar_sdk.xdr.change_trust_asset.ChangeTrustAsset

ChangeTrustOp
-------------
.. autoclass:: stellar_sdk.xdr.change_trust_op.ChangeTrustOp

ChangeTrustResult
-----------------
.. autoclass:: stellar_sdk.xdr.change_trust_result.ChangeTrustResult

ChangeTrustResultCode
---------------------
.. autoclass:: stellar_sdk.xdr.change_trust_result_code.ChangeTrustResultCode

ClaimAtom
---------
.. autoclass:: stellar_sdk.xdr.claim_atom.ClaimAtom

ClaimAtomType
-------------
.. autoclass:: stellar_sdk.xdr.claim_atom_type.ClaimAtomType

ClaimClaimableBalanceOp
-----------------------
.. autoclass:: stellar_sdk.xdr.claim_claimable_balance_op.ClaimClaimableBalanceOp

ClaimClaimableBalanceResult
---------------------------
.. autoclass:: stellar_sdk.xdr.claim_claimable_balance_result.ClaimClaimableBalanceResult

ClaimClaimableBalanceResultCode
-------------------------------
.. autoclass:: stellar_sdk.xdr.claim_claimable_balance_result_code.ClaimClaimableBalanceResultCode

ClaimLiquidityAtom
------------------
.. autoclass:: stellar_sdk.xdr.claim_liquidity_atom.ClaimLiquidityAtom

ClaimOfferAtom
--------------
.. autoclass:: stellar_sdk.xdr.claim_offer_atom.ClaimOfferAtom

ClaimOfferAtomV0
----------------
.. autoclass:: stellar_sdk.xdr.claim_offer_atom_v0.ClaimOfferAtomV0

ClaimPredicate
--------------
.. autoclass:: stellar_sdk.xdr.claim_predicate.ClaimPredicate

ClaimPredicateType
------------------
.. autoclass:: stellar_sdk.xdr.claim_predicate_type.ClaimPredicateType

ClaimableBalanceEntry
---------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_entry.ClaimableBalanceEntry

ClaimableBalanceEntryExt
------------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_entry_ext.ClaimableBalanceEntryExt

ClaimableBalanceEntryExtensionV1
--------------------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_entry_extension_v1.ClaimableBalanceEntryExtensionV1

ClaimableBalanceEntryExtensionV1Ext
-----------------------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_entry_extension_v1_ext.ClaimableBalanceEntryExtensionV1Ext

ClaimableBalanceFlags
---------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_flags.ClaimableBalanceFlags

ClaimableBalanceID
------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_id.ClaimableBalanceID

ClaimableBalanceIDType
----------------------
.. autoclass:: stellar_sdk.xdr.claimable_balance_id_type.ClaimableBalanceIDType

Claimant
--------
.. autoclass:: stellar_sdk.xdr.claimant.Claimant

ClaimantType
------------
.. autoclass:: stellar_sdk.xdr.claimant_type.ClaimantType

ClaimantV0
----------
.. autoclass:: stellar_sdk.xdr.claimant_v0.ClaimantV0

ClawbackClaimableBalanceOp
--------------------------
.. autoclass:: stellar_sdk.xdr.clawback_claimable_balance_op.ClawbackClaimableBalanceOp

ClawbackClaimableBalanceResult
------------------------------
.. autoclass:: stellar_sdk.xdr.clawback_claimable_balance_result.ClawbackClaimableBalanceResult

ClawbackClaimableBalanceResultCode
----------------------------------
.. autoclass:: stellar_sdk.xdr.clawback_claimable_balance_result_code.ClawbackClaimableBalanceResultCode

ClawbackOp
----------
.. autoclass:: stellar_sdk.xdr.clawback_op.ClawbackOp

ClawbackResult
--------------
.. autoclass:: stellar_sdk.xdr.clawback_result.ClawbackResult

ClawbackResultCode
------------------
.. autoclass:: stellar_sdk.xdr.clawback_result_code.ClawbackResultCode

CreateAccountOp
---------------
.. autoclass:: stellar_sdk.xdr.create_account_op.CreateAccountOp

CreateAccountResult
-------------------
.. autoclass:: stellar_sdk.xdr.create_account_result.CreateAccountResult

CreateAccountResultCode
-----------------------
.. autoclass:: stellar_sdk.xdr.create_account_result_code.CreateAccountResultCode

CreateClaimableBalanceOp
------------------------
.. autoclass:: stellar_sdk.xdr.create_claimable_balance_op.CreateClaimableBalanceOp

CreateClaimableBalanceResult
----------------------------
.. autoclass:: stellar_sdk.xdr.create_claimable_balance_result.CreateClaimableBalanceResult

CreateClaimableBalanceResultCode
--------------------------------
.. autoclass:: stellar_sdk.xdr.create_claimable_balance_result_code.CreateClaimableBalanceResultCode

CreatePassiveSellOfferOp
------------------------
.. autoclass:: stellar_sdk.xdr.create_passive_sell_offer_op.CreatePassiveSellOfferOp

CryptoKeyType
-------------
.. autoclass:: stellar_sdk.xdr.crypto_key_type.CryptoKeyType

Curve25519Public
----------------
.. autoclass:: stellar_sdk.xdr.curve25519_public.Curve25519Public

Curve25519Secret
----------------
.. autoclass:: stellar_sdk.xdr.curve25519_secret.Curve25519Secret

DataEntry
---------
.. autoclass:: stellar_sdk.xdr.data_entry.DataEntry

DataEntryExt
------------
.. autoclass:: stellar_sdk.xdr.data_entry_ext.DataEntryExt

DataValue
---------
.. autoclass:: stellar_sdk.xdr.data_value.DataValue

DecoratedSignature
------------------
.. autoclass:: stellar_sdk.xdr.decorated_signature.DecoratedSignature

DontHave
--------
.. autoclass:: stellar_sdk.xdr.dont_have.DontHave

EncryptedBody
-------------
.. autoclass:: stellar_sdk.xdr.encrypted_body.EncryptedBody

EndSponsoringFutureReservesResult
---------------------------------
.. autoclass:: stellar_sdk.xdr.end_sponsoring_future_reserves_result.EndSponsoringFutureReservesResult

EndSponsoringFutureReservesResultCode
-------------------------------------
.. autoclass:: stellar_sdk.xdr.end_sponsoring_future_reserves_result_code.EndSponsoringFutureReservesResultCode

EnvelopeType
------------
.. autoclass:: stellar_sdk.xdr.envelope_type.EnvelopeType

Error
-----
.. autoclass:: stellar_sdk.xdr.error.Error

ErrorCode
---------
.. autoclass:: stellar_sdk.xdr.error_code.ErrorCode

FeeBumpTransaction
------------------
.. autoclass:: stellar_sdk.xdr.fee_bump_transaction.FeeBumpTransaction

FeeBumpTransactionEnvelope
--------------------------
.. autoclass:: stellar_sdk.xdr.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope

FeeBumpTransactionExt
---------------------
.. autoclass:: stellar_sdk.xdr.fee_bump_transaction_ext.FeeBumpTransactionExt

FeeBumpTransactionInnerTx
-------------------------
.. autoclass:: stellar_sdk.xdr.fee_bump_transaction_inner_tx.FeeBumpTransactionInnerTx

Hash
----
.. autoclass:: stellar_sdk.xdr.hash.Hash

Hello
-----
.. autoclass:: stellar_sdk.xdr.hello.Hello

HmacSha256Key
-------------
.. autoclass:: stellar_sdk.xdr.hmac_sha256_key.HmacSha256Key

HmacSha256Mac
-------------
.. autoclass:: stellar_sdk.xdr.hmac_sha256_mac.HmacSha256Mac

Hyper
-----
.. autoclass:: stellar_sdk.xdr.base.Hyper

IPAddrType
----------
.. autoclass:: stellar_sdk.xdr.ip_addr_type.IPAddrType

InflationPayout
---------------
.. autoclass:: stellar_sdk.xdr.inflation_payout.InflationPayout

InflationResult
---------------
.. autoclass:: stellar_sdk.xdr.inflation_result.InflationResult

InflationResultCode
-------------------
.. autoclass:: stellar_sdk.xdr.inflation_result_code.InflationResultCode

InnerTransactionResult
----------------------
.. autoclass:: stellar_sdk.xdr.inner_transaction_result.InnerTransactionResult

InnerTransactionResultExt
-------------------------
.. autoclass:: stellar_sdk.xdr.inner_transaction_result_ext.InnerTransactionResultExt

InnerTransactionResultPair
--------------------------
.. autoclass:: stellar_sdk.xdr.inner_transaction_result_pair.InnerTransactionResultPair

InnerTransactionResultResult
----------------------------
.. autoclass:: stellar_sdk.xdr.inner_transaction_result_result.InnerTransactionResultResult

Int32
-----
.. autoclass:: stellar_sdk.xdr.int32.Int32

Int64
-----
.. autoclass:: stellar_sdk.xdr.int64.Int64

Integer
-------
.. autoclass:: stellar_sdk.xdr.base.Integer

LedgerCloseMeta
---------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta.LedgerCloseMeta

LedgerCloseMetaV0
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta_v0.LedgerCloseMetaV0

LedgerCloseValueSignature
-------------------------
.. autoclass:: stellar_sdk.xdr.ledger_close_value_signature.LedgerCloseValueSignature

LedgerEntry
-----------
.. autoclass:: stellar_sdk.xdr.ledger_entry.LedgerEntry

LedgerEntryChange
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_change.LedgerEntryChange

LedgerEntryChangeType
---------------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_change_type.LedgerEntryChangeType

LedgerEntryChanges
------------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_changes.LedgerEntryChanges

LedgerEntryData
---------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_data.LedgerEntryData

LedgerEntryExt
--------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_ext.LedgerEntryExt

LedgerEntryExtensionV1
----------------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_extension_v1.LedgerEntryExtensionV1

LedgerEntryExtensionV1Ext
-------------------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_extension_v1_ext.LedgerEntryExtensionV1Ext

LedgerEntryType
---------------
.. autoclass:: stellar_sdk.xdr.ledger_entry_type.LedgerEntryType

LedgerHeader
------------
.. autoclass:: stellar_sdk.xdr.ledger_header.LedgerHeader

LedgerHeaderExt
---------------
.. autoclass:: stellar_sdk.xdr.ledger_header_ext.LedgerHeaderExt

LedgerHeaderHistoryEntry
------------------------
.. autoclass:: stellar_sdk.xdr.ledger_header_history_entry.LedgerHeaderHistoryEntry

LedgerHeaderHistoryEntryExt
---------------------------
.. autoclass:: stellar_sdk.xdr.ledger_header_history_entry_ext.LedgerHeaderHistoryEntryExt

LedgerKey
---------
.. autoclass:: stellar_sdk.xdr.ledger_key.LedgerKey

LedgerKeyAccount
----------------
.. autoclass:: stellar_sdk.xdr.ledger_key_account.LedgerKeyAccount

LedgerKeyClaimableBalance
-------------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_claimable_balance.LedgerKeyClaimableBalance

LedgerKeyData
-------------
.. autoclass:: stellar_sdk.xdr.ledger_key_data.LedgerKeyData

LedgerKeyLiquidityPool
----------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_liquidity_pool.LedgerKeyLiquidityPool

LedgerKeyOffer
--------------
.. autoclass:: stellar_sdk.xdr.ledger_key_offer.LedgerKeyOffer

LedgerKeyTrustLine
------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_trust_line.LedgerKeyTrustLine

LedgerSCPMessages
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_scp_messages.LedgerSCPMessages

LedgerUpgrade
-------------
.. autoclass:: stellar_sdk.xdr.ledger_upgrade.LedgerUpgrade

LedgerUpgradeType
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_upgrade_type.LedgerUpgradeType

Liabilities
-----------
.. autoclass:: stellar_sdk.xdr.liabilities.Liabilities

LiquidityPoolConstantProductParameters
--------------------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_constant_product_parameters.LiquidityPoolConstantProductParameters

LiquidityPoolDepositOp
----------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_deposit_op.LiquidityPoolDepositOp

LiquidityPoolDepositResult
--------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_deposit_result.LiquidityPoolDepositResult

LiquidityPoolDepositResultCode
------------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_deposit_result_code.LiquidityPoolDepositResultCode

LiquidityPoolEntry
------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_entry.LiquidityPoolEntry

LiquidityPoolEntryBody
----------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_entry_body.LiquidityPoolEntryBody

LiquidityPoolEntryConstantProduct
---------------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_entry_constant_product.LiquidityPoolEntryConstantProduct

LiquidityPoolParameters
-----------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_parameters.LiquidityPoolParameters

LiquidityPoolType
-----------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_type.LiquidityPoolType

LiquidityPoolWithdrawOp
-----------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_withdraw_op.LiquidityPoolWithdrawOp

LiquidityPoolWithdrawResult
---------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_withdraw_result.LiquidityPoolWithdrawResult

LiquidityPoolWithdrawResultCode
-------------------------------
.. autoclass:: stellar_sdk.xdr.liquidity_pool_withdraw_result_code.LiquidityPoolWithdrawResultCode

ManageBuyOfferOp
----------------
.. autoclass:: stellar_sdk.xdr.manage_buy_offer_op.ManageBuyOfferOp

ManageBuyOfferResult
--------------------
.. autoclass:: stellar_sdk.xdr.manage_buy_offer_result.ManageBuyOfferResult

ManageBuyOfferResultCode
------------------------
.. autoclass:: stellar_sdk.xdr.manage_buy_offer_result_code.ManageBuyOfferResultCode

ManageDataOp
------------
.. autoclass:: stellar_sdk.xdr.manage_data_op.ManageDataOp

ManageDataResult
----------------
.. autoclass:: stellar_sdk.xdr.manage_data_result.ManageDataResult

ManageDataResultCode
--------------------
.. autoclass:: stellar_sdk.xdr.manage_data_result_code.ManageDataResultCode

ManageOfferEffect
-----------------
.. autoclass:: stellar_sdk.xdr.manage_offer_effect.ManageOfferEffect

ManageOfferSuccessResult
------------------------
.. autoclass:: stellar_sdk.xdr.manage_offer_success_result.ManageOfferSuccessResult

ManageOfferSuccessResultOffer
-----------------------------
.. autoclass:: stellar_sdk.xdr.manage_offer_success_result_offer.ManageOfferSuccessResultOffer

ManageSellOfferOp
-----------------
.. autoclass:: stellar_sdk.xdr.manage_sell_offer_op.ManageSellOfferOp

ManageSellOfferResult
---------------------
.. autoclass:: stellar_sdk.xdr.manage_sell_offer_result.ManageSellOfferResult

ManageSellOfferResultCode
-------------------------
.. autoclass:: stellar_sdk.xdr.manage_sell_offer_result_code.ManageSellOfferResultCode

Memo
----
.. autoclass:: stellar_sdk.xdr.memo.Memo

MemoType
--------
.. autoclass:: stellar_sdk.xdr.memo_type.MemoType

MessageType
-----------
.. autoclass:: stellar_sdk.xdr.message_type.MessageType

MuxedAccount
------------
.. autoclass:: stellar_sdk.xdr.muxed_account.MuxedAccount

MuxedAccountMed25519
--------------------
.. autoclass:: stellar_sdk.xdr.muxed_account_med25519.MuxedAccountMed25519

NodeID
------
.. autoclass:: stellar_sdk.xdr.node_id.NodeID

OfferEntry
----------
.. autoclass:: stellar_sdk.xdr.offer_entry.OfferEntry

OfferEntryExt
-------------
.. autoclass:: stellar_sdk.xdr.offer_entry_ext.OfferEntryExt

OfferEntryFlags
---------------
.. autoclass:: stellar_sdk.xdr.offer_entry_flags.OfferEntryFlags

Opaque
------
.. autoclass:: stellar_sdk.xdr.base.Opaque

Operation
---------
.. autoclass:: stellar_sdk.xdr.operation.Operation

OperationBody
-------------
.. autoclass:: stellar_sdk.xdr.operation_body.OperationBody

OperationID
-----------
.. autoclass:: stellar_sdk.xdr.operation_id.OperationID

OperationIDId
-------------
.. autoclass:: stellar_sdk.xdr.operation_id_id.OperationIDId

OperationMeta
-------------
.. autoclass:: stellar_sdk.xdr.operation_meta.OperationMeta

OperationResult
---------------
.. autoclass:: stellar_sdk.xdr.operation_result.OperationResult

OperationResultCode
-------------------
.. autoclass:: stellar_sdk.xdr.operation_result_code.OperationResultCode

OperationResultTr
-----------------
.. autoclass:: stellar_sdk.xdr.operation_result_tr.OperationResultTr

OperationType
-------------
.. autoclass:: stellar_sdk.xdr.operation_type.OperationType

PathPaymentStrictReceiveOp
--------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_receive_op.PathPaymentStrictReceiveOp

PathPaymentStrictReceiveResult
------------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_receive_result.PathPaymentStrictReceiveResult

PathPaymentStrictReceiveResultCode
----------------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_receive_result_code.PathPaymentStrictReceiveResultCode

PathPaymentStrictReceiveResultSuccess
-------------------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_receive_result_success.PathPaymentStrictReceiveResultSuccess

PathPaymentStrictSendOp
-----------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_send_op.PathPaymentStrictSendOp

PathPaymentStrictSendResult
---------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_send_result.PathPaymentStrictSendResult

PathPaymentStrictSendResultCode
-------------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_send_result_code.PathPaymentStrictSendResultCode

PathPaymentStrictSendResultSuccess
----------------------------------
.. autoclass:: stellar_sdk.xdr.path_payment_strict_send_result_success.PathPaymentStrictSendResultSuccess

PaymentOp
---------
.. autoclass:: stellar_sdk.xdr.payment_op.PaymentOp

PaymentResult
-------------
.. autoclass:: stellar_sdk.xdr.payment_result.PaymentResult

PaymentResultCode
-----------------
.. autoclass:: stellar_sdk.xdr.payment_result_code.PaymentResultCode

PeerAddress
-----------
.. autoclass:: stellar_sdk.xdr.peer_address.PeerAddress

PeerAddressIp
-------------
.. autoclass:: stellar_sdk.xdr.peer_address_ip.PeerAddressIp

PeerStatList
------------
.. autoclass:: stellar_sdk.xdr.peer_stat_list.PeerStatList

PeerStats
---------
.. autoclass:: stellar_sdk.xdr.peer_stats.PeerStats

PoolID
------
.. autoclass:: stellar_sdk.xdr.pool_id.PoolID

Price
-----
.. autoclass:: stellar_sdk.xdr.price.Price

PublicKey
---------
.. autoclass:: stellar_sdk.xdr.public_key.PublicKey

PublicKeyType
-------------
.. autoclass:: stellar_sdk.xdr.public_key_type.PublicKeyType

RevokeSponsorshipOp
-------------------
.. autoclass:: stellar_sdk.xdr.revoke_sponsorship_op.RevokeSponsorshipOp

RevokeSponsorshipOpSigner
-------------------------
.. autoclass:: stellar_sdk.xdr.revoke_sponsorship_op_signer.RevokeSponsorshipOpSigner

RevokeSponsorshipResult
-----------------------
.. autoclass:: stellar_sdk.xdr.revoke_sponsorship_result.RevokeSponsorshipResult

RevokeSponsorshipResultCode
---------------------------
.. autoclass:: stellar_sdk.xdr.revoke_sponsorship_result_code.RevokeSponsorshipResultCode

RevokeSponsorshipType
---------------------
.. autoclass:: stellar_sdk.xdr.revoke_sponsorship_type.RevokeSponsorshipType

SCPBallot
---------
.. autoclass:: stellar_sdk.xdr.scp_ballot.SCPBallot

SCPEnvelope
-----------
.. autoclass:: stellar_sdk.xdr.scp_envelope.SCPEnvelope

SCPHistoryEntry
---------------
.. autoclass:: stellar_sdk.xdr.scp_history_entry.SCPHistoryEntry

SCPHistoryEntryV0
-----------------
.. autoclass:: stellar_sdk.xdr.scp_history_entry_v0.SCPHistoryEntryV0

SCPNomination
-------------
.. autoclass:: stellar_sdk.xdr.scp_nomination.SCPNomination

SCPQuorumSet
------------
.. autoclass:: stellar_sdk.xdr.scp_quorum_set.SCPQuorumSet

SCPStatement
------------
.. autoclass:: stellar_sdk.xdr.scp_statement.SCPStatement

SCPStatementConfirm
-------------------
.. autoclass:: stellar_sdk.xdr.scp_statement_confirm.SCPStatementConfirm

SCPStatementExternalize
-----------------------
.. autoclass:: stellar_sdk.xdr.scp_statement_externalize.SCPStatementExternalize

SCPStatementPledges
-------------------
.. autoclass:: stellar_sdk.xdr.scp_statement_pledges.SCPStatementPledges

SCPStatementPrepare
-------------------
.. autoclass:: stellar_sdk.xdr.scp_statement_prepare.SCPStatementPrepare

SCPStatementType
----------------
.. autoclass:: stellar_sdk.xdr.scp_statement_type.SCPStatementType

SequenceNumber
--------------
.. autoclass:: stellar_sdk.xdr.sequence_number.SequenceNumber

SetOptionsOp
------------
.. autoclass:: stellar_sdk.xdr.set_options_op.SetOptionsOp

SetOptionsResult
----------------
.. autoclass:: stellar_sdk.xdr.set_options_result.SetOptionsResult

SetOptionsResultCode
--------------------
.. autoclass:: stellar_sdk.xdr.set_options_result_code.SetOptionsResultCode

SetTrustLineFlagsOp
-------------------
.. autoclass:: stellar_sdk.xdr.set_trust_line_flags_op.SetTrustLineFlagsOp

SetTrustLineFlagsResult
-----------------------
.. autoclass:: stellar_sdk.xdr.set_trust_line_flags_result.SetTrustLineFlagsResult

SetTrustLineFlagsResultCode
---------------------------
.. autoclass:: stellar_sdk.xdr.set_trust_line_flags_result_code.SetTrustLineFlagsResultCode

Signature
---------
.. autoclass:: stellar_sdk.xdr.signature.Signature

SignatureHint
-------------
.. autoclass:: stellar_sdk.xdr.signature_hint.SignatureHint

SignedSurveyRequestMessage
--------------------------
.. autoclass:: stellar_sdk.xdr.signed_survey_request_message.SignedSurveyRequestMessage

SignedSurveyResponseMessage
---------------------------
.. autoclass:: stellar_sdk.xdr.signed_survey_response_message.SignedSurveyResponseMessage

Signer
------
.. autoclass:: stellar_sdk.xdr.signer.Signer

SignerKey
---------
.. autoclass:: stellar_sdk.xdr.signer_key.SignerKey

SignerKeyType
-------------
.. autoclass:: stellar_sdk.xdr.signer_key_type.SignerKeyType

SimplePaymentResult
-------------------
.. autoclass:: stellar_sdk.xdr.simple_payment_result.SimplePaymentResult

SponsorshipDescriptor
---------------------
.. autoclass:: stellar_sdk.xdr.sponsorship_descriptor.SponsorshipDescriptor

StellarMessage
--------------
.. autoclass:: stellar_sdk.xdr.stellar_message.StellarMessage

StellarValue
------------
.. autoclass:: stellar_sdk.xdr.stellar_value.StellarValue

StellarValueExt
---------------
.. autoclass:: stellar_sdk.xdr.stellar_value_ext.StellarValueExt

StellarValueType
----------------
.. autoclass:: stellar_sdk.xdr.stellar_value_type.StellarValueType

String
------
.. autoclass:: stellar_sdk.xdr.base.String

String32
--------
.. autoclass:: stellar_sdk.xdr.string32.String32

String64
--------
.. autoclass:: stellar_sdk.xdr.string64.String64

SurveyMessageCommandType
------------------------
.. autoclass:: stellar_sdk.xdr.survey_message_command_type.SurveyMessageCommandType

SurveyRequestMessage
--------------------
.. autoclass:: stellar_sdk.xdr.survey_request_message.SurveyRequestMessage

SurveyResponseBody
------------------
.. autoclass:: stellar_sdk.xdr.survey_response_body.SurveyResponseBody

SurveyResponseMessage
---------------------
.. autoclass:: stellar_sdk.xdr.survey_response_message.SurveyResponseMessage

ThresholdIndexes
----------------
.. autoclass:: stellar_sdk.xdr.threshold_indexes.ThresholdIndexes

Thresholds
----------
.. autoclass:: stellar_sdk.xdr.thresholds.Thresholds

TimeBounds
----------
.. autoclass:: stellar_sdk.xdr.time_bounds.TimeBounds

TimePoint
---------
.. autoclass:: stellar_sdk.xdr.time_point.TimePoint

TopologyResponseBody
--------------------
.. autoclass:: stellar_sdk.xdr.topology_response_body.TopologyResponseBody

Transaction
-----------
.. autoclass:: stellar_sdk.xdr.transaction.Transaction

TransactionEnvelope
-------------------
.. autoclass:: stellar_sdk.xdr.transaction_envelope.TransactionEnvelope

TransactionExt
--------------
.. autoclass:: stellar_sdk.xdr.transaction_ext.TransactionExt

TransactionHistoryEntry
-----------------------
.. autoclass:: stellar_sdk.xdr.transaction_history_entry.TransactionHistoryEntry

TransactionHistoryEntryExt
--------------------------
.. autoclass:: stellar_sdk.xdr.transaction_history_entry_ext.TransactionHistoryEntryExt

TransactionHistoryResultEntry
-----------------------------
.. autoclass:: stellar_sdk.xdr.transaction_history_result_entry.TransactionHistoryResultEntry

TransactionHistoryResultEntryExt
--------------------------------
.. autoclass:: stellar_sdk.xdr.transaction_history_result_entry_ext.TransactionHistoryResultEntryExt

TransactionMeta
---------------
.. autoclass:: stellar_sdk.xdr.transaction_meta.TransactionMeta

TransactionMetaV1
-----------------
.. autoclass:: stellar_sdk.xdr.transaction_meta_v1.TransactionMetaV1

TransactionMetaV2
-----------------
.. autoclass:: stellar_sdk.xdr.transaction_meta_v2.TransactionMetaV2

TransactionResult
-----------------
.. autoclass:: stellar_sdk.xdr.transaction_result.TransactionResult

TransactionResultCode
---------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_code.TransactionResultCode

TransactionResultExt
--------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_ext.TransactionResultExt

TransactionResultMeta
---------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_meta.TransactionResultMeta

TransactionResultPair
---------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_pair.TransactionResultPair

TransactionResultResult
-----------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_result.TransactionResultResult

TransactionResultSet
--------------------
.. autoclass:: stellar_sdk.xdr.transaction_result_set.TransactionResultSet

TransactionSet
--------------
.. autoclass:: stellar_sdk.xdr.transaction_set.TransactionSet

TransactionSignaturePayload
---------------------------
.. autoclass:: stellar_sdk.xdr.transaction_signature_payload.TransactionSignaturePayload

TransactionSignaturePayloadTaggedTransaction
--------------------------------------------
.. autoclass:: stellar_sdk.xdr.transaction_signature_payload_tagged_transaction.TransactionSignaturePayloadTaggedTransaction

TransactionV0
-------------
.. autoclass:: stellar_sdk.xdr.transaction_v0.TransactionV0

TransactionV0Envelope
---------------------
.. autoclass:: stellar_sdk.xdr.transaction_v0_envelope.TransactionV0Envelope

TransactionV0Ext
----------------
.. autoclass:: stellar_sdk.xdr.transaction_v0_ext.TransactionV0Ext

TransactionV1Envelope
---------------------
.. autoclass:: stellar_sdk.xdr.transaction_v1_envelope.TransactionV1Envelope

TrustLineAsset
--------------
.. autoclass:: stellar_sdk.xdr.trust_line_asset.TrustLineAsset

TrustLineEntry
--------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry.TrustLineEntry

TrustLineEntryExt
-----------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry_ext.TrustLineEntryExt

TrustLineEntryExtensionV2
-------------------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry_extension_v2.TrustLineEntryExtensionV2

TrustLineEntryExtensionV2Ext
----------------------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry_extension_v2_ext.TrustLineEntryExtensionV2Ext

TrustLineEntryV1
----------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry_v1.TrustLineEntryV1

TrustLineEntryV1Ext
-------------------
.. autoclass:: stellar_sdk.xdr.trust_line_entry_v1_ext.TrustLineEntryV1Ext

TrustLineFlags
--------------
.. autoclass:: stellar_sdk.xdr.trust_line_flags.TrustLineFlags

Uint256
-------
.. autoclass:: stellar_sdk.xdr.uint256.Uint256

Uint32
------
.. autoclass:: stellar_sdk.xdr.uint32.Uint32

Uint64
------
.. autoclass:: stellar_sdk.xdr.uint64.Uint64

UnsignedHyper
-------------
.. autoclass:: stellar_sdk.xdr.base.UnsignedHyper

UnsignedInteger
---------------
.. autoclass:: stellar_sdk.xdr.base.UnsignedInteger

UpgradeEntryMeta
----------------
.. autoclass:: stellar_sdk.xdr.upgrade_entry_meta.UpgradeEntryMeta

UpgradeType
-----------
.. autoclass:: stellar_sdk.xdr.upgrade_type.UpgradeType

Value
-----
.. autoclass:: stellar_sdk.xdr.value.Value

Constants
---------
.. autodata:: stellar_sdk.xdr.constants.LIQUIDITY_POOL_FEE_V18
.. autodata:: stellar_sdk.xdr.constants.MASK_ACCOUNT_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_ACCOUNT_FLAGS_V17
.. autodata:: stellar_sdk.xdr.constants.MASK_CLAIMABLE_BALANCE_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_OFFERENTRY_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS_V13
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS_V17
.. autodata:: stellar_sdk.xdr.constants.MAX_OPS_PER_TX
.. autodata:: stellar_sdk.xdr.constants.MAX_SIGNERS