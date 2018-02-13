# coding: utf-8
import base64

from .keypair import Keypair
from .network import Network, NETWORKS
from .stellarxdr import Xdr
from .transaction import Transaction
from .utils import xdr_hash, SignatureExistError, PreimageLengthError, hashX_sign_decorated


class TransactionEnvelope(object):
    def __init__(self, tx, opts=None):
        self.tx = tx
        try:
            self.signatures = opts.get('signatures') or []
        except AttributeError:
            self.signatures = []
        self.network_id = Network(NETWORKS[opts.get('network_id', 'TESTNET')]).network_id()

    def sign(self, keypair):
        assert isinstance(keypair, Keypair)
        tx_hash = self.hash_meta()
        sig = keypair.sign_decorated(tx_hash)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('already signed')
        else:
            self.signatures.append(sig)

    def sign_hashX(self, preimage):
        if len(preimage) > 64:
            raise PreimageLengthError('preimage must <= 64 bytes')
        sig = hashX_sign_decorated(preimage)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('already signed')
        else:
            self.signatures.append(sig)

    def hash_meta(self):
        return xdr_hash(self.signature_base())

    def signature_base(self):
        network_id = self.network_id
        tx_type = Xdr.StellarXDRPacker()
        tx_type.pack_EnvelopeType(Xdr.const.ENVELOPE_TYPE_TX)
        tx_type = tx_type.get_buffer()

        tx = Xdr.StellarXDRPacker()
        tx.pack_Transaction(self.tx.to_xdr_object())
        tx = tx.get_buffer()
        return network_id + tx_type + tx

    def to_xdr_object(self):
        tx = self.tx.to_xdr_object()
        return Xdr.types.TransactionEnvelope(tx, self.signatures)

    def xdr(self):
        te = Xdr.StellarXDRPacker()
        te.pack_TransactionEnvelope(self.to_xdr_object())
        te = base64.b64encode(te.get_buffer())
        return te

    # can not get network id from XDR , default is 'TESTNET'
    @classmethod
    def from_xdr(cls, xdr):
        xdr_decoded = base64.b64decode(xdr)
        te = Xdr.StellarXDRUnpacker(xdr_decoded)
        te_xdr_object = te.unpack_TransactionEnvelope()
        signatures = te_xdr_object.signatures
        tx_xdr_object = te_xdr_object.tx
        tx = Transaction.from_xdr_object(tx_xdr_object)
        te = TransactionEnvelope(tx, {'signatures': signatures})
        # te = TransactionEnvelope(tx, {'signatures': signatures, 'network_id': 'PUBLIC'})
        return te
