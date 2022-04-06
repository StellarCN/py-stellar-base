import binascii

import pytest

import stellar_sdk
import stellar_sdk.xdr
from stellar_sdk import SignedPayloadSigner, SignerKey, SignerKeyType, StrKey
from stellar_sdk import xdr as stellar_xdr


class TestSignerKey:
    def test_ed25519_public_key(self):
        account_id = "GCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVPIYV"
        signer_key_data = b"\x85\xba{e\xeb\x92\x83r\xb2\xf5\xc4Z$\xc2\x84b\xc6\x8a\xa6\x04\x86dg$x6\x0c\xeb\x9aW\x13W"
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_ED25519
        signer_key = SignerKey(signer_key_data, signer_key_type)
        signer_key_xdr = stellar_xdr.SignerKey(
            type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519,
            ed25519=stellar_sdk.xdr.Uint256(signer_key_data),
        )
        assert signer_key.to_xdr_object() == signer_key_xdr
        assert signer_key.encoded_signer_key == account_id
        assert SignerKey.from_xdr_object(signer_key_xdr) == signer_key
        assert SignerKey.ed25519_public_key(account_id) == signer_key
        assert SignerKey.ed25519_public_key(signer_key_data) == signer_key

    def test_pre_auth_tx(self):
        pre_auth_tx = "TCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVOVKE"
        signer_key_data = b"\x85\xba{e\xeb\x92\x83r\xb2\xf5\xc4Z$\xc2\x84b\xc6\x8a\xa6\x04\x86dg$x6\x0c\xeb\x9aW\x13W"
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX
        signer_key = SignerKey(signer_key_data, signer_key_type)
        signer_key_xdr = stellar_xdr.SignerKey(
            type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_PRE_AUTH_TX,
            pre_auth_tx=stellar_sdk.xdr.Uint256(signer_key_data),
        )
        assert signer_key.to_xdr_object() == signer_key_xdr
        assert signer_key.encoded_signer_key == pre_auth_tx
        assert SignerKey.from_xdr_object(signer_key_xdr) == signer_key
        assert SignerKey.pre_auth_tx(pre_auth_tx) == signer_key
        assert SignerKey.pre_auth_tx(signer_key_data) == signer_key

    def test_sha256_hash(self):
        sha256_hash = "XCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVPRP5"
        signer_key_data = b"\x85\xba{e\xeb\x92\x83r\xb2\xf5\xc4Z$\xc2\x84b\xc6\x8a\xa6\x04\x86dg$x6\x0c\xeb\x9aW\x13W"
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_HASH_X
        signer_key = SignerKey(signer_key_data, signer_key_type)
        signer_key_xdr = stellar_xdr.SignerKey(
            type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_HASH_X,
            hash_x=stellar_sdk.xdr.Uint256(signer_key_data),
        )
        assert signer_key.to_xdr_object() == signer_key_xdr
        assert signer_key.encoded_signer_key == sha256_hash
        assert SignerKey.from_xdr_object(signer_key_xdr) == signer_key
        assert SignerKey.sha256_hash(sha256_hash) == signer_key
        assert SignerKey.sha256_hash(signer_key_data) == signer_key

    def test_ed25519_signed_payload(self):
        ed25519_signed_payload = "PA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAAAAAEQAAAAAAAAAAAAAAAAAABBXA"
        signer_key_data = bytes(
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
        signer_key_type = SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        signer_key = SignerKey(signer_key_data, signer_key_type)
        signer_key_xdr = stellar_xdr.SignerKey(
            type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD,
            ed25519_signed_payload=stellar_xdr.SignerKeyEd25519SignedPayload(
                ed25519=stellar_xdr.Uint256(
                    bytes(
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
                            ]
                        )
                    )
                ),
                payload=bytes(
                    bytearray(
                        [
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
                ),
            ),
        )
        assert signer_key.to_xdr_object() == signer_key_xdr
        assert signer_key.encoded_signer_key == ed25519_signed_payload
        assert SignerKey.from_xdr_object(signer_key_xdr) == signer_key
        assert SignerKey.ed25519_signed_payload(ed25519_signed_payload) == signer_key
        assert SignerKey.ed25519_signed_payload(signer_key_data) == signer_key


class TestSignedPayloadSigner:
    @pytest.mark.parametrize(
        "account_id, payload, strkey",
        [
            (
                "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
                "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20",
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM",
            ),
            (
                "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
                "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d",
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUAAAAFGBU",
            ),
        ],
    )
    def test_encoded_signer_key(self, account_id, payload, strkey):
        payload = binascii.unhexlify(payload)
        signed_payload_signer = SignedPayloadSigner(account_id, payload)
        signer_key = SignerKey.ed25519_signed_payload(signed_payload_signer)
        assert signer_key.encoded_signer_key == strkey

    @pytest.mark.parametrize(
        "account_id, payload, strkey",
        [
            (
                "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
                "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20",
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM",
            ),
            (
                "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
                "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d",
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUAAAAFGBU",
            ),
        ],
    )
    def test_xdr(self, account_id, payload, strkey):
        payload = binascii.unhexlify(payload)
        signed_payload_signer = SignedPayloadSigner(account_id, payload)
        signer_key = SignerKey.ed25519_signed_payload(signed_payload_signer)

        xdr_obj = signer_key.to_xdr_object()
        assert (
            xdr_obj.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        )
        assert (
            xdr_obj.ed25519_signed_payload.ed25519.uint256
            == StrKey.decode_ed25519_public_key(account_id)
        )
        assert xdr_obj.ed25519_signed_payload.payload == payload
        assert (
            signed_payload_signer
            == SignerKey.from_xdr_object(xdr_obj).to_signed_payload_signer()
        )
