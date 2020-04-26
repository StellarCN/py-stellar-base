import pytest

from stellar_sdk import (
    TransactionBuilder,
    Account,
    Network,
    Keypair,
    FeeBumpTransactionEnvelope,
    FeeBumpTransaction,
)
from stellar_sdk.exceptions import ValueError


class TestFeeBumpTransaction:
    def test_to_xdr(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 200
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source.public_key,
            base_fee,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source)
        xdr = "AAAABQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAGQAAAAAgAAAAAcVPE+R/n1VnbIrAK3tu5yVfTkhkqVz04ShWk2SrF3wAAAAMgAAAAAAAAACAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAAEqBfIAAAAAAAAAAABSrF3wAAAAEAordQh63kT50muRLVYaWW7Pgtt8i1tc4t9Bv9MWFWFN3WfTHSU2Jxv7hedjZEyfBPvaS/XnwvYJFcHgPDd1JkNAAAAAAAAAAHov5sSAAAAQKu/RuArXn/P13IIJ8WlnVDStwOquXM0CsWzA4ooZY6gqJ3k1EfmMVIJ0cir0bMTJD9r+g2IUZCANU7wdC38PA0="

        assert fee_bump_tx.to_xdr() == xdr
        restore_te = FeeBumpTransactionEnvelope.from_xdr(
            xdr, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert (
                restore_te.to_xdr()
                == TransactionBuilder.from_xdr(
            xdr, Network.TESTNET_NETWORK_PASSPHRASE
        ).to_xdr()
        )
        assert isinstance(restore_te, FeeBumpTransactionEnvelope)
        restore_tx = restore_te.transaction
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source == fee_source.public_key
        assert restore_tx.base_fee == base_fee
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_to_xdr_with_muxed_account_fee_source(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account("MAAAAAAAAAAAH2A4KTYT4R7Z6VLHNSFMAK33N3TSKX2OJBSKSXHU4EUFNE3EVMLXYA662", 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 200
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source.public_key,
            base_fee,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source)
        # xdr = "AAAABQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAGQAAAAAgAAAAAcVPE+R/n1VnbIrAK3tu5yVfTkhkqVz04ShWk2SrF3wAAAAMgAAAAAAAAACAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAAEqBfIAAAAAAAAAAABSrF3wAAAAEAordQh63kT50muRLVYaWW7Pgtt8i1tc4t9Bv9MWFWFN3WfTHSU2Jxv7hedjZEyfBPvaS/XnwvYJFcHgPDd1JkNAAAAAAAAAAHov5sSAAAAQKu/RuArXn/P13IIJ8WlnVDStwOquXM0CsWzA4ooZY6gqJ3k1EfmMVIJ0cir0bMTJD9r+g2IUZCANU7wdC38PA0="
        # assert fee_bump_tx.to_xdr() == xdr
        restore_te = FeeBumpTransactionEnvelope.from_xdr(
            fee_bump_tx.to_xdr(), Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert (
                restore_te.to_xdr()
                == TransactionBuilder.from_xdr(
            fee_bump_tx.to_xdr(), Network.TESTNET_NETWORK_PASSPHRASE
        ).to_xdr()
        )
        assert isinstance(restore_te, FeeBumpTransactionEnvelope)
        restore_tx = restore_te.transaction
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source == fee_source.public_key
        assert restore_tx.base_fee == base_fee
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_to_xdr_with_inner_muxed_account_source(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 200
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            "MAAAAAAAAAAAH2HAJCI3MGHFBTF7D7MUPSRWDE5QZLWLFND7GLJQLGVBZZ66RP43CKRMY",
            base_fee,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source)
        # xdr = "AAAABQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAGQAAAAAgAAAAAcVPE+R/n1VnbIrAK3tu5yVfTkhkqVz04ShWk2SrF3wAAAAMgAAAAAAAAACAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAAEqBfIAAAAAAAAAAABSrF3wAAAAEAordQh63kT50muRLVYaWW7Pgtt8i1tc4t9Bv9MWFWFN3WfTHSU2Jxv7hedjZEyfBPvaS/XnwvYJFcHgPDd1JkNAAAAAAAAAAHov5sSAAAAQKu/RuArXn/P13IIJ8WlnVDStwOquXM0CsWzA4ooZY6gqJ3k1EfmMVIJ0cir0bMTJD9r+g2IUZCANU7wdC38PA0="

        # assert fee_bump_tx.to_xdr() == xdr
        restore_te = FeeBumpTransactionEnvelope.from_xdr(
            fee_bump_tx.to_xdr(), Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert (
                restore_te.to_xdr()
                == TransactionBuilder.from_xdr(
            fee_bump_tx.to_xdr(), Network.TESTNET_NETWORK_PASSPHRASE
        ).to_xdr()
        )
        assert isinstance(restore_te, FeeBumpTransactionEnvelope)
        restore_tx = restore_te.transaction
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source == "MAAAAAAAAAAAH2HAJCI3MGHFBTF7D7MUPSRWDE5QZLWLFND7GLJQLGVBZZ66RP43CKRMY"
        assert restore_tx.base_fee == base_fee
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_tx_not_v1(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=False
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 200
        with pytest.raises(
                ValueError,
                match="Invalid `inner_transaction`, it should be TransactionV1.",
        ):
            TransactionBuilder.build_fee_bump_transaction(
                fee_source.public_key,
                base_fee,
                inner_tx,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    def test_tx_fee_less_than_inner_tx_fee(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 150
        with pytest.raises(
                ValueError, match="Invalid `base_fee`, it should be at least 200 stroops.",
        ):
            TransactionBuilder.build_fee_bump_transaction(
                fee_source.public_key,
                base_fee,
                inner_tx,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    def test_tx_fee_less_than_base_fee(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(inner_keypair.public_key, 7)
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 50, v1=True
            )
                .append_payment_op(destination=destination, amount=amount, asset_code="XLM")
                .add_time_bounds(0, 0)
                .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 60
        with pytest.raises(
                ValueError, match="Invalid `base_fee`, it should be at least 100 stroops.",
        ):
            TransactionBuilder.build_fee_bump_transaction(
                fee_source.public_key,
                base_fee,
                inner_tx,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )
