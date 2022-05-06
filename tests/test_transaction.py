import pytest

from stellar_sdk import (
    Asset,
    Claimant,
    ClaimPredicate,
    CreateClaimableBalance,
    IdMemo,
    Keypair,
    MuxedAccount,
    NoneMemo,
    Preconditions,
)
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
        cond = Preconditions(time_bounds=time_bounds)
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
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
        assert restore_transaction.preconditions == cond
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        tx_object = tx.to_xdr_object()
        xdr = "AAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAA"

        assert tx_object.to_xdr() == xdr

        restore_transaction = Transaction.from_xdr(xdr, True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.preconditions == cond
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx_object = Transaction(
            source, sequence, fee, ops, memo, cond, True
        ).to_xdr_object()
        restore_transaction = Transaction.from_xdr(tx_object.to_xdr(), True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source == MuxedAccount.from_account(source)
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.preconditions == cond
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]

        tx_object = Transaction(
            source, sequence, fee, ops, memo, cond, True
        ).to_xdr_object()
        restore_transaction = Transaction.from_xdr(tx_object.to_xdr(), True)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source == source
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.preconditions == cond
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=False)
        tx_object = tx.to_xdr_object()

        restore_transaction = Transaction.from_xdr_object(tx_object, False)
        assert isinstance(restore_transaction, Transaction)
        assert restore_transaction.source.account_id == source.public_key
        assert restore_transaction.fee == fee
        assert restore_transaction.memo == memo
        assert restore_transaction.preconditions == cond
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=False)
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
        assert restore_transaction.preconditions == cond
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

    def test_get_claimable_balance_id(self):
        predicate = ClaimPredicate.predicate_unconditional()
        claimant = Claimant(
            destination="GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
            predicate=predicate,
        )
        claimants = [claimant]
        op = CreateClaimableBalance(
            asset=Asset.native(),
            amount="100",
            claimants=claimants,
        )
        source = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        sequence = 1235
        fee = 100
        tx = Transaction(source, sequence, fee, [op])
        assert (
            tx.get_claimable_balance_id(0)
            == "00000000536af35c666a28d26775008321655e9eda2039154270484e3f81d72c66d5c26f"
        )

    def test_get_claimable_balance_id_with_muxed_source(self):
        predicate = ClaimPredicate.predicate_unconditional()
        claimant = Claimant(
            destination="GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
            predicate=predicate,
        )
        claimants = [claimant]
        op = CreateClaimableBalance(
            asset=Asset.native(),
            amount="100",
            claimants=claimants,
        )
        source = MuxedAccount(
            "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ", 1234
        )
        sequence = 1235
        fee = 100
        tx = Transaction(source, sequence, fee, [op])
        assert (
            tx.get_claimable_balance_id(0)
            == "00000000536af35c666a28d26775008321655e9eda2039154270484e3f81d72c66d5c26f"
        )

    def test_get_claimable_balance_id_invalid_operation_index_raise(self):
        predicate = ClaimPredicate.predicate_unconditional()
        claimant = Claimant(
            destination="GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
            predicate=predicate,
        )
        claimants = [claimant]
        op = CreateClaimableBalance(
            asset=Asset.native(),
            amount="100",
            claimants=claimants,
        )
        source = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        sequence = 1235
        fee = 100
        tx = Transaction(source, sequence, fee, [op])
        with pytest.raises(
            IndexError,
            match='Invalid operation index, "operation_index" should not be greater than 0',
        ):
            tx.get_claimable_balance_id(1)

    def test_get_claimable_balance_id_invalid_op_type_raise(self):
        op = ManageData("a", "b")
        source = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        sequence = 1235
        fee = 100
        tx = Transaction(source, sequence, fee, [op])
        with pytest.raises(
            TypeError,
            match="Type of the operation must be <class 'stellar_sdk.operation.create_claimable_balance.CreateClaimableBalance'>, got <class 'stellar_sdk.operation.manage_data.ManageData'> instead",
        ):
            tx.get_claimable_balance_id(0)

    def test_convert_empty_preconditions_to_none(self):
        op = ManageData("a", "b")
        source = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        sequence = 1235
        fee = 100
        preconditions = Preconditions()
        tx = Transaction(source, sequence, fee, [op], preconditions=preconditions)
        assert tx.preconditions is None
