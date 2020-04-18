from typing import Union

from .exceptions import ValueError
from .fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from .transaction_envelope import TransactionEnvelope
from .xdr import Xdr


__all__ = ["parse_transaction_envelope_from_xdr"]


def parse_transaction_envelope_from_xdr(
    xdr: str, network_passphrase: str
) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
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
            "This transaction envelope type is not currently supported, type = {}.".format(
                te_type
            )
        )
