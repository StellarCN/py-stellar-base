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
)


class TestTransactionBuilder:
    def test_to_xdr_v0(self):
        sequence = 1
        source = Account(
            "GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", sequence
        )
        builder = TransactionBuilder(
            source, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=150
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
            .append_path_payment_op(
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
            .build()
        )

        xdr = "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"
        assert te.to_xdr() == xdr

        xdr_signed = "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAKjAAAAAAAAAACAAAAAQAAAABdUQHwAAAAAF1RKQAAAAABAAAAElN0ZWxsYXIgUHl0aG9uIFNESwAAAAAAEgAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAAAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAANHO8AAAAAAAAAABgAAAAFYQ04AAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAA6NSlEAAAAAAAAAAAAQAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAAAAAAAB00zoAAAAAAAAAACAAAAAAAAAAA7msoAAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAAAVhDTgAAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAACVFgvQAAAAAIAAAABVVNEAAAAAADbKWJClJP/FJHtiEuwnTcZMVAqHGElOw/flUVUYdVEwgAAAAFCVEMAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAAAAAAIAAAAAAAAAADuaygAAAAAALt+fMJnQ+326OZ4LsjzS3p7VeLsEJ1+D2kXBQyZA90wAAAABWENOAAAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAAAJUWC9AAAAAAgAAAAFVU0QAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAUJUQwAAAAAA2yliQpST/xSR7YhLsJ03GTFQKhxhJTsP35VFVGHVRMIAAAAAAAAADQAAAAAAAAAAO5rKAAAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAFYQ04AAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAAAlRYL0AAAAACAAAAAVVTRAAAAAAA2yliQpST/xSR7YhLsJ03GTFQKhxhJTsP35VFVGHVRMIAAAABQlRDAAAAAADbKWJClJP/FJHtiEuwnTcZMVAqHGElOw/flUVUYdVEwgAAAAAAAAAHAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAVhDTgAAAAABAAAAAQAAAADL13HWIyocdKsZ7A7HM8Srqmv+uZWc+rI4xx3M8oedCQAAAAUAAAABAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAAAQAAAAEAAAABAAAABgAAAAEAAAAUAAAAAQAAABQAAAABAAAAFAAAAAEAAAAUAAAAAQAAAA1zdGVsbGFyY24ub3JnAAAAAAAAAQAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAoAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAACbw4cmK9wEdGXmIIl5wReUlQxfEmUuh4WxLsTKznkwAAAAAAUAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAIzienw8aZfGXNsrPVEwuglMT6ER/VpIzu42zmqYHyAAAAAAAoAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEttLIsoBgRnFAnqAV4gT/89YLNpKqeMc2StDz6T8WgAAAAAAoAAAAAAAAACQAAAAAAAAAKAAAABWhlbGxvAAAAAAAAAQAAAAdvdmVyY2F0AAAAAAAAAAALAAAAAAAAAAoAAAAAAAAADAAAAAFYQ04AAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAAAAAAAAAGQixAAAAALQAAAAQAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAFYQ04AAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAAAAZCLEAAAAAIAAAACQAAAAAAACdmAAAAAAAAAAQAAAABWENOAAAAAACbw4cmK9wEdGXmIIl5wReUlQxfEmUuh4WxLsTKznkwAAAAAAAAAAAABkIsQAAAAC0AAAAEAAAAAAAAAAgAAAAALt+fMJnQ+326OZ4LsjzS3p7VeLsEJ1+D2kXBQyZA90wAAAAAAAAAAfKHnQkAAABAK4QrN2s/qldwTQG+XHZ/KgKmc1t3MoTE7wa34OuIBVCDdC58WChaHVaB40hcGGbR6Q9Y83Qdj+e1dPNLBQ18Bw=="
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
            .append_path_payment_op(
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
