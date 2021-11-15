import pytest

from stellar_sdk.exceptions import NoApproximationError
from stellar_sdk.utils import (
    best_rational_approximation,
    hex_to_bytes,
    is_valid_hash,
    raise_if_not_valid_amount,
    raise_if_not_valid_balance_id,
    raise_if_not_valid_ed25519_public_key,
    raise_if_not_valid_hash,
    urljoin_with_query,
)


class TestUtils:
    @pytest.mark.parametrize(
        "n, d, v",
        [
            (1, 10, "0.1"),
            (1, 100, "0.01"),
            (1, 1000, "0.001"),
            (54301793, 100000, "543.017930"),
            (31969983, 100000, "319.69983"),
            (93, 100, "0.93"),
            (1, 2, "0.5"),
            (173, 100, "1.730"),
            (5333399, 6250000, "0.85334384"),
            (11, 2, "5.5"),
            (272783, 100000, "2.72783"),
            (638082, 1, "638082.0"),
            (36731261, 12500000, "2.93850088"),
            (1451, 25, "58.04"),
            (8253, 200, "41.265"),
            (12869, 2500, "5.1476"),
            (4757, 50, "95.14"),
            (3729, 5000, "0.74580"),
            (4119, 1, "4119.0"),
        ],
    )
    def test_best_rational_approximation(self, v, n, d):
        assert best_rational_approximation(v) == {"n": n, "d": d}

    @pytest.mark.parametrize("v", ["0.0000000003", 2147483648])
    def test_best_rational_approximation_raise(self, v):
        with pytest.raises(NoApproximationError, match="Couldn't find approximation."):
            best_rational_approximation(v)

    @pytest.mark.parametrize(
        "input_value, except_return",
        [
            (b"hello", b"hello"),
            (
                "bbf50b0fb8e4b0ad8b005eb39d96e068776f43f16a5858a2dafaa3e8045887dd",
                b"\xbb\xf5\x0b\x0f\xb8\xe4\xb0\xad\x8b\x00^\xb3\x9d\x96\xe0hwoC\xf1jXX\xa2\xda\xfa\xa3\xe8\x04X\x87\xdd",
            ),
        ],
    )
    def test_hex_to_bytes(self, input_value, except_return):
        assert hex_to_bytes(input_value) == except_return

    @pytest.mark.parametrize(
        "base, path, output",
        [
            (
                "https://horizon.stellar.org/",
                "transaction",
                "https://horizon.stellar.org/transaction",
            ),
            (
                "https://horizon.stellar.org/hello",
                "transaction",
                "https://horizon.stellar.org/hello/transaction",
            ),
            (
                "https://horizon.stellar.org/?auth=password",
                "transaction",
                "https://horizon.stellar.org/transaction?auth=password",
            ),
            (
                "https://horizon.stellar.org/hello?auth=password",
                "transaction",
                "https://horizon.stellar.org/hello/transaction?auth=password",
            ),
            (
                "https://horizon.stellar.org?auth=password&name=overcat",
                "transaction",
                "https://horizon.stellar.org/transaction?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello?auth=password&name=overcat",
                "transaction",
                "https://horizon.stellar.org/hello/transaction?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello/world?auth=password&name=overcat",
                "transaction",
                "https://horizon.stellar.org/hello/world/transaction?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello/world?auth=password&name=overcat",
                "",
                "https://horizon.stellar.org/hello/world?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello/world?auth=password&name=overcat",
                None,
                "https://horizon.stellar.org/hello/world?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello/world/?auth=password&name=overcat",
                "",
                "https://horizon.stellar.org/hello/world/?auth=password&name=overcat",
            ),
            (
                "https://horizon.stellar.org/hello/world/?auth=password&name=overcat",
                None,
                "https://horizon.stellar.org/hello/world/?auth=password&name=overcat",
            ),
        ],
    )
    def test_urljoin_with_query(self, base, path, output):
        assert output == urljoin_with_query(base, path)

    @pytest.mark.parametrize(
        "data, result",
        [
            ("", False),
            ("abc", False),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7d",
                False,
            ),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7123",
                False,
            ),
            ("dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7", True),
            ("DD7B1AB831C273310DDBEC6F97870AA83C2FBD78CE22ADED37ECBF4F3380FAC7", True),
            ("DD7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7", True),
        ],
    )
    def test_is_valid_hash(self, data, result):
        assert is_valid_hash(data) == result

    @pytest.mark.parametrize(
        "account_id, argument_name, raise_err",
        [
            ("", "account_id", True),
            ("", "account_id2", True),
            ("GDWZCOEQRODFCH6ISYQPWY67L3ULLWS5ISXYYL5GH43W7Y", "account_id", True),
            (
                "SBCVMMCBEDB64TVJZFYJOJAERZC4YVVUOE6SYR2Y76CBTENGUSGWRRVO",
                "account_id",
                True,
            ),
            (
                "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26",
                "account_id",
                True,
            ),
            (
                "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY",
                "account_id",
                False,
            ),
        ],
    )
    def test_raise_if_not_valid_ed25519_public_key(
        self, account_id, argument_name, raise_err
    ):
        if raise_err:
            with pytest.raises(
                ValueError,
                match=f'Value of argument "{argument_name}" is not a valid ed25519 public key: {account_id}',
            ):
                raise_if_not_valid_ed25519_public_key(account_id, argument_name)
        else:
            raise_if_not_valid_ed25519_public_key(account_id, argument_name)

    @pytest.mark.parametrize(
        "amount, argument_name, raise_err",
        [
            ("-0.1", "amount", True),
            ("-0.1", "amount2", True),
            ("922337203685.4775808", "amount", True),
            ("922337203685.4775807", "amount", False),
            ("0", "amount", False),
        ],
    )
    def test_raise_if_not_valid_amount_out_of_range(
        self, amount, argument_name, raise_err
    ):
        if raise_err:
            with pytest.raises(
                ValueError,
                match=f'Value of argument "{argument_name}" must represent a positive number and the max valid value is 922337203685.4775807: {amount}',
            ):
                raise_if_not_valid_amount(amount, argument_name)
        else:
            raise_if_not_valid_amount(amount, argument_name)

    @pytest.mark.parametrize(
        "amount, argument_name, raise_err",
        [
            ("922337203685.47758070", "amount", True),
            ("922337203685.47758070", "amount2", True),
            ("0.0000001", "amount", False),
            ("922337203685.4775807", "amount", False),
        ],
    )
    def test_raise_if_not_valid_too_many_digits(
        self, amount, argument_name, raise_err
    ):
        if raise_err:
            with pytest.raises(
                ValueError,
                match=f'Value of argument "{argument_name}" must have at most 7 digits after the decimal: {amount}',
            ):
                raise_if_not_valid_amount(amount, argument_name)
        else:
            raise_if_not_valid_amount(amount, argument_name)

    @pytest.mark.parametrize(
        "hash, argument_name, raise_err",
        [
            ("", "hash", True),
            ("", "hash2", True),
            ("abc", "hash", True),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7d",
                "hash",
                True,
            ),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7123",
                "hash",
                True,
            ),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7",
                "hash",
                False,
            ),
            (
                "DD7B1AB831C273310DDBEC6F97870AA83C2FBD78CE22ADED37ECBF4F3380FAC7",
                "hash",
                False,
            ),
            (
                "DD7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7",
                "hash",
                False,
            ),
        ],
    )
    def test_raise_if_not_valid_hash(self, hash, argument_name, raise_err):
        if raise_err:
            with pytest.raises(
                ValueError,
                match=f'Value of argument "{argument_name}" is not a valid hash: {hash}',
            ):
                raise_if_not_valid_hash(hash, argument_name)
        else:
            raise_if_not_valid_hash(hash, argument_name)

    @pytest.mark.parametrize(
        "balance_id, argument_name, raise_err",
        [
            ("", "balance_id", True),
            ("", "balance_id2", True),
            ("abc", "balance_id", True),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7d",
                "balance_id",
                True,
            ),
            (
                "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7123",
                "balance_id",
                True,
            ),
            (
                "00000001da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                "balance_id",
                True,
            ),
            (
                "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be",
                "balance_id",
                False,
            ),
            (
                "00000000DA0D57DA7D4850E7FC10D2A9D0EBC731F7AFB40574C03395B17D49149B91F5BE",
                "balance_id",
                False,
            ),
            (
                "00000000da0d57da7d4850e7fc10d2a9d0EBC731F7AFB40574C03395B17D49149B91F5BE",
                "balance_id",
                False,
            ),
        ],
    )
    def test_raise_if_not_valid_balance_id(self, balance_id, argument_name, raise_err):
        if raise_err:
            with pytest.raises(
                ValueError,
                match=f'Value of argument "{argument_name}" is not a valid balance id: {balance_id}',
            ):
                raise_if_not_valid_balance_id(balance_id, argument_name)
        else:
            raise_if_not_valid_balance_id(balance_id, argument_name)
