.. _api:

*****************
API Documentation
*****************


.. module:: stellar_sdk


Account
^^^^^^^

.. autoclass:: stellar_sdk.account.Account
   :members:
   :inherited-members:

Address
^^^^^^^

.. autoclass:: stellar_sdk.address.Address
   :members:

.. autoclass:: stellar_sdk.address.AddressType
   :members:

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

Contract
^^^^^^^^

ContractClient
---------------

.. autoclass:: stellar_sdk.contract.ContractClient
   :members:

AssembledTransaction
--------------------

.. autoclass:: stellar_sdk.contract.AssembledTransaction
   :members:


ContractClientAsync
-------------------

.. autoclass:: stellar_sdk.contract.ContractClientAsync
   :members:

AssembledTransactionAsync
-------------------------

.. autoclass:: stellar_sdk.contract.AssembledTransactionAsync
   :members:

Exceptions
----------

.. automodule:: stellar_sdk.contract.exceptions
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

InvokeHostFunction
------------------
.. autoclass:: stellar_sdk.operation.InvokeHostFunction
   :members: to_xdr_object, from_xdr_object

ExtendFootprintTTL
------------------
.. autoclass:: stellar_sdk.operation.ExtendFootprintTTL
   :members: to_xdr_object, from_xdr_object

RestoreFootprint
----------------
.. autoclass:: stellar_sdk.operation.RestoreFootprint
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

SorobanDataBuilder
^^^^^^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.SorobanDataBuilder
   :members:

SorobanServer
^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.SorobanServer
   :members:

SorobanServer
^^^^^^^^^^^^^

.. autoclass:: stellar_sdk.SorobanServerAsync
   :members:

Soroban RPC Definitions
^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: stellar_sdk.soroban_rpc
   :members:

scval
^^^^^
.. autofunction:: stellar_sdk.scval.to_native
.. autofunction:: stellar_sdk.scval.to_address
.. autofunction:: stellar_sdk.scval.from_address
.. autofunction:: stellar_sdk.scval.to_bool
.. autofunction:: stellar_sdk.scval.from_bool
.. autofunction:: stellar_sdk.scval.to_bytes
.. autofunction:: stellar_sdk.scval.from_bytes
.. autofunction:: stellar_sdk.scval.to_duration
.. autofunction:: stellar_sdk.scval.from_duration
.. autofunction:: stellar_sdk.scval.to_int32
.. autofunction:: stellar_sdk.scval.from_int32
.. autofunction:: stellar_sdk.scval.to_int64
.. autofunction:: stellar_sdk.scval.from_int64
.. autofunction:: stellar_sdk.scval.to_int128
.. autofunction:: stellar_sdk.scval.from_int128
.. autofunction:: stellar_sdk.scval.to_int256
.. autofunction:: stellar_sdk.scval.from_int256
.. autofunction:: stellar_sdk.scval.to_map
.. autofunction:: stellar_sdk.scval.from_map
.. autofunction:: stellar_sdk.scval.to_string
.. autofunction:: stellar_sdk.scval.from_string
.. autofunction:: stellar_sdk.scval.to_symbol
.. autofunction:: stellar_sdk.scval.from_symbol
.. autofunction:: stellar_sdk.scval.to_timepoint
.. autofunction:: stellar_sdk.scval.from_timepoint
.. autofunction:: stellar_sdk.scval.to_uint32
.. autofunction:: stellar_sdk.scval.from_uint32
.. autofunction:: stellar_sdk.scval.to_uint64
.. autofunction:: stellar_sdk.scval.from_uint64
.. autofunction:: stellar_sdk.scval.to_uint128
.. autofunction:: stellar_sdk.scval.from_uint128
.. autofunction:: stellar_sdk.scval.to_uint256
.. autofunction:: stellar_sdk.scval.from_uint256
.. autofunction:: stellar_sdk.scval.to_vec
.. autofunction:: stellar_sdk.scval.from_vec
.. autofunction:: stellar_sdk.scval.to_enum
.. autofunction:: stellar_sdk.scval.from_enum
.. autofunction:: stellar_sdk.scval.to_tuple_struct
.. autofunction:: stellar_sdk.scval.from_tuple_struct
.. autofunction:: stellar_sdk.scval.to_struct
.. autofunction:: stellar_sdk.scval.from_struct

Auth
^^^^
.. autofunction:: stellar_sdk.auth.authorize_entry
.. autofunction:: stellar_sdk.auth.authorize_invocation

Helpers
^^^^^^^
.. autofunction:: stellar_sdk.helpers.parse_transaction_envelope_from_xdr

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

SEP 0035: Operation IDs
-----------------------
.. autoclass:: stellar_sdk.sep.toid.TOID
   :members:
   :inherited-members:

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

AccountEntryExtensionV3
-----------------------
.. autoclass:: stellar_sdk.xdr.account_entry_extension_v3.AccountEntryExtensionV3

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

ArchivalProof
-------------
.. autoclass:: stellar_sdk.xdr.archival_proof.ArchivalProof

ArchivalProofBody
-----------------
.. autoclass:: stellar_sdk.xdr.archival_proof_body.ArchivalProofBody

ArchivalProofNode
-----------------
.. autoclass:: stellar_sdk.xdr.archival_proof_node.ArchivalProofNode

ArchivalProofType
-----------------
.. autoclass:: stellar_sdk.xdr.archival_proof_type.ArchivalProofType

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

BinaryFuseFilterType
--------------------
.. autoclass:: stellar_sdk.xdr.binary_fuse_filter_type.BinaryFuseFilterType

Boolean
-------
.. autoclass:: stellar_sdk.xdr.base.Boolean

BucketEntry
-----------
.. autoclass:: stellar_sdk.xdr.bucket_entry.BucketEntry

BucketEntryType
---------------
.. autoclass:: stellar_sdk.xdr.bucket_entry_type.BucketEntryType

BucketListType
--------------
.. autoclass:: stellar_sdk.xdr.bucket_list_type.BucketListType

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

ColdArchiveArchivedLeaf
-----------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_archived_leaf.ColdArchiveArchivedLeaf

ColdArchiveBoundaryLeaf
-----------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_boundary_leaf.ColdArchiveBoundaryLeaf

ColdArchiveBucketEntry
----------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_bucket_entry.ColdArchiveBucketEntry

ColdArchiveBucketEntryType
--------------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_bucket_entry_type.ColdArchiveBucketEntryType

ColdArchiveDeletedLeaf
----------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_deleted_leaf.ColdArchiveDeletedLeaf

ColdArchiveHashEntry
--------------------
.. autoclass:: stellar_sdk.xdr.cold_archive_hash_entry.ColdArchiveHashEntry

ConfigSettingContractBandwidthV0
--------------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_bandwidth_v0.ConfigSettingContractBandwidthV0

ConfigSettingContractComputeV0
------------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_compute_v0.ConfigSettingContractComputeV0

ConfigSettingContractEventsV0
-----------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_events_v0.ConfigSettingContractEventsV0

ConfigSettingContractExecutionLanesV0
-------------------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_execution_lanes_v0.ConfigSettingContractExecutionLanesV0

ConfigSettingContractHistoricalDataV0
-------------------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_historical_data_v0.ConfigSettingContractHistoricalDataV0

ConfigSettingContractLedgerCostV0
---------------------------------
.. autoclass:: stellar_sdk.xdr.config_setting_contract_ledger_cost_v0.ConfigSettingContractLedgerCostV0

ConfigSettingEntry
------------------
.. autoclass:: stellar_sdk.xdr.config_setting_entry.ConfigSettingEntry

ConfigSettingID
---------------
.. autoclass:: stellar_sdk.xdr.config_setting_id.ConfigSettingID

ConfigUpgradeSet
----------------
.. autoclass:: stellar_sdk.xdr.config_upgrade_set.ConfigUpgradeSet

ConfigUpgradeSetKey
-------------------
.. autoclass:: stellar_sdk.xdr.config_upgrade_set_key.ConfigUpgradeSetKey

ContractCodeCostInputs
----------------------
.. autoclass:: stellar_sdk.xdr.contract_code_cost_inputs.ContractCodeCostInputs

ContractCodeEntry
-----------------
.. autoclass:: stellar_sdk.xdr.contract_code_entry.ContractCodeEntry

ContractCodeEntryExt
--------------------
.. autoclass:: stellar_sdk.xdr.contract_code_entry_ext.ContractCodeEntryExt

ContractCodeEntryV1
-------------------
.. autoclass:: stellar_sdk.xdr.contract_code_entry_v1.ContractCodeEntryV1

ContractCostParamEntry
----------------------
.. autoclass:: stellar_sdk.xdr.contract_cost_param_entry.ContractCostParamEntry

ContractCostParams
------------------
.. autoclass:: stellar_sdk.xdr.contract_cost_params.ContractCostParams

ContractCostType
----------------
.. autoclass:: stellar_sdk.xdr.contract_cost_type.ContractCostType

ContractDataDurability
----------------------
.. autoclass:: stellar_sdk.xdr.contract_data_durability.ContractDataDurability

ContractDataEntry
-----------------
.. autoclass:: stellar_sdk.xdr.contract_data_entry.ContractDataEntry

ContractEvent
-------------
.. autoclass:: stellar_sdk.xdr.contract_event.ContractEvent

ContractEventBody
-----------------
.. autoclass:: stellar_sdk.xdr.contract_event_body.ContractEventBody

ContractEventType
-----------------
.. autoclass:: stellar_sdk.xdr.contract_event_type.ContractEventType

ContractEventV0
---------------
.. autoclass:: stellar_sdk.xdr.contract_event_v0.ContractEventV0

ContractExecutable
------------------
.. autoclass:: stellar_sdk.xdr.contract_executable.ContractExecutable

ContractExecutableType
----------------------
.. autoclass:: stellar_sdk.xdr.contract_executable_type.ContractExecutableType

ContractIDPreimage
------------------
.. autoclass:: stellar_sdk.xdr.contract_id_preimage.ContractIDPreimage

ContractIDPreimageFromAddress
-----------------------------
.. autoclass:: stellar_sdk.xdr.contract_id_preimage_from_address.ContractIDPreimageFromAddress

ContractIDPreimageType
----------------------
.. autoclass:: stellar_sdk.xdr.contract_id_preimage_type.ContractIDPreimageType

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

CreateContractArgs
------------------
.. autoclass:: stellar_sdk.xdr.create_contract_args.CreateContractArgs

CreateContractArgsV2
--------------------
.. autoclass:: stellar_sdk.xdr.create_contract_args_v2.CreateContractArgsV2

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

DiagnosticEvent
---------------
.. autoclass:: stellar_sdk.xdr.diagnostic_event.DiagnosticEvent

DiagnosticEvents
----------------
.. autoclass:: stellar_sdk.xdr.diagnostic_events.DiagnosticEvents

DontHave
--------
.. autoclass:: stellar_sdk.xdr.dont_have.DontHave

Double
------
.. autoclass:: stellar_sdk.xdr.base.Double

Duration
--------
.. autoclass:: stellar_sdk.xdr.duration.Duration

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

EvictionIterator
----------------
.. autoclass:: stellar_sdk.xdr.eviction_iterator.EvictionIterator

ExistenceProofBody
------------------
.. autoclass:: stellar_sdk.xdr.existence_proof_body.ExistenceProofBody

ExtendFootprintTTLOp
--------------------
.. autoclass:: stellar_sdk.xdr.extend_footprint_ttl_op.ExtendFootprintTTLOp

ExtendFootprintTTLResult
------------------------
.. autoclass:: stellar_sdk.xdr.extend_footprint_ttl_result.ExtendFootprintTTLResult

ExtendFootprintTTLResultCode
----------------------------
.. autoclass:: stellar_sdk.xdr.extend_footprint_ttl_result_code.ExtendFootprintTTLResultCode

ExtensionPoint
--------------
.. autoclass:: stellar_sdk.xdr.extension_point.ExtensionPoint

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

Float
-----
.. autoclass:: stellar_sdk.xdr.base.Float

FloodAdvert
-----------
.. autoclass:: stellar_sdk.xdr.flood_advert.FloodAdvert

FloodDemand
-----------
.. autoclass:: stellar_sdk.xdr.flood_demand.FloodDemand

GeneralizedTransactionSet
-------------------------
.. autoclass:: stellar_sdk.xdr.generalized_transaction_set.GeneralizedTransactionSet

Hash
----
.. autoclass:: stellar_sdk.xdr.hash.Hash

HashIDPreimage
--------------
.. autoclass:: stellar_sdk.xdr.hash_id_preimage.HashIDPreimage

HashIDPreimageContractID
------------------------
.. autoclass:: stellar_sdk.xdr.hash_id_preimage_contract_id.HashIDPreimageContractID

HashIDPreimageOperationID
-------------------------
.. autoclass:: stellar_sdk.xdr.hash_id_preimage_operation_id.HashIDPreimageOperationID

HashIDPreimageRevokeID
----------------------
.. autoclass:: stellar_sdk.xdr.hash_id_preimage_revoke_id.HashIDPreimageRevokeID

HashIDPreimageSorobanAuthorization
----------------------------------
.. autoclass:: stellar_sdk.xdr.hash_id_preimage_soroban_authorization.HashIDPreimageSorobanAuthorization

Hello
-----
.. autoclass:: stellar_sdk.xdr.hello.Hello

HmacSha256Key
-------------
.. autoclass:: stellar_sdk.xdr.hmac_sha256_key.HmacSha256Key

HmacSha256Mac
-------------
.. autoclass:: stellar_sdk.xdr.hmac_sha256_mac.HmacSha256Mac

HostFunction
------------
.. autoclass:: stellar_sdk.xdr.host_function.HostFunction

HostFunctionType
----------------
.. autoclass:: stellar_sdk.xdr.host_function_type.HostFunctionType

HotArchiveBucketEntry
---------------------
.. autoclass:: stellar_sdk.xdr.hot_archive_bucket_entry.HotArchiveBucketEntry

HotArchiveBucketEntryType
-------------------------
.. autoclass:: stellar_sdk.xdr.hot_archive_bucket_entry_type.HotArchiveBucketEntryType

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

Int128Parts
-----------
.. autoclass:: stellar_sdk.xdr.int128_parts.Int128Parts

Int256Parts
-----------
.. autoclass:: stellar_sdk.xdr.int256_parts.Int256Parts

Int32
-----
.. autoclass:: stellar_sdk.xdr.int32.Int32

Int64
-----
.. autoclass:: stellar_sdk.xdr.int64.Int64

Integer
-------
.. autoclass:: stellar_sdk.xdr.base.Integer

InvokeContractArgs
------------------
.. autoclass:: stellar_sdk.xdr.invoke_contract_args.InvokeContractArgs

InvokeHostFunctionOp
--------------------
.. autoclass:: stellar_sdk.xdr.invoke_host_function_op.InvokeHostFunctionOp

InvokeHostFunctionResult
------------------------
.. autoclass:: stellar_sdk.xdr.invoke_host_function_result.InvokeHostFunctionResult

InvokeHostFunctionResultCode
----------------------------
.. autoclass:: stellar_sdk.xdr.invoke_host_function_result_code.InvokeHostFunctionResultCode

InvokeHostFunctionSuccessPreImage
---------------------------------
.. autoclass:: stellar_sdk.xdr.invoke_host_function_success_pre_image.InvokeHostFunctionSuccessPreImage

LedgerBounds
------------
.. autoclass:: stellar_sdk.xdr.ledger_bounds.LedgerBounds

LedgerCloseMeta
---------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta.LedgerCloseMeta

LedgerCloseMetaExt
------------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta_ext.LedgerCloseMetaExt

LedgerCloseMetaExtV1
--------------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta_ext_v1.LedgerCloseMetaExtV1

LedgerCloseMetaV0
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta_v0.LedgerCloseMetaV0

LedgerCloseMetaV1
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_close_meta_v1.LedgerCloseMetaV1

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

LedgerFootprint
---------------
.. autoclass:: stellar_sdk.xdr.ledger_footprint.LedgerFootprint

LedgerHeader
------------
.. autoclass:: stellar_sdk.xdr.ledger_header.LedgerHeader

LedgerHeaderExt
---------------
.. autoclass:: stellar_sdk.xdr.ledger_header_ext.LedgerHeaderExt

LedgerHeaderExtensionV1
-----------------------
.. autoclass:: stellar_sdk.xdr.ledger_header_extension_v1.LedgerHeaderExtensionV1

LedgerHeaderExtensionV1Ext
--------------------------
.. autoclass:: stellar_sdk.xdr.ledger_header_extension_v1_ext.LedgerHeaderExtensionV1Ext

LedgerHeaderFlags
-----------------
.. autoclass:: stellar_sdk.xdr.ledger_header_flags.LedgerHeaderFlags

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

LedgerKeyConfigSetting
----------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_config_setting.LedgerKeyConfigSetting

LedgerKeyContractCode
---------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_contract_code.LedgerKeyContractCode

LedgerKeyContractData
---------------------
.. autoclass:: stellar_sdk.xdr.ledger_key_contract_data.LedgerKeyContractData

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

LedgerKeyTtl
------------
.. autoclass:: stellar_sdk.xdr.ledger_key_ttl.LedgerKeyTtl

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

NonexistenceProofBody
---------------------
.. autoclass:: stellar_sdk.xdr.nonexistence_proof_body.NonexistenceProofBody

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

PersistedSCPState
-----------------
.. autoclass:: stellar_sdk.xdr.persisted_scp_state.PersistedSCPState

PersistedSCPStateV0
-------------------
.. autoclass:: stellar_sdk.xdr.persisted_scp_state_v0.PersistedSCPStateV0

PersistedSCPStateV1
-------------------
.. autoclass:: stellar_sdk.xdr.persisted_scp_state_v1.PersistedSCPStateV1

PoolID
------
.. autoclass:: stellar_sdk.xdr.pool_id.PoolID

PreconditionType
----------------
.. autoclass:: stellar_sdk.xdr.precondition_type.PreconditionType

Preconditions
-------------
.. autoclass:: stellar_sdk.xdr.preconditions.Preconditions

PreconditionsV2
---------------
.. autoclass:: stellar_sdk.xdr.preconditions_v2.PreconditionsV2

Price
-----
.. autoclass:: stellar_sdk.xdr.price.Price

ProofLevel
----------
.. autoclass:: stellar_sdk.xdr.proof_level.ProofLevel

PublicKey
---------
.. autoclass:: stellar_sdk.xdr.public_key.PublicKey

PublicKeyType
-------------
.. autoclass:: stellar_sdk.xdr.public_key_type.PublicKeyType

RestoreFootprintOp
------------------
.. autoclass:: stellar_sdk.xdr.restore_footprint_op.RestoreFootprintOp

RestoreFootprintResult
----------------------
.. autoclass:: stellar_sdk.xdr.restore_footprint_result.RestoreFootprintResult

RestoreFootprintResultCode
--------------------------
.. autoclass:: stellar_sdk.xdr.restore_footprint_result_code.RestoreFootprintResultCode

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

SCAddress
---------
.. autoclass:: stellar_sdk.xdr.sc_address.SCAddress

SCAddressType
-------------
.. autoclass:: stellar_sdk.xdr.sc_address_type.SCAddressType

SCBytes
-------
.. autoclass:: stellar_sdk.xdr.sc_bytes.SCBytes

SCContractInstance
------------------
.. autoclass:: stellar_sdk.xdr.sc_contract_instance.SCContractInstance

SCEnvMetaEntry
--------------
.. autoclass:: stellar_sdk.xdr.sc_env_meta_entry.SCEnvMetaEntry

SCEnvMetaEntryInterfaceVersion
------------------------------
.. autoclass:: stellar_sdk.xdr.sc_env_meta_entry_interface_version.SCEnvMetaEntryInterfaceVersion

SCEnvMetaKind
-------------
.. autoclass:: stellar_sdk.xdr.sc_env_meta_kind.SCEnvMetaKind

SCError
-------
.. autoclass:: stellar_sdk.xdr.sc_error.SCError

SCErrorCode
-----------
.. autoclass:: stellar_sdk.xdr.sc_error_code.SCErrorCode

SCErrorType
-----------
.. autoclass:: stellar_sdk.xdr.sc_error_type.SCErrorType

SCMap
-----
.. autoclass:: stellar_sdk.xdr.sc_map.SCMap

SCMapEntry
----------
.. autoclass:: stellar_sdk.xdr.sc_map_entry.SCMapEntry

SCMetaEntry
-----------
.. autoclass:: stellar_sdk.xdr.sc_meta_entry.SCMetaEntry

SCMetaKind
----------
.. autoclass:: stellar_sdk.xdr.sc_meta_kind.SCMetaKind

SCMetaV0
--------
.. autoclass:: stellar_sdk.xdr.sc_meta_v0.SCMetaV0

SCNonceKey
----------
.. autoclass:: stellar_sdk.xdr.sc_nonce_key.SCNonceKey

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

SCSpecEntry
-----------
.. autoclass:: stellar_sdk.xdr.sc_spec_entry.SCSpecEntry

SCSpecEntryKind
---------------
.. autoclass:: stellar_sdk.xdr.sc_spec_entry_kind.SCSpecEntryKind

SCSpecFunctionInputV0
---------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_function_input_v0.SCSpecFunctionInputV0

SCSpecFunctionV0
----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_function_v0.SCSpecFunctionV0

SCSpecType
----------
.. autoclass:: stellar_sdk.xdr.sc_spec_type.SCSpecType

SCSpecTypeBytesN
----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_bytes_n.SCSpecTypeBytesN

SCSpecTypeDef
-------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_def.SCSpecTypeDef

SCSpecTypeMap
-------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_map.SCSpecTypeMap

SCSpecTypeOption
----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_option.SCSpecTypeOption

SCSpecTypeResult
----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_result.SCSpecTypeResult

SCSpecTypeTuple
---------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_tuple.SCSpecTypeTuple

SCSpecTypeUDT
-------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_udt.SCSpecTypeUDT

SCSpecTypeVec
-------------
.. autoclass:: stellar_sdk.xdr.sc_spec_type_vec.SCSpecTypeVec

SCSpecUDTEnumCaseV0
-------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_enum_case_v0.SCSpecUDTEnumCaseV0

SCSpecUDTEnumV0
---------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_enum_v0.SCSpecUDTEnumV0

SCSpecUDTErrorEnumCaseV0
------------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_error_enum_case_v0.SCSpecUDTErrorEnumCaseV0

SCSpecUDTErrorEnumV0
--------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_error_enum_v0.SCSpecUDTErrorEnumV0

SCSpecUDTStructFieldV0
----------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_struct_field_v0.SCSpecUDTStructFieldV0

SCSpecUDTStructV0
-----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_struct_v0.SCSpecUDTStructV0

SCSpecUDTUnionCaseTupleV0
-------------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_union_case_tuple_v0.SCSpecUDTUnionCaseTupleV0

SCSpecUDTUnionCaseV0
--------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_union_case_v0.SCSpecUDTUnionCaseV0

SCSpecUDTUnionCaseV0Kind
------------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_union_case_v0_kind.SCSpecUDTUnionCaseV0Kind

SCSpecUDTUnionCaseVoidV0
------------------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_union_case_void_v0.SCSpecUDTUnionCaseVoidV0

SCSpecUDTUnionV0
----------------
.. autoclass:: stellar_sdk.xdr.sc_spec_udt_union_v0.SCSpecUDTUnionV0

SCString
--------
.. autoclass:: stellar_sdk.xdr.sc_string.SCString

SCSymbol
--------
.. autoclass:: stellar_sdk.xdr.sc_symbol.SCSymbol

SCVal
-----
.. autoclass:: stellar_sdk.xdr.sc_val.SCVal

SCValType
---------
.. autoclass:: stellar_sdk.xdr.sc_val_type.SCValType

SCVec
-----
.. autoclass:: stellar_sdk.xdr.sc_vec.SCVec

SendMore
--------
.. autoclass:: stellar_sdk.xdr.send_more.SendMore

SendMoreExtended
----------------
.. autoclass:: stellar_sdk.xdr.send_more_extended.SendMoreExtended

SequenceNumber
--------------
.. autoclass:: stellar_sdk.xdr.sequence_number.SequenceNumber

SerializedBinaryFuseFilter
--------------------------
.. autoclass:: stellar_sdk.xdr.serialized_binary_fuse_filter.SerializedBinaryFuseFilter

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

ShortHashSeed
-------------
.. autoclass:: stellar_sdk.xdr.short_hash_seed.ShortHashSeed

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

SignedTimeSlicedSurveyRequestMessage
------------------------------------
.. autoclass:: stellar_sdk.xdr.signed_time_sliced_survey_request_message.SignedTimeSlicedSurveyRequestMessage

SignedTimeSlicedSurveyResponseMessage
-------------------------------------
.. autoclass:: stellar_sdk.xdr.signed_time_sliced_survey_response_message.SignedTimeSlicedSurveyResponseMessage

SignedTimeSlicedSurveyStartCollectingMessage
--------------------------------------------
.. autoclass:: stellar_sdk.xdr.signed_time_sliced_survey_start_collecting_message.SignedTimeSlicedSurveyStartCollectingMessage

SignedTimeSlicedSurveyStopCollectingMessage
-------------------------------------------
.. autoclass:: stellar_sdk.xdr.signed_time_sliced_survey_stop_collecting_message.SignedTimeSlicedSurveyStopCollectingMessage

Signer
------
.. autoclass:: stellar_sdk.xdr.signer.Signer

SignerKey
---------
.. autoclass:: stellar_sdk.xdr.signer_key.SignerKey

SignerKeyEd25519SignedPayload
-----------------------------
.. autoclass:: stellar_sdk.xdr.signer_key_ed25519_signed_payload.SignerKeyEd25519SignedPayload

SignerKeyType
-------------
.. autoclass:: stellar_sdk.xdr.signer_key_type.SignerKeyType

SimplePaymentResult
-------------------
.. autoclass:: stellar_sdk.xdr.simple_payment_result.SimplePaymentResult

SorobanAddressCredentials
-------------------------
.. autoclass:: stellar_sdk.xdr.soroban_address_credentials.SorobanAddressCredentials

SorobanAuthorizationEntry
-------------------------
.. autoclass:: stellar_sdk.xdr.soroban_authorization_entry.SorobanAuthorizationEntry

SorobanAuthorizedFunction
-------------------------
.. autoclass:: stellar_sdk.xdr.soroban_authorized_function.SorobanAuthorizedFunction

SorobanAuthorizedFunctionType
-----------------------------
.. autoclass:: stellar_sdk.xdr.soroban_authorized_function_type.SorobanAuthorizedFunctionType

SorobanAuthorizedInvocation
---------------------------
.. autoclass:: stellar_sdk.xdr.soroban_authorized_invocation.SorobanAuthorizedInvocation

SorobanCredentials
------------------
.. autoclass:: stellar_sdk.xdr.soroban_credentials.SorobanCredentials

SorobanCredentialsType
----------------------
.. autoclass:: stellar_sdk.xdr.soroban_credentials_type.SorobanCredentialsType

SorobanResources
----------------
.. autoclass:: stellar_sdk.xdr.soroban_resources.SorobanResources

SorobanTransactionData
----------------------
.. autoclass:: stellar_sdk.xdr.soroban_transaction_data.SorobanTransactionData

SorobanTransactionMeta
----------------------
.. autoclass:: stellar_sdk.xdr.soroban_transaction_meta.SorobanTransactionMeta

SorobanTransactionMetaExt
-------------------------
.. autoclass:: stellar_sdk.xdr.soroban_transaction_meta_ext.SorobanTransactionMetaExt

SorobanTransactionMetaExtV1
---------------------------
.. autoclass:: stellar_sdk.xdr.soroban_transaction_meta_ext_v1.SorobanTransactionMetaExtV1

SponsorshipDescriptor
---------------------
.. autoclass:: stellar_sdk.xdr.sponsorship_descriptor.SponsorshipDescriptor

StateArchivalSettings
---------------------
.. autoclass:: stellar_sdk.xdr.state_archival_settings.StateArchivalSettings

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

StoredDebugTransactionSet
-------------------------
.. autoclass:: stellar_sdk.xdr.stored_debug_transaction_set.StoredDebugTransactionSet

StoredTransactionSet
--------------------
.. autoclass:: stellar_sdk.xdr.stored_transaction_set.StoredTransactionSet

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

SurveyMessageResponseType
-------------------------
.. autoclass:: stellar_sdk.xdr.survey_message_response_type.SurveyMessageResponseType

SurveyRequestMessage
--------------------
.. autoclass:: stellar_sdk.xdr.survey_request_message.SurveyRequestMessage

SurveyResponseBody
------------------
.. autoclass:: stellar_sdk.xdr.survey_response_body.SurveyResponseBody

SurveyResponseMessage
---------------------
.. autoclass:: stellar_sdk.xdr.survey_response_message.SurveyResponseMessage

TTLEntry
--------
.. autoclass:: stellar_sdk.xdr.ttl_entry.TTLEntry

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

TimeSlicedNodeData
------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_node_data.TimeSlicedNodeData

TimeSlicedPeerData
------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_peer_data.TimeSlicedPeerData

TimeSlicedPeerDataList
----------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_peer_data_list.TimeSlicedPeerDataList

TimeSlicedSurveyRequestMessage
------------------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_survey_request_message.TimeSlicedSurveyRequestMessage

TimeSlicedSurveyResponseMessage
-------------------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_survey_response_message.TimeSlicedSurveyResponseMessage

TimeSlicedSurveyStartCollectingMessage
--------------------------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_survey_start_collecting_message.TimeSlicedSurveyStartCollectingMessage

TimeSlicedSurveyStopCollectingMessage
-------------------------------------
.. autoclass:: stellar_sdk.xdr.time_sliced_survey_stop_collecting_message.TimeSlicedSurveyStopCollectingMessage

TopologyResponseBodyV0
----------------------
.. autoclass:: stellar_sdk.xdr.topology_response_body_v0.TopologyResponseBodyV0

TopologyResponseBodyV1
----------------------
.. autoclass:: stellar_sdk.xdr.topology_response_body_v1.TopologyResponseBodyV1

TopologyResponseBodyV2
----------------------
.. autoclass:: stellar_sdk.xdr.topology_response_body_v2.TopologyResponseBodyV2

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

TransactionMetaV3
-----------------
.. autoclass:: stellar_sdk.xdr.transaction_meta_v3.TransactionMetaV3

TransactionPhase
----------------
.. autoclass:: stellar_sdk.xdr.transaction_phase.TransactionPhase

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

TransactionSetV1
----------------
.. autoclass:: stellar_sdk.xdr.transaction_set_v1.TransactionSetV1

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

TxAdvertVector
--------------
.. autoclass:: stellar_sdk.xdr.tx_advert_vector.TxAdvertVector

TxDemandVector
--------------
.. autoclass:: stellar_sdk.xdr.tx_demand_vector.TxDemandVector

TxSetComponent
--------------
.. autoclass:: stellar_sdk.xdr.tx_set_component.TxSetComponent

TxSetComponentTxsMaybeDiscountedFee
-----------------------------------
.. autoclass:: stellar_sdk.xdr.tx_set_component_txs_maybe_discounted_fee.TxSetComponentTxsMaybeDiscountedFee

TxSetComponentType
------------------
.. autoclass:: stellar_sdk.xdr.tx_set_component_type.TxSetComponentType

UInt128Parts
------------
.. autoclass:: stellar_sdk.xdr.u_int128_parts.UInt128Parts

UInt256Parts
------------
.. autoclass:: stellar_sdk.xdr.u_int256_parts.UInt256Parts

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
.. autodata:: stellar_sdk.xdr.constants.AUTH_MSG_FLAG_FLOW_CONTROL_BYTES_REQUESTED
.. autodata:: stellar_sdk.xdr.constants.CONTRACT_COST_COUNT_LIMIT
.. autodata:: stellar_sdk.xdr.constants.LIQUIDITY_POOL_FEE_V18
.. autodata:: stellar_sdk.xdr.constants.MASK_ACCOUNT_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_ACCOUNT_FLAGS_V17
.. autodata:: stellar_sdk.xdr.constants.MASK_CLAIMABLE_BALANCE_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_LEDGER_HEADER_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_OFFERENTRY_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS_V13
.. autodata:: stellar_sdk.xdr.constants.MASK_TRUSTLINE_FLAGS_V17
.. autodata:: stellar_sdk.xdr.constants.MAX_OPS_PER_TX
.. autodata:: stellar_sdk.xdr.constants.MAX_SIGNERS
.. autodata:: stellar_sdk.xdr.constants.SCSYMBOL_LIMIT
.. autodata:: stellar_sdk.xdr.constants.SC_SPEC_DOC_LIMIT
.. autodata:: stellar_sdk.xdr.constants.TX_ADVERT_VECTOR_MAX_SIZE
.. autodata:: stellar_sdk.xdr.constants.TX_DEMAND_VECTOR_MAX_SIZE
