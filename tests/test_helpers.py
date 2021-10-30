import pytest

from stellar_sdk import (
    FeeBumpTransactionEnvelope,
    TransactionEnvelope,
    parse_transaction_envelope_from_xdr,
)


class TestHelpers:
    @pytest.mark.parametrize(
        "xdr, te_type",
        [
            (
                pytest.param(
                    "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAAAAAAAvKHnQkAAABAM4dg0J1LEFBmbDESJ5d+60WCuZC8lnA80g45qyEgz2oRBSNw1mOfZETnL/BgrebkG/K03oI2Wqcs9lvDKrDGDE0sOBsAAAAglOgiOlGKwWqMsRCrGVLvFNosELJkZFw4yLPYK9KyAAA=",
                    TransactionEnvelope,
                    id="TransactionEnvelopeV0",
                )
            ),
            (
                pytest.param(
                    "AAAAAgAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAAMgAAAAAAAAAAQAAAAEAAAAAAAAwOQAAAAAAAN3VAAAAAgAAAAAAAABkAAAAAQAAAAAAAAABAAAAANKYxYFXEWWR6TIJ6Vx6W/8SGy4dP2GLaND8yO/l5eRwAAAAAAAAAAJUC+QAAAAAAAAAAAHyh50JAAAAQCXOQnmno3he687bKRtDc6+BXRUf8t+RnTuHy+sKf35UjfFiQbIge+txehmg0N61JsFWfwbL0JtgOjzyeZw5JAs=",
                    TransactionEnvelope,
                    id="TransactionEnvelopeV1",
                )
            ),
            (
                pytest.param(
                    "AAAABQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAGQAAAAAgAAAAAcVPE+R/n1VnbIrAK3tu5yVfTkhkqVz04ShWk2SrF3wAAAAMgAAAAAAAAACAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAAEqBfIAAAAAAAAAAABSrF3wAAAAEAordQh63kT50muRLVYaWW7Pgtt8i1tc4t9Bv9MWFWFN3WfTHSU2Jxv7hedjZEyfBPvaS/XnwvYJFcHgPDd1JkNAAAAAAAAAAHov5sSAAAAQKu/RuArXn/P13IIJ8WlnVDStwOquXM0CsWzA4ooZY6gqJ3k1EfmMVIJ0cir0bMTJD9r+g2IUZCANU7wdC38PA0=",
                    FeeBumpTransactionEnvelope,
                    id="FeeBumpTransactionEnvelope",
                )
            ),
        ],
    )
    def test_parse_transaction_envelope_from_xdr(self, xdr, te_type):
        te = parse_transaction_envelope_from_xdr(xdr, "")
        assert isinstance(te, te_type)
