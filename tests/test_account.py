import pytest

from stellar_sdk.account import Account
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError


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

    def test_bad_account_id_raise(self):
        invalid_account_id = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOBAD"
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(invalid_account_id),
        ):
            Account(invalid_account_id, 0)
