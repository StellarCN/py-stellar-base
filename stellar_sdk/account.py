from .strkey import StrKey


class Account:
    def __init__(self, account_id: str, sequence: int) -> None:
        StrKey.decode_ed25519_public_key(account_id)

        self.account_id = account_id
        self.sequence = sequence

    def increment_sequence_number(self) -> None:
        self.sequence += 1

    def __eq__(self, other: 'Account'):
        return self.account_id == other.account_id and self.sequence == other.sequence

    def __str__(self):
        return '<Account [account_id={account_id}, sequence={sequence}]>'.format(account_id=self.account_id,
                                                                                 sequence=self.sequence)
