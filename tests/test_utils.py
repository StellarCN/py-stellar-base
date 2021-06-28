import pytest

from stellar_sdk.exceptions import NoApproximationError, TypeError
from stellar_sdk.strkey import StrKey
from stellar_sdk.utils import (
    best_rational_approximation,
    hex_to_bytes,
    urljoin_with_query,
    parse_ed25519_account_id_from_muxed_account_xdr_object,
)
from stellar_sdk import xdr as stellar_xdr


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

    @pytest.mark.parametrize("input_value", [12, None])
    def test_hex_to_bytes_type_raise(self, input_value):
        with pytest.raises(
            TypeError,
            match="`hex_string` should be a 32 byte hash or hex encoded string.",
        ):
            hex_to_bytes(input_value)

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

    def test_parse_ed25519_account_id_from_muxed_account_xdr_object_ed25519(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        muxed = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
            ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(account_id)),
        )
        assert (
            parse_ed25519_account_id_from_muxed_account_xdr_object(muxed) == account_id
        )

    def test_parse_ed25519_account_id_from_muxed_account_xdr_object_muxed_account(self):
        account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
        ed25519 = StrKey.decode_ed25519_public_key(account_id)
        id = 1234
        med25519 = stellar_xdr.MuxedAccountMed25519(
            id=stellar_xdr.Uint64(id), ed25519=stellar_xdr.Uint256(ed25519)
        )
        muxed = stellar_xdr.MuxedAccount(
            type=stellar_xdr.CryptoKeyType.KEY_TYPE_MUXED_ED25519, med25519=med25519
        )
        assert (
            parse_ed25519_account_id_from_muxed_account_xdr_object(muxed) == account_id
        )
