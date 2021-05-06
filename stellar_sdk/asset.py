import re
from typing import Optional, Dict

from . import xdr as stellar_xdr
from .exceptions import AssetCodeInvalidError, AssetIssuerInvalidError, AttributeError
from .keypair import Keypair
from .strkey import StrKey

__all__ = ["Asset"]


class Asset:
    """The :class:`Asset` object, which represents an asset and its
    corresponding issuer on the Stellar network.

    For more information about the formats used for asset codes and how issuers
    work on Stellar's network, see `Stellar's guide on assets`_.

    :param code: The asset code, in the formats specified in `Stellar's
        guide on assets`_.
    :param issuer: The account ID of the issuer. Note if the
        currency is the native currency (XLM (Lumens)), no issuer is necessary.
    :raises:
        | :exc:`AssetCodeInvalidError <stellar_sdk.exceptions.AssetCodeInvalidError>`: if ``code`` is invalid.
        | :exc:`AssetIssuerInvalidError <stellar_sdk.exceptions.AssetIssuerInvalidError>`: if ``issuer`` is not a valid ed25519 public key.

    .. _Stellar's guide on assets:
        https://www.stellar.org/developers/guides/concepts/assets.html
    """

    def __init__(self, code: str, issuer: Optional[str] = None) -> None:
        Asset.check_if_asset_code_is_valid(code)

        if code != "XLM" and issuer is None:
            raise AssetIssuerInvalidError(
                "The issuer cannot be `None` except for the native asset."
            )

        if issuer is not None and not StrKey.is_valid_ed25519_public_key(issuer):
            raise AssetIssuerInvalidError("The issuer should be a correct public key.")

        self.code: str = code
        self.issuer: Optional[str] = issuer
        self._type: str = self.guess_asset_type()

    @staticmethod
    def check_if_asset_code_is_valid(code: str) -> None:
        asset_code_re = re.compile(r"^[a-zA-Z0-9]{1,12}$")
        if not asset_code_re.match(code):
            raise AssetCodeInvalidError(
                "Asset code is invalid (maximum alphanumeric, 12 characters at max)."
            )

    @property
    def type(self) -> str:
        """Return the type of the asset, Can be one of following types: `native`, `credit_alphanum4` or `credit_alphanum12`

        :return: The type of the asset.
        """
        return self._type

    @type.setter
    def type(self, v) -> None:
        raise AttributeError("Asset type is immutable.")

    def guess_asset_type(self) -> str:
        """Return the type of the asset, Can be one of following types: `native`, `credit_alphanum4` or `credit_alphanum12`

        :return: The type of the asset.
        """
        if self.code == "XLM" and self.issuer is None:
            asset_type = "native"
        elif len(self.code) > 4:
            asset_type = "credit_alphanum12"
        else:
            asset_type = "credit_alphanum4"
        return asset_type

    def to_dict(self) -> dict:
        """Generate a dict for this object's attributes.

        :return: A dict representing an :class:`Asset`
        """
        rv: Dict[str, Optional[str]] = {"type": self.type}
        if not self.is_native():
            rv["code"] = self.code
            rv["issuer"] = self.issuer
        return rv

    @classmethod
    def native(cls) -> "Asset":
        """Returns an asset object for the native asset.

        :return: An asset object for the native asset.
        """
        return cls("XLM")

    def is_native(self) -> bool:
        """Return true if the :class:`Asset` is the native asset.

        :return: True if the Asset is native, False otherwise.
        """
        return self.issuer is None

    def to_xdr_object(self) -> stellar_xdr.Asset:
        """Returns the xdr object for this asset.

        :return: XDR Asset object
        """
        if self.is_native():
            asset_type = stellar_xdr.AssetType.ASSET_TYPE_NATIVE
            return stellar_xdr.Asset(type=asset_type)
        else:
            assert self.issuer is not None
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            asset_code = bytearray(self.code, "ascii") + b"\x00" * pad_length
            issuer = Keypair.from_public_key(self.issuer).xdr_account_id()
        if length <= 4:
            xdr_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4
            asset_code4 = stellar_xdr.AssetCode4(asset_code)
            alpha_num4 = stellar_xdr.AssetAlphaNum4(asset_code4, issuer)
            return stellar_xdr.Asset(type=xdr_type, alpha_num4=alpha_num4)
        else:
            xdr_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12
            asset_code12 = stellar_xdr.AssetCode12(asset_code)
            alpha_num12 = stellar_xdr.AssetAlphaNum12(asset_code12, issuer)
            return stellar_xdr.Asset(type=xdr_type, alpha_num12=alpha_num12)

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Asset) -> "Asset":
        """Create a :class:`Asset` from an XDR Asset object.

        :param xdr_object: The XDR Asset object.
        :return: A new :class:`Asset` object from the given XDR Asset object.
        """
        if xdr_object.type == stellar_xdr.AssetType.ASSET_TYPE_NATIVE:
            return Asset.native()
        elif xdr_object.type == stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4:
            assert xdr_object.alpha_num4 is not None
            assert xdr_object.alpha_num4.issuer.account_id.ed25519 is not None
            issuer = StrKey.encode_ed25519_public_key(
                xdr_object.alpha_num4.issuer.account_id.ed25519.uint256
            )
            code = xdr_object.alpha_num4.asset_code.asset_code4.decode().rstrip("\x00")
        else:
            assert xdr_object.alpha_num12 is not None
            assert xdr_object.alpha_num12.issuer.account_id.ed25519 is not None
            issuer = StrKey.encode_ed25519_public_key(
                xdr_object.alpha_num12.issuer.account_id.ed25519.uint256
            )
            code = xdr_object.alpha_num12.asset_code.asset_code12.decode().rstrip(
                "\x00"
            )
        return cls(code, issuer)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.code == other.code and self.issuer == other.issuer

    def __str__(self):
        return f"<Asset [code={self.code}, issuer={self.issuer}, type={self.type}]>"
