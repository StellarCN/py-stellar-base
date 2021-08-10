from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..price import Price
from .operation import Operation
from .utils import check_amount, check_price

__all__ = ["ManageSellOffer"]


class ManageSellOffer(Operation):
    """The :class:`ManageSellOffer` object, which represents a ManageSellOffer
    operation on Stellar's network.

    Creates, updates, or deletes an sell offer.

    If you want to create a new offer set Offer ID to 0.

    If you want to update an existing offer set Offer ID to existing offer ID.

    If you want to delete an existing offer set Offer ID to existing offer ID
    and set Amount to 0.

    Threshold: Medium

    :param selling: What you're selling.
    :param buying: What you're buying.
    :param amount: The total amount you're selling. If `0`, deletes the offer.
    :param price: Price of 1 unit of `selling` in terms of `buying`.
    :param offer_id: If `0`, will create a new offer (default). Otherwise,
        edits an existing offer.
    :param source: The source account (defaults to transaction source).

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.MANAGE_SELL_OFFER
    )

    def __init__(
        self,
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        offer_id: int = 0,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        check_price(price)
        check_amount(amount)
        self.selling: Asset = selling
        self.buying: Asset = buying
        self.amount: Union[str, Decimal] = amount
        self.price: Union[Price, str, Decimal] = price
        self.offer_id: int = offer_id

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        if isinstance(self.price, Price):
            price_fraction = self.price
        else:
            price_fraction = Price.from_raw_price(self.price)

        price = price_fraction.to_xdr_object()
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        manage_sell_offer_op = stellar_xdr.ManageSellOfferOp(
            selling, buying, amount, price, stellar_xdr.Int64(self.offer_id)
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, manage_sell_offer_op=manage_sell_offer_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "ManageSellOffer":
        """Creates a :class:`ManageSellOffer` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.manage_sell_offer_op is not None
        selling = Asset.from_xdr_object(xdr_object.body.manage_sell_offer_op.selling)
        buying = Asset.from_xdr_object(xdr_object.body.manage_sell_offer_op.buying)
        amount = Operation.from_xdr_amount(
            xdr_object.body.manage_sell_offer_op.amount.int64
        )
        price = Price.from_xdr_object(xdr_object.body.manage_sell_offer_op.price)
        offer_id = xdr_object.body.manage_sell_offer_op.offer_id.int64

        op = cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )
        return op

    def __str__(self):
        return (
            f"<ManageSellOffer [selling={self.selling}, buying={self.buying}, "
            f"amount={self.amount}, price={self.price}, offer_id={self.offer_id}, source={self.source}]>"
        )
