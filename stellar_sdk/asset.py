import re
from typing import Dict, Optional, Type, Union

from . import xdr as stellar_xdr
from .exceptions import AssetCodeInvalidError, AssetIssuerInvalidError
from .keypair import Keypair
from .network import Network
from .strkey import StrKey
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
        print(f"Asset type: {credit_alphanum4_asset.type}\\n"
              f"Asset code: {credit_alphanum4_asset.code}\\n"
              f"Asset issuer: {credit_alphanum4_asset.issuer}\\n"
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
        https://developers.stellar.org/docs/glossary/assets/
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
        preimage = stellar_xdr.HashIDPreimage(
            stellar_xdr.EnvelopeType.ENVELOPE_TYPE_CONTRACT_ID,
            contract_id=stellar_xdr.HashIDPreimageContractID(
                network_id=network_id_hash,
                contract_id_preimage=stellar_xdr.ContractIDPreimage(
                    stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET,
                    from_asset=self.to_xdr_object(),
                ),
            ),
        )
        contract_id = sha256(preimage.to_xdr_bytes())
        return StrKey.encode_contract(contract_id)

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
        """Return ``Ture`` if the :class:`Asset` object is the native asset.

        :return: ``True`` if the asset object is native, ``False`` otherwise.
        """
        return self.issuer is None

    def to_xdr_object(self) -> stellar_xdr.Asset:
        """Returns the xdr object for this asset.

        :return: XDR Asset object
        """
        asset_xdr = self._to_xdr_object(stellar_xdr.Asset)
        assert isinstance(asset_xdr, stellar_xdr.Asset)
        return asset_xdr

    def to_change_trust_asset_xdr_object(self) -> stellar_xdr.ChangeTrustAsset:
        """Returns the xdr object for this asset.

        :return: XDR ChangeTrustAsset object
        """
        asset_xdr = self._to_xdr_object(stellar_xdr.ChangeTrustAsset)
        assert isinstance(asset_xdr, stellar_xdr.ChangeTrustAsset)
        return asset_xdr

    def to_trust_line_asset_xdr_object(self) -> stellar_xdr.TrustLineAsset:
        """Returns the xdr object for this asset.

        :return: XDR TrustLineAsset object
        """
        asset_xdr = self._to_xdr_object(stellar_xdr.TrustLineAsset)
        assert isinstance(asset_xdr, stellar_xdr.TrustLineAsset)
        return asset_xdr

    def _to_xdr_object(
        self,
        xdr_asset: Union[
            Type[stellar_xdr.Asset],
            Type[stellar_xdr.ChangeTrustAsset],
            Type[stellar_xdr.TrustLineAsset],
        ],
    ) -> Union[
        stellar_xdr.Asset, stellar_xdr.ChangeTrustAsset, stellar_xdr.TrustLineAsset
    ]:
        if self.is_native():
            asset_type = stellar_xdr.AssetType.ASSET_TYPE_NATIVE
            return xdr_asset(type=asset_type)
        else:
            assert self.issuer is not None
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            asset_code = bytearray(self.code, "ascii") + b"\x00" * pad_length
            issuer = Keypair.from_public_key(self.issuer).xdr_account_id()
        if length <= 4:
            xdr_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM4
            asset_code4 = stellar_xdr.AssetCode4(asset_code)
            alpha_num4 = stellar_xdr.AlphaNum4(asset_code4, issuer)
            return xdr_asset(type=xdr_type, alpha_num4=alpha_num4)
        else:
            xdr_type = stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12
            asset_code12 = stellar_xdr.AssetCode12(asset_code)
            alpha_num12 = stellar_xdr.AlphaNum12(asset_code12, issuer)
            return xdr_asset(type=xdr_type, alpha_num12=alpha_num12)

    @classmethod
    def from_xdr_object(
        cls,
        xdr_object: Union[
            stellar_xdr.Asset, stellar_xdr.ChangeTrustAsset, stellar_xdr.TrustLineAsset
        ],
    ) -> "Asset":
        """Create a :class:`Asset` from an XDR Asset/ChangeTrustAsset/TrustLineAsset object.

        Please note that this function only supports processing the following types of assets:

        - ASSET_TYPE_NATIVE
        - ASSET_TYPE_CREDIT_ALPHANUM4
        - ASSET_TYPE_CREDIT_ALPHANUM12

        :param xdr_object: The XDR Asset/ChangeTrustAsset/TrustLineAsset object.
        :return: A new :class:`Asset` object from the given XDR object.
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
        elif xdr_object.type == stellar_xdr.AssetType.ASSET_TYPE_CREDIT_ALPHANUM12:
            assert xdr_object.alpha_num12 is not None
            assert xdr_object.alpha_num12.issuer.account_id.ed25519 is not None
            issuer = StrKey.encode_ed25519_public_key(
                xdr_object.alpha_num12.issuer.account_id.ed25519.uint256
            )
            code = xdr_object.alpha_num12.asset_code.asset_code12.decode().rstrip(
                "\x00"
            )
        else:
            raise ValueError(f"Invalid asset type: {xdr_object.type}")
        return cls(code, issuer)

    def __hash__(self) -> int:
        return hash((self.type, self.code, self.issuer))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.code == other.code and self.issuer == other.issuer

    def __repr__(self):
        return f"<Asset [code={self.code}, issuer={self.issuer}, type={self.type}]>"
