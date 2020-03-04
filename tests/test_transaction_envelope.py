import binascii
import pytest

from stellar_sdk.asset import Asset
from stellar_sdk.exceptions import SignatureExistError
from stellar_sdk.keypair import Keypair
from stellar_sdk.memo import IdMemo
from stellar_sdk.network import Network
from stellar_sdk.operation import Payment, ManageData
from stellar_sdk.time_bounds import TimeBounds
from stellar_sdk.transaction import Transaction
from stellar_sdk.transaction_envelope import TransactionEnvelope


class TestTransactionEnvelope:
    def test_to_xdr(self):
        # GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign(source)
        hashx = bytes.fromhex(
            "94e8223a518ac16a8cb110ab1952ef14da2c10b264645c38c8b3d82bd2b20000"
        )
        te.sign_hashx(hashx)
        te_xdr = "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAAAAAAAvKHnQkAAABAM4dg0J1LEFBmbDESJ5d+60WCuZC8lnA80g45qyEgz2oRBSNw1mOfZETnL/BgrebkG/K03oI2Wqcs9lvDKrDGDE0sOBsAAAAglOgiOlGKwWqMsRCrGVLvFNosELJkZFw4yLPYK9KyAAA="
        assert te.to_xdr() == te_xdr
        restore_te = TransactionEnvelope.from_xdr(
            te_xdr, Network.PUBLIC_NETWORK_PASSPHRASE
        )
        assert restore_te.to_xdr() == te_xdr

    def test_already_signed_raise(self):
        # GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, time_bounds)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        # te.sign(source)
        te.sign("SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH")
        hashx = bytes.fromhex(
            "94e8223a518ac16a8cb110ab1952ef14da2c10b264645c38c8b3d82bd2b20000"
        )
        te.sign_hashx(hashx)
        with pytest.raises(
            SignatureExistError, match="The keypair has already signed."
        ):
            te.sign(source)
        with pytest.raises(
            SignatureExistError, match="The preimage has already signed."
        ):
            te.sign_hashx(hashx)

    def test_equal(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        time_bounds = TimeBounds(12345, 56789)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx1 = Transaction(source, sequence, fee, ops, memo, time_bounds)
        tx2 = Transaction(source, sequence, fee, ops, memo, time_bounds)
        te1 = TransactionEnvelope(tx1, Network.PUBLIC_NETWORK_PASSPHRASE)
        te2 = TransactionEnvelope(tx2, Network.PUBLIC_NETWORK_PASSPHRASE)
        te3 = TransactionEnvelope(tx2, Network.TESTNET_NETWORK_PASSPHRASE)
        assert te1 == te2
        assert te1 != te3
        assert te1 != "BAD TYPE"
