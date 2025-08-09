import pytest

from stellar_sdk import StrKey
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.address import Address, AddressType


class TestAddress:
    def test_constructor_account_id(self):
        account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        address = Address(account_id)
        assert address.type == AddressType.ACCOUNT
        assert address.address == account_id

    def test_constructor_contract_id(self):
        contract_id = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        address = Address(contract_id)
        assert address.type == AddressType.CONTRACT
        assert address.address == contract_id

    def test_constructor_muxed_account_id(self):
        muxed_account_id = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        address = Address(muxed_account_id)
        assert address.type == AddressType.MUXED_ACCOUNT
        assert address.address == muxed_account_id

    def test_constructor_claimable_balance_id(self):
        claimable_balance_id = (
            "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
        )
        address = Address(claimable_balance_id)
        assert address.type == AddressType.CLAIMABLE_BALANCE
        assert address.address == claimable_balance_id

    def test_constructor_liquidity_pool_id(self):
        liquidity_pool_id = "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
        address = Address(liquidity_pool_id)
        assert address.type == AddressType.LIQUIDITY_POOL
        assert address.address == liquidity_pool_id

    def test_constructor_invalid_address_throws(self):
        account_id = "GINVALID"
        with pytest.raises(ValueError, match="Unsupported address type."):
            Address(account_id)

    def test_constructor_secret_throws(self):
        secret = "SBUIAXRYKAEJWBSJZYE6P4N4X4ATXP5GAFK5TZ6SKKQ6TS4MLX6G6E4M"
        with pytest.raises(ValueError, match="Unsupported address type."):
            Address(secret)

    def test_from_account_byte(self):
        account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        address = Address.from_raw_account(StrKey.decode_ed25519_public_key(account_id))
        assert address.type == AddressType.ACCOUNT
        assert address.address == account_id

    def test_from_contract_byte(self):
        contract_id = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        address = Address.from_raw_contract(StrKey.decode_contract(contract_id))
        assert address.type == AddressType.CONTRACT
        assert address.address == contract_id

    def test_from_muxed_account_byte(self):
        muxed_account_id = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        address = Address.from_raw_muxed_account(
            StrKey.decode_med25519_public_key(muxed_account_id)
        )
        assert address.type == AddressType.MUXED_ACCOUNT
        assert address.address == muxed_account_id

    def test_from_claimable_balance_byte(self):
        claimable_balance_id = (
            "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
        )
        address = Address.from_raw_claimable_balance(
            StrKey.decode_claimable_balance(claimable_balance_id)
        )
        assert address.type == AddressType.CLAIMABLE_BALANCE
        assert address.address == claimable_balance_id

    def test_from_liquidity_pool_byte(self):
        liquidity_pool_id = "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
        address = Address.from_raw_liquidity_pool(
            StrKey.decode_liquidity_pool(liquidity_pool_id)
        )
        assert address.type == AddressType.LIQUIDITY_POOL
        assert address.address == liquidity_pool_id

    def test_to_xdr_sc_address_account(self):
        account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        address = Address(account_id)
        sc_address = address.to_xdr_sc_address()

        xdr = "AAAAAAAAAAA/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="
        assert sc_address.to_xdr() == xdr

    def test_to_xdr_sc_address_contract(self):
        contract = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        address = Address(contract)
        sc_address = address.to_xdr_sc_address()

        xdr = "AAAAAT8MNL+TrQ2ZcdBMzJD3BVEcg4qtlzSkovsNegP8f+ia"
        assert sc_address.to_xdr() == xdr

    def test_to_xdr_sc_address_muxed_account(self):
        muxed_account_id = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        address = Address(muxed_account_id)
        sc_address = address.to_xdr_sc_address()

        xdr = "AAAAAgAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="
        assert sc_address.to_xdr() == xdr

    def test_to_xdr_sc_address_claimable_balance(self):
        claimable_balance_id = (
            "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
        )
        address = Address(claimable_balance_id)
        sc_address = address.to_xdr_sc_address()

        xdr = "AAAAAwAAAAA/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="
        assert sc_address.to_xdr() == xdr

    def test_to_xdr_sc_address_liquidity_pool(self):
        liquidity_pool_id = "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
        address = Address(liquidity_pool_id)
        sc_address = address.to_xdr_sc_address()

        xdr = "AAAABD8MNL+TrQ2ZcdBMzJD3BVEcg4qtlzSkovsNegP8f+ia"
        assert sc_address.to_xdr() == xdr

    def test_from_xdr_sc_address_account(self):
        xdr = "AAAAAAAAAAA/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="

        sc_address = Address.from_xdr_sc_address(stellar_xdr.SCAddress.from_xdr(xdr))
        account_id = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
        assert sc_address.address == account_id
        assert sc_address.type == AddressType.ACCOUNT

    def test_from_xdr_sc_address_contract(self):
        xdr = "AAAAAT8MNL+TrQ2ZcdBMzJD3BVEcg4qtlzSkovsNegP8f+ia"

        sc_address = Address.from_xdr_sc_address(stellar_xdr.SCAddress.from_xdr(xdr))
        contract = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        assert sc_address.address == contract
        assert sc_address.type == AddressType.CONTRACT

    def test_from_xdr_sc_address_muxed_account(self):
        xdr = "AAAAAgAAAAAAAATSIAB1furlg/xQ3Wafl2c6zCXsclgjrHP69sffMa0x5Qk="

        sc_address = Address.from_xdr_sc_address(stellar_xdr.SCAddress.from_xdr(xdr))
        muxed_account_id = (
            "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        )
        assert sc_address.address == muxed_account_id
        assert sc_address.type == AddressType.MUXED_ACCOUNT

    def test_from_xdr_sc_address_claimable_balance(self):
        xdr = "AAAAAwAAAAA/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="

        sc_address = Address.from_xdr_sc_address(stellar_xdr.SCAddress.from_xdr(xdr))
        claimable_balance_id = (
            "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
        )
        assert sc_address.address == claimable_balance_id
        assert sc_address.type == AddressType.CLAIMABLE_BALANCE

    def test_from_xdr_sc_address_liquidity_pool(self):
        xdr = "AAAABD8MNL+TrQ2ZcdBMzJD3BVEcg4qtlzSkovsNegP8f+ia"

        sc_address = Address.from_xdr_sc_address(stellar_xdr.SCAddress.from_xdr(xdr))
        liquidity_pool_id = "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"
        assert sc_address.address == liquidity_pool_id
        assert sc_address.type == AddressType.LIQUIDITY_POOL

    def test_to_xdr_sc_val(self):
        contract = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        address = Address(contract)
        sc_val = address.to_xdr_sc_val()

        xdr = "AAAAEgAAAAE/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="
        assert sc_val.to_xdr() == xdr

    def test_from_xdr_sc_val(self):
        xdr = "AAAAEgAAAAE/DDS/k60NmXHQTMyQ9wVRHIOKrZc0pKL7DXoD/H/omg=="

        sc_val = Address.from_xdr_sc_val(stellar_xdr.SCVal.from_xdr(xdr))
        contract = "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA"
        assert sc_val.address == contract
        assert sc_val.type == AddressType.CONTRACT
