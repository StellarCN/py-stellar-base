import binascii
import time
from typing import Optional

import pytest

from stellar_sdk import (
    LIQUIDITY_POOL_FEE_V18,
    Account,
    Address,
    Asset,
    AuthorizationFlag,
    Claimant,
    ExtendFootprintTTL,
    FeeBumpTransactionEnvelope,
    InvokeHostFunction,
    Keypair,
    LedgerBounds,
    LiquidityPoolAsset,
    Network,
    Preconditions,
    RestoreFootprint,
    SignedPayloadSigner,
    Signer,
    SignerKey,
    SorobanDataBuilder,
    TimeBounds,
    TransactionBuilder,
    TransactionEnvelope,
    TrustLineEntryFlag,
    TrustLineFlags,
    scval,
)
from stellar_sdk import xdr as stellar_xdr

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
    parsed_tx = TransactionBuilder.from_xdr(xdr, Network.TESTNET_NETWORK_PASSPHRASE)
    assert xdr == parsed_tx.to_xdr()


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
        assert tx.transaction.preconditions.time_bounds.min_time == 0
        assert (
            now + 256 <= tx.transaction.preconditions.time_bounds.max_time <= now + 257
        )

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

    def test_build_without_timebounds_warn(self):
        source_account = Account(kp1.public_key, 100000000000000000)
        tx = TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=100,
            v1=True,
        )
        with pytest.warns(
            UserWarning,
            match="It looks like you haven't set a TimeBounds for the transaction, "
            "we strongly recommend that you set it. "
            "You can learn why you should set it up through this link: "
            "https://www.stellar.org/developers-blog/transaction-submission-timeouts-and-dynamic-fees-faq",
        ):
            _ = tx.append_payment_op(
                kp2.public_key, asset1, "10000", kp1.public_key
            ).build()

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

    def test_set_conds(self):
        source_account = Account(kp1.public_key, 100000000000000000)
        time_bounds = TimeBounds(1649237469, 1649238469)
        ledger_bounds = LedgerBounds(40351800, 40352000)
        min_sequence_number = 103420918407103888
        min_sequence_age = 1649239999
        min_sequence_ledger_gap = 30
        extra_signers = [
            SignerKey.from_encoded_signer_key(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            ),
            SignerKey.from_encoded_signer_key(
                "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
            ),
        ]
        cond = Preconditions(
            time_bounds,
            ledger_bounds,
            min_sequence_number,
            min_sequence_age,
            min_sequence_ledger_gap,
            extra_signers,
        )

        tx1 = (
            TransactionBuilder(
                source_account=source_account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=100,
                v1=True,
            )
            .add_time_bounds(1649237469, 1649238469)
            .set_ledger_bounds(40351800, 40352000)
            .set_min_sequence_number(103420918407103888)
            .set_min_sequence_age(1649239999)
            .set_min_sequence_ledger_gap(30)
            .add_extra_signer(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            )
            .add_extra_signer(
                SignerKey.from_encoded_signer_key(
                    "PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAQACAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUPB6IBZGM"
                )
            )
            .append_bump_sequence_op(0)
            .build()
        )

        assert tx1.transaction.preconditions == cond

        tx2 = (
            TransactionBuilder(
                source_account=source_account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=100,
                v1=True,
            )
            .add_time_bounds(1649237469, 1649238469)
            .set_ledger_bounds(40351800, 40352000)
            .set_min_sequence_number(103420918407103888)
            .set_min_sequence_age(1649239999)
            .set_min_sequence_ledger_gap(30)
            .add_extra_signer(
                "GBJCHUKZMTFSLOMNC7P4TS4VJJBTCYL3XKSOLXAUJSD56C4LHND5TWUC"
            )
            .add_extra_signer(
                SignedPayloadSigner(
                    "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ",
                    b"\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f ",
                )
            )
            .append_bump_sequence_op(0)
            .build()
        )

        assert tx2.transaction.preconditions == cond

    def test_append_invoke_contract_function_op(self):
        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials(
                    stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
                ),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction(
                        type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                        contract_fn=stellar_xdr.InvokeContractArgs(
                            contract_address=Address(
                                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                            ).to_xdr_sc_address(),
                            function_name=scval.to_symbol("hello").sym,
                            args=[
                                scval.to_address(kp2.public_key),
                                scval.to_uint32(10),
                            ],
                        ),
                    ),
                    sub_invocations=[],
                ),
            )
        ]
        tx = get_tx_builder().append_invoke_contract_function_op(
            "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA",
            "hello",
            [scval.to_symbol("world")],
            auth,
            kp2.public_key,
        )
        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT,
            invoke_contract=stellar_xdr.InvokeContractArgs(
                contract_address=Address(
                    "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                ).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(sc_symbol="hello".encode("utf-8")),
                args=[scval.to_symbol("world")],
            ),
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=auth, source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_upload_contract_wasm_op(self):
        tx = get_tx_builder().append_upload_contract_wasm_op(
            b"test_contract_data", kp2.public_key
        )
        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_UPLOAD_CONTRACT_WASM,
            wasm=b"test_contract_data",
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=[], source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_create_contract_op(self):
        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials(
                    stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
                ),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction(
                        type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                        contract_fn=stellar_xdr.InvokeContractArgs(
                            contract_address=Address(
                                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                            ).to_xdr_sc_address(),
                            function_name=scval.to_symbol("hello").sym,
                            args=[
                                scval.to_address(kp2.public_key),
                                scval.to_uint32(10),
                            ],
                        ),
                    ),
                    sub_invocations=[],
                ),
            )
        ]
        salt = b"V2\x1c\x18\xecF\xea-\x83\x90\xdc\x96\xe0\xdd\x8e\x9a}\x96\x88\xc7\x13\xaa\xa5\xef\xc5az\xa3\xf8\xb0F_"
        wasm_id = "75cab8d0f9efb285ef229d57342550dea3c43f5fe397bb500c40eba22900def2"
        tx = get_tx_builder().append_create_contract_op(
            wasm_id, kp2.public_key, None, salt, auth, kp2.public_key
        )
        create_contract = stellar_xdr.CreateContractArgsV2(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                from_address=stellar_xdr.ContractIDPreimageFromAddress(
                    address=Address(kp2.public_key).to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(salt),
                ),
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
                stellar_xdr.Hash(binascii.unhexlify(wasm_id)),
            ),
            constructor_args=[],
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2,
            create_contract_v2=create_contract,
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=auth, source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_create_contract_op_with_constructor_args(self):
        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials(
                    stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
                ),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction(
                        type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                        contract_fn=stellar_xdr.InvokeContractArgs(
                            contract_address=Address(
                                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                            ).to_xdr_sc_address(),
                            function_name=scval.to_symbol("hello").sym,
                            args=[
                                scval.to_address(kp2.public_key),
                                scval.to_uint32(10),
                            ],
                        ),
                    ),
                    sub_invocations=[],
                ),
            )
        ]
        constructor_args = [scval.to_uint32(123), scval.to_uint256(7788)]
        salt = b"V2\x1c\x18\xecF\xea-\x83\x90\xdc\x96\xe0\xdd\x8e\x9a}\x96\x88\xc7\x13\xaa\xa5\xef\xc5az\xa3\xf8\xb0F_"
        wasm_id = "75cab8d0f9efb285ef229d57342550dea3c43f5fe397bb500c40eba22900def2"
        tx = get_tx_builder().append_create_contract_op(
            wasm_id, kp2.public_key, constructor_args, salt, auth, kp2.public_key
        )
        create_contract = stellar_xdr.CreateContractArgsV2(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                from_address=stellar_xdr.ContractIDPreimageFromAddress(
                    address=Address(kp2.public_key).to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(salt),
                ),
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_WASM,
                stellar_xdr.Hash(binascii.unhexlify(wasm_id)),
            ),
            constructor_args=constructor_args,
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT_V2,
            create_contract_v2=create_contract,
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=auth, source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_create_stellar_asset_contract_from_asset_op(self):
        asset = Asset.native()
        tx = get_tx_builder().append_create_stellar_asset_contract_from_asset_op(
            asset, kp2.public_key
        )
        asset_param = asset.to_xdr_object()

        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ASSET,
                from_asset=asset_param,
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
            ),
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=[], source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_create_stellar_asset_contract_from_address_op(self):
        auth = [
            stellar_xdr.SorobanAuthorizationEntry(
                credentials=stellar_xdr.SorobanCredentials(
                    stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
                ),
                root_invocation=stellar_xdr.SorobanAuthorizedInvocation(
                    function=stellar_xdr.SorobanAuthorizedFunction(
                        type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                        contract_fn=stellar_xdr.InvokeContractArgs(
                            contract_address=Address(
                                "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                            ).to_xdr_sc_address(),
                            function_name=scval.to_symbol("hello").sym,
                            args=[
                                scval.to_address(kp2.public_key),
                                scval.to_uint32(10),
                            ],
                        ),
                    ),
                    sub_invocations=[],
                ),
            )
        ]
        salt = b"V2\x1c\x18\xecF\xea-\x83\x90\xdc\x96\xe0\xdd\x8e\x9a}\x96\x88\xc7\x13\xaa\xa5\xef\xc5az\xa3\xf8\xb0F_"

        tx = get_tx_builder().append_create_stellar_asset_contract_from_address_op(
            kp2.public_key, salt, auth, kp2.public_key
        )
        create_contract = stellar_xdr.CreateContractArgs(
            contract_id_preimage=stellar_xdr.ContractIDPreimage(
                stellar_xdr.ContractIDPreimageType.CONTRACT_ID_PREIMAGE_FROM_ADDRESS,
                from_address=stellar_xdr.ContractIDPreimageFromAddress(
                    address=Address(kp2.public_key).to_xdr_sc_address(),
                    salt=stellar_xdr.Uint256(salt),
                ),
            ),
            executable=stellar_xdr.ContractExecutable(
                stellar_xdr.ContractExecutableType.CONTRACT_EXECUTABLE_STELLAR_ASSET,
            ),
        )

        host_function = stellar_xdr.HostFunction(
            stellar_xdr.HostFunctionType.HOST_FUNCTION_TYPE_CREATE_CONTRACT,
            create_contract=create_contract,
        )
        expected_op = InvokeHostFunction(
            host_function=host_function, auth=auth, source=kp2.public_key
        )
        assert tx.build().transaction.operations[0] == expected_op
        check_from_xdr(tx)

    def test_append_bump_footprint_expiration_op(self):
        ledger_key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.CONTRACT_DATA,
            contract_data=stellar_xdr.LedgerKeyContractData(
                contract=Address(
                    "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                ).to_xdr_sc_address(),
                key=stellar_xdr.SCVal(
                    stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE
                ),
                durability=stellar_xdr.ContractDataDurability.PERSISTENT,
            ),
        )
        soroban_data = SorobanDataBuilder().set_read_only([ledger_key]).build()
        tx = (
            get_tx_builder()
            .append_extend_footprint_ttl_op(10, kp2.public_key)
            .set_soroban_data(soroban_data)
        )

        expected_op = ExtendFootprintTTL(10, source=kp2.public_key)
        assert tx.build().transaction.operations[0] == expected_op
        assert tx.soroban_data == soroban_data
        check_from_xdr(tx)

    def test_append_restore_footprint_op(self):
        ledger_key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.CONTRACT_DATA,
            contract_data=stellar_xdr.LedgerKeyContractData(
                contract=Address(
                    "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
                ).to_xdr_sc_address(),
                key=stellar_xdr.SCVal(
                    stellar_xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE
                ),
                durability=stellar_xdr.ContractDataDurability.PERSISTENT,
            ),
        )
        soroban_data = SorobanDataBuilder().set_read_only([ledger_key]).build()
        tx = (
            get_tx_builder()
            .append_restore_footprint_op(kp2.public_key)
            .set_soroban_data(soroban_data)
        )

        expected_op = RestoreFootprint(source=kp2.public_key)
        assert tx.build().transaction.operations[0] == expected_op
        assert tx.soroban_data == soroban_data
        check_from_xdr(tx)

    def test_from_xdr_with_soroban_tx(self):
        xdr = "AAAAAgAAAABz2D6cjPPUvjjROiBj8175aE2/4KmveaaEZX3GNYcLDgAGfMwDGLsIAAADFgAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAGAAAAAAAAAABDdXHEOpqSiOzIgf9Ew6t+cnOiZ9DCOk+T/5T+68QigQAAAAcc3dhcF9leGFjdF90b2tlbnNfZm9yX3Rva2VucwAAAAUAAAAKAAAAAAAAAAAAAAAABkR3SwAAAAoAAAAAAAAAAAAAAAA7r91uAAAAEAAAAAEAAAACAAAAEgAAAAGt785ZruUpaPdgYdSUwlJbdWWfpClqZfSZ7ynlZHfklgAAABIAAAABJbT82FmuwvpjSEOMSJs8PBDJi20hvk/TyzDLaJU++XcAAAASAAAAAAAAAABz2D6cjPPUvjjROiBj8175aE2/4KmveaaEZX3GNYcLDgAAAAW5ofzTAAABkAAAAAEAAAAAAAAAAAAAAAEN1ccQ6mpKI7MiB/0TDq35yc6Jn0MI6T5P/lP7rxCKBAAAABxzd2FwX2V4YWN0X3Rva2Vuc19mb3JfdG9rZW5zAAAABQAAAAoAAAAAAAAAAAAAAAAGRHdLAAAACgAAAAAAAAAAAAAAADuv3W4AAAAQAAAAAQAAAAIAAAASAAAAAa3vzlmu5Slo92Bh1JTCUlt1ZZ+kKWpl9JnvKeVkd+SWAAAAEgAAAAEltPzYWa7C+mNIQ4xImzw8EMmLbSG+T9PLMMtolT75dwAAABIAAAAAAAAAAHPYPpyM89S+ONE6IGPzXvloTb/gqa95poRlfcY1hwsOAAAABbmh/NMAAAGQAAAAAQAAAAAAAAABre/OWa7lKWj3YGHUlMJSW3Vln6QpamX0me8p5WR35JYAAAAIdHJhbnNmZXIAAAADAAAAEgAAAAAAAAAAc9g+nIzz1L440TogY/Ne+WhNv+Cpr3mmhGV9xjWHCw4AAAASAAAAARnx47s3t3BwCYy1zPqlwAspF/4W4550JO4pssJd13rnAAAACgAAAAAAAAAAAAAAAAZEd0sAAAAAAAAAAQAAAAAAAAAFAAAABgAAAAEN1ccQ6mpKI7MiB/0TDq35yc6Jn0MI6T5P/lP7rxCKBAAAABQAAAABAAAABgAAAAEltPzYWa7C+mNIQ4xImzw8EMmLbSG+T9PLMMtolT75dwAAABQAAAABAAAABgAAAAGt785ZruUpaPdgYdSUwlJbdWWfpClqZfSZ7ynlZHfklgAAABQAAAABAAAABxgFFFaBa2bxLnc6Vvd8V5T6wbH7erbiLU+tWkEncPc+AAAAB0w9s+vS1qKrI94fYi6quzlQFTm0YRtoYi7E5H92xLoHAAAABQAAAAAAAAAAc9g+nIzz1L440TogY/Ne+WhNv+Cpr3mmhGV9xjWHCw4AAAABAAAAAHPYPpyM89S+ONE6IGPzXvloTb/gqa95poRlfcY1hwsOAAAAAVVTREMAAAAAO5kROA7+mIugqJAOsc/kTzZvfb6Ua+0HckD39iTfFcUAAAAGAAAAARnx47s3t3BwCYy1zPqlwAspF/4W4550JO4pssJd13rnAAAAFAAAAAEAAAAGAAAAASW0/NhZrsL6Y0hDjEibPDwQyYttIb5P08swy2iVPvl3AAAAEAAAAAEAAAACAAAADwAAAAdCYWxhbmNlAAAAABIAAAABGfHjuze3cHAJjLXM+qXACykX/hbjnnQk7imywl3XeucAAAABAAAABgAAAAGt785ZruUpaPdgYdSUwlJbdWWfpClqZfSZ7ynlZHfklgAAABAAAAABAAAAAgAAAA8AAAAHQmFsYW5jZQAAAAASAAAAARnx47s3t3BwCYy1zPqlwAspF/4W4550JO4pssJd13rnAAAAAQGvzCUAAPnYAAAFCAAAAAAABnxoAAAAATWHCw4AAABA9kGkBFYVo6hFxiwkXLUlBsCzgi4UspM9K6PWZMYhgQZ9kBksR/XLKA86BSaOOcBchII4oqTo9Aqa3fZs08aNBw=="
        tx = TransactionBuilder.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
        assert isinstance(tx, TransactionEnvelope)
        assert tx.transaction.fee == 425164
        expected_tx = stellar_xdr.TransactionEnvelope.from_xdr(xdr)
        assert tx.to_xdr() == expected_tx.to_xdr()
