import pytest

from stellar_sdk import MuxedAccount
from stellar_sdk.account import Account
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from stellar_sdk.sep.ed25519_public_key_signer import Ed25519PublicKeySigner


class TestAccount:
    def test_account_with_ed25519_key(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        assert account.account == MuxedAccount(account_id, None)
        assert account.sequence == sequence
        assert account.account.account_id == account_id
        assert account.universal_account_id == account_id
        other_account = Account(account=account_id, sequence=sequence)
        assert account == other_account

        account.increment_sequence_number()
        assert account.sequence == sequence + 1
        assert account != other_account
        assert account != "bad type"

    def test_account_with_muxed_account_key(self):
        account_muxed = (
            "MA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOAAAAAAAAAAE2LEM6"
        )
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        account_muxed_id = 1234
        sequence = 123123
        account = Account(account=account_muxed, sequence=sequence)
        assert account.sequence == sequence
        assert account.account == MuxedAccount(account_id, account_muxed_id)
        assert account.account.account_id == account_id
        assert account.universal_account_id == account_muxed
        other_account = Account(account=account_muxed, sequence=sequence)
        assert account == other_account

        account.increment_sequence_number()
        assert account.sequence == sequence + 1
        assert account != other_account
        assert account != "bad type"

    def test_account_with_muxed_account_instance(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account=account_id, sequence=sequence)
        assert account.sequence == sequence
        assert account.account.account_id == account_id
        other_account = Account(account=account_id, sequence=sequence)
        assert account == other_account

        account.increment_sequence_number()
        assert account.sequence == sequence + 1
        assert account != other_account
        assert account != "bad type"

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

    def test_bad_account_id_raise(self):
        invalid_account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOBAD"
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(invalid_account_id),
        ):
            Account(invalid_account_id, 0)
