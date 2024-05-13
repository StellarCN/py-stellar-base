class Ed25519PublicKeySigner:
    def __init__(self, account_id: str, weight: int = 0) -> None:
        """The :class:`Signer` object, which represents the signer for the client account.

        :param account_id: Account ID (ex. ``"GBYNR2QJXLBCBTRN44MRORCMI4YO7FZPFBCNOKTOBCAAFC7KC3LNPRYS"``)
        :param weight: The signer's weight.
        """
        self.account_id = account_id
        self.weight = weight

    def __hash__(self):
        return hash((self.account_id, self.weight))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.weight == other.weight

    def __repr__(self):
        return f"<Ed25519PublicKeySigner [account_id={self.account_id}, weight={self.weight}]>"
