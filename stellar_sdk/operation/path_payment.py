import typing

from .operation import Operation
from ..asset import Asset
from ..keypair import Keypair
from ..stellarxdr import Xdr
from ..strkey import StrKey


class PathPayment(Operation):

    def __init__(self,
                 destination: str,
                 send_asset: Asset,
                 send_max: str,
                 dest_asset: Asset,
                 dest_amount: str,
                 path: typing.List[Asset],
                 source: str = None) -> None:
        super().__init__(source)
        self.destination = destination
        self.send_asset = send_asset
        self.send_max = send_max
        self.dest_asset = dest_asset
        self.dest_amount = dest_amount
        self.path = path  # a list of paths/assets

    @classmethod
    def __type_code(cls) -> int:
        return Xdr.const.PATH_PAYMENT

    def __to_operation_body(self) -> Xdr.nullclass:
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        send_asset = self.send_asset.to_xdr_object()
        dest_asset = self.dest_asset.to_xdr_object()
        path = [asset.to_xdr_object() for asset in self.path]

        path_payment = Xdr.types.PathPaymentOp(
            send_asset, Operation.to_xdr_amount(self.send_max), destination,
            dest_asset, Operation.to_xdr_amount(self.dest_amount), path)
        body = Xdr.nullclass()
        body.type = Xdr.const.PATH_PAYMENT
        body.pathPaymentOp = path_payment
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> 'PathPayment':
        """Creates a :class:`PathPayment` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = StrKey.encode_ed25519_public_key(operation_xdr_object.body.pathPaymentOp.destination.ed25519)

        send_asset = Asset.from_xdr_object(operation_xdr_object.body.pathPaymentOp.sendAsset)
        dest_asset = Asset.from_xdr_object(operation_xdr_object.body.pathPaymentOp.destAsset)
        send_max = Operation.from_xdr_amount(operation_xdr_object.body.pathPaymentOp.sendMax)
        dest_amount = Operation.from_xdr_amount(operation_xdr_object.body.pathPaymentOp.destAmount)

        path = []
        if operation_xdr_object.body.pathPaymentOp.path:
            for x in operation_xdr_object.body.pathPaymentOp.path:
                path.append(Asset.from_xdr_object(x))

        return cls(
            source=source,
            destination=destination,
            send_asset=send_asset,
            send_max=send_max,
            dest_asset=dest_asset,
            dest_amount=dest_amount,
            path=path)
