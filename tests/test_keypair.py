import os

import pytest
import nacl.signing as ed25519
from stellar_sdk.exceptions import ValueError, AttributeError

from stellar_sdk.exceptions import (
    Ed25519SecretSeedInvalidError,
    Ed25519PublicKeyInvalidError,
    MissingEd25519SecretSeedError,
    BadSignatureError,
)
from stellar_sdk.keypair import Keypair, _get_key_of_expected_type
from stellar_sdk.strkey import StrKey


class TestKeypair:
    def test_create_random(self):
        kp = Keypair.random()
        public_key = kp.public_key
        secret = kp.secret
        assert StrKey.is_valid_ed25519_public_key(public_key)
        assert StrKey.is_valid_ed25519_secret_seed(secret)

    def test_create_from_secret(self):
        secret = "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        kp = Keypair.from_secret(secret)
        assert isinstance(kp, Keypair)
        assert (
            kp.public_key == "GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7"
        )
        assert kp.secret == secret

    @pytest.mark.parametrize(
        "invalid_secret",
        [
            "",
            "hello",
            "SBWUBZ3SIPLLF5CCXLWUB2Z6UBTYAW34KVXOLRQ5HDAZG4ZY7MHNBWJ1",
            "masterpassphrasemasterpassphrase",
            "gsYRSEQhTffqA9opPepAENCr2WG6z5iBHHubxxbRzWaHf8FBWcu",
        ],
    )
    def test_create_from_invalid_secret_raise(self, invalid_secret):
        with pytest.raises(
            Ed25519SecretSeedInvalidError,
            match="Invalid Ed25519 Secret Seed: {}".format(invalid_secret),
        ):
            Keypair.from_secret(invalid_secret)

    def test_create_from_public_key(self):
        public_key = "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        kp = Keypair.from_public_key(public_key)
        assert isinstance(kp, Keypair)
        assert (
            kp.public_key == "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        assert (
            kp.raw_public_key().hex()
            == "2e3c35010749c1de3d9a5bdd6a31c12458768da5ce87cca6aad63ebbaaef7432"
        )

    @pytest.mark.parametrize(
        "invalid_public_key",
        [
            "",
            "hello" "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DFBAD",
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5Z"
            "masterpassphrasemasterpassphrase",
            "gsYRSEQhTffqA9opPepAENCr2WG6z5iBHHubxxbRzWaHf8FBWcu",
        ],
    )
    def test_create_from_invalid_public_key_raise(self, invalid_public_key):
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(invalid_public_key),
        ):
            Keypair.from_public_key(invalid_public_key)

    def test_can_sign(self):
        can_sign_kp = Keypair.from_secret(
            "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        )
        can_not_sign_kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        assert can_sign_kp.can_sign() is True
        assert can_not_sign_kp.can_sign() is False

    def test_sign_without_secret_raise(self):
        data = b"Hello, Stellar!"
        can_not_sign_kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        with pytest.raises(MissingEd25519SecretSeedError):
            can_not_sign_kp.sign(data)

    def test_sign_and_verify(self):
        kp = Keypair.from_secret(
            "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B"
        )
        data = b"Hello, overcat!"
        signature = kp.sign(data)
        assert (
            signature.hex()
            == "ff7c4346977144019e7be0c12c033e99f412e70361924e298e6152dd924c88f2"
            "725c60c56067f20c35a8ff29c936b983f652b4df2d9de8f2851605df2f680c06"
        )
        kp.verify(data, signature)

    def test_verify_failed_raise(self):
        kp = Keypair.from_secret(
            "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B"
        )
        data = b"Hello, Stellar!"
        signature = kp.sign(data)
        with pytest.raises(BadSignatureError, match="Signature verification failed."):
            kp.verify(data, signature + b"failed")
        with pytest.raises(BadSignatureError, match="Signature verification failed."):
            kp.verify(b"test_verify_failed", signature)

    @pytest.mark.parametrize(
        "secret, hint",
        [
            ("SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36", "0bfad134"),
            ("SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B", "4ab84399"),
            ("SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6", "091e5da1"),
        ],
    )
    def test_signature_hint(self, secret, hint):
        assert Keypair.from_secret(secret).signature_hint().hex() == hint

    def test_get_key_of_expected_type(self):
        raw_seed = os.urandom(32)
        signing_key = ed25519.SigningKey(raw_seed)
        verify_key = signing_key.verify_key
        assert _get_key_of_expected_type(signing_key, ed25519.SigningKey) == signing_key
        assert _get_key_of_expected_type(verify_key, ed25519.VerifyKey) == verify_key

    def test_get_key_of_expected_type_raise(self):
        fake_data = "Hello, overcat!"
        fake_expected = ed25519.SigningKey
        with pytest.raises(
            ValueError,
            match="The given key_type={} is not of type {}.".format(
                type(fake_data), fake_expected
            ),
        ):
            _get_key_of_expected_type(fake_data, fake_expected)

    def test_read_secret_without_secret_raise(self):
        kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        with pytest.raises(MissingEd25519SecretSeedError):
            secret = kp.secret

    def test_set_keypair_raise(self):
        secret = "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        kp = Keypair.from_secret(secret)
        with pytest.raises(
            AttributeError,
            match="Please use `Keypair.from_secret` to generate a new Keypair object.",
        ):
            kp.secret = "SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6"

        with pytest.raises(
            AttributeError,
            match="Please use `Keypair.from_public_key` to generate a new Keypair object.",
        ):
            kp.public_key = "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
