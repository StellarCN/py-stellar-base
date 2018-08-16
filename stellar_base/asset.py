# coding: utf-8

import base64
import re

from .utils import account_xdr_object, encode_check, is_valid_address
from .stellarxdr import Xdr


class Asset(object):
    """The :class:`Asset` object, which represents an asset and its
    corresponding issuer on the Stellar network.

    For more information about the formats used for asset codes and how issuers
    work on Stellar's network, see `Stellar's guide on assets`_.

    :param str code: The asset code, in the formats specified in `Stellar's
        guide on assets`_.
    :param issuer: The strkey encoded issuer of the asset. Note if the
        currency is the native currency (XLM (Lumens)), no issuer is necessary.
    :type issuer: str, None

    .. _Stellar's guide on assets:
        https://www.stellar.org/developers/guides/concepts/assets.html

    """

    _ASSET_CODE_RE = re.compile(r'^[a-zA-Z0-9]{1,12}$')

    def __init__(self, code, issuer=None):
        if not self._ASSET_CODE_RE.match(code):
            raise ValueError("Asset code is invalid (alphanumeric, 12 "
                             "characters max).")

        if issuer is not None and not is_valid_address(issuer):
            raise ValueError('Invalid issuer account: {}'.format(issuer))

        if code.lower() != 'xlm' and issuer is None:
            raise ValueError("Issuer cannot be None")

        self.code = code
        self.issuer = issuer
        self.type = self.guess_asset_type()

    def __eq__(self, other):
        return self.xdr() == other.xdr()

    def guess_asset_type(self):
        if self.code.lower() == 'xlm' and self.issuer is None:
            asset_type = 'native'
        elif len(self.code) > 4:
            asset_type = 'credit_alphanum12'
        else:
            asset_type = 'credit_alphanum4'
        return asset_type

    def to_dict(self):
        """Generate a dict for this object's attributes.

        :return: A dict representing an :class:`Asset`
        """
        rv = {'code': self.code}
        if not self.is_native():
            rv['issuer'] = self.issuer
            rv['type'] = self.type
        else:
            rv['type'] = 'native'
        return rv

    @staticmethod
    def native():
        """Create a :class:`Asset` with the native currency.

        Currently, the native currency is Stellar Lumens (XLM)

        :return: A new :class:`Asset` representing the native currency on the
            Stellar network.
        """
        return Asset("XLM")

    def is_native(self):
        """Return true if the :class:`Asset` is the native asset.

        :return: True if the Asset is native, False otherwise.
        """
        return self.issuer is None

    def to_xdr_object(self):
        """Create an XDR object for this :class:`Asset`.

        :return: An XDR Asset object
        """
        if self.is_native():
            xdr_type = Xdr.const.ASSET_TYPE_NATIVE
            return Xdr.types.Asset(type=xdr_type)
        else:
            x = Xdr.nullclass()
            length = len(self.code)
            pad_length = 4 - length if length <= 4 else 12 - length
            x.assetCode = bytearray(self.code, 'ascii') + b'\x00' * pad_length
            x.issuer = account_xdr_object(self.issuer)
        if length <= 4:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
            return Xdr.types.Asset(type=xdr_type, alphaNum4=x)
        else:
            xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
            return Xdr.types.Asset(type=xdr_type, alphaNum12=x)

    def xdr(self):
        """Create an base64 encoded XDR string for this :class:`Asset`.

        :return str: A base64 encoded XDR object representing this
            :class:`Asset`.

        """
        asset = Xdr.StellarXDRPacker()
        asset.pack_Asset(self.to_xdr_object())
        return base64.b64encode(asset.get_buffer())

    @classmethod
    def from_xdr_object(cls, asset_xdr_object):
        """Create a :class:`Asset` from an XDR Asset object.

        :param asset_xdr_object: The XDR Asset object.

        :return: A new :class:`Asset` object from the given XDR Asset object.
        """
        if asset_xdr_object.type == Xdr.const.ASSET_TYPE_NATIVE:
            return Asset.native()
        elif asset_xdr_object.type == Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4:
            issuer = encode_check(
                'account', asset_xdr_object.alphaNum4.issuer.ed25519).decode()
            code = asset_xdr_object.alphaNum4.assetCode.decode().rstrip('\x00')
        else:
            issuer = encode_check(
                'account',
                asset_xdr_object.alphaNum12.issuer.ed25519).decode()
            code = (
                asset_xdr_object.alphaNum12.assetCode.decode().rstrip('\x00'))
        return cls(code, issuer)

    @classmethod
    def from_xdr(cls, xdr):
        """Create an :class:`Asset` object from its base64 encoded XDR
        representation.

        :param bytes xdr: The base64 encoded XDR Asset object.

        :return: A new :class:`Asset` object from its encoded XDR
            representation.

        """
        xdr_decoded = base64.b64decode(xdr)
        asset = Xdr.StellarXDRUnpacker(xdr_decoded)
        asset_xdr_object = asset.unpack_Asset()
        asset = Asset.from_xdr_object(asset_xdr_object)
        return asset
