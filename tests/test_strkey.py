import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.strkey import StrKey


class TestStrKey:
    # TODO: we need more tests here
    @pytest.mark.parametrize(
        "key",
        [
            "GAAAAAAAACGC6",
            "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUR",
            "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZA",
            "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUACUSI",
            "G47QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVP2I",
            "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVAAAAAAAAAAAAAJLKA",
            "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVAAAAAAAAAAAAAAV75I",
            "M47QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUQ",
            "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUK===",
            "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUO",
        ],
    )
    def test_decode_invalid_muxed_account_raise(self, key):
        with pytest.raises(ValueError):
            StrKey.decode_muxed_account(key)

    def test_decode_muxed_account_med25519(self):
        # account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        # account_id_id = 1234
        account_id_muxed = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        decoded = StrKey.decode_muxed_account(account_id_muxed)
        assert (
            decoded.to_xdr()
            == "AAABAAAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="
        )

    def test_decode_muxed_account_ed25519(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        # account_id_id = 1234
        # account_id_muxed = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        decoded = StrKey.decode_muxed_account(account_id)
        assert (
            decoded.to_xdr()
            == stellar_xdr.MuxedAccount(
                type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
                ed25519=stellar_xdr.Uint256(
                    StrKey.decode_ed25519_public_key(account_id)
                ),
            ).to_xdr()
        )

    def test_encode_muxed_account_ed25519(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        data = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )
        encoded = StrKey.encode_muxed_account(data)
        assert encoded == account_id

    def test_encode_muxed_account_med25519(self):
        data = stellar_xdr.MuxedAccount.from_xdr(
            "AAABAAAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="
        )
        expected = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        assert StrKey.encode_muxed_account(data) == expected
