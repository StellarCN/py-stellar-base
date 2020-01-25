import pytest

from stellar_sdk.account import Account
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from stellar_sdk.sep.ed25519_public_key_signer import Ed25519PublicKeySigner


class TestAccount:
    def test_account(self):
        account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        sequence = 123123
        account = Account(account_id=account_id, sequence=sequence)
        assert account.sequence == sequence
        assert account.account_id == account_id
        other_account = Account(account_id=account_id, sequence=sequence)
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
        account = Account(account_id=account_id, sequence=sequence)
        account._signers = signers
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
