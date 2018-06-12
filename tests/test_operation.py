# coding:utf-8
import mock
import pytest

from stellar_base.operation import *
from stellar_base.asset import Asset


class TestXdrAmount:
    def test_to_xdr_amount(self):
        assert (Operation.to_xdr_amount("20") == 20 * 10 ** 7)
        assert (Operation.to_xdr_amount("0.1234567") == 1234567)

    def test_to_xdr_amount_inexact(self):
        with pytest.raises(Exception):
            Operation.to_xdr_amount("0.12345678")

    def test_to_xdr_amount_not_number(self):
        with pytest.raises(Exception):
            # in python2.7 it will raise Exception('Invalid literal for Decimal')
            # but in python3, it will raise decimal.InvalidOperation
            Operation.to_xdr_amount("test")

    def test_to_xdr_amount_not_string(self):
        with pytest.raises(
                TypeError, match="value of type 'float' is not a string"):
            Operation.to_xdr_amount(0.1234)

    def test_from_xdr_amount(self):
        assert (Operation.from_xdr_amount(10 ** 7) == "1")
        assert (Operation.from_xdr_amount(20 * 10 ** 7) == "20")
        assert (Operation.from_xdr_amount(1234567) == "0.1234567")
        assert (Operation.from_xdr_amount(112345678) == "11.2345678")


def _load_operations():
    source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
    amount = "1"
    return [
        ("create_account_min", CreateAccount({
            'source': source, 'destination': dest,
            'starting_balance': amount
        })),
        ("payment_min", Payment({
            'source': source, 'destination': dest,
            'asset': Asset.native(), 'amount': amount,
        })),
        ("payment_short_asset", Payment({
            'source': source, 'destination': dest,
            'asset': Asset('USD4', source), 'amount': amount,
        })),
        ("payment_long_asset", Payment({
            'source': source, 'destination': dest,
            'asset': Asset('SNACKS789ABC', source), 'amount': amount,
        })),
        ("path_payment_min", PathPayment({
            'source': source, 'destination': dest,
            'send_asset': Asset.native(), 'dest_asset': Asset.native(),
            'send_max': amount, 'dest_amount': amount, 'path': [],
        })),
        ("allow_trust_short_asset", AllowTrust({
            'source': source, 'trustor': dest, 'asset_code': 'beer',
            'authorize': True,
        })),
        ("allow_trust_long_asset", AllowTrust({
            'source': source, 'trustor': dest,
            'asset_code': 'pocketknives', 'authorize': True,
        })),
        ("manage_offer_min", ManageOffer({
            'selling': Asset('beer', source), 'buying': Asset('beer', dest),
            'amount': "100", 'price': 3.14159, 'offer_id': 1,
        })),
        ("create_passive_offer_min", CreatePassiveOffer({
            'selling': Asset('beer', source), 'buying': Asset('beer', dest),
            'amount': "100", 'price': 3.14159,
        })),
        ("set_options_empty", SetOptions({})),
        ("change_trust_min", ChangeTrust({
            'source': source, 'asset': Asset('beer', dest), 'limit': '100'
        })),
        ("account_merge_min", AccountMerge({
            'source': source, 'destination': dest,
        })),
        ("inflation", Inflation({'source': source})),
        ("manage_data", ManageData({
            'source': source,
            'data_name': '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
            'data_value': source,
        })),
    ]


@pytest.mark.parametrize("name, operation", _load_operations())
def test_operation(name, operation):
    operation_restored = Operation.from_xdr(operation.xdr())
    assert operation == operation_restored
    original = dict(operation.__dict__)
    original.pop("body")
    restored = dict(operation_restored.__dict__)
    restored.pop("body")
    assert original == restored


def test_from_xdr_object_raise():
    operation = mock.MagicMock(type=2561)
    pytest.raises(NotImplementedError, Operation.from_xdr_object, operation)


def test_manage_data_too_long_raises():
    msg = 'Data or value should be <= 64 bytes \(ascii encoded\).'
    with pytest.raises(XdrLengthError, match=msg):
        ManageData({
            'data_name': '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
            'data_value': '1234567890' * 7
        })
