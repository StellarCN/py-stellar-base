import pytest

from stellar_sdk import Operation, SetTrustLineFlags, TrustLineFlags

from . import *


class TestSetTrustLineFlags:
    @pytest.mark.parametrize(
        "clear_flags, set_flags, source, xdr",
        [
            pytest.param(
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                None,
                "AAAAAAAAABUAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAIAAAAB",
                id="without_source",
            ),
            pytest.param(
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABUAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAIAAAAB",
                id="with_source_public_key",
            ),
            pytest.param(
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAgAAAAE=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAgAAAAE=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG
                | TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABUAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAYAAAAB",
                id="with_multi_clear_flags",
            ),
            pytest.param(
                TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG
                | TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABUAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAQAAAAD",
                id="with_multi_set_flags",
            ),
            pytest.param(
                None,
                None,
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAABUAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAAAAAAA",
                id="no_flags",
            ),
        ],
    )
    def test_xdr(self, clear_flags, set_flags, source, xdr):
        op = SetTrustLineFlags(kp2.public_key, asset1, clear_flags, set_flags, source)
        assert op.trustor == kp2.public_key
        assert op.asset == asset1
        assert op.clear_flags == clear_flags
        assert op.set_flags == set_flags
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_trustor_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "trustor" is not a valid ed25519 public key: {key}',
        ):
            SetTrustLineFlags(
                key,
                asset1,
                TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                TrustLineFlags.AUTHORIZED_FLAG,
                kp1.public_key,
            )
