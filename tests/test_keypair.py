import unittest
from stellar_base.keypair import Keypair


class TestKeypair(unittest.TestCase):
    def test_sep0005(self):
        # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
        mnemonic = 'illness spike retreat truth genius clock brain pass fit cave bargain toe'
        seed = Keypair.deterministic(mnemonic).seed().decode()
        seed_expect = 'SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN'
        self.assertEqual(seed, seed_expect)
        address = Keypair.deterministic(mnemonic, index=6).address().decode()
        address_expect = 'GBY27SJVFEWR3DUACNBSMJB6T4ZPR4C7ZXSTHT6GMZUDL23LAM5S2PQX'
        self.assertEqual(address, address_expect)

        mnemonic = 'cable spray genius state float twenty onion head street palace net private method loan turn phrase state blanket interest dry amazing dress blast tube'
        seed = Keypair.deterministic(mnemonic, passphrase='p4ssphr4se').seed().decode()
        seed_expect = 'SAFWTGXVS7ELMNCXELFWCFZOPMHUZ5LXNBGUVRCY3FHLFPXK4QPXYP2X'
        self.assertEqual(seed, seed_expect)
        address = Keypair.deterministic(mnemonic, passphrase='p4ssphr4se', index=9).address().decode()
        address_expect = 'GBOSMFQYKWFDHJWCMCZSMGUMWCZOM4KFMXXS64INDHVCJ2A2JAABCYRR'
        self.assertEqual(address, address_expect)

        mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
        seed = Keypair.deterministic(mnemonic).seed().decode()
        seed_expect = 'SBUV3MRWKNS6AYKZ6E6MOUVF2OYMON3MIUASWL3JLY5E3ISDJFELYBRZ'
        self.assertEqual(seed, seed_expect)
        address = Keypair.deterministic(mnemonic, index=8).address().decode()
        address_expect = 'GABTYCZJMCP55SS6I46SR76IHETZDLG4L37MLZRZKQDGBLS5RMP65TSX'
        self.assertEqual(address, address_expect)
