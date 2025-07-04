import binascii

import pytest

from stellar_sdk import StrKey
from stellar_sdk import xdr as stellar_xdr


class TestStrKey:
    def test_encode_ed25519_public_key(self):
        data = binascii.unhexlify(
            "5223d15964cb25b98d17dfc9cb954a4331617bbaa4e5dc144c87df0b8b3b47d9"
        )
        encoded = "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
        assert StrKey.encode_ed25519_public_key(data) == encoded

    def test_decode_ed25519_public_key(self):
        decoded = binascii.unhexlify(
            "5223d15964cb25b98d17dfc9cb954a4331617bbaa4e5dc144c87df0b8b3b47d9"
        )
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

    @pytest.mark.parametrize(
        "key",
        [
            "GAAAAAAAACGC6",
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY",
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
    def test_decode_invalid_med25519_public_key_raise(self, key):
        with pytest.raises(ValueError):
            StrKey.decode_med25519_public_key(key)

    def test_decode_med25519_public_key(self):
        # account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        # account_id_id = 1234
        account_id_muxed = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        decoded = StrKey.decode_med25519_public_key(account_id_muxed)
        assert len(decoded) == 40
        assert (
            StrKey.encode_ed25519_public_key(decoded[0:32])
            == "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        )
        assert int.from_bytes(decoded[32:], "big") == 1234

    def test_encode_med25519_public_key(self):
        # GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY + 1234
        data = StrKey.decode_ed25519_public_key(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        ) + int.to_bytes(1234, 8, "big")
        expected = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        assert StrKey.encode_med25519_public_key(data) == expected

    @pytest.mark.parametrize(
        "key, valid",
        [
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7YFMTLB65PYM", False),
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7Y", False),
            ("", False),
            ("SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO", False),
            (
                "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26",
                True,
            ),
        ],
    )
    def test_is_valid_med25519_public_key(self, key, valid):
        assert StrKey.is_valid_med25519_public_key(key) is valid

    def test_encode_ed25519_signed_payload(self):
        data = binascii.unhexlify(
            "363eaa3867841fbad0f4ed88c779e4fe66e56a2470dc98c0ec9c073d05c7b10300000009000000000000000000000000"
        )
        encoded = "PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAEQAAAAAAAAAAAAAAAAAABBXA"
        assert StrKey.encode_ed25519_signed_payload(data) == encoded

    def test_decode_ed25519_signed_payload(self):
        decoded = binascii.unhexlify(
            "363eaa3867841fbad0f4ed88c779e4fe66e56a2470dc98c0ec9c073d05c7b10300000009000000000000000000000000"
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
        data = binascii.unhexlify(
            "3f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.encode_contract(data)
            == "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        )

    def test_decode_contract(self):
        data = binascii.unhexlify(
            "3f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.decode_contract(
                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
            )
            == data
        )

    def test_encode_liquidity_pool(self):
        data = binascii.unhexlify(
            "3f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.encode_liquidity_pool(data)
            == "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
        )

    def test_decode_liquidity_pool(self):
        data = binascii.unhexlify(
            "3f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.decode_liquidity_pool(
                "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
            )
            == data
        )

    @pytest.mark.parametrize(
        "key",
        [
            "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA",
            "",
            "SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO",
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26",
        ],
    )
    def test_decode_liquidity_pool_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid Liquidity Pool Key: {key}"):
            StrKey.decode_liquidity_pool(key)

    def test_encode_claimable_balance(self):
        data = binascii.unhexlify(
            "003f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.encode_claimable_balance(data)
            == "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
        )

    def test_decode_claimable_balance(self):
        data = binascii.unhexlify(
            "003f0c34bf93ad0d9971d04ccc90f705511c838aad9734a4a2fb0d7a03fc7fe89a"
        )
        assert (
            StrKey.decode_claimable_balance(
                "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
            )
            == data
        )

    @pytest.mark.parametrize(
        "key",
        [
            "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4T",
            "",
            "SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO",
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26",
        ],
    )
    def test_decode_claimable_balance_raise(self, key):
        with pytest.raises(ValueError, match=f"Invalid Claimable Balance Key: {key}"):
            StrKey.decode_claimable_balance(key)
