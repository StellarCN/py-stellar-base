# coding: utf-8

from .network import Network
from .hash import hash
from .stellarxdr import StellarXDR_pack as xdr
import base64


class TransactionEnvelope(object):

    def __init__(self, tx, opts=None):
        self.tx = tx
        try:
            self.signatures = opts.get('signatures')
        except:
            self.signatures = []

    def sign(self, *args):
        txHash = self.hash()
        for kp in args:
            sig = kp.signDecorated(txHash)
            self.signatures.append(sig)

    def hash(self):
        return hash(self.signatureBase())

    def signatureBase(self):
        networkId = Network.useTestNetwork().networkId()
        tx_type = bytes([xdr.const.ENVELOPE_TYPE_TX]) # int to bytes
        tx = xdr.STELLARXDRPacker()
        tx.pack_Transaction(self.tx.toXDRObject())
        tx = tx.get_buffer()
        return networkId+tx_type+tx

    def toXDRObject(self):
        return xdr.types.TransactionEnvelope(self.tx.toXDRObject(), self.signatures)

    def submit(self):
        te = xdr.STELLARXDRPacker()
        te.pack_TransactionEnvelope(self.toXDRObject())
        te = base64.encodebytes(te.get_buffer())
        return te
