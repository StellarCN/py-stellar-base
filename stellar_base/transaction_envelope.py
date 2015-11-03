# coding: utf-8
from .network import Network, NETWORKS
from .utils import xdr_hash
from .stellarxdr import StellarXDR_pack as Xdr
from .keypair import Keypair
import base64


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
        self.signatures.append(sig)
        return self

    def hash_meta(self):
        return xdr_hash(self.signature_base())

    def signature_base(self):
        network_id = self.network_id
        tx_type = Xdr.STELLARXDRPacker()
        tx_type.pack_EnvelopeType(Xdr.const.ENVELOPE_TYPE_TX)
        tx_type = tx_type.get_buffer()

        tx = Xdr.STELLARXDRPacker()
        tx.pack_Transaction(self.tx.to_xdr_object())
        tx = tx.get_buffer()
        return network_id+tx_type+tx

    def to_xdr_object(self):
        tx = self.tx.to_xdr_object()
        return Xdr.types.TransactionEnvelope(tx, self.signatures)

    def xdr(self):
        te = Xdr.STELLARXDRPacker()
        te.pack_TransactionEnvelope(self.to_xdr_object())
        # te = base64.encodebytes(te.get_buffer()) # with \n
        te = base64.b64encode(te.get_buffer())
        return te
