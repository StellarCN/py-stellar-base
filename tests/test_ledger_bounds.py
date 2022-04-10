import pytest

from stellar_sdk import LedgerBounds


class TestLedgerBounds:
    @pytest.mark.parametrize(
        "min_ledger, max_ledger",
        [
            (1560844454, 1560846000),
            (1560844454, 0),
            (1583633108, 1583633108),
        ],
    )
    def test_to_xdr(self, min_ledger, max_ledger):
        op_xdr_object = LedgerBounds(min_ledger, max_ledger).to_xdr_object()
        assert op_xdr_object.min_ledger.uint32 == min_ledger
        assert op_xdr_object.max_ledger.uint32 == max_ledger
        from_instance = LedgerBounds.from_xdr_object(op_xdr_object)
        assert isinstance(from_instance, LedgerBounds)
        assert from_instance.max_ledger == max_ledger
        assert from_instance.min_ledger == min_ledger

    @pytest.mark.parametrize(
        "min_ledger, max_ledger, message",
        [
            (-1, 1560844454, "min_ledger cannot be negative."),
            (1560844454, -1, "max_ledger cannot be negative."),
            (
                1560844455,
                156084454,
                "min_ledger cannot be greater than max_ledger.",
            ),
        ],
    )
    def test_to_xdr_with_invalid_ledger_raise(self, min_ledger, max_ledger, message):
        with pytest.raises(ValueError, match=message):
            LedgerBounds(min_ledger, max_ledger)

    def test_equals(self):
        assert LedgerBounds(1, 2) == LedgerBounds(1, 2)
        assert LedgerBounds(1, 2) != LedgerBounds(1, 0)
        assert LedgerBounds(1, 2) != LedgerBounds(0, 2)
