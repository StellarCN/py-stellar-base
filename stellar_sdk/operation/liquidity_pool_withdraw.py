import binascii
from decimal import Decimal
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..exceptions import ValueError
from ..muxed_account import MuxedAccount
from .operation import Operation
from .utils import check_amount, is_valid_hash

__all__ = ["LiquidityPoolWithdraw"]


class LiquidityPoolWithdraw(Operation):
    """The :class:`LiquidityPoolWithdraw` object, which represents a LiquidityPoolWithdraw
    operation on Stellar's network.

    Creates a liquidity pool withdraw operation.

    Threshold: Medium

    :param liquidity_pool_id: The liquidity pool ID.
    :param amount: Amount of pool shares to withdraw.
    :param min_amount_a: Minimum amount of first asset to withdraw.
    :param min_amount_b: Minimum amount of second asset to withdraw.
    :param source: The source account for the operation. Defaults to the
        transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.LIQUIDITY_POOL_WITHDRAW
    )

    def __init__(
        self,
        liquidity_pool_id: str,
        amount: Union[str, Decimal],
        min_amount_a: Union[str, Decimal],
        min_amount_b: Union[str, Decimal],
        source: Optional[Union[MuxedAccount, str]] = None,
    ):
        super().__init__(source)
        if not is_valid_hash(liquidity_pool_id):
            raise ValueError("`liquidity_pool_id` is not a valid hash.")
        check_amount(amount)
        check_amount(min_amount_a)
        check_amount(min_amount_b)
        self.liquidity_pool_id = liquidity_pool_id
        self.amount = amount
        self.min_amount_a = min_amount_a
        self.min_amount_b = min_amount_b

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        liquidity_pool_id_bytes = binascii.unhexlify(self.liquidity_pool_id)
        liquidity_pool_id = stellar_xdr.PoolID.from_xdr_bytes(liquidity_pool_id_bytes)
        amount = stellar_xdr.Int64(Operation.to_xdr_amount(self.amount))
        min_amount_a = stellar_xdr.Int64(Operation.to_xdr_amount(self.min_amount_a))
        min_amount_b = stellar_xdr.Int64(Operation.to_xdr_amount(self.min_amount_b))
        liquidity_pool_withdraw_op = stellar_xdr.LiquidityPoolWithdrawOp(
            liquidity_pool_id, amount, min_amount_a, min_amount_b
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            liquidity_pool_withdraw_op=liquidity_pool_withdraw_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "LiquidityPoolWithdraw":
        """Creates a :class:`LiquidityPoolWithdraw` object from an XDR Operation object."""
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.liquidity_pool_withdraw_op is not None
        liquidity_pool_id_bytes = (
            xdr_object.body.liquidity_pool_withdraw_op.liquidity_pool_id.pool_id.hash
        )
        liquidity_pool_id = liquidity_pool_id_bytes.hex()
        amount = Operation.from_xdr_amount(
            xdr_object.body.liquidity_pool_withdraw_op.amount.int64
        )
        min_amount_a = Operation.from_xdr_amount(
            xdr_object.body.liquidity_pool_withdraw_op.min_amount_a.int64
        )
        min_amount_b = Operation.from_xdr_amount(
            xdr_object.body.liquidity_pool_withdraw_op.min_amount_b.int64
        )

        op = cls(
            source=source,
            liquidity_pool_id=liquidity_pool_id,
            amount=amount,
            min_amount_a=min_amount_a,
            min_amount_b=min_amount_b,
        )
        return op

    def __str__(self):
        return (
            f"<LiquidityPoolWithdraw [liquidity_pool_id={self.liquidity_pool_id}, amount={self.amount}, "
            f"min_amount_a={self.min_amount_a}, min_amount_b={self.min_amount_b}, source={self.source}]>"
        )
