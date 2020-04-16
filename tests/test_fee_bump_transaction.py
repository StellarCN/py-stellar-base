from stellar_sdk import (
    TransactionBuilder,
    Account,
    Network,
    Keypair,
    FeeBumpTransactionEnvelope,
    FeeBumpTransaction,
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
        assert isinstance(restore_te, FeeBumpTransactionEnvelope)
        restore_tx = restore_te.transaction
        assert isinstance(restore_tx, FeeBumpTransaction)
        assert restore_tx.fee_source.public_key == fee_source.public_key
        assert restore_tx.base_fee == base_fee
        assert restore_tx.inner_transaction_envelope.to_xdr() == inner_tx.to_xdr()
