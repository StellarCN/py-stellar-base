import pytest

from stellar_sdk import Network
from stellar_sdk.asset import Asset
from stellar_sdk.exceptions import AssetCodeInvalidError, AssetIssuerInvalidError


class TestAsset:
    @pytest.mark.parametrize("code", ["XCN", "Banana"])
    def test_non_native_asset_without_issuer_raise(self, code):
        with pytest.raises(
            AssetIssuerInvalidError,
            match="The issuer cannot be `None` except for the native asset.",
        ):
            Asset(code)

    @pytest.mark.parametrize(
        "code",
        [
            "",
            "1234567890123",
            "ab_",
        ],
    )
    def test_invalid_code(self, code):
        with pytest.raises(
            AssetCodeInvalidError,
            match=r"Asset code is invalid \(maximum alphanumeric, 12 characters at max\).",
        ):
            Asset(code, "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ")

    @pytest.mark.parametrize(
        "issuer",
        [
            "",
            "GCEZWKCA5",
            "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS67BAD",
            "MA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOAAAAAAAAAAE2LEM6",
        ],
    )
    def test_invalid_issuer(self, issuer):
        with pytest.raises(
            AssetIssuerInvalidError, match="The issuer should be a correct public key."
        ):
            Asset("XCN", issuer)

    def test_init_native_asset(self):
        asset = Asset("XLM")
        assert asset.code == "XLM"
        assert asset.issuer is None
        assert asset.type == "native"
        assert asset.to_dict() == {"type": "native"}
        assert asset.is_native() is True

    def test_init_native_asset_with_native_function(self):
        asset = Asset.native()
        assert asset.code == "XLM"
        assert asset.issuer is None
        assert asset.type == "native"
        assert asset.to_dict() == {"type": "native"}
        assert asset.is_native() is True

    def test_init_credit_alphanum4_asset(self):
        code = "XCN"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum4"
        asset = Asset(code, issuer)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type
        assert asset.to_dict() == {"type": type, "code": code, "issuer": issuer}
        assert asset.is_native() is False

    def test_init_credit_alphanum12_asset(self):
        code = "Banana"
        issuer = "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        type = "credit_alphanum12"
        asset = Asset(code, issuer)
        assert asset.code == code
        assert asset.issuer == issuer
        assert asset.type == type
        assert asset.to_dict() == {"type": type, "code": code, "issuer": issuer}
        assert asset.is_native() is False

    def test_set_type_raise(self):
        asset = Asset.native()
        with pytest.raises(AttributeError, match="Asset type is immutable."):
            asset.type = "credit_alphanum4"

    def test_equals(self):
        asset1 = Asset(
            "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        )
        asset2 = Asset(
            "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        )
        asset3 = Asset(
            "USD", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        )
        asset4 = Asset(
            "XCN", "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"
        )
        assert asset1 == asset2
        assert asset1 != asset3
        assert asset1 != asset4

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
        xdr_object = asset.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Asset.from_xdr_object(xdr_object) == asset

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
    def test_to_xdr_trust_line_xdr_asset_object(self, asset: Asset, xdr):
        xdr_object = asset.to_trust_line_asset_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Asset.from_xdr_object(xdr_object) == asset

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
    def test_to_xdr_change_trust_xdr_asset_object(self, asset, xdr):
        xdr_object = asset.to_change_trust_asset_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Asset.from_xdr_object(xdr_object) == asset

    @pytest.mark.parametrize(
        "asset, network_passphrase, contract_id",
        [
            pytest.param(
                Asset.native(),
                Network.PUBLIC_NETWORK_PASSPHRASE,
                "CAS3J7GYLGXMF6TDJBBYYSE3HQ6BBSMLNUQ34T6TZMYMW2EVH34XOWMA",
                id="native_public",
            ),
            pytest.param(
                Asset.native(),
                Network.TESTNET_NETWORK_PASSPHRASE,
                "CDLZFC3SYJYDZT7K67VZ75HPJVIEUVNIXF47ZG2FB2RMQQVU2HHGCYSC",
                id="native_testnet",
            ),
            pytest.param(
                Asset(
                    "USDC", "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN"
                ),
                Network.PUBLIC_NETWORK_PASSPHRASE,
                "CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75",
                id="alphanum4_public",
            ),
            pytest.param(
                Asset(
                    "yUSDC", "GDGTVWSM4MGS4T7Z6W4RPWOCHE2I6RDFCIFZGS3DOA63LWQTRNZNTTFF"
                ),
                Network.PUBLIC_NETWORK_PASSPHRASE,
                "CDOFW7HNKLUZRLFZST4EW7V3AV4JI5IHMT6BPXXSY2IEFZ4NE5TWU2P4",
                id="alphanum12_public",
            ),
        ],
    )
    def test_contract_id(self, asset, network_passphrase, contract_id):
        assert asset.contract_id(network_passphrase) == contract_id
