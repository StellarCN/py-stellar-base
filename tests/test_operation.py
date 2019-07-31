import pytest
from stellar_sdk.asset import Asset

from stellar_sdk.operation import Operation, CreateAccount
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from stellar_sdk.operation.account_merge import AccountMerge
from stellar_sdk.operation.bump_sequence import BumpSequence
from stellar_sdk.operation.change_trust import ChangeTrust
from stellar_sdk.operation.inflation import Inflation


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