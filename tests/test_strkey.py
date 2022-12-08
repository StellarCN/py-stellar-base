import pytest

from stellar_sdk import StrKey
from stellar_sdk import xdr as stellar_xdr


class TestStrKey:
    def test_encode_ed25519_public_key(self):
        data = b"R#\xd1Yd\xcb%\xb9\x8d\x17\xdf\xc9\xcb\x95JC1a{\xba\xa4\xe5\xdc\x14L\x87\xdf\x0b\x8b;G\xd9"
        encoded = "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
        assert StrKey.encode_ed25519_public_key(data) == encoded

    def test_decode_ed25519_public_key(self):
        decoded = b"R#\xd1Yd\xcb%\xb9\x8d\x17\xdf\xc9\xcb\x95JC1a{\xba\xa4\xe5\xdc\x14L\x87\xdf\x0b\x8b;G\xd9"
        data = "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
        assert StrKey.decode_ed25519_public_key(data) == decoded

    @pytest.mark.parametrize(
        "key",
        [
            "GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7Y",
            "",
            "SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO",
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26",
        ],
    )
    def test_decode_ed25519_public_key_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid Ed25519 Public Key: {key}"):
            StrKey.decode_ed25519_public_key(key)

    def test_encode_ed25519_secret_seed(self):
        data = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        encoded = "SB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLZV4E"
        assert StrKey.encode_ed25519_secret_seed(data) == encoded

    def test_decode_ed25519_secret_seed(self):
        decoded = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        data = "SB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLZV4E"
        assert StrKey.decode_ed25519_secret_seed(data) == decoded

    @pytest.mark.parametrize(
        "key",
        [
            "SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWR",
            "",
            "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC",
        ],
    )
    def test_decode_ed25519_secret_seed_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid Ed25519 Secret Seed: {key}"):
            StrKey.decode_ed25519_secret_seed(key)

    def test_encode_pre_auth_tx(self):
        data = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        encoded = "TB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLZM5K"
        assert StrKey.encode_pre_auth_tx(data) == encoded

    def test_decode_pre_auth_tx(self):
        decoded = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        data = "TB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLZM5K"
        assert StrKey.decode_pre_auth_tx(data) == decoded

    @pytest.mark.parametrize(
        "key",
        [
            "TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH23",
            "",
            "XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL",
        ],
    )
    def test_decode_pre_auth_tx_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid Pre Auth Tx Key: {key}"):
            StrKey.decode_pre_auth_tx(key)

    def test_encode_sha256_hash(self):
        data = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        encoded = "XB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLYIYT"
        assert StrKey.encode_sha256_hash(data) == encoded

    def test_decode_sha256_hash(self):
        decoded = b"}\xd6\x1c\xa0\xd6w\xcd\x0e\xfc+Ts\xe9Blz\x98\xb3\xe6Egh-F\xee|\xbd\x80\x07\xe52\xbc"
        data = "XB65MHFA2Z342DX4FNKHH2KCNR5JRM7GIVTWQLKG5Z6L3AAH4UZLYIYT"
        assert StrKey.decode_sha256_hash(data) == decoded

    @pytest.mark.parametrize(
        "key",
        [
            "XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH23",
            "",
            "TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS",
        ],
    )
    def test_decode_sha256_hash_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid sha256 Hash Key: {key}"):
            StrKey.decode_sha256_hash(key)

    @pytest.mark.parametrize(
        "key, valid",
        [
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7YFMTLB65PYM", True),
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7Y", False),
            ("", False),
            ("SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO", False),
        ],
    )
    def test_is_valid_ed25519_public_key(self, key, valid):
        assert StrKey.is_valid_ed25519_public_key(key) is valid

    @pytest.mark.parametrize(
        "key, valid",
        [
            ("SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO", True),
            ("SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSG", False),
            ("", False),
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7YFMTLB65PYM", False),
        ],
    )
    def test_is_valid_ed25519_secret_seed(self, key, valid):
        assert StrKey.is_valid_ed25519_secret_seed(key) is valid

    @pytest.mark.parametrize(
        "key, valid",
        [
            ("TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS", True),
            ("TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH23", False),
            ("", False),
            ("XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL", False),
        ],
    )
    def test_is_valid_pre_auth_tx(self, key, valid):
        assert StrKey.is_valid_pre_auth_tx(key) is valid

    @pytest.mark.parametrize(
        "key, valid",
        [
            ("XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL", True),
            ("XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH23", False),
            ("", False),
            ("TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS", False),
        ],
    )
    def test_is_valid_sha256_hash(self, key, valid):
        assert StrKey.is_valid_sha256_hash(key) is valid

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

    def test_encode_ed25519_signed_payload(self):
        data = bytes(
            bytearray(
                [
                    0x36,
                    0x3E,
                    0xAA,
                    0x38,
                    0x67,
                    0x84,
                    0x1F,
                    0xBA,
                    0xD0,
                    0xF4,
                    0xED,
                    0x88,
                    0xC7,
                    0x79,
                    0xE4,
                    0xFE,
                    0x66,
                    0xE5,
                    0x6A,
                    0x24,
                    0x70,
                    0xDC,
                    0x98,
                    0xC0,
                    0xEC,
                    0x9C,
                    0x07,
                    0x3D,
                    0x05,
                    0xC7,
                    0xB1,
                    0x03,
                    0x00,
                    0x00,
                    0x00,
                    0x09,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )
        )
        encoded = "PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAEQAAAAAAAAAAAAAAAAAABBXA"
        assert StrKey.encode_ed25519_signed_payload(data) == encoded

    def test_decode_ed25519_signed_payload(self):
        decoded = bytes(
            bytearray(
                [
                    0x36,
                    0x3E,
                    0xAA,
                    0x38,
                    0x67,
                    0x84,
                    0x1F,
                    0xBA,
                    0xD0,
                    0xF4,
                    0xED,
                    0x88,
                    0xC7,
                    0x79,
                    0xE4,
                    0xFE,
                    0x66,
                    0xE5,
                    0x6A,
                    0x24,
                    0x70,
                    0xDC,
                    0x98,
                    0xC0,
                    0xEC,
                    0x9C,
                    0x07,
                    0x3D,
                    0x05,
                    0xC7,
                    0xB1,
                    0x03,
                    0x00,
                    0x00,
                    0x00,
                    0x09,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                ]
            )
        )
        data = "PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAEQAAAAAAAAAAAAAAAAAABBXA"
        assert StrKey.decode_ed25519_signed_payload(data) == decoded

    @pytest.mark.parametrize(
        "key",
        [
            "PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAEQAAAAAAAAAAAAAAAAAABB",
            "",
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY",
        ],
    )
    def test_decode_ed25519_signed_payload_raise(self, key):
        with pytest.raises(
            ValueError, match=f"Invalid Ed25519 Signed Payload Key: {key}"
        ):
            StrKey.decode_ed25519_signed_payload(key)

    @pytest.mark.parametrize(
        "key, valid",
        [
            (
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM",
                True,
            ),
            (
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUAAAAFGBU",
                True,
            ),
            (
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IAAAAAAAAPM",
                False,
            ),
            (
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4Z2PQ",
                False,
            ),
            (
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DXFH6",
                False,
            ),
            ("", False),
            (
                "PDPYP7E6NEYZSVOTV6M23OFM2XRIMPDUJABHGHHH2Y67X7JL25GW6AAAAAAAAAAAAAAJE",
                False,
            ),
            ("GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", False),
            ("PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAAGK7I", False),
        ],
    )
    def test_is_valid_ed25519_signed_payload(self, key, valid):
        assert StrKey.is_valid_ed25519_signed_payload(key) is valid

    def test_encode_contract(self):
        data = bytes(
            bytearray(
                [
                    0x3F,
                    0x0C,
                    0x34,
                    0xBF,
                    0x93,
                    0xAD,
                    0x0D,
                    0x99,
                    0x71,
                    0xD0,
                    0x4C,
                    0xCC,
                    0x90,
                    0xF7,
                    0x05,
                    0x51,
                    0x1C,
                    0x83,
                    0x8A,
                    0xAD,
                    0x97,
                    0x34,
                    0xA4,
                    0xA2,
                    0xFB,
                    0x0D,
                    0x7A,
                    0x03,
                    0xFC,
                    0x7F,
                    0xE8,
                    0x9A,
                ]
            )
        )
        assert (
            StrKey.encode_contract(data)
            == "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        )

    def test_decode_contract(self):
        data = bytes(
            bytearray(
                [
                    0x3F,
                    0x0C,
                    0x34,
                    0xBF,
                    0x93,
                    0xAD,
                    0x0D,
                    0x99,
                    0x71,
                    0xD0,
                    0x4C,
                    0xCC,
                    0x90,
                    0xF7,
                    0x05,
                    0x51,
                    0x1C,
                    0x83,
                    0x8A,
                    0xAD,
                    0x97,
                    0x34,
                    0xA4,
                    0xA2,
                    0xFB,
                    0x0D,
                    0x7A,
                    0x03,
                    0xFC,
                    0x7F,
                    0xE8,
                    0x9A,
                ]
            )
        )
        assert (
            StrKey.decode_contract(
                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
            )
            == data
        )
