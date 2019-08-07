import pytest

from stellar_sdk.xdr import Xdr
from stellar_sdk.asset import Asset
from stellar_sdk.exceptions import AssetIssuerInvalidError, AssetCodeInvalidError
from stellar_sdk.keypair import Keypair


class TestAsset:
    @pytest.mark.parametrize("code", ["XCN", "Banana"])
    def test_non_native_asset_without_issuer_raise(self, code):
        with pytest.raises(
            AssetIssuerInvalidError,
            match="The issuer cannot be `None` except for the native asset.",
        ):
            Asset(code)

    @pytest.mark.parametrize("code", ["", "1234567890123", "ab_"])
    def test_invalid_code(self, code):
        with pytest.raises(
            AssetCodeInvalidError,
            match=r"Asset code is invalid \(maximum alphanumeric, 12 characters at max\).",
        ):
            Asset(code, "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ")

    @pytest.mark.parametrize(
        "issuer",
        ["", "GCEZWKCA5", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS67BAD"],
    )
    def test_invalid_issuer(self, issuer):
        with pytest.raises(
            AssetIssuerInvalidError, match="The issuer should be a correct public key."
        ):
            Asset("XCN", issuer)

    def test_native_asset(self):
        asset_1 = Asset("XLM")
        asset_2 = Asset.native()
        assert asset_1 == asset_2
        assert asset_1.code == "XLM"
        assert asset_1.issuer is None
        assert asset_1.type == "native"
        assert asset_1.to_dict() == {"type": "native"}

    def test_credit_alphanum4_asset(self):
        code = "XCN"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum4"
        asset = Asset(code, issuer)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type
        assert asset.to_dict() == {"type": type, "code": code, "issuer": issuer}

    def test_credit_alphanum12_asset(self):
        code = "Banana"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum12"
        asset = Asset(code, issuer)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type
        assert asset.to_dict() == {"type": type, "code": code, "issuer": issuer}

    def test_set_type_raise(self):
        asset = Asset.native()
        with pytest.raises(AttributeError, match="Asset type is immutable."):
            asset.type = "credit_alphanum4"

    def test_equals(self):
        assert Asset(
            "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        ) == Asset("XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
        assert Asset(
            "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        ) != Asset("USD", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
        assert (
            Asset("XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
            != "BAD TYPE"
        )

    @pytest.mark.parametrize(
        "asset, xdr",
        [
            pytest.param(Asset.native(), "AAAAAA==", id="native"),
            pytest.param(
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "AAAAAVhDTgAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3Wdg=",
                id="alphanum4",
            ),
            pytest.param(
                Asset(
                    "CATCOIN",
                    "GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z",
                ),
                "AAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYw==",
                id="alphanum12",
            ),
        ],
    )
    def test_to_xdr_object(self, asset, xdr):
        assert asset.to_xdr_object().to_xdr() == xdr

    def test_from_xdr_object_native(self):
        xdr_type = Xdr.const.ASSET_TYPE_NATIVE
        xdr = Xdr.types.Asset(type=xdr_type)

        asset = Asset.from_xdr_object(xdr)
        assert asset.is_native()

    def test_from_xdr_object_alphanum4(self):
        code = "XCN"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum4"

        x = Xdr.nullclass()
        x.assetCode = bytearray(code, "ascii") + b"\x00"
        x.issuer = Keypair.from_public_key(issuer).xdr_account_id()
        xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM4
        xdr = Xdr.types.Asset(type=xdr_type, alphaNum4=x)

        asset = Asset.from_xdr_object(xdr)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type

    def test_from_xdr_object_alphanum12(self):
        code = "Banana"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum12"

        x = Xdr.nullclass()
        x.assetCode = bytearray(code, "ascii") + b"\x00" * 6
        x.issuer = Keypair.from_public_key(issuer).xdr_account_id()
        xdr_type = Xdr.const.ASSET_TYPE_CREDIT_ALPHANUM12
        xdr = Xdr.types.Asset(type=xdr_type, alphaNum12=x)

        asset = Asset.from_xdr_object(xdr)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type
