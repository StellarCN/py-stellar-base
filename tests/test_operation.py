# coding:utf-8
import sys
import decimal
import mock
import pytest

from stellar_base.operation import *
from stellar_base.asset import Asset


@pytest.mark.parametrize("s, error_type", [
    ("0.12345678", decimal.Inexact),
    ("test", decimal.InvalidOperation),
    (0.1234, TypeError),
])
def test_to_xdr_amount_raise(s, error_type):
    if sys.version_info.major == 2:
        error_type = Exception
    with pytest.raises(error_type):
        Operation.to_xdr_amount(s)


@pytest.mark.parametrize("num, s", [
    (10 ** 7, "1"),
    (20 * 10 ** 7, "20"),
    (1234567, "0.1234567"),
    (112345678, "11.2345678"),
])
def test_from_and_to_xdr_amount(num, s):
    assert s == Operation.from_xdr_amount(num)
    assert num == Operation.to_xdr_amount(s)


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
        ("change_trust_default_limit", ChangeTrust({
            'source': source, 'asset': Asset('beer', dest)
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
