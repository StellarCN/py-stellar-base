import os

import pytest

from stellar_sdk import *
from stellar_sdk.exceptions import ValueError
from stellar_sdk.sep.txrep import (
    _decode_asset,
    _get_bool_value,
    _get_bytes_value,
    _get_int_value,
    _get_memo,
    _get_string_value,
    _get_value,
    _remove_comment,
    from_txrep,
    to_txrep,
)
from stellar_sdk.transaction_builder import TransactionBuilder


def get_txrep_file(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "txrep_data", filename)
    with open(file_path, "r") as f:
        content = f.read()
        return content.strip()


class TestTxrep:
    def test_to_txrep(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep.txt")
        assert txrep == to_txrep(from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE))
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_v0(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
            v1=False,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_v0.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_fullline_comment(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        file_txrep = get_txrep_file("test_to_txrep_fullline_comment.txt")
        assert txrep == to_txrep(
            from_txrep(file_txrep, Network.TESTNET_NETWORK_PASSPHRASE)
        )

    def test_to_txrep_no_utf8(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        memo = bytes.fromhex("7ed49fbfab2e545cafdb0cd81b9463e2")
        transaction_builder.add_text_memo(memo)
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_utf8.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_from_xdr(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_no_signer(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_signer.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_no_source(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_source.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_no_timebounds(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_timebounds.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_id_memo(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_id_memo(114514)
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_id_memo.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_none_memo(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_none_memo.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_hash_memo(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_hash_memo(
            "ef14f82df770697f56789b4db4e59d1ece902484739ba167cf99fae319ebcc34"
        )
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_hash_memo.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_return_memo(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_return_hash_memo(
            "ef14f82df770697f56789b4db4e59d1ece902484739ba167cf99fae319ebcc34"
        )
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_return_memo.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_full_tx(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=200,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        ),
        transaction_builder.append_path_payment_strict_receive_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            send_asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            send_max="10",
            dest_asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            dest_amount="5.125",
            path=[
                Asset(
                    "Hello", "GD3RXMK2GHSXXEHPBZY5IL7VW5BXQEDJMCD4KVMXOH2GRFKDGZXR5PFO"
                ),
                Asset.native(),
                Asset(
                    "MOEW", "GBR765FQTCAJLLJGZVYLXCFAOZI6ORTHPDPOOHJOHFRZ5GHNVYGK4IFM"
                ),
            ],
            source=keypair.public_key,
        )
        transaction_builder.append_manage_sell_offer_op(
            selling=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            buying=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="100.123",
            price=Price(n=7, d=1),
            offer_id=12345,
            source=keypair.public_key,
        )
        transaction_builder.append_create_passive_sell_offer_op(
            selling=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            buying=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="100.123",
            price="7.1",
            source=keypair.public_key,
        )
        transaction_builder.append_set_options_op(
            inflation_dest="GCVAZXCGX3HLHZ6P5WKEPE3U2YJMTLMPTZJFGY67MTNPSOA4COKVJ6AF",
            clear_flags=3,
            set_flags=3,
            master_weight=255,
            low_threshold=1,
            med_threshold=2,
            high_threshold=3,
            home_domain="stellar.org",
            signer=Signer.ed25519_public_key(
                "GAO3YIWNOBP4DN3ORDXYXTUMLF5S54OK4PKAFCWE23TTOML4COGQOIYA", 255
            ),
            source=keypair.public_key,
        )
        transaction_builder.append_set_options_op(home_domain="stellarcn.org")
        transaction_builder.append_pre_auth_tx_signer(
            "0ab0c76b1c661db0e829abfdd9e32e6ce3c11f756bdf71aa23846582106c1783", 5
        )
        transaction_builder.append_hashx_signer(
            "0d64fac556c1545616b3c915a4ec215239500bce287007cff038b6020950af46", 10
        )
        transaction_builder.append_change_trust_op(
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            limit="1000",
            source=keypair.public_key,
        )
        transaction_builder.append_allow_trust_op(
            trustor="GDU64QWPRTO3LW5VGZPTLRR6QROFWV36XG5QT4C6FZBPHQBBFYRCWZTZ",
            asset_code="CAT",
            authorize=True,
            source=keypair.public_key,
        )
        transaction_builder.append_account_merge_op(
            destination="GDU64QWPRTO3LW5VGZPTLRR6QROFWV36XG5QT4C6FZBPHQBBFYRCWZTZ",
            source=keypair.public_key,
        )
        transaction_builder.append_manage_data_op(
            "Hello", "Stellar", source=keypair.public_key
        )
        transaction_builder.append_manage_data_op(
            "World", None, source=keypair.public_key
        )
        transaction_builder.append_bump_sequence_op(
            bump_to=46489056724385800, source=keypair.public_key
        )
        transaction_builder.append_manage_buy_offer_op(
            selling=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            buying=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="100.123",
            price="7.1",
            source=keypair.public_key,
        )
        transaction_builder.append_path_payment_strict_send_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            send_asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            send_amount="10",
            dest_asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            dest_min="5.125",
            path=[
                Asset(
                    "Hello", "GD3RXMK2GHSXXEHPBZY5IL7VW5BXQEDJMCD4KVMXOH2GRFKDGZXR5PFO"
                ),
                Asset.native(),
                Asset(
                    "MOEW", "GBR765FQTCAJLLJGZVYLXCFAOZI6ORTHPDPOOHJOHFRZ5GHNVYGK4IFM"
                ),
            ],
            source=keypair.public_key,
        )
        transaction_builder.append_inflation_op()
        claim_predicate = ClaimPredicate.predicate_and(
            left=ClaimPredicate.predicate_and(
                left=ClaimPredicate.predicate_and(
                    left=ClaimPredicate.predicate_before_relative_time(40000),
                    right=ClaimPredicate.predicate_not(
                        ClaimPredicate.predicate_before_relative_time(50000)
                    ),
                ),
                right=ClaimPredicate.predicate_before_relative_time(30000),
            ),
            right=ClaimPredicate.predicate_or(
                left=ClaimPredicate.predicate_not(
                    ClaimPredicate.predicate_before_relative_time(10000)
                ),
                right=ClaimPredicate.predicate_before_absolute_time(20000),
            ),
        )
        transaction_builder.append_create_claimable_balance_op(
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            amount="10000.567",
            claimants=[
                Claimant(
                    "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
                    claim_predicate,
                ),
                Claimant(
                    "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
                    claim_predicate,
                ),
            ],
            source=keypair.public_key,
        )
        transaction_builder.append_claim_claimable_balance_op(
            balance_id="00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
            source=keypair.public_key,
        )
        transaction_builder.append_begin_sponsoring_future_reserves_op(
            sponsored_id=keypair.public_key, source=keypair.public_key
        )
        transaction_builder.append_create_account_op(
            destination="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            starting_balance="10",
            source=keypair.public_key,
        )
        transaction_builder.append_end_sponsoring_future_reserves_op(
            source=keypair.public_key
        )
        transaction_builder.append_revoke_ed25519_public_key_signer_sponsorship_op(
            account_id="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            signer_key="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_hashx_signer_sponsorship_op(
            account_id="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            signer_key="0d64fac556c1545616b3c915a4ec215239500bce287007cff038b6020950af46",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_pre_auth_tx_signer_sponsorship_op(
            account_id="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            signer_key="0ab0c76b1c661db0e829abfdd9e32e6ce3c11f756bdf71aa23846582106c1783",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_ed25519_public_key_signer_sponsorship_op(
            account_id="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            signer_key="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_account_sponsorship_op(
            account_id="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_data_sponsorship_op(
            account_id="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            data_name="hello",
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_offer_sponsorship_op(
            seller_id="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            offer_id=99876,
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_trustline_sponsorship_op(
            account_id="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            source=keypair.public_key,
        )
        transaction_builder.append_revoke_claimable_balance_sponsorship_op(
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
            source=keypair.public_key,
        )
        transaction_builder.append_clawback_op(
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            from_="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="1234.5678",
            source=keypair.public_key,
        )
        transaction_builder.append_clawback_claimable_balance_op(
            balance_id="00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
            source=keypair.public_key,
        )
        transaction_builder.append_set_trust_line_flags_op(
            trustor="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            set_flags=TrustLineFlags.AUTHORIZED_FLAG
            | TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
            clear_flags=TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG,
            source=keypair.public_key,
        )
        transaction_builder.append_set_trust_line_flags_op(
            trustor="GDUF4TESKD5H47VB6KRWIYX7CL4TADDB2QJALCFHPIZLCGFMNTRVX4HM",
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        te.sign_hashx(
            bytes.fromhex(
                "8b73f9e12fcc8cd9580a2a26aec14d6175aa1ff45e76b816618635d03f3256b8"
            )
        )
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_full_tx.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_fee_bump(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=keypair.public_key,
        )
        inner_tx = transaction_builder.build()
        inner_tx.sign(keypair)
        fee_source_keypair = Keypair.from_secret(
            "SASZKBDB6PFHXN6LRH4NQNTRGLGDTI3PSUVIKMZMLTYYBB7NDVMA6DSL"
        )

        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source=fee_source_keypair,
            base_fee=200,
            inner_transaction_envelope=inner_tx,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source_keypair)
        txrep = to_txrep(fee_bump_tx)
        assert txrep == get_txrep_file("test_to_txrep_fee_bump.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == fee_bump_tx.to_xdr()
        )

    def test_muxed_account(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account_muxed = MuxedAccount(keypair.public_key, 1)
        account = Account(account_muxed, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_text_memo("Enjoy this transaction")
        transaction_builder.add_time_bounds(1535756672, 1567292672)
        transaction_builder.append_account_merge_op(
            destination="MCMXCNQPSKNQC4KSKZ6EEC56W525V63SV7BUWKEOKPNHAWBKYLPS2AAAAAAAAAAAAHKEE",
            source=account_muxed,
        )
        transaction_builder.append_payment_op(
            destination="MBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IAAAAAAAAAAAAF7WE",
            asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            amount="40.0004",
            source=account_muxed,
        )
        transaction_builder.append_path_payment_strict_receive_op(
            destination="MBCCOULOS5TNW5HEQLGZMF4HMJXWT47HKA5GOHCHF437SMXX3CWIQAAAAAAAAAAAAGFTY",
            send_asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            send_max="10",
            dest_asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            dest_amount="5.125",
            path=[
                Asset(
                    "Hello", "GD3RXMK2GHSXXEHPBZY5IL7VW5BXQEDJMCD4KVMXOH2GRFKDGZXR5PFO"
                ),
                Asset.native(),
                Asset(
                    "MOEW", "GBR765FQTCAJLLJGZVYLXCFAOZI6ORTHPDPOOHJOHFRZ5GHNVYGK4IFM"
                ),
            ],
            source=account_muxed,
        )
        transaction_builder.append_path_payment_strict_send_op(
            destination="MATDIL6CGXI6HFQ7UPBGIJR5QNMGNPVVTTHIPZWIQ3AFCS2YO3M3CAAAAAAAAAAAAFGHU",
            send_asset=Asset(
                "USD", "GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
            ),
            send_amount="10",
            dest_asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            dest_min="5.125",
            path=[
                Asset(
                    "Hello", "GD3RXMK2GHSXXEHPBZY5IL7VW5BXQEDJMCD4KVMXOH2GRFKDGZXR5PFO"
                ),
                Asset.native(),
                Asset(
                    "MOEW", "GBR765FQTCAJLLJGZVYLXCFAOZI6ORTHPDPOOHJOHFRZ5GHNVYGK4IFM"
                ),
            ],
            source=account_muxed,
        )
        transaction_builder.append_clawback_op(
            asset=Asset(
                "XCN", "GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F"
            ),
            from_="MD6Q33M4R4PLM7TXU75G2UFDP6XBW7UEBSWT6ECDVNGBKIY2Z44HUAAAAAAAAAAAAECFU",
            amount="1234.5678",
            source=account_muxed,
        )
        inner_tx = transaction_builder.build()
        inner_tx.sign(keypair)
        fee_source_keypair = Keypair.from_secret(
            "SASZKBDB6PFHXN6LRH4NQNTRGLGDTI3PSUVIKMZMLTYYBB7NDVMA6DSL"
        )
        fee_source_muxed = MuxedAccount(fee_source_keypair.public_key, 1)

        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source=fee_source_muxed,
            base_fee=200,
            inner_transaction_envelope=inner_tx,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        )
        fee_bump_tx.sign(fee_source_keypair)
        txrep = to_txrep(fee_bump_tx)
        assert txrep == get_txrep_file("test_to_txrep_muxed_account.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == fee_bump_tx.to_xdr()
        )

    def test_get_value_missing_raise(self):
        raw_data_map = {"k": "v"}
        missing_key = "missing_key"
        with pytest.raises(ValueError, match=f"`{missing_key}` is missing from txrep."):
            _get_value(raw_data_map, missing_key)

    def test_get_bytes_value_invalid_bytes_raise(self):
        raw_data_map = {"k": "v"}
        key = "k"
        with pytest.raises(
            ValueError, match=f"Failed to convert `{raw_data_map[key]}` to bytes type."
        ):
            _get_bytes_value(raw_data_map, key)

    def test_get_int_value_raise(self):
        raw_data_map = {"k": "v"}
        key = "k"
        with pytest.raises(
            ValueError, match=f"Failed to convert `{raw_data_map[key]}` to int type."
        ):
            _get_int_value(raw_data_map, key)

    def test_get_bool_value_raise(self):
        raw_data_map = {"k": "v"}
        key = "k"
        with pytest.raises(
            ValueError, match=f"Failed to convert `{raw_data_map[key]}` to bool type."
        ):
            _get_bool_value(raw_data_map, key)

    def test_decode_asset_raise(self):
        with pytest.raises(ValueError, match="Failed to decode asset string."):
            _decode_asset("bad:assert:string")

    def test_get_memo_raise(self):
        prefix = "test."
        memo_type = "INVALID_MEMO"
        raw_data_map = {f"{prefix}memo.type": memo_type}
        with pytest.raises(
            ValueError,
            match=f"`{memo_type}` is not a valid memo type, expected one of "
            f"`MEMO_TEXT`, `MEMO_ID`, `MEMO_HASH`, `MEMO_RETURN`, `MEMO_NONE`.",
        ):
            _get_memo(raw_data_map, prefix)

    @pytest.mark.parametrize(
        "k, v",
        [
            ('"hello world"', "hello world"),
            ("", ""),
            ('""hello world""', '"hello world"'),
        ],
    )
    def test(self, k, v):
        raw_data_map = {"k": k}
        key = "k"
        assert _get_string_value(raw_data_map, key) == v

    @pytest.mark.parametrize(
        "k, v",
        [
            ("", ""),
            ("  ", ""),
            ("123 (comment here)", "123"),
            (
                '"\\"Enjoy this \\"\\" transaction\\n\\""',
                '""Enjoy this "" transaction\n""',
            ),
        ],
    )
    def test_remove_comment(self, k, v):
        assert _remove_comment(k) == v
