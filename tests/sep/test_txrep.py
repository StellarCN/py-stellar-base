import os
import re
import sys
from enum import IntEnum

import pytest

from stellar_sdk import *
from stellar_sdk.operation import ClaimPredicate
from stellar_sdk.operation.allow_trust import TrustLineEntryFlag
from stellar_sdk.sep import txrep
from stellar_sdk.sep._txrep_lines import (
    NATIVE,
    asset_kind,
    parse_integer,
    read_code,
    read_pool_share,
    read_string,
    split_asset,
    write_code,
)
from stellar_sdk.sep._txrep_schema import SCHEMA
from stellar_sdk.sep.exceptions import InvalidTxrepError
from stellar_sdk.sep.txrep import from_txrep, to_txrep
from stellar_sdk.signer_key import SignedPayloadSigner
from stellar_sdk.transaction_builder import TransactionBuilder


def get_txrep_file(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "txrep_data", filename)
    with open(file_path) as f:
        return f.read()


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
        )
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
        transaction_builder.append_liquidity_pool_deposit_op(
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7",
            "10",
            "20",
            "0.45",
            "0.55",
            keypair.public_key,
        )
        transaction_builder.append_liquidity_pool_withdraw_op(
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7",
            "5",
            "10",
            "20",
            keypair.public_key,
        )
        transaction_builder.append_revoke_liquidity_pool_sponsorship_op(
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7",
            keypair.public_key,
        )
        asset_a = Asset(
            "ARST", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO"
        )
        asset_b = Asset(
            "USD", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        )
        fee = LIQUIDITY_POOL_FEE_V18
        line = LiquidityPoolAsset(asset_a, asset_b, fee)
        transaction_builder.append_change_trust_op(line, "10000", keypair.public_key)
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

    def test_to_txrep_cond_precond_timebounds(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_time_bounds(1649237469, 1649238469)
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
        assert txrep == get_txrep_file("test_to_txrep_cond_precond_timebounds.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_ledger_bounds(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.set_ledger_bounds(40351800, 40352000)
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
        assert txrep == get_txrep_file("test_to_txrep_cond_precond_ledger_bounds.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_min_sequence_number(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.set_min_sequence_number(103420918407103888)
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
        assert txrep == get_txrep_file(
            "test_to_txrep_cond_precond_min_sequence_number.txt"
        )
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_min_sequence_age(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.set_min_sequence_age(1649239999)
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
        assert txrep == get_txrep_file(
            "test_to_txrep_cond_precond_min_sequence_age.txt"
        )
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_min_sequence_ledger_gap(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.set_min_sequence_ledger_gap(30)
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
        assert txrep == get_txrep_file(
            "test_to_txrep_cond_precond_min_sequence_ledger_gap.txt"
        )
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_extra_signers(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )
        transaction_builder.add_extra_signer(
            "TCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVOVKE"
        )
        transaction_builder.add_extra_signer(
            "XCC3U63F5OJIG4VS6XCFUJGCQRRMNCVGASDGIZZEPA3AZ242K4JVPRP5"
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
        assert txrep == get_txrep_file("test_to_txrep_cond_precond_extra_signers.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_precond_full(self):
        keypair = Keypair.from_secret(
            "SAHGKA7QJB6SRFDZSPZDEEIOEHUHTQS4XVN4IMR5YCKBPEN5A6YNKKUO"
        )
        account = Account(keypair.public_key, 46489056724385792)
        transaction_builder = TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
        )

        transaction_builder.add_time_bounds(1649237469, 1649238469)
        transaction_builder.set_ledger_bounds(40351800, 40352000)
        transaction_builder.set_min_sequence_number(103420918407103888)
        transaction_builder.set_min_sequence_age(1649239999)
        transaction_builder.set_min_sequence_ledger_gap(30)
        transaction_builder.add_extra_signer(
            "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
        )
        transaction_builder.add_extra_signer(
            "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
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
        assert txrep == get_txrep_file("test_to_txrep_cond_precond_full.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )

    def test_to_txrep_cond_none(self):
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
        assert txrep == get_txrep_file("test_to_txrep_cond_precond_none.txt")
        assert (
            from_txrep(txrep, Network.TESTNET_NETWORK_PASSPHRASE).to_xdr()
            == te.to_xdr()
        )


KP = Keypair.from_raw_ed25519_seed(bytes(range(32)))
DEST = Keypair.from_raw_ed25519_seed(bytes(range(1, 33))).public_key
MUXED = MuxedAccount(DEST, 42).account_muxed
USD = Asset("USD", DEST)
POOL_ID = LiquidityPoolAsset(Asset.native(), USD).liquidity_pool_id
BALANCE_ID = "00000000" + "ab" * 32
CONTRACT = "CA3D5KRYM6CB7OWQ6TWYRR3Z4T7GNZLKERYNZGGA5SOAOPIFY6YQGAXE"
PAYLOAD_SIGNER = SignerKey.ed25519_signed_payload(SignedPayloadSigner(DEST, b"payload"))
P = ClaimPredicate

# Each builds onto a TransactionBuilder: every operation type, the arms of the unions
# they hold, and the parts of a transaction.
BUILDS = {
    "payment to muxed": lambda b: b.append_payment_op(MUXED, USD, "1"),
    "path payment": lambda b: b.append_path_payment_strict_send_op(
        DEST, USD, "5", Asset.native(), "1", [Asset("LONGASSET12", DEST)]
    ),
    "offer": lambda b: b.append_manage_sell_offer_op(
        USD, Asset.native(), "1", "0.5", 7
    ),
    "set options": lambda b: b.append_set_options_op(
        home_domain="example.com", signer=Signer(PAYLOAD_SIGNER, 1)
    ),
    "change trust pool share": lambda b: b.append_change_trust_op(
        LiquidityPoolAsset(Asset.native(), USD)
    ),
    "allow trust 2": lambda b: b.append_allow_trust_op(
        DEST, "USD", TrustLineEntryFlag.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG
    ),
    "allow trust long code": lambda b: b.append_allow_trust_op(
        DEST, "LONGCODE", TrustLineEntryFlag.AUTHORIZED_FLAG
    ),
    "manage data empty": lambda b: b.append_manage_data_op("my key", b""),
    "claimable unconditional": lambda b: b.append_create_claimable_balance_op(
        Asset.native(),
        "1",
        [Claimant(DEST), Claimant(DEST, P.predicate_not(P.predicate_unconditional()))],
    ),
    "revoke pool trustline": lambda b: b.append_revoke_trustline_sponsorship_op(
        DEST, LiquidityPoolId(POOL_ID)
    ),
    "revoke data with space": lambda b: b.append_revoke_data_sponsorship_op(
        DEST, "my key"
    ),
    "revoke signed payload": lambda b: b.append_operation(
        RevokeSponsorship.revoke_signer_sponsorship(DEST, PAYLOAD_SIGNER)
    ),
    "claim and clawback": lambda b: b.append_claim_claimable_balance_op(
        BALANCE_ID
    ).append_clawback_claimable_balance_op(BALANCE_ID),
    "liquidity pool": lambda b: b.append_liquidity_pool_deposit_op(
        POOL_ID, "1", "2", "0.5", "1.5"
    ).append_liquidity_pool_withdraw_op(POOL_ID, "1", "0.1", "0.2"),
    "memo": lambda b: b.append_bump_sequence_op(1).add_text_memo("café\tok"),
    "preconditions": lambda b: (
        b.append_bump_sequence_op(1)
        .set_ledger_bounds(10, 20)
        .set_min_sequence_number(5)
        .add_extra_signer(PAYLOAD_SIGNER)
    ),
    "invoke contract": lambda b: b.append_invoke_contract_function_op(
        CONTRACT, "hello", [scval.to_symbol("world"), scval.to_address(DEST)]
    ).set_soroban_data(SorobanDataBuilder().set_resource_fee(100).build()),
    "upload wasm": lambda b: b.append_upload_contract_wasm_op(b"\0asm"),
    "extend ttl": lambda b: b.append_extend_footprint_ttl_op(1000),
    "restore": lambda b: b.append_restore_footprint_op(),
    "create contract": lambda b: b.append_create_contract_op(
        bytes(range(32)), KP.public_key, [scval.to_uint32(1)], salt=bytes(32)
    ),
    "create asset contract": lambda b: (
        b.append_create_stellar_asset_contract_from_asset_op(USD)
    ),
}


def build_envelope(build, network=Network.TESTNET_NETWORK_PASSPHRASE):
    """A transaction of KP's account, which `build` adds to."""
    builder = TransactionBuilder(Account(KP.public_key, 1), network)
    build(builder.add_time_bounds(0, 0))
    return builder.build()


@pytest.mark.parametrize("build", BUILDS.values(), ids=BUILDS.keys())
def test_every_operation_round_trips(build):
    envelope = build_envelope(build)
    envelope.sign(KP)
    txrep = to_txrep(envelope)
    assert from_txrep(txrep, NETWORK).to_xdr() == envelope.to_xdr()
    bump = TransactionBuilder.build_fee_bump_transaction(DEST, 200, envelope, NETWORK)
    restored = from_txrep(to_txrep(bump), NETWORK)
    assert isinstance(restored, FeeBumpTransactionEnvelope)
    assert restored.to_xdr() == bump.to_xdr()


@pytest.mark.parametrize(
    ("network", "native"),
    [
        (Network.PUBLIC_NETWORK_PASSPHRASE, "XLM"),
        (Network.TESTNET_NETWORK_PASSPHRASE, "TestXLM"),
        (Network.FUTURENET_NETWORK_PASSPHRASE, "native"),
    ],
)
def test_the_native_asset_is_named_after_the_network(network, native):
    envelope = build_envelope(
        lambda b: b.append_payment_op(DEST, Asset.native(), "1"), network
    )
    field = "tx.operations[0].body.paymentOp.asset"
    assert f"\n{field}: {native}\n" in to_txrep(envelope)


NETWORK = Network.TESTNET_NETWORK_PASSPHRASE
KEY = bytes(range(32))
ACCOUNT = Keypair.from_raw_ed25519_public_key(KEY).public_key
SPEC_EXAMPLE = (
    "AAAAAgAAAAArFkuQQ4QuQY6SkLc5xxSdwpFOvl7VqKVvrfkPSqB+0AAAAGQApSmNAAAAAQAAAAEAAAAAW4nJ"
    "gAAAAABdav0AAAAAAQAAABZFbmpveSB0aGlzIHRyYW5zYWN0aW9uAAAAAAABAAAAAAAAAAEAAAAAQF82"
    "7djPIu+/gHK5hbakwBVRw03TjBN6yNQNQCzR97QAAAABVVNEAAAAAAAyUlQyIZKfbs+tUWuvK7N0nGSC"
    "II0/Go1/CpHXNW3tCwAAAAAX15OgAAAAAAAAAAFKoH7QAAAAQN77Tx+tHCeTJ7Va8YT9zd9z9Peoy0Dn"
    "5TSnHXOgUSS6Np23ptMbR8r9EYWSJGqFdebCSauU7Ddo3ttikiIc5Qw="
)
SPEC_TXREP = """\
type: ENVELOPE_TYPE_TX
tx.sourceAccount: GAVRMS4QIOCC4QMOSKILOOOHCSO4FEKOXZPNLKFFN6W7SD2KUB7NBPLN
tx.fee: 100
tx.seqNum: 46489056724385793
tx.cond.type: PRECOND_TIME
tx.cond.timeBounds.minTime: 1535756672 (2018-08-31T23:04:32Z)
tx.cond.timeBounds.maxTime: 1567292672 (2019-08-31T23:04:32Z)
tx.memo.type: MEMO_TEXT
tx.memo.text: "Enjoy this transaction"
tx.operations.len: 1
tx.operations[0].sourceAccount._present: false
tx.operations[0].body.type: PAYMENT
tx.operations[0].body.paymentOp.destination: \
GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O
tx.operations[0].body.paymentOp.asset: \
USD:GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI
tx.operations[0].body.paymentOp.amount: 400004000 (40.0004)
tx.ext.v: 0
signatures.len: 1
signatures[0].hint: 4aa07ed0
signatures[0].signature: \
defb4f1fad1c279327b55af184fdcddf73f4f7a8cb40e7e534a71d73a05124ba\
369db7a6d31b47cafd118592246a8575e6c249ab94ec3768dedb6292221ce50c
"""


def read(text):
    """The XDR of the transaction envelope a txrep reads as."""
    return from_txrep(text, NETWORK).to_xdr_object()


def lines(text, prefix):
    """The lines of a txrep whose field starts with `prefix`."""
    return [line for line in text.splitlines() if line.startswith(prefix)]


# --- Writing -------------------------------------------------------------------------


def test_the_example_of_the_sep():
    # The SEP's example predates protocol 19, which put timeBounds into cond.
    assert to_txrep(TransactionEnvelope.from_xdr(SPEC_EXAMPLE, NETWORK)) == SPEC_TXREP
    assert from_txrep(SPEC_TXREP, NETWORK).to_xdr() == SPEC_EXAMPLE


def test_assets_and_asset_codes():
    text = to_txrep(
        build_envelope(
            lambda b: (
                b.append_payment_op(DEST, Asset("LONGASSET12", DEST), "1")
                .append_change_trust_op(USD)
                .append_allow_trust_op(DEST, "USD", TrustLineEntryFlag.AUTHORIZED_FLAG)
                .append_revoke_trustline_sponsorship_op(DEST, LiquidityPoolId(POOL_ID))
            )
        )
    )
    op = "tx.operations[0].body.paymentOp.asset"
    assert lines(text, op) == [f"{op}: LONGASSET12:{DEST}"]
    op = "tx.operations[1].body.changeTrustOp"
    assert lines(text, op) == [
        f"{op}.line.type: ASSET_TYPE_CREDIT_ALPHANUM4",
        f"{op}.line.alphaNum4: USD:{DEST}",
        f"{op}.limit: 9223372036854775807 (922337203685.4775807)",
    ]
    op = "tx.operations[2].body.allowTrustOp"
    assert lines(text, op) == [
        f"{op}.trustor: {DEST}",
        f"{op}.asset: USD",
        f"{op}.authorize: 1",
    ]
    op = "tx.operations[3].body.revokeSponsorshipOp.ledgerKey.trustLine.asset"
    assert lines(text, op) == [f"{op}: {POOL_ID}:lp"]


def test_strkeys():
    envelope = build_envelope(
        lambda b: b.append_set_options_op(signer=Signer(PAYLOAD_SIGNER, 1))
    )
    field = "tx.operations[0].body.setOptionsOp.signer.key"
    assert lines(to_txrep(envelope), field) == [
        f"{field}: {PAYLOAD_SIGNER.encoded_signer_key}"
    ]


def test_comments():
    text = to_txrep(
        build_envelope(
            lambda b: b.add_time_bounds(0, 2**64 - 1).append_manage_data_op("a", b"")
        )
    )
    # No date for 0, or for a time beyond the dates Python has.
    assert "\ntx.cond.timeBounds.minTime: 0\n" in text
    assert f"\ntx.cond.timeBounds.maxTime: {2**64 - 1}\n" in text
    assert "manageDataOp.dataValue._present: true\n" in text
    assert "manageDataOp.dataValue: 0 bytes\n" in text


def test_strings_are_escaped():
    envelope = build_envelope(lambda b: b.add_text_memo(b'caf\xc3\xa9 "a\\b"\n\t\x7f'))
    assert lines(to_txrep(envelope), "tx.memo.text") == [
        'tx.memo.text: "caf\\xc3\\xa9 \\"a\\\\b\\"\\n\\x09\\x7f"'
    ]


# A mainnet transaction, 655a25d1c322034d332e5708b1e3dd5139435eb5d3c20c40f0ee1d579e2f50a6
# of ledger 65569438: a fee bump of a deposit_for_burn call to contract
# CAE2G5Z77UP7GYPYGFOWFGW7C7J6I4YP2AFGSADRKQY62SYUFLPNFTXL.
SOROBAN_FEE_BUMP = (
    "AAAABQAAAACfqq0UrRcxxr/H/+B5l03U4RsYLJgchJtBvSoxYdJG7AAAAAABUKU1AAAAAgAAAADZw6Tx"
    "A3MTJlwgVK/EeFuOqhblia4umK62e734lLV80QCY4qkDKMwJAAAAXQAAAAEAAAAAAAAAAAAAAABq/5GG"
    "AAAAAAAAAAEAAAAAAAAAGAAAAAAAAAABCaN3P/0f82H4MV1imt8X0+RzD9AKaQBxVDHtSxQq3tIAAAAQ"
    "ZGVwb3NpdF9mb3JfYnVybgAAAAgAAAASAAAAAAAAAADZw6TxA3MTJlwgVK/EeFuOqhblia4umK62e734"
    "lLV80QAAAAoAAAAAAAAAAAAAAABZaC8AAAAAAwAAAAUAAAANAAAAIP9/EZEV4g1Pp0RnYS9Md8Xt98jc"
    "2CGTasnX0BHdzd4BAAAAEgAAAAGt785ZruUpaPdgYdSUwlJbdWWfpClqZfSZ7ynlZHfklgAAAA0AAAAg"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAAAAAAAAAAAAAAAAAAAAAAAAAAMAAAfQ"
    "AAAAAQAAAAAAAAAAAAAAAQmjdz/9H/Nh+DFdYprfF9Pkcw/QCmkAcVQx7UsUKt7SAAAAEGRlcG9zaXRf"
    "Zm9yX2J1cm4AAAAIAAAAEgAAAAAAAAAA2cOk8QNzEyZcIFSvxHhbjqoW5YmuLpiutnu9+JS1fNEAAAAK"
    "AAAAAAAAAAAAAAAAWWgvAAAAAAMAAAAFAAAADQAAACD/fxGRFeINT6dEZ2EvTHfF7ffI3Nghk2rJ19AR"
    "3c3eAQAAABIAAAABre/OWa7lKWj3YGHUlMJSW3Vln6QpamX0me8p5WR35JYAAAANAAAAIAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgAAAAAAAAAAAAAAAAAAAAAAAAADAAAH0AAAAAAAAAAB"
    "AAAAAAAAAAoAAAAGAAAAAQTCNKVL0skMCYLvyP1bkXKLaWmRNx1RizSscp5b7stbAAAAFAAAAAEAAAAG"
    "AAAAAQmjdz/9H/Nh+DFdYprfF9Pkcw/QCmkAcVQx7UsUKt7SAAAAEAAAAAEAAAACAAAADwAAAAlCdXJu"
    "TGltaXQAAAAAAAASAAAAAa3vzlmu5Slo92Bh1JTCUlt1ZZ+kKWpl9JnvKeVkd+SWAAAAAQAAAAYAAAAB"
    "CaN3P/0f82H4MV1imt8X0+RzD9AKaQBxVDHtSxQq3tIAAAAQAAAAAQAAAAIAAAAPAAAACERlbnlsaXN0"
    "AAAAEgAAAAAAAAAA2cOk8QNzEyZcIFSvxHhbjqoW5YmuLpiutnu9+JS1fNEAAAABAAAABgAAAAEJo3c/"
    "/R/zYfgxXWKa3xfT5HMP0AppAHFUMe1LFCre0gAAABAAAAABAAAAAgAAAA8AAAARTWluRmVlQnlCdXJu"
    "VG9rZW4AAAAAAAASAAAAAa3vzlmu5Slo92Bh1JTCUlt1ZZ+kKWpl9JnvKeVkd+SWAAAAAQAAAAYAAAAB"
    "CaN3P/0f82H4MV1imt8X0+RzD9AKaQBxVDHtSxQq3tIAAAAQAAAAAQAAAAIAAAAPAAAAFFJlbW90ZVRv"
    "a2VuTWVzc2VuZ2VyAAAAAwAAAAUAAAABAAAABgAAAAEJo3c//R/zYfgxXWKa3xfT5HMP0AppAHFUMe1L"
    "FCre0gAAABAAAAABAAAAAgAAAA8AAAASVG9rZW5EZWNpbWFsQ29uZmlnAAAAAAASAAAAAa3vzlmu5Slo"
    "92Bh1JTCUlt1ZZ+kKWpl9JnvKeVkd+SWAAAAAQAAAAYAAAABCaN3P/0f82H4MV1imt8X0+RzD9AKaQBx"
    "VDHtSxQq3tIAAAAUAAAAAQAAAAYAAAABre/OWa7lKWj3YGHUlMJSW3Vln6QpamX0me8p5WR35JYAAAAU"
    "AAAAAQAAAAeZvQ3cUG7hP8T0M/BicJIDTcOPR3PsFpMKGCOhF0Qx1AAAAAemwazG42fkZTVzPOinMgxx"
    "hhbtQvdizy8aCqd6xuBW9gAAAAMAAAABAAAAANnDpPEDcxMmXCBUr8R4W46qFuWJri6YrrZ7vfiUtXzR"
    "AAAAAVVTREMAAAAAO5kROA7+mIugqJAOsc/kTzZvfb6Ua+0HckD39iTfFcUAAAAGAAAAAa3vzlmu5Slo"
    "92Bh1JTCUlt1ZZ+kKWpl9JnvKeVkd+SWAAAAEAAAAAEAAAACAAAADwAAAAlBbGxvd2FuY2UAAAAAAAAR"
    "AAAAAQAAAAIAAAAPAAAABGZyb20AAAASAAAAAAAAAADZw6TxA3MTJlwgVK/EeFuOqhblia4umK62e734"
    "lLV80QAAAA8AAAAHc3BlbmRlcgAAAAASAAAAAQmjdz/9H/Nh+DFdYprfF9Pkcw/QCmkAcVQx7UsUKt7S"
    "AAAAAAAAAAYAAAABre/OWa7lKWj3YGHUlMJSW3Vln6QpamX0me8p5WR35JYAAAAQAAAAAQAAAAIAAAAP"
    "AAAAB0JhbGFuY2UAAAAAEgAAAAEJo3c//R/zYfgxXWKa3xfT5HMP0AppAHFUMe1LFCre0gAAAAEALOF5"
    "AAAAoAAAAqgAAAAAAABMKQAAAAGUtXzRAAAAQJ9DAraTCIdExSvAo373quFd7vUbDgJZ8Wou92/Xd2dU"
    "gKpn4reJF5M9Vk1EPvUPjJLft6wx67SG8FQFbWHRRwcAAAAAAAAAAWHSRuwAAABA1g4e9pHFY6CAUD1N"
    "6UN1YsRUPLS5GJsuSmVYBp5+w1njgto9aGC/uWlKBNG8A8M7l3dHurKhMLZDhsxvexcPDg=="
)


def test_to_txrep_soroban():
    envelope = FeeBumpTransactionEnvelope.from_xdr(
        SOROBAN_FEE_BUMP, Network.PUBLIC_NETWORK_PASSPHRASE
    )
    txrep = to_txrep(envelope)
    assert txrep == get_txrep_file("test_to_txrep_soroban.txt")
    restored = from_txrep(txrep, Network.PUBLIC_NETWORK_PASSPHRASE)
    assert restored.to_xdr() == SOROBAN_FEE_BUMP


def complex_soroban_envelope():
    """A contract call built to hold every kind of Soroban value, address,
    credential, authorized function and ledger key."""
    x = stellar_xdr
    contract = Address(CONTRACT)
    token = Address("CAS3J7GYLGXMF6TDJBBYYSE3HQ6BBSMLNUQ34T6TZMYMW2EVH34XOWMA")
    key = Keypair.from_public_key(DEST).raw_public_key()
    addresses = [
        scval.to_address(DEST),
        scval.to_address(token.address),
        x.SCVal.Address(x.SCAddress.MuxedAccount(x.MuxedEd25519Account(42, key))),
        x.SCVal.Address(x.SCAddress.MuxedContract(x.MuxedContract(7, bytes(32)))),
        x.SCVal.Address(
            x.SCAddress.ClaimableBalance(x.ClaimableBalanceID.V0(bytes([0xAB] * 32)))
        ),
        x.SCVal.Address(x.SCAddress.LiquidityPool(bytes.fromhex(POOL_ID))),
    ]
    numbers = [
        scval.to_bool(True),
        scval.to_void(),
        scval.to_uint32(2**32 - 1),
        scval.to_int32(-(2**31)),
        scval.to_uint64(2**64 - 1),
        scval.to_int64(-1),
        scval.to_timepoint(1795132800),
        scval.to_duration(3600),
        scval.to_uint128(2**128 - 1),
        scval.to_int128(-(10**20)),
        scval.to_uint256(2**256 - 1),
        scval.to_int256(-(2**255)),
    ]
    texts = [
        scval.to_string('say "café"\n'),
        scval.to_symbol("swap_exact"),
        scval.to_bytes(bytes(range(16))),
        scval.to_bytes(b""),
        x.SCVal.Error(x.SCError.Contract(3)),
        x.SCVal.LedgerKeyNonce(x.SCNonceKey(-5)),
    ]
    nested = scval.to_map(
        {
            scval.to_symbol("path"): scval.to_vec(
                [scval.to_vec([]), scval.to_map({}), x.SCVal.Vec(None)]
            ),
            scval.to_symbol("min_out"): scval.to_int128(1),
        }
    )
    arguments = [*addresses, *numbers, *texts, nested]

    def call(address, function, args):
        return x.SorobanAuthorizedFunction.ContractFn(
            x.InvokeContractArgs(address.to_xdr_sc_address(), function.encode(), args)
        )

    def ed25519_signature(seed):
        return scval.to_vec(
            [
                scval.to_map(
                    {
                        scval.to_symbol("public_key"): scval.to_bytes(
                            bytes([seed] * 32)
                        ),
                        scval.to_symbol("signature"): scval.to_bytes(
                            bytes([seed] * 64)
                        ),
                    }
                )
            ]
        )

    wasm = bytes(range(32))
    deploy = x.SorobanAuthorizedInvocation(
        x.SorobanAuthorizedFunction.CreateContractV2HostFn(
            x.CreateContractArgsV2(
                x.ContractIDPreimage.Address(
                    x.ContractIDPreimageFromAddress(
                        Address(DEST).to_xdr_sc_address(), bytes([1] * 32)
                    )
                ),
                x.ContractExecutable.Wasm(wasm),
                [scval.to_symbol("init"), scval.to_uint32(1)],
            )
        ),
        [],
    )
    transfer = x.SorobanAuthorizedInvocation(
        call(token, "transfer", [*addresses[:2], scval.to_int128(10**7)]), [deploy]
    )
    delegate = x.SorobanDelegateSignature(
        token.to_xdr_sc_address(),
        ed25519_signature(2),
        [x.SorobanDelegateSignature(contract.to_xdr_sc_address(), scval.to_void(), [])],
    )
    credentials = x.SorobanAddressCredentials(
        Address(DEST).to_xdr_sc_address(), -(2**63), 2**32 - 1, ed25519_signature(1)
    )
    asset_contract = x.SorobanAuthorizedFunction.CreateContractHostFn(
        x.CreateContractArgs(
            x.ContractIDPreimage.Asset(USD.to_xdr_object()),
            x.ContractExecutable.StellarAsset(),
        )
    )
    auth = [
        x.SorobanAuthorizationEntry(
            x.SorobanCredentials.AddressWithDelegates(
                x.SorobanAddressCredentialsWithDelegates(credentials, [delegate])
            ),
            x.SorobanAuthorizedInvocation(
                call(contract, "swap", arguments), [transfer]
            ),
        ),
        x.SorobanAuthorizationEntry(
            x.SorobanCredentials.AddressV2(
                x.SorobanAddressCredentials(
                    contract.to_xdr_sc_address(), 1, 100, scval.to_void()
                )
            ),
            transfer,
        ),
        x.SorobanAuthorizationEntry(
            x.SorobanCredentials.SourceAccount(),
            x.SorobanAuthorizedInvocation(asset_contract, []),
        ),
    ]

    def data(address, key, durability):
        return x.LedgerKey.ContractData(
            x.LedgerKeyContractData(address.to_xdr_sc_address(), key, durability)
        )

    account = Keypair.from_public_key(DEST).xdr_account_id()
    footprint = x.LedgerFootprint(
        [
            x.LedgerKey.Account(x.LedgerKeyAccount(account)),
            x.LedgerKey.TrustLine(
                x.LedgerKeyTrustLine(account, USD.to_trust_line_asset_xdr_object())
            ),
            x.LedgerKey.TrustLine(
                x.LedgerKeyTrustLine(
                    account, x.TrustLineAsset.PoolShare(bytes.fromhex(POOL_ID))
                )
            ),
            x.LedgerKey.ContractCode(x.LedgerKeyContractCode(wasm)),
            data(
                contract,
                x.SCVal.LedgerKeyContractInstance(),
                x.ContractDataDurability.PERSISTENT,
            ),
        ],
        [
            data(
                token,
                scval.to_vec([scval.to_symbol("Balance"), scval.to_address(DEST)]),
                x.ContractDataDurability.PERSISTENT,
            ),
            data(
                contract,
                x.SCVal.LedgerKeyNonce(x.SCNonceKey(-(2**63))),
                x.ContractDataDurability.TEMPORARY,
            ),
            x.LedgerKey.TTL(x.LedgerKeyTTL(bytes([0xCD] * 32))),
        ],
    )
    soroban_data = x.SorobanTransactionData(
        x.SorobanTransactionDataExt.V1(x.SorobanResourcesExtV0([0, 5])),
        x.SorobanResources(footprint, 50_000_000, 200_000, 66_000),
        12_345_678,
    )
    envelope = (
        TransactionBuilder(Account(KP.public_key, 1), NETWORK, base_fee=100)
        .add_time_bounds(1795132800, 1795133100)
        .add_hash_memo(bytes([0xEF] * 32))
        .append_invoke_contract_function_op(
            CONTRACT, "swap", arguments, auth=auth, source=MUXED
        )
        .set_soroban_data(soroban_data)
        .build()
    )
    envelope.sign(KP)
    return envelope


def test_to_txrep_soroban_complex():
    envelope = complex_soroban_envelope()
    txrep = to_txrep(envelope)
    assert txrep == get_txrep_file("test_to_txrep_soroban_complex.txt")
    assert from_txrep(txrep, NETWORK).to_xdr() == envelope.to_xdr()
    bump = TransactionBuilder.build_fee_bump_transaction(DEST, 200, envelope, NETWORK)
    assert from_txrep(to_txrep(bump), NETWORK).to_xdr() == bump.to_xdr()


def test_soroban_transactions():
    envelope = build_envelope(
        lambda b: b.append_invoke_contract_function_op(
            CONTRACT,
            "hello",
            [scval.to_uint32(7), scval.to_vec([]), scval.to_bool(True)],
        ).set_soroban_data(SorobanDataBuilder().set_resource_fee(100).build())
    )
    text = to_txrep(envelope)
    assert "\ntx.ext.v: 1\n" in text
    assert ".hostFunction.invokeContract.args[2].b: true\n" in text
    assert "\ntx.ext.sorobanData.resourceFee: 100\n" in text
    assert ".hostFunction.invokeContract.args[1].vec._present: true\n" in text
    assert from_txrep(text, NETWORK).to_xdr() == envelope.to_xdr()


# --- Reading -------------------------------------------------------------------------


def test_fields_left_out_are_zero():
    transaction = stellar_xdr.Transaction(
        stellar_xdr.MuxedAccount.Ed25519(bytes(32)),
        0,
        0,
        stellar_xdr.Preconditions.None_(),
        stellar_xdr.Memo.None_(),
        [],
        stellar_xdr.TransactionExt.V0(),
    )
    signature = stellar_xdr.DecoratedSignature(bytes(4), b"")
    assert read("type: ENVELOPE_TYPE_TX\nsignatures.len: 1\n") == (
        stellar_xdr.TransactionEnvelope.Tx(
            stellar_xdr.TransactionV1Envelope(transaction, [signature])
        )
    )


def test_comments_blank_lines_and_line_endings():
    text = SPEC_TXREP.replace("tx.fee: 100\n", ": a comment\r\n\n \ntx.fee: 100 ok\r\n")
    assert read(text) == read(SPEC_TXREP)


def test_the_last_line_of_a_field_counts():
    expected = read(SPEC_TXREP.replace("tx.fee: 100", "tx.fee: 200"))
    assert read(SPEC_TXREP + "tx.fee: 200\n") == expected


def test_enums_by_number_and_integers_in_c_syntax():
    octal = "0" + format(46489056724385793, "o")
    text = (
        SPEC_TXREP.replace("type: ENVELOPE_TYPE_TX", "type: EnvelopeType#2")
        .replace("tx.fee: 100", "tx.fee: 0x64")
        .replace("tx.seqNum: 46489056724385793", f"tx.seqNum: {octal}")
    )
    assert read(text) == read(SPEC_TXREP)


def test_indexes_may_have_leading_zeros():
    expected = read(SPEC_TXREP.replace("amount: 400004000", "amount: 7"))
    text = SPEC_TXREP + "tx.operations[00].body.paymentOp.amount: 7\n"
    assert read(text) == expected


def test_present_left_out_is_there_when_a_field_is():
    absent = "tx.operations[0].sourceAccount._present: false\n"
    text = SPEC_TXREP.replace(absent, "")
    assert read(text) == read(SPEC_TXREP)
    source = f"tx.operations[0].sourceAccount: {ACCOUNT}\n"
    present = f"tx.operations[0].sourceAccount._present: true\n{source}"
    assert read(text + source) == read(SPEC_TXREP.replace(absent, present))


def test_empty_opaque_data_is_0():
    envelope = build_envelope(lambda b: b.append_manage_data_op("a", b""))
    text = to_txrep(envelope).replace("dataValue: 0 bytes", "dataValue:")
    with pytest.raises(InvalidTxrepError, match="'' is not hex"):
        from_txrep(text, NETWORK)


def test_assets_read_as_the_sep_says():
    issued = "asset: USD:GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI"
    for name in ("XLM", "TestXLM", "anything"):
        envelope = from_txrep(SPEC_TXREP.replace(issued, f"asset: {name}"), NETWORK)
        assert "paymentOp.asset: TestXLM\n" in to_txrep(envelope)
    escaped = SPEC_TXREP.replace("asset: USD:", "asset: U\\x53\\D:")
    assert read(escaped) == read(SPEC_TXREP)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (("tx.fee: 100", "tx.feee: 100"), "line 3: tx.feee is not part of the"),
        (("type: MEMO_TEXT", "type: MEMO_ID"), "line 9: tx.memo.text is not part"),
        (("tx.fee: 100", "tx.fee: x"), "line 3: tx.fee: 'x' is not an integer"),
        (("tx.fee: 100", "tx.fee: 4294967296"), "out of range for uint32"),
        (("tx.fee: 100", "tx.fee: 0" + "1" * 30), "is not an integer"),
        (("tx.fee: 100", "tx.fee 100"), "line 3: expected `field: value`"),
        (("tx.fee: 100", "tx..fee: 100"), "line 3: 'tx..fee' is not a field name"),
        (("type: ENVELOPE_TYPE_TX", "type: TX"), "'TX' is not a EnvelopeType"),
        (("type: ENVELOPE_TYPE_TX", "type: EnvelopeType#99"), "is not a EnvelopeType"),
        (("type: ENVELOPE_TYPE_TX", "type: EnvelopeType#x"), "is not a EnvelopeType"),
        (("type: MEMO_TEXT", "type: MemoType#7"), "is not a MemoType"),
        (("_present: false", "_present: no"), "expected true or false, not 'no'"),
        (("operations.len: 1", "operations.len: -1"), "-1 is negative"),
        (("operations.len: 1", "operations.len: 101"), "above the maximum 100"),
        (("operations.len: 1", "operations.len: x"), "'x' is not an integer"),
        (('"Enjoy this transaction"', "Enjoy"), "expected a string in double quotes"),
        (('"Enjoy this transaction"', '"Enjoy'), "the string has no closing quote"),
        (('"Enjoy this transaction"', '"\\q"'), "invalid escape '\\\\q'"),
        (('"Enjoy this transaction"', '"' + "x" * 29 + '"'), "more than 28 bytes"),
        (("hint: 4aa07ed0", "hint: 4aa07e"), "expected 4 bytes, not 3"),
        (("hint: 4aa07ed0", "hint: 4aa07ed0ff"), "more than 4 bytes"),
        (("hint: 4aa07ed0", "hint: 4aa07edz"), "is not hex of whole bytes"),
        (("signature: defb", "signature: d" + "0" * 200), "more than 64 bytes"),
        (("asset: USD:", "asset: USD"), "expected CODE:ISSUER or native"),
        (("asset: USD:", "asset: USDUSDUSDUSDX:"), "at most 12 bytes"),
        (("asset: USD:", "asset: U\\xZZ:"), "\\x without two hex digits"),
        (("asset: USD:", "asset: Ü:"), "printable ASCII"),
        (("destination: GBAF", "destination: GBAD"), "line 13: tx.operations[0]"),
        (("sourceAccount: GAVR", "sourceAccount: TAVR"), "line 2: tx.sourceAccount"),
    ],
)
def test_invalid_txrep(change, message):
    old, new = change
    text = SPEC_TXREP.replace(old, new, 1)
    assert text != SPEC_TXREP
    with pytest.raises(InvalidTxrepError, match=re.escape(message)):
        from_txrep(text, NETWORK)


def test_the_arrays_share_a_budget_of_items():
    def invoke(arguments):
        text = "type: ENVELOPE_TYPE_TX\n"
        text += f"tx.operations.len: {len(arguments)}\n"
        for i, count in enumerate(arguments):
            body = f"tx.operations[{i}].body"
            function = f"{body}.invokeHostFunctionOp.hostFunction"
            text += f"{body}.type: INVOKE_HOST_FUNCTION\n"
            text += f"{function}.type: HOST_FUNCTION_TYPE_INVOKE_CONTRACT\n"
            text += f"{function}.invokeContract.args.len: {count}\n"
        return text

    # Items left out are zero values, which a short text may hold a few of.
    args = "tx.operations[0].body.invokeHostFunctionOp.hostFunction.invokeContract.args"
    assert lines(to_txrep(from_txrep(invoke([2]), NETWORK)), args) == [
        f"{args}.len: 2",
        f"{args}[0].type: SCV_BOOL",
        f"{args}[0].b: false",
        f"{args}[1].type: SCV_BOOL",
        f"{args}[1].b: false",
    ]
    # 8 lines, so at most 1008 items in all.
    with pytest.raises(InvalidTxrepError, match="at most 1008 items"):
        read(invoke([600, 600]))


def test_a_discriminant_without_an_arm():
    message = "line 1: type: TransactionEnvelope has no arm for ENVELOPE_TYPE_SCP"
    with pytest.raises(InvalidTxrepError, match=message):
        read("type: ENVELOPE_TYPE_SCP\n")
    # Left out, a discriminant is the enum's member of 0, ENVELOPE_TYPE_TX_V0.
    message = (
        "feeBump.tx.innerTx.type is left out: "
        "FeeBumpTransactionInnerTx has no arm for ENVELOPE_TYPE_TX_V0"
    )
    with pytest.raises(InvalidTxrepError, match=re.escape(message)):
        read("type: ENVELOPE_TYPE_TX_FEE_BUMP\n")


def test_an_asset_code_left_out_has_no_value():
    text = (
        "type: ENVELOPE_TYPE_TX\ntx.operations.len: 1\n"
        "tx.operations[0].body.type: ALLOW_TRUST\n"
    )
    message = "tx.operations[0].body.allowTrustOp.asset is left out"
    with pytest.raises(InvalidTxrepError, match=re.escape(message)):
        read(text)


def test_messages_quote_the_input_briefly():
    with pytest.raises(InvalidTxrepError) as long_value:
        read(SPEC_TXREP + "signatures[0].signature: " + "z" * 60 + "\n")
    assert f"'{'z' * 37}...' is not hex" in str(long_value.value)
    with pytest.raises(InvalidTxrepError) as long_field:
        read("a" + ".b" * 1000 + ": 1\n")
    assert len(str(long_field.value)) < 200
    unused = "".join(f"x{i}: 1\n" for i in range(12))
    with pytest.raises(InvalidTxrepError, match=r"line 10: x9 .*; and 2 more lines$"):
        read(unused)


def test_nesting_too_deep_for_the_sdk_is_an_error(monkeypatch):
    def convert(envelope, network_passphrase):
        raise RecursionError

    monkeypatch.setattr(TransactionEnvelope, "from_xdr_object", convert)
    with pytest.raises(InvalidTxrepError, match="nested too deeply"):
        read(SPEC_TXREP)


def test_nesting_beyond_python_limits_is_an_error():
    op = "tx.operations[0].body"
    predicate = f"{op}.createClaimableBalanceOp.claimants[0].v0.predicate"
    text = (
        "type: ENVELOPE_TYPE_TX\ntx.operations.len: 1\n"
        f"{op}.type: CREATE_CLAIMABLE_BALANCE\n"
        f"{op}.createClaimableBalanceOp.claimants.len: 1\n"
    )
    text += "".join(
        f"{predicate}{'.notPredicate' * i}.type: CLAIM_PREDICATE_NOT\n"
        for i in range(sys.getrecursionlimit())
    )
    with pytest.raises(InvalidTxrepError, match="nested too deeply"):
        read(text)


# --- The values of fields ------------------------------------------------------------


def test_integers_in_c_syntax():
    texts = ["0", "7", "100", "010", "0x1F", "0X1f", "-5", "+12"]
    assert [parse_integer(t) for t in texts] == [0, 7, 100, 8, 31, 31, -5, 12]
    for text in ["", "1.5", "0b1", "08", "1e3", "--1", "9" * 30]:
        with pytest.raises(InvalidTxrepError, match="is not an integer"):
            parse_integer(text)


def test_string_literals():
    backslash = chr(92)
    assert read_string('"a\\tb\\rc" comment') == b"a\tb\rc"
    assert read_string('"\\b\\f"') == b"\b\f"
    assert read_string('"café"') == "café".encode()
    # A surrogate is no character, even in the pair JSON writes beyond 16 bits.
    for text in [
        f"{backslash}ud83d x",
        f"{backslash}ud83d{backslash}ude00",
        chr(0xD800),
    ]:
        with pytest.raises(InvalidTxrepError, match="is not a character"):
            read_string(f'"{text}"')
    for escape in [f"{backslash}u12", f"{backslash}/"]:
        with pytest.raises(InvalidTxrepError, match="invalid escape"):
            read_string(f'"{escape}"')


def test_string_literals_of_go():
    # SEP-11 strings are Go's interpreted string literals, as its reference
    # implementation writes them.
    b = chr(92)
    text = f'"{b}a{b}v{b}101{b}377{b}U0001f600"'
    assert read_string(text) == b"\a\vA\xff" + "\N{GRINNING FACE}".encode()
    # Go escapes a single quote only in a rune literal.
    for escape in [f"{b}400", f"{b}'"]:
        with pytest.raises(InvalidTxrepError, match="invalid escape"):
            read_string(f'"{escape}"')
    for character in [f"{b}U00110000", f"{b}U0000d800"]:
        with pytest.raises(InvalidTxrepError, match="is not a character"):
            read_string(f'"{character}"')


def test_asset_codes_and_assets():
    assert write_code(b"\x01:\\Z", 0) == "\\x01\\:\\\\Z"
    assert read_code("\\x01\\:\\\\Z", 4) == b"\x01:\\Z"
    assert write_code(b"A B\0", 0) == "A\\x20B"
    # A short code of an AlphaNum12 keeps NULs up to 5 bytes, to read as one.
    assert write_code(b"ABC" + bytes(9), 5) == "ABC\\x00\\x00"
    with pytest.raises(InvalidTxrepError, match="printable ASCII"):
        read_code("U\\", 4)
    with pytest.raises(InvalidTxrepError, match="at most 4 bytes"):
        read_code("ABCDE", 4)
    assert asset_kind("abcdefghijkl", pool_share=False) == NATIVE
    assert asset_kind("A\\:B", pool_share=False) == NATIVE
    with pytest.raises(InvalidTxrepError, match="expected CODE:ISSUER"):
        split_asset("USD")
    with pytest.raises(InvalidTxrepError, match="64 hex digits of a pool ID"):
        read_pool_share("abcd:lp")


# --- The schema ----------------------------------------------------------------------


def test_the_schema_matches_stellar_xdr():
    # A stellar-xdr release that adds a field or an arm, or changes one, needs
    # scripts/txrep_schema.py run.
    for name, d in SCHEMA.items():
        if d[0] == "struct":
            attributes = tuple(attribute for _, attribute, _ in d[2])
            assert getattr(stellar_xdr, d[1]).__match_args__ == attributes, name
        elif d[0] == "union":
            namespace = getattr(stellar_xdr, d[1])
            arms = {
                getattr(cls, d[3])
                for cls in vars(namespace).values()
                if isinstance(cls, type) and issubclass(cls, stellar_xdr.XdrArm)
            }
            assert arms == set(d[5]), name
            for value, (arm_class, _, attribute, _) in d[5].items():
                cls = getattr(namespace, arm_class)
                assert getattr(cls, d[3]) == value, name
                assert cls.__match_args__ == ((attribute,) if attribute else ()), name
        elif d[0] == "enum":
            assert issubclass(getattr(stellar_xdr, d[1]), IntEnum), name


def test_the_rules_match_the_schema():
    def fields(struct):
        return {field: t for field, _, t in SCHEMA[struct][2]}

    for name in {*txrep._STRKEYS, *txrep._ASSETS, txrep._ASSET_CODE}:
        assert SCHEMA[name][0] == "union", name
    for name in txrep._ALPHANUMS:
        assert set(fields(name)) == {"assetCode", "issuer"}, name
    for (struct, field), renamed in txrep._ACCOUNTS.items():
        assert fields(struct)[field] == ("ref", "uint256")
        assert renamed not in fields(struct)
    for struct, field in txrep._AMOUNTS:
        assert fields(struct)[field] == ("ref", "int64"), (struct, field)
    assert SCHEMA[txrep._TIME_POINT] == ("typedef", ("ref", "uint64"))
    inlined = {
        t[1]
        for d in SCHEMA.values()
        if d[0] == "union"
        for _, _, _, t in d[5].values()
        if t is not None and txrep._inlined(t)
    }
    assert inlined == {"TransactionV0Envelope", "TransactionV1Envelope"}
