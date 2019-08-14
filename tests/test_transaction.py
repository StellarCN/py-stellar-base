import pytest

from stellar_sdk import Keypair, IdMemo, Asset, NoneMemo
from stellar_sdk.operation import Payment, ManageData
from stellar_sdk.exceptions import ValueError
from stellar_sdk.time_bounds import TimeBounds
from stellar_sdk.transaction import Transaction


class TestTransaction:
    def test_to_xdr(self):
        source = Keypair.from_public_key(
            "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx_object = Transaction(
            source, sequence, fee, ops, memo, time_bounds
        ).to_xdr_object()
        assert (
            tx_object.to_xdr()
            == "AAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAA"
        )

        restore_transaction = Transaction.from_xdr_object(tx_object)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence

    def test_none_memo(self):
        source = Keypair.from_public_key(
            "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        fee = 200
        asset = Asset.native()
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx = Transaction(source, sequence, fee, ops)
        assert tx.memo == NoneMemo()

    def test_no_operation_raise(self):
        with pytest.raises(ValueError, match="At least one operation required."):
            source = Keypair.from_public_key(
                "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
            )
            sequence = 1
            memo = IdMemo(100)
            fee = 200
            time_bounds = TimeBounds(12345, 56789)
            ops = []
            Transaction(source, sequence, fee, ops, memo, time_bounds).to_xdr_object()
