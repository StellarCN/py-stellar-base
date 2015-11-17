from stellar_base import utils
from stellar_base.stellarxdr import StellarXDR_pack as Xdr

class TestUtils():
    def __init__(self):
        self.account = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
        self.secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'

    def test_account_xdr_object(self):
        assert isinstance(utils.account_xdr_object(self.account), Xdr.types.PublicKey)

    def test_decode_check(self):
        assert type(utils.decode_check('account', self.account)) is bytes

    # def test_encode_check(self):
        # TODO

