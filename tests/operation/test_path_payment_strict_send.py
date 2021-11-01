from decimal import Decimal

import pytest

from stellar_sdk import Operation, PathPaymentStrictSend

from . import *


class TestPathPaymentStrictSend:
    @pytest.mark.parametrize(
        "destination, send_amount, dest_min, path, source, xdr",
        [
            pytest.param(
                kp2.public_key,
                "100",
                "200",
                [asset2, asset3],
                None,
                "AAAAAAAAAA0AAAAAAAAAADuaygAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAB3NZQAAAAAAgAAAAJDQVRDT0lOAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAACUEFOREEAAAAAAAAAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNj",
                id="without_source",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                "200",
                [asset2, asset3],
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA0AAAAAAAAAADuaygAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAB3NZQAAAAAAgAAAAJDQVRDT0lOAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAACUEFOREEAAAAAAAAAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNj",
                id="with_source_public_key",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                "200",
                [asset2, asset3],
                muxed1,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADQAAAAAAAAAAO5rKAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M=",
                id="with_source_muxed_account",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                "200",
                [asset2, asset3],
                muxed1.account_muxed,
                "AAAAAQAAAQAAAAAAAAAAAWJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2hAAAADQAAAAAAAAAAO5rKAAAAAAC0afgnwmih/lUCr1WHAREWI+O/+IF0s7BtVkiMxS7+uAAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M=",
                id="with_source_muxed_account_strkey",
            ),
            pytest.param(
                muxed2,
                "100",
                "200",
                [asset2, asset3],
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA0AAAAAAAAAADuaygAAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M=",
                id="with_destination_muxed_account",
            ),
            pytest.param(
                muxed2.account_muxed,
                "100",
                "200",
                [asset2, asset3],
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA0AAAAAAAAAADuaygAAAAEAAAAAAAAAAAJiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAAFVU0QAAAAAAJuOuviWOFUdz56k90MgcRBrh6sOLbPWm3WlOCJy91nYAAAAAHc1lAAAAAACAAAAAkNBVENPSU4AAAAAAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAJQQU5EQQAAAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M=",
                id="with_destination_muxed_account_strkey",
            ),
            pytest.param(
                kp2.public_key,
                Decimal("100"),
                Decimal("200"),
                [asset2, asset3],
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA0AAAAAAAAAADuaygAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAB3NZQAAAAAAgAAAAJDQVRDT0lOAAAAAAAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAACUEFOREEAAAAAAAAAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNj",
                id="amount_decimal",
            ),
            pytest.param(
                kp2.public_key,
                "100",
                "200",
                [],
                kp1.public_key,
                "AAAAAQAAAABiXz1Zw/ieWRoG2l4IxdbkvfDRUDq5wyKBSUnrCR5doQAAAA0AAAAAAAAAADuaygAAAAAAtGn4J8Joof5VAq9VhwERFiPjv/iBdLOwbVZIjMUu/rgAAAABVVNEAAAAAACbjrr4ljhVHc+epPdDIHEQa4erDi2z1pt1pTgicvdZ2AAAAAB3NZQAAAAAAA==",
                id="empty_path",
            ),
        ],
    )
    def test_xdr(self, destination, send_amount, dest_min, path, source, xdr):
        send_asset = native_asset
        dest_asset = asset1

        op = PathPaymentStrictSend(
            destination, send_asset, send_amount, dest_asset, dest_min, path, source
        )
        assert (
            op.destination == destination
            if isinstance(destination, MuxedAccount)
            else MuxedAccount.from_account(destination)
        )
        assert op.send_asset == send_asset
        assert op.send_amount == str(send_amount)
        assert op.dest_asset == dest_asset
        assert op.dest_min == str(dest_min)
        assert op.path == path
        check_source(op.source, source)
        xdr_object = op.to_xdr_object()
        assert xdr_object.to_xdr() == xdr
        assert Operation.from_xdr_object(xdr_object) == op

    def test_invalid_send_amount_raise(self):
        send_amount = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "send_amount" must have at most 7 digits after the decimal: {send_amount}',
        ):
            PathPaymentStrictSend(
                kp2.public_key,
                native_asset,
                send_amount,
                asset1,
                "200",
                [asset2, asset3],
                kp1.public_key,
            )

    def test_invalid_dest_min_raise(self):
        dest_min = "12345678902.23423324"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "dest_min" must have at most 7 digits after the decimal: {dest_min}',
        ):
            PathPaymentStrictSend(
                kp2.public_key,
                native_asset,
                "100",
                asset1,
                dest_min,
                [asset2, asset3],
                kp1.public_key,
            )
