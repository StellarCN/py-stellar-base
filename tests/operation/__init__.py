from stellar_sdk import (
    LIQUIDITY_POOL_FEE_V18,
    Asset,
    Keypair,
    LiquidityPoolAsset,
    MuxedAccount,
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

muxed1 = MuxedAccount(kp1.public_key, 1)
muxed2 = MuxedAccount(kp1.public_key, 2)
muxed3 = MuxedAccount(kp1.public_key, 3)

native_asset = Asset.native()
asset1 = Asset("USD", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")
asset2 = Asset("CATCOIN", "GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z")
asset3 = Asset("PANDA", "GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z")
liquidity_pool_asset = LiquidityPoolAsset(asset1, asset2, LIQUIDITY_POOL_FEE_V18)


def check_source(op_source, source):
    if source is None:
        assert op_source is None
    elif isinstance(source, str):
        assert op_source == MuxedAccount.from_account(source)
    else:
        assert op_source == source
