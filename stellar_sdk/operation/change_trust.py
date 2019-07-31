from .operation import Operation

from ..asset import Asset
from ..stellarxdr import Xdr


class ChangeTrust(Operation):
    _DEFAULT_LIMIT = "922337203685.4775807"

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CHANGE_TRUST

    def __init__(self, asset: Asset, limit: str = None, source: str = None) -> None:
        super().__init__(source)
        self.asset = asset
        if limit is None:  # We don't need this if the user can send the value with correct type.
            self.limit = self._DEFAULT_LIMIT
        else:
            self.limit = limit

    def to_operation_body(self) -> Xdr.nullclass:
        line = self.asset.to_xdr_object()
        limit = Operation.to_xdr_amount(self.limit)

        change_trust_op = Xdr.types.ChangeTrustOp(line, limit)
        body = Xdr.nullclass()
        body.type = Xdr.const.CHANGE_TRUST
        body.changeTrustOp = change_trust_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> 'ChangeTrust':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        line = Asset.from_xdr_object(op_xdr_object.body.changeTrustOp.line)
        limit = Operation.from_xdr_amount(op_xdr_object.body.changeTrustOp.limit)

        return cls(source=source, asset=line, limit=limit)
