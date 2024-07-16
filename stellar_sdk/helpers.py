import warnings
from typing import Union

from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .transaction_envelope import TransactionEnvelope

__all__ = ["parse_transaction_envelope_from_xdr"]


def parse_transaction_envelope_from_xdr(
    xdr: str, network_passphrase: str
) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
    """When you are not sure whether your XDR belongs to
    :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
    or :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`,
    you can use this helper function.

    An example::

        from stellar_sdk import Network
        from stellar_sdk.helpers import parse_transaction_envelope_from_xdr

        xdr = "AAAAAgAAAADHJNEDn33/C1uDkDfzDfKVq/4XE9IxDfGiLCfoV7riZQAAA+gCI4TVABpRPgAAAAAAAAAAAAAAAQAAAAAAAAADAAAAAUxpcmEAAAAAabIaDgm0ypyJpsVfEjZw2mO3Enq4Q4t5URKfWtqukSUAAAABVVNEAAAAAADophqGHmCvYPgHc+BjRuXHLL5Z3K3aN2CNWO9CUR2f3AAAAAAAAAAAE8G9mAADcH8AAAAAMYdBWgAAAAAAAAABV7riZQAAAEARGCGwYk/kEB2Z4UL20y536evnwmmSc4c2FnxlvUcPZl5jgWHcNwY8LTpFhdrUN9TZWciCRp/JCZYa0SJh8cYB"
        te = parse_transaction_envelope_from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        print(te)

    :param xdr: Transaction envelope XDR
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. ``"Public Global Stellar Network ; September 2015"``)
    :raises: :exc:`ValueError <stellar_sdk.exceptions.ValueError>` - XDR is neither :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
        nor :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
    """
    warnings.warn(
        "This function is deprecated. Use `TransactionBuilder.from_xdr` instead.",
        DeprecationWarning,
    )
    if FeeBumpTransactionEnvelope.is_fee_bump_transaction_envelope(xdr):
        return FeeBumpTransactionEnvelope.from_xdr(xdr, network_passphrase)
    return TransactionEnvelope.from_xdr(xdr, network_passphrase)
