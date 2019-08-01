from .stellarxdr import Xdr
from .strkey import StrKey


class Signer:
    """The :class:`Signer` object, which represents an account signer on Stellar's network.

    :param signer: The XDR signer object
    """

    def __init__(self, signer: Xdr.types.SignerKey) -> 'None':
        self.signer = signer

    @classmethod
    def ed25519_public_key(cls, account_id: str) -> 'Signer':
        """Create ED25519 PUBLIC KEY Signer from account id.

        :param account_id: account id
        :return: ED25519 PUBLIC KEY Signer
        """
        signer = Xdr.types.SignerKey(Xdr.const.SIGNER_KEY_TYPE_ED25519,
                                     ed25519=StrKey.decode_ed25519_public_key(account_id))
        return cls(signer)

    @classmethod
    def pre_auth_tx(cls, pre_auth_tx_hash: bytes) -> 'Signer':
        """Create Pre AUTH TX Signer from the sha256 hash of a transaction,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#pre-authorized-transaction>`_ for more information.

        :param pre_auth_tx_hash: The sha256 hash of a transaction.
        :return: Pre AUTH TX Signer
        """
        signer = Xdr.types.SignerKey(
            Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX, preAuthTx=pre_auth_tx_hash)

        return cls(signer)

    @classmethod
    def sha256_hash(cls, sha256_hash: bytes) -> 'Signer':
        """Create SHA256 HASH Signer from a sha256 hash of a preimage,
        click `here <https://www.stellar.org/developers/guides/concepts/multi-sig.html#hashx>`_ for more information.

        :param sha256_hash: a sha256 hash of a preimage
        :return: SHA256 HASH Signer
        """
        signer = Xdr.types.SignerKey(
            Xdr.const.SIGNER_KEY_TYPE_HASH_X, hashX=sha256_hash)
        return cls(signer)
