import stellar_sdk
import stellar_sdk.xdr
from stellar_sdk import SignerKey, SignerKeyType
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
