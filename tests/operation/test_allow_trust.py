import pytest

from stellar_sdk import AllowTrust, Operation, TrustLineEntryFlag

from . import *


class TestAllowTrust:
    @pytest.mark.parametrize(
        "asset_code, authorize, source, xdr",
        [
            pytest.param(
                "USD",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                None,
                "AAAAAAAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAE=",
                id="without_source",
            ),
            pytest.param(
                "USD",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAE=",
                id="with_source_public_key",
            ),
            pytest.param(
                "USD",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABwAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAQ==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "USD",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABwAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAQ==",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                "USDT",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEVAAAAAE=",
                id="asset_code_length_4",
            ),
            pytest.param(
                "USDTUSDT",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAACVVNEVFVTRFQAAAAAAAAAAQ==",
                id="asset_code_length_8",
            ),
            pytest.param(
                "USDTUSDTUSDT",
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAACVVNEVFVTRFRVU0RUAAAAAQ==",
                id="asset_code_length_12",
            ),
            pytest.param(
                "USD",
                True,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAE=",
                id="with_bool_flag_true",
            ),
            pytest.param(
                "USD",
                False,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAA=",
                id="with_bool_flag_false",
            ),
            pytest.param(
                "USD",
                TrustLineEntryFlag.UNAUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAA=",
                id="with_entry_flag_UNAUTHORIZED_FLAG",
            ),
            pytest.param(
                "USD",
                TrustLineEntryFlag.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAcAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAAI=",
                id="with_entry_flag_AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG",
            ),
        ],
    )
    def test_xdr(self, asset_code, authorize, source, xdr):
        op = AllowTrust(kp2.public_key, asset_code, authorize, source)
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op
        assert op.asset_code == asset_code
        if isinstance(authorize, bool):
            if authorize:
                assert op.authorize == TrustLineEntryFlag.AUTHORIZED_FLAG
            else:
                assert op.authorize == TrustLineEntryFlag.UNAUTHORIZED_FLAG
        else:
            assert op.authorize == authorize

    def test_invalid_trustor_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "trustor" is not a valid ed25519 public key: {key}',
        ):
            AllowTrust(key, "USD", TrustLineEntryFlag.UNAUTHORIZED_FLAG, kp1.public_key)

    def test_invalid_asset_code_raise(self):
        asset_code = "-123456"
        with pytest.raises(
            ValueError,
            match=r"Asset code is invalid \(maximum alphanumeric, 12 characters at max\).",
        ):
            AllowTrust(
                kp2.public_key,
                asset_code,
                TrustLineEntryFlag.UNAUTHORIZED_FLAG,
                kp1.public_key,
            )
