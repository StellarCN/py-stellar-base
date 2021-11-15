import binascii
import time
from typing import Optional

import pytest

from stellar_sdk import (
    LIQUIDITY_POOL_FEE_V18,
    Account,
    Asset,
    AuthorizationFlag,
    Claimant,
    FeeBumpTransactionEnvelope,
    Keypair,
    LiquidityPoolAsset,
    Network,
    Signer,
    TransactionBuilder,
    TrustLineEntryFlag,
    TrustLineFlags,
)

kp1 = Keypair.from_secret(
    "SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6"
)  # GBRF6PKZYP4J4WI2A3NF4CGF23SL34GRKA5LTQZCQFEUT2YJDZO2COXH
kp2 = Keypair.from_secret(
    "SAEHLO5233DRWHKG3GN7TLJIHCWWZOACUEYRRKW7FPWC3H4EYX7NEPL4"
)  # GC2GT6BHYJUKD7SVAKXVLBYBCELCHY577CAXJM5QNVLERDGFF37LR35K
kp3 = Keypair.from_secret(
    "SATIN2FUZMRCEU4AWQDY7ZDEX26MF33HRIXCK2L5SPNEABPIT22M446F"
)  # GBMJBEQIHYY5YUY2EMSLRK7Q6T6GSP3FRJKZFYFFKABKTY2CWGLVLKH5

native_asset = Asset.native()
asset1 = Asset("USD", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
asset2 = Asset("CATCOIN", "GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z")
asset3 = Asset("PANDA", "GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z")


def get_tx_builder(
    source_account: Account = None,
    base_fee: int = 100,
    network_passphrase: str = Network.TESTNET_NETWORK_PASSPHRASE,
    min_time: Optional[int] = 1600000000,
    max_time: Optional[int] = 1700000000,
    v1: bool = True,
) -> TransactionBuilder:
    if source_account is None:
        source_account = Account(kp1.public_key, 100000000000000000)
    tx = TransactionBuilder(
        source_account=source_account,
        network_passphrase=network_passphrase,
        base_fee=base_fee,
        v1=v1,
    )
    if min_time is not None and max_time is not None:
        tx.add_time_bounds(min_time, max_time)
    return tx


def check_from_xdr(tx: TransactionBuilder):
    xdr = tx.build().to_xdr()
    tx_builder = TransactionBuilder.from_xdr(xdr, Network.TESTNET_NETWORK_PASSPHRASE)
    assert isinstance(tx_builder, TransactionBuilder)
    assert (
        xdr
        == tx_builder.build().to_xdr()
    )


class TestTransaction:
    def test_append_create_account_op(self):
        tx = get_tx_builder().append_create_account_op(
            kp2.public_key, "1234.56789", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAALf3Bw0AAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_change_trust_op(self):
        tx = get_tx_builder().append_change_trust_op(asset1, "10000", kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAF0h26AAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_payment_op(self):
        tx = get_tx_builder().append_payment_op(
            kp2.public_key, asset1, "10000", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAF0h26AAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_path_payment_strict_receive_op(self):
        tx = get_tx_builder().append_path_payment_strict_receive_op(
            kp2.public_key,
            native_asset,
            "100",
            asset1,
            "200",
            [asset2, asset3],
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAgAAAAAAAAAAO5rKAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_path_payment_strict_send_op(self):
        tx = get_tx_builder().append_path_payment_strict_send_op(
            kp2.public_key,
            native_asset,
            "100",
            asset1,
            "200",
            [asset2, asset3],
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADQAAAAAAAAAAO5rKAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_allow_trust_op(self):
        tx = get_tx_builder().append_allow_trust_op(
            kp2.public_key,
            asset1.code,
            TrustLineEntryFlag.AUTHORIZED_FLAG,
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABwAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAQAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_set_options_op(self):
        tx = get_tx_builder().append_set_options_op(
            kp2.public_key,
            AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED,
            AuthorizationFlag.AUTHORIZATION_REQUIRED,
            255,
            10,
            20,
            30,
            "stellar.org",
            Signer.ed25519_public_key(kp3.public_key, 10),
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABQAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABAAAACAAAAAEAAAABAAAAAQAAAP8AAAABAAAACgAAAAEAAAAUAAAAAQAAAB4AAAABAAAAC3N0ZWxsYXIub3JnAAAAAAEAAAAAWJCSCD4x3FMaIyS4q/D0/Gk/ZYpVkuClUAKp40Kxl1UAAAAKAAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_ed25519_public_key_signer(self):
        tx = get_tx_builder().append_ed25519_public_key_signer(
            kp2.public_key, 10, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAoAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    @pytest.mark.parametrize(
        "key",
        [
            pytest.param(
                "XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL", id="strkey"
            ),
            pytest.param(
                binascii.unhexlify(
                    "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
                ),
                id="bytes",
            ),
            pytest.param(
                "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                id="hex",
            ),
        ],
    )
    def test_append_hashx_signer(self, key):
        tx = get_tx_builder().append_hashx_signer(
            key,
            10,
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAALaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAoAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    @pytest.mark.parametrize(
        "key",
        [
            pytest.param(
                "TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS", id="strkey"
            ),
            pytest.param(
                binascii.unhexlify(
                    "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
                ),
                id="bytes",
            ),
            pytest.param(
                "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                id="hex",
            ),
        ],
    )
    def test_append_pre_auth_tx_signer(self, key):
        tx = get_tx_builder().append_pre_auth_tx_signer(
            key,
            10,
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAHaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAoAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_manage_buy_offer_op(self):
        tx = get_tx_builder().append_manage_buy_offer_op(
            native_asset, asset1, "10", "1", 123456, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAAF9eEAAAAAAQAAAAEAAAAAAAHiQAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_manage_sell_offer_op(self):
        tx = get_tx_builder().append_manage_sell_offer_op(
            native_asset, asset1, "10", "1", 123456, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAwAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAAF9eEAAAAAAQAAAAEAAAAAAAHiQAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_create_passive_sell_offer_op(self):
        tx = get_tx_builder().append_create_passive_sell_offer_op(
            native_asset, asset1, "10", "1", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAABAAAAAAAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAAF9eEAAAAAAQAAAAEAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_account_merge_op(self):
        tx = get_tx_builder().append_account_merge_op(kp2.public_key, kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_inflation_op(self):
        tx = get_tx_builder().append_inflation_op(kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACQAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_manage_data_op(self):
        tx = get_tx_builder().append_manage_data_op("hello", "world", kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACgAAAAVoZWxsbwAAAAAAAAEAAAAFd29ybGQAAAAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_bump_sequence_op(self):
        tx = get_tx_builder().append_bump_sequence_op(
            200000000000000000, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAACwLGivC7FAAAAAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_create_claimable_balance_op(self):
        tx = get_tx_builder().append_create_claimable_balance_op(
            asset1, "100", [Claimant(destination=kp2.public_key)], kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygAAAAABAAAAAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_claim_claimable_balance_op(self):
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        tx = get_tx_builder().append_claim_claimable_balance_op(
            balance_id, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADwAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_begin_sponsoring_future_reserves_op(self):
        tx = get_tx_builder().append_begin_sponsoring_future_reserves_op(
            kp2.public_key, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_end_sponsoring_future_reserves_op(self):
        tx = get_tx_builder().append_end_sponsoring_future_reserves_op(kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEQAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_account_sponsorship_op(self):
        tx = get_tx_builder().append_revoke_account_sponsorship_op(
            kp2.public_key, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAAAAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_trustline_sponsorship_op(self):
        tx = get_tx_builder().append_revoke_trustline_sponsorship_op(
            kp2.public_key, asset1, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_offer_sponsorship_op(self):
        tx = get_tx_builder().append_revoke_offer_sponsorship_op(
            kp2.public_key, 123456, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAACAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAAAB4kAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_data_sponsorship_op(self):
        tx = get_tx_builder().append_revoke_data_sponsorship_op(
            kp2.public_key, "hello", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAADAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAABWhlbGxvAAAAAAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_claimable_balance_sponsorship_op(self):
        claimable_balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        tx = get_tx_builder().append_revoke_claimable_balance_sponsorship_op(
            claimable_balance_id, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAAEAAAAANoNV9p9SFDn/BDSqdDrxzH3r7QFdMAzlbF9SRSbkfW+AAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_liquidity_pool_sponsorship_op(self):
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        tx = get_tx_builder().append_revoke_liquidity_pool_sponsorship_op(
            liquidity_pool_id, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAAAAAAF3XsauDHCczEN2+xvl4cKqDwvvXjOIq3tN+y/TzOA+scAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_revoke_ed25519_public_key_signer_sponsorship_op(self):
        tx = get_tx_builder().append_revoke_ed25519_public_key_signer_sponsorship_op(
            kp2.public_key, kp3.public_key, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAAWJCSCD4x3FMaIyS4q/D0/Gk/ZYpVkuClUAKp40Kxl1UAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    @pytest.mark.parametrize(
        "key",
        [
            pytest.param(
                "XDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH235FXL", id="strkey"
            ),
            pytest.param(
                binascii.unhexlify(
                    "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
                ),
                id="bytes",
            ),
            pytest.param(
                "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                id="hex",
            ),
        ],
    )
    def test_append_revoke_hashx_signer_sponsorship_op(self, key):
        tx = get_tx_builder().append_revoke_hashx_signer_sponsorship_op(
            kp2.public_key, key, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAC2g1X2n1IUOf8ENKp0OvHMfevtAV0wDOVsX1JFJuR9b4AAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    @pytest.mark.parametrize(
        "key",
        [
            pytest.param(
                "TDNA2V62PVEFBZ74CDJKTUHLY4Y7PL5UAV2MAM4VWF6USFE3SH234BSS", id="strkey"
            ),
            pytest.param(
                binascii.unhexlify(
                    "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
                ),
                id="bytes",
            ),
            pytest.param(
                "da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                id="hex",
            ),
        ],
    )
    def test_append_revoke_pre_auth_tx_signer_sponsorship_op(self, key):
        tx = get_tx_builder().append_revoke_pre_auth_tx_signer_sponsorship_op(
            kp2.public_key, key, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEgAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAAB2g1X2n1IUOf8ENKp0OvHMfevtAV0wDOVsX1JFJuR9b4AAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_clawback_op(self):
        tx = get_tx_builder().append_clawback_op(
            asset1, kp2.public_key, "1000", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAEwAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAlQL5AAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_clawback_claimable_balance_op(self):
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        tx = get_tx_builder().append_clawback_claimable_balance_op(
            balance_id, kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFAAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vgAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_set_trust_line_flags_op(self):
        tx = get_tx_builder().append_set_trust_line_flags_op(
            kp2.public_key,
            asset1,
            TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG,
            TrustLineFlags.AUTHORIZED_FLAG
            | TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
            kp1.public_key,
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAABAAAAAMAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_liquidity_pool_deposit_op(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        tx = get_tx_builder().append_liquidity_pool_deposit_op(
            liquidity_pool_id, "10", "20", "0.45", "0.55", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAFmGQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAX14QAAAAAAC+vCAAAAAAkAAAAUAAAACwAAABQAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_append_liquidity_pool_withdraw_op(self):
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset1, asset2, fee)
        liquidity_pool_id = asset.liquidity_pool_id
        tx = get_tx_builder().append_liquidity_pool_withdraw_op(
            liquidity_pool_id, "5", "10", "20", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAF2GQCZjxanl+HB27LrIaAWV9pY5swvK63Ewe95DxeiLKAAAAAAL68IAAAAAABfXhAAAAAAAL68IAAAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_add_text_memo(self):
        tx = (
            get_tx_builder()
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
            .add_text_memo("Hello, Stellar!")
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAQAAAA9IZWxsbywgU3RlbGxhciEAAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_add_id_memo(self):
        tx = (
            get_tx_builder()
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
            .add_id_memo(123456)
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAgAAAAAAAeJAAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_add_hash_memo(self):
        memo = binascii.unhexlify(
            "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
        )
        tx = (
            get_tx_builder()
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
            .add_hash_memo(memo)
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAA1c8ELFI/EvH25dUDOSdoikw9LzUigYNxzR76E6p9S2fAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_add_return_hash_memo(self):
        memo = binascii.unhexlify(
            "573c10b148fc4bc7db97540ce49da22930f4bcd48a060dc7347be84ea9f52d9f"
        )
        tx = (
            get_tx_builder()
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
            .add_return_hash_memo(memo)
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAABFc8ELFI/EvH25dUDOSdoikw9LzUigYNxzR76E6p9S2fAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_tx_v0(self):
        tx = get_tx_builder(v1=False).append_payment_op(
            kp2.public_key, asset1, "10000", kp1.public_key
        )
        xdr = "AAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAZAFjRXhdigABAAAAAQAAAABfXhAAAAAAAGVT8QAAAAAAAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_without_timebounds(self):
        tx = get_tx_builder(min_time=None, max_time=None).append_payment_op(
            kp2.public_key, asset1, "10000", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAAAAAAAAAAAAQAAAAEAAAAAYl89WcP4nlkaBtpeCMXW5L3w0VA6ucMigUlJ6wkeXaEAAAABAAAAALRp+CfCaKH+VQKvVYcBERYj47/4gXSzsG1WSIzFLv64AAAAAVVTRAAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAXSHboAAAAAAAAAAAA"
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_set_timeout(self):
        now = int(time.time())
        tx = (
            get_tx_builder(min_time=None, max_time=None)
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
            .set_timeout(256)
        )
        check_from_xdr(tx)
        tx = tx.build()
        assert tx.transaction.time_bounds.min_time == 0
        assert now + 256 <= tx.transaction.time_bounds.max_time <= now + 257

    def test_build_set_timeout_with_timebounds_exists_raise(self):
        with pytest.raises(
            ValueError,
            match="TimeBounds has been already set - setting timeout would overwrite it.",
        ):
            _ = (
                get_tx_builder()
                .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
                .set_timeout(256)
            )

    def test_build_with_base_fee_equals_500(self):
        tx = get_tx_builder(base_fee=500).append_payment_op(
            kp2.public_key, asset1, "10000", kp1.public_key
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAfQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAF0h26AAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_with_public_network(self):
        tx = get_tx_builder(
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE
        ).append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAF0h26AAAAAAAAAAAAA=="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_with_multi_operations(self):
        tx = (
            get_tx_builder()
            .append_create_account_op(kp2.public_key, "1234.56789", kp1.public_key)
            .append_payment_op(kp2.public_key, asset1, "10000", kp1.public_key)
        )
        xdr = "AAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAMgBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAIAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAALf3Bw0AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAEAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAABdIdugAAAAAAAAAAAA="
        assert tx.build().to_xdr() == xdr
        check_from_xdr(tx)

    def test_build_fee_bump_tx(self):
        inner_tx = (
            get_tx_builder().append_payment_op(
                kp2.public_key, asset1, "10000", kp1.public_key
            )
        ).build()
        inner_tx.sign(kp1)
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            kp2.public_key,
            200,
            inner_tx,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )

        xdr = "AAAABQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAAAAAGQAAAAAgAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAGQBY0V4XYoAAQAAAAEAAAAAX14QAAAAAABlU/EAAAAAAAAAAAEAAAABAAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAAAQAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAF0h26AAAAAAAAAAAAQkeXaEAAABA+hygqmVkdMmAtDZZTHtr5nGeE0OrtZAgNDLyTo2IOajCghiurn6NdxYLSmGScYD+I7FbbA0JUtWlrE97HGpCCAAAAAAAAAAA"
        assert fee_bump_tx.to_xdr() == xdr
        new_te = TransactionBuilder.from_xdr(xdr, Network.TESTNET_NETWORK_PASSPHRASE)
        assert isinstance(new_te, FeeBumpTransactionEnvelope)
        assert new_te.to_xdr() == xdr

    def test_from_xdr_remove_signatures(self):
        tx = (
            get_tx_builder().append_payment_op(
                kp2.public_key, asset1, "10000", kp1.public_key
            )
        ).build()
        xdr = tx.to_xdr()
        tx.sign(kp1)
        xdr_with_signature = tx.to_xdr()
        new_tx_builder = TransactionBuilder.from_xdr(
            xdr_with_signature, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert new_tx_builder.build().to_xdr() == xdr
