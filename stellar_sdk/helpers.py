from typing import Union

from .exceptions import ValueError
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .transaction_envelope import TransactionEnvelope
from .xdr import Xdr


__all__ = ["parse_transaction_envelope_from_xdr"]


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
    xdr_object = Xdr.types.TransactionEnvelope.from_xdr(xdr)
    te_type = xdr_object.type
    if te_type == Xdr.const.ENVELOPE_TYPE_TX_FEE_BUMP:
        return FeeBumpTransactionEnvelope.from_xdr_object(
            xdr_object, network_passphrase
        )
    elif (
        te_type == Xdr.const.ENVELOPE_TYPE_TX
        or te_type == Xdr.const.ENVELOPE_TYPE_TX_V0
    ):
        return TransactionEnvelope.from_xdr_object(xdr_object, network_passphrase)
    else:
        raise ValueError(
            "This transaction envelope type is not supported, type = {}.".format(
                te_type
            )
        )
