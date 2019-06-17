import typing

from .operation import Operation

from ..asset import Asset
from ..price import Price
from ..stellarxdr import Xdr


class ManageBuyOffer(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.MANAGE_BUY_OFFER

    def __init__(self, selling: Asset, buying: Asset, amount: str, price: typing.Union[Price, str], offer_id: int = 0,
                 source: str = None) -> None:
        super().__init__(source)
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price
        if not isinstance(price, Price):
            self.price = Price.from_raw_price(price)
        self.offer_id = offer_id

    def to_operation_body(self) -> Xdr.nullclass:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = self.price.to_xdr_object()

        amount = Operation.to_xdr_amount(self.amount)

        manage_buy_offer_op = Xdr.types.ManageBuyOfferOp(selling, buying, amount,
                                                         price, self.offer_id)
        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_BUY_OFFER
        body.manageBuyOfferOp = manage_buy_offer_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'ManageBuyOffer':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        selling = Asset.from_xdr_object(
            op_xdr_object.body.manageBuyOfferOp.selling)
        buying = Asset.from_xdr_object(op_xdr_object.body.manageBuyOfferOp.buying)
        amount = Operation.from_xdr_amount(
            op_xdr_object.body.manageBuyOfferOp.buyAmount)
        price = Price.from_xdr_object(op_xdr_object.body.manageBuyOfferOp.price)
        offer_id = op_xdr_object.body.manageBuyOfferOp.offerID

        return cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id)
