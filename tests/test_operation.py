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


class TestOp:
    source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
    dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
    amount = "1"

    def test_from_xdr_object_raise(self):
        operation = mock.MagicMock(type=2561)
        pytest.raises(NotImplementedError, Operation.from_xdr_object, operation)

    def test_createAccount_min(self):
        op = CreateAccount({
            'source': self.source,
            'destination': self.dest,
            'starting_balance': self.amount
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest
        assert op_x.starting_balance == self.amount

    def test_payment_min(self):
        op = Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset.native(),
            'amount': self.amount,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest
        assert op_x.asset == Asset.native()
        assert op_x.amount == self.amount

    def test_payment_short_asset(self):
        op = Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset('USD4', self.source),
            'amount': self.amount,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest
        assert op_x.asset == Asset('USD4', self.source)
        assert op_x.amount == self.amount

    def test_payment_long_asset(self):
        op = Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset('SNACKS789ABC', self.source),
            'amount': self.amount,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest
        assert op_x.asset == Asset('SNACKS789ABC', self.source)
        assert op_x.amount == self.amount

    def test_pathPayment_min(self):
        op = PathPayment({
            'source': self.source,
            'destination': self.dest,
            'send_asset': Asset.native(),
            'dest_asset': Asset.native(),
            'send_max': self.amount,
            'dest_amount': self.amount,
            'path': [],
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest
        assert op_x.send_asset == Asset.native()
        assert op_x.dest_asset == Asset.native()
        assert op_x.send_max == self.amount
        assert op_x.dest_amount == self.amount
        assert op_x.path == []

    def test_manageOffer_min(self):
        op = ManageOffer({
            'selling': Asset('beer', self.source),
            'buying': Asset('beer', self.dest),
            'amount': "100",
            'price': 3.14159,
            'offer_id': 1,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == None
        assert op_x.selling == Asset('beer', self.source)
        assert op_x.buying == Asset('beer', self.dest)
        assert op_x.amount == "100"
        assert op_x.price == 3.14159
        assert op_x.offer_id == 1

    def test_createPassiveOffer_min(self):
        op = CreatePassiveOffer({
            'selling': Asset('beer', self.source),
            'buying': Asset('beer', self.dest),
            'amount': "100",
            'price': 3.14159,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == None
        assert op_x.selling == Asset('beer', self.source)
        assert op_x.buying == Asset('beer', self.dest)
        assert op_x.amount == "100"
        assert op_x.price == 3.14159

    def test_SetOptions_empty(self):
        op = SetOptions({})
        assert op == Operation.from_xdr(op.xdr())

    def test_changeTrust_min(self):
        op = ChangeTrust({
            'source': self.source,
            'asset': Asset('beer', self.dest),
            'limit': '100'
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.line == Asset('beer', self.dest)
        assert op_x.limit == '100'

    def test_allowTrust_shortAsset(self):
        op = AllowTrust({
            'source': self.source,
            'trustor': self.dest,
            'asset_code': 'beer',
            'authorize': True,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.trustor == self.dest
        assert op_x.asset_code == 'beer'
        assert op_x.authorize == True

    def test_allowTrust_longAsset(self):
        op = AllowTrust({
            'source': self.source,
            'trustor': self.dest,
            'asset_code': 'pocketknives',
            'authorize': True,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.trustor == self.dest
        assert op_x.asset_code == 'pocketknives'
        assert op_x.authorize == True

    def test_accountMerge_min(self):
        op = AccountMerge({
            'source': self.source,
            'destination': self.dest,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.destination == self.dest

    def test_inflation(self):
        op = Inflation({
            'source': self.source,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source

    def test_manage_data(self):
        op = ManageData({
            'source': self.source,
            'data_name': '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
            'data_value': self.source,
        })
        op_x = Operation.from_xdr(op.xdr())
        assert op == op_x
        assert op_x.source == self.source
        assert op_x.data_name == '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY'
        assert op_x.data_value == self.source

    def test_manage_data_toolong(self):
        with pytest.raises(XdrLengthError, match='Data or value should be <= 64 bytes \(ascii encoded\).'):
            ManageData({
                'data_name': '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
                'data_value': '1234567890' * 7
            })
