import os

from stellar_sdk import Account, Keypair, Network, Asset, Price, Signer
from stellar_sdk.sep.txrep import to_txrep
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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_utf8.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te.to_xdr())
        assert txrep == get_txrep_file("test_to_txrep.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_signer.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_source.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_no_timebounds.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_id_memo.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_none_memo.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_hash_memo.txt")

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
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        )
        te = transaction_builder.build()
        te.sign(keypair)
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_return_memo.txt")

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
        transaction_builder.append_create_account_op(
            destination="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            starting_balance="10",
            source=keypair.public_key,
        )
        transaction_builder.append_payment_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            asset_code="USD",
            asset_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="40.0004",
            source=keypair.public_key,
        ),
        transaction_builder.append_path_payment_strict_receive_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            send_code="USD",
            send_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            send_max="10",
            dest_code="XCN",
            dest_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
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
            selling_code="XCN",
            selling_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            buying_code="USD",
            buying_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="100.123",
            price=Price(n=7, d=1),
            offer_id=12345,
            source=keypair.public_key,
        )
        transaction_builder.append_create_passive_sell_offer_op(
            selling_code="XCN",
            selling_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            buying_code="USD",
            buying_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="100.123",
            price="7.1",
            source=keypair.public_key,
        )
        transaction_builder.append_set_options_op(
            inflation_dest="GCVAZXCGX3HLHZ6P5WKEPE3U2YJMTLMPTZJFGY67MTNPSOA4COKVJ6AF",
            clear_flags=None,
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
            asset_code="XCN",
            asset_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
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
            selling_code="XCN",
            selling_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
            buying_code="USD",
            buying_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            amount="100.123",
            price="7.1",
            source=keypair.public_key,
        )
        transaction_builder.append_path_payment_strict_send_op(
            destination="GBAF6NXN3DHSF357QBZLTBNWUTABKUODJXJYYE32ZDKA2QBM2H33IK6O",
            send_code="USD",
            send_issuer="GAZFEVBSEGJJ63WPVVIWXLZLWN2JYZECECGT6GUNP4FJDVZVNXWQWMYI",
            send_amount="10",
            dest_code="XCN",
            dest_issuer="GAYE5SDEM5JIEMGQ7LBMQVRQRVJB6A5E7AZVLJYFL3CNHLZX24DFD35F",
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

        te = transaction_builder.build()
        te.sign(keypair)
        te.sign_hashx(
            bytes.fromhex(
                "8b73f9e12fcc8cd9580a2a26aec14d6175aa1ff45e76b816618635d03f3256b8"
            )
        )
        txrep = to_txrep(te)
        assert txrep == get_txrep_file("test_to_txrep_full_tx.txt")
