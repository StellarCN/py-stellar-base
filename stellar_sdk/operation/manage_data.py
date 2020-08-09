from typing import Union

from .operation import Operation
from ..exceptions import ValueError
from ..utils import pack_xdr_array, unpack_xdr_array
from ..xdr import Xdr


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

    def __init__(
        self, data_name: str, data_value: Union[str, bytes, None], source: str = None,
    ) -> None:  # TODO: bytes only?
        super().__init__(source)
        self.data_name: str = data_name
        if isinstance(data_value, str):
            data_value = data_value.encode()
        self.data_value: Union[str, bytes, None] = data_value

        valid_data_name_len = len(self.data_name) <= 64
        valid_data_val_len = self.data_value is None or len(self.data_value) <= 64

        if not valid_data_name_len or not valid_data_val_len:
            raise ValueError("Data and value should be <= 64 bytes (ascii encoded).")

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.MANAGE_DATA

    def _to_operation_body(self) -> Xdr.nullclass:
        data_name = bytes(self.data_name, encoding="utf-8")

        data_value = pack_xdr_array(self.data_value)
        manage_data_op = Xdr.types.ManageDataOp(data_name, data_value)

        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_DATA
        body.manageDataOp = manage_data_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "ManageData":
        """Creates a :class:`ManageData` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        data_name = operation_xdr_object.body.manageDataOp.dataName.decode()

        data_value = unpack_xdr_array(operation_xdr_object.body.manageDataOp.dataValue)
        op = cls(data_name=data_name, data_value=data_value, source=source)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
