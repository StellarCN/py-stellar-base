import pytest

from stellar_sdk.sep.toid import TOID

ledger_first = 4294967296  # ledger sequence 1
tx_first = 4096  # tx index 1
op_first = 1  # op index 1


class TestTOID:
    @pytest.mark.parametrize(
        "id, expected",
        [
            # accommodates 12-bits of precision for the operation field
            (TOID(0, 0, 1), 1),
            (TOID(0, 0, 4095), 4095),
            # accommodates 20-bits of precision for the transaction field
            (TOID(0, 1, 0), 4096),
            (TOID(0, 1048575, 0), 4294963200),
            # accommodates 32-bits of precision for the ledger field
            (TOID(1, 0, 0), 4294967296),
            (TOID(2**31 - 1, 0, 0), 9223372032559808512),
            # works as expected
            (TOID(1, 1, 1), ledger_first + tx_first + op_first),
            (TOID(1, 1, 0), ledger_first + tx_first),
            (TOID(1, 0, 1), ledger_first + op_first),
            (TOID(1, 0, 0), ledger_first),
            (TOID(0, 1, 0), tx_first),
            (TOID(0, 0, 1), op_first),
            (TOID(0, 0, 0), 0),
            (TOID(2**31 - 1, 2**20 - 1, 2**12 - 1), 2**63 - 1),
        ],
    )
    def test_to_int64_and_from_int64(self, id, expected):
        assert id.to_int64() == expected
        assert TOID.from_int64(expected) == id

    @pytest.mark.parametrize(
        "ledger_sequence, transaction_order, operation_order",
        [
            (2**31, 0, 0),
            (0, 0, 4096),
            (0, 1048576, 0),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
        ],
    )
    def test_init_raise(self, ledger_sequence, transaction_order, operation_order):
        with pytest.raises(ValueError):
            TOID(ledger_sequence, transaction_order, operation_order)

    @pytest.mark.parametrize("value", [2**63, -1])
    def test_from_int64_raise(self, value):
        with pytest.raises(ValueError):
            TOID.from_int64(value)

    @pytest.mark.parametrize(
        "start, end, start_ledger, end_ledger",
        [
            (1, 1, 0, 2),
            (1, 2, 0, 3),
            (2, 2, 2, 3),
            (2, 3, 2, 4),
        ],
    )
    def test_ledger_range_inclusive(self, start, end, start_ledger, end_ledger):
        toid_from, toid_to = TOID.ledger_range_inclusive(start, end)
        id = TOID.from_int64(toid_from)
        assert id.ledger_sequence == start_ledger
        assert id.transaction_order == 0
        assert id.operation_order == 0

        id = TOID.from_int64(toid_to)
        assert id.ledger_sequence == end_ledger
        assert id.transaction_order == 0
        assert id.operation_order == 0

    def test_ledger_range_inclusive_raises(self):
        with pytest.raises(ValueError):
            TOID.ledger_range_inclusive(2, 1)

    @pytest.mark.parametrize(
        "ledger_seq, toid",
        [
            (1, TOID(0, 0, 0)),
            (2**31 - 1, TOID(0, 0, 0)),
        ],
    )
    def test_after_ledger(self, ledger_seq, toid):
        assert TOID.after_ledger(ledger_seq) == TOID(ledger_seq, 2**20 - 1, 2**12 - 1)

    def test_increment_operation_order(self):
        toid = TOID(0, 0, 1)
        toid.increment_operation_order()
        assert toid == TOID(0, 0, 2)
        toid.increment_operation_order()
        assert toid == TOID(0, 0, 3)

        toid = TOID(0, 0, 2**12 - 1)
        toid.increment_operation_order()
        assert toid == TOID(1, 0, 0)
        toid.increment_operation_order()
        assert toid == TOID(1, 0, 1)
