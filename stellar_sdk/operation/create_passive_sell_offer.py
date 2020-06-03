from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount, check_price
from ..asset import Asset
from ..price import Price
from ..xdr import Xdr


class CreatePassiveSellOffer(Operation):
    """The :class:`CreatePassiveSellOffer` object, which represents a
    CreatePassiveSellOffer operation on Stellar's network.

    A passive sell offer is an offer that does not act on and take a reverse offer
    of equal price. Instead, they only take offers of lesser price. For
    example, if an offer exists to buy 5 BTC for 30 XLM, and you make a passive
    sell offer to buy 30 XLM for 5 BTC, your passive sell offer does not take the first
    offer.

    Note that regular offers made later than your passive sell offer can act on and
    take your passive sell offer, even if the regular offer is of the same price as
    your passive sell offer.

    Passive sell offers allow market makers to have zero spread. If you want to
    trade EUR for USD at 1:1 price and USD for EUR also at 1:1, you can create
    two passive sell offers so the two offers don't immediately act on each other.

    Once the passive sell offer is created, you can manage it like any other offer
    using the manage offer operation - see :class:`ManageOffer` for more
    details.

    :param selling: What you're selling.
    :param buying: What you're buying.
    :param amount: The total amount you're selling. If 0,
        deletes the offer.
    :param price: Price of 1 unit of `selling` in
        terms of `buying`.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(
        self,
        selling: Asset,
        buying: Asset,
        amount: Union[str, Decimal],
        price: Union[Price, str, Decimal],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_amount(amount)
        check_price(price)
        self.selling: Asset = selling
        self.buying: Asset = buying
        self.amount: Union[str, Decimal] = amount
        self.price: Union[Price, str, Decimal] = price

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CREATE_PASSIVE_SELL_OFFER

    def _to_operation_body(self) -> Xdr.nullclass:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        if isinstance(self.price, Price):
            price_fraction = self.price
        else:
            price_fraction = Price.from_raw_price(self.price)

        price = price_fraction.to_xdr_object()

        amount = Operation.to_xdr_amount(self.amount)

        create_passive_sell_offer_op = Xdr.types.CreatePassiveSellOfferOp(
            selling, buying, amount, price
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_PASSIVE_SELL_OFFER
        body.createPassiveSellOfferOp = create_passive_sell_offer_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "CreatePassiveSellOffer":
        """Creates a :class:`CreatePassiveSellOffer` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        selling = Asset.from_xdr_object(
            operation_xdr_object.body.createPassiveSellOfferOp.selling
        )
        buying = Asset.from_xdr_object(
            operation_xdr_object.body.createPassiveSellOfferOp.buying
        )
        amount = Operation.from_xdr_amount(
            operation_xdr_object.body.createPassiveSellOfferOp.amount
        )
        price = Price.from_xdr_object(
            operation_xdr_object.body.createPassiveSellOfferOp.price
        )

        op = cls(
            source=source, selling=selling, buying=buying, amount=amount, price=price
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
