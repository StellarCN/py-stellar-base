import pytest
from stellar_sdk.hashing import hash256

from stellar_sdk.asset import Asset

from stellar_sdk.operation import Operation, CreateAccount
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from stellar_sdk.operation.account_merge import AccountMerge
from stellar_sdk.operation.allow_trust import AllowTrust
from stellar_sdk.operation.bump_sequence import BumpSequence
from stellar_sdk.operation.change_trust import ChangeTrust
from stellar_sdk.operation.inflation import Inflation
from stellar_sdk.operation.manage_data import ManageData
from stellar_sdk.operation.path_payment import PathPayment
from stellar_sdk.operation.payment import Payment
from stellar_sdk.operation.set_options import SetOptions


class TestBaseOperation:

    @pytest.mark.parametrize('origin_amount, expect_value', [
        ('10', 100000000),
        ('0.10', 1000000),
        ('0.1234567', 1234567),
        ('922337203685.4775807', 9223372036854775807)
    ])
    def test_to_xdr_amount(self, origin_amount, expect_value):
        assert Operation.to_xdr_amount(origin_amount) == expect_value

    @pytest.mark.parametrize('origin_amount, exception, reason', [
        (10, TypeError, "Value of type '{}' must be of type String, but got {}.".format(10, type(10))),
        ('-0.1', ValueError,
         "Value of '-0.1' must represent a positive number and the max valid value is 9223372036854775807."),
        ('9223372036854775808', ValueError,
         "Value of '9223372036854775808' must represent a positive number and the max valid value is 9223372036854775807."),
        ('0.123456789', ValueError, "Value of '0.123456789' must have at most 7 digits after the decimal."),

    ])
    def test_to_xdr_amount_raise(self, origin_amount, exception, reason):
        with pytest.raises(exception, match=reason):
            assert Operation.to_xdr_amount(origin_amount)

    @pytest.mark.parametrize('origin_amount, expect_value', [
        (100000000, '10'),
        (1000000, '0.1'),
        (1234567, '0.1234567'),
        (9223372036854775807, '922337203685.4775807')
    ])
    def test_from_xdr_amount(self, origin_amount, expect_value):
        assert Operation.from_xdr_amount(origin_amount) == expect_value

    def test_get_source_exist_from_xdr_obj(self):  # BAD TEST
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source == source
        assert op.starting_balance == '1000'
        assert op.destination == destination

    def test_get_source_no_exist_from_xdr_obj(self):  # BAD TEST
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        origin_op = CreateAccount(destination, starting_balance)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source == None
        assert op.starting_balance == '1000'
        assert op.destination == destination


class TestCreateAccount:
    def test_to_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        op = CreateAccount(destination, starting_balance, source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAA' \
                                              b'AAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAACVAvkAA=='

    def test_to_xdr_obj_without_source(self):
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        op = CreateAccount(destination, starting_balance)
        assert op.to_xdr_object().to_xdr() == b'AAAAAAAAAAAAAAAAiZsoQO1WNsVt3F8Usjl' \
                                              b'1958bojiNJpTkxW7N3clg5e8AAAACVAvkAA=='

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID'
        starting_balance = '1000.00'
        op = CreateAccount(destination, starting_balance)
        with pytest.raises(Ed25519PublicKeyInvalidError, match='Invalid Ed25519 Public Key: {}'.format(destination)):
            op.to_xdr_object().to_xdr()

    def test_to_xdr_obj_with_invalid_source_raise(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLINVALID'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        op = CreateAccount(destination, starting_balance, source)
        with pytest.raises(Ed25519PublicKeyInvalidError, match='Invalid Ed25519 Public Key: {}'.format(source)):
            op.to_xdr_object().to_xdr()

    def test_to_xdr_obj_with_invalid_starting_balance_raise(self):
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '-1'
        op = CreateAccount(destination, starting_balance)
        with pytest.raises(ValueError, match="Value of '{}' must represent a positive number and "
                                             "the max valid value is 9223372036854775807.".format(starting_balance)):
            op.to_xdr_object()

    def test_from_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        starting_balance = '1000.00'
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source == source
        assert op.starting_balance == '1000'
        assert op.destination == destination


class TestBumpSequence:
    def test_to_xdr_obj(self):
        bump_to = 114514
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'

        op = BumpSequence(bump_to, source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAsAAAAAAAG/Ug=='

    def test_from_xdr_obj(self):
        bump_to = 123123123
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        origin_xdr_obj = BumpSequence(bump_to, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, BumpSequence)
        assert op.source == source
        assert op.bump_to == bump_to


class TestInflation:
    def test_to_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        op = Inflation(source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAk='

    def test_from_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        origin_xdr_obj = Inflation(source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Inflation)
        assert op.source == source


class TestAccountMerge:
    def test_to_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        op = AccountMerge(destination, source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAgAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8='

    def test_from_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AccountMerge)
        assert op.source == source
        assert op.destination == destination


class TestChangeTrust:
    @pytest.mark.parametrize('limit, xdr', [
        ("922337203685.4775807",
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9e3//////////'),
        ("0",
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAAAAAAA'),
        ("50.1234567",
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAAd4DuH'),
        (None,
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9e3//////////')
    ])
    def test_to_xdr_obj(self, limit, xdr):
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        op = ChangeTrust(asset, limit, source)
        assert op.to_xdr_object().to_xdr() == xdr

    def test_from_xdr_obj(self):
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        limit = '123456.789'
        origin_xdr_obj = ChangeTrust(asset, limit, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, ChangeTrust)
        assert op.source == source
        assert op.limit == limit
        assert op.asset == asset


class TestPayment:
    def test_to_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        amount = '1000.0000000'
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        op = Payment(destination, asset, amount, source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAEAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAJUC+QA'

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZW'
        amount = '1000.0000000'
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        op = Payment(destination, asset, amount, source)
        with pytest.raises(Ed25519PublicKeyInvalidError):
            op.to_xdr_object()

    def test_to_xdr_obj_with_invalid_amount_raise(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        amount = 1
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        op = Payment(destination, asset, amount, source)
        with pytest.raises(TypeError):
            op.to_xdr_object()

    def test_from_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        amount = '1000.0000000'
        asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Payment)
        assert op.source == source
        assert op.destination == destination
        assert op.amount == '1000'
        assert op.asset == asset


class TestPathPayment:
    def test_to_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        send_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        dest_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        send_max = '3.0070000'
        dest_amount = '3.1415000'
        path = [Asset('USD', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB'),
                Asset('EUR', 'GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL')]
        op = PathPayment(destination, send_asset, send_max, dest_asset, dest_amount, path, source)
        assert op.to_xdr_object().to_xdr() == b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAIAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAABytTwAAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAAVVTRAAAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAAAAd9a2AAAAAIAAAABVVNEAAAAAABCzwVZeQ9sO2TeFRIN8Lslyqt9wttPtKGKNeiBvzI69wAAAAFFVVIAAAAAAObbxW5I9YIF6lfUJkfp3sADdrm5wJmdBv78Py6kKta1'

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZW'
        send_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        dest_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        send_max = '3.0070000'
        dest_amount = '3.1415000'
        path = [Asset('USD', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB'),
                Asset('EUR', 'GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL')]
        op = PathPayment(destination, send_asset, send_max, dest_asset, dest_amount, path, source)
        with pytest.raises(Ed25519PublicKeyInvalidError):
            op.to_xdr_object()

    # TODO
    # def test_to_xdr_obj_with_invalid_amount_raise(self):
    #     pass

    def test_from_xdr_obj(self):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        destination = 'GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ'
        send_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        dest_asset = Asset('USD', 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7')
        send_max = '3.0070000'
        dest_amount = '3.1415000'
        path = [Asset('USD', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB'),
                Asset('EUR', 'GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL')]
        origin_xdr_obj = PathPayment(destination, send_asset, send_max, dest_asset, dest_amount, path,
                                     source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, PathPayment)
        assert op.source == source
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_max == '3.007'
        assert op.dest_amount == '3.1415'
        assert op.path == path


class TestAllowTrust:
    @pytest.mark.parametrize('authorize, xdr', [
        (True,
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAE='),
        (False,
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAA=')])
    def test_to_xdr_obj(self, authorize, xdr):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        trustor = 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7'
        asset_code = 'USD'
        op = AllowTrust(trustor, asset_code, authorize, source)
        assert op.to_xdr_object().to_xdr() == xdr

    @pytest.mark.parametrize('asset_code, authorize', [
        ('USD', True),
        ('USDT', False),
        ('Banana', True),
        ("STELLAROVERC", False)])
    def test_from_xdr_obj(self, asset_code, authorize):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        trustor = 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7'
        origin_xdr_obj = AllowTrust(trustor, asset_code, authorize, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AllowTrust)
        assert op.source == source
        assert op.trustor == trustor
        assert op.asset_code == asset_code
        assert op.authorize == authorize


class TestManageData:
    @pytest.mark.parametrize('name, value, xdr', [
        ('add_data', 'value',
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAIYWRkX2RhdGEAAAABAAAABXZhbHVlAAAA'),
        ('remove_data', None,
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAALcmVtb3ZlX2RhdGEAAAAAAA=='),
        ('add_bytes_data', b'bytes_value',
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAOYWRkX2J5dGVzX2RhdGEAAAAAAAEAAAALYnl0ZXNfdmFsdWUA'),
        ('add_data_中文', '恒星',
         b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAPYWRkX2RhdGFf5Lit5paHAAAAAAEAAAAG5oGS5pifAAA=')
    ])
    def test_to_xdr_obj(self, name, value, xdr):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        op = ManageData(name, value, source)
        assert op.to_xdr_object().to_xdr() == xdr

    @pytest.mark.parametrize('name, value', [
        ('name_too_long' + '-' * 64, 'value'),
        ('value_too_long', 'value' + 'a' * 64),
    ])
    def test_to_xdr_obj_with_invalid_value_raise(self, name, value):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        with pytest.raises(ValueError, match=r'Data and value should be <= 64 bytes \(ascii encoded\).'):
            ManageData(name, value, source)

    @pytest.mark.parametrize('name, value', [
        ('add_data', 'value'),
        ('remove_data', None),
        ('add_bytes_data', b'bytes_value'),
        ('add_data_中文', '恒星')
    ])
    def test_from_xdr_obj(self, name, value):
        source = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        origin_xdr_obj = ManageData(name, value, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, ManageData)
        assert op.source == source
        assert op.name == name
        if isinstance(value, str):
            value = value.encode()
        assert op.value == value


class TestSetOptions:
    def test_auth_flags_set_correctly(self):
        assert SetOptions.AuthFlag.AUTHORIZATION_REQUIRED == 1
        assert SetOptions.AuthFlag.AUTHORIZATION_REVOCABLE == 2
        assert SetOptions.AuthFlag.AUTHORIZATION_IMMUTABLE == 4

    def test_signer_type_flags_set_correctly(self):
        assert SetOptions.SignerType.ED25519_PUBLIC_KEY.value == 'ed25519_public_key'
        assert SetOptions.SignerType.SHA256_HASH.value == 'sha256_hash'
        assert SetOptions.SignerType.PRE_AUTH_TX.value == 'pre_auth_tx'

    @pytest.mark.parametrize(
        'inflation_dest, clear_flags, set_flags, master_weight, low_threshold, med_threshold, high_threshold, home_domain, signer_type, signer_key, signer_weight, source, xdr',
        [
            ('GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7',
             SetOptions.AuthFlag.AUTHORIZATION_REVOCABLE | SetOptions.AuthFlag.AUTHORIZATION_IMMUTABLE,
             SetOptions.AuthFlag.AUTHORIZATION_REQUIRED, 0, 1, 2, 3, 'www.example.com',
             SetOptions.SignerType.ED25519_PUBLIC_KEY, 'GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7', 1,
             None,
             b'AAAAAAAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAYAAAABAAAAAQAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAgAAAAEAAAADAAAAAQAAAA93d3cuZXhhbXBsZS5jb20AAAAAAQAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAE='),
            ('GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7',
             SetOptions.AuthFlag.AUTHORIZATION_REQUIRED | SetOptions.AuthFlag.AUTHORIZATION_REVOCABLE,
             SetOptions.AuthFlag.AUTHORIZATION_REVOCABLE, 3, 2, 4, 6, None,
             SetOptions.SignerType.PRE_AUTH_TX, hash256(b"PRE_AUTH_TX"), 2,
             'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV',
             b'AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAMAAAABAAAAAgAAAAEAAAADAAAAAQAAAAIAAAABAAAABAAAAAEAAAAGAAAAAAAAAAEAAAAB96nlNnQ/Aq5uCbYXnGJN/EXa76Y2RQP6S1wP8lOEL1UAAAAC'),
            (None, None, None, 0, 255, 255, 255, 'overcat.me', SetOptions.SignerType.SHA256_HASH,
             hash256(b"SHA256_HASH"), 0, None,
             b'AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAD/AAAAAQAAAP8AAAABAAAA/wAAAAEAAAAKb3ZlcmNhdC5tZQAAAAAAAQAAAALB1I1O+GEAV87X3eYN/uAYDIDzP5mY4SVTEQFFYFq6nwAAAAA='),
            (None, None, None, None, None, None, None, None, None, None, None, None,
             b'AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='),

        ])
    def test_to_xdr(self, inflation_dest, clear_flags, set_flags, master_weight, low_threshold, med_threshold,
                    high_threshold, home_domain, signer_type, signer_key, signer_weight, source, xdr):
        op = SetOptions(inflation_dest,
                        clear_flags,
                        set_flags,
                        master_weight,
                        low_threshold,
                        med_threshold,
                        high_threshold,
                        signer_type,
                        signer_key,
                        signer_weight,
                        home_domain,
                        source)
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_ins = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_ins, SetOptions)
        assert from_ins.source == source
        assert from_ins.clear_flags == clear_flags
        assert from_ins.set_flags == set_flags
        assert from_ins.master_weight == master_weight
        assert from_ins.low_threshold == low_threshold
        assert from_ins.med_threshold == med_threshold
        assert from_ins.high_threshold == high_threshold
        assert from_ins.signer_type == signer_type
        assert from_ins.signer_key == signer_key
        assert from_ins.signer_weight == signer_weight
        assert from_ins.home_domain == home_domain

    @pytest.mark.parametrize('signer_type, signer_key, signer_weight', [
        (SetOptions.SignerType.ED25519_PUBLIC_KEY, 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV', None),
        (SetOptions.SignerType.ED25519_PUBLIC_KEY, None, 1),
        (None, 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV', 1),

    ])
    def test_to_xdr_with_invalid_signer_arguments_raise(self, signer_type, signer_key, signer_weight):
        with pytest.raises(ValueError, match="If you want to set up signer, you must provide signer_type, signer_key and signer_weight."):
            SetOptions(signer_type=signer_type, signer_key=signer_key, signer_weight=signer_weight)

    def test_to_xdr_with_invalid_signer_type_raise(self):
        signer_type = 'BAD_TYPE'
        signer_key = 'GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV'
        signer_weight = 1

        with pytest.raises(ValueError,
                           match='Invalid signer type, sign_type should be SetOptions.SignerType.ED25519_PUBLIC_KEY, '
                                 'SetOptions.SHA256_HASH.ED25519_PUBLIC_KEY or SetOptions.SignerType.PRE_AUTH_TX'):
            SetOptions(signer_type=signer_type, signer_key=signer_key, signer_weight=signer_weight)

