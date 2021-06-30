import pytest

from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import ValueError
from stellar_sdk.muxed_account import MuxedAccount
from stellar_sdk.strkey import StrKey


class TestMuxedAccount:
    def test_init_with_account_id_id(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        account_id_id = 1234
        account_id_muxed = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        med25519 = stellar_xdr.MuxedAccountMed25519(
            id=stellar_xdr.Uint64(account_id_id),
            ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )
        muxed_account_xdr = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_MUXED_ED25519, med25519=med25519
        )
        muxed_account = MuxedAccount(account_id, account_id_id)
        assert muxed_account.account_muxed == account_id_muxed
        assert muxed_account.to_xdr_object().to_xdr() == muxed_account_xdr.to_xdr()
        assert MuxedAccount.from_xdr_object(muxed_account_xdr) == muxed_account

    def test_init_without_account_id_id(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        account_id_id = None
        muxed_account_xdr = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )
        muxed_account = MuxedAccount(account_id, account_id_id)
        assert muxed_account.to_xdr_object().to_xdr() == muxed_account_xdr.to_xdr()
        assert MuxedAccount.from_xdr_object(muxed_account_xdr) == muxed_account
        assert muxed_account.account_muxed is None

    def test_from_account_muxed_account(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        account_id_id = 1234
        account_id_muxed = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        muxed_account = MuxedAccount.from_account(account_id_muxed)
        assert muxed_account.account_id == account_id
        assert muxed_account.account_muxed_id == account_id_id

    def test_from_account_ed25519_account(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        account_id_id = None
        muxed_account = MuxedAccount.from_account(account_id)
        assert muxed_account.account_id == account_id
        assert muxed_account.account_muxed_id == account_id_id

    def test_from_account_invalid_account_raise(self):
        invalid_account = "A" * 100
        with pytest.raises(ValueError, match="This is not a valid account."):
            MuxedAccount.from_account(invalid_account)
