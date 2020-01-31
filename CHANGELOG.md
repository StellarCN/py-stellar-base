Release History
===============

### Version 2.2.0

Unreleased

Horizon v1.0.0 Compatibility.

* **[Breaking Change]** Add support for `/offers` end-point with query parameters, this will affect the existing API, please refer to the documentation. (See [SDK API Documentation](https://stellar-sdk.readthedocs.io/en/2.2.0-beta1/api.html#offerscallbuilder) and [Stellar documentation for offers](https://www.stellar.org/developers/horizon/reference/endpoints/offers.html))
* Regenerate the XDR definitions to include [MetaV2](https://github.com/jonjove/stellar-core/blob/b299b3a458a15f592352c67d4da69baa6e8fbb6a/src/xdr/Stellar-ledger.x#L309) support (also see [#1902](https://github.com/stellar/go/issues/1902)).

There are also some updates that have been released in previous versions, see this [issue](https://github.com/StellarCN/py-stellar-base/issues/257) for details.

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