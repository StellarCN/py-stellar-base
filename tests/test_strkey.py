import pytest

from stellar_sdk.strkey import StrKey
from stellar_sdk import xdr as stellarxdr


class TestStrKey:
    # TODO: we need more tests here
    @pytest.mark.parametrize(
        "key",
        [
            ("GAAAAAAAACGC6",),
            ("MAAAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITLVL7",),
            ("GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZA",),
            ("GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUACUSI",),
            ("G47QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVP2I",),
            ("MCAAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITKNOGA",),
            (
                "MAAAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITIADJPA",
            ),
            ("M4AAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITIU2K",),
            (
                "MAAAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITLVL6===",
            ),
            ("MAAAAAAAAAAAAAB7BQ2L7E5NBWMXDUCMZSIPOBKRDSBYVLMXGSSKF6YNPIB7Y77ITLVL4",),
        ],
    )
    def test_decode_invalid_muxed_account_raise(self, key):
        with pytest.raises(ValueError):
            StrKey.decode_muxed_account(key)

    def test_decode_muxed_account_med25519(self):
        # account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        # account_id_id = 1234
        account_id_muxed = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        decoded = StrKey.decode_muxed_account(account_id_muxed).to_xdr()
        assert decoded == "AAABAAAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="

    def test_decode_muxed_account_ed25519(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        # account_id_id = 1234
        # account_id_muxed = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        decoded = StrKey.decode_muxed_account(account_id)
        assert (
            decoded.to_xdr()
            == stellarxdr.MuxedAccount(
                type=stellarxdr.CryptoKeyType.KEY_TYPE_ED25519,
                ed25519=stellarxdr.Uint256(
                    StrKey.decode_ed25519_public_key(account_id)
                ),
            ).to_xdr()
        )

    def test_encode_muxed_account_ed25519(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        data = stellarxdr.MuxedAccount(
            type=stellarxdr.CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=stellarxdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )
        encoded = StrKey.encode_muxed_account(data)
        assert encoded == StrKey.encode_ed25519_public_key(
            StrKey.decode_ed25519_public_key(account_id)
        )

    def test_encode_muxed_account_med25519(self):
        data = stellarxdr.MuxedAccount.from_xdr(
            "AAABAAAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="
        )
        expected = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        assert StrKey.encode_muxed_account(data) == expected
