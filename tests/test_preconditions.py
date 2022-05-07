import pytest

from stellar_sdk import LedgerBounds, Preconditions, SignerKey, TimeBounds


class TestPreconditions:
    def test_xdr_empty(self):
        cond = Preconditions()
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_time_bounds(self):
        time_bounds = TimeBounds(1649237469, 1649238469)

        cond = Preconditions(time_bounds)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_ledger_bounds(self):
        ledger_bounds = LedgerBounds(40351800, 40352000)
        cond = Preconditions(ledger_bounds=ledger_bounds)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_min_sequence_number(self):
        min_sequence_number = 103420918407103888
        cond = Preconditions(min_sequence_number=min_sequence_number)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_min_sequence_age(self):
        min_sequence_age = 1649239999
        cond = Preconditions(min_sequence_age=min_sequence_age)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_min_sequence_ledger_gap(self):
        min_sequence_ledger_gap = 30
        cond = Preconditions(min_sequence_ledger_gap=min_sequence_ledger_gap)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_extra_signers(self):
        extra_signers = [
            SignerKey.from_encoded_signer_key(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            ),
            SignerKey.from_encoded_signer_key(
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
            ),
        ]
        cond = Preconditions(extra_signers=extra_signers)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_with_one_extra_signers(self):
        extra_signers = [
            SignerKey.from_encoded_signer_key(
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
            ),
            SignerKey.from_encoded_signer_key(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            ),
            SignerKey.from_encoded_signer_key(
                "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
            ),
        ]
        with pytest.raises(
            ValueError, match='"extra_signers" cannot be longer than 2 elements.'
        ):
            Preconditions(extra_signers=extra_signers)

    def test_xdr_with_too_many_extra_signers_raise(self):
        extra_signers = [
            SignerKey.from_encoded_signer_key(
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
            )
        ]
        cond = Preconditions(extra_signers=extra_signers)
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_full(self):
        time_bounds = TimeBounds(1649237469, 1649238469)
        ledger_bounds = LedgerBounds(40351800, 40352000)
        min_sequence_number = 103420918407103888
        min_sequence_age = 1649239999
        min_sequence_ledger_gap = 30
        extra_signers = [
            SignerKey.from_encoded_signer_key(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            ),
            SignerKey.from_encoded_signer_key(
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
            ),
        ]
        cond = Preconditions(
            time_bounds,
            ledger_bounds,
            min_sequence_number,
            min_sequence_age,
            min_sequence_ledger_gap,
            extra_signers,
        )
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)
        assert cond == restore_cond
        assert xdr_object == restore_cond.to_xdr_object()

    def test_xdr_full_with_field_set_to_zero(self):
        time_bounds = TimeBounds(0, 0)
        ledger_bounds = LedgerBounds(0, 0)
        min_sequence_number = 0
        min_sequence_age = 0
        min_sequence_ledger_gap = 0
        extra_signers = []
        cond = Preconditions(
            time_bounds,
            ledger_bounds,
            min_sequence_number,
            min_sequence_age,
            min_sequence_ledger_gap,
            extra_signers,
        )
        xdr_object = cond.to_xdr_object()
        restore_cond = Preconditions.from_xdr_object(xdr_object)

        assert xdr_object == restore_cond.to_xdr_object()
        assert cond.time_bounds == restore_cond.time_bounds
        assert cond.ledger_bounds == restore_cond.ledger_bounds
        assert cond.min_sequence_number == restore_cond.min_sequence_number == 0
        assert cond.min_sequence_age is restore_cond.min_sequence_age == 0
        assert cond.min_sequence_ledger_gap is restore_cond.min_sequence_ledger_gap == 0
        assert cond.extra_signers == restore_cond.extra_signers == []

    @pytest.mark.parametrize(
        "preconditions, is_null",
        [
            (Preconditions(), True),
            (Preconditions(time_bounds=TimeBounds(0, 1)), False),
            (Preconditions(ledger_bounds=LedgerBounds(0, 1)), False),
            (Preconditions(min_sequence_number=0), False),
            (Preconditions(min_sequence_number=1), False),
            (Preconditions(min_sequence_age=0), False),
            (Preconditions(min_sequence_age=1), False),
            (Preconditions(min_sequence_ledger_gap=0), False),
            (Preconditions(min_sequence_ledger_gap=1), False),
            (Preconditions(extra_signers=[]), True),
            (
                Preconditions(
                    extra_signers=[
                        SignerKey.from_encoded_signer_key(
                            "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
                        )
                    ]
                ),
                False,
            ),
        ],
    )
    def test_is_empty_preconditions(self, preconditions: Preconditions, is_null: bool):
        assert preconditions._is_empty_preconditions() is is_null

    @pytest.mark.parametrize(
        "preconditions, is_v2",
        [
            (Preconditions(), False),
            (Preconditions(time_bounds=TimeBounds(0, 1)), False),
            (Preconditions(ledger_bounds=LedgerBounds(0, 1)), True),
            (Preconditions(min_sequence_number=0), True),
            (Preconditions(min_sequence_number=1), True),
            (Preconditions(min_sequence_age=0), True),
            (Preconditions(min_sequence_age=1), True),
            (Preconditions(min_sequence_ledger_gap=0), True),
            (Preconditions(min_sequence_ledger_gap=1), True),
            (Preconditions(extra_signers=[]), False),
            (
                Preconditions(
                    extra_signers=[
                        SignerKey.from_encoded_signer_key(
                            "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
                        )
                    ]
                ),
                True,
            ),
        ],
    )
    def test_is_v2(self, preconditions: Preconditions, is_v2: bool):
        assert preconditions._is_v2() is is_v2
