# coding: utf-8 

from nose.tools import raises
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

    def test_best_rational_approximation(self):
        assert {'n': 1, 'd': 10} == utils.best_rational_approximation("0.1")
        assert {'n': 1, 'd': 100} == utils.best_rational_approximation("0.01")
        assert {'n': 1, 'd': 1000} == utils.best_rational_approximation("0.001")
        assert {'n': 54301793, 'd': 100000} == utils.best_rational_approximation("543.017930")
        assert {'n': 31969983, 'd': 100000} == utils.best_rational_approximation("319.69983")
        assert {'n': 93, 'd': 100} == utils.best_rational_approximation("0.93")
        assert {'n': 1, 'd': 2} == utils.best_rational_approximation("0.5")
        assert {'n': 173, 'd': 100} == utils.best_rational_approximation("1.730")
        assert {'n': 5333399, 'd': 6250000} == utils.best_rational_approximation("0.85334384")
        assert {'n': 11, 'd': 2} == utils.best_rational_approximation("5.5")
        assert {'n': 272783, 'd': 100000} == utils.best_rational_approximation("2.72783")
        assert {'n': 638082, 'd': 1} == utils.best_rational_approximation("638082.0")
        assert {'n': 36731261, 'd': 12500000} == utils.best_rational_approximation("2.93850088")
        assert {'n': 1451, 'd': 25} == utils.best_rational_approximation("58.04")
        assert {'n': 8253, 'd': 200} == utils.best_rational_approximation("41.265")
        assert {'n': 12869, 'd': 2500} == utils.best_rational_approximation("5.1476")
        assert {'n': 4757, 'd': 50} == utils.best_rational_approximation("95.14")
        assert {'n': 3729, 'd': 5000} == utils.best_rational_approximation("0.74580")
        assert {'n': 4119, 'd': 1} == utils.best_rational_approximation("4119.0")
        assert {'n': 1, 'd': 100000000} == utils.best_rational_approximation("0.00000001")
        assert {'n': 1, 'd': 1000000000} == utils.best_rational_approximation("0.000000001")
        assert {'n': 1, 'd': 500000000} == utils.best_rational_approximation("0.000000002")
        assert {'n': 3, 'd': 1000000000} == utils.best_rational_approximation("0.000000003")
        assert {'n': 2147483647, 'd': 1} == utils.best_rational_approximation("2147483647")

    @raises(Exception)
    def test_best_rational_approximation_not_found_denominator(self):
        utils.best_rational_approximation("0.0000000003")

    @raises(Exception)
    def test_best_rational_approximation_not_found_numerator(self):
        utils.best_rational_approximation("2147483648")

    @raises(utils.MnemonicError)
    def test_mnemonic_check(self):
        sm = utils.StellarMnemonic()
        m = sm.generate()
        sm.to_seed(m + '1')

    def test_menonic(self):
        sm = utils.StellarMnemonic('chinese')
        mnemonic = u'域 监 惜 国 期 碱 珍 继 造 监 剥 电'
        assert sm.check(mnemonic)
