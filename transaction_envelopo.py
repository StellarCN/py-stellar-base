# coding: utf-8
from .network import Network
from .hash import hash
from .stellarxdr import StellarXDR_pack as Xdr
import base64


class TransactionEnvelope(object):

    def __init__(self, tx, opts=None):
        self.tx = tx
        try:
            self.signatures = opts.get('signatures')
        except:
            self.signatures = []

    def sign(self, *args):
        tx_hash = self.hash()
        for kp in args:
            sig = kp.signDecorated(tx_hash)
            self.signatures.append(sig)

    def hash(self):
        return hash(self.signature_base())

    def signature_base(self):
        network_id = Network.use_testnet_work().network_id()
        tx_type = bytes([Xdr.const.ENVELOPE_TYPE_TX])  # int to bytes
        tx = Xdr.STELLARXDRPacker()
        tx.pack_Transaction(self.tx.to_xdr_object())
        tx = tx.get_buffer()
        return network_id+tx_type+tx

    def to_xdr_object(self):
        return Xdr.types.TransactionEnvelope(self.tx.to_xdr_object(), self.signatures)

    def submit(self):
        te = Xdr.STELLARXDRPacker()
        te.pack_TransactionEnvelope(self.to_xdr_object())
        te = base64.encodebytes(te.get_buffer())
        return te
