Release History
===============

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