from typing import Optional

from .strkey import StrKey, encode_check, VersionByte
from .utils import check_ed25519_public_key
from .xdr import xdr as stellarxdr

__all__ = ["MuxedAccount"]


class MuxedAccount:
    """The :class:`MuxedAccount` object, which represents a multiplexed account on Stellar's network.

    See `SEP-0023 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md>`_ for more
    information.

    :param account_id: account id, for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD`
    :param account_id_id: account multiplexing id, for example: `1234`
    """

    def __init__(self, account_id: str, account_id_id: int = None) -> None:
        check_ed25519_public_key(account_id)
        self.account_id: str = account_id
        self.account_id_id: Optional[int] = account_id_id

    @property
    def account_id_muxed(self) -> Optional[str]:
        """Get the multiplex address starting with `M`, return `None` if `account_id_id` is `None`
        """
        if self.account_id_id is None:
            return None
        muxed_account = stellarxdr.MuxedAccountMed25519(
            id=stellarxdr.Uint64(self.account_id_id),
            ed25519=stellarxdr.Uint256(
                StrKey.decode_ed25519_public_key(self.account_id)
            ),
        )
        muxed_account_raw_xdr = muxed_account.to_raw_xdr()
        return encode_check(VersionByte.MUXED_ACCOUNT, muxed_account_raw_xdr)

    @account_id_muxed.setter
    def account_id_muxed(self, value):
        raise AttributeError(
            "Can't set attribute, use `MuxedAccount.from_account` instead."
        )

    @classmethod
    def from_account(cls, account: str) -> "MuxedAccount":
        """Create a :class:`MuxedAccount` from account id or muxed account id.

        :param account: account id or muxed account id,
            for example: `GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD` or
            `MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY`
        """
        muxed = StrKey.decode_muxed_account(account)
        if muxed.type == stellarxdr.CryptoKeyType.KEY_TYPE_ED25519:
            account_id = StrKey.encode_ed25519_public_key(muxed.ed25519.uint256)
            return cls(account_id=account_id, account_id_id=None)
        if muxed.type == stellarxdr.CryptoKeyType.KEY_TYPE_MUXED_ED25519:
            account_id = StrKey.encode_ed25519_public_key(
                muxed.med25519.ed25519.uint256
            )
            account_id_id = muxed.med25519.id.uint64
            return cls(account_id=account_id, account_id_id=account_id_id)

    def to_xdr_object(self) -> stellarxdr.MuxedAccount:
        """Returns the xdr object for this MuxedAccount object.

        :return: XDR MuxedAccount object
        """
        if self.account_id_id is None:
            return StrKey.decode_muxed_account(self.account_id)
        return StrKey.decode_muxed_account(self.account_id_muxed)

    @classmethod
    def from_xdr_object(
        cls, muxed_account_xdr_object: stellarxdr.MuxedAccount
    ) -> "MuxedAccount":
        """Create a :class:`MuxedAccount` from an XDR Asset object.

        :param muxed_account_xdr_object: The MuxedAccount Price object.
        :return: A new :class:`MuxedAccount` object from the given XDR MuxedAccount object.
        """
        account = StrKey.encode_muxed_account(muxed_account_xdr_object)
        return cls.from_account(account)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.account_id == other.account_id
            and self.account_id_id == other.account_id_id
        )

    def __str__(self):
        return "<MuxedAccount [account_id={account_id}, account_id_id={account_id_id}]>".format(
            account_id=self.account_id, account_id_id=self.account_id_id
        )
