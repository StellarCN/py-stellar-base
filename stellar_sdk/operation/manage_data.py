import typing

from .operation import Operation

from ..stellarxdr import Xdr


class ManageData(Operation):
    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.MANAGE_DATA

    def __init__(self, name: str, value: typing.Union[str, bytes, None], source=None) -> None:  # TODO: bytes only?
        super().__init__(source)
        self.name = name
        self.value = value

        valid_data_name_len = len(self.name) <= 64
        valid_data_val_len = (self.value is None
                              or len(self.value) <= 64)

        if not valid_data_name_len or not valid_data_val_len:
            raise ValueError("Data and value should be <= 64 bytes (ascii encoded).")

    def to_operation_body(self) -> Xdr.nullclass:
        data_name = bytes(self.name, encoding='utf-8')

        if self.value is not None:
            if isinstance(self.value, bytes):
                data_value = [self.value]
            else:
                data_value = [bytes(self.value, 'utf-8')]
        else:
            data_value = []
        manage_data_op = Xdr.types.ManageDataOp(data_name, data_value)

        body = Xdr.nullclass()
        body.type = Xdr.const.MANAGE_DATA
        body.manageDataOp = manage_data_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'ManageData':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)
        data_name = op_xdr_object.body.manageDataOp.dataName.decode()

        if op_xdr_object.body.manageDataOp.dataValue:
            data_value = op_xdr_object.body.manageDataOp.dataValue[0]
        else:
            data_value = None
        return cls(source=source, name=data_name, value=data_value)
