import unittest
from stellar_base import utils
from stellar_base.stellarxdr import StellarXDR_pack as Xdr


class UtilsTest(unittest.TestCase):
    def __init__(self):
        #super().__init__()
        self.account = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
        self.secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'

    def test_account_xdr_object(self):
        self.assertIsInstance(Xdr.types.PublicKey, utils.account_xdr_object(self.account))

    def test_decode_check(self):
        self.assertTrue(type(utils.decode_check('account', self.account)) is bytes)

    def test_encode_check(self):
        pass

