from unittest import TestCase
from pytest import raises

from stellar_base.keypair import Keypair
from stellar_base.exceptions import MissingSigningKeyError


def test_sep0005():
    # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
    mnemonic = 'illness spike retreat truth genius clock brain pass fit cave bargain toe'
    seed = Keypair.deterministic(mnemonic).seed()
    assert seed == b'SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN'
    address = Keypair.deterministic(mnemonic, index=6).address().decode()
    assert address == 'GBY27SJVFEWR3DUACNBSMJB6T4ZPR4C7ZXSTHT6GMZUDL23LAM5S2PQX'

    mnemonic = 'cable spray genius state float twenty onion head street palace net private method loan turn phrase state blanket interest dry amazing dress blast tube'
    seed = Keypair.deterministic(mnemonic, passphrase='p4ssphr4se').seed()
    assert seed == b'SAFWTGXVS7ELMNCXELFWCFZOPMHUZ5LXNBGUVRCY3FHLFPXK4QPXYP2X'
    address = Keypair.deterministic(
        mnemonic, passphrase='p4ssphr4se', index=9).address().decode()
    assert address == 'GBOSMFQYKWFDHJWCMCZSMGUMWCZOM4KFMXXS64INDHVCJ2A2JAABCYRR'

    mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
    seed = Keypair.deterministic(mnemonic).seed()
    assert seed == b'SBUV3MRWKNS6AYKZ6E6MOUVF2OYMON3MIUASWL3JLY5E3ISDJFELYBRZ'
    address = Keypair.deterministic(mnemonic, index=8).address().decode()
    assert address == 'GABTYCZJMCP55SS6I46SR76IHETZDLG4L37MLZRZKQDGBLS5RMP65TSX'


class KeypairTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mnemonic = ('illness spike retreat truth genius clock brain pass '
                        'fit cave bargain toe')
        cls.key_pair0 = Keypair.deterministic(cls.mnemonic)

    def test_from_seed(self):
        key_pair = Keypair.from_seed(self.key_pair0.seed())
        assert self.key_pair0.address() == key_pair.address()

    def test_sign_missing_signing_key_raise(self):
        key_pair = Keypair.from_address(self.key_pair0.address())
        raises(MissingSigningKeyError, key_pair.sign, "")

    def test_init_wrong_type_key_raise(self):
        raises(TypeError, Keypair, self.mnemonic)
