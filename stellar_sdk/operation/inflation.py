from .operation import Operation

from ..stellarxdr import Xdr


class Inflation(Operation):
    @classmethod
    def type_code(cls):
        return Xdr.const.INFLATION

    def __init__(self, source=None):
        super().__init__(source)

    def to_operation_body(self):
        body = Xdr.nullclass
        body.type = Xdr.const.INFLATION
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        source = Operation.get_source_from_xdr_obj(op_xdr_object)
        return cls(source)

