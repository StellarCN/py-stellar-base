import os
import time

import pytest

from stellar_sdk import (
    TransactionBuilder,
    Account,
    Network,
    Signer,
    TimeBounds,
    Asset,
    Price,
    Keypair,
    IdMemo,
    HashMemo,
    ReturnHashMemo,
    Claimant,
)


class TestTransactionBuilder:
    def test_to_xdr_v0(self):
        sequence = 1
        source = Account(
            "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", sequence
        )
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150, v1=False
        )
        builder.add_text_memo("Stellar Python SDK")
        builder.add_time_bounds(1565590000, 1565600000)
        te = (
            builder.append_create_account_op(
                "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                "5.5",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
            )
            .append_change_trust_op(
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "100000",
            )
            .append_payment_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "12.25",
                "XLM",
            )
            .append_path_payment_strict_receive_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "XLM",
                None,
                "100",
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "1000.5",
                [
                    Asset(
                        "USD",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                    Asset(
                        "BTC",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                ],
            )
            .append_path_payment_strict_send_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "XLM",
                None,
                "100",
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "1000.5",
                [
                    Asset(
                        "USD",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                    Asset(
                        "BTC",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                ],
            )
            .append_allow_trust_op(
                "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6", "XCN", True
            )
            .append_set_options_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                1,
                6,
                20,
                20,
                20,
                20,
                "stellarcn.org",
                Signer.ed25519_public_key(
                    "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF", 10
                ),
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
            )
            .append_ed25519_public_key_signer(
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD", 5
            )
            .append_hashx_signer(
                bytes.fromhex(
                    "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8000"
                ),
                10,
            )
            .append_pre_auth_tx_signer(
                bytes.fromhex(
                    "2db4b22ca018119c5027a80578813ffcf582cda4aa9e31cd92b43cfa4fc5a000"
                ),
                10,
            )
            .append_inflation_op()
            .append_manage_data_op("hello", "overcat")
            .append_bump_sequence_op(10)
            .append_manage_buy_offer_op(
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "XLM",
                None,
                "10.5",
                "11.25",
            )
            .append_manage_sell_offer_op(
                "XLM",
                None,
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "10.5",
                Price(8, 9),
                10086,
            )
            .append_create_passive_sell_offer_op(
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "XLM",
                None,
                "10.5",
                "11.25",
            )
            .append_account_merge_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF"
            )
            .append_claim_claimable_balance_op(
                "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
            )
            .append_create_claimable_balance_op(
                Asset.native(),
                "100",
                [
                    Claimant(
                        destination="GCXGGIREYPENNT3LYFRD5I2SDALFWM3NKKLIQD3DMJ63ML5N3FG4OQQG"
                    )
                ],
            )
            .build()
        )
        xdr = "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"
        assert te.to_xdr() == xdr

        xdr_signed = "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"
        signer = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        te.sign(signer)
        assert te.to_xdr() == xdr_signed

        restore_te = TransactionBuilder.from_xdr(
            xdr_signed, Network.TESTNET_NETWORK_PASSPHRASE
        ).build()
        assert restore_te.to_xdr() == xdr
        assert source.sequence == sequence + 1
        restore_builder = TransactionBuilder.from_xdr(
            xdr_signed, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert restore_builder.v1 is False
        assert restore_builder.build().to_xdr() == xdr

    def test_to_xdr_v1(self):
        sequence = 1
        source = Account(
            "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", sequence
        )
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150, v1=True
        )
        builder.add_text_memo("Stellar Python SDK")
        builder.add_time_bounds(1565590000, 1565600000)
        te = (
            builder.append_create_account_op(
                "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                "5.5",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
            )
            .append_change_trust_op(
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "100000",
            )
            .append_payment_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "12.25",
                "XLM",
            )
            .append_path_payment_strict_receive_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "XLM",
                None,
                "100",
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "1000.5",
                [
                    Asset(
                        "USD",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                    Asset(
                        "BTC",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                ],
            )
            .append_path_payment_strict_send_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                "XLM",
                None,
                "100",
                "XCN",
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
                "1000.5",
                [
                    Asset(
                        "USD",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                    Asset(
                        "BTC",
                        "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6",
                    ),
                ],
            )
            .append_allow_trust_op(
                "GDNSSYSCSSJ76FER5WEEXME5G4MTCUBKDRQSKOYP36KUKVDB2VCMERS6", "XCN", True
            )
            .append_set_options_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF",
                1,
                6,
                20,
                20,
                20,
                20,
                "stellarcn.org",
                Signer.ed25519_public_key(
                    "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF", 10
                ),
                "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM",
            )
            .append_ed25519_public_key_signer(
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD", 5
            )
            .append_hashx_signer(
                bytes.fromhex(
                    "3389e9f0f1a65f19736cacf544c2e825313e8447f569233bb8db39aa607c8000"
                ),
                10,
            )
            .append_pre_auth_tx_signer(
                bytes.fromhex(
                    "2db4b22ca018119c5027a80578813ffcf582cda4aa9e31cd92b43cfa4fc5a000"
                ),
                10,
            )
            .append_inflation_op()
            .append_manage_data_op("hello", "overcat")
            .append_bump_sequence_op(10)
            .append_manage_buy_offer_op(
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "XLM",
                None,
                "10.5",
                "11.25",
            )
            .append_manage_sell_offer_op(
                "XLM",
                None,
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "10.5",
                Price(8, 9),
                10086,
            )
            .append_create_passive_sell_offer_op(
                "XCN",
                "GCN4HBZGFPOAI5DF4YQIS6OBC6KJKDC7CJSS5B4FWEXMJSWOPEYABLSD",
                "XLM",
                None,
                "10.5",
                "11.25",
            )
            .append_account_merge_op(
                "GAXN7HZQTHIPW7N2HGPAXMR42LPJ5VLYXMCCOX4D3JC4CQZGID3UYUPF"
            )
            .append_claim_claimable_balance_op(
                "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
            )
            .append_create_claimable_balance_op(
                Asset.native(),
                "100",
                [
                    Claimant(
                        destination="GCXGGIREYPENNT3LYFRD5I2SDALFWM3NKKLIQD3DMJ63ML5N3FG4OQQG"
                    )
                ],
            )
            .build()
        )

        xdr_unsigned = te.to_xdr()

        signer = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        te.sign(signer)
        restore_builder = TransactionBuilder.from_xdr(
            te.to_xdr(), Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert restore_builder.v1 is True
        assert restore_builder.build().to_xdr() == xdr_unsigned

    def test_set_timeout(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        timeout = 1000
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).set_timeout(1000)
        now = int(time.time())
        assert isinstance(builder.time_bounds, TimeBounds)
        assert builder.time_bounds.min_time == 0
        assert now + timeout - 1 <= builder.time_bounds.max_time <= now + timeout + 1

    def test_set_timeout_timebounds_raise(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        timeout = 1000
        now = int(time.time())
        with pytest.raises(
            ValueError,
            match="TimeBounds has been already set - setting timeout would overwrite it.",
        ):
            TransactionBuilder(
                source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
            ).add_time_bounds(0, now + timeout).set_timeout(1000)

    def test_add_memo(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_id_memo(100)
        assert builder.memo == IdMemo(100)

        memo_hash = os.urandom(32)
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_hash_memo(memo_hash)
        assert builder.memo == HashMemo(memo_hash)
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_return_hash_memo(memo_hash)
        assert builder.memo == ReturnHashMemo(memo_hash)

    def test_to_xdr_sponsored_reserves(self):
        sequence = 1
        source = Account(
            "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", sequence
        )
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150, v1=False
        )
        builder.add_text_memo("Stellar Python SDK")
        builder.add_time_bounds(1565590000, 1565600000)
        op_source = "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM"
        op_account_id = "GCWWANEIF3Z4DMOE4LDRCS22HLLHOEQCOF3QKAC2XWTSYR2AEEQ3P5FW"
        te = (
            builder.append_begin_sponsoring_future_reserves_op(
                sponsored_id="GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC",
                source=op_source,
            )
            .append_end_sponsoring_future_reserves_op(source=op_source)
            .append_revoke_account_sponsorship_op(
                account_id=op_account_id, source=op_source
            )
            .append_revoke_trustline_sponsorship_op(
                account_id=op_account_id, asset=Asset.native(), source=op_source
            )
            .append_revoke_offer_sponsorship_op(
                seller_id=op_account_id, offer_id=12315, source=op_source
            )
            .append_revoke_data_sponsorship_op(
                account_id=op_account_id, data_name="stellar", source=op_source
            )
            .append_revoke_claimable_balance_sponsorship_op(
                claimable_balance_id="00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                source=op_source,
            )
            .append_revoke_ed25519_public_key_signer_sponsorship_op(
                account_id=op_account_id,
                signer_key="GBWYVWA2PZBTRRBNZI55OG4EFDJSDNL6ASP2VAQKHORNUSSXP2NCV4N2",
                source=op_source,
            )
            .append_revoke_hashx_signer_sponsorship_op(
                account_id=op_account_id,
                signer_key="da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                source=op_source,
            )
            .append_revoke_pre_auth_tx_signer_sponsorship_op(
                account_id=op_account_id,
                signer_key="da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                source=op_source,
            )
            .build()
        )

        xdr = "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAF3AAAAAAAAAACAAAAAQAAAABdUQHwAAAAAF1RKQAAAAABAAAAElN0ZWxsYXIgUHl0aG9uIFNESwAAAAAACgAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAAQAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCxAAAAAQAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAABEAAAABAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAEgAAAAAAAAAAAAAAAK1gNIgu88GxxOLHEUtaOtZ3EgJxdwUAWr2nLEdAISG3AAAAAQAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAABIAAAAAAAAAAQAAAACtYDSILvPBscTixxFLWjrWdxICcXcFAFq9pyxHQCEhtwAAAAAAAAABAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAEgAAAAAAAAACAAAAAK1gNIgu88GxxOLHEUtaOtZ3EgJxdwUAWr2nLEdAISG3AAAAAAAAMBsAAAABAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAEgAAAAAAAAADAAAAAK1gNIgu88GxxOLHEUtaOtZ3EgJxdwUAWr2nLEdAISG3AAAAB3N0ZWxsYXIAAAAAAQAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAABIAAAAAAAAABAAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAASAAAAAQAAAACtYDSILvPBscTixxFLWjrWdxICcXcFAFq9pyxHQCEhtwAAAABtitgafkM4xC3KO9cbhCjTIbV+BJ+qggo7otpKV36aKgAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAASAAAAAQAAAACtYDSILvPBscTixxFLWjrWdxICcXcFAFq9pyxHQCEhtwAAAALaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAASAAAAAQAAAACtYDSILvPBscTixxFLWjrWdxICcXcFAFq9pyxHQCEhtwAAAAHaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAAAAAAA"
        assert te.to_xdr() == xdr
        restore_te = TransactionBuilder.from_xdr(
            xdr, Network.TESTNET_NETWORK_PASSPHRASE
        ).build()
        assert restore_te.to_xdr() == xdr
