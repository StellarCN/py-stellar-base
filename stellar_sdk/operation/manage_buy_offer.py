from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_price, check_amount
from ..asset import Asset
from ..price import Price
from ..xdr import Xdr


class ManageBuyOffer(Operation):
    """The :class:`ManageBuyOffer` object, which represents a ManageBuyOffer
    operation on Stellar's network.

    Creates, updates, or deletes an buy offer.

    If you want to create a new offer set Offer ID to 0.

    If you want to update an existing offer set Offer ID to existing offer ID.

    If you want to delete an existing offer set Offer ID to existing offer ID
    and set Amount to 0.

    Threshold: Medium

    :param selling: What you're selling.
    :param buying: What you're buying.
    :param amount: Amount being bought. if set to 0, delete the offer.
    :param price: Price of thing being bought in terms of what you are selling.
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
        check_amount(amount)
        check_price(price)
        self.selling: Asset = selling
        self.buying: Asset = buying
        self.amount: Union[str, Decimal] = amount
        self.price: Union[Price, str, Decimal] = price
        self.offer_id: int = offer_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.MANAGE_BUY_OFFER

    def _to_operation_body(self) -> Xdr.nullclass:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        if isinstance(self.price, Price):
            price_fraction = self.price
        else:
            price_fraction = Price.from_raw_price(self.price)

        price = price_fraction.to_xdr_object()

        amount = Operation.to_xdr_amount(self.amount)

        manage_buy_offer_op = Xdr.types.ManageBuyOfferOp(
            selling, buying, amount, price, self.offer_id
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_BUY_OFFER
        body.manageBuyOfferOp = manage_buy_offer_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ManageBuyOffer":
        """Creates a :class:`ManageBuyOffer` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        selling = Asset.from_xdr_object(
            operation_xdr_object.body.manageBuyOfferOp.selling
        )
        buying = Asset.from_xdr_object(
            operation_xdr_object.body.manageBuyOfferOp.buying
        )
        amount = Operation.from_xdr_amount(
            operation_xdr_object.body.manageBuyOfferOp.buyAmount
        )
        price = Price.from_xdr_object(operation_xdr_object.body.manageBuyOfferOp.price)
        offer_id = operation_xdr_object.body.manageBuyOfferOp.offerID

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
