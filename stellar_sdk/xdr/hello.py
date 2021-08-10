# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from xdrlib import Packer, Unpacker

from .auth_cert import AuthCert
from .base import Integer, String
from .hash import Hash
from .node_id import NodeID
from .uint32 import Uint32
from .uint256 import Uint256

__all__ = ["Hello"]


class Hello:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct Hello
    {
        uint32 ledgerVersion;
        uint32 overlayVersion;
        uint32 overlayMinVersion;
        Hash networkID;
        string versionStr<100>;
        int listeningPort;
        NodeID peerID;
        AuthCert cert;
        uint256 nonce;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_version: Uint32,
        overlay_version: Uint32,
        overlay_min_version: Uint32,
        network_id: Hash,
        version_str: bytes,
        listening_port: int,
        peer_id: NodeID,
        cert: AuthCert,
        nonce: Uint256,
    ) -> None:
        self.ledger_version = ledger_version
        self.overlay_version = overlay_version
        self.overlay_min_version = overlay_min_version
        self.network_id = network_id
        self.version_str = version_str
        self.listening_port = listening_port
        self.peer_id = peer_id
        self.cert = cert
        self.nonce = nonce

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.overlay_version.pack(packer)
        self.overlay_min_version.pack(packer)
        self.network_id.pack(packer)
        String(self.version_str, 100).pack(packer)
        Integer(self.listening_port).pack(packer)
        self.peer_id.pack(packer)
        self.cert.pack(packer)
        self.nonce.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "Hello":
        ledger_version = Uint32.unpack(unpacker)
        overlay_version = Uint32.unpack(unpacker)
        overlay_min_version = Uint32.unpack(unpacker)
        network_id = Hash.unpack(unpacker)
        version_str = String.unpack(unpacker)
        listening_port = Integer.unpack(unpacker)
        peer_id = NodeID.unpack(unpacker)
        cert = AuthCert.unpack(unpacker)
        nonce = Uint256.unpack(unpacker)
        return cls(
            ledger_version=ledger_version,
            overlay_version=overlay_version,
            overlay_min_version=overlay_min_version,
            network_id=network_id,
            version_str=version_str,
            listening_port=listening_port,
            peer_id=peer_id,
            cert=cert,
            nonce=nonce,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "Hello":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "Hello":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_version == other.ledger_version
            and self.overlay_version == other.overlay_version
            and self.overlay_min_version == other.overlay_min_version
            and self.network_id == other.network_id
            and self.version_str == other.version_str
            and self.listening_port == other.listening_port
            and self.peer_id == other.peer_id
            and self.cert == other.cert
            and self.nonce == other.nonce
        )

    def __str__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"overlay_version={self.overlay_version}",
            f"overlay_min_version={self.overlay_min_version}",
            f"network_id={self.network_id}",
            f"version_str={self.version_str}",
            f"listening_port={self.listening_port}",
            f"peer_id={self.peer_id}",
            f"cert={self.cert}",
            f"nonce={self.nonce}",
        ]
        return f"<Hello {[', '.join(out)]}>"
