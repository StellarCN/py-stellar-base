from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_price, check_amount
from ..asset import Asset
from ..price import Price
from ..xdr import Xdr


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

    def __init__(
        self,
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        offer_id: int = 0,
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_price(price)
        check_amount(amount)
        self.selling: Asset = selling
        self.buying: Asset = buying
        self.amount: Union[str, Decimal] = amount
        self.price: Union[Price, str, Decimal] = price
        self.offer_id: int = offer_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.MANAGE_SELL_OFFER

    def _to_operation_body(self) -> Xdr.nullclass:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        if isinstance(self.price, Price):
            price_fraction = self.price
        else:
            price_fraction = Price.from_raw_price(self.price)

        price = price_fraction.to_xdr_object()

        amount = Operation.to_xdr_amount(self.amount)

        manage_sell_offer_op = Xdr.types.ManageSellOfferOp(
            selling, buying, amount, price, self.offer_id
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_SELL_OFFER
        body.manageSellOfferOp = manage_sell_offer_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ManageSellOffer":
        """Creates a :class:`ManageSellOffer` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        selling = Asset.from_xdr_object(
            operation_xdr_object.body.manageSellOfferOp.selling
        )
        buying = Asset.from_xdr_object(
            operation_xdr_object.body.manageSellOfferOp.buying
        )
        amount = Operation.from_xdr_amount(
            operation_xdr_object.body.manageSellOfferOp.amount
        )
        price = Price.from_xdr_object(operation_xdr_object.body.manageSellOfferOp.price)
        offer_id = operation_xdr_object.body.manageSellOfferOp.offerID

        op = cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
