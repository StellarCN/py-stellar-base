from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..price import Price
from ..utils import raise_if_not_valid_amount
from .operation import Operation

__all__ = ["ManageBuyOffer"]


class ManageBuyOffer(Operation):
    """The :class:`ManageBuyOffer` object, which represents a ManageBuyOffer
    operation on Stellar's network.

    Creates, updates, or deletes an buy offer.

    If you want to create a new offer set `offer_id` to ``0``.

    If you want to update an existing offer set `offer_id` to existing offer ID.

    If you want to delete an existing offer set `offer_id` to existing offer ID
    and set `amount` to ``0``.

    Threshold: Medium

    See `Manage Buy Offer <https://developers.stellar.org/docs/start/list-of-operations/#manage-buy-offer>`_ for more information.

    :param selling: What you're selling.
    :param buying: What you're buying.
    :param amount: Amount being bought. if set to ``0``, delete the offer.
    :param price: Price of thing being bought in terms of what you are selling.
    :param offer_id: If ``0``, will create a new offer (default). Otherwise,
        edits an existing offer.
    :param source: The source account for the operation. Defaults to the transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.MANAGE_BUY_OFFER
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
        if not isinstance(price, Price):
            price = Price.from_raw_price(price)
        self.selling: Asset = selling
        self.buying: Asset = buying
        self.amount: str = str(amount)
        self.price: Price = price
        self.offer_id: int = offer_id
        raise_if_not_valid_amount(self.amount, "amount")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        selling = self.selling.to_xdr_object()
        buying = self.buying.to_xdr_object()
        price = self.price.to_xdr_object()
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        manage_buy_offer_op = stellar_xdr.ManageBuyOfferOp(
            selling, buying, amount, price, stellar_xdr.Int64(self.offer_id)
        )

        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, manage_buy_offer_op=manage_buy_offer_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "ManageBuyOffer":
        """Creates a :class:`ManageBuyOffer` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.manage_buy_offer_op is not None
        selling = Asset.from_xdr_object(xdr_object.body.manage_buy_offer_op.selling)
        buying = Asset.from_xdr_object(xdr_object.body.manage_buy_offer_op.buying)
        amount = Operation.from_xdr_amount(
            xdr_object.body.manage_buy_offer_op.buy_amount.int64
        )
        price = Price.from_xdr_object(xdr_object.body.manage_buy_offer_op.price)
        offer_id = xdr_object.body.manage_buy_offer_op.offer_id.int64

        op = cls(
            source=source,
            selling=selling,
            buying=buying,
            amount=amount,
            price=price,
            offer_id=offer_id,
        )
        return op

    def __repr__(self):
        return (
            f"<ManageBuyOffer [selling={self.selling}, buying={self.buying}, "
            f"amount={self.amount}, price={self.price}, offer_id={self.offer_id}, source={self.source}]>"
        )
