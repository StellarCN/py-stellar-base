import pytest

from stellar_sdk import Account, MuxedAccount
from stellar_sdk.account import Thresholds
from stellar_sdk.exceptions import (
    Ed25519PublicKeyInvalidError,
    MuxedEd25519AccountInvalidError,
)
from stellar_sdk.sep.ed25519_public_key_signer import Ed25519PublicKeySigner


class TestAccount:
    def test_init_with_ed25519_key(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        assert account.account == MuxedAccount(account_id, None)
        assert account.sequence == sequence
        assert account.universal_account_id == account_id

    def test_init_with_muxed_account_key(self):
        account_muxed = (
            "MA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOAAAAAAAAAAE2LEM6"
        )
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        account_muxed_id = 1234
        sequence = 123123
        account = Account(account=account_muxed, sequence=sequence)
        assert account.sequence == sequence
        assert account.account == MuxedAccount(account_id, account_muxed_id)
        assert account.universal_account_id == account_muxed

    def test_init_with_muxed_account(self):
        account_muxed = MuxedAccount.from_account(
            "MA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOAAAAAAAAAAE2LEM6"
        )
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        account_muxed_id = 1234
        sequence = 123123
        account = Account(account=account_muxed, sequence=sequence)
        assert account.sequence == sequence
        assert account.account == MuxedAccount(account_id, account_muxed_id)
        assert account.universal_account_id == account_muxed.universal_account_id

    def test_increment_sequence_number(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        account.increment_sequence_number()
        assert account.account == MuxedAccount(account_id, None)
        assert account.sequence == sequence + 1
        assert account.universal_account_id == account_id

    def test_load_ed25519_public_key_signers(self):
        signers = [
            {
                "weight": 10,
                "key": "XCRJANZNX6PX42O2PTZ5PTKAQYZNQOXHDRF7PI7ANSJSW4RKGT63XCDN",
                "type": "sha256_hash",
            },
            {
                "weight": 1,
                "key": "GCV5YZ7R6IAKQCIGDP6TS6GHUXSNWVLP2CNRCUSIPQFRX67LGQRXTCL6",
                "type": "ed25519_public_key",
            },
            {
                "weight": 2,
                "key": "GBUGPGCH6YTEOT2CQJDRYPIXK5KTVUZOWIQMLIAOLYKZMPWT23CVQMPH",
                "type": "ed25519_public_key",
            },
        ]
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(
            account=account_id, sequence=sequence, raw_data={"signers": signers}
        )
        assert account.load_ed25519_public_key_signers() == [
            Ed25519PublicKeySigner(
                "GCV5YZ7R6IAKQCIGDP6TS6GHUXSNWVLP2CNRCUSIPQFRX67LGQRXTCL6", 1
            ),
            Ed25519PublicKeySigner(
                "GBUGPGCH6YTEOT2CQJDRYPIXK5KTVUZOWIQMLIAOLYKZMPWT23CVQMPH", 2
            ),
        ]

    def test_thresholds(self):
        thresholds = {"low_threshold": 10, "med_threshold": 20, "high_threshold": 30}
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(
            account=account_id, sequence=sequence, raw_data={"thresholds": thresholds}
        )
        assert account.thresholds == Thresholds(10, 20, 30)

    def test_account_with_invalid_account_raise(self):
        invalid_account_id = "INVALID"
        with pytest.raises(
            ValueError, match=f"This is not a valid account: {invalid_account_id}"
        ):
            Account(invalid_account_id, 0)

    def test_account_with_invalid_ed25519_public_key_raise(self):
        invalid_account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOBAD"
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match=f"Invalid Ed25519 Public Key: {invalid_account_id}",
        ):
            Account(invalid_account_id, 0)

    def test_account_with_invalid_muxed_account_raise(self):
        invalid_muxed_account = (
            "MA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOAAAAAAAAEINVALID"
        )
        with pytest.raises(
            MuxedEd25519AccountInvalidError,
            match=f"Invalid Muxed Account: {invalid_muxed_account}",
        ):
            Account(invalid_muxed_account, 0)

    def test_thresholds_without_raw_data(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        with pytest.raises(
            ValueError,
            match='"raw_data" is None, unable to get thresholds from it.',
        ):
            _ = account.thresholds

    def test_load_ed25519_public_key_signers_without_raw_data(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        with pytest.raises(
            ValueError,
            match='"raw_data" is None, unable to get signers from it.',
        ):
            account.load_ed25519_public_key_signers()

    def test_equals(self):
        account1 = Account(
            account="GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH",
            sequence=123123,
        )
        account2 = Account(
            account="GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH",
            sequence=123123,
        )
        account3 = Account(
            account="GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH",
            sequence=0,
        )
        account4 = Account(
            account="GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY",
            sequence=123123,
        )
        assert account1 == account2
        assert account1 != account3
        assert account1 != account4
