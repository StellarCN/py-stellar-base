from decimal import Decimal

import pytest

from stellar_sdk import Claimant, ClaimPredicate, CreateClaimableBalance, Operation
from stellar_sdk.xdr.claim_predicate import ClaimPredicate as XdrClaimPredicate

from . import *


class TestCreateClaimableBalance:
    @pytest.mark.parametrize(
        "amount, source, xdr",
        [
            pytest.param(
                "100",
                None,
                "AAAAAAAAAA4AAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAwAAAAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAABAAAAAgAAAAEAAAACAAAABAAAAABfXhAAAAAAAAAAAAIAAAACAAAABQAAAAAAAMNQAAAAAwAAAAEAAAAEAAAAAGVT8QAAAAAAAAAAAGMovsAmvK7LPSwaKH87rbUPu+L3M6626b2Xw4TS/+/xAAAAAAAAAAAAAAAArmMiJMPI1s9rwWI+o1IYFlszbVKWiA9jYn22L63ZTccAAAAEAAAAAF9zSqI=",
                id="without_source",
            ),
            pytest.param(
                "100",
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA4AAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAwAAAAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAABAAAAAgAAAAEAAAACAAAABAAAAABfXhAAAAAAAAAAAAIAAAACAAAABQAAAAAAAMNQAAAAAwAAAAEAAAAEAAAAAGVT8QAAAAAAAAAAAGMovsAmvK7LPSwaKH87rbUPu+L3M6626b2Xw4TS/+/xAAAAAAAAAAAAAAAArmMiJMPI1s9rwWI+o1IYFlszbVKWiA9jYn22L63ZTccAAAAEAAAAAF9zSqI=",
                id="with_source_public_key",
            ),
            pytest.param(
                "100",
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygAAAAADAAAAAAAAAACJmyhA7VY2xW3cXxSyOXX3nxuiOI0mlOTFbs3dyWDl7wAAAAEAAAACAAAAAQAAAAIAAAAEAAAAAF9eEAAAAAAAAAAAAgAAAAIAAAAFAAAAAAAAw1AAAAADAAAAAQAAAAQAAAAAZVPxAAAAAAAAAAAAYyi+wCa8rss9LBoofzuttQ+74vczrrbpvZfDhNL/7/EAAAAAAAAAAAAAAACuYyIkw8jWz2vBYj6jUhgWWzNtUpaID2NifbYvrdlNxwAAAAQAAAAAX3NKog==",
                id="with_source_muxed_account",
            ),
            pytest.param(
                "100",
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADgAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAADuaygAAAAADAAAAAAAAAACJmyhA7VY2xW3cXxSyOXX3nxuiOI0mlOTFbs3dyWDl7wAAAAEAAAACAAAAAQAAAAIAAAAEAAAAAF9eEAAAAAAAAAAAAgAAAAIAAAAFAAAAAAAAw1AAAAADAAAAAQAAAAQAAAAAZVPxAAAAAAAAAAAAYyi+wCa8rss9LBoofzuttQ+74vczrrbpvZfDhNL/7/EAAAAAAAAAAAAAAACuYyIkw8jWz2vBYj6jUhgWWzNtUpaID2NifbYvrdlNxwAAAAQAAAAAX3NKog==",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                Decimal("100"),
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA4AAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAA7msoAAAAAAwAAAAAAAAAAiZsoQO1WNsVt3F8Usjl1958bojiNJpTkxW7N3clg5e8AAAABAAAAAgAAAAEAAAACAAAABAAAAABfXhAAAAAAAAAAAAIAAAACAAAABQAAAAAAAMNQAAAAAwAAAAEAAAAEAAAAAGVT8QAAAAAAAAAAAGMovsAmvK7LPSwaKH87rbUPu+L3M6626b2Xw4TS/+/xAAAAAAAAAAAAAAAArmMiJMPI1s9rwWI+o1IYFlszbVKWiA9jYn22L63ZTccAAAAEAAAAAF9zSqI=",
                id="starting_balance_decimal",
            ),
        ],
    )
    def test_xdr(self, amount, source, xdr):
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
        claimants = [claimant1, claimant2, claimant3]
        op = CreateClaimableBalance(
            asset=asset1,
            amount=amount,
            claimants=claimants,
            source=source,
        )

        assert op.asset == asset1
        assert op.amount == str(amount)
        assert op.claimants == claimants
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_amount_raise(self):
        amount = "12345678902.23423324"
        claimants = [
            Claimant(
                destination=kp2.public_key,
                predicate=ClaimPredicate.predicate_unconditional(),
            )
        ]
        with pytest.raises(
            ValueError,
            match=f'Value of argument "amount" must have at most 7 digits after the decimal: {amount}',
        ):
            CreateClaimableBalance(asset1, amount, claimants, kp1.public_key)


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

    def test_invalid_destination_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "destination" is not a valid ed25519 public key: {key}',
        ):
            Claimant(destination=key)
