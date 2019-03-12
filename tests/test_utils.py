# coding: utf-8
import binascii
from unittest import TestCase
import pytest

from stellar_base import utils
from stellar_base.exceptions import StellarAddressInvalidError, StellarSecretInvalidError, NotValidParamError, \
    DecodeError
from stellar_base.stellarxdr import StellarXDR_pack as Xdr
from stellar_base.utils import is_valid_address, is_valid_secret_key


class TestUtils(TestCase):
    account = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
    bad_account = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSXXXXXX'
    bad_secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6XXX'

    def test_account_xdr_object(self):
        assert isinstance(
            utils.account_xdr_object(self.account), Xdr.types.PublicKey)

    def test_decode_check(self):
        assert type(utils.decode_check('account', self.account)) is bytes

    def test_decode_check_raise(self):
        with pytest.raises(DecodeError, match='Invalid version byte'):
            utils.decode_check('seed', 'GD6H3MA2SIQ3HLSKUVAJ5SJDXM7UWJ4L5N4HMIG3QBDB22GZ5MQPRAGF')

    def test_is_valid_address(self):
        assert type(is_valid_address(self.account)) is bytes
        with pytest.raises(StellarAddressInvalidError, match='Invalid Stellar Address: {}'.format(self.bad_account)):
            utils.is_valid_address(self.bad_account)

    def test_is_valid_secret_key(self):
        assert type(is_valid_secret_key(self.secret)) is bytes
        with pytest.raises(StellarSecretInvalidError, match='Invalid Stellar Secret: {}'.format(self.bad_secret)):
            utils.is_valid_secret_key(self.bad_secret)

    def test_bytes_from_decode_data_raise(self):
        with pytest.raises(NotValidParamError, match="String argument should contain only ASCII characters"):
            utils.bytes_from_decode_data(u"恒星")

    def test_encode_check_raise(self):
        with pytest.raises(NotValidParamError, match="cannot encode null data"):
            utils.encode_check("account", None)

    def test_best_rational_approximation(self):
        assert {'n': 1, 'd': 10} == utils.best_rational_approximation("0.1")
        assert {'n': 1, 'd': 100} == utils.best_rational_approximation("0.01")
        assert {
                   'n': 1,
                   'd': 1000
               } == utils.best_rational_approximation("0.001")
        assert {
                   'n': 54301793,
                   'd': 100000
               } == utils.best_rational_approximation("543.017930")
        assert {
                   'n': 31969983,
                   'd': 100000
               } == utils.best_rational_approximation("319.69983")
        assert {'n': 93, 'd': 100} == utils.best_rational_approximation("0.93")
        assert {'n': 1, 'd': 2} == utils.best_rational_approximation("0.5")
        assert {
                   'n': 173,
                   'd': 100
               } == utils.best_rational_approximation("1.730")
        assert {
                   'n': 5333399,
                   'd': 6250000
               } == utils.best_rational_approximation("0.85334384")
        assert {'n': 11, 'd': 2} == utils.best_rational_approximation("5.5")
        assert {
                   'n': 272783,
                   'd': 100000
               } == utils.best_rational_approximation("2.72783")
        assert {
                   'n': 638082,
                   'd': 1
               } == utils.best_rational_approximation("638082.0")
        assert {
                   'n': 36731261,
                   'd': 12500000
               } == utils.best_rational_approximation("2.93850088")
        assert {
                   'n': 1451,
                   'd': 25
               } == utils.best_rational_approximation("58.04")
        assert {
                   'n': 8253,
                   'd': 200
               } == utils.best_rational_approximation("41.265")
        assert {
                   'n': 12869,
                   'd': 2500
               } == utils.best_rational_approximation("5.1476")
        assert {
                   'n': 4757,
                   'd': 50
               } == utils.best_rational_approximation("95.14")
        assert {
                   'n': 3729,
                   'd': 5000
               } == utils.best_rational_approximation("0.74580")
        assert {
                   'n': 4119,
                   'd': 1
               } == utils.best_rational_approximation("4119.0")
        assert {
                   'n': 1,
                   'd': 100000000
               } == utils.best_rational_approximation("0.00000001")
        assert {
                   'n': 1,
                   'd': 1000000000
               } == utils.best_rational_approximation("0.000000001")
        assert {
                   'n': 1,
                   'd': 500000000
               } == utils.best_rational_approximation("0.000000002")
        assert {
                   'n': 3,
                   'd': 1000000000
               } == utils.best_rational_approximation("0.000000003")
        assert {
                   'n': 2147483647,
                   'd': 1
               } == utils.best_rational_approximation("2147483647")

    def test_best_rational_approximation_not_found_denominator(self):
        with pytest.raises(Exception, match="Couldn't find approximation"):
            utils.best_rational_approximation("0.0000000003")

    def test_best_rational_approximation_not_found_numerator(self):
        with pytest.raises(Exception, match="Couldn't find approximation"):
            utils.best_rational_approximation("2147483648")

    def test_mnemonic_check(self):
        sm = utils.StellarMnemonic()
        m = sm.generate()
        with pytest.raises(utils.MnemonicError):
            sm.to_seed(m + '1')

    def test_mnemonic_lang_chinese(self):
        sm = utils.StellarMnemonic('chinese')
        mnemonic = u'域 监 惜 国 期 碱 珍 继 造 监 剥 电'
        assert sm.check(mnemonic)

    def test_convert_hex_to_bytes(self):
        data = b'\x9f<\x8d\xec\xfc5n\xca\xef?\x11\xb8\x7fx<Z!=\x85>\x94R\x13\xbbI\x1f\xf7i_\xd6\xb0\xf3'
        assert utils.convert_hex_to_bytes(data) == data
        assert utils.convert_hex_to_bytes(binascii.hexlify(data)) == data

        with pytest.raises(NotValidParamError,
                           match="Value should be 32 byte hash or hex encoded string"):
            utils.convert_hex_to_bytes(None)

        bad_value = data + ' '.encode()
        with pytest.raises(NotValidParamError):
            utils.convert_hex_to_bytes(bad_value)
