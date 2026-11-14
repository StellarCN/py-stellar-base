import re

from . import xdr as stellar_xdr
from .exceptions import AssetCodeInvalidError, AssetIssuerInvalidError
from .keypair import Keypair
from .network import Network
from .strkey import Contract, Ed25519PublicKey
from .utils import sha256

__all__ = ["Asset"]


class Asset:
    """The :class:`Asset` object, which represents an asset and its
    corresponding issuer on the Stellar network.

    The following example shows how to create an Asset object::

        from stellar_sdk import Asset

        native_asset = Asset.native()  # You can also create a native asset through Asset("XLM").
        credit_alphanum4_asset = Asset("USD", "GBSKJPM2FM6O2C6GVZNAUAMGXZ6I4QIUPMNWVDN2NZULPWWTV3GI2SOX")
        credit_alphanum12_asset = Asset("BANANA", "GA6VT2PDD73TNNRYLPJPJYAAI7EGKBATZ7V562S7XY7TJD4GNOXRG6OS")
        print(f"Asset type: {credit_alphanum4_asset.type}\n"
              f"Asset code: {credit_alphanum4_asset.code}\n"
              f"Asset issuer: {credit_alphanum4_asset.issuer}\n"
              f"Is native asset: {credit_alphanum4_asset.is_native()}")

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
        https://developers.stellar.org/docs/learn/fundamentals/stellar-data-structures/assets
    """

    def __init__(self, code: str, issuer: str | None = None) -> None:
        Asset.check_if_asset_code_is_valid(code)

        if code != "XLM" and issuer is None:
            raise AssetIssuerInvalidError(
                "The issuer cannot be `None` except for the native asset."
            )

        if issuer is not None and not Ed25519PublicKey.is_valid(issuer):
            raise AssetIssuerInvalidError("The issuer should be a correct public key.")

        self.code: str = code
        self.issuer: str | None = issuer
        self._type: str = self.guess_asset_type()

    @staticmethod
    def check_if_asset_code_is_valid(code: str) -> None:
        """Check whether the `code` passed in by the user is a valid asset code,
        if not, an exception will be thrown.

        :param code: The asset code.
        :raises: :exc:`AssetCodeInvalidError <stellar_sdk.exceptions.AssetCodeInvalidError>`: if ``code`` is invalid.
        """
        asset_code_re = re.compile(r"^[a-zA-Z0-9]{1,12}$")
        if not asset_code_re.match(code):
            raise AssetCodeInvalidError(
                "Asset code is invalid (maximum alphanumeric, 12 characters at max)."
            )

    @property
    def type(self) -> str:
        """Return the type of the asset, can be one of
        following types: `native`, `credit_alphanum4` or `credit_alphanum12`

        :return: The type of the asset.
        """
        return self._type

    @type.setter
    def type(self, v) -> None:
        raise AttributeError("Asset type is immutable.")

    def contract_id(self, network_passphrase: str) -> str:
        """Return the contract Id for the asset contract.

        :param network_passphrase: The network where the asset is located.
        :return: The contract Id for the asset contract.
        """
        network_id_hash = stellar_xdr.Hash(Network(network_passphrase).network_id())
        preimage = stellar_xdr.HashIDPreimage.ContractID(
            stellar_xdr.HashIDPreimageContractID(
                network_id=network_id_hash,
                contract_id_preimage=stellar_xdr.ContractIDPreimage.Asset(
                    self.to_xdr_object()
                ),
            )
        )
        contract_id = sha256(preimage.to_xdr_bytes())
        return str(Contract(contract_id))

    def guess_asset_type(self) -> str:
        """Return the type of the asset, Can be one of
        following types: ``native``, ``credit_alphanum4`` or ``credit_alphanum12``.

        :return: The type of the asset.
        """
        if self.code == "XLM" and self.issuer is None:
            asset_type = "native"
        elif len(self.code) > 4:
            asset_type = "credit_alphanum12"
        else:
            asset_type = "credit_alphanum4"
        return asset_type

    def to_dict(self) -> dict[str, str | None]:
        """Generate a dict for this object's attributes.

        :return: A dict representing an :class:`Asset`
        """
        rv: dict[str, str | None] = {"type": self.type}
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
        """Return ``Ture`` if the :class:`Asset` object is the native asset.

        :return: ``True`` if the asset object is native, ``False`` otherwise.
        """
        return self.issuer is None

    def to_xdr_object(self) -> stellar_xdr.Asset.Any:
        """Returns the xdr object for this asset.

        :return: XDR Asset object
        """
        alpha_num = self._to_xdr_alpha_num()
        if alpha_num is None:
            return stellar_xdr.Asset.Native()
        if isinstance(alpha_num, stellar_xdr.AlphaNum4):
            return stellar_xdr.Asset.CreditAlphaNum4(alpha_num)
        return stellar_xdr.Asset.CreditAlphaNum12(alpha_num)

    def to_change_trust_asset_xdr_object(self) -> stellar_xdr.ChangeTrustAsset.Any:
        """Returns the xdr object for this asset.

        :return: XDR ChangeTrustAsset object
        """
        alpha_num = self._to_xdr_alpha_num()
        if alpha_num is None:
            return stellar_xdr.ChangeTrustAsset.Native()
        if isinstance(alpha_num, stellar_xdr.AlphaNum4):
            return stellar_xdr.ChangeTrustAsset.CreditAlphaNum4(alpha_num)
        return stellar_xdr.ChangeTrustAsset.CreditAlphaNum12(alpha_num)

    def to_trust_line_asset_xdr_object(self) -> stellar_xdr.TrustLineAsset.Any:
        """Returns the xdr object for this asset.

        :return: XDR TrustLineAsset object
        """
        alpha_num = self._to_xdr_alpha_num()
        if alpha_num is None:
            return stellar_xdr.TrustLineAsset.Native()
        if isinstance(alpha_num, stellar_xdr.AlphaNum4):
            return stellar_xdr.TrustLineAsset.CreditAlphaNum4(alpha_num)
        return stellar_xdr.TrustLineAsset.CreditAlphaNum12(alpha_num)

    def _to_xdr_alpha_num(
        self,
    ) -> stellar_xdr.AlphaNum4 | stellar_xdr.AlphaNum12 | None:
        """Returns the code and issuer of a non-native asset, or ``None`` for the native one."""
        if self.is_native():
            return None
        assert self.issuer is not None
        issuer = Keypair.from_public_key(self.issuer).xdr_account_id()
        code = self.code.encode("ascii")
        if len(code) <= 4:
            return stellar_xdr.AlphaNum4(code.ljust(4, b"\x00"), issuer)
        return stellar_xdr.AlphaNum12(code.ljust(12, b"\x00"), issuer)

    @classmethod
    def from_xdr_object(
        cls,
        xdr_object: (
            stellar_xdr.Asset.Any
            | stellar_xdr.ChangeTrustAsset.Any
            | stellar_xdr.TrustLineAsset.Any
        ),
    ) -> "Asset":
        """Create a :class:`Asset` from an XDR Asset/ChangeTrustAsset/TrustLineAsset object.

        Please note that this function only supports processing the following types of assets:

        - ASSET_TYPE_NATIVE
        - ASSET_TYPE_CREDIT_ALPHANUM4
        - ASSET_TYPE_CREDIT_ALPHANUM12

        :param xdr_object: The XDR Asset/ChangeTrustAsset/TrustLineAsset object.
        :return: A new :class:`Asset` object from the given XDR object.
        """
        alpha_num: stellar_xdr.AlphaNum4 | stellar_xdr.AlphaNum12
        match xdr_object:
            case (
                stellar_xdr.Asset.Native()
                | stellar_xdr.ChangeTrustAsset.Native()
                | stellar_xdr.TrustLineAsset.Native()
            ):
                return Asset.native()
            case (
                stellar_xdr.Asset.CreditAlphaNum4(alpha_num)
                | stellar_xdr.ChangeTrustAsset.CreditAlphaNum4(alpha_num)
                | stellar_xdr.TrustLineAsset.CreditAlphaNum4(alpha_num)
                | stellar_xdr.Asset.CreditAlphaNum12(alpha_num)
                | stellar_xdr.ChangeTrustAsset.CreditAlphaNum12(alpha_num)
                | stellar_xdr.TrustLineAsset.CreditAlphaNum12(alpha_num)
            ):
                pass
            case _:
                raise ValueError(f"Invalid asset type: {xdr_object.type}")
        issuer = str(Ed25519PublicKey(alpha_num.issuer.ed25519))
        code = alpha_num.asset_code.decode().rstrip("\x00")
        return cls(code, issuer)

    def __hash__(self) -> int:
        return hash((self.type, self.code, self.issuer))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.issuer == other.issuer

    def __repr__(self):
        return f"<Asset [code={self.code}, issuer={self.issuer}, type={self.type}]>"
