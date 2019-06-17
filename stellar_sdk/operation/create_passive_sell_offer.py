import typing

from .operation import Operation

from ..asset import Asset
from ..price import Price
from ..stellarxdr import Xdr


class CreatePassiveSellOffer(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CREATE_PASSIVE_SELL_OFFER

    def __init__(self, selling: Asset, buying: Asset, amount: str, price: typing.Union[Price, str],
                 source: str = None) -> None:
        super().__init__(source)
        self.selling = selling
        self.buying = buying
        self.amount = amount
        self.price = price
        if not isinstance(price, Price):
            self.price = Price.from_raw_price(price)

    def to_operation_body(self) -> Xdr.nullclass:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = self.price.to_xdr_object()

        amount = Operation.to_xdr_amount(self.amount)

        create_passive_sell_offer_op = Xdr.types.CreatePassiveSellOfferOp(selling, buying, amount, price)
        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_PASSIVE_SELL_OFFER
        body.createPassiveSellOfferOp = create_passive_sell_offer_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'CreatePassiveSellOffer':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        selling = Asset.from_xdr_object(op_xdr_object.body.createPassiveSellOfferOp.selling)
        buying = Asset.from_xdr_object(op_xdr_object.body.createPassiveSellOfferOp.buying)
        amount = Operation.from_xdr_amount(op_xdr_object.body.createPassiveSellOfferOp.amount)
        price = Price.from_xdr_object(op_xdr_object.body.createPassiveSellOfferOp.price)

        return cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price)
