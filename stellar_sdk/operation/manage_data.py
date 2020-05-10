from typing import Union

from .operation import Operation
from ..exceptions import ValueError
from ..muxed_account import MuxedAccount
from ..xdr import xdr


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

    TYPE_CODE = xdr.OperationType.MANAGE_DATA

    def __init__(
        self,
        data_name: str,
        data_value: Union[str, bytes, None],
        source: Union[MuxedAccount, str] = None,
    ) -> None:  # TODO: bytes only?
        super().__init__(source)
        self.data_name: str = data_name
        self.data_value: Union[str, bytes, None] = data_value

        valid_data_name_len = len(self.data_name) <= 64
        valid_data_val_len = self.data_value is None or len(self.data_value) <= 64

        if not valid_data_name_len or not valid_data_val_len:
            raise ValueError("Data and value should be <= 64 bytes (ascii encoded).")

    def _to_operation_body(self) -> xdr.OperationBody:
        data_name = xdr.String64(bytes(self.data_name, encoding="utf-8"))

        if self.data_value is None:
            data_value = None
        else:
            if isinstance(self.data_value, bytes):
                data_value = self.data_value
            else:
                data_value = bytes(self.data_value, "utf-8")
            data_value = xdr.DataValue(data_value)

        manage_data_op = xdr.ManageDataOp(data_name, data_value)

        body = xdr.OperationBody(type=self.TYPE_CODE, manage_data_op=manage_data_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "ManageData":
        """Creates a :class:`ManageData` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        # TODO: should we decode it?
        data_name = operation_xdr_object.body.manage_data_op.data_name.string64.decode()
        data_value_xdr = operation_xdr_object.body.manage_data_op.data_value
        data_value = None if data_value_xdr is None else data_value_xdr.data_value
        return cls(data_name=data_name, data_value=data_value, source=source)
