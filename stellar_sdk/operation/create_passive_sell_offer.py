from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount, check_price
from .. import xdr as stellar_xdr
from ..asset import Asset
from ..price import Price


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

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.CREATE_PASSIVE_SELL_OFFER

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

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()

        if isinstance(self.price, Price):
            price_fraction = self.price
        else:
            price_fraction = Price.from_raw_price(self.price)

        price = price_fraction.to_xdr_object()
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        create_passive_sell_offer_op = stellar_xdr.CreatePassiveSellOfferOp(
            selling, buying, amount, price
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            create_passive_sell_offer_op=create_passive_sell_offer_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "CreatePassiveSellOffer":
        """Creates a :class:`CreatePassiveSellOffer` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.create_passive_sell_offer_op is not None
        selling = Asset.from_xdr_object(
            xdr_object.body.create_passive_sell_offer_op.selling
        )
        buying = Asset.from_xdr_object(
            xdr_object.body.create_passive_sell_offer_op.buying
        )
        amount = Operation.from_xdr_amount(
            xdr_object.body.create_passive_sell_offer_op.amount.int64
        )
        price = Price.from_xdr_object(
            xdr_object.body.create_passive_sell_offer_op.price
        )

        op = cls(
            source=source, selling=selling, buying=buying, amount=amount, price=price
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<CreatePassiveSellOffer [selling={self.selling}, buying={self.buying}, "
            f"amount={self.amount}, price={self.price}, source={self.source}]>"
        )
