"""Every type of Stellar's XDR definitions, with binary XDR and SEP-51 JSON encoding.

This module re-exports `stellar-xdr <https://stellar-xdr.readthedocs.io/>`_, which the
SDK depends on, so it can be used without adding another dependency::

    from stellar_sdk import xdr

    value = xdr.SCVal.U32(7)
    assert value.to_xdr_base64() == "AAAAAwAAAAc="
    assert xdr.SCVal.from_xdr_base64("AAAAAwAAAAc=") == value

See the stellar-xdr documentation for the guide and the full API.
"""

import stellar_xdr as _stellar_xdr
# A wildcard import keeps this module in step with stellar-xdr as types are added.
# Type checkers still see every name, since `__all__` below is built from stellar-xdr's.
from stellar_xdr import *  # noqa: F403  # pyright: ignore[reportWildcardImportFromLibrary]

__all__: list[str] = []
__all__ += _stellar_xdr.__all__
