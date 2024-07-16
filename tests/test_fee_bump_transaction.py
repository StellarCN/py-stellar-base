import pytest

from stellar_sdk import (
    Account,
    Asset,
    FeeBumpTransaction,
    FeeBumpTransactionEnvelope,
    Keypair,
    MuxedAccount,
    Network,
    TransactionBuilder,
)


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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
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
        assert restore_te == fee_bump_tx
        assert restore_te.transaction == fee_bump_tx.transaction
        assert restore_te.transaction == FeeBumpTransaction.from_xdr(
            fee_bump_tx.transaction.to_xdr_object().to_xdr(),
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        restore_tx = restore_te.transaction
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source.account_id == fee_source.public_key
        assert restore_tx.fee == base_fee * (len(inner_tx.transaction.operations) + 1)
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_to_source_muxed_xdr(self):
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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
            .add_time_bounds(0, 0)
            .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        fee_source2 = Keypair.from_secret(
            "SCVFDAOOXWR5TSPZF5U2MIE6V7M4LTOCNCD624Q6AEVBZ2XMH7HOWFZL"
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
        assert restore_te == fee_bump_tx
        assert restore_te.transaction == fee_bump_tx.transaction
        assert restore_te.transaction == FeeBumpTransaction.from_xdr(
            fee_bump_tx.transaction.to_xdr_object().to_xdr(),
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        assert (
            restore_te.to_xdr()
            == TransactionBuilder.from_xdr(
                xdr, Network.TESTNET_NETWORK_PASSPHRASE
            ).to_xdr()
        )

    def test_to_xdr_with_muxed_account_str_fee_source(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(
            "MAAAAAAAAAAAH2A4KTYT4R7Z6VLHNSFMAK33N3TSKX2OJBSKSXHU4EUFNE3EVMLXYA662", 7
        )
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
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
        assert restore_tx.fee_source == MuxedAccount.from_account(fee_source.public_key)
        assert restore_tx.fee == base_fee * (len(inner_tx.transaction.operations) + 1)
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_to_xdr_with_muxed_account_fee_source(self):
        inner_keypair = Keypair.from_secret(
            "SBKTIFHJSS3JJWEZO2W74DZSA45WZU56LOL3AY7GAW63BXPEJQFYV53E"
        )
        inner_source = Account(
            MuxedAccount(
                "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
            ),
            7,
        )
        destination = "GDQERENWDDSQZS7R7WKHZI3BSOYMV3FSWR7TFUYFTKQ447PIX6NREOJM"
        amount = "2000.0000000"
        inner_tx = (
            TransactionBuilder(
                inner_source, Network.TESTNET_NETWORK_PASSPHRASE, 200, v1=True
            )
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
            .add_time_bounds(0, 0)
            .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source_keypair = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        fee_source = MuxedAccount(fee_source_keypair.public_key, 1234)
        base_fee = 200
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source,
            base_fee,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source_keypair)
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
        assert restore_tx.fee_source == fee_source
        assert restore_tx.fee == base_fee * (len(inner_tx.transaction.operations) + 1)
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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
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
        assert restore_tx.fee_source == MuxedAccount.from_account(
            "MAAAAAAAAAAAH2HAJCI3MGHFBTF7D7MUPSRWDE5QZLWLFND7GLJQLGVBZZ66RP43CKRMY"
        )
        assert restore_tx.fee == base_fee * (len(inner_tx.transaction.operations) + 1)
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()

    def test_tx_v0(self):
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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
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
        assert restore_te == fee_bump_tx
        assert restore_te.transaction == fee_bump_tx.transaction
        assert restore_te.transaction == FeeBumpTransaction.from_xdr(
            fee_bump_tx.transaction.to_xdr_object().to_xdr(),
            Network.TESTNET_NETWORK_PASSPHRASE,
        )
        assert (
            restore_te.to_xdr()
            == TransactionBuilder.from_xdr(
                xdr, Network.TESTNET_NETWORK_PASSPHRASE
            ).to_xdr()
        )
        assert isinstance(restore_te, FeeBumpTransactionEnvelope)
        restore_tx = restore_te.transaction
        assert restore_tx.inner_transaction_envelope.transaction.v1 is True
        assert inner_tx.transaction.v1 is False
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source.account_id == fee_source.public_key
        assert restore_tx.fee == base_fee * (len(inner_tx.transaction.operations) + 1)
        assert restore_tx.inner_transaction_envelope.hash() == inner_tx.hash()

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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
            .add_time_bounds(0, 0)
            .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 150
        with pytest.raises(
            ValueError,
            match="Invalid `base_fee`, it should be at least 200 stroops.",
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
            .append_payment_op(
                destination=destination, amount=amount, asset=Asset.native()
            )
            .add_time_bounds(0, 0)
            .build()
        )
        inner_tx.sign(inner_keypair)
        fee_source = Keypair.from_secret(
            "SB7ZMPZB3YMMK5CUWENXVLZWBK4KYX4YU5JBXQNZSK2DP2Q7V3LVTO5V"
        )
        base_fee = 60
        with pytest.raises(
            ValueError,
            match="Invalid `base_fee`, it should be at least 100 stroops.",
        ):
            TransactionBuilder.build_fee_bump_transaction(
                fee_source.public_key,
                base_fee,
                inner_tx,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    @pytest.mark.parametrize(
        "xdr, is_fee_bump_te",
        [
            (
                "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAyAAAAAAAAAABAAAAAQAAAAAAADA5AAAAAAAA3dUAAAACAAAAAAAAAGQAAAACAAAAAAAAAAEAAAAA0pjFgVcRZZHpMgnpXHpb/xIbLh0/YYto0PzI7+Xl5HAAAAAAAAAAAlQL5AAAAAAAAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAAAAAAAvKHnQkAAABAM4dg0J1LEFBmbDESJ5d+60WCuZC8lnA80g45qyEgz2oRBSNw1mOfZETnL/BgrebkG/K03oI2Wqcs9lvDKrDGDE0sOBsAAAAglOgiOlGKwWqMsRCrGVLvFNosELJkZFw4yLPYK9KyAAA=",
                False,
            ),
            (
                "AAAAAgAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAAMgAAAAAAAAAAQAAAAEAAAAAAAAwOQAAAAAAAN3VAAAAAgAAAAAAAABkAAAAAQAAAAAAAAABAAAAANKYxYFXEWWR6TIJ6Vx6W/8SGy4dP2GLaND8yO/l5eRwAAAAAAAAAAJUC+QAAAAAAAAAAAHyh50JAAAAQCXOQnmno3he687bKRtDc6+BXRUf8t+RnTuHy+sKf35UjfFiQbIge+txehmg0N61JsFWfwbL0JtgOjzyeZw5JAs=",
                False,
            ),
            (
                "AAAABQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAGQAAAAAgAAAAAcVPE+R/n1VnbIrAK3tu5yVfTkhkqVz04ShWk2SrF3wAAAAMgAAAAAAAAACAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAADgSJG2GOUMy/H9lHyjYZOwyuyytH8y0wWaoc596L+bEgAAAAAAAAAEqBfIAAAAAAAAAAABSrF3wAAAAEAordQh63kT50muRLVYaWW7Pgtt8i1tc4t9Bv9MWFWFN3WfTHSU2Jxv7hedjZEyfBPvaS/XnwvYJFcHgPDd1JkNAAAAAAAAAAHov5sSAAAAQKu/RuArXn/P13IIJ8WlnVDStwOquXM0CsWzA4ooZY6gqJ3k1EfmMVIJ0cir0bMTJD9r+g2IUZCANU7wdC38PA0=",
                True,
            ),
            (
                b"\x00\x00\x00\x00\xcb\xd7q\xd6#*\x1ct\xab\x19\xec\x0e\xc73\xc4\xab\xaak\xfe\xb9\x95\x9c\xfa\xb28\xc7\x1d\xcc\xf2\x87\x9d\t\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0009\x00\x00\x00\x00\x00\x00\xdd\xd5\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\xd2\x98\xc5\x81W\x11e\x91\xe92\t\xe9\\z[\xff\x12\x1b.\x1d?a\x8bh\xd0\xfc\xc8\xef\xe5\xe5\xe4p\x00\x00\x00\x00\x00\x00\x00\x02T\x0b\xe4\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x05hello\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x05world\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xf2\x87\x9d\t\x00\x00\x00@3\x87`\xd0\x9dK\x10Pfl1\x12'\x97~\xebE\x82\xb9\x90\xbc\x96p<\xd2\x0e9\xab! \xcfj\x11\x05#p\xd6c\x9fdD\xe7/\xf0`\xad\xe6\xe4\x1b\xf2\xb4\xde\x826Z\xa7,\xf6[\xc3*\xb0\xc6\x0cM,8\x1b\x00\x00\x00 \x94\xe8\":Q\x8a\xc1j\x8c\xb1\x10\xab\x19R\xef\x14\xda,\x10\xb2dd\\8\xc8\xb3\xd8+\xd2\xb2\x00\x00",
                False,
            ),
            (
                b"\x00\x00\x00\x02\x00\x00\x00\x00\xcb\xd7q\xd6#*\x1ct\xab\x19\xec\x0e\xc73\xc4\xab\xaak\xfe\xb9\x95\x9c\xfa\xb28\xc7\x1d\xcc\xf2\x87\x9d\t\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0009\x00\x00\x00\x00\x00\x00\xdd\xd5\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\xd2\x98\xc5\x81W\x11e\x91\xe92\t\xe9\\z[\xff\x12\x1b.\x1d?a\x8bh\xd0\xfc\xc8\xef\xe5\xe5\xe4p\x00\x00\x00\x00\x00\x00\x00\x02T\x0b\xe4\x00\x00\x00\x00\x00\x00\x00\x00\x01\xf2\x87\x9d\t\x00\x00\x00@%\xceBy\xa7\xa3x^\xeb\xce\xdb)\x1bCs\xaf\x81]\x15\x1f\xf2\xdf\x91\x9d;\x87\xcb\xeb\n\x7f~T\x8d\xf1bA\xb2 {\xebqz\x19\xa0\xd0\xde\xb5&\xc1V\x7f\x06\xcb\xd0\x9b`:<\xf2y\x9c9$\x0b",
                False,
            ),
            (
                b"\x00\x00\x00\x05\x00\x00\x00\x00\xe0H\x91\xb6\x18\xe5\x0c\xcb\xf1\xfd\x94|\xa3a\x93\xb0\xca\xec\xb2\xb4\x7f2\xd3\x05\x9a\xa1\xce}\xe8\xbf\x9b\x12\x00\x00\x00\x00\x00\x00\x01\x90\x00\x00\x00\x02\x00\x00\x00\x00\x1cT\xf1>G\xf9\xf5Vv\xc8\xac\x02\xb7\xb6\xeerU\xf4\xe4\x86J\x95\xcfN\x12\x85i6J\xb1w\xc0\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\xe0H\x91\xb6\x18\xe5\x0c\xcb\xf1\xfd\x94|\xa3a\x93\xb0\xca\xec\xb2\xb4\x7f2\xd3\x05\x9a\xa1\xce}\xe8\xbf\x9b\x12\x00\x00\x00\x00\x00\x00\x00\x04\xa8\x17\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x01J\xb1w\xc0\x00\x00\x00@(\xad\xd4!\xeby\x13\xe7I\xaeD\xb5Xie\xbb>\x0bm\xf2-ms\x8b}\x06\xffLXU\x857u\x9fLt\x94\xd8\x9co\xee\x17\x9d\x8d\x912|\x13\xefi/\xd7\x9f\x0b\xd8$W\x07\x80\xf0\xdd\xd4\x99\r\x00\x00\x00\x00\x00\x00\x00\x01\xe8\xbf\x9b\x12\x00\x00\x00@\xab\xbfF\xe0+^\x7f\xcf\xd7r\x08'\xc5\xa5\x9dP\xd2\xb7\x03\xaa\xb9s4\n\xc5\xb3\x03\x8a(e\x8e\xa0\xa8\x9d\xe4\xd4G\xe61R\t\xd1\xc8\xab\xd1\xb3\x13$?k\xfa\r\x88Q\x90\x805N\xf0t-\xfc<\r",
                True,
            ),
        ],
    )
    def test_parse_transaction_envelope_from_xdr(self, xdr, is_fee_bump_te):
        result = FeeBumpTransactionEnvelope.is_fee_bump_transaction_envelope(xdr)
        assert result is is_fee_bump_te

    # https://github.com/StellarCN/py-stellar-base/issues/953
    def test_from_xdr_soroban_tx(self):
        xdr = "AAAABQAAAADmsIA5404L0SCejoRDuqDIG98rMHsELDMTJKJAjYs8+AAAAAACCZiCAAAAAgAAAACR+IxMOJ3vkHZSFqPCpyLqFENdLN/yYjRhojIE5Dz6rAIJcXMDHa56AAAAAQAAAAEAAAAAAAAAAAAAAABmeizDAAAAAAAAAAEAAAAAAAAAGAAAAAAAAAABZHpg2j3gSXQ3PwbyO22dfOAJnhhvMuSRR0rxTI3UXh8AAAAGZGVwbG95AAAAAAACAAAADQAAABQM+a7vJ6ylUis8qPSmfQFRMCEsiwAAAA0AAABBBOWQPnfY1mHIqdwoxJOQb1i4tnFqD3I0tbhPt7/HIIzHUq1IQE4Z+emcO6gdoVslu3Kcqd/F7LP0TraQJKGoUiQAAAAAAAAAAAAAAQAAAAAAAAADAAAABgAAAAFkemDaPeBJdDc/BvI7bZ184AmeGG8y5JFHSvFMjdReHwAAABQAAAABAAAAB09Tl/U18epBIuYjX6O0rlMYzF1tZw4eWExTxGEszzU7AAAAB87BdThZEbuVmpK08n1L5YNRSsOezRbC6ffF06PZOXseAAAAAwAAAAYAAAABZHpg2j3gSXQ3PwbyO22dfOAJnhhvMuSRR0rxTI3UXh8AAAANAAAAFAz5ru8nrKVSKzyo9KZ9AVEwISyLAAAAAQAAAAYAAAABtGdHSrNHQUIXBdV6XwV1HTOwHfPJC4/9iche36y+lA4AAAANAAAAFAz5ru8nrKVSKzyo9KZ9AVEwISyLAAAAAQAAAAYAAAABtGdHSrNHQUIXBdV6XwV1HTOwHfPJC4/9iche36y+lA4AAAAUAAAAAQAztcMAAC0UAAACIAAAAAACCXFzAAAAAeQ8+qwAAABA/dwY67dCI3kuyQpDA3dMUELXMomr/5+OpKV5JQsXSzGBEKpHMYC/zVrEE5SxUsn1ODSCPhID7esWNCjdxPWTBgAAAAAAAAABjYs8+AAAAEDZ7AFWIW5/ZKIBs8CAzbqVcxK5szuxUMeW5pkhSv+mKDxxSEpvYgvn+XaVUXUywnoxS7OB+eIo1IOg43XoLpcH"
        te = FeeBumpTransactionEnvelope.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert isinstance(te, FeeBumpTransactionEnvelope)
        assert te.transaction.fee == 34183298
        assert te.to_xdr() == xdr

    def test_build_fee_bump_transaction_with_soroban_tx(self):
        fee_source = "GDTLBABZ4NHAXUJAT2HIIQ52UDEBXXZLGB5QILBTCMSKEQENRM6PRIZ5"
        xdr = "AAAAAgAAAACR+IxMOJ3vkHZSFqPCpyLqFENdLN/yYjRhojIE5Dz6rAIJcXMDHa56AAAAAQAAAAEAAAAAAAAAAAAAAABmeizDAAAAAAAAAAEAAAAAAAAAGAAAAAAAAAABZHpg2j3gSXQ3PwbyO22dfOAJnhhvMuSRR0rxTI3UXh8AAAAGZGVwbG95AAAAAAACAAAADQAAABQM+a7vJ6ylUis8qPSmfQFRMCEsiwAAAA0AAABBBOWQPnfY1mHIqdwoxJOQb1i4tnFqD3I0tbhPt7/HIIzHUq1IQE4Z+emcO6gdoVslu3Kcqd/F7LP0TraQJKGoUiQAAAAAAAAAAAAAAQAAAAAAAAADAAAABgAAAAFkemDaPeBJdDc/BvI7bZ184AmeGG8y5JFHSvFMjdReHwAAABQAAAABAAAAB09Tl/U18epBIuYjX6O0rlMYzF1tZw4eWExTxGEszzU7AAAAB87BdThZEbuVmpK08n1L5YNRSsOezRbC6ffF06PZOXseAAAAAwAAAAYAAAABZHpg2j3gSXQ3PwbyO22dfOAJnhhvMuSRR0rxTI3UXh8AAAANAAAAFAz5ru8nrKVSKzyo9KZ9AVEwISyLAAAAAQAAAAYAAAABtGdHSrNHQUIXBdV6XwV1HTOwHfPJC4/9iche36y+lA4AAAANAAAAFAz5ru8nrKVSKzyo9KZ9AVEwISyLAAAAAQAAAAYAAAABtGdHSrNHQUIXBdV6XwV1HTOwHfPJC4/9iche36y+lA4AAAAUAAAAAQAztcMAAC0UAAACIAAAAAACCXFzAAAAAeQ8+qwAAABA/dwY67dCI3kuyQpDA3dMUELXMomr/5+OpKV5JQsXSzGBEKpHMYC/zVrEE5SxUsn1ODSCPhID7esWNCjdxPWTBg=="
        inner = TransactionBuilder.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source, 200, inner
        )
        assert fee_bump_tx.transaction.fee == 34173299 + 400
        assert fee_bump_tx.transaction.fee_source == MuxedAccount.from_account(
            fee_source
        )
        assert fee_bump_tx.transaction.inner_transaction_envelope == inner
