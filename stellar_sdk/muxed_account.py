from typing import Optional

from . import xdr as stellar_xdr
from .keypair import Keypair
from .strkey import StrKey

__all__ = ["MuxedAccount"]


class MuxedAccount:
    """The :class:`MuxedAccount` object, which represents a multiplexed account on Stellar's network.

    An example::

        from stellar_sdk import MuxedAccount

        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        account_muxed_id = 1234
        account_muxed = "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"

        # generate account_muxed
        muxed = MuxedAccount(account=account_id, account_muxed_id=1234)  # account_muxed_id is optional.
        print(f"account_muxed: {muxed.account_muxed}")  # `account_muxed` returns ``None`` if `account_muxed_id` is ``None``.

        # parse account_muxed
        muxed = MuxedAccount.from_account(account_muxed)
        print(f"account_id: {muxed.account_id}\\n"
              f"account_muxed_id: {muxed.account_muxed_id}")


    See `SEP-0023 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md>`_ for more
    information.

    :param account_id: ed25519 account id, for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``.
        It should be a string starting with ``G``. If you want to build a MuxedAccount
        object using an address starting with ``M``, please use :func:`stellar_sdk.MuxedAccount.from_account`.
    :param account_muxed_id: account multiplexing id (ex. ``1234``)
    """

    def __init__(self, account_id: str, account_muxed_id: Optional[int] = None) -> None:
        Keypair.from_public_key(account_id)
        self.account_id: str = account_id
        self.account_muxed_id: Optional[int] = account_muxed_id

    @property
    def account_muxed(self) -> Optional[str]:
        """Get the multiplex address starting with ``M``, return ``None`` if `account_id_id` is ``None``."""

        if self.account_muxed_id is None:
            return None

        muxed_xdr = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_MUXED_ED25519,
            med25519=stellar_xdr.MuxedAccountMed25519(
                id=stellar_xdr.Uint64(self.account_muxed_id),
                ed25519=stellar_xdr.Uint256(
                    StrKey.decode_ed25519_public_key(self.account_id)
                ),
            ),
        )
        return StrKey.encode_muxed_account(muxed_xdr)

    @account_muxed.setter
    def account_muxed(self, value):
        raise AttributeError(
            "Can't set attribute, use `MuxedAccount.from_account` instead."
        )

    @property
    def universal_account_id(self) -> str:
        """Get the universal account id,
        if `account_muxed_id` is ``None``, it will return ed25519
        public key (ex. ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``),
        otherwise it will return muxed
        account (ex. ``"MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"``)
        """
        if self.account_muxed_id is None:
            return self.account_id
        assert self.account_muxed is not None
        return self.account_muxed

    @classmethod
    def from_account(cls, account: str) -> "MuxedAccount":
        """Create a :class:`MuxedAccount` object from account id or muxed account id.

        :param account: account id
            or muxed account id (ex. ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
            or ``"MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"``)
        """
        data_length = len(account)
        if data_length == 56:
            return cls(account_id=account, account_muxed_id=None)
        elif data_length == 69:
            muxed_xdr = StrKey.decode_muxed_account(account)
            assert muxed_xdr.med25519 is not None
            assert muxed_xdr.med25519.ed25519 is not None
            return cls(
                account_id=StrKey.encode_ed25519_public_key(
                    muxed_xdr.med25519.ed25519.uint256
                ),
                account_muxed_id=muxed_xdr.med25519.id.uint64,
            )
        else:
            raise ValueError(f"This is not a valid account: {account}")

    def to_xdr_object(self) -> stellar_xdr.MuxedAccount:
        """Returns the xdr object for this MuxedAccount object.

        :return: XDR MuxedAccount object
        """
        if self.account_muxed_id is None:
            return StrKey.decode_muxed_account(self.account_id)
        assert self.account_muxed is not None
        return StrKey.decode_muxed_account(self.account_muxed)

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.MuxedAccount) -> "MuxedAccount":
        """Create a :class:`MuxedAccount` object from an XDR Asset object.

        :param xdr_object: The MuxedAccount object.
        :return: A new :class:`MuxedAccount` object from the given XDR MuxedAccount object.
        """
        if xdr_object.type == stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519:
            assert xdr_object.ed25519 is not None
            account_id = StrKey.encode_ed25519_public_key(xdr_object.ed25519.uint256)
            return cls(account_id=account_id, account_muxed_id=None)
        assert xdr_object.med25519 is not None
        account_id_id = xdr_object.med25519.id.uint64
        assert xdr_object.med25519 is not None
        account_id = StrKey.encode_ed25519_public_key(
            xdr_object.med25519.ed25519.uint256
        )
        return cls(account_id=account_id, account_muxed_id=account_id_id)

    def __hash__(self):
        return hash((self.account_id, self.account_muxed_id))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.account_id == other.account_id
            and self.account_muxed_id == other.account_muxed_id
        )

    def __repr__(self):
        return "<MuxedAccount [account_id={account_id}, account_muxed_id={account_muxed_id}]>".format(
            account_id=self.account_id, account_muxed_id=self.account_muxed_id
        )
