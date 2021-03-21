# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .envelope_type import EnvelopeType
from .operation_id_id import OperationIDId
from ..exceptions import ValueError

__all__ = ["OperationID"]


class OperationID:
    """
    XDR Source Code
    ----------------------------------------------------------------
    union OperationID switch (EnvelopeType type)
    {
    case ENVELOPE_TYPE_OP_ID:
        struct
        {
            MuxedAccount sourceAccount;
            SequenceNumber seqNum;
            uint32 opNum;
        } id;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        type: EnvelopeType,
        id: OperationIDId = None,
    ) -> None:
        self.type = type
        self.id = id

    def pack(self, packer: Packer) -> None:
        self.type.pack(packer)
        if self.type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            if self.id is None:
                raise ValueError("id should not be None.")
            self.id.pack(packer)
            return
        raise ValueError("Invalid type.")

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "OperationID":
        type = EnvelopeType.unpack(unpacker)
        if type == EnvelopeType.ENVELOPE_TYPE_OP_ID:
            id = OperationIDId.unpack(unpacker)
            if id is None:
                raise ValueError("id should not be None.")
            return cls(type, id=id)
        raise ValueError("Invalid type.")

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "OperationID":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "OperationID":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.type == other.type and self.id == other.id

    def __str__(self):
        out = []
        out.append(f"type={self.type}")
        out.append(f"id={self.id}") if self.id is not None else None
        return f"<OperationID {[', '.join(out)]}>"
