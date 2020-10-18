import base64
from decimal import Decimal

import pytest
from stellar_sdk.operation.claim_claimable_balance import ClaimClaimableBalance

from stellar_sdk import Price, Asset, Keypair
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, AssetCodeInvalidError
from stellar_sdk.operation import Operation, CreateAccount
from stellar_sdk.operation.create_claimable_balance import *
from stellar_sdk.operation.account_merge import AccountMerge
from stellar_sdk.operation.allow_trust import AllowTrust, TrustLineEntryFlag
from stellar_sdk.operation.begin_sponsoring_future_reserves import (
    BeginSponsoringFutureReserves,
)
from stellar_sdk.operation.bump_sequence import BumpSequence
from stellar_sdk.operation.change_trust import ChangeTrust
from stellar_sdk.operation.create_passive_sell_offer import CreatePassiveSellOffer
from stellar_sdk.operation.end_sponsoring_future_reserves import (
    EndSponsoringFutureReserves,
)
from stellar_sdk.operation.inflation import Inflation
from stellar_sdk.operation.manage_buy_offer import ManageBuyOffer
from stellar_sdk.operation.manage_data import ManageData
from stellar_sdk.operation.manage_sell_offer import ManageSellOffer
from stellar_sdk.operation.path_payment import PathPayment
from stellar_sdk.operation.path_payment_strict_receive import PathPaymentStrictReceive
from stellar_sdk.operation.path_payment_strict_send import PathPaymentStrictSend
from stellar_sdk.operation.payment import Payment
from stellar_sdk.operation.set_options import SetOptions, Flag
from stellar_sdk.operation.revoke_sponsorship import RevokeSponsorship
from stellar_sdk.operation.utils import (
    check_price,
    check_amount,
    check_source,
    check_asset_code,
    check_ed25519_public_key,
)
from stellar_sdk.signer import Signer
from stellar_sdk.signer_key import SignerKey
from stellar_sdk.utils import sha256
from stellar_sdk import xdr as stellar_xdr


class TestBaseOperation:
    @pytest.mark.parametrize(
        "origin_amount, expect_value",
        [
            ("10", 100000000),
            ("0.10", 1000000),
            ("0.1234567", 1234567),
            ("922337203685.4775807", 9223372036854775807),
        ],
    )
    def test_to_xdr_amount(self, origin_amount, expect_value):
        assert Operation.to_xdr_amount(origin_amount) == expect_value

    @pytest.mark.parametrize(
        "origin_amount, exception, reason",
        [
            (
                10,
                TypeError,
                "Value of type '{}' must be of type {} or {}, but got {}.".format(
                    10, str, Decimal, type(10)
                ),
            ),
            (
                "-0.1",
                ValueError,
                "Value of '-0.1' must represent a positive number and the max valid value is 922337203685.4775807.",
            ),
            (
                "922337203685.4775808",
                ValueError,
                "Value of '922337203685.4775808' must represent a positive number and the max valid value is 922337203685.4775807.",
            ),
            (
                "0.123456789",
                ValueError,
                "Value of '0.123456789' must have at most 7 digits after the decimal.",
            ),
        ],
    )
    def test_to_xdr_amount_raise(self, origin_amount, exception, reason):
        with pytest.raises(exception, match=reason):
            Operation.to_xdr_amount(origin_amount)

    @pytest.mark.parametrize(
        "origin_amount, expect_value",
        [
            (100000000, "10"),
            (1000000, "0.1"),
            (1234567, "0.1234567"),
            (9223372036854775807, "922337203685.4775807"),
        ],
    )
    def test_from_xdr_amount(self, origin_amount, expect_value):
        assert Operation.from_xdr_amount(origin_amount) == expect_value

    def test_get_source_no_exist_from_xdr_obj(self):  # BAD TEST
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        origin_op = CreateAccount(destination, starting_balance)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source is None
        assert op._source_muxed is None
        assert op.starting_balance == "1000"
        assert op.destination == destination

    def test_equal(self):
        op1 = ManageData("a", "b")
        op2 = ManageData("a", "b")
        op3 = ManageData("A", "B")
        op4 = "BAD TYEE"
        assert op1 == op2 != op3 != op4

    def test_get_source_muxed_from_xdr_obj(self):  # BAD TEST
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        source = "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"
        source2 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        starting_balance = "1000.00"
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        assert op.source == source
        assert (
            op._source_muxed.to_xdr()
            == Keypair.from_public_key(source).xdr_muxed_account().to_xdr()
        )
        op.source = source2
        assert op.source == source2
        assert op._source_muxed is None


class TestCreateAccount:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        op = CreateAccount(destination, starting_balance, source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAA"
            "AAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAACVAvkAA=="
        )

    def test_to_xdr_obj_without_source(self):
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        op = CreateAccount(destination, starting_balance)
        assert (
            op.to_xdr_object().to_xdr() == "AAAAAAAAAAAAAAAAiZsoQO1WNsVt3F8Usjl"
            "1958bojiNJpTkxW7N3clg5e8AAAACVAvkAA=="
        )

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        starting_balance = "1000.00"
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(destination),
        ):
            CreateAccount(destination, starting_balance)

    def test_to_xdr_obj_with_invalid_source_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLINVALID"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(source),
        ):
            CreateAccount(destination, starting_balance, source)

    def test_to_xdr_obj_with_invalid_starting_balance_raise(self):
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "-1"
        with pytest.raises(
            ValueError,
            match="Value of '{}' must represent a positive number and "
            "the max valid value is 922337203685.4775807.".format(starting_balance),
        ):
            CreateAccount(destination, starting_balance)

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source == source
        assert op.starting_balance == "1000"
        assert op.destination == destination


class TestBumpSequence:
    def test_to_xdr_obj(self):
        bump_to = 114514
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"

        op = BumpSequence(bump_to, source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAsAAAAAAAG/Ug=="
        )

    def test_from_xdr_obj(self):
        bump_to = 123123123
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        origin_xdr_obj = BumpSequence(bump_to, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, BumpSequence)
        assert op.source == source
        assert op.bump_to == bump_to


class TestInflation:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        op = Inflation(source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAk="
        )

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        origin_xdr_obj = Inflation(source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Inflation)
        assert op.source == source


class TestAccountMerge:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        op = AccountMerge(destination, source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAgAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8="
        )

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AccountMerge)
        assert op.source == source
        assert op.destination == destination

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination2 = "GBL3NR5XNBNFAYVQMZ7R6RMUKLMGRUHNIYDYMEUPANQV6OROQXSDZYHV"
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        restore_op = AccountMerge.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        assert (
            restore_op._destination_muxed.to_xdr()
            == Keypair.from_public_key(destination).xdr_muxed_account().to_xdr()
        )
        restore_op.destination = destination2
        assert restore_op._destination_muxed is None
        assert restore_op.destination == destination2


class TestChangeTrust:
    @pytest.mark.parametrize(
        "limit, xdr",
        [
            (
                "922337203685.4775807",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9e3//////////",
            ),
            (
                "0",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAAAAAAA",
            ),
            (
                "50.1234567",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAAd4DuH",
            ),
            (
                None,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9e3//////////",
            ),
        ],
    )
    def test_to_xdr_obj(self, limit, xdr):
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        op = ChangeTrust(asset, limit, source)
        assert op.to_xdr_object().to_xdr() == xdr

    def test_from_xdr_obj(self):
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        limit = "123456.789"
        origin_xdr_obj = ChangeTrust(asset, limit, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, ChangeTrust)
        assert op.source == source
        assert op.limit == limit
        assert op.asset == asset


class TestClaimClaimableBalance:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        op = ClaimClaimableBalance(balance_id=balance_id, source=source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAA8AAAAA2g1X2n1IUOf8ENKp0OvHMfevtAV0wDOVsX1JFJuR9b4="
        )

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        origin_xdr_obj = ClaimClaimableBalance(
            balance_id=balance_id, source=source
        ).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, ClaimClaimableBalance)
        assert op.source == source
        assert op.balance_id == balance_id


class TestPayment:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        op = Payment(destination, asset, amount, source)
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAEAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAJUC+QA"
        )

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZW"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        with pytest.raises(ValueError):
            Payment(destination, asset, amount, source)

    def test_to_xdr_obj_with_invalid_amount_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        amount = 1
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        with pytest.raises(TypeError):
            Payment(destination, asset, amount, source)

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Payment)
        assert op.source == source
        assert op.destination == destination
        assert op.amount == "1000"
        assert op.asset == asset

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination2 = "GBL3NR5XNBNFAYVQMZ7R6RMUKLMGRUHNIYDYMEUPANQV6OROQXSDZYHV"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        restore_op = Payment.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        assert (
            restore_op._destination_muxed.to_xdr()
            == Keypair.from_public_key(destination).xdr_muxed_account().to_xdr()
        )
        restore_op.destination = destination2
        assert restore_op._destination_muxed is None
        assert restore_op.destination == destination2


class TestPathPayment:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        op = PathPayment(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        )
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAIAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAABytTwAAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAAVVTRAAAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAAAAd9a2AAAAAIAAAABVVNEAAAAAABCzwVZeQ9sO2TeFRIN8Lslyqt9wttPtKGKNeiBvzI69wAAAAFFVVIAAAAAAObbxW5I9YIF6lfUJkfp3sADdrm5wJmdBv78Py6kKta1"
        )

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZW"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        with pytest.raises(ValueError):
            PathPayment(
                destination, send_asset, send_max, dest_asset, dest_amount, path, source
            )

    # TODO
    # def test_to_xdr_obj_with_invalid_amount_raise(self):
    #     pass

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        origin_xdr_obj = PathPayment(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        ).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, PathPaymentStrictReceive)
        assert op.source == source
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_max == "3.007"
        assert op.dest_amount == "3.1415"
        assert op.path == path


class TestPathPaymentStrictReceive:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        op = PathPaymentStrictReceive(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        )
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAIAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAABytTwAAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAAVVTRAAAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAAAAd9a2AAAAAIAAAABVVNEAAAAAABCzwVZeQ9sO2TeFRIN8Lslyqt9wttPtKGKNeiBvzI69wAAAAFFVVIAAAAAAObbxW5I9YIF6lfUJkfp3sADdrm5wJmdBv78Py6kKta1"
        )

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZW"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        with pytest.raises(ValueError):
            PathPaymentStrictReceive(
                destination, send_asset, send_max, dest_asset, dest_amount, path, source
            )

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        origin_xdr_obj = PathPaymentStrictReceive(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        ).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, PathPaymentStrictReceive)
        assert op.source == source
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_max == "3.007"
        assert op.dest_amount == "3.1415"
        assert op.path == path

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination2 = "GBL3NR5XNBNFAYVQMZ7R6RMUKLMGRUHNIYDYMEUPANQV6OROQXSDZYHV"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_max = "3.0070000"
        dest_amount = "3.1415000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        origin_xdr_obj = PathPaymentStrictReceive(
            destination, send_asset, send_max, dest_asset, dest_amount, path, source
        ).to_xdr_object()
        restore_op = PathPaymentStrictReceive.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        assert (
            restore_op._destination_muxed.to_xdr()
            == Keypair.from_public_key(destination).xdr_muxed_account().to_xdr()
        )
        restore_op.destination = destination2
        assert restore_op._destination_muxed is None
        assert restore_op.destination == destination2


class TestPathPaymentStrictSend:
    def test_to_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_amount = "3.1415000"
        dest_min = "3.0070000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        op = PathPaymentStrictSend(
            destination, send_asset, send_amount, dest_asset, dest_min, path, source
        )
        assert (
            op.to_xdr_object().to_xdr()
            == "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAA0AAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAAB31rYAAAAAImbKEDtVjbFbdxfFLI5dfefG6I4jSaU5MVuzd3JYOXvAAAAAVVTRAAAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAAAAcrU8AAAAAIAAAABVVNEAAAAAABCzwVZeQ9sO2TeFRIN8Lslyqt9wttPtKGKNeiBvzI69wAAAAFFVVIAAAAAAObbxW5I9YIF6lfUJkfp3sADdrm5wJmdBv78Py6kKta1"
        )

    def test_to_xdr_obj_with_invalid_destination_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZW"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_amount = "3.1415000"
        dest_min = "3.0070000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        with pytest.raises(ValueError):
            PathPaymentStrictSend(
                destination, send_asset, send_amount, dest_asset, dest_min, path, source
            )

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_amount = "3.1415000"
        dest_min = "3.0070000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        origin_xdr_obj = PathPaymentStrictSend(
            destination, send_asset, send_amount, dest_asset, dest_min, path, source
        ).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, PathPaymentStrictSend)
        assert op.source == source
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_amount == "3.1415"
        assert op.dest_min == "3.007"
        assert op.path == path

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination2 = "GBL3NR5XNBNFAYVQMZ7R6RMUKLMGRUHNIYDYMEUPANQV6OROQXSDZYHV"
        send_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        dest_asset = Asset(
            "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        )
        send_amount = "3.1415000"
        dest_min = "3.0070000"
        path = [
            Asset("USD", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB"),
            Asset("EUR", "GDTNXRLOJD2YEBPKK7KCMR7J33AAG5VZXHAJTHIG736D6LVEFLLLKPDL"),
        ]
        origin_xdr_obj = PathPaymentStrictSend(
            destination, send_asset, send_amount, dest_asset, dest_min, path, source
        ).to_xdr_object()
        restore_op = PathPaymentStrictSend.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        assert (
            restore_op._destination_muxed.to_xdr()
            == Keypair.from_public_key(destination).xdr_muxed_account().to_xdr()
        )
        restore_op.destination = destination2
        assert restore_op._destination_muxed is None
        assert restore_op.destination == destination2


class TestAllowTrust:
    @pytest.mark.parametrize(
        "authorize, xdr",
        [
            (
                True,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAE=",
            ),
            (
                False,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAA=",
            ),
            (
                TrustLineEntryFlag.AUTHORIZED_FLAG,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAE=",
            ),
            (
                TrustLineEntryFlag.UNAUTHORIZED_FLAG,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAA=",
            ),
            (
                TrustLineEntryFlag.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAcAAAAAzU64DztfTtBLJ2I0nN998lhiyhFcS8rtZHyowijs/XsAAAABVVNEAAAAAAI=",
            ),
        ],
    )
    def test_to_xdr_obj(self, authorize, xdr):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        trustor = "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        asset_code = "USD"
        op = AllowTrust(trustor, asset_code, authorize, source)
        assert op.to_xdr_object().to_xdr() == xdr

    @pytest.mark.parametrize(
        "asset_code, authorize",
        [
            ("USD", TrustLineEntryFlag.AUTHORIZED_FLAG),
            ("USDT", TrustLineEntryFlag.UNAUTHORIZED_FLAG),
            ("Banana", TrustLineEntryFlag.AUTHORIZED_FLAG),
            ("STELLAROVERC", TrustLineEntryFlag.UNAUTHORIZED_FLAG),
        ],
    )
    def test_from_xdr_obj(self, asset_code, authorize):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        trustor = "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
        origin_xdr_obj = AllowTrust(
            trustor, asset_code, authorize, source
        ).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AllowTrust)
        assert op.source == source
        assert op.trustor == trustor
        assert op.asset_code == asset_code
        assert op.authorize == authorize


class TestManageData:
    @pytest.mark.parametrize(
        "name, value, xdr",
        [
            (
                "add_data",
                "value",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAIYWRkX2RhdGEAAAABAAAABXZhbHVlAAAA",
            ),
            (
                "remove_data",
                None,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAALcmVtb3ZlX2RhdGEAAAAAAA==",
            ),
            (
                "add_bytes_data",
                b"bytes_value",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAOYWRkX2J5dGVzX2RhdGEAAAAAAAEAAAALYnl0ZXNfdmFsdWUA",
            ),
            (
                "add_data_中文",
                "恒星",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAoAAAAPYWRkX2RhdGFf5Lit5paHAAAAAAEAAAAG5oGS5pifAAA=",
            ),
        ],
    )
    def test_to_xdr_obj(self, name, value, xdr):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        op = ManageData(name, value, source)
        assert op.to_xdr_object().to_xdr() == xdr

    @pytest.mark.parametrize(
        "name, value",
        [("name_too_long" + "-" * 64, "value"), ("value_too_long", "value" + "a" * 64)],
    )
    def test_to_xdr_obj_with_invalid_value_raise(self, name, value):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        with pytest.raises(
            ValueError, match=r"Data and value should be <= 64 bytes \(ascii encoded\)."
        ):
            ManageData(name, value, source)

    @pytest.mark.parametrize(
        "name, value",
        [
            ("add_data", "value"),
            ("remove_data", None),
            ("add_bytes_data", "bytes_value"),
            ("add_data_中文", "恒星"),
        ],
    )
    def test_from_xdr_obj(self, name, value):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        origin_xdr_obj = ManageData(name, value, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, ManageData)
        assert op.source == source
        assert op.data_name == name
        if isinstance(value, str):
            value = value.encode()
        assert op.data_value == value


class TestSetOptions:
    AUTHORIZATION_REQUIRED = 1
    AUTHORIZATION_REVOCABLE = 2
    AUTHORIZATION_IMMUTABLE = 4

    @pytest.mark.parametrize(
        "inflation_dest, clear_flags, set_flags, master_weight, low_threshold, med_threshold, high_threshold, home_domain, signer, source, xdr",
        [
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                AUTHORIZATION_REVOCABLE | AUTHORIZATION_IMMUTABLE,
                AUTHORIZATION_REQUIRED,
                0,
                1,
                2,
                3,
                "www.example.com",
                Signer.ed25519_public_key(
                    "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7", 1
                ),
                None,
                "AAAAAAAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAYAAAABAAAAAQAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAgAAAAEAAAADAAAAAQAAAA93d3cuZXhhbXBsZS5jb20AAAAAAQAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAE=",
            ),
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                Flag.AUTHORIZATION_REVOCABLE | Flag.AUTHORIZATION_IMMUTABLE,
                Flag.AUTHORIZATION_REQUIRED,
                0,
                1,
                2,
                3,
                "www.example.com",
                Signer.ed25519_public_key(
                    "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7", 1
                ),
                None,
                "AAAAAAAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAYAAAABAAAAAQAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAgAAAAEAAAADAAAAAQAAAA93d3cuZXhhbXBsZS5jb20AAAAAAQAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAE=",
            ),
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                AUTHORIZATION_REQUIRED | AUTHORIZATION_REVOCABLE,
                AUTHORIZATION_REVOCABLE,
                3,
                2,
                4,
                6,
                None,
                Signer.pre_auth_tx(sha256(b"PRE_AUTH_TX"), 2),
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAMAAAABAAAAAgAAAAEAAAADAAAAAQAAAAIAAAABAAAABAAAAAEAAAAGAAAAAAAAAAEAAAAB96nlNnQ/Aq5uCbYXnGJN/EXa76Y2RQP6S1wP8lOEL1UAAAAC",
            ),
            (
                None,
                None,
                None,
                0,
                255,
                255,
                255,
                "overcat.me",
                Signer.sha256_hash(sha256(b"SHA256_HASH"), 0),
                None,
                "AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAD/AAAAAQAAAP8AAAABAAAA/wAAAAEAAAAKb3ZlcmNhdC5tZQAAAAAAAQAAAALB1I1O+GEAV87X3eYN/uAYDIDzP5mY4SVTEQFFYFq6nwAAAAA=",
            ),
            (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
            ),
        ],
    )
    def test_to_xdr(
        self,
        inflation_dest,
        clear_flags,
        set_flags,
        master_weight,
        low_threshold,
        med_threshold,
        high_threshold,
        home_domain,
        signer,
        source,
        xdr,
    ):
        op = SetOptions(
            inflation_dest,
            clear_flags,
            set_flags,
            master_weight,
            low_threshold,
            med_threshold,
            high_threshold,
            signer,
            home_domain,
            source,
        )
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_instance = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_instance, SetOptions)
        assert from_instance.source == source
        assert from_instance.clear_flags == clear_flags
        assert from_instance.set_flags == set_flags
        assert from_instance.master_weight == master_weight
        assert from_instance.low_threshold == low_threshold
        assert from_instance.med_threshold == med_threshold
        assert from_instance.high_threshold == high_threshold
        assert from_instance.signer == signer
        assert from_instance.home_domain == home_domain


class TestManageSellOffer:
    @pytest.mark.parametrize(
        "selling, buying, amount, price, offer_id, source, xdr",
        [
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "3.123456",
                "8.141592",
                1,
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAMAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAAHcmgAAD4djAAHoSAAAAAAAAAAB",
            ),
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "8",
                "238.141592",
                0,
                None,
                "AAAAAAAAAAMAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAATEtAABxjgTAAHoSAAAAAAAAAAA",
            ),
            (
                Asset("XLM"),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "3.123456",
                Price(11, 10),
                1,
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAMAAAAAAAAAAVhDTgAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAAdyaAAAAAAsAAAAKAAAAAAAAAAE=",
            ),
        ],
    )
    def test_to_xdr(self, selling, buying, amount, price, offer_id, source, xdr):
        op = ManageSellOffer(selling, buying, amount, price, offer_id, source)
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_instance = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_instance, ManageSellOffer)
        assert from_instance.source == source
        assert from_instance.buying == buying
        assert from_instance.selling == selling
        assert from_instance.amount == amount
        if not isinstance(price, Price):
            price = Price.from_raw_price(price)
        assert from_instance.price == price
        assert from_instance.offer_id == offer_id


class TestManageBuyOffer:
    @pytest.mark.parametrize(
        "selling, buying, amount, price, offer_id, source, xdr",
        [
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "3.123456",
                "8.141592",
                1,
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAwAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAAHcmgAAD4djAAHoSAAAAAAAAAAB",
            ),
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "8",
                "238.141592",
                0,
                None,
                "AAAAAAAAAAwAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAATEtAABxjgTAAHoSAAAAAAAAAAA",
            ),
            (
                Asset("XLM"),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "3.123456",
                Price(11, 10),
                1,
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAwAAAAAAAAAAVhDTgAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAAAdyaAAAAAAsAAAAKAAAAAAAAAAE=",
            ),
        ],
    )
    def test_to_xdr(self, selling, buying, amount, price, offer_id, source, xdr):
        op = ManageBuyOffer(selling, buying, amount, price, offer_id, source)
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_instance = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_instance, ManageBuyOffer)
        assert from_instance.source == source
        assert from_instance.buying == buying
        assert from_instance.selling == selling
        assert from_instance.amount == amount
        if not isinstance(price, Price):
            price = Price.from_raw_price(price)
        assert from_instance.price == price
        assert from_instance.offer_id == offer_id


class TestCreatePassiveSellOffer:
    @pytest.mark.parametrize(
        "selling, buying, amount, price, source, xdr",
        [
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "11.2782700",
                "3.07",
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAQAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAAa47WwAAAEzAAAAZA==",
            ),
            (
                Asset(
                    "USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7"
                ),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "8.000",
                "238.141592",
                None,
                "AAAAAAAAAAQAAAABVVNEAAAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAFYQ04AAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAATEtAABxjgTAAHoSA==",
            ),
            (
                Asset("XLM"),
                Asset(
                    "XCN", "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
                ),
                "11.2782700",
                Price(453, 4354),
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAQAAAAAAAAAAVhDTgAAAAAAm466+JY4VR3PnqT3QyBxEGuHqw4ts9abdaU4InL3WdgAAAAABrjtbAAAAcUAABEC",
            ),
        ],
    )
    def test_to_xdr(self, selling, buying, amount, price, source, xdr):
        op = CreatePassiveSellOffer(selling, buying, amount, price, source)
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_instance = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_instance, CreatePassiveSellOffer)
        assert from_instance.source == source
        assert from_instance.buying == buying
        assert from_instance.selling == selling
        assert Decimal(from_instance.amount) == Decimal(amount)
        if not isinstance(price, Price):
            price = Price.from_raw_price(price)
        assert from_instance.price == price


class TestOperationUtils:
    def test_check_source(self):
        check_source(None)
        check_source("GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY")

    @pytest.mark.parametrize(
        "source,msg",
        [
            (
                "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RBAD",
                "Invalid Ed25519 Public Key: ",
            ),
            (
                "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHBAD",
                "Invalid Ed25519 Public Key: ",
            ),
        ],
    )
    def test_check_source_raise(self, source, msg):
        with pytest.raises(ValueError, match=msg + source):
            check_source(source)

    def test_check_ed25519_public_key(self):
        check_ed25519_public_key(
            "GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RCNY"
        )

    @pytest.mark.parametrize(
        "source",
        ["GCNY5OXYSY4FKHOPT2SPOQZAOEIGXB5LBYW3HVU3OWSTQITS65M5RBAD", "", " ", 123],
    )
    def test_check_ed25519_public_key_raise(self, source):
        with pytest.raises(
            ValueError, match="Invalid Ed25519 Public Key: {}".format(source)
        ):
            check_ed25519_public_key(source)

    @pytest.mark.parametrize(
        "amount",
        [
            "0",
            "0.0000000",
            "922337203685.4775807",
            "123466",
            Decimal(12),
            Decimal("0.0000000"),
            Decimal("922337203685.4775807"),
            Decimal("123466"),
        ],
    )
    def test_check_amount(self, amount):
        check_amount(amount)

    @pytest.mark.parametrize("amount", [234, Price(12, 34)])
    def test_check_amount_type_raise(self, amount):
        with pytest.raises(
            TypeError, match="amount should be type of {} or {}.".format(str, Decimal)
        ):
            check_amount(amount)

    @pytest.mark.parametrize(
        "amount",
        [
            "-0.1",
            "922337203685.4775808",
            Decimal("-0.1"),
            Decimal("922337203685.4775808"),
        ],
    )
    def test_check_amount_exceed_raise(self, amount):
        with pytest.raises(
            ValueError,
            match="Value of '{}' must represent a positive "
            "number and the max valid value is 922337203685.4775807.".format(amount),
        ):
            check_amount(amount)

    @pytest.mark.parametrize(
        "amount",
        [
            "0.00000000",
            "922337203685.47758001",
            Decimal("0.00000000"),
            Decimal("922337203685.47758001"),
        ],
    )
    def test_check_amount_bad_precision_raise(self, amount):
        with pytest.raises(
            ValueError,
            match="must have at most 7 digits after the decimal.".format(amount),
        ):
            check_amount(amount)

    @pytest.mark.parametrize(
        "price",
        [
            "0",
            "0.0000000",
            "922337203685.4775807",
            "123466",
            Decimal(12),
            Decimal("0.0000000"),
            Decimal("922337203685.4775807"),
            Decimal("123466"),
            Price(1, 2),
        ],
    )
    def test_check_price(self, price):
        check_price(price)

    @pytest.mark.parametrize("price", [234, True])
    def test_check_price_type_raise(self, price):
        with pytest.raises(
            TypeError,
            match="price should be type of {}, {} or {}.".format(str, Decimal, Price),
        ):
            check_price(price)

    @pytest.mark.parametrize(
        "price",
        [
            "-0.1",
            "922337203685.4775808",
            Decimal("-0.1"),
            Decimal("922337203685.4775808"),
        ],
    )
    def test_check_price_exceed_raise(self, price):
        with pytest.raises(
            ValueError,
            match="Value of '{}' must represent a positive "
            "number and the max valid value is 922337203685.4775807.".format(price),
        ):
            check_price(price)

    @pytest.mark.parametrize(
        "price",
        [
            "0.00000000",
            "922337203685.47758001",
            Decimal("0.00000000"),
            Decimal("922337203685.47758001"),
        ],
    )
    def test_check_price_bad_precision_raise(self, price):
        with pytest.raises(
            ValueError,
            match="must have at most 7 digits after the decimal.".format(price),
        ):
            check_price(price)

    @pytest.mark.parametrize("asset_code", ["XLM", "Bananana", "Bananananana"])
    def test_check_asset_code(self, asset_code):
        check_asset_code(asset_code)

    @pytest.mark.parametrize("asset_code", ["", "Banananananan", "XLM-XCN"])
    def test_check_asset_code_raise(self, asset_code):
        with pytest.raises(AssetCodeInvalidError, match="Asset code is invalid"):
            check_asset_code(asset_code)


class TestBeginSponsoringFutureReserves:
    def test_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        sponsored_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABAAAAAAdDis4rHoIOgy4iMcaMGCqgUS7qaIybFyo69Wszj9vBk="
        op = BeginSponsoringFutureReserves(sponsored_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_xdr_no_source(self):
        source = None
        sponsored_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        xdr = "AAAAAAAAABAAAAAAdDis4rHoIOgy4iMcaMGCqgUS7qaIybFyo69Wszj9vBk="
        op = BeginSponsoringFutureReserves(sponsored_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )


class TestEndSponsoringFutureReserves:
    def test_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABE="
        op = EndSponsoringFutureReserves(source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_xdr_no_source(self):
        source = None
        xdr = "AAAAAAAAABE="
        op = EndSponsoringFutureReserves(source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )


class TestRevokeSponsorship:
    def test_account_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAAAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQ=="

        op = RevokeSponsorship.revoke_account_sponsorship(account_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_trustline_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset = Asset("CAT", "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC")
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAQAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAFDQVQAAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_offer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        offer_id = 12345
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAgAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAAAADA5"

        op = RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_date_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        data_name = "Stellar Python SDK"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAwAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAABJTdGVsbGFyIFB5dGhvbiBTREsAAA=="

        op = RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_claimable_balance_id_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAABAAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vg=="

        op = RevokeSponsorship.revoke_claimable_balance_sponsorship(balance_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )

    def test_signer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        signer_key = SignerKey.ed25519_public_key(
            "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAABAAAAAHQ4rOKx6CDoMuIjHGjBgqoFEu6miMmxcqOvVrM4/bwZAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )


class TestClaimPredicate:
    @staticmethod
    def to_xdr(predicate):
        return predicate.to_xdr_object().to_xdr()

    def test_predicate_unconditional(self):
        xdr = "AAAAAA=="
        predicate = ClaimPredicate.predicate_unconditional()
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_before_relative_time(self):
        xdr = "AAAABQAAAAAAAAPo"
        predicate = ClaimPredicate.predicate_before_relative_time(1000)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())


    def test_predicate_before_absolute_time(self):
        xdr = "AAAABAAAAABfc0qi"
        predicate = ClaimPredicate.predicate_before_absolute_time(1601391266)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())


    def test_predicate_not(self):
        xdr = "AAAAAwAAAAEAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate = ClaimPredicate.predicate_not(predicate_abs)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())


    def test_predicate_and_1(self):
        xdr = "AAAAAQAAAAIAAAAEAAAAAF9zSqIAAAAFAAAAAAAAA+g="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_and(predicate_abs, predicate_rel)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_and_2(self):
        xdr = "AAAAAQAAAAIAAAAFAAAAAAAAA+gAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_and(predicate_rel, predicate_abs)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_or_1(self):
        xdr = "AAAAAgAAAAIAAAAEAAAAAF9zSqIAAAAFAAAAAAAAA+g="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_or(predicate_abs, predicate_rel)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_or_2(self):
        xdr = "AAAAAgAAAAIAAAAFAAAAAAAAA+gAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_or(predicate_rel, predicate_abs)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_mix(self):
        xdr = "AAAAAQAAAAIAAAABAAAAAgAAAAQAAAAAX14QAAAAAAAAAAACAAAAAgAAAAUAAAAAAADDUAAAAAMAAAABAAAABAAAAABlU/EA"
        predicate_left = ClaimPredicate.predicate_and(
            ClaimPredicate.predicate_before_absolute_time(1600000000),
            ClaimPredicate.predicate_unconditional(),
        )
        predicate_right = ClaimPredicate.predicate_or(
            ClaimPredicate.predicate_before_relative_time(50000),
            ClaimPredicate.predicate_not(
                ClaimPredicate.predicate_before_absolute_time(1700000000)
            ),
        )
        predicate = ClaimPredicate.predicate_and(predicate_left, predicate_right)
        assert xdr == self.to_xdr(predicate)
        assert predicate == ClaimPredicate.from_xdr_object(predicate.to_xdr_object())

    def test_predicate_invalid_type_raise(self):
        predicate = ClaimPredicate(
            claim_predicate_type="invalid",
            and_predicates=None,
            or_predicates=None,
            not_predicate=None,
            abs_before=None,
            rel_before=1,
        )
        with pytest.raises(
            ValueError, match=f"invalid is not a valid ClaimPredicateType."
        ):
            predicate.to_xdr_object()


class TestClaimant:
    @staticmethod
    def to_xdr(claimant):
        return claimant.to_xdr_object().to_xdr()

    def test_claimant(self):
        xdr = "AAAAAAAAAACJmyhA7VY2xW3cXxSyOXX3nxuiOI0mlOTFbs3dyWDl7wAAAAEAAAACAAAAAQAAAAIAAAAEAAAAAF9eEAAAAAAAAAAAAgAAAAIAAAAFAAAAAAAAw1AAAAADAAAAAQAAAAQAAAAAZVPxAA=="
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        predicate_left = ClaimPredicate.predicate_and(
            ClaimPredicate.predicate_before_absolute_time(1600000000),
            ClaimPredicate.predicate_unconditional(),
        )
        predicate_right = ClaimPredicate.predicate_or(
            ClaimPredicate.predicate_before_relative_time(50000),
            ClaimPredicate.predicate_not(
                ClaimPredicate.predicate_before_absolute_time(1700000000)
            ),
        )
        predicate = ClaimPredicate.predicate_and(predicate_left, predicate_right)
        claimant = Claimant(destination=destination, predicate=predicate)
        assert self.to_xdr(claimant) == xdr
        assert claimant == Claimant.from_xdr_object(claimant.to_xdr_object())

    def test_claimant_default(self):
        xdr = "AAAAAAAAAACJmyhA7VY2xW3cXxSyOXX3nxuiOI0mlOTFbs3dyWDl7wAAAAA="
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        claimant = Claimant(destination=destination)
        assert self.to_xdr(claimant) == xdr
        assert claimant == Claimant.from_xdr_object(claimant.to_xdr_object())


class TestCreateClaimableBalance:
    def test_xdr(self):
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAA4AAAAAAAAAAEqTzAAAAAADAAAAAAAAAACJmyhA7VY2xW3cXxSyOXX3nxuiOI0mlOTFbs3dyWDl7wAAAAEAAAACAAAAAQAAAAIAAAAEAAAAAF9eEAAAAAAAAAAAAgAAAAIAAAAFAAAAAAAAw1AAAAADAAAAAQAAAAQAAAAAZVPxAAAAAAAAAAAAYyi+wCa8rss9LBoofzuttQ+74vczrrbpvZfDhNL/7/EAAAAAAAAAAAAAAACuYyIkw8jWz2vBYj6jUhgWWzNtUpaID2NifbYvrdlNxwAAAAQAAAAAX3NKog=="
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"

        predicate_left = ClaimPredicate.predicate_and(
            ClaimPredicate.predicate_before_absolute_time(1600000000),
            ClaimPredicate.predicate_unconditional(),
        )
        predicate_right = ClaimPredicate.predicate_or(
            ClaimPredicate.predicate_before_relative_time(50000),
            ClaimPredicate.predicate_not(
                ClaimPredicate.predicate_before_absolute_time(1700000000)
            ),
        )
        predicate1 = ClaimPredicate.predicate_and(predicate_left, predicate_right)
        claimant1 = Claimant(
            destination="GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ",
            predicate=predicate1,
        )

        predicate2 = ClaimPredicate.predicate_unconditional()
        claimant2 = Claimant(
            destination="GBRSRPWAE26K5SZ5FQNCQ7Z3VW2Q7O7C64Z25NXJXWL4HBGS77X7CWTG",
            predicate=predicate2,
        )

        predicate3 = ClaimPredicate.predicate_before_absolute_time(1601391266)
        claimant3 = Claimant(
            destination="GCXGGIREYPENNT3LYFRD5I2SDALFWM3NKKLIQD3DMJ63ML5N3FG4OQQG",
            predicate=predicate3,
        )

        op = CreateClaimableBalance(
            asset=Asset.native(),
            amount="125.12",
            claimants=[claimant1, claimant2, claimant3],
            source=source,
        )
        assert op.to_xdr_object().to_xdr() == xdr
        assert (
            Operation.from_xdr_object(op.to_xdr_object()).to_xdr_object().to_xdr()
            == xdr
        )
