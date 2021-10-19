from decimal import Decimal

import pytest

from stellar_sdk import (
    LIQUIDITY_POOL_FEE_V18,
    Asset,
    LiquidityPoolAsset,
    LiquidityPoolDeposit,
    LiquidityPoolId,
    LiquidityPoolWithdraw,
    MuxedAccount,
    Price,
)
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError
from stellar_sdk.operation import CreateAccount, Operation
from stellar_sdk.operation.account_merge import AccountMerge
from stellar_sdk.operation.allow_trust import AllowTrust, TrustLineEntryFlag
from stellar_sdk.operation.begin_sponsoring_future_reserves import (
    BeginSponsoringFutureReserves,
)
from stellar_sdk.operation.bump_sequence import BumpSequence
from stellar_sdk.operation.change_trust import ChangeTrust
from stellar_sdk.operation.claim_claimable_balance import ClaimClaimableBalance
from stellar_sdk.operation.clawback import Clawback
from stellar_sdk.operation.clawback_claimable_balance import ClawbackClaimableBalance
from stellar_sdk.operation.create_claimable_balance import *
from stellar_sdk.operation.create_passive_sell_offer import CreatePassiveSellOffer
from stellar_sdk.operation.end_sponsoring_future_reserves import (
    EndSponsoringFutureReserves,
)
from stellar_sdk.operation.inflation import Inflation
from stellar_sdk.operation.manage_buy_offer import ManageBuyOffer
from stellar_sdk.operation.manage_data import ManageData
from stellar_sdk.operation.manage_sell_offer import ManageSellOffer
from stellar_sdk.operation.path_payment_strict_receive import PathPaymentStrictReceive
from stellar_sdk.operation.path_payment_strict_send import PathPaymentStrictSend
from stellar_sdk.operation.payment import Payment
from stellar_sdk.operation.revoke_sponsorship import Data, Offer, RevokeSponsorship
from stellar_sdk.operation.revoke_sponsorship import Signer as RevokeSponsorshipSigner
from stellar_sdk.operation.revoke_sponsorship import TrustLine
from stellar_sdk.operation.set_options import AuthorizationFlag, SetOptions
from stellar_sdk.operation.set_trust_line_flags import SetTrustLineFlags, TrustLineFlags
from stellar_sdk.signer import Signer
from stellar_sdk.signer_key import SignerKey
from stellar_sdk.utils import sha256
from stellar_sdk.xdr.claim_predicate import ClaimPredicate as XdrClaimPredicate


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
                'type of argument "value" must be one of \(str, decimal.Decimal\); got int instead',
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
        assert op.source.account_id == source


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
            match=f'Value of argument "destination" is not a valid ed25519 public key: {destination}',
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
            match='Value of argument "starting_balance" must represent a positive number and '
            f"the max valid value is 922337203685.4775807: {starting_balance}",
        ):
            CreateAccount(destination, starting_balance)

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source.account_id == source
        assert op.starting_balance == "1000"
        assert op.destination == destination

    def test_get_muxed_account_str_source_exist_from_xdr_obj(self):  # BAD TEST
        source = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        starting_balance = "1000.00"
        origin_op = CreateAccount(destination, starting_balance, source)
        origin_xdr_obj = origin_op.to_xdr_object()

        op = Operation.from_xdr_object(origin_xdr_obj)
        assert op.source == MuxedAccount.from_account(source)
        assert op.starting_balance == "1000"
        assert op.destination == destination

    def test_get_muxed_account_source_exist_from_xdr_obj(self):  # BAD TEST
        source = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
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
        assert op.source.account_id == source
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
        assert op.source.account_id == source


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
        assert op.source.account_id == source
        assert op.destination.account_id == destination

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        destination2 = "GBL3NR5XNBNFAYVQMZ7R6RMUKLMGRUHNIYDYMEUPANQV6OROQXSDZYHV"
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        restore_op = AccountMerge.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()
        restore_op.destination = destination2
        assert restore_op.destination == destination2

    def test_from_xdr_obj_muxed_str_account(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AccountMerge)
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == MuxedAccount.from_account(destination)

    def test_from_xdr_obj_muxed_account(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
        origin_xdr_obj = AccountMerge(destination, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, AccountMerge)
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == destination


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
    def test_xdr_with_asset(self, limit, xdr):
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        op = ChangeTrust(asset, limit, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, ChangeTrust)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        if limit is None:
            limit = "922337203685.4775807"
        assert restore_op.limit == limit
        assert restore_op.asset == asset

    @pytest.mark.parametrize(
        "limit, xdr",
        [
            (
                "922337203685.4775807",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAADAAAAAAAAAAFBUlNUAAAAAH8wYjTJienWf2nf2TEZi2APPWzmtkwiQHAftisIgyuHAAAAAVVTRAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAAef/////////8=",
            ),
            (
                "0",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAADAAAAAAAAAAFBUlNUAAAAAH8wYjTJienWf2nf2TEZi2APPWzmtkwiQHAftisIgyuHAAAAAVVTRAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAAeAAAAAAAAAAA=",
            ),
            (
                "50.1234567",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAADAAAAAAAAAAFBUlNUAAAAAH8wYjTJienWf2nf2TEZi2APPWzmtkwiQHAftisIgyuHAAAAAVVTRAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAAeAAAAAB3gO4c=",
            ),
            (
                None,
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAYAAAADAAAAAAAAAAFBUlNUAAAAAH8wYjTJienWf2nf2TEZi2APPWzmtkwiQHAftisIgyuHAAAAAVVTRAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAAef/////////8=",
            ),
        ],
    )
    def test_xdr_with_liquidity_pool_asset(self, limit, xdr):
        asset_a = Asset(
            "ARST", "GB7TAYRUZGE6TVT7NHP5SMIZRNQA6PLM423EYISAOAP3MKYIQMVYP2JO"
        )
        asset_b = Asset(
            "USD", "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        )
        fee = LIQUIDITY_POOL_FEE_V18
        asset = LiquidityPoolAsset(asset_a, asset_b, fee=fee)
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        op = ChangeTrust(asset, limit, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, ChangeTrust)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        if limit is None:
            limit = "922337203685.4775807"
        assert restore_op.limit == limit
        assert restore_op.asset == asset


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
        assert op.source.account_id == source
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

    # def test_to_xdr_obj_with_invalid_amount_raise(self):
    #     source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
    #     destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
    #     amount = 1
    #     asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
    #     with pytest.raises(TypeError):
    #         Payment(destination, asset, amount, source)

    def test_from_xdr_obj(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Payment)
        assert op.source.account_id == source
        assert op.destination.account_id == destination
        assert op.amount == "1000"
        assert op.asset == asset

    def test_from_xdr_muxed(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMDS674JZ"
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        restore_op = Payment.from_xdr_object(origin_xdr_obj)
        assert restore_op.to_xdr_object().to_xdr() == origin_xdr_obj.to_xdr()

    def test_from_xdr_obj_mux_account_str(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Payment)
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == MuxedAccount.from_account(destination)
        assert op.amount == "1000"
        assert op.asset == asset

    def test_from_xdr_obj_mux_account(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
        amount = "1000.0000000"
        asset = Asset("USD", "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7")
        origin_xdr_obj = Payment(destination, asset, amount, source).to_xdr_object()
        op = Operation.from_xdr_object(origin_xdr_obj)
        assert isinstance(op, Payment)
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == destination
        assert op.amount == "1000"
        assert op.asset == asset


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
        assert op.source.account_id == source
        assert op.destination.account_id == destination
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
        restore_op.destination = destination2
        assert restore_op.destination == destination2

    def test_from_xdr_obj_muxed_account_str(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
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
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == MuxedAccount.from_account(destination)
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_max == "3.007"
        assert op.dest_amount == "3.1415"
        assert op.path == path

    def test_from_xdr_obj_muxed_account(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
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
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_max == "3.007"
        assert op.dest_amount == "3.1415"
        assert op.path == path


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
        assert op.source.account_id == source
        assert op.destination.account_id == destination
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
        restore_op.destination = destination2
        assert restore_op.destination == destination2

    def test_from_xdr_obj_muxed_account_str(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = (
            "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
        )
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
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == MuxedAccount.from_account(destination)
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_amount == "3.1415"
        assert op.dest_min == "3.007"
        assert op.path == path

    def test_from_xdr_obj_muxed_account(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        destination = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
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
        assert (
            op.source == source if source is None else MuxedAccount.from_account(source)
        )
        assert op.destination == destination
        assert op.send_asset == send_asset
        assert op.dest_asset == dest_asset
        assert op.send_amount == "3.1415"
        assert op.dest_min == "3.007"
        assert op.path == path


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
        assert op.source.account_id == source
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
        assert op.source.account_id == source
        assert op.data_name == name
        if isinstance(value, str):
            value = value.encode()
        assert op.data_value == value


class TestSetOptions:
    AUTHORIZATION_REQUIRED = 1
    AUTHORIZATION_REVOCABLE = 2
    AUTHORIZATION_IMMUTABLE = 4
    AUTHORIZATION_CLAWBACK_ENABLED = 8

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
                AuthorizationFlag.AUTHORIZATION_REVOCABLE
                | AuthorizationFlag.AUTHORIZATION_IMMUTABLE,
                AuthorizationFlag.AUTHORIZATION_REQUIRED,
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
        if source:
            assert from_instance.source == MuxedAccount.from_account(source)
        else:
            assert from_instance.source is None
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
        if source:
            assert from_instance.source == MuxedAccount.from_account(source)
        else:
            assert from_instance.source is None
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
        if source:
            assert from_instance.source == MuxedAccount.from_account(source)
        else:
            assert from_instance.source is None
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
        if source:
            assert from_instance.source == MuxedAccount.from_account(source)
        else:
            assert from_instance.source is None
        assert from_instance.buying == buying
        assert from_instance.selling == selling
        assert Decimal(from_instance.amount) == Decimal(amount)
        if not isinstance(price, Price):
            price = Price.from_raw_price(price)
        assert from_instance.price == price


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
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_trustline_xdr_with_asset(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset = Asset("CAT", "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC")
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAQAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAFDQVQAAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_trustline_xdr_with_liquidity_pool_id(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset = LiquidityPoolId(
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAQAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAPdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xw=="

        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_offer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        offer_id = 12345
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAgAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAAAADA5"

        op = RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_date_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        data_name = "Stellar Python SDK"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAwAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAABJTdGVsbGFyIFB5dGhvbiBTREsAAA=="

        op = RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_claimable_balance_id_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAABAAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vg=="

        op = RevokeSponsorship.revoke_claimable_balance_sponsorship(balance_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_liquidity_pool(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAABd17GrgxwnMxDdvsb5eHCqg8L714ziKt7Tfsv08zgPrH"

        op = RevokeSponsorship.revoke_liquidity_pool_sponsorship(
            liquidity_pool_id, source
        )
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_signer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        signer_key = SignerKey.ed25519_public_key(
            "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAABAAAAAHQ4rOKx6CDoMuIjHGjBgqoFEu6miMmxcqOvVrM4/bwZAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_trustline_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset1 = Asset.native()
        asset2 = Asset(
            "TEST", "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        )
        assert TrustLine(account1, asset1) == TrustLine(account1, asset1)
        assert TrustLine(account1, asset1) != TrustLine(account1, asset2)
        assert TrustLine(account1, asset1) != TrustLine(account2, asset1)

    def test_offer_equal(self):
        seller1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        offer_id1 = 0
        offer_id2 = 1
        assert Offer(seller1, offer_id1) == Offer(seller1, offer_id1)
        assert Offer(seller1, offer_id1) != Offer(seller1, offer_id2)
        assert Offer(seller1, offer_id1) != Offer(seller2, offer_id1)

    def test_data_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        data_name1 = "data_name1"
        data_name2 = "data_name2"
        assert Data(account1, data_name1) == Data(account1, data_name1)
        assert Data(account1, data_name1) != Data(account1, data_name2)
        assert Data(account1, data_name1) != Data(account2, data_name1)

    def test_signer_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        signer1 = SignerKey.ed25519_public_key(account1)
        signer2 = SignerKey.ed25519_public_key(account2)
        assert RevokeSponsorshipSigner(account1, signer1) == RevokeSponsorshipSigner(
            account1, signer1
        )
        assert RevokeSponsorshipSigner(account1, signer1) != RevokeSponsorshipSigner(
            account1, signer2
        )
        assert RevokeSponsorshipSigner(account1, signer1) != RevokeSponsorshipSigner(
            account2, signer1
        )


class TestClaimPredicate:
    @staticmethod
    def to_xdr(predicate):
        return predicate.to_xdr_object().to_xdr()

    def test_predicate_unconditional(self):
        xdr = "AAAAAA=="
        predicate = ClaimPredicate.predicate_unconditional()
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_before_relative_time(self):
        xdr = "AAAABQAAAAAAAAPo"
        predicate = ClaimPredicate.predicate_before_relative_time(1000)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_before_absolute_time(self):
        xdr = "AAAABAAAAABfc0qi"
        predicate = ClaimPredicate.predicate_before_absolute_time(1601391266)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_not(self):
        xdr = "AAAAAwAAAAEAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate = ClaimPredicate.predicate_not(predicate_abs)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_and_1(self):
        xdr = "AAAAAQAAAAIAAAAEAAAAAF9zSqIAAAAFAAAAAAAAA+g="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_and(predicate_abs, predicate_rel)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_and_2(self):
        xdr = "AAAAAQAAAAIAAAAFAAAAAAAAA+gAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_and(predicate_rel, predicate_abs)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_or_1(self):
        xdr = "AAAAAgAAAAIAAAAEAAAAAF9zSqIAAAAFAAAAAAAAA+g="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_or(predicate_abs, predicate_rel)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_or_2(self):
        xdr = "AAAAAgAAAAIAAAAFAAAAAAAAA+gAAAAEAAAAAF9zSqI="
        predicate_abs = ClaimPredicate.predicate_before_absolute_time(1601391266)
        predicate_rel = ClaimPredicate.predicate_before_relative_time(1000)
        predicate = ClaimPredicate.predicate_or(predicate_rel, predicate_abs)
        assert xdr == self.to_xdr(predicate)
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

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
        xdr_object = XdrClaimPredicate.from_xdr(xdr)
        assert predicate == ClaimPredicate.from_xdr_object(xdr_object)

    def test_predicate_invalid_type_raise(self):
        with pytest.raises(
            TypeError,
            match='type of argument "claim_predicate_type" must be stellar_sdk.operation.create_claimable_balance.ClaimPredicateType; got str instead',
        ):
            ClaimPredicate(
                claim_predicate_type="invalid",
                and_predicates=None,
                or_predicates=None,
                not_predicate=None,
                abs_before=None,
                rel_before=1,
            )


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


class TestClawback:
    def test_xdr(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        from_ = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        amount = "100"
        op = Clawback(asset, from_, amount, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, Clawback)
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABMAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAAND42wpWEfOthyO+2vpGJJ5QgHfCRRZKvHXjjhkRA7SwAAAAA7msoA"
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.from_.account_id == from_
        assert restore_op.asset == asset
        assert restore_op.amount == amount

    def test_xdr_no_source(self):
        source = None
        from_ = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        amount = "100"
        op = Clawback(asset, from_, amount, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, Clawback)
        xdr = "AAAAAAAAABMAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAAND42wpWEfOthyO+2vpGJJ5QgHfCRRZKvHXjjhkRA7SwAAAAA7msoA"
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source is None
        assert restore_op.from_.account_id == from_
        assert restore_op.asset == asset
        assert restore_op.amount == amount

    def test_xdr_set_from(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        from_ = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        amount = "100"
        op = Clawback(asset, from_, amount, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, Clawback)
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABMAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAAND42wpWEfOthyO+2vpGJJ5QgHfCRRZKvHXjjhkRA7SwAAAAA7msoA"
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.from_.account_id == from_
        assert restore_op.asset == asset
        assert restore_op.amount == amount

    def test_from_xdr_obj_muxed_account_str(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        from_ = "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        amount = "100"
        op = Clawback(asset, from_, amount, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, Clawback)
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABMAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAQAAAAAAAAAE0iAAdX7q5YP8UN1mn5dnOswl7HJYI6xz+vbH3zGtMeUJAAAAADuaygA="
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.from_.account_muxed == from_
        assert restore_op.asset == asset
        assert restore_op.amount == amount

    def test_from_xdr_obj_muxed_account(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        from_ = MuxedAccount(
            "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY", 1234
        )
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        amount = "100"
        op = Clawback(asset, from_, amount, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, Clawback)
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABMAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAQAAAAAAAAAE0iAAdX7q5YP8UN1mn5dnOswl7HJYI6xz+vbH3zGtMeUJAAAAADuaygA="
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.from_ == from_
        assert restore_op.asset == asset
        assert restore_op.amount == amount


class TestClawbackClaimableBalance:
    def test_xdr(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        balance_id = (
            "00000000929b20b72e5890ab51c24f1cc46fa01c4f318d8d33367d24dd614cfdf5491072"
        )
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABQAAAAAkpsgty5YkKtRwk8cxG+gHE8xjY0zNn0k3WFM/fVJEHI="
        op = ClawbackClaimableBalance(balance_id, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, ClawbackClaimableBalance)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.balance_id == balance_id

    def test_xdr_no_source(self):
        source = None
        balance_id = (
            "00000000929b20b72e5890ab51c24f1cc46fa01c4f318d8d33367d24dd614cfdf5491072"
        )
        xdr = "AAAAAAAAABQAAAAAkpsgty5YkKtRwk8cxG+gHE8xjY0zNn0k3WFM/fVJEHI="
        op = ClawbackClaimableBalance(balance_id, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, ClawbackClaimableBalance)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source is None
        assert restore_op.balance_id == balance_id


class TestSetTrustLineFlags:
    def test_xdr(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        trustor = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        clear_flags = TrustLineFlags.AUTHORIZED_FLAG
        set_flags = (
            TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG
            | TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG
        )
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABUAAAAADQ+NsKVhHzrYcjvtr6RiSeUIB3wkUWSrx1444ZEQO0sAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAEAAAAG"

        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, SetTrustLineFlags)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.trustor == trustor
        assert restore_op.clear_flags == clear_flags
        assert restore_op.set_flags == set_flags
        assert restore_op.asset == asset

    def test_xdr_no_source(self):
        source = None
        trustor = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        clear_flags = TrustLineFlags.AUTHORIZED_FLAG
        set_flags = (
            TrustLineFlags.AUTHORIZED_TO_MAINTAIN_LIABILITIES_FLAG
            | TrustLineFlags.TRUSTLINE_CLAWBACK_ENABLED_FLAG
        )
        xdr = "AAAAAAAAABUAAAAADQ+NsKVhHzrYcjvtr6RiSeUIB3wkUWSrx1444ZEQO0sAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAEAAAAG"

        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, SetTrustLineFlags)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source is None
        assert restore_op.trustor == trustor
        assert restore_op.clear_flags == clear_flags
        assert restore_op.set_flags == set_flags
        assert restore_op.asset == asset

    def test_xdr_set_flags_and_clear_flags_is_none(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        trustor = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        clear_flags = None
        set_flags = None
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABUAAAAADQ+NsKVhHzrYcjvtr6RiSeUIB3wkUWSrx1444ZEQO0sAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAAAAAAA"
        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, SetTrustLineFlags)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.trustor == trustor
        assert restore_op.clear_flags == clear_flags
        assert restore_op.set_flags == set_flags
        assert restore_op.asset == asset

    def test_xdr_set_flags_is_none(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        trustor = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        clear_flags = TrustLineFlags.AUTHORIZED_FLAG
        set_flags = None
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABUAAAAADQ+NsKVhHzrYcjvtr6RiSeUIB3wkUWSrx1444ZEQO0sAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAEAAAAA"
        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, SetTrustLineFlags)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.trustor == trustor
        assert restore_op.clear_flags == clear_flags
        assert restore_op.set_flags == set_flags
        assert restore_op.asset == asset

    def test_xdr_clear_flags_is_none(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        trustor = "GAGQ7DNQUVQR6OWYOI563L5EMJE6KCAHPQSFCZFLY5PDRYMRCA5UWCMP"
        asset = Asset(
            "DEMO", "GCWPICV6IV35FQ2MVZSEDLORHEMMIAODRQPVDEIKZOW2GC2JGGDCXVVV"
        )
        clear_flags = None
        set_flags = TrustLineFlags.AUTHORIZED_FLAG
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABUAAAAADQ+NsKVhHzrYcjvtr6RiSeUIB3wkUWSrx1444ZEQO0sAAAABREVNTwAAAACs9Aq+RXfSw0yuZEGt0TkYxAHDjB9RkQrLraMLSTGGKwAAAAAAAAAB"
        op = SetTrustLineFlags(trustor, asset, clear_flags, set_flags, source)
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, SetTrustLineFlags)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.trustor == trustor
        assert restore_op.clear_flags == clear_flags
        assert restore_op.set_flags == set_flags
        assert restore_op.asset == asset


class TestLiquidityPoolDeposit:
    def test_xdr(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        max_amount_a = "10"
        max_amount_b = "20"
        min_price = "0.45"
        max_price = "0.55"
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABbdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xwAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU"
        op = LiquidityPoolDeposit(
            liquidity_pool_id, max_amount_a, max_amount_b, min_price, max_price, source
        )
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, LiquidityPoolDeposit)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.liquidity_pool_id == liquidity_pool_id
        assert restore_op.max_amount_a == max_amount_a
        assert restore_op.max_amount_b == max_amount_b
        assert restore_op.min_price == Price.from_raw_price(min_price)
        assert restore_op.max_price == Price.from_raw_price(max_price)

    def test_xdr_no_source(self):
        source = None
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        max_amount_a = "10"
        max_amount_b = "20"
        min_price = "0.45"
        max_price = "0.55"
        xdr = "AAAAAAAAABbdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xwAAAAAF9eEAAAAAAAvrwgAAAAAJAAAAFAAAAAsAAAAU"
        op = LiquidityPoolDeposit(
            liquidity_pool_id, max_amount_a, max_amount_b, min_price, max_price, source
        )
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, LiquidityPoolDeposit)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source is None
        assert restore_op.liquidity_pool_id == liquidity_pool_id
        assert restore_op.max_amount_a == max_amount_a
        assert restore_op.max_amount_b == max_amount_b
        assert restore_op.min_price == Price.from_raw_price(min_price)
        assert restore_op.max_price == Price.from_raw_price(max_price)


class TestLiquidityPoolWithdraw:
    def test_xdr(self):
        source = "GA2N7NI5WEMJILMK4UPDTF2ZX2BIRQUM3HZUE27TRUNRFN5M5EXU6RQV"
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        amount = "5"
        min_amount_a = "10"
        min_amount_b = "20"
        xdr = "AAAAAQAAAAA037UdsRiULYrlHjmXWb6CiMKM2fNCa/ONGxK3rOkvTwAAABfdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xwAAAAAC+vCAAAAAAAX14QAAAAAAC+vCAA=="
        op = LiquidityPoolWithdraw(
            liquidity_pool_id, amount, min_amount_a, min_amount_b, source
        )
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, LiquidityPoolWithdraw)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source.account_id == source
        assert restore_op.liquidity_pool_id == liquidity_pool_id
        assert restore_op.amount == amount
        assert restore_op.min_amount_a == min_amount_a
        assert restore_op.min_amount_b == min_amount_b

    def test_xdr_no_source(self):
        source = None
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        amount = "5"
        min_amount_a = "10"
        min_amount_b = "20"
        xdr = "AAAAAAAAABfdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xwAAAAAC+vCAAAAAAAX14QAAAAAAC+vCAA=="
        op = LiquidityPoolWithdraw(
            liquidity_pool_id, amount, min_amount_a, min_amount_b, source
        )
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert isinstance(restore_op, LiquidityPoolWithdraw)
        assert op.to_xdr_object().to_xdr() == xdr
        assert restore_op.to_xdr_object().to_xdr() == xdr
        assert restore_op.source is None
        assert restore_op.liquidity_pool_id == liquidity_pool_id
        assert restore_op.amount == amount
        assert restore_op.min_amount_a == min_amount_a
        assert restore_op.min_amount_b == min_amount_b
