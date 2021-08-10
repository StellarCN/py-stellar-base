from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..exceptions import ValueError
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["ManageData"]


class ManageData(Operation):
    """The :class:`ManageData` object, which represents a
    ManageData operation on Stellar's network.

    Allows you to set, modify or delete a Data Entry (name/value pair) that is
    attached to a particular account. An account can have an arbitrary amount
    of DataEntries attached to it. Each DataEntry increases the minimum balance
    needed to be held by the account.

    DataEntries can be used for application specific things. They are not used
    by the core Stellar protocol.

    Threshold: Medium

    :param data_name: The name of the data entry.
    :param data_value: The value of the data entry.
    :param source: The optional source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.MANAGE_DATA
    )

    def __init__(
        self,
        data_name: str,
        data_value: Union[str, bytes, None],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:  # TODO: bytes only?
        super().__init__(source)
        self.data_name: str = data_name
        if isinstance(data_value, str):
            data_value = data_value.encode()
        self.data_value: Union[bytes, None] = data_value

        valid_data_name_len = len(self.data_name) <= 64
        valid_data_val_len = self.data_value is None or len(self.data_value) <= 64

        if not valid_data_name_len or not valid_data_val_len:
            raise ValueError("Data and value should be <= 64 bytes (ascii encoded).")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        data_name = stellar_xdr.String64(bytes(self.data_name, encoding="utf-8"))
        if self.data_value is None:
            data_value = None
        else:
            data_value = stellar_xdr.DataValue(self.data_value)

        manage_data_op = stellar_xdr.ManageDataOp(data_name, data_value)

        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, manage_data_op=manage_data_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "ManageData":
        """Creates a :class:`ManageData` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.manage_data_op is not None
        # TODO: should we decode it?
        data_name = xdr_object.body.manage_data_op.data_name.string64.decode()
        data_value_xdr = xdr_object.body.manage_data_op.data_value
        data_value = None if data_value_xdr is None else data_value_xdr.data_value

        op = cls(data_name=data_name, data_value=data_value, source=source)
        return op

    def __str__(self):
        return f"<ManageData [data_name={self.data_name}, data_value={self.data_value}, source={self.source}]>"
