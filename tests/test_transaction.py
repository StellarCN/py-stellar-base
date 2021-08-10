from stellar_sdk import Asset, IdMemo, Keypair, MuxedAccount, NoneMemo
from stellar_sdk.operation import ManageData, Payment
from stellar_sdk.time_bounds import TimeBounds
from stellar_sdk.transaction import Transaction


class TestTransaction:
    def test_to_xdr_v1(self):
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
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds, True)
        tx_object = tx.to_xdr_object()
        assert (
            tx_object.to_xdr()
            == "AAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAA"
        )

        restore_transaction = Transaction.from_xdr_object(tx_object, v1=True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source.public_key
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence
        assert restore_transaction == tx

    def test_to_xdr_str_source_v1(self):
        source = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds, True)
        tx_object = tx.to_xdr_object()
        xdr = "AAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAA"

        assert tx_object.to_xdr() == xdr

        restore_transaction = Transaction.from_xdr(xdr, True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence
        assert restore_transaction == tx

    def test_to_xdr_str_source_muxed_v1(self):
        source = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        source2 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx = Transaction(source, sequence, fee, ops, memo, time_bounds, True)
        tx_object = tx.to_xdr_object()
        restore_tx = Transaction.from_xdr_object(tx_object, v1=True)
        assert restore_tx.to_xdr_object().to_xdr() == tx_object.to_xdr()
        assert restore_tx.source.account_id == source
        assert restore_tx == tx

    def test_to_xdr_str_muxed_account_str_source_v1(self):
        source = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx_object = Transaction(
            source, sequence, fee, ops, memo, time_bounds, True
        ).to_xdr_object()
        restore_transaction = Transaction.from_xdr(tx_object.to_xdr(), True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source == MuxedAccount.from_account(source)
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence

    def test_to_xdr_str_muxed_account_source_v1(self):
        source = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
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
            source, sequence, fee, ops, memo, time_bounds, True
        ).to_xdr_object()
        restore_transaction = Transaction.from_xdr(tx_object.to_xdr(), True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence

    def test_none_memo_v1(self):
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

    def test_to_xdr_v0(self):
        source = Keypair.from_public_key(
            "GC3GJU6L7V7ZLPLKG3NTMC6GYYKBMNNKCPP36FG3LWEVPOHUPY6QJIGL"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 2
        memo = NoneMemo()
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds, False)
        tx_object = tx.to_xdr_object()

        restore_transaction = Transaction.from_xdr_object(tx_object, False)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source.public_key
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence
        assert restore_transaction == tx

    def test_to_xdr_str_source_v0(self):
        source = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds, False)
        tx_object = tx.to_xdr_object()
        # assert (
        #     tx_object.to_xdr()
        #     == "AAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAA"
        # )

        restore_transaction = Transaction.from_xdr(tx_object.to_xdr(), False)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.time_bounds == time_bounds
        assert restore_transaction.sequence == sequence
        assert restore_transaction == tx

    def test_none_memo_v0(self):
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

    # def test_no_operation_raise(self):
    #     with pytest.raises(ValueError, match="At least one operation required."):
    #         source = Keypair.from_public_key(
    #             "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
    #         )
    #         sequence = 1
    #         memo = IdMemo(100)
    #         fee = 200
    #         time_bounds = TimeBounds(12345, 56789)
    #         ops = []
    #         Transaction(source, sequence, fee, ops, memo, time_bounds).to_xdr_object()
