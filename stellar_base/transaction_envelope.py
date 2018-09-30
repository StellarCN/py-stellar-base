# coding: utf-8
import base64

from .keypair import Keypair
from .network import Network, NETWORKS
from .stellarxdr import Xdr
from .transaction import Transaction
from .utils import hashX_sign_decorated, xdr_hash, convert_hex_to_bytes
from .exceptions import SignatureExistError, PreimageLengthError


class TransactionEnvelope(object):
    """The :class:`TransactionEnvelope` object, which represents a transaction
    envelope ready to sign and submit to send over the network.

    When a transaction is ready to be prepared for sending over the network, it
    must be put into a :class:`TransactionEnvelope`, which includes additional
    metadata such as the signers for a given transaction. Ultimately, this
    class handles signing and conversion to and from XDR for usage on Stellar's
    network.

    :param tx: The transaction that is encapsulated in this envelope.
    :type tx: :class:`Transaction <stellar_base.transaction.Transaction>`
    :param list signatures: which contains a list of signatures that have
          already been created.
    :param str network_id: which contains the network ID for which network this
          transaction envelope is associated with.

    """

    def __init__(self, tx, signatures=None, network_id=None):
        self.tx = tx
        self.signatures = signatures or []
        if network_id:
            if network_id in NETWORKS:
                passphrase = NETWORKS[network_id]
            else:
                passphrase = network_id
        else:
            passphrase = NETWORKS['TESTNET']
        self.network_id = Network(passphrase).network_id()

    def sign(self, keypair):
        """Sign this transaction envelope with a given keypair.

        Note that the signature must not already be in this instance's list of
        signatures.

        :param keypair: The keypair to use for signing this transaction
            envelope.
        :type keypair: :class:`Keypair <stellar_base.keypair.Keypair>`
        :raises: :exc:`SignatureExistError
            <stellar_base.utils.SignatureExistError>`

        """
        assert isinstance(keypair, Keypair)
        tx_hash = self.hash_meta()
        sig = keypair.sign_decorated(tx_hash)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('already signed')
        else:
            self.signatures.append(sig)

    def sign_hashX(self, preimage):
        """Sign this transaction envelope with a Hash(X) signature.

        See Stellar's documentation on `Multi-Sig
        <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_
        for more details on Hash(x) signatures.

        :param preimage: 32 byte hash or hex encoded string, the "x" value to be hashed and used as a
            signature.
        :type preimage: str, bytes

        """
        if len(preimage) > 64:
            raise PreimageLengthError('preimage must <= 64 bytes')
        preimage = convert_hex_to_bytes(preimage)
        sig = hashX_sign_decorated(preimage)
        sig_dict = [signature.__dict__ for signature in self.signatures]
        if sig.__dict__ in sig_dict:
            raise SignatureExistError('already signed')
        else:
            self.signatures.append(sig)

    def hash_meta(self):
        """Get the XDR Hash of the signature base.

        This hash is ultimately what is signed before transactions are sent
        over the network. See :meth:`signature_base` for more details about
        this process.

        :return: The XDR Hash of this transaction envelope's signature base.

        """
        return xdr_hash(self.signature_base())

    def signature_base(self):
        """Get the signature base of this transaction envelope.

        Return the "signature base" of this transaction, which is the value
        that, when hashed, should be signed to create a signature that
        validators on the Stellar Network will accept.

        It is composed of a 4 prefix bytes followed by the xdr-encoded form of
        this transaction.

        :return: The signature base of this transaction envelope.

        """
        network_id = self.network_id
        tx_type = Xdr.StellarXDRPacker()
        tx_type.pack_EnvelopeType(Xdr.const.ENVELOPE_TYPE_TX)
        tx_type = tx_type.get_buffer()

        tx = Xdr.StellarXDRPacker()
        tx.pack_Transaction(self.tx.to_xdr_object())
        tx = tx.get_buffer()
        return network_id + tx_type + tx

    def to_xdr_object(self):
        """Get an XDR object representation of this
        :class:`TransactionEnvelope`.

        """
        tx = self.tx.to_xdr_object()
        return Xdr.types.TransactionEnvelope(tx, self.signatures)

    def xdr(self):
        """Get the base64 encoded XDR string representing this
        :class:`TransactionEnvelope`.

        """
        te = Xdr.StellarXDRPacker()
        te.pack_TransactionEnvelope(self.to_xdr_object())
        te = base64.b64encode(te.get_buffer())
        return te

    @classmethod
    def from_xdr(cls, xdr):
        """Create a new :class:`TransactionEnvelope` from an XDR string.

        :param xdr: The XDR string that represents a transaction
            envelope.
        :type xdr: bytes, str

        """
        xdr_decoded = base64.b64decode(xdr)
        te = Xdr.StellarXDRUnpacker(xdr_decoded)
        te_xdr_object = te.unpack_TransactionEnvelope()
        signatures = te_xdr_object.signatures
        tx_xdr_object = te_xdr_object.tx
        tx = Transaction.from_xdr_object(tx_xdr_object)
        te = TransactionEnvelope(tx, signatures=signatures)
        # te = TransactionEnvelope(
        #     tx, {'signatures': signatures, 'network_id': 'PUBLIC'})
        return te
