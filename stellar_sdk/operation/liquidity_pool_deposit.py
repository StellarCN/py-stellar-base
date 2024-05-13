import binascii
from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from ..price import Price
from ..utils import raise_if_not_valid_amount, raise_if_not_valid_hash
from .operation import Operation

__all__ = ["LiquidityPoolDeposit"]


class LiquidityPoolDeposit(Operation):
    """The :class:`LiquidityPoolDeposit` object, which represents a LiquidityPoolDeposit
    operation on Stellar's network.

    Creates a liquidity pool deposit operation.

    Threshold: Medium

    See `Liquidity Pool Deposit <https://developers.stellar.org/docs/start/list-of-operations/#liquidity-pool-deposit>`_ for more information.

    :param liquidity_pool_id: The liquidity pool ID.
    :param max_amount_a: Maximum amount of first asset to deposit.
    :param max_amount_b: Maximum amount of second asset to deposit.
    :param min_price: Minimum deposit_a/deposit_b price.
    :param max_price: Maximum deposit_a/deposit_b price.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.LIQUIDITY_POOL_DEPOSIT
    )

    def __init__(
        self,
        liquidity_pool_id: str,
        max_amount_a: Union[str, Decimal],
        max_amount_b: Union[str, Decimal],
        min_price: Union[str, Decimal, Price],
        max_price: Union[str, Decimal, Price],
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        self.liquidity_pool_id: str = liquidity_pool_id
        self.max_amount_a: str = str(max_amount_a)
        self.max_amount_b: str = str(max_amount_b)
        if isinstance(min_price, Price):
            self.min_price: Price = min_price
        else:
            self.min_price = Price.from_raw_price(min_price)
        if isinstance(max_price, Price):
            self.max_price: Price = max_price
        else:
            self.max_price = Price.from_raw_price(max_price)
        raise_if_not_valid_amount(self.max_amount_a, "max_amount_a")
        raise_if_not_valid_amount(self.max_amount_b, "max_amount_b")
        raise_if_not_valid_hash(self.liquidity_pool_id, "liquidity_pool_id")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        liquidity_pool_id_bytes = binascii.unhexlify(self.liquidity_pool_id)
        liquidity_pool_id = stellar_xdr.PoolID.from_xdr_bytes(liquidity_pool_id_bytes)
        max_amount_a = stellar_xdr.Int64(Operation.to_xdr_amount(self.max_amount_a))
        max_amount_b = stellar_xdr.Int64(Operation.to_xdr_amount(self.max_amount_b))
        min_price = self.min_price.to_xdr_object()
        max_price = self.max_price.to_xdr_object()
        liquidity_pool_deposit_op = stellar_xdr.LiquidityPoolDepositOp(
            liquidity_pool_id, max_amount_a, max_amount_b, min_price, max_price
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            liquidity_pool_deposit_op=liquidity_pool_deposit_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "LiquidityPoolDeposit":
        """Creates a :class:`LiquidityPoolDeposit` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.liquidity_pool_deposit_op is not None
        liquidity_pool_id_bytes = (
            xdr_object.body.liquidity_pool_deposit_op.liquidity_pool_id.pool_id.hash
        )
        liquidity_pool_id = liquidity_pool_id_bytes.hex()
        max_amount_a = Operation.from_xdr_amount(
            xdr_object.body.liquidity_pool_deposit_op.max_amount_a.int64
        )
        max_amount_b = Operation.from_xdr_amount(
            xdr_object.body.liquidity_pool_deposit_op.max_amount_b.int64
        )
        min_price = Price.from_xdr_object(
            xdr_object.body.liquidity_pool_deposit_op.min_price
        )
        max_price = Price.from_xdr_object(
            xdr_object.body.liquidity_pool_deposit_op.max_price
        )

        op = cls(
            source=source,
            liquidity_pool_id=liquidity_pool_id,
            max_amount_a=max_amount_a,
            max_amount_b=max_amount_b,
            min_price=min_price,
            max_price=max_price,
        )
        return op

    def __repr__(self):
        return (
            f"<LiquidityPoolDeposit [liquidity_pool_id={self.liquidity_pool_id}, max_amount_a={self.max_amount_a}, "
            f"max_amount_b={self.max_amount_b}, min_price={self.min_price}, max_price={self.max_price}, "
            f"source={self.source}]>"
        )
