Release History
===============

### Version 2.1.1
Unreleased

* feat: update challenge tx helpers for SEP-0010 v1.3.0

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