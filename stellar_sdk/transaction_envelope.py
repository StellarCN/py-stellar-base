import typing

from .transaction import Transaction
from .exceptions import SignatureExistError
from .keypair import Keypair
from .utils import sha256
from .network import Network
from .stellarxdr import Xdr


class TransactionEnvelope:
    def __init__(self, tx, network: Network, signatures: typing.List[Xdr.types.DecoratedSignature] = None) -> None:
        self.tx = tx
        self.network_id = network.network_id()
        self.signatures = signatures or []

    def signature_base(self) -> bytes:
        network_id = self.network_id
        tx_type = Xdr.StellarXDRPacker()
        tx_type.pack_EnvelopeType(Xdr.const.ENVELOPE_TYPE_TX)
        tx_type = tx_type.get_buffer()

        tx = Xdr.StellarXDRPacker()
        tx.pack_Transaction(self.tx.to_xdr_object())
        tx = tx.get_buffer()
        return network_id + tx_type + tx

    def hash(self) -> bytes:
        return sha256(self.signature_base())

    def sign(self, signer: Keypair) -> None:
        tx_hash = self.hash()
        sig = signer.sign_decorated(tx_hash)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('The keypair has already signed.')
        else:
            self.signatures.append(sig)

    def sign_hashx(self, preimage: bytes) -> None:
        hash_preimage = sha256(preimage)
        hint = hash_preimage[-4:]
        sig = Xdr.types.DecoratedSignature(hint, preimage)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('The preimage has already signed.')
        else:
            self.signatures.append(sig)

    def to_xdr_object(self) -> Xdr.types.TransactionEnvelope:
        tx = self.tx.to_xdr_object()
        transaction_envelope = Xdr.types.TransactionEnvelope(tx, self.signatures)
        return transaction_envelope

    def to_xdr(self) -> str:
        return self.to_xdr_object().to_xdr()

    @classmethod
    def from_xdr_object(cls, te_xdr_object: Xdr.types.TransactionEnvelope, network: Network) -> 'TransactionEnvelope':
        signatures = te_xdr_object.signatures
        tx_xdr_object = te_xdr_object.tx
        tx = Transaction.from_xdr_object(tx_xdr_object)
        te = TransactionEnvelope(tx, network=network, signatures=signatures)
        return te

    @classmethod
    def from_xdr(cls, xdr: str, network: Network) -> 'TransactionEnvelope':
        xdr_object = Xdr.types.TransactionEnvelope.from_xdr(xdr)
        return cls.from_xdr_object(xdr_object, network)
