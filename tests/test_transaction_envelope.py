import binascii

import pytest

from stellar_sdk import Preconditions, SignedPayloadSigner, SignerKey
from stellar_sdk.asset import Asset
from stellar_sdk.exceptions import SignatureExistError
from stellar_sdk.keypair import Keypair
from stellar_sdk.memo import IdMemo
from stellar_sdk.network import Network
from stellar_sdk.operation import ManageData, Payment
from stellar_sdk.time_bounds import TimeBounds
from stellar_sdk.transaction import Transaction
from stellar_sdk.transaction_envelope import TransactionEnvelope


class TestTransactionEnvelope:
    def test_to_xdr_v0(self):
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
        cond = Preconditions(time_bounds=time_bounds)

        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=False)
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

    def test_to_xdr_v1(self):
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign(source)
        te_xdr = "AAAAAgAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAAMgAAAAAAAAAAQAAAAEAAAAAAAAwOQAAAAAAAN3VAAAAAgAAAAAAAABkAAAAAQAAAAAAAAABAAAAANKYxYFXEWWR6TIJ6Vx6W/8SGy4dP2GLaND8yO/l5eRwAAAAAAAAAAJUC+QAAAAAAAAAAAHyh50JAAAAQCXOQnmno3he687bKRtDc6+BXRUf8t+RnTuHy+sKf35UjfFiQbIge+txehmg0N61JsFWfwbL0JtgOjzyeZw5JAs="
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
        cond = Preconditions(time_bounds=time_bounds)
        ops = [Payment(destination, asset, amount), ManageData("hello", "world")]
        tx = Transaction(source, sequence, fee, ops, memo, cond)
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

    def test_sign_extra_signers_payload_one_extra_signer(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = Preconditions(
            extra_signers=[
                SignerKey.ed25519_signed_payload(
                    SignedPayloadSigner(signer1.public_key, b"cat!!!")
                )
            ]
        )
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer1)
        assert len(te.signatures) == 1
        assert te.signatures[0] == signer1.sign_payload_decorated(b"cat!!!")

    def test_sign_extra_signers_payload_two_extra_signer(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = Preconditions(
            extra_signers=[
                SignerKey.ed25519_signed_payload(
                    SignedPayloadSigner(signer1.public_key, b"cat!!!")
                ),
                SignerKey.ed25519_signed_payload(
                    SignedPayloadSigner(signer1.public_key, b"cat")
                ),
            ]
        )
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer1)
        assert len(te.signatures) == 2
        assert te.signatures[0] == signer1.sign_payload_decorated(b"cat!!!")
        assert te.signatures[1] == signer1.sign_payload_decorated(b"cat")

    def test_sign_extra_signers_payload_two_extra_signer_not_same_signer(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        signer2 = Keypair.from_secret(
            "SAUQGMBSYKZ73CZCVEOE44Z7FDSZWP4VORDVQMGOTBADVT3K5SQXBFTY"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = Preconditions(
            extra_signers=[
                SignerKey.ed25519_signed_payload(
                    SignedPayloadSigner(signer1.public_key, b"cat!!!")
                ),
                SignerKey.ed25519_signed_payload(
                    SignedPayloadSigner(signer2.public_key, b"cat")
                ),
            ]
        )
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer2)
        assert len(te.signatures) == 1
        assert te.signatures[0] == signer2.sign_payload_decorated(b"cat")
        te.sign_extra_signers_payload(signer1.secret)
        assert len(te.signatures) == 2
        assert te.signatures[1] == signer1.sign_payload_decorated(b"cat!!!")

    def test_sign_extra_signers_payload_no_extra_signer(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = Preconditions(extra_signers=None)
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer1)
        assert len(te.signatures) == 0

    def test_sign_extra_signers_cond_is_none(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = None
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer1)
        assert len(te.signatures) == 0

    def test_sign_extra_signers_payload_is_not_signed_extra_signer(self):
        source = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        signer1 = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        destination = "GDJJRRMBK4IWLEPJGIE6SXD2LP7REGZODU7WDC3I2D6MR37F4XSHBKX2"
        amount = "1000.0"
        sequence = 1
        memo = IdMemo(100)
        fee = 200
        asset = Asset.native()
        cond = Preconditions(
            extra_signers=[SignerKey.ed25519_public_key(signer1.public_key)]
        )
        ops = [Payment(destination, asset, amount)]
        tx = Transaction(source, sequence, fee, ops, memo, cond, v1=True)
        te = TransactionEnvelope(tx, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert binascii.hexlify(te.hash()).decode() == te.hash_hex()
        te.sign_extra_signers_payload(signer1)
        assert len(te.signatures) == 0
