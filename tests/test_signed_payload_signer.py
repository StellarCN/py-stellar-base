import binascii

import pytest

import stellar_sdk.xdr as stellar_xdr
from stellar_sdk import SignedPayloadSigner, StrKey


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
        assert signed_payload_signer.encoded_signer_key == strkey
        assert (
            SignedPayloadSigner.from_encoded_signer_key(strkey) == signed_payload_signer
        )

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
        xdr_obj = signed_payload_signer.to_xdr_object()
        assert (
            xdr_obj.type
            == stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        )
        assert (
            xdr_obj.ed25519_signed_payload.ed25519.uint256
            == StrKey.decode_ed25519_public_key(account_id)
        )
        assert xdr_obj.ed25519_signed_payload.payload == payload
        assert signed_payload_signer == SignedPayloadSigner.from_xdr_object(xdr_obj)
