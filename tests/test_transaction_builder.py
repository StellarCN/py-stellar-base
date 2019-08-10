import os
import time

import pytest

from stellar_sdk import (
    TransactionBuilder,
    Asset,
    Price,
    Keypair,
    IdMemo,
    HashMemo,
    ReturnHashMemo,
)
from stellar_sdk.account import Account
from stellar_sdk.network import TESTNET_NETWORK_PASSPHRASE
from stellar_sdk.signer import Signer
from stellar_sdk.time_bounds import TimeBounds


class TestTransactionBuilder:
    def test_to_xdr(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        builder = TransactionBuilder(source, TESTNET_NETWORK_PASSPHRASE, base_fee=150)
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

        xdr = "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAJYAAAAAAAAAACAAAAAQAAAABdUQHwAAAAAF1RKQAAAAABAAAAElN0ZWxsYXIgUHl0aG9uIFNESwAAAAAAEAAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAAAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAANHO8AAAAAAAAAABgAAAAFYQ04AAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAA6NSlEAAAAAAAAAAAAQAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAAAAAAAB00zoAAAAAAAAAACAAAAAAAAAAA7msoAAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAAAVhDTgAAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAACVFgvQAAAAAIAAAABVVNEAAAAAADbKWJClJP/FJHtiEuwnTcZMVAqHGElOw/flUVUYdVEwgAAAAFCVEMAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAAAAAAcAAAAA2yliQpST/xSR7YhLsJ03GTFQKhxhJTsP35VFVGHVRMIAAAABWENOAAAAAAEAAAABAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAABQAAAAEAAAAALt+fMJnQ+326OZ4LsjzS3p7VeLsEJ1+D2kXBQyZA90wAAAABAAAAAQAAAAEAAAAGAAAAAQAAABQAAAABAAAAFAAAAAEAAAAUAAAAAQAAABQAAAABAAAADXN0ZWxsYXJjbi5vcmcAAAAAAAABAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAACgAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAABQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAjOJ6fDxpl8Zc2ys9UTC6CUxPoRH9WkjO7jbOapgfIAAAAAACgAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAS20siygGBGcUCeoBXiBP/z1gs2kqp4xzZK0PPpPxaAAAAAACgAAAAAAAAAJAAAAAAAAAAoAAAAFaGVsbG8AAAAAAAABAAAAB292ZXJjYXQAAAAAAAAAAAsAAAAAAAAACgAAAAAAAAAMAAAAAVhDTgAAAAAAm8OHJivcBHRl5iCJecEXlJUMXxJlLoeFsS7Eys55MAAAAAAAAAAAAAZCLEAAAAAtAAAABAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAVhDTgAAAAAAm8OHJivcBHRl5iCJecEXlJUMXxJlLoeFsS7Eys55MAAAAAAABkIsQAAAAAgAAAAJAAAAAAAAJ2YAAAAAAAAABAAAAAFYQ04AAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAAAAAAAAAGQixAAAAALQAAAAQAAAAAAAAACAAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAAAAAAA"
        assert te.to_xdr() == xdr

        xdr_signed = "AAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAJYAAAAAAAAAACAAAAAQAAAABdUQHwAAAAAF1RKQAAAAABAAAAElN0ZWxsYXIgUHl0aG9uIFNESwAAAAAAEAAAAAEAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAAAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAANHO8AAAAAAAAAABgAAAAFYQ04AAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAA6NSlEAAAAAAAAAAAAQAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAAAAAAAB00zoAAAAAAAAAACAAAAAAAAAAA7msoAAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAAAVhDTgAAAAAAy9dx1iMqHHSrGewOxzPEq6pr/rmVnPqyOMcdzPKHnQkAAAACVFgvQAAAAAIAAAABVVNEAAAAAADbKWJClJP/FJHtiEuwnTcZMVAqHGElOw/flUVUYdVEwgAAAAFCVEMAAAAAANspYkKUk/8Uke2IS7CdNxkxUCocYSU7D9+VRVRh1UTCAAAAAAAAAAcAAAAA2yliQpST/xSR7YhLsJ03GTFQKhxhJTsP35VFVGHVRMIAAAABWENOAAAAAAEAAAABAAAAAMvXcdYjKhx0qxnsDsczxKuqa/65lZz6sjjHHczyh50JAAAABQAAAAEAAAAALt+fMJnQ+326OZ4LsjzS3p7VeLsEJ1+D2kXBQyZA90wAAAABAAAAAQAAAAEAAAAGAAAAAQAAABQAAAABAAAAFAAAAAEAAAAUAAAAAQAAABQAAAABAAAADXN0ZWxsYXJjbi5vcmcAAAAAAAABAAAAAC7fnzCZ0Pt9ujmeC7I80t6e1Xi7BCdfg9pFwUMmQPdMAAAACgAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAABQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAjOJ6fDxpl8Zc2ys9UTC6CUxPoRH9WkjO7jbOapgfIAAAAAACgAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAS20siygGBGcUCeoBXiBP/z1gs2kqp4xzZK0PPpPxaAAAAAACgAAAAAAAAAJAAAAAAAAAAoAAAAFaGVsbG8AAAAAAAABAAAAB292ZXJjYXQAAAAAAAAAAAsAAAAAAAAACgAAAAAAAAAMAAAAAVhDTgAAAAAAm8OHJivcBHRl5iCJecEXlJUMXxJlLoeFsS7Eys55MAAAAAAAAAAAAAZCLEAAAAAtAAAABAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAVhDTgAAAAAAm8OHJivcBHRl5iCJecEXlJUMXxJlLoeFsS7Eys55MAAAAAAABkIsQAAAAAgAAAAJAAAAAAAAJ2YAAAAAAAAABAAAAAFYQ04AAAAAAJvDhyYr3AR0ZeYgiXnBF5SVDF8SZS6HhbEuxMrOeTAAAAAAAAAAAAAGQixAAAAALQAAAAQAAAAAAAAACAAAAAAu358wmdD7fbo5nguyPNLentV4uwQnX4PaRcFDJkD3TAAAAAAAAAAB8oedCQAAAEDRFF2/sLeCbe9/ZdylwgbxzX00Lhy0osQm4EXQrXj+VT1D5G9WHt06QF7JnDl7W+QnrV03MPjkSUWp3zQ+ob4A"
        signer = Keypair.from_secret(
            "SCCS5ZBI7WVIJ4SW36WGOQQIWJYCL3VOAULSXX3FB57USIO25EDOYQHH"
        )
        te.sign(signer)
        print(te.to_xdr())
        assert te.to_xdr() == xdr_signed

        restore_te = TransactionBuilder.from_xdr(xdr_signed, TESTNET_NETWORK_PASSPHRASE)
        assert restore_te.to_xdr() == xdr_signed

    def test_set_timeout(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        timeout = 1000
        builder = TransactionBuilder(
            source, TESTNET_NETWORK_PASSPHRASE, base_fee=150
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
                source, TESTNET_NETWORK_PASSPHRASE, base_fee=150
            ).add_time_bounds(0, now + timeout).set_timeout(1000)

    def test_add_memo(self):
        source = Account("GDF5O4OWEMVBY5FLDHWA5RZTYSV2U276XGKZZ6VSHDDR3THSQ6OQS7UM", 1)
        builder = TransactionBuilder(
            source, TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_id_memo(100)
        assert builder.memo == IdMemo(100)

        memo_hash = os.urandom(32)
        builder = TransactionBuilder(
            source, TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_hash_memo(memo_hash)
        assert builder.memo == HashMemo(memo_hash)
        builder = TransactionBuilder(
            source, TESTNET_NETWORK_PASSPHRASE, base_fee=150
        ).add_return_hash_memo(memo_hash)
        assert builder.memo == ReturnHashMemo(memo_hash)
