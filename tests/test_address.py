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
