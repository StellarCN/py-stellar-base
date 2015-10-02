from unittest import TestCase
from stellar_base.asset import Asset
from stellar_base.stellarxdr import StellarXDR_pack as Xdr


class TestAsset(TestCase):

    def test_native(self):
        self.assertEqual('XLM', Asset.native().code)
        self.assertEqual(None,Asset.native().issuer)

    def test_is_native(self):
        native = Asset('XLM')
        cny = Asset('CNY','GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG')
        self.assertTrue(native.is_native())
        self.assertFalse(cny.is_native())

    def test_to_xdr_object(self):
        cny = Asset('CNY','GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG')
        self.assertIsInstance(cny.test_to_xdr_object(), Xdr.types.Asset)
