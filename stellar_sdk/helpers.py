from typing import Union

from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .transaction_envelope import TransactionEnvelope
from .type_checked import type_checked

__all__ = ["parse_transaction_envelope_from_xdr"]


@type_checked
def parse_transaction_envelope_from_xdr(
    xdr: str, network_passphrase: str
) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
    """When you are not sure whether your XDR belongs to
        :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
        or :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`,
        you can use this helper function.

    :param xdr: Transaction envelope XDR
    :param network_passphrase: The network to connect to for verifying and retrieving
        additional attributes from. (ex. 'Public Global Stellar Network ; September 2015')
    :raises: :exc:`ValueError <stellar_sdk.exceptions.ValueError>` - XDR is neither :py:class:`TransactionEnvelope <stellar_sdk.transaction_envelope.TransactionEnvelope>`
        nor :py:class:`FeeBumpTransactionEnvelope <stellar_sdk.fee_bump_transaction_envelope.FeeBumpTransactionEnvelope>`
    """
    # TODO: accepts te
    if FeeBumpTransactionEnvelope.is_fee_bump_transaction_envelope(xdr):
        return FeeBumpTransactionEnvelope.from_xdr(xdr, network_passphrase)
    return TransactionEnvelope.from_xdr(xdr, network_passphrase)
