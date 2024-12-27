Release History
==============

### Pending

### Version 12.1.0

Released on December 27, 2024

#### Update
- feat: Add optional support for Shamir Secret Sharing with `Keypair.from_shamir_mnemonic_phrases` and `Keypair.generate_shamir_mnemonic_phrases`. ([#1010](https://github.com/StellarCN/py-stellar-base/pull/1010))

### Version 12.0.0

Released on November 28, 2024

This is the first stable release that supports Protocol 22. While the network has not upgraded yet, 
you can start integrating the new features into your codebase if you want a head start.

If you are using this SDK to call Soroban contracts, please check [stellar-contract-bindings](https://github.com/lightsail-network/stellar-contract-bindings), 
which can automatically generate contract binding code for you, making it incredibly easy to call contracts.

The following log is the changes since 11.1.0:

#### Update
- feat: add support for Soroban PRC's `getVersionInfo` API interfaces. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- feat: Add `transaction_hash` to `GetTransactionResponse` and `GetTransactionsResponse`. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- feat: `scval.from_enum` and `scval.to_enum` now support multiple values. ([#1004](https://github.com/StellarCN/py-stellar-base/pull/1004))
- feat: add support for Soroban PRC's `getLedgers` API interfaces. ([#992](https://github.com/StellarCN/py-stellar-base/pull/992))
- feat: add `stellar_sdk.contract.ContractClient` and `stellar_sdk.contract.ContractClientAsync`, this greatly reduces the difficulty of calling contracts, and you can learn more through the documentation and [examples](https://github.com/StellarCN/py-stellar-base/blob/main/examples/soroban_invoke_contract_function.py). ([#998](https://github.com/StellarCN/py-stellar-base/pull/998))

#### Breaking changes
- refactor!: The `EventInfo.paging_token` field has been marked as deprecated, use the `cursor` in `GetEventsResponse` instead. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- refactor!: The legacy `cost` field has been removed from `SimulateTransactionResponse`, parse it from `transaction_data` instead. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- feat!: support constructors in contract creation via `TransactionBuilder.append_create_contract_op`, the signature of the function has been changed. ([#979](https://github.com/StellarCN/py-stellar-base/pull/979))
- refactor!: Updated `signer` parameter in auth to accept a callable returning (public_key, signatures) instead of just public_key. ([#982](https://github.com/StellarCN/py-stellar-base/pull/982))

### Version 12.0.0-beta6

Released on November 26, 2024

#### Update
- feat: `scval.from_enum` and `scval.to_enum` now support multiple values. ([#1004](https://github.com/StellarCN/py-stellar-base/pull/1004))

### Version 12.0.0-beta5

Released on November 23, 2024

#### Update
- fix: fix a bug in `AssembledTransaction.simulate`. ([#1000](https://github.com/StellarCN/py-stellar-base/pull/1000))

### Version 12.0.0-beta4

Released on November 22, 2024

#### Update
- feat: add `stellar_sdk.contract.ContractClient` and `stellar_sdk.contract.ContractClientAsync`, this greatly reduces the difficulty of calling contracts, and you can learn more through the documentation and [examples](https://github.com/StellarCN/py-stellar-base/blob/main/examples/soroban_invoke_contract_function.py). ([#998](https://github.com/StellarCN/py-stellar-base/pull/998))

### Version 12.0.0-beta3

Released on November 14, 2024

Several hours ago, I released version 12.0.0-beta2, which added support for the Soroban RPC's getLedgers API interface. 
However, some field names in the implementation need to be renamed.

#### Update
- refactor: rename `LedgerInfo.ledger_header` to `LedgerInfo.header_xdr`, `LedgerInfo.ledger_metadata` to `LedgerInfo.metadata_xdr`. ([#994](https://github.com/StellarCN/py-stellar-base/pull/992))

### Version 12.0.0-beta2

Released on November 14, 2024

#### Update
- feat: add support for Soroban PRC's `getLedgers` API interfaces. ([#992](https://github.com/StellarCN/py-stellar-base/pull/992))

### Version 12.0.0-beta1

Released on November 01, 2024

#### Update
- refactor: add `paging_token` back to `EventInfo`. This is to ensure compatibility with older versions of Soroban-RPC. We still recommend using the `GetEventsResponse.cursor` field after upgrading Soroban-RPC. ([#990](https://github.com/StellarCN/py-stellar-base/pull/990))

### Version 12.0.0-beta0

Released on October 14, 2024

This is the first release that supports Protocol 22. While the network has not upgraded yet, 
you can start integrating the new features into your codebase if you want a head start.

#### Update
- feat: add support for Soroban PRC's `getVersionInfo` API interfaces. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- feat: Add `transaction_hash` to `GetTransactionResponse` and `GetTransactionsResponse`. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))

#### Breaking changes
- refactor!: The `paging_token` field has been removed from `EventInfo`, use the `cursor` in `GetEventsResponse` instead. (Reverted in 12.0.0-beta1) ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- refactor!: The legacy `cost` field has been removed from `SimulateTransactionResponse`, parse it from `transaction_data` instead. ([#984](https://github.com/StellarCN/py-stellar-base/pull/984))
- feat!: support constructors in contract creation via `TransactionBuilder.append_create_contract_op`, the signature of the function has been changed. ([#979](https://github.com/StellarCN/py-stellar-base/pull/979))
- refactor!: Updated `signer` parameter in auth to accept a callable returning (public_key, signatures) instead of just public_key. ([#982](https://github.com/StellarCN/py-stellar-base/pull/982))

### Version 11.1.0

Released on September 18, 2024

#### Update
- feat: add support for Soroban PRC's `getTransactions` and `getFeeStats` API interfaces. ([#960](https://github.com/StellarCN/py-stellar-base/pull/960))
- feat: add support for Horizon's `transactions_async` API interfaces. ([#961](https://github.com/StellarCN/py-stellar-base/pull/961))
- fix: fix `authorize_entry` to use the correct public key when passing `Keypair` as signer. ([#971](https://github.com/StellarCN/py-stellar-base/pull/971))
- feat: Expose `stellar_sdk.address.AddressType` for easy importing. ([#973](https://github.com/StellarCN/py-stellar-base/pull/973))
- chore: bump dependencies.

### Version 11.0.0

Released on July 16, 2024

#### Update
- feat: `SorobanServer.send_transaction` supports sending FeeBumpTransactionEnvelope. ([#956](https://github.com/StellarCN/py-stellar-base/pull/956))
- fix: Corrected the issue where `TransactionBuilder.from_xdr` could not properly parse transactions containing Soroban operations. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- fix: Corrected the issue where `FeeBumpTransactionEnvelope.from_xdr` could not properly parse transactions containing Soroban operations. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- refactor: `TransactionBuilder.from_xdr` previously could return `TransactionBuilder` or `FeeBumpTransactionEnvelope`. Now it will no longer return `TransactionBuilder`, but will return `TransactionEnvelope` or `FeeBumpTransactionEnvelope`. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- feat: `TransactionBuilder.build_fee_bump_transaction` now supports transactions containing Soroban operations. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- fix: fix the issue where invoking `SorobanServer.prepare_transaction` for transactions that have already set `SorobanData` could result in unexpected high fees. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- chore: bump dependencies.

#### Breaking changes
- refactor: `FeeBumpTransactionEnvelope.base_fee` has been removed. Please use `FeeBumpTransactionEnvelope.fee instead`. Note that their meanings are different: ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
  - `FeeBumpTransactionEnvelope.base_fee` represented the maximum fee you were willing to pay per operation for this transaction.
  - `FeeBumpTransactionEnvelope.fee` represents the maximum fee you are willing to pay for this transaction.
- refactor: `TransactionBuilder.from_xdr` previously could return `TransactionBuilder` or `FeeBumpTransactionEnvelope`. Now it will no longer return `TransactionBuilder`, but will return `TransactionEnvelope` or `FeeBumpTransactionEnvelope`. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))
- refactor: `helpers.parse_transaction_envelope_from_xdr` has been marked as deprecated. Please use the refactored `TransactionEnvelope.from_xdr` instead. ([#957](https://github.com/StellarCN/py-stellar-base/pull/957))

### Version 10.0.0

Released on May 15, 2024

#### Update
- improve: The function in `stellar_xdr.scval` can accept `sc_val` of `base64` and `bytes` types. ([#932](https://github.com/StellarCN/py-stellar-base/pull/932))
- feat: add support for Soroban-RPC 21. ([#933](https://github.com/StellarCN/py-stellar-base/pull/933))
- refactor: use `__repr__` instead of `__str__` in classes. ([#936](https://github.com/StellarCN/py-stellar-base/pull/936))
- feat: add a helper function to convert SCVal to native types. ([#937](https://github.com/StellarCN/py-stellar-base/pull/937))
- chore: updated various dependencies.

#### Breaking changes
- feat: add support for Soroban-RPC 21, you need to upgrade Soroban PRC to version v21 or above. ([#933](https://github.com/StellarCN/py-stellar-base/pull/933))

### Version 9.4.0

Released on May 01, 2024

#### Update
- chore: The generated XDR has been upgraded to match the upcoming Protocol 21, namely [stellar/stellar-xdr@v21.1](https://github.com/stellar/stellar-xdr/tree/v21.1). ([#927](https://github.com/StellarCN/py-stellar-base/pull/927))
- chore: updated various dependencies.

### Version 9.3.0

Released on March 13, 2024

#### Update
- feat: Add `Asset.contract_id()` for calculating the id of the asset contract. ([#901](https://github.com/StellarCN/py-stellar-base/pull/901))
- chore: throw an exception when the API does not provide streaming support. ([#878](https://github.com/StellarCN/py-stellar-base/pull/878))

### Version 9.2.0

Released on Jan 14, 2024

#### Update
- feat: add `scv.to_void` and `scv.from_void`. ([#863](https://github.com/StellarCN/py-stellar-base/pull/863))
- feat: Support for the new, optional `diagnostic_events_xdr` field on the `SorobanServer.send_transaction` method. ([#866](https://github.com/stellar/java-stellar-sdk/pull/866))
- chore: update dependencies.

### Version 9.1.3

Released on Jan 3, 2024

#### Update
- fix: fix the way of exporting modules to resolve pyright warnings. ([#858](https://github.com/StellarCN/py-stellar-base/pull/858))

### Version 9.1.2

Released on Dec 26, 2023

#### Update
- fix: mark GetTransactionResponse.create_at as Optional. ([#854](https://github.com/StellarCN/py-stellar-base/pull/854))

### Version 9.1.1

Released on Dec 16, 2023

#### Update
- improve: add the missing `create_at` field to `GetTransactionResponse`. ([#849](https://github.com/StellarCN/py-stellar-base/pull/849))

### Version 9.1.0

Released on Dec 16, 2023

#### Update
- feat: support resource leeway parameter when simulating Soroban transactions. ([#846](https://github.com/StellarCN/py-stellar-base/pull/846))
- refactor: the type of `GetEventsRequest.start_ledger` has changed from `str` to `int`. ([#847](https://github.com/StellarCN/py-stellar-base/pull/847))

### Version 9.0.0

Released on Dec 9, 2023

#### Update
- fix: fix the issue of incorrect handling of special horizon links on the Windows platform. ([#825](https://github.com/StellarCN/py-stellar-base/pull/825))
- chore: add support for Python 3.12. ([#799](https://github.com/StellarCN/py-stellar-base/pull/799))
- chore: `SorobanServer` uses testnet instead of futurenet by default ([#831](https://github.com/StellarCN/py-stellar-base/pull/831))

### Version 9.0.0-beta1

Released on Nov 15, 2023

#### Update
- refactor: make the `parameters` parameter in `TransactionBuilder.append_invoke_contract_function_op` optional. ([#789](https://github.com/StellarCN/py-stellar-base/pull/789))
- improve: sort the dictionary based on the key when calling `scval.to_struct`.  ([#817](https://github.com/StellarCN/py-stellar-base/pull/817))

#### Breaking changes
- chore: drop support for Python 3.7. ([#813](https://github.com/StellarCN/py-stellar-base/pull/813))
- refactor: replace `stellar-base-sseclient` with `requests-sse` to improve the stability of the stream. Previously, when encountering an error, it would throw a `ConnectionError`, but now it will throw a `StreamClientError`. ([#814](https://github.com/StellarCN/py-stellar-base/pull/814))
- feat: update the SDK to the stable Protocol 20 release, this contains some breaking updates, please check [#808](https://github.com/StellarCN/py-stellar-base/issues/808) for more information. ([#809](https://github.com/StellarCN/py-stellar-base/pull/809))

### Version 9.0.0-beta0

Released on September 20, 2023

#### Update
- feat: add helper functions to sign authorization entries. ([#776](https://github.com/StellarCN/py-stellar-base/pull/776))
- feat: add `SorobanServerAsync` to support asynchronous requests. ([#782](https://github.com/StellarCN/py-stellar-base/pull/782))

### Version 9.0.0-alpha2

Released on September 16, 2023

#### Update
- feat: add support for Soroban Preview 11 ([#777](https://github.com/StellarCN/py-stellar-base/pull/777))

### Version 9.0.0-alpha1

Released on Aug 28, 2023

#### Update
- fix: fix the issue where soroban data is not correctly set when building a transaction through TransactionBuilder. ([#770](https://github.com/StellarCN/py-stellar-base/pull/770))

### Version 9.0.0-alpha0

Released on Aug 27, 2023

#### Add
- feat: add support for Soroban Preview 10. Please check the examples in the `examples` folder to learn how to use it.

#### Update
- Runtime type checking has now been removed. Please use tools like mypy for type checking. ([#706](https://github.com/StellarCN/py-stellar-base/pull/706))
- Add `__hash__` to the xdr classes. ([#757](https://github.com/StellarCN/py-stellar-base/pull/757))
- Make `aiohttp` and `aiohttp-sse-client` as optional dependencies. ([#765](https://github.com/StellarCN/py-stellar-base/pull/765))
- Publishing to PyPI with a Trusted Publisher. ([#767](https://github.com/StellarCN/py-stellar-base/pull/767))
- Update dependencies.

#### Breaking changes
- Remove `ValueError`, `TypeError` and `AttributeError` from `stellar_sdk.exceptions`. ([#763](https://github.com/StellarCN/py-stellar-base/pull/763))


### Version 8.2.1

Released on June 22, 2023

#### Add
- feat: add comparison operators to Price class. ([#741](https://github.com/StellarCN/py-stellar-base/pull/741))

### Version 8.2.0

Released on March 15, 2023

#### Add
- feat: add support for SEP-0035. ([#711](https://github.com/StellarCN/py-stellar-base/pull/711))

#### Note
- Python 3.6 is no longer supported.

### Version 8.1.1

Released on October 12, 2022

#### Update
- docs: correct the horizon address of the public network ([#611](https://github.com/StellarCN/py-stellar-base/pull/611))
- deps: Update dependencies.

### Version 8.1.0

Released on June 13, 2022

#### Add

- feat: allow custom headers to be set in `stellar_sdk.client.requests_client.RequestsClient`. ([#600](https://github.com/StellarCN/py-stellar-base/pull/600))
- feat: allow custom headers to be set in `stellar_sdk.client.aiohttp_client.AiohttpClient`. ([#601](https://github.com/StellarCN/py-stellar-base/pull/601))

### Version 8.0.1

Released on June 06, 2022

#### Update

- Make some amount fields accept `Decimal`. ([#597](https://github.com/StellarCN/py-stellar-base/pull/597))
- Regenerate xdr files with the latest xdrgen. ([#595](https://github.com/StellarCN/py-stellar-base/pull/595))

### Version 8.0.0

Released on May 07, 2022

**This release includes breaking changes.**

**This release adds support for Protocol 19.**

It includes [CAP-21](https://stellar.org/protocol/cap-21) (new transaction preconditions) and [CAP-40](https://stellar.org/protocol/cap-40) (signed payload signers).

#### Breaking changes

- `Transaction.time_bounds` has been removed, please use `Transaction.preconditions.time_bounds` instead.
- No longer sets "now" as the default cursor for AiohttpClient.stream ([#591](https://github.com/StellarCN/py-stellar-base/pull/591))
- Some breaking updates are included in XDR, you can check the changes [here](https://github.com/stellar/stellar-protocol/blob/70cb1449c4/core/cap-0021.md#xdr-diff).

#### Add

- Support for converting signed payloads ([CAP-40](https://stellar.org/protocol/cap-40)) to and from their StrKey (`P...`) representation, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/ed25519_signed_payload.py).
  
- Support for creating transactions with the new preconditions ([CAP-21](https://stellar.org/protocol/cap-21)) via `TransactionBuilder`, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/preconditions.py).
  
  - `TransactionBuilder.set_ledger_bounds(min_ledger: int, max_ledger: int)`
    
  - `TransactionBuilder.set_min_sequence_number(min_sequence_number: int)`
    
  - `TransactionBuilder.set_min_sequence_age(min_sequence_age: int)`
    
  - `TransactionBuilder.set_min_sequence_ledger_gap(min_sequence_ledger_gap: int)`
    
  - `TransactionBuilder.add_extra_signer(signer_key: Union[SignerKey, SignedPayloadSigner, str])`
    
- Support for Signing transactions containing the ed25519 payload extra signer, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/preconditions.py).
  
  - `Keypair.sign_payload_decorated(data: bytes)`
  - `TransactionEnvelope.sign_extra_signers_payload(signer: Union[Keypair, str])`
- Support for CAP-21 has been added to `stellar_sdk.sep.txrep`.
  

#### Update

- feat: you can turn off runtime type checking by configuring `STELLAR_SDK_RUNTIME_TYPE_CHECKING=0` in environment variables. ([#589](https://github.com/StellarCN/py-stellar-base/pull/589))
  
  In order to make the program more rigorous and novice friendly, we previously introduced runtime type checking, but this would cause a significant performance penalty, so now we allow users to turn it off.
  
- refactor: remove runtime type checking in `stellar_sdk.xdr` package ([#584](https://github.com/StellarCN/py-stellar-base/pull/584))

### Version 8.0.0-beta4
Released on April 24, 2022

#### Breaking changes
* refactor: no longer sets "now" as the default cursor for AiohttpClient.stream ([#591](https://github.com/StellarCN/py-stellar-base/pull/591))

### Version 8.0.0-beta3
Released on April 24, 2022

#### Add
* feat: add `server.offers().for_account(account_id)` to retrieve the account's offers. ([#590](https://github.com/StellarCN/py-stellar-base/pull/590))

### Version 8.0.0-beta2
Released on April 20, 2022

**This is a pre-release version, please do not use it in production.**

#### Update
* feat: you can turn off runtime type checking by configuring `STELLAR_SDK_RUNTIME_TYPE_CHECKING=0` in environment variables. ([#589](https://github.com/StellarCN/py-stellar-base/pull/589))
  
  In order to make the program more rigorous and novice friendly, we previously introduced runtime type checking, but this would cause a significant performance penalty, so now we allow users to turn it off.

### Version 8.0.0-beta1
Released on April 19, 2022

**This is a pre-release version, please do not use it in production.**

#### Update
* refactor: remove runtime type checking in `stellar_sdk.xdr` package ([#584](https://github.com/StellarCN/py-stellar-base/pull/584))

### Version 8.0.0-beta0
Released on April 13, 2022

**This is a pre-release version, please do not use it in production.**

It includes [CAP-21](https://stellar.org/protocol/cap-21) (new transaction preconditions) and [CAP-40](https://stellar.org/protocol/cap-40) (signed payload signers).

#### Breaking changes

- `Transaction.time_bounds` is moved to `Transaction.preconditions.time_bounds`.
- Some breaking updates are included in XDR, you can check the changes [here](https://github.com/stellar/stellar-protocol/blob/70cb1449c4/core/cap-0021.md#xdr-diff).

#### Add

- Support for converting signed payloads ([CAP-40](https://stellar.org/protocol/cap-40)) to and from their StrKey (`P...`) representation, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/ed25519_signed_payload.py).

- Support for creating transactions with the new preconditions ([CAP-21](https://stellar.org/protocol/cap-21)) via `TransactionBuilder`, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/preconditions.py).

  - `TransactionBuilder.set_ledger_bounds(min_ledger: int, max_ledger: int)`

  - `TransactionBuilder.set_min_sequence_number(min_sequence_number: int)`

  - `TransactionBuilder.set_min_sequence_age(min_sequence_age: int)`

  - `TransactionBuilder.set_min_sequence_ledger_gap(min_sequence_ledger_gap: int)`

  - `TransactionBuilder.add_extra_signer(signer_key: Union[SignerKey, SignedPayloadSigner, str])`

- Support for Signing transactions containing the ed25519 payload extra signer, you can find the example [here](https://github.com/StellarCN/py-stellar-base/blob/v8/examples/preconditions.py).
  - `Keypair.sign_payload_decorated(data: bytes)`
  - `TransactionEnvelope.sign_extra_signers_payload(signer: Union[Keypair, str])`

-  Support for CAP-21 has been added to `stellar_sdk.sep.txrep`.

### Version 7.0.3
Released on April 24, 2022

#### Add
* feat: add `server.offers().for_account(account_id)` to retrieve the account's offers. ([#590](https://github.com/StellarCN/py-stellar-base/pull/590))

### Version 7.0.2
Released on April 07, 2022

#### Update
* fix: fixed-length arrays pack/unpack should not include length, but the previous releases incorrectly include it. ([#581](https://github.com/StellarCN/py-stellar-base/pull/581))

### Version 7.0.1
Released on February 23, 2022

#### Update
* feat: make stellar_sdk.Asset hashable. ([#576](https://github.com/StellarCN/py-stellar-base/pull/576))

### Version 7.0.0
Released on January 12, 2022

**This update includes breaking changes.**

This release introduces unconditional support for muxed accounts. ([#574](https://github.com/StellarCN/py-stellar-base/pull/574))

#### Breaking changes
* In [v4.0.0](https://github.com/StellarCN/py-stellar-base/releases/tag/4.0.0), we introduced opt-in support for muxed accounts, 
  you would need to set `ENABLE_SEP_0023` to `true` in the environment variable to enable support for this feature. 
  In the new release, this feature will be enabled by default. ([#574](https://github.com/StellarCN/py-stellar-base/pull/574))
  
#### Add
* Introduced a helper function which lets you pre-determine the hex claimable balance ID of a CreateClaimableBalance operation prior to submission to the network: ([#575](https://github.com/StellarCN/py-stellar-base/pull/575))

  ```python
  class Transaction:
      def get_claimable_balance_id(self, operation_index: int) -> str:
          pass
  ```

#### Update
* When the user builds a transaction through TransactionBuilder but does not set TimeBounds, the SDK will give a warning. ([#565](https://github.com/StellarCN/py-stellar-base/pull/565))
* `stellar_sdk.xdr` module adds some validation to the data. ([#564](https://github.com/StellarCN/py-stellar-base/pull/564))

### Version 6.1.1
Released on November 24, 2021

#### Update
* Specify the version of urllib3 >= 1.26.7 and < 2.0.0. ([#563](https://github.com/StellarCN/py-stellar-base/pull/563))

### Version 6.1.0
Released on November 17, 2021

#### Add
* feat: add a way to filter liquidity pools by participating account. ([#558](https://github.com/StellarCN/py-stellar-base/pull/558))

### Version 6.0.1
Released on November 15, 2021

#### Update
* Upgrade outdated third-party dependencies.

### Version 6.0.0
Released on November 13, 2021

**This update includes breaking changes.**

#### Note

- As we introduced in the [5.0.0](https://github.com/StellarCN/py-stellar-base/releases/tag/5.0.0) release log, this release contains almost no new features, but contains a lot of refactorings, which improve the quality of the code and reduce the chance of users making mistakes.
- I would like to draw your attention to the changes in `TransactionBuilder`. This update changes some functions that have not been changed since v0.1.x, and I know that this change will affect many existing tutorials and programs, so please pay particular attention to this.

#### Update

- Added a `py.typed` file so that mypy will know to use our type annotations, **I strongly recommend that you use it in development**. ([#543](https://github.com/StellarCN/py-stellar-base/pull/543))
- Strictly check whether the type of data input by the user meets the requirements, and if it does not, `TypeError` will be thrown.  ([#542](https://github.com/StellarCN/py-stellar-base/pull/542)) ([#544](https://github.com/StellarCN/py-stellar-base/pull/544))
- `universal_account_id` attribute has been added to `stellar_sdk.MuxedAccount` and `stellar_sdk.Account`, please turn to the documentation to find out more. ([#548](https://github.com/StellarCN/py-stellar-base/pull/548))
- Improve document.

#### Breaking changes

- `stellar_sdk.Server` can now only be used to send synchronous requests, if you need to send asynchronous requests, use `stellar_sdk.ServerAsync` instead.  ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))
- The signature of the following function contained in `stellar_sdk.TransactionBuilder` has changed: ([#547](https://github.com/StellarCN/py-stellar-base/pull/))
  - append_change_trust_op
  - append_payment_op
  - append_path_payment_strict_receive_op
  - append_path_payment_strict_send_op
  - append_manage_buy_offer_op
  - append_manage_sell_offer_op
  - append_create_passive_sell_offer_op


- `append_change_trust_liquidity_pool_asset_op` in `stellar_sdk.TransactionBuilder` has been removed, please use `append_change_trust_op` instead. ([#547](https://github.com/StellarCN/py-stellar-base/pull/547))

- The initialization function for `stellar_sdk.Account` has changed, previously it was  `def __init__(self, account_id: Union[str, MuxedAccount], sequence: int)` and now it is  `def __init__(self, account: Union[str, MuxedAccount], sequence: int, raw_data: Dict[str, Any])`.  ([#548](https://github.com/StellarCN/py-stellar-base/pull/548))

- `stellar_sdk.exceptions.ValueError`, `stellar_sdk.exceptions.TypeError` and `stellar_sdk.exceptions.AttributeError` are no longer subclass of `stellar_sdk.exceptions.SdkError`, they are now aliases for Python's built-in functions. ([#549](https://github.com/StellarCN/py-stellar-base/pull/549))

- The previous type of `stellar_sdk.BaseTransactionEnvelope.signatures` was `stellar_sdk.xdr.DecoratedSignature`, now it is `stellar_sdk.DecoratedSignature`. ([#538](https://github.com/StellarCN/py-stellar-base/pull/538))

- `stellar_sdk.sep.federation.resolve_stellar_address` and `stellar_sdk.sep.federation.resolve_account_id` can also only be used to send synchronization requests, please `stellar_sdk.sep.federation.resolve_stellar_address_async` and `stellar_sdk.sep.federation.resolve_account_id_async` to send asynchronous requests. ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))

- `stellar_sdk.sep.stellar_toml.fetch_stellar_toml` can also only be used to send synchronization requests, please `stellar_sdk.sep.stellar_toml.fetch_stellar_toml_async`  to send asynchronous requests. ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))

- The initialization function for `stellar_sdk.SignerKey` has changed, previously it was  `def __init__(self, signer_key: stellar_xdr.SignerKey)` and now it is `def __init__(self, signer_key: bytes, signer_key_type: SignerKeyType)`, the attribute contained therein has been changed accordingly. ([#537](https://github.com/StellarCN/py-stellar-base/pull/537))

- `clear_flags` and `set_flags` in `stellar_sdk.operation.SetOptions` have been changed to `stellar_sdk.operation.AuthorizationFlag` type, previously it was `int`. ([#528](https://github.com/StellarCN/py-stellar-base/pull/528))

- the client's `USER_AGENT` and `IDENTIFICATION_HEADERS` are changed to "py-stellar-base" ([#550](https://github.com/StellarCN/py-stellar-base/pull/550))

- The types of the following attribute may have previously varied with the type of the parameters entered by the user, but now they are deterministic: ([#528](https://github.com/StellarCN/py-stellar-base/pull/528))

  | attribute                                                  | current type |
  | ---------------------------------------------------------- | ------------ |
  | stellar_sdk.operation.ChangeTrust.limit                    | str          |
  | stellar_sdk.operation.Clawback.amount                      | str          |
  | stellar_sdk.operation.CreateAccount.starting_balance       | str          |
  | stellar_sdk.operation.CreateClaimableBalance.amount        | str          |
  | stellar_sdk.operation.CreatePassiveSellOffer.amount        | str          |
  | stellar_sdk.operation.CreatePassiveSellOffer.price         | Price        |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_amount_a    | str          |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_amount_b    | str          |
  | stellar_sdk.operation.LiquidityPoolDeposit.min_price       | Price        |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_price       | Price        |
  | stellar_sdk.operation.LiquidityPoolWithdraw.amount         | str          |
  | stellar_sdk.operation.LiquidityPoolWithdraw.min_amount_a   | str          |
  | stellar_sdk.operation.LiquidityPoolWithdraw.min_amount_b   | str          |
  | stellar_sdk.operation.ManageBuyOffer.amount                | str          |
  | stellar_sdk.operation.ManageBuyOffer.price                 | Price        |
  | stellar_sdk.operation.ManageSellOffer.amount               | str          |
  | stellar_sdk.operation.ManageSellOffer.price                | Price        |
  | stellar_sdk.operation.PathPaymentStrictReceive.send_max    | str          |
  | stellar_sdk.operation.PathPaymentStrictReceive.dest_amount | str          |
  | stellar_sdk.operation.PathPaymentStrictSend.send_amount    | str          |
  | stellar_sdk.operation.PathPaymentStrictSend.dest_min       | str          |
  | stellar_sdk.operation.Payment.amount                       | str          |

### Version 6.0.0-beta3
Released on November 01, 2021

**This is a pre-release version, please do not use it in production.**

#### Update

- Added more test cases.

### Version 6.0.0-beta2
Released on October 29, 2021

**This is a pre-release version, please do not use it in production.**

#### Update

- Improve documentation.
- refactor: optimize the implementation of StrKey. ([#551](https://github.com/StellarCN/py-stellar-base/pull/551))

### Version 6.0.0-beta1
Released on October 26, 2021

**This update includes breaking changes.**
**This is a pre-release version, please do not use it in production.**

#### Breaking changes

- refactor: the client's `USER_AGENT` and `IDENTIFICATION_HEADERS` are changed to "py-stellar-base" ([#550](https://github.com/StellarCN/py-stellar-base/pull/550))

### Version 6.0.0-beta0
Released on October 25, 2021

**This update includes breaking changes.**
**This is a pre-release version, please do not use it in production.**

#### Note

As we introduced in the [5.0.0](https://github.com/StellarCN/py-stellar-base/releases/tag/5.0.0) release log, this release contains almost no new features, but contains a lot of refactorings, which improve the quality of the code and reduce the chance of users making mistakes.

#### Update

- Added a `py.typed` file so that mypy will know to use our type annotations, **I strongly recommend that you use it in development**. ([#543](https://github.com/StellarCN/py-stellar-base/pull/543))
- Strictly check whether the type of data input by the user meets the requirements, and if it does not, `TypeError` will be thrown.  ([#542](https://github.com/StellarCN/py-stellar-base/pull/542)) ([#544](https://github.com/StellarCN/py-stellar-base/pull/544))
- `universal_account_id` attribute has been added to `stellar_sdk.MuxedAccount` and `stellar_sdk.Account`, please turn to the documentation to find out more. ([#548](https://github.com/StellarCN/py-stellar-base/pull/548))
- Improve document.

#### Breaking changes

- `stellar_sdk.Server` can now only be used to send synchronous requests, if you need to send asynchronous requests, use `stellar_sdk.ServerAsync` instead.  ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))
- The signature of the following function contained in `stellar_sdk.TransactionBuilder` has changed: ([#547](https://github.com/StellarCN/py-stellar-base/pull/))
  - append_change_trust_op
  - append_payment_op
  - append_path_payment_strict_receive_op
  - append_path_payment_strict_send_op
  - append_manage_buy_offer_op
  - append_manage_sell_offer_op
  - append_create_passive_sell_offer_op


- `append_change_trust_liquidity_pool_asset_op` in `stellar_sdk.TransactionBuilder` has been removed, please use `append_change_trust_op` instead. ([#547](https://github.com/StellarCN/py-stellar-base/pull/547))

- The initialization function for `stellar_sdk.Account` has changed, previously it was  `def __init__(self, account_id: Union[str, MuxedAccount], sequence: int)` and now it is  `def __init__(self, account: Union[str, MuxedAccount], sequence: int, raw_data: Dict[str, Any])`.  ([#548](https://github.com/StellarCN/py-stellar-base/pull/548))

- `stellar_sdk.exceptions.ValueError`, `stellar_sdk.exceptions.TypeError` and `stellar_sdk.exceptions.AttributeError` are no longer subclass of `stellar_sdk.exceptions.SdkError`, they are now aliases for Python's built-in functions. ([#549](https://github.com/StellarCN/py-stellar-base/pull/549))

- The previous type of `stellar_sdk.BaseTransactionEnvelope.signatures` was `stellar_sdk.xdr.DecoratedSignature`, now it is `stellar_sdk.DecoratedSignature`. ([#538](https://github.com/StellarCN/py-stellar-base/pull/538))

- `stellar_sdk.sep.federation.resolve_stellar_address` and `stellar_sdk.sep.federation.resolve_account_id` can also only be used to send synchronization requests, please `stellar_sdk.sep.federation.resolve_stellar_address_async` and `stellar_sdk.sep.federation.resolve_account_id_async` to send asynchronous requests. ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))

- `stellar_sdk.sep.stellar_toml.fetch_stellar_toml` can also only be used to send synchronization requests, please `stellar_sdk.sep.stellar_toml.fetch_stellar_toml_async`  to send asynchronous requests. ([#540](https://github.com/StellarCN/py-stellar-base/pull/540))

- The initialization function for `stellar_sdk.SignerKey` has changed, previously it was  `def __init__(self, signer_key: stellar_xdr.SignerKey)` and now it is `def __init__(self, signer_key: bytes, signer_key_type: SignerKeyType)`, the attribute contained therein has been changed accordingly. ([#537](https://github.com/StellarCN/py-stellar-base/pull/537))

- `clear_flags` and `set_flags` in `stellar_sdk.operation.SetOptions` have been changed to `stellar_sdk.operation.AuthorizationFlag` type, previously it was `int`. ([#528](https://github.com/StellarCN/py-stellar-base/pull/528))

- The types of the following attribute may have previously varied with the type of the parameters entered by the user, but now they are deterministic: ([#528](https://github.com/StellarCN/py-stellar-base/pull/528))

  | attribute                                                  | current type |
  | ---------------------------------------------------------- | ------------ |
  | stellar_sdk.operation.ChangeTrust.limit                    | str          |
  | stellar_sdk.operation.Clawback.amount                      | str          |
  | stellar_sdk.operation.CreateAccount.starting_balance       | str          |
  | stellar_sdk.operation.CreateClaimableBalance.amount        | str          |
  | stellar_sdk.operation.CreatePassiveSellOffer.amount        | str          |
  | stellar_sdk.operation.CreatePassiveSellOffer.price         | Price        |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_amount_a    | str          |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_amount_b    | str          |
  | stellar_sdk.operation.LiquidityPoolDeposit.min_price       | Price        |
  | stellar_sdk.operation.LiquidityPoolDeposit.max_price       | Price        |
  | stellar_sdk.operation.LiquidityPoolWithdraw.amount         | str          |
  | stellar_sdk.operation.LiquidityPoolWithdraw.min_amount_a   | str          |
  | stellar_sdk.operation.LiquidityPoolWithdraw.min_amount_b   | str          |
  | stellar_sdk.operation.ManageBuyOffer.amount                | str          |
  | stellar_sdk.operation.ManageBuyOffer.price                 | Price        |
  | stellar_sdk.operation.ManageSellOffer.amount               | str          |
  | stellar_sdk.operation.ManageSellOffer.price                | Price        |
  | stellar_sdk.operation.PathPaymentStrictReceive.send_max    | str          |
  | stellar_sdk.operation.PathPaymentStrictReceive.dest_amount | str          |
  | stellar_sdk.operation.PathPaymentStrictSend.send_amount    | str          |
  | stellar_sdk.operation.PathPaymentStrictSend.dest_min       | str          |
  | stellar_sdk.operation.Payment.amount                       | str          |


### Version 5.0.1
Released on November 10, 2021

#### Update
* Upgrade outdated third-party dependencies.

### Version 5.0.0
Released on October 06, 2021

**This update includes breaking changes.**

#### Note

- This release adds support for Automated Market Makers. For details, you can refer to [CAP-38](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0038.md) for XDR changes and [this document](https://docs.google.com/document/d/1pXL8kr1a2vfYSap9T67R-g72B_WWbaE1YsLMa04OgoU/view) for detailed changes to the Horizon API. ([Download Horizon Liquidity Pool API.pdf](https://github.com/StellarCN/py-stellar-base/files/7199228/Horizon.Liquidity.Pool.API.pdf)) 
- You can get a simple example of CAP-38 [here](https://github.com/StellarCN/py-stellar-base/blob/55943959958ae6c80170f5ddfd6616a61c104122/examples/amm.py).
- Although this update is a major version update, but only the `stellar.xdr` module contains breaking changes, if you don’t directly rely on this module in your code, you should be able to migrate easily.
- I want to make some improvements to the SDK, but I don’t want to introduce too many breaking changes in this version, so I plan to postpone it to the next major version. The next major version features will not include feature updates, I will do my best to make it easy to migrate.
- I will not be adding Stellar Protocol 18 support to v2.x. I will only provide the necessary security updates and will end support for it on 2022.01.01.

#### Add ([#512](https://github.com/StellarCN/py-stellar-base/pull/512) [#517](https://github.com/StellarCN/py-stellar-base/pull/517) [#518](https://github.com/StellarCN/py-stellar-base/pull/518))

- Introduced new CAP-38 operations `LiquidityPoolDeposit` and `LiquidityPoolWithdraw`.
- Introduced two new types of assets, `LiquidityPoolId` and `LiquidityPoolAsset`.
- The following functions have been added to `TransactionBuilder`:
  - `append_liquidity_pool_deposit_op`
  - `append_liquidity_pool_withdraw_op`
  - `append_revoke_liquidity_pool_sponsorship_op`
  - `append_change_trust_liquidity_pool_asset_op`
- Introduced a `LiquidityPoolsCallBuilder` to make calls to a new endpoint, you can use `Server.liquidity_pools` to build it.
- Expanded the `TransactionsCallBuilder`, `OperationsCallBuilder`, `TradesCallBuilder` and `EffectsCallBuilder` to apply to specific liquidity pools.
- Expanded the `TradesCallBuilder` to support fetching liquidity pool trades and accepts a new `trade_type` filter.
- Update SEP-11 to support CAP-38 

#### Breaking changes ([#512](https://github.com/StellarCN/py-stellar-base/pull/512))

- This XDR file contains breaking changes, you can click [here](https://github.com/StellarCN/py-stellar-base/commit/bffd02dfe9487a254c0c6ceaae889db380ba878a) to view the changes.

### Version 5.0.0-beta3
Released on September 23, 2021

**This is a pre-release version, please do not use it in production.**

* fix: SEP-10, fix case where muxed accounts are not enabled. ([#530](https://github.com/StellarCN/py-stellar-base/pull/530))

### Version 4.2.2
Released on September 23, 2021

#### Update
* fix: SEP-10, fix case where muxed accounts are not enabled. ([#530](https://github.com/StellarCN/py-stellar-base/pull/530))

### Version 5.0.0-beta2
Released on September 21, 2021

**This is a pre-release version, please do not use it in production.**

This beta release adds support for Automated Market Makers. For details, you can refer to [CAP-38](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0038.md) for XDR changes and [this document](https://docs.google.com/document/d/1pXL8kr1a2vfYSap9T67R-g72B_WWbaE1YsLMa04OgoU/view) for detailed changes to the Horizon API.

#### Add

* feat: add `/liquidity_pools/:pool_id/trades` endpoint support. ([#527](https://github.com/StellarCN/py-stellar-base/pull/527))
* Contains the updates provided in [v4.2.0](https://github.com/StellarCN/py-stellar-base/releases/tag/4.2.0) and [v4.2.1](https://github.com/StellarCN/py-stellar-base/releases/tag/4.2.1).

### Version 4.2.1
Released on September 18, 2021

#### Update
* add check for muxed accounts in `verify_challenge_transaction()`. ([#525](https://github.com/StellarCN/py-stellar-base/pull/525))
* `read_challenge_transaction()` now checks `timebounds.min_time` with a 5-minute grace period to account for clock drift. ([#526](https://github.com/StellarCN/py-stellar-base/pull/526))

### Version 4.2.0
Released on September 17, 2021

#### Update

* Updated the following SEP-10 utility functions to be compliant with the protocols ([#521](https://github.com/StellarCN/py-stellar-base/pull/521), [stellar-protocol/#1036](https://github.com/stellar/stellar-protocol/pull/1036)):
  - Updated `build_challenge_transaction()` to accept muxed accounts (`M...`) for client account IDs.
  - Updated `build_challenge_transaction()` to accept a `memo` parameter to attach to the challenge transaction.
  - Updated `ChallengeTransaction` to provide a `memo` property.
  - Updated `read_challenge_transaction()` to validate challenge transactions with muxed accounts (`M...`) as the client account ID.
  
### Version 5.0.0-beta1
Released on September 11, 2021

**This update includes breaking changes.**

**This is a pre-release version, please do not use it in production.**

#### Note

- Although this update is a major version update, but only the `stellar.xdr` module contains breaking changes, if you don’t directly rely on this module in your code, you should be able to migrate easily.
- I want to make some improvements to the SDK, but I don’t want to introduce too many breaking changes in this version, so I plan to postpone it to the next major version. The next major version features will not include feature updates, I will do my best to make it easy to migrate.
- I will not be adding Stellar Protocol 18 support to v2.x. I will only provide the necessary security updates and will end support for it on 2022.01.01.
- Since Stellar Protocol 18 has not yet been deployed to the test network, I have not provided relevant examples for the time being, I will provide it later.

#### Add ([#512](https://github.com/StellarCN/py-stellar-base/pull/512) [#517](https://github.com/StellarCN/py-stellar-base/pull/517) [#518](https://github.com/StellarCN/py-stellar-base/pull/518))

- Introduced new CAP-38 operations `LiquidityPoolDeposit` and `LiquidityPoolWithdraw`.
- Introduced two new types of assets, `LiquidityPoolId` and `LiquidityPoolAsset`.
- The following functions have been added to `TransactionBuilder`:
  - `append_liquidity_pool_deposit_op`
  - `append_liquidity_pool_withdraw_op`
  - `append_revoke_liquidity_pool_sponsorship_op`
  - `append_change_trust_liquidity_pool_asset_op`
- Introduced a `LiquidityPoolsCallBuilder` to make calls to a new endpoint, you can use `Server.liquidity_pools` to build it.
- Expanded the `TransactionsCallBuilder`, `OperationsCallBuilder`, and `EffectsCallBuilder` to apply to specific liquidity pools.
- Expanded the `TradesCallBuilder` to support fetching liquidity pool trades and accepts a new `trade_type` filter.
- Update SEP-11 to support CAP-38 
#### Breaking changes ([#512](https://github.com/StellarCN/py-stellar-base/pull/512))

- This XDR file contains breaking changes, you can click [here](https://github.com/StellarCN/py-stellar-base/commit/bffd02dfe9487a254c0c6ceaae889db380ba878a) to view the changes.

### Version 5.0.0-beta0
Released on September 05, 2021

**This update includes breaking changes.**

**This is a pre-release version, please do not use it in production.**

#### Note

- Although this update is a major version update, it only **contains a small number of breaking changes**, and you should be able to migrate easily.
- I want to make some improvements to the SDK, but I don’t want to introduce too many breaking changes in this version, so I plan to postpone it to the next major version. The next major version features will not include feature updates, I will make it as easy to migrate as possible, thanks.
- I will not be adding Stellar Protocol 18 support to v2.x. I will only provide the necessary security updates and will end support for it on 2022.01.01.
- Since Stellar Protocol 18 has not yet been deployed to the test network, I have not provided relevant examples for the time being, I will provide it later.

#### Add ([#512](https://github.com/StellarCN/py-stellar-base/pull/512))

- Introduced new CAP-38 operations `LiquidityPoolDeposit` and `LiquidityPoolWithdraw`.
- Introduced two new types of assets, `LiquidityPoolId` and `LiquidityPoolAsset`.
- The following functions have been added to `TransactionBuilder`:
  - `append_liquidity_pool_deposit_op`
  - `append_liquidity_pool_withdraw_op`
  - `append_revoke_liquidity_pool_sponsorship_op`
- Introduced a `LiquidityPoolsCallBuilder` to make calls to a new endpoint, you can use `Server.liquidity_pools` to build it.
- Expanded the `TransactionsCallBuilder`, `OperationsCallBuilder`, and `EffectsCallBuilder` to apply to specific liquidity pools.
- Expanded the `TradesCallBuilder` to support fetching liquidity pool trades and accepts a new `trade_type` filter.

#### Breaking changes ([#512](https://github.com/StellarCN/py-stellar-base/pull/512))

- This XDR file contains breaking changes, you can click [here](https://github.com/StellarCN/py-stellar-base/commit/bffd02dfe9487a254c0c6ceaae889db380ba878a) to view the changes.
- Due to the introduction of new asset types, the signature of `TransactionBuilder.append_change_trust_op` has been changed.  ([c152dbb](https://github.com/StellarCN/py-stellar-base/commit/c152dbbf8cb7e18e93f900b3fce8f6d86b1ec6ad))

  Formerly:

  ```python
  def append_change_trust_op(
      self,
      asset_code: str,
      asset_issuer: str,
      limit: Union[str, Decimal] = None,
      source: Optional[Union[MuxedAccount, str]] = None,
  ) -> "TransactionBuilder":
      pass
  ```

  Now:

  ```python
  def append_change_trust_op(
      self,
      asset: Union[Asset, LiquidityPoolAsset],
      limit: Union[str, Decimal] = None,
      source: Optional[Union[MuxedAccount, str]] = None,
  ) -> "TransactionBuilder":
      pass
  ```

### Version 4.1.1
Released on August 23, 2021

#### Update
* fix: AiohttpClient.__str__() references missing instance attribute self.pool_size. ([#511](https://github.com/StellarCN/py-stellar-base/pull/511))
* refactor: use binascii.crc_hqx to calculate checksum. ([#507](https://github.com/StellarCN/py-stellar-base/pull/507))
* chore: upgrade package dependencies.

### Version 4.1.0
Released on July 28, 2021

#### Update
* feat: SEP-0011, add support for the following operations: ([#502](https://github.com/StellarCN/py-stellar-base/pull/502))
	- CreateClaimableBalance
	- ClaimClaimableBalance
	- BeginSponsoringFutureReserves
    - EndSponsoringFutureReserves
	- RevokeSponsorship
	- Clawback
	- ClawbackClaimableBalance
	- SetTrustLineFlags

- feat: SEP-0011, add support for the muxed account. ([#503](https://github.com/StellarCN/py-stellar-base/pull/503))

  If you want to enable this feature, please set `ENABLE_SEP_0023` to `true` in the environment variable; otherwise, you will encounter exceptions when processing with muxed account, check [here](https://github.com/StellarCN/py-stellar-base/releases/tag/4.1.0) for more detail.

- feat: SEP-0011, add comments to txrep to improve readability. ([#504](https://github.com/StellarCN/py-stellar-base/pull/504))

### Version 4.0.0
Released on June 30, 2021

**This update includes breaking changes.**

#### Added:

* feat: add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md) and [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#479](https://github.com/StellarCN/py-stellar-base/pull/479) [#492](https://github.com/StellarCN/py-stellar-base/pull/492) [#493](https://github.com/StellarCN/py-stellar-base/pull/493)):

  SEP-0023 is still a Draft, so currently we do not enable it by default. If you want to enable this feature, please set `ENABLE_SEP_0023` to `true` in the environment variable

#### Breaking changes

* The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#479](https://github.com/StellarCN/py-stellar-base/pull/479)):

  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`
  - `stellar_sdk.operation.Clawback.from_`
  
* `stellar_sdk.operation.Operation.source` previously returned `Optional[str]`, now it returns `Optional[stellar_sdk.MuxedAccount]`. ([#479](https://github.com/StellarCN/py-stellar-base/pull/479))

* `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction` previously returned a tuple, now it returns `stellar_sdk.sep.stellar_web_authentication.ChallengeTransaction`. ([#454](https://github.com/StellarCN/py-stellar-base/pull/454))

* The `v1` parameter in the `stellar_sdk.Transaction.from_xdr_object` and `stellar_sdk.Transaction.from_xdr` functions is set to `True` by default. ([#494](https://github.com/StellarCN/py-stellar-base/pull/494))

#### Deprecated

* `stellar_sdk.Account.account_id` has been marked as deprecated, it will be removed in v5.0.0, use `stellar_sdk.Account.account` instead.  ([#479](https://github.com/StellarCN/py-stellar-base/pull/479))

### Example

If you want to enable SEP-0023 support, please set `ENABLE_SEP_0023` to `true` in the environment variable, on Linux and MacOS, generally you can use `export ENABLE_SEP_0023=true` to set it.

- MuxedAccount

  ```python
  from stellar_sdk import MuxedAccount
  
  account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
  account_muxed_id = 1234
  account_muxed = "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
  
  # generate account_muxed
  muxed = MuxedAccount(account_id=account_id, account_muxed_id=1234)  # account_muxed_id is optional.
  print(f"account_muxed: {muxed.account_muxed}")  # `account_muxed` returns `None` if `account_muxed_id` is `None`.
  
  # parse account_muxed
  muxed = MuxedAccount.from_account(account_muxed)
  print(f"account_id: {muxed.account_id}\naccount_muxed_id: {muxed.account_muxed_id}")
  ```

- Pay to muxed account

  ```python
  import pprint
  
  from stellar_sdk import Keypair, Server, MuxedAccount, TransactionBuilder, Network
  
  horizon_url = "https://horizon-testnet.stellar.org/"
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  alice_secret = "SAHN2RCKC5I7NFDCIUKA3BG4H4T6WMLLGSAZVDKUHF7PQXHMYWD7UAIH"
  bob_account = MuxedAccount(
      account_id="GBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46UMF",
      account_muxed_id=1234,
  )
  print(f"account_id_muxed: {bob_account.account_muxed}")
  # You can also use addresses starting with M.
  # bob_account = "MBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46AAAAAAAAAAE2L2QE"
  
  alice_keypair = Keypair.from_secret(alice_secret)
  
  server = Server(horizon_url=horizon_url)
  alice_account = server.load_account(alice_keypair.public_key)
  transaction = TransactionBuilder(
      source_account=alice_account,
      network_passphrase=network_passphrase,
      base_fee=100
  ) \
      .append_payment_op(destination=bob_account, amount="100", asset_code="XLM") \
      .build()
  
  transaction.sign(alice_keypair)
  resp = server.submit_transaction(transaction)
  pprint.pprint(resp)
  ```

### Version 4.0.0-beta0
Released on June 29, 2021

**This update includes breaking changes.**

**This is a pre-release version, please do not use it in production.**

#### Added:

* feat: add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md) and [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#479](https://github.com/StellarCN/py-stellar-base/pull/479) [#492](https://github.com/StellarCN/py-stellar-base/pull/492) [#493](https://github.com/StellarCN/py-stellar-base/pull/493)):

  SEP-0023 is still a Draft, so currently we do not enable it by default. If you want to enable this feature, please set `ENABLE_SEP_0023` to `true` in the environment variable

#### Breaking changes

* The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#479](https://github.com/StellarCN/py-stellar-base/pull/479)):

  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`
  - `stellar_sdk.operation.Clawback.from_`
  
* `stellar_sdk.operation.Operation.source` previously returned `Optional[str]`, now it returns `Optional[stellar_sdk.MuxedAccount]`. ([#479](https://github.com/StellarCN/py-stellar-base/pull/479))

* `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction` previously returned a tuple, now it returns `stellar_sdk.sep.stellar_web_authentication.ChallengeTransaction`. ([#454](https://github.com/StellarCN/py-stellar-base/pull/454))

#### Deprecated

* `stellar_sdk.Account.account_id` has been marked as deprecated, it will be removed in v5.0.0, use `stellar_sdk.Account.account` instead.  ([#479](https://github.com/StellarCN/py-stellar-base/pull/479))

### Example

If you want to enable SEP-0023 support, please set `ENABLE_SEP_0023` to `true` in the environment variable, on Linux and MacOS, generally you can use `export ENABLE_SEP_0023=true` to set it.

- MuxedAccount

  ```python
  from stellar_sdk import MuxedAccount
  
  account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
  account_muxed_id = 1234
  account_muxed = "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
  
  # generate account_muxed
  muxed = MuxedAccount(account_id=account_id, account_muxed_id=1234)  # account_muxed_id is optional.
  print(f"account_muxed: {muxed.account_muxed}")  # `account_muxed` returns `None` if `account_muxed_id` is `None`.
  
  # parse account_muxed
  muxed = MuxedAccount.from_account(account_muxed)
  print(f"account_id: {muxed.account_id}\naccount_muxed_id: {muxed.account_muxed_id}")
  ```

- Pay to muxed account

  ```python
  import pprint
  
  from stellar_sdk import Keypair, Server, MuxedAccount, TransactionBuilder, Network
  
  horizon_url = "https://horizon-testnet.stellar.org/"
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  alice_secret = "SAHN2RCKC5I7NFDCIUKA3BG4H4T6WMLLGSAZVDKUHF7PQXHMYWD7UAIH"
  bob_account = MuxedAccount(
      account_id="GBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46UMF",
      account_muxed_id=1234,
  )
  print(f"account_id_muxed: {bob_account.account_muxed}")
  # You can also use addresses starting with M.
  # bob_account = "MBZSQ3YZMZEWL5ZRCEQ5CCSOTXCFCMKDGFFP4IEQN2KN6LCHCLI46AAAAAAAAAAE2L2QE"
  
  alice_keypair = Keypair.from_secret(alice_secret)
  
  server = Server(horizon_url=horizon_url)
  alice_account = server.load_account(alice_keypair.public_key)
  transaction = TransactionBuilder(
      source_account=alice_account,
      network_passphrase=network_passphrase,
      base_fee=100
  ) \
      .append_payment_op(destination=bob_account, amount="100", asset_code="XLM") \
      .build()
  
  transaction.sign(alice_keypair)
  resp = server.submit_transaction(transaction)
  pprint.pprint(resp)
  ```

### Version 3.3.5
Released on June 03, 2021

#### Update
* feat: add support for claimable balances endpoints. ([#491](https://github.com/StellarCN/py-stellar-base/pull/491))

### Version 3.3.4
Released on May 18, 2021

#### Update
* refactor: use the pure Python implemented crc16 module instead of the C implemented. ([#483](https://github.com/StellarCN/py-stellar-base/pull/483))

### Version 3.3.3
Released on May 15, 2021

#### Update
* fix: correct the type of `stellar_sdk.xdr.SponsorshipDescriptor.sponsorship_descriptor` from `AccountID` to `Optional[AccountID]`. ([#478](https://github.com/StellarCN/py-stellar-base/pull/478))

### Version 3.3.2
Released on May 06, 2021

#### Update

* fix: fix an import related bug and optimize the import code. ([#473](https://github.com/StellarCN/py-stellar-base/pull/473))
* example: added clawback operation [example](https://github.com/StellarCN/py-stellar-base/blob/bbdf42dd75/examples/clawback.py). ([#474](https://github.com/StellarCN/py-stellar-base/pull/474))

### Version 3.3.1
Released on April 25, 2021

#### Update

* fix: remove exceptions that should not be thrown in XDR. ([#469](https://github.com/StellarCN/py-stellar-base/pull/469))

### Version 3.3.0
Released on April 17, 2021

#### Update

* feat: add support for Stellar Protocol 17. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

#### Added

* feat: add support for [CAP-35](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0035.md). ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_clawback_op
  - append_clawback_claimable_balance_op
  - append_set_trust_line_flags_op

* `AUTHORIZATION_CLAWBACK_ENABLED` has been added in `stellar_sdk.operation.set_options.AuthorizationFlag`. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

#### Deprecated

* `stellar_sdk.TransactionBuilder.append_allow_trust_op` and `stellar_sdk.operation.AllowTrust` have now been marked as deprecated, they will be removed in v4.0.0. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

### Version 2.13.0
Released on April 17, 2021

#### Update

* feat: add support for Stellar Protocol 17. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

#### Added

* feat: add support for [CAP-35](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0035.md). ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_clawback_op
  - append_clawback_claimable_balance_op
  - append_set_trust_line_flags_op

* `AUTHORIZATION_CLAWBACK_ENABLED` has been added in `stellar_sdk.operation.set_options.Flag`. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

#### Deprecated

* `stellar_sdk.TransactionBuilder.append_allow_trust_op` and `stellar_sdk.operation.AllowTrust` have now been marked as deprecated, they will be removed in v4.0.0. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

### Version 3.2.1
Released on April 16, 2021

#### Update
fix: fix the issue that `not_predicate` cannot be parsed normally. ([#465](https://github.com/StellarCN/py-stellar-base/pull/465))

### Version 3.3.0-beta0
Released on April 03, 2021

#### Update

* feat: add support for Stellar Protocol 17. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

#### Added

* feat: add support for [CAP-35](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0035.md). ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_clawback_op
  - append_clawback_claimable_balance_op
  - append_set_trust_line_flags_op

* `AUTHORIZATION_CLAWBACK_ENABLED` has been added in `stellar_sdk.operation.set_options.AuthorizationFlag`. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

#### Deprecated

* `stellar_sdk.TransactionBuilder.append_allow_trust_op` and `stellar_sdk.operation.AllowTrust` have now been marked as deprecated, they will be removed in v4.0.0. ([#453](https://github.com/StellarCN/py-stellar-base/pull/453))

### Version 2.13.0-beta0
Released on April 03, 2021

#### Update

* feat: add support for Stellar Protocol 17. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

#### Added

* feat: add support for [CAP-35](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0035.md). ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_clawback_op
  - append_clawback_claimable_balance_op
  - append_set_trust_line_flags_op

* `AUTHORIZATION_CLAWBACK_ENABLED` has been added in `stellar_sdk.operation.set_options.Flag`. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

#### Deprecated

* `stellar_sdk.TransactionBuilder.append_allow_trust_op` and `stellar_sdk.operation.AllowTrust` have now been marked as deprecated, they will be removed in v4.0.0. ([#446](https://github.com/StellarCN/py-stellar-base/pull/446))

### Version 3.2.0
Released on April 01, 2021

#### Update
feat: SEP-10: added support for 'client_domain' ManageData operations in challenges (client attribution). ([#428](https://github.com/StellarCN/py-stellar-base/pull/428))

### Version 2.12.0
Released on April 01, 2021

#### Update
feat: SEP-10: added support for 'client_domain' ManageData operations in challenges (client attribution). ([#428](https://github.com/StellarCN/py-stellar-base/pull/428))

### Version 2.12.0-beta0
Released on Mar 25, 2021

#### Update
feat: SEP-10: added support for 'client_domain' ManageData operations in challenges (client attribution). ([#428](https://github.com/StellarCN/py-stellar-base/pull/428))

### Version 3.1.4
Released on Mar 16, 2021

#### Update
* fix: make `AiohttpClient` compatible with Python 3.6 and 3.7. ([#449](https://github.com/StellarCN/py-stellar-base/pull/449))

### Version 2.11.3
Released on Mar 16, 2021

#### Update
* fix: make `AiohttpClient` compatible with Python 3.6 and 3.7. ([#449](https://github.com/StellarCN/py-stellar-base/pull/449))

### Version 3.1.3
Released on Mar 4, 2021

#### Update
* fix: throw stellar_sdk.exceptions.ConnectionError in AiohttpClient instead of the built-in ConnectionError. ([#441](https://github.com/StellarCN/py-stellar-base/pull/441))

### Version 2.11.2
Released on Mar 4, 2021

#### Update
* fix: throw stellar_sdk.exceptions.ConnectionError in AiohttpClient instead of the built-in ConnectionError. ([#441](https://github.com/StellarCN/py-stellar-base/pull/441))

### Version 3.1.2
Released on Feb 28, 2021

#### Update
* Update dependencies.
  
  The latest version of aiohttp includes [security updates](https://github.com/aio-libs/aiohttp/security/advisories/GHSA-v6wp-4m6f-gcjg), this security issue has no direct impact on this SDK. ([#437](https://github.com/StellarCN/py-stellar-base/pull/437))

### Version 3.1.1
Released on Jan 20, 2021

#### Update
* fix: SEP-10, removed non-null constraint for manageData op values. ([#424](https://github.com/StellarCN/py-stellar-base/pull/424))

### Version 2.11.1
Released on Jan 20, 2021

#### Update
* fix: SEP-10, removed non-null constraint for manageData op values. ([#424](https://github.com/StellarCN/py-stellar-base/pull/424))

### Version 3.1.0
Released on Jan 19, 2021

#### Breaking changes
* Updates the SEP-10 utility function parameters to support [SEP-10 v3.1.0](https://github.com/stellar/stellar-protocol/commit/6c8c9cf6685c85509835188a136ffb8cd6b9c11c).

    - The following functions add the `web_auth_domain` parameter:
        - `stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction()`

### Version 2.11.0
Released on Jan 19, 2021

#### Breaking changes
* Updates the SEP-10 utility function parameters to support [SEP-10 v3.1.0](https://github.com/stellar/stellar-protocol/commit/6c8c9cf6685c85509835188a136ffb8cd6b9c11c).

    - The following functions add the `web_auth_domain` parameter:
        - `stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction()`

### Version 3.0.0

Released on Jan 06, 2021

**This update include breaking changes.**

**The v2.x version will continue to be maintained until at least Jun 01, 2021.**

I've upgraded [django-polaris](https://github.com/stellar/django-polaris/pull/369) to stellar-sdk 3.0.0, perhaps this can be used as a reference for the upgrade.

This release brings new XDR code generated by the new XDR generator, with type hint support, if you need to use XDR objects, this release will bring a great experience improvement.

#### Breaking changes
- The old XDR code has been completely removed, and you can find the new XDR code [here](https://github.com/StellarCN/py-stellar-base/tree/c45d0874db5feccefe7ba57b7141eb06e064e09b/.xdr). ([#383](https://github.com/StellarCN/py-stellar-base/pull/383))

  The XDR Object returned by the following functions has changed:

  - Asset.to_xdr_object()
  - TransactionEnvelope.to_xdr_object()
  - FeeBumpTransaction.to_xdr_object()
  - TransactionEnvelope.to_xdr_object()
  - Keypair.xdr_public_key()
  - Keypair.xdr_account_id()
  - Keypair.xdr_muxed_account()
  - Keypair.sign_decorated()
  - Memo.to_xdr_object() (All types of Memos.)
  - ClaimPredicate.to_xdr_object()
  - Claimant.to_xdr_object()
  - Operation.to_xdr_object() (All types of Operations.)
  - Price.to_xdr_object()
  - Signer.to_xdr_object()
  - SignerKey.to_xdr_object()
  - TimeBounds.to_xdr_object()

- Rename the parameter name that accepts XDR Object in the `from_xdr_object` functions to `xdr_object`. ([#384](https://github.com/StellarCN/py-stellar-base/pull/384))
  
  This change affects the following functions:
  
  - Asset.from_xdr_object(cls, asset_xdr_object: stellar_xdr.Asset)
  - FeeBumpTransaction.from_xdr_object(cls, te_xdr_object: stellar_xdr.TransactionEnvelope, cls, te_xdr_object: stellar_xdr.TransactionEnvelope)
  - Memo.from_xdr_object(cls, xdr_obj: stellar_xdr.Memo) (All types of Memos.)
  - Opeartion.from_xdr_object(cls, operation_xdr_object: stellar_xdr.Operation) (All types of Operations.)
  - Price.from_xdr_object(cls, price_xdr_object: stellar_xdr.Price)
  - Signer.from_xdr_object(cls, signer_xdr_object: stellar_xdr.Signer)
  - SignerKey.from_xdr_object(cls, xdr_object: stellar_xdr.SignerKey)
  - TimeBounds.from_xdr_object(cls, time_bounds_xdr_object: stellar_xdr.TimeBounds)
  - Transaction.from_xdr_object(cls, tx_xdr_object: Union[stellar_xdr.Transaction, stellar_xdr.TransactionV0], v1: bool = False)
  - TransactionEnvelope.from_xdr_object(cls, te_xdr_object: stellar_xdr.TransactionEnvelope, network_passphrase: str)

- Remove Operation.type_code(). ([#390](https://github.com/StellarCN/py-stellar-base/pull/390))
  
- Remove deprecated classes and functions. ([#389](https://github.com/StellarCN/py-stellar-base/pull/389))
  
  The following classes and functions were marked as deprecated in v2, and now we have removed them.
  
  Classes:
  
  - stellar_sdk.call_builder.paths_call_builder.PathsCallBuilder

  - stellar_sdk.operation.path_payment.PathPayment
  
  Functions:

  - stellar_sdk.call_builder.accounts_call_builder.AccountsCallBuilder.signer(self, signer: str)

  - stellar_sdk.call_builder.accounts_call_builder.AccountsCallBuilder.asset(self, asset: Asset)

  - stellar_sdk.call_builder.offers_call_builder.OffersCallBuilder.account(self, account_id: str)

  - stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client(challenge_transaction: str, server_account_id: str, domain_name: str, network_passphrase: str)

  - stellar_sdk.server.Server.paths(selfsource_account: str, destination_account: str, destination_asset: Asset, destination_amount: str)

  - stellar_sdk.transaction_builder.TransactionBuilder.append_path_payment_op(self, destination: str, send_code: str, send_issuer: Optional[str], send_max: Union[str, Decimal], dest_code: str, dest_issuer: Optional[str], dest_amount: Union[str, Decimal], path: List[Asset], source: str = None)

- Rename `stellar_sdk.operation.set_options.Flag` to `stellar_sdk.operation.set_options.AuthorizationFlag`.

#### Update

- add missing `__str__` and `__equals__` functions. ([#385](https://github.com/StellarCN/py-stellar-base/pull/385))

#### Tips

- Parse XDR into XDR object, the resolved object has complete type hint support, and you can also analyze it through the debug tool(such as PyCharm Debugger).

  ```python
  from stellar_sdk.xdr import TransactionEnvelope
  
  xdr = "AAAAAgAAAAA1y7+IlEXtO3+d01lKBazo8wCpZsqsEItW7y2WHv2sOgAAAfQAD5ZNAAQJtwAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAGAQSwhD6XHfd4T2PjJc088ZwWyrfxr6Tcq7baksg1EHAAAAAlNJTEFVU0QAAAAAAAAAAABgEEsIQ+lx33eE9j4yXNPPGcFsq38a+k3Ku22pLINRBwAAAAAC+vCAAAAAAAAAAAEe/aw6AAAAQEDTXnTMoAwF7zM/dWDLAmxA02mVSXdqAbUzs1N/pJtrkOwlEk021zLnjTEo/5FeYGDaNktS8RemgQDYPxoL1QY="
  te = TransactionEnvelope.from_xdr(xdr)
  ...
  ```
 
### Version 3.0.0-beta5
Released on Jan 06, 2021

#### Update
- Add `from_xdr_amount` and `to_xdr_amount` to stellar_sdk.xdr.utils. ([#419](https://github.com/StellarCN/py-stellar-base/pull/419))

#### Breaking changes
- Rename `stellar_sdk.operation.set_options.Flag` to `stellar_sdk.operation.set_options.AuthorizationFlag`.
- Remove `TYPE` field in Operations. ([#418](https://github.com/StellarCN/py-stellar-base/pull/418))

### Version 2.10.1
Released on Dec 22, 2020

#### Update
* Upgrade dependencies so that this SDK can run on Apple M1 Chip.

### Version 2.10.1-beta0
Released on Dec 22, 2020

#### Update
* Upgrade dependencies so that this SDK can run on Apple M1 Chip.

### Version 3.0.0-beta4
Released on Dec 29, 2020

#### Update
* Upgrade dependencies.

### Version 2.10.0

Released on Nov 15, 2020

**This update include breaking changes**

#### Breaking changes
* feat: check the mnemonic is correct before using it to generate the seed. ([#406](https://github.com/StellarCN/py-stellar-base/pull/406))
    - A parameter named `language` is added to `stellar_sdk.keypair.Keypair.from_mnemonic_phrase()`.

### Version 3.0.0-beta3
Released on Nov 11, 2020

#### Update
* feat: updates the SEP-10 utility function parameters and return values to support [SEP-10 v3.0](https://github.com/stellar/stellar-protocol/commit/9d121f98fd2201a5edfe0ed2befe92f4bf88bfe4)  ([#400](https://github.com/StellarCN/py-stellar-base/pull/400))
* refactor: change the type of Operation.TYPE_CODE from `stellar_sdk.xdr.OperationType` to `str`. ([#401](https://github.com/StellarCN/py-stellar-base/pull/401))

### Version 3.0.0-beta2
Released on Nov 07, 2020

#### Update
* refactor: change the type of Operation.TYPE_CODE from `stellar_sdk.xdr.OperationType` to `str`. ([#401](https://github.com/StellarCN/py-stellar-base/pull/401))

### Version 3.0.0-beta1
Released on Nov 01, 2020

#### Update
* Add mypy check and bug fix. ([#398](https://github.com/StellarCN/py-stellar-base/pull/398))
* Fix wrong type hinting.

### Version 3.0.0-beta0

Released on Oct 22, 2020

**This update include breaking changes.**

**This is a pre-release version, please do not use it in production.**

This release brings new XDR code generated by the new XDR generator, with type hint support, if you need to use XDR objects, this release will bring a great experience improvement.

#### Breaking changes
- The old XDR code has been completely removed, and you can find the new XDR code [here](https://github.com/StellarCN/py-stellar-base/tree/c45d0874db5feccefe7ba57b7141eb06e064e09b/.xdr). ([#383](https://github.com/StellarCN/py-stellar-base/pull/383))

  The XDR Object returned by the following functions has changed:

  - Asset.to_xdr_object()
  - TransactionEnvelope.to_xdr_object()
  - FeeBumpTransaction.to_xdr_object()
  - TransactionEnvelope.to_xdr_object()
  - Keypair.xdr_public_key()
  - Keypair.xdr_account_id()
  - Keypair.xdr_muxed_account()
  - Keypair.sign_decorated()
  - Memo.to_xdr_object() (All types of Memos.)
  - ClaimPredicate.to_xdr_object()
  - Claimant.to_xdr_object()
  - Operation.to_xdr_object() (All types of Operations.)
  - Price.to_xdr_object()
  - Signer.to_xdr_object()
  - SignerKey.to_xdr_object()
  - TimeBounds.to_xdr_object()

- Rename the field that accepts XDR Object in the `from_xdr_object` function to `xdr_object`. ([#384](https://github.com/StellarCN/py-stellar-base/pull/384))
  
  This change affects the following functions:
  
  - Asset.from_xdr_object(cls, asset_xdr_object: stellar_xdr.Asset)
  - FeeBumpTransaction.from_xdr_object(cls, te_xdr_object: stellar_xdr.TransactionEnvelope, cls, te_xdr_object: stellar_xdr.TransactionEnvelope)
  - Memo.from_xdr_object(cls, xdr_obj: stellar_xdr.Memo) (All types of Memos.)
  - Opeartion.from_xdr_object(cls, operation_xdr_object: stellar_xdr.Operation) (All types of Operations.)
  - Price.from_xdr_object(cls, price_xdr_object: stellar_xdr.Price)
  - Signer.from_xdr_object(cls, signer_xdr_object: stellar_xdr.Signer)
  - SignerKey.from_xdr_object(cls, xdr_object: stellar_xdr.SignerKey)
  - TimeBounds.from_xdr_object(cls, time_bounds_xdr_object: stellar_xdr.TimeBounds)
  - Transaction.from_xdr_object(cls, tx_xdr_object: Union[stellar_xdr.Transaction, stellar_xdr.TransactionV0], v1: bool = False)
  - TransactionEnvelope.from_xdr_object(cls, te_xdr_object: stellar_xdr.TransactionEnvelope, network_passphrase: str)

- Remove Operation.type_code(), and add Operation.TYPE_CODE, it returns `stellar_sdk.xdr.OperationType`. ([#390](https://github.com/StellarCN/py-stellar-base/pull/390))
  
- Remove deprecated classes and functions. ([#389](https://github.com/StellarCN/py-stellar-base/pull/389))
  
  The following classes and functions were marked as deprecated in v2, and now we have removed them.
  
  Classes:
  
  - stellar_sdk.call_builder.paths_call_builder.PathsCallBuilder

  - stellar_sdk.call_builder.payments_call_builder.PaymentsCallBuilder

  - stellar_sdk.operation.path_payment.PathPayment
  
  Functions:

  - stellar_sdk.call_builder.accounts_call_builder.AccountsCallBuilder.signer(self, signer: str)

  - stellar_sdk.call_builder.accounts_call_builder.AccountsCallBuilder.asset(self, asset: Asset)

  - stellar_sdk.call_builder.offers_call_builder.OffersCallBuilder.account(self, account_id: str)

  - stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client(challenge_transaction: str, server_account_id: str, domain_name: str, network_passphrase: str)

  - stellar_sdk.server.Server.paths(selfsource_account: str, destination_account: str, destination_asset: Asset, destination_amount: str)

  - stellar_sdk.server.Server.payments(self)

  - stellar_sdk.transaction_builder.TransactionBuilder.append_path_payment_op(self, destination: str, send_code: str, send_issuer: Optional[str], send_max: Union[str, Decimal], dest_code: str, dest_issuer: Optional[str], dest_amount: Union[str, Decimal], path: List[Asset], source: str = None)

#### Updated

- add missing `__str__` and `__equals__` functions. ([#385](https://github.com/StellarCN/py-stellar-base/pull/385))

#### Tips

- Parse XDR into XDR object, the resolved object has complete type hint support, and you can also analyze it through the debug tool(such as PyCharm Debugger).

  ```python
  from stellar_sdk.xdr import TransactionEnvelope
  
  xdr = "AAAAAgAAAAA1y7+IlEXtO3+d01lKBazo8wCpZsqsEItW7y2WHv2sOgAAAfQAD5ZNAAQJtwAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAGAQSwhD6XHfd4T2PjJc088ZwWyrfxr6Tcq7baksg1EHAAAAAlNJTEFVU0QAAAAAAAAAAABgEEsIQ+lx33eE9j4yXNPPGcFsq38a+k3Ku22pLINRBwAAAAAC+vCAAAAAAAAAAAEe/aw6AAAAQEDTXnTMoAwF7zM/dWDLAmxA02mVSXdqAbUzs1N/pJtrkOwlEk021zLnjTEo/5FeYGDaNktS8RemgQDYPxoL1QY="
  te = TransactionEnvelope.from_xdr(xdr)
  ...
  ```

### Version 2.9.0

Released on Nov 11, 2020

**This update include breaking changes**

#### Breaking changes
* Updates the SEP-10 utility function parameters and return values to support [SEP-10 v3.0](https://github.com/stellar/stellar-protocol/commit/9d121f98fd2201a5edfe0ed2befe92f4bf88bfe4) ([#400](https://github.com/StellarCN/py-stellar-base/pull/400))

    - The following functions replaced the `domain_name` parameter with `home_domains`:

        - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction()`

    - The following function replaced the `domain_name` parameter with `home_domain`:
        - `stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction()`

    - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()` now returns an additional object attribute, `matched_home_domain`


### Version 2.8.1

Released on Oct 15, 2020

#### Update
* feat: add support for SEP-0010 v2.1.0. ([#380](https://github.com/StellarCN/py-stellar-base/pull/380))

In SEP-10 SEP-0010 v2.1.0, the `domain_name` field is no longer needed, but we still keep it to reduce breaking changes.


### Version 2.8.0

Released on Oct 04, 2020

**This update include breaking changes**

#### Update

* feat: add support for Stellar Protocol 14. ([#367](https://github.com/StellarCN/py-stellar-base/pull/367))

#### Added

- feat: add support for [CAP-23](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0023.md). ([#371](https://github.com/StellarCN/py-stellar-base/pull/371))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_create_claimable_balance_op
  - append_claim_claimable_balance_op

  We have added `ClaimPredicate`, please use helper function to build ClaimPredicate, method list:

  - predicate_and
  - predicate_or
  - predicate_not
  - predicate_before_absolute_time
  - predicate_before_relative_time
  - predicate_unconditional

  The following is an [example](https://github.com/StellarCN/py-stellar-base/blob/9a6f1e4a3dbf2693016e678b108737b3a7cfb967/examples/claimable_balances.py).

  ```python
  from stellar_sdk import Server, TransactionBuilder, Keypair, ClaimPredicate, Claimant, Asset, Network
  
  sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
  claimant_secret = "SBOLGU7D7A7MTY4JZ3WZUKSKB6NZBQFNQG3BZT4HZW4AAVZJRG7TWXGQ"
  
  sponsor_keypair = Keypair.from_secret(sponsor_secret)
  claimant_keypair = Keypair.from_secret(claimant_secret)
  
  server = Server("https://horizon-testnet.stellar.org")
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  # Create Claimable Balance
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  
  predicate_left = ClaimPredicate.predicate_before_relative_time(60 * 60 * 24 * 7)
  predicate_right = ClaimPredicate.predicate_not(ClaimPredicate.predicate_before_relative_time(60 * 3))
  predicate = ClaimPredicate.predicate_and(predicate_left, predicate_right)
  claimant = Claimant(destination=claimant_keypair.public_key, predicate=predicate)
  create_claimable_balance_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_create_claimable_balance_op(
      asset=Asset.native(),
      amount="100",
      claimants=[claimant],
      source=sponsor_keypair.public_key
  ).build()
  create_claimable_balance_te.sign(sponsor_keypair)
  create_claimable_balance_resp = server.submit_transaction(create_claimable_balance_te)
  print(create_claimable_balance_resp)
  
  # Claim Claimable Balance
  balance_id = "00000000550e14acbdafcd3089289363b3b0c8bec9b4edd87298c690655b4b2456d68ba0"
  claimant_account = server.load_account(claimant_keypair.public_key)
  claim_claimable_balance_te = TransactionBuilder(
      source_account=claimant_account,
      network_passphrase=network_passphrase
  ).append_claim_claimable_balance_op(
      balance_id=balance_id,
      source=claimant_keypair.public_key
  ).build()
  
  claim_claimable_balance_te.sign(claimant_keypair)
  claim_claimable_balance_resp = server.submit_transaction(claim_claimable_balance_te)
  print(claim_claimable_balance_resp)
  ```

- feat: add support for [CAP-33](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0033.md). ([#372](https://github.com/StellarCN/py-stellar-base/pull/372) [#374](https://github.com/StellarCN/py-stellar-base/pull/374))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_begin_sponsoring_future_reserves_op
  - append_end_sponsoring_future_reserves_op
  - append_revoke_account_sponsorship_op
  - append_revoke_trustline_sponsorship_op
  - append_revoke_offer_sponsorship_op
  - append_revoke_data_sponsorship_op
  - append_revoke_claimable_balance_sponsorship_op
  - append_revoke_ed25519_public_key_signer_sponsorship_op
  - append_revoke_hashx_signer_sponsorship_op
  - append_revoke_pre_auth_tx_signer_sponsorship_op

  The following is an [example](https://github.com/StellarCN/py-stellar-base/blob/9a6f1e4a3dbf2693016e678b108737b3a7cfb967/examples/sponsored_reserves.py).

  ```python
  from stellar_sdk import Server, TransactionBuilder, Keypair, Network
  
  sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
  new_account_secret = "SCN5D72JHQAHUHGIA23SLS3LBYCPHJWD7HLYNJRBBZIG4PD74UCGQBYM"
  
  sponsor_keypair = Keypair.from_secret(sponsor_secret)
  newly_created_keypair = Keypair.from_secret(new_account_secret)
  
  server = Server("https://horizon-testnet.stellar.org")
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  # Sponsoring Account Creation
  # https://github.com/stellar/stellar-protocol/blob/master/core/cap-0033.md#example-sponsoring-account-creation
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  sponsoring_account_creation_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_begin_sponsoring_future_reserves_op(
      sponsored_id=newly_created_keypair.public_key,
      source=sponsor_keypair.public_key
  ).append_create_account_op(
      destination=newly_created_keypair.public_key,
      starting_balance="10",
      source=sponsor_keypair.public_key
  ).append_end_sponsoring_future_reserves_op(
      source=newly_created_keypair.public_key
  ).build()
  sponsoring_account_creation_te.sign(sponsor_keypair)
  sponsoring_account_creation_te.sign(new_account_secret)
  sponsoring_account_creation_resp = server.submit_transaction(sponsoring_account_creation_te)
  print(sponsoring_account_creation_resp)
  
  # Revoke Account Sponsorship
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  revoke_account_sponsorship_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_revoke_account_sponsorship_op(
      account_id=newly_created_keypair.public_key,
      source=sponsor_keypair.public_key
  ).build()
  revoke_account_sponsorship_te.sign(sponsor_keypair)
  revoke_account_sponsorship_resp = server.submit_transaction(revoke_account_sponsorship_te)
  print(revoke_account_sponsorship_resp)
  ```

- feat: add support for new endpoint of Protocol 14. ([#373](https://github.com/StellarCN/py-stellar-base/pull/373))

  The following are the newly added endpoints.

  - server.claimable_balances().claimable_balance(claimable_balance_id)
  - server.claimable_balances().for_asset(asset)
  - server.claimable_balances().for_sponsor(sponsor)
  - server.claimable_balances().for_claimant(claimant)
  - server.accounts().for_sponsor(sponsor)
  - server.offers().for_sponsor(sponsor)

#### Breaking changes

* The type of `stellar_sdk.signer.Signer.signer_key` is changed from  `Xdr.types.SignerKey` to  `stellar_sdk.signer_key.SignerKey`.

### Version 2.7.0

Released on Aug 28, 2020

**This update include breaking changes**

#### Update
* feat: add support for SEP-0010 v2.0.0. ([#363](https://github.com/StellarCN/py-stellar-base/pull/363))

#### Breaking changes

Due to the addition of support for SEP-10 v2.0.0, we no longer support SEP-10 v1.x. 

The **domain_name** parameter is required in SEP-10, and the **anchor_name** parameter is no longer needed, you can get these SEP-10 changes [here](https://github.com/stellar/stellar-protocol/pull/708).

There have been some breaking changes to SEP-10 related functions, the following is a breaking changes list, you can also check our [latest document](https://stellar-sdk.readthedocs.io/en/2.7.0/api.html#sep-0010-stellar-web-authentication).

- stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction (**domain_name** parameter is required, **anchor_name**  parameter has been removed.)
- stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction (**domain_name** parameter is required)


### Version 2.6.4

Released on Aug 14, 2020

#### Added
* feat: add support for parsing Stellar URI (SEP-0007). ([#360](https://github.com/StellarCN/py-stellar-base/pull/360))

### Version 2.6.3

Released on Aug 09, 2020

#### Added
* feat: add support to SEP-0011 (Txrep: human-readable low-level representation of Stellar transactions). ([#357](https://github.com/StellarCN/py-stellar-base/pull/357))

### Version 2.6.2

Released on Jul 20, 2020

#### Added
* feat: add support for SEP-0007 (URI Scheme to facilitate delegated signing). ([#349](https://github.com/StellarCN/py-stellar-base/pull/349))

### Version 2.6.1

Released on Jun 21, 2020

**This update has breaking changes compared to 2.5.3.**

For [some reason](https://github.com/StellarCN/py-stellar-base/issues/338), we yanked [2.6.0](https://pypi.org/project/stellar-sdk/2.6.0/) on PyPi, 
but actually 2.6.0 can be used normally. 

This update log will contain the updated content of 2.6.0.

#### Update
- Optimize SEP-10, when you call `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key`, 
  an exception will be thrown if the transaction contains extra signatures. ([#338](https://github.com/StellarCN/py-stellar-base/pull/338)) (2.6.1)
- Generate V1 transactions by default. ([#337](https://github.com/StellarCN/py-stellar-base/pull/337)) (2.6.0)
- Allow V0 transactions to be fee bumped. ([#331](https://github.com/StellarCN/py-stellar-base/pull/331)) (2.6.0)

#### Breaking changes
- The default values of the following parameters have changed, 
  they used to default to False, but now they default to True. (2.6.0)
    - the `v1` parameter in stellar_sdk.transaction_builder.TransactionBuilder
    - the `v1` parameter in stellar_sdk.transaction.Transaction
    
### Version 2.6.0

Released on Jun 18, 2020

**This update include breaking changes**

#### Update
- Generate V1 transactions by default. ([#337](https://github.com/StellarCN/py-stellar-base/pull/337))
- Allow V0 transactions to be fee bumped. ([#331](https://github.com/StellarCN/py-stellar-base/pull/331))

#### Breaking changes
- The default values of the following parameters have changed, 
  they used to default to False, but now they default to True.
    - the `v1` parameter in stellar_sdk.transaction_builder.TransactionBuilder
    - the `v1` parameter in stellar_sdk.transaction.Transaction

### Version 2.5.3

Released on Jun 14, 2020

#### Fixed
- Set the value of the `v1` property correctly when calling TransactionBuilder.from_xdr. ([#333](https://github.com/StellarCN/py-stellar-base/pull/333))


### Version 2.5.2

Released on Jun 03, 2020

#### Update
- Optimized the way to read xdr. In 2.5.x, we will discard the id in muxed account, 
    in this update, we will keep the id, but it is invisible to users. 
    We recommend that all users using 2.5.x upgrade to this version. ([#326](https://github.com/StellarCN/py-stellar-base/pull/326))
  
### Version 2.5.1

Released on May 27, 2020

#### Added

- add `stellar_sdk.call_builder.PaymentsCallBuilder.join` ([#323](https://github.com/StellarCN/py-stellar-base/pull/323))

  ```python
  from stellar_sdk import Server
  
  horizon_url = "https://horizon.stellar.org/"
  account_id = "GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A"
  server = Server(horizon_url)
  # Set `join` to `transactions` to include the transactions which created each of the payments in the response.
  resp = server.payments().for_account(account_id).include_failed(False).join("transactions").call()
  print(resp)
  ```

### Version 2.5.0

Released on May 25, 2020

**This update include breaking changes**

In [2.4.0](https://github.com/StellarCN/py-stellar-base/releases/tag/2.4.0), we added support for Stellar Protocol 13, it also includes support for M-strkeys ([SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md)), but now we are going to remove support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md), because it is still a draft and may not be promoted to final, adding support for it means that users may end up storing M-strkeys, which can create a lot of problems if [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md) ends up not being implemented. If you want to know more details, please click [here](https://github.com/StellarCN/py-stellar-base/issues/304#issuecomment-632876302).

#### Update

- Revert support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

#### Breaking changes

- `stellar_sdk.muxed_account.MuxedAccount` has been removed. ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

- we will no longer accept the M-strkeys address, when resolving the XDR, if it contains a muxed account, only the G-strkeys will be resolved, and the id will be discarded.

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `str` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `stellar_sdk.Keypair` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  
### Version 2.5.0-alpha1

Released on May 23, 2020

**This update include breaking changes**

In [2.4.0](https://github.com/StellarCN/py-stellar-base/releases/tag/2.4.0), we added support for Stellar Protocol 13, it also includes support for M-strkeys ([SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md)), but now we are going to remove support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md), because it is still a draft and may not be promoted to final, adding support for it means that users may end up storing M-strkeys, which can create a lot of problems if [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md) ends up not being implemented. If you want to know more details, please click [here](https://github.com/StellarCN/py-stellar-base/issues/304#issuecomment-632876302).

#### Update

- Revert support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

#### Breaking changes

- `stellar_sdk.muxed_account.MuxedAccount` has been removed. ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

- we will no longer accept the M-strkeys address, when resolving the XDR, if it contains a muxed account, only the G-strkeys will be resolved, and the id will be discarded.

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `str` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `stellar_sdk.Keypair` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  
### Version 2.4.2

Released on May 23, 2020

- refactor: separating client GET and POST timeout values. ([#315](https://github.com/StellarCN/py-stellar-base/pull/315))

- refactor: optimize the use of `stellar_sdk.client.AiohttpClient`, it may throw a `stellar_sdk.exceptions.StreamClientError` exception now, and you should catch it. ([#317](https://github.com/StellarCN/py-stellar-base/pull/317))

  ```python
  import asyncio
  import logging
  
  from stellar_sdk import AiohttpClient, Server
  from stellar_sdk.exceptions import StreamClientError
  
  horizon_url = "https://horizon.stellar.org"
  
  async def listen_transaction():
      async with Server(horizon_url, AiohttpClient()) as server:
          cursor = "now"
          while True:
              try:
                  async for transaction in server.transactions().cursor(cursor).stream():
                      print(f"Transaction: {transaction}")
              except StreamClientError as e:
                  logging.error(f'A StreamClientError was encountered while reading the SSE message, which was caused by {e.current_cursor}.')
                  cursor = e.current_cursor
  
  
  if __name__ == '__main__':
      asyncio.run(listen_transaction())
  ```
  
### Version 2.4.2-alpha2

Released on May 18, 2020

- fix: monkey patch `aiohttp.streams.StreamReader.readline` to solve the problem that `aiohttp_sse_client` cannot read long stream messages.


### Version 2.4.2-alpha1

Released on May 17, 2020

- refactor: separating client GET and POST timeout values. (#315)

- refactor: optimize the use of `stellar_sdk.client.AiohttpClient`, it may throw a `stellar_sdk.exceptions.StreamClientError` exception now, and you should catch it. (#317)

  ```python
  import asyncio
  import logging
  
  from stellar_sdk import AiohttpClient, Server
  from stellar_sdk.exceptions import StreamClientError
  
  horizon_url = "https://horizon.stellar.org"
  
  async def listen_transaction():
      async with Server(horizon_url, AiohttpClient()) as server:
          cursor = "now"
          while True:
              try:
                  async for transaction in server.transactions().cursor(cursor).stream():
                      print(f"Transaction: {transaction}")
              except StreamClientError as e:
                  logging.error(f'A StreamClientError was encountered while reading the SSE message, which was caused by {e.current_cursor}.')
                  cursor = e.current_cursor
  
  
  if __name__ == '__main__':
      asyncio.run(listen_transaction())
  ```


### Version 2.4.1

Released on May 10, 2020

- fix type hint for `stellar_sdk.Server.submit_transaction()`.
- fix broken links in examples.


### Version 2.4.0

Released on May 05, 2020

**This update include breaking changes**.

This version brings protocol 13 support with backwards compatibility support for protocol 12.

#### Added

- Add `stellar_sdk.MuxedAccount` which makes it easy to use muxed account. ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)).
- Add `TransactionBuilder.build_fee_bump_transaction` which makes it easy to create `FeeBumpTransaction`, we have written an example, please click [here](https://github.com/StellarCN/py-stellar-base/blob/91fbd2ad61/examples/build_fee_bump_transaction.py) to view it ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Adds a feature flag which allow consumers of this library to create V1 (Protocol 13) transactions using the `TransactionBuilder` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md): First-class multiplexed accounts ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `Keypair.xdr_muxed_account` which creates a new `MuxedAccount`([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `FeeBumpTransaction` and `FeeBumpTransactionEnvelope` which makes it easy to work with fee bump transactions ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add `stellar_sdk.helpers.parse_transaction_envelope_from_xdr` which makes it easy to parse `TransactionEnvelope` and `FeeBumpTransactionEnvelope`([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).

#### Update

- Update XDR definitions with protocol 13.
- Extend `TransactionEnvelope` to work with `TransactionEnvelope`and `FeeBumpTransactionEnvelope` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add backward compatibility support for [CAP-0018](https://github.com/stellar/stellar-protocol/blob/f01c9354aaab1e8ca97a25cf888829749cadf36a/core/cap-0018.md) ([#307](https://github.com/StellarCN/py-stellar-base/pull/307)).

#### Breaking changes

- The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)):

  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- In this version, some changes have occurred in the XDR files. If you depend on them, please click [here](https://github.com/StellarCN/py-stellar-base/compare/686cf05be3c76426b6386eb31658615aa708b293...30311f51ff0f27f000cf5bc61c5c98ac734eb8f7) to view the changes.

#### Example

Some examples let you quickly learn about these changes.

1. MuxedAccount

   ```python
   from stellar_sdk import MuxedAccount
   
   account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
   account_id_id = 1234
   account_id_muxed = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
   
   # generate account_id_muxed
   muxed = MuxedAccount(account_id=account_id, account_id_id=account_id_id)  # account_id_id is optional.
   print(f"account_id_muxed: {muxed.account_id_muxed}")
   
   # parse account_id_muxed
   muxed = MuxedAccount.from_account(account_id_muxed)
   print(f"account_id: {muxed.account_id}\naccount_id_id: {muxed.account_id_id}")
   
   # without `account_id_id`
   muxed = MuxedAccount.from_account(account_id)
   print(f"account_id_muxed: {muxed.account_id_muxed}")  # None
   ```

2. Pay to muxed account

   ```python
   import pprint
   
   from stellar_sdk import Keypair, Server, MuxedAccount, TransactionBuilder, Network
   
   horizon_url = "http://horizon-testnet.stellar.org/"
   network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
   
   alice_secret = "SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L"
   bob_account = MuxedAccount(
       account_id="GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK",
       account_id_id=12387,
   )
   print(f"account_id_muxed: {bob_account.account_id_muxed}")
   
   alice_keypair = Keypair.from_secret(alice_secret)
   
   server = Server(horizon_url=horizon_url)
   alice_account = server.load_account(alice_keypair.public_key)
   transaction = TransactionBuilder(
       source_account=alice_account,
       network_passphrase=network_passphrase,
       base_fee=100,
       v1=True,  # If you want to build Protocol 13 transactions, you need to set `v1` to `True`
   ) \
       .append_payment_op(destination=bob_account, amount="100", asset_code="XLM") \
       .build()
   
   transaction.sign(alice_keypair)
   resp = server.submit_transaction(transaction)
   pprint.pprint(resp) 
   ```

3. Build fee bump transaction

   ```python
   import pprint
   
   from stellar_sdk import Keypair, Server, TransactionBuilder, Network
   from stellar_sdk.exceptions import BadRequestError
   
   horizon_url = "http://horizon-testnet.stellar.org/"
   network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
   
   fee_source_keypair = Keypair.from_secret("SASZKBDB6PFHXN6LRH4NQNTRGLGDTI3PSUVIKMZMLTYYBB7NDVMA6DSL")
   inner_source_keypair = Keypair.from_secret("SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L")
   destination_address = "GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK"
   
   server = Server(horizon_url=horizon_url)
   inner_account = server.load_account(inner_source_keypair)
   
   inner_tx = TransactionBuilder(
       source_account=inner_account,
       network_passphrase=network_passphrase,
       base_fee=50,
       v1=True) \
       .append_payment_op(destination=destination_address, amount="100", asset_code="XLM") \
       .build()
   
   inner_tx.sign(inner_source_keypair)
   
   try:
       # This transaction will fail.
       tx_insufficient_fee_resp = server.submit_transaction(inner_tx)
   except BadRequestError as e:
       print(e)
   
   fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
       fee_source=fee_source_keypair,
       base_fee=200,
       inner_transaction_envelope=inner_tx, network_passphrase=network_passphrase
   )
   fee_bump_tx.sign(fee_source_keypair)
   response = server.submit_transaction(fee_bump_tx)
   pprint.pprint(response)
   ```


### Version 2.4.0-alpha2

Released on May 03, 2020

#### Added

- Add `stellar_sdk.MuxedAccount` which makes it easy to use muxed account. ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)).

#### Breaking changes

- The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)):

  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.AllowTrust.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`


### Version 2.3.2
Released on May 01, 2020

- fix: typo in fetching previous page.([#312](https://github.com/StellarCN/py-stellar-base/issues/312))


### Version 2.4.0-alpha1

Released on April 26, 2020

**This update include breaking changes**.

This version brings protocol 13 support with backwards compatibility support for protocol 12.

#### Added

- Add `TransactionBuilder.build_fee_bump_transaction` which makes it easy to create `FeeBumpTransaction`, we have written an example, please click [here](https://github.com/StellarCN/py-stellar-base/blob/91fbd2ad61/examples/build_fee_bump_transaction.py) to view it ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Adds a feature flag which allow consumers of this library to create V1 (Protocol 13) transactions using the `TransactionBuilder` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md): First-class multiplexed accounts ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `Keypair.xdr_muxed_account` which creates a new `MuxedAccount`([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `FeeBumpTransaction` and `FeeBumpTransactionEnvelope` which makes it easy to work with fee bump transactions ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add `stellar_sdk.helpers.parse_transaction_envelope_from_xdr` which makes it easy to parse `TransactionEnvelope` and `FeeBumpTransactionEnvelope`([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).

#### Update

- Update XDR definitions with protocol 13.
- Extend `TransactionEnvelope` to work with `TransactionEnvelope`and `FeeBumpTransactionEnvelope` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add backward compatibility support for [CAP-0018](https://github.com/stellar/stellar-protocol/blob/f01c9354aaab1e8ca97a25cf888829749cadf36a/core/cap-0018.md) ([#307](https://github.com/StellarCN/py-stellar-base/pull/307)).

#### Breaking changes

- The type of `Transaction.source` changes from `Keypair` to `str`.

- In this version, some changes have occurred in the XDR files. If you depend on them, please click [here](https://github.com/StellarCN/py-stellar-base/compare/686cf05be3c76426b6386eb31658615aa708b293...30311f51ff0f27f000cf5bc61c5c98ac734eb8f7) to view the changes.

- The following XDR fields, which were previously an `AccountID` are now a `MuxedAccount` ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)):

  - `PaymentOp.destination`
  - `PathPaymentStrictReceiveOp.destination`
  - `PathPaymentStrictSendOp.destination`
  - `OperationOp.source`
  - `Operation.destination` (for `ACCOUNT_MERGE`)
  - `Transaction.source`
  - `FeeBumpTransaction.feeSource`

  You can get the string representation by calling `StrKey.encode_muxed_account` which will return a `G..` or `M..` account.

### Version 2.3.1
Released on April 12, 2020

- Update dependencies.

### Version 2.3.0
Released on March 31, 2020

#### Added
- Add SEP0029 (memo required) support. ([#291](https://github.com/StellarCN/py-stellar-base/pull/291))
  Extends `Server.submit_transaction` to always run a memo required check before 
  sending the transaction. If any of the destinations require a memo and the 
  transaction doesn't include one, then an `AccountRequiresMemoError` will be thrown.
  
  This may degrade performance, but you can skip this check by passing `skip_memo_required_check=True` to `Server.submit_transaction`:

  ```
  server.submit_transaction(tx, skip_memo_required_check=True)
  ```
  The check runs for each operation of type:
    - `Payment`
    - `PathPaymentStrictReceive`
    - `PathPaymentStrictSend`
    - `AccountMerge`
  
  If the transaction includes a memo, then memo required checking is skipped.
  
  See [SEP-0029](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0029.md) for more information about memo required check.

#### Changed
- Optimize the processing of horizon parameters. ([#289](https://github.com/StellarCN/py-stellar-base/pull/289))

### Version 2.2.3
Released on March 12, 2020

* feat: add `stellar_sdk.operation.set_options.Flag`, we can express flag more conveniently. ([fdb1f7d](https://github.com/StellarCN/py-stellar-base/commit/fdb1f7da42c2c6307fa91b010addc9535c77b7d5))

### Version 2.2.2
Released on March 08, 2020

* fix: parameters checking rule in TimeBounds. ([561f3e7](https://github.com/StellarCN/py-stellar-base/commit/561f3e7a3c407783eb8ecbed4134978fd88497f4))
* fix: HashMemo and ReturnHashMemo should be fixed in length (32 bytes). ([22cd179](https://github.com/StellarCN/py-stellar-base/commit/22cd1794ea7c35b059549588893c410b6fd297d8))

### Version 2.2.1
Released on February 12, 2020

* fix: orderbook async streams (#265)

### Version 2.2.0
Released on February 07, 2020

Horizon v1.0.0 Compatibility.

#### Added

- Add support for top-level offers endpoint with `seller`, `selling`, and `buying` filter.
  Horizon 1.0 includes a new `/offers` end-point, which allows you to list all offers, supporting filtering by `seller`, `selling`, or `buying` asset.

  You can fetch data from this endpoint by doing `server.offers()` and use any of the following filters:

  - `seller`: `server.offers().for_seller(account_id)`
  - `buying`: `server.offers().for_buying(asset)`
  - `selling`: `server.offers().for_selling(asset)`
  - `offer detail` : `server.offers().offer(offer_id)`

  This introduced a breaking change since it modified the signature for the function `server.offers()`.

  Before, if you wanted to list all the offers for a given account, you'd do:

  ```
  server.offers(account_id)
  ```

  Starting on this version you'll need to do:

  ```
  server.offers().for_seller(account_id)
  ```

  You can do now things that were not possible before, like finding
  all offers for an account filtering by the selling or buying asset

  ```
  server.offers().for_seller(account_id).for_buying(buying_asset).for_selling(selling_asset)
  ```

- Add support for filtering accounts by `signer` or `asset`, this has been released in a previous patch version.
  Horizon 1.0 includes a new `/accounts` end-point, which allows you to list all accounts who have another account as a signer or hold a given asset.

  You can fetch data from this endpoint by doing `server.accounts()` and use any of the following filters:

  - `acount detail`: `server.accounts().account_id(account_id)`, returns a single account.
  - `for signer`: `server.accounts().for_signer(account_id)`, returns accounts where `account_id` is a signer.
  - `for asset`: `server.accounts().for_asset(asset)`, returns accounts which hold the `asset`.

#### Changed

- Regenerate the XDR definitions to include [MetaV2](https://github.com/jonjove/stellar-core/blob/b299b3a458a15f592352c67d4da69baa6e8fbb6a/src/xdr/Stellar-ledger.x#L309) support (also see [#1902](https://github.com/stellar/go/issues/1902)).

#### Fixed

- Fixed some documentation errors.

#### Breaking

- Change function signature for `server.offers`. 
  The signature for the function `server.offers()` was changed to bring support for other filters.

  Before, if you wanted to list all the offers for a given account, you'd do:

  ```
  server.offers(account_id)
  ```

  Starting on this version you'll need to do:

  ```
  server.offers().for_seller(account_id)
  ```

* `server.accounts().signer` and `server.accounts().asset` are marked as deprecated, use `server.accounts().for_signer` and `server.accounts().for_asset` instead.

There are also some changes related to the horizon's response, currently, SDK has not added parse support to it, 
so please refer to this [issue](https://github.com/StellarCN/py-stellar-base/issues/257) or release notes of Stellar horizon 1.0.0. In addition, support for parsing the horizon's responses will be added in the next major update.

### Version 2.1.4
Released on February 12, 2020

* fix: orderbook async streams (#265)

### Version 2.1.3
Released on February 03, 2020

* fix: fix bug in SEP-0010 implementation.

### Version 2.1.2
Released on February 02, 2020

* fix: fix bug in SEP-0010 implementation.

### Version 2.1.1
Released on January 31, 2020

* feat: update challenge tx helpers for SEP-0010 v1.3.0.

### Version 2.1.0
Released on January 04, 2020

* feat: add support for SEP-0001 (stellar.toml).
* feat: add support for SEP-0002 (Federation protocol).
* perf: adjust the client's default timeout.

### Version 2.0.0
Released on November 29, 2019

This is a major upgrade and is not compatible with the v1.x version, 
don't worry, the v1.x version will still be maintained. 

Anyway, welcome to the v2.0.0 release, 
we have a [great document](https://stellar-sdk.readthedocs.org/) to help you get started. 

If you have suggestions, feel free to submit an issue or email me. Thank you for your patience as we transition!

New features: 
- New API design. We refactored most of the code, there are a lot of designs in v1.x that are not reasonable, 
and we can't modify them smoothly, this is one of the reasons we released v2.x.
- Added type hint support.
- Added asynchronous support.
