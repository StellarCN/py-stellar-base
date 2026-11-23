import base64
import re
from decimal import Decimal
from urllib.parse import quote

import pytest

from stellar_sdk import Asset, Keypair, MuxedAccount, Network, strkey
from stellar_sdk.exceptions import BadSignatureError
from stellar_sdk.fee_bump_transaction_envelope import FeeBumpTransactionEnvelope
from stellar_sdk.memo import HashMemo, IdMemo, NoneMemo, ReturnHashMemo, TextMemo
from stellar_sdk.sep.exceptions import InvalidStellarUriError
from stellar_sdk.sep.stellar_uri import (
    PayStellarUri,
    Replacement,
    TransactionStellarUri,
    parse_stellar_uri,
)
from stellar_sdk.transaction_envelope import TransactionEnvelope

SECRET = "SBPOVRVKTTV7W3IOX2FJPSMPCJ5L2WU2YKTP3HCLYPXNI5MDIGREVNYC"
SIGNER = Keypair.from_secret(SECRET)
SIGNING_KEY = SIGNER.public_key
DESTINATION = "GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO"
ISSUER = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
PUBKEY = "GAU2ZSYYEYO5S5ZQSMMUENJ2TANY4FPXYGGIMU6GMGKTNVDG5QYFW6JS"
MUXED = MuxedAccount(DESTINATION, 7).account_muxed
CONTRACT = str(strkey.Contract(bytes(range(32))))
MUXED_CONTRACT = str(strkey.MuxedContract(bytes(range(32)), 7))
PUBLIC = Network.PUBLIC_NETWORK_PASSPHRASE
TESTNET = Network.TESTNET_NETWORK_PASSPHRASE
HASH = bytes.fromhex("218a3ef357324c496d07f7d7b31be5c2a11a1ac44af9b81938a6c5b9c0684af4")

# The signed request of the "Request Signing" example of SEP-7.
SPEC_PAY = "web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.1234567&memo=skdjfasf&memo_type=MEMO_TEXT&msg=pay%20me%20with%20lumens&origin_domain=someDomain.com&signature=tbsLtlK%2FfouvRWk2UWFP47yHYeI1g1NEC%2FfEQvuXG6V8P%2BbeLxplYbOVtTk1g94Wp97cHZ3pVJy%2FtZNYobl3Cw%3D%3D"
# URIs the SDK wrote and signed before its SEP-7 support was rewritten.
PAY_VECTOR = "web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.1234567&asset_code=Hello&asset_issuer=GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF&memo=Hello%20World&memo_type=MEMO_TEXT&callback=url%3Ahttps%3A%2F%2Fexample.com%2Fcallback&msg=pay%20me%20with%20lumens&network_passphrase=Test%20SDF%20Network%20%3B%20September%202015&origin_domain=someDomain.com&signature=k5cDMVTD2W2lKeEGqakjOTf3aPuPumlr8ObBOvauaa2QiXqa7%2Bw9WRgtmo6NaPXdOoFG5ScUIp9k7PdeuPieCw%3D%3D"
PAY_HASH_VECTOR = "web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.1234567&memo=IYo%2B81cyTEltB%2FfXsxvlwqEaGsRK%2BbgZOKbFucBoSvQ%3D&memo_type=MEMO_HASH&msg=pay%20me%20with%20lumens&origin_domain=someDomain.com&signature=CzqyewhypDQGCBlvxSj%2BazIm5iS2GDqcOlBeXT%2FB7s8ogEXC8hNa6HjOArdbTkvNCUvTl6lgyKOj%2FeeNE%2BA5DQ%3D%3D"
PAY_RETURN_VECTOR = "web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.1234567&memo=IYo%2B81cyTEltB%2FfXsxvlwqEaGsRK%2BbgZOKbFucBoSvQ%3D&memo_type=MEMO_RETURN&msg=pay%20me%20with%20lumens&origin_domain=someDomain.com&signature=4OJcgA0qxjUhqJL79MeK%2BkHgNjdKXiGhufvw2yjcXud7Ce%2BG53N0qSUpgXDT8OBDQRrI7Pe%2FUPu0%2FCM7DJkXAQ%3D%3D"
TX_VECTOR = "web+stellar:tx?xdr=AAAAAP%2Byw%2BZEuNg533pUmwlYxfrq6%2FBoMJqiJ8vuQhf6rHWmAAAAZAB8NHAAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABSFVHAAAAAABAH0wIyY3BJBS2qHdRPAV80M8hF7NBpxRjXyjuT9kEbH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAAAAAAAAAA%3D&callback=url%3Ahttps%3A%2F%2FsomeSigningService.com&replace=sourceAccount%3AX%3BX%3Aaccount%20on%20which%20to%20create%20the%20trustline&pubkey=GAU2ZSYYEYO5S5ZQSMMUENJ2TANY4FPXYGGIMU6GMGKTNVDG5QYFW6JS&msg=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&network_passphrase=Test%20SDF%20Network%20%3B%20September%202015&origin_domain=someDomain.com&signature=8uiZ2r7KT3gRsO%2BrzmofGHyl%2FLFMfOgNtx5oOddK2rAy8M%2BOgBYOSQpASNbIm%2BIvZVojxv8tKTYuzOkbyhPODA%3D%3D"
FEE_BUMP_VECTOR = "web+stellar:tx?xdr=AAAABQAAAABDqliFalCjYChydhLNq0lXO8PWMJGrsl8naSePTpNR2wAAAAAAAAGQAAAAAgAAAABzdv3ojkzWHMD7KUoXhrPx0GH18vHKV0ZfqpMiEblG1gAAADIAAAAAAAAwOgAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAGqka26GRAaOmdSR%2B9P28gWFYn%2FiQ3GPQsRGAuT5bF4JAAAAAAAAAAA7msoAAAAAAAAAAAERuUbWAAAAQM7EA7Pnkeyqzpa%2BKgOTDLX66WKBk32BSF4NocSAeOkfUDwIODWvgcToOAH4%2BjaeOqdWhmxjC0mQ0vO3V14u7AwAAAAAAAAAAU6TUdsAAABAt2wuZNUirKyCkv7Sc3B1kk5CUPt7eitpaZjRBpbrW1p8wVIZ6IsaRzzIVHP7YpGhzbPImXkahlolf0IL3sevBA%3D%3D&callback=url%3Ahttps%3A%2F%2FsomeSigningService.com&replace=sourceAccount%3AX%3BX%3Aaccount%20on%20which%20to%20create%20the%20trustline&pubkey=GAU2ZSYYEYO5S5ZQSMMUENJ2TANY4FPXYGGIMU6GMGKTNVDG5QYFW6JS&msg=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&network_passphrase=Test%20SDF%20Network%20%3B%20September%202015&origin_domain=someDomain.com&signature=x968yy0d2uFhx6At2mxd6yK%2F0ZZCz%2F%2FQT%2BmlIXmJwI6xe4RuYVIPZpROVx8HUYtcL9ok%2FrwzlQHnBg%2F%2Ba0YYDg%3D%3D"
TX_XDR = "AAAAAP+yw+ZEuNg533pUmwlYxfrq6/BoMJqiJ8vuQhf6rHWmAAAAZAB8NHAAAAABAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABSFVHAAAAAABAH0wIyY3BJBS2qHdRPAV80M8hF7NBpxRjXyjuT9kEbH//////////AAAAAAAAAAA="
FEE_BUMP_XDR = "AAAABQAAAABDqliFalCjYChydhLNq0lXO8PWMJGrsl8naSePTpNR2wAAAAAAAAGQAAAAAgAAAABzdv3ojkzWHMD7KUoXhrPx0GH18vHKV0ZfqpMiEblG1gAAADIAAAAAAAAwOgAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAGqka26GRAaOmdSR+9P28gWFYn/iQ3GPQsRGAuT5bF4JAAAAAAAAAAA7msoAAAAAAAAAAAERuUbWAAAAQM7EA7Pnkeyqzpa+KgOTDLX66WKBk32BSF4NocSAeOkfUDwIODWvgcToOAH4+jaeOqdWhmxjC0mQ0vO3V14u7AwAAAAAAAAAAU6TUdsAAABAt2wuZNUirKyCkv7Sc3B1kk5CUPt7eitpaZjRBpbrW1p8wVIZ6IsaRzzIVHP7YpGhzbPImXkahlolf0IL3sevBA=="

PAY = f"web+stellar:pay?destination={DESTINATION}"
TX = f"web+stellar:tx?xdr={quote(TX_XDR, safe='')}"
REPLACE = (
    Replacement(
        identifier="X",
        hint="account on which to create the trustline",
        fields=("sourceAccount",),
    ),
)


def envelope(network_passphrase: str = TESTNET) -> TransactionEnvelope:
    return TransactionEnvelope.from_xdr(TX_XDR, network_passphrase)


def invalid(message: str):
    """Expect an `InvalidStellarUriError` whose message holds `message`."""
    return pytest.raises(InvalidStellarUriError, match=re.escape(message))


def sign_text(text: str) -> str:
    """Sign a request as SEP-7 describes, without the code under test."""
    payload = bytes(35) + b"\x04" + b"stellar.sep.7 - URI Scheme" + text.encode()
    signature = base64.b64encode(SIGNER.sign(payload)).decode()
    return f"{text}&signature={quote(signature, safe='')}"


# --- Vectors -------------------------------------------------------------------------


def test_the_signed_example_of_the_sep():
    uri = PayStellarUri(
        DESTINATION,
        amount="120.1234567",
        memo=TextMemo("skdjfasf"),
        message="pay me with lumens",
    )
    signed = uri.sign(SECRET, "someDomain.com")
    assert signed.to_uri() == SPEC_PAY
    signed.verify_signature(SIGNING_KEY)
    assert PayStellarUri.from_uri(SPEC_PAY) == signed


VECTORS = {
    "pay": (
        lambda: PayStellarUri(
            DESTINATION,
            amount="120.1234567",
            asset=Asset("Hello", ISSUER),
            memo=TextMemo("Hello World"),
            callback="https://example.com/callback",
            message="pay me with lumens",
            network_passphrase=TESTNET,
        ),
        PAY_VECTOR,
    ),
    "pay with a hash memo": (
        lambda: PayStellarUri(
            DESTINATION,
            amount="120.1234567",
            memo=HashMemo(HASH),
            message="pay me with lumens",
        ),
        PAY_HASH_VECTOR,
    ),
    "pay with a return memo": (
        lambda: PayStellarUri(
            DESTINATION,
            amount="120.1234567",
            memo=ReturnHashMemo(HASH),
            message="pay me with lumens",
        ),
        PAY_RETURN_VECTOR,
    ),
    "tx": (
        lambda: TransactionStellarUri(
            envelope(),
            replace=REPLACE,
            callback="https://someSigningService.com",
            pubkey=PUBKEY,
            message="a" * 300,
        ),
        TX_VECTOR,
    ),
    "tx with a fee bump": (
        lambda: TransactionStellarUri(
            FeeBumpTransactionEnvelope.from_xdr(FEE_BUMP_XDR, TESTNET),
            replace=REPLACE,
            callback="https://someSigningService.com",
            pubkey=PUBKEY,
            message="a" * 300,
        ),
        FEE_BUMP_VECTOR,
    ),
}


@pytest.mark.parametrize(("build", "vector"), VECTORS.values(), ids=VECTORS.keys())
def test_uris_written_before_the_rewrite(build, vector):
    uri = build().sign(SIGNER, "someDomain.com")
    assert uri.to_uri() == vector
    assert parse_stellar_uri(vector) == uri
    uri.verify_signature(SIGNING_KEY)


# --- What a URI holds ----------------------------------------------------------------


def test_pay_fields():
    uri = PayStellarUri.from_uri(PAY_VECTOR)
    assert uri.destination == DESTINATION
    assert uri.amount == "120.1234567"
    assert uri.asset == Asset("Hello", ISSUER)
    assert uri.memo == TextMemo("Hello World")
    assert uri.callback == "https://example.com/callback"
    assert uri.message == "pay me with lumens"
    assert uri.network_passphrase == TESTNET
    assert uri.origin_domain == "someDomain.com"
    assert uri.signature is not None
    assert uri.signature.startswith("k5cDMVTD2W2lKeEGqakjOTf3aPuPumlr8ObBOvauaa2Q")


def test_pay_defaults():
    uri = PayStellarUri.from_uri(PAY)
    assert uri == PayStellarUri(DESTINATION)
    assert uri.amount is None
    assert uri.asset == Asset.native()
    assert uri.memo == NoneMemo()
    assert uri.callback is None
    assert uri.message is None
    assert uri.network_passphrase == PUBLIC
    assert uri.origin_domain is None
    assert uri.signature is None


def test_tx_fields():
    uri = TransactionStellarUri.from_uri(TX_VECTOR)
    assert uri.xdr == TX_XDR
    assert uri.network_passphrase == TESTNET
    assert uri.replace == REPLACE
    assert uri.callback == "https://someSigningService.com"
    assert uri.pubkey == PUBKEY
    assert uri.chain is None
    assert uri.message == "a" * 300
    assert uri.origin_domain == "someDomain.com"
    transaction_envelope = uri.to_transaction_envelope()
    assert isinstance(transaction_envelope, TransactionEnvelope)
    assert transaction_envelope.to_xdr() == TX_XDR
    assert transaction_envelope.network_passphrase == TESTNET


def test_tx_defaults():
    uri = TransactionStellarUri.from_uri(TX)
    assert uri.replace == ()
    assert uri.callback is None
    assert uri.pubkey is None
    assert uri.chain is None
    assert uri.message is None


def test_tx_with_a_fee_bump():
    uri = TransactionStellarUri.from_uri(FEE_BUMP_VECTOR)
    transaction_envelope = uri.to_transaction_envelope()
    assert isinstance(transaction_envelope, FeeBumpTransactionEnvelope)
    assert transaction_envelope.to_xdr() == FEE_BUMP_XDR


def test_tx_takes_its_network_from_the_envelope():
    testnet = TransactionStellarUri(envelope(TESTNET))
    network = "network_passphrase=Test%20SDF%20Network%20%3B%20September%202015"
    assert testnet.to_uri() == f"{TX}&{network}"
    assert testnet.network_passphrase == TESTNET
    assert TransactionStellarUri(envelope(PUBLIC)).to_uri() == TX
    # A URI without `network_passphrase` is for the public network.
    public = TransactionStellarUri.from_uri(TX)
    assert public.network_passphrase == PUBLIC
    assert public.to_transaction_envelope().network_passphrase == PUBLIC


def test_uris_cannot_be_changed():
    asset = Asset("USD", ISSUER)
    uri = PayStellarUri(DESTINATION, amount="1", asset=asset)
    attribute = "amount"
    with pytest.raises(AttributeError):
        setattr(uri, attribute, "1000")
    # Nor by changing what the caller passed in.
    asset.code = "EUR"
    assert uri.asset == Asset("USD", ISSUER)
    assert uri.to_uri() == f"{PAY}&amount=1&asset_code=USD&asset_issuer={ISSUER}"


def test_tx_keeps_the_envelope_as_it_was_given():
    transaction_envelope = envelope()
    uri = TransactionStellarUri(transaction_envelope)
    transaction_envelope.sign(SIGNER)
    assert uri.xdr == TX_XDR
    # Each call gives another envelope, for the wallet to sign.
    signed = uri.to_transaction_envelope()
    signed.sign(SIGNER)
    assert signed.to_xdr() == transaction_envelope.to_xdr()
    assert uri.to_transaction_envelope().to_xdr() == TX_XDR


def test_uris_are_equal_when_their_text_is():
    uri = PayStellarUri(DESTINATION, message="pay me")
    same = PayStellarUri.from_uri(uri.to_uri())
    assert uri == same
    assert hash(uri) == hash(same)
    assert len({uri, same, PayStellarUri(DESTINATION)}) == 2
    # The same request written another way is another text.
    other = PayStellarUri.from_uri(f"{PAY}&msg=pay+me")
    assert other.message == uri.message
    assert other != uri
    assert uri != uri.to_uri()
    assert TransactionStellarUri.from_uri(TX) != uri
    assert (
        len({TransactionStellarUri.from_uri(TX), TransactionStellarUri.from_uri(TX)})
        == 1
    )


def test_parse_stellar_uri():
    assert isinstance(parse_stellar_uri(PAY), PayStellarUri)
    assert isinstance(parse_stellar_uri(TX), TransactionStellarUri)
    with invalid("The URI is neither a `pay` nor a `tx` request."):
        parse_stellar_uri(f"web+stellar:payment?destination={DESTINATION}")
    with invalid("The URI doesn't start with `web+stellar:`."):
        parse_stellar_uri("https://example.org")


# --- Reading a URI -------------------------------------------------------------------


def test_what_a_received_uri_may_hold():
    # Parameters in any order, `+` for a space, and parameters the SDK doesn't know,
    # even repeated ones. The text is kept as it came.
    text = (
        "web+stellar:pay?msg=pay+me&invoice=42&tag=a&tag=b"
        f"&destination={DESTINATION}&&amount=1"
    )
    uri = PayStellarUri.from_uri(text)
    assert (uri.destination, uri.message, uri.amount) == (DESTINATION, "pay me", "1")
    assert uri.to_uri() == text


def test_an_empty_value_is_a_value():
    assert PayStellarUri.from_uri(f"{PAY}&msg=").message == ""
    assert PayStellarUri(DESTINATION, message="").to_uri() == f"{PAY}&msg="


INVALID_PAY = [
    (f"stellar:pay?destination={DESTINATION}", "The URI doesn't start with"),
    (TX, "The URI is not a `pay` request."),
    ("web+stellar:pay", "`destination` is missing."),
    (f"{PAY}&destination={DESTINATION}", "`destination` is given more than once."),
    (f"{PAY}&msg=a#b", "The URI has a `#`"),
    (f"{PAY}&msg=%E9", "is not UTF-8 when its percent-encoding is decoded: 'msg=%E9'"),
    (f"{PAY}&msg={'a' * 301}", "`msg` is longer than 300 characters."),
    (f"{PAY}&callback=https%3A%2F%2Fexample.com", "`callback` must be `url:`"),
    (f"{PAY}&callback=url%3A", "`callback` must be `url:`"),
    (f"{PAY}&callback=", "`callback` must be `url:`"),
    (f"{PAY}&network_passphrase=", "`network_passphrase` is empty."),
    ("web+stellar:pay?destination=alice", "`destination` is not an account"),
    ("web+stellar:pay?destination=alice*", "`destination` is not an account"),
    ("web+stellar:pay?destination=*example.com", "`destination` is not an account"),
    ("web+stellar:pay?destination=a*b*example.com", "`destination` is not an"),
    # `+` is a space, which a federation name can't have.
    ("web+stellar:pay?destination=+1415*example.com", "`destination` is not an"),
    ("web+stellar:pay?destination=a%3Eb*example.com", "`destination` is not an"),
    ("web+stellar:pay?destination=a%00b*example.com", "`destination` is not an"),
    (f"web+stellar:pay?destination={SECRET}", "`destination` is not an account"),
    ("web+stellar:pay?destination=", "`destination` is not an account"),
    (f"{PAY}&amount=", "`amount` is not a number with at most"),
    (f"{PAY}&amount=abc", "`amount` is not a number with at most"),
    (f"{PAY}&amount=1E-7", "`amount` is not a number with at most"),
    (f"{PAY}&amount=1_000", "`amount` is not a number with at most"),
    (f"{PAY}&amount=-1", "`amount` is not a number with at most"),
    (f"{PAY}&amount=%2B1", "`amount` is not a number with at most"),
    (f"{PAY}&amount=1.", "`amount` is not a number with at most"),
    (f"{PAY}&amount=.5", "`amount` is not a number with at most"),
    (f"{PAY}&amount=0", "`amount` must be above zero."),
    (f"{PAY}&amount=0.0", "`amount` must be above zero."),
    (f"{PAY}&amount=1.00000001", "`amount` is not a number with at most"),
    (f"{PAY}&amount=1.00000000", "`amount` is not a number with at most"),
    (f"{PAY}&amount=1.{'0' * 27}1", "`amount` is not a number with at most"),
    (f"{PAY}&amount=922337203685.4775808", "`amount` is invalid"),
    (f"{PAY}&asset_issuer={ISSUER}", "`asset_issuer` is given without `asset_code`."),
    (f"{PAY}&asset_code=USD", "`asset_code` or `asset_issuer` is invalid"),
    (f"{PAY}&asset_code=USD&asset_issuer=alice", "`asset_code` or `asset_issuer`"),
    (f"{PAY}&asset_code=&asset_issuer={ISSUER}", "`asset_code` or `asset_issuer`"),
    (f"{PAY}&memo_type=MEMO_TEXT", "`memo_type` is given without `memo`."),
    (f"{PAY}&memo=a&memo_type=MEMO_TXT", "`memo_type` is not a memo type"),
    (f"{PAY}&memo={'a' * 29}", "`memo` is not a valid MEMO_TEXT"),
    (f"{PAY}&memo=1_000&memo_type=MEMO_ID", "`memo` is not a valid MEMO_ID"),
    (f"{PAY}&memo=-1&memo_type=MEMO_ID", "`memo` is not a valid MEMO_ID"),
    (f"{PAY}&memo={2**64}&memo_type=MEMO_ID", "`memo` is not a valid MEMO_ID"),
    (f"{PAY}&memo=abc&memo_type=MEMO_HASH", "`memo` is not a valid MEMO_HASH"),
    (f"{PAY}&memo=AAAA&memo_type=MEMO_RETURN", "`memo` is not a valid MEMO_RETURN"),
    (f"web+stellar:pay?destination={CONTRACT}&memo=hi", "`memo` can't be given"),
    (f"web+stellar:pay?destination={MUXED_CONTRACT}&memo=hi", "`memo` can't be"),
    (f"{PAY}&origin_domain=example.org", "`origin_domain` and `signature` must"),
    (f"{PAY}&signature=abc", "`origin_domain` and `signature` must be given"),
]


@pytest.mark.parametrize(("uri", "message"), INVALID_PAY)
def test_invalid_pay_uri(uri, message):
    with invalid(message):
        PayStellarUri.from_uri(uri)


@pytest.mark.parametrize(
    "destination", [DESTINATION, MUXED, CONTRACT, MUXED_CONTRACT, "alice*example.com"]
)
def test_pay_destinations(destination):
    uri = PayStellarUri(destination)
    assert uri.destination == destination
    assert PayStellarUri.from_uri(uri.to_uri()) == uri


def test_pay_federation_address_of_a_phone_number():
    uri = PayStellarUri("+14155550100*example.com")
    assert uri.to_uri() == "web+stellar:pay?destination=%2B14155550100%2Aexample.com"
    assert uri.destination == "+14155550100*example.com"


@pytest.mark.parametrize(
    "amount", ["1", "0.0000001", "1.50", "1.0000000", "922337203685.4775807"]
)
def test_pay_amounts(amount):
    assert PayStellarUri.from_uri(f"{PAY}&amount={amount}").amount == amount
    assert PayStellarUri(DESTINATION, amount=amount).amount == amount


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        # str() writes these with an exponent.
        (Decimal("0.0000001"), "0.0000001"),
        (Decimal("100").normalize(), "100"),
        (Decimal("1E+11"), "100000000000"),
        (Decimal("1.23E+3"), "1230"),
        # str() writes these plain, whether given with an exponent or not.
        (Decimal("1.2E-6"), "0.0000012"),
        (Decimal("9.223372036854775807E+11"), "922337203685.4775807"),
        (Decimal("922337203685.4775807"), "922337203685.4775807"),
        (Decimal("12.3400"), "12.3400"),
        (Decimal("5"), "5"),
    ],
)
def test_pay_decimal_amount_is_written_without_an_exponent(amount, expected):
    uri = PayStellarUri(DESTINATION, amount=amount)
    assert uri.amount == expected
    assert uri.to_uri() == f"{PAY}&amount={expected}"


def test_pay_assets():
    credit = PayStellarUri(DESTINATION, asset=Asset("USD", ISSUER))
    assert credit.to_uri() == f"{PAY}&asset_code=USD&asset_issuer={ISSUER}"
    assert credit.asset == Asset("USD", ISSUER)
    assert PayStellarUri(DESTINATION, asset=Asset.native()).to_uri() == PAY
    # `asset_code=XLM` alone is the native asset; with an issuer, an asset of that code.
    assert PayStellarUri.from_uri(f"{PAY}&asset_code=XLM").asset == Asset.native()
    issued = Asset("XLM", ISSUER)
    assert PayStellarUri(DESTINATION, asset=issued).asset == issued


@pytest.mark.parametrize(
    ("memo", "query"),
    [
        (TextMemo("Hello World"), "memo=Hello%20World&memo_type=MEMO_TEXT"),
        (TextMemo("café"), "memo=caf%C3%A9&memo_type=MEMO_TEXT"),
        (TextMemo(""), "memo=&memo_type=MEMO_TEXT"),
        (IdMemo(2**64 - 1), "memo=18446744073709551615&memo_type=MEMO_ID"),
        (
            HashMemo(HASH),
            "memo=IYo%2B81cyTEltB%2FfXsxvlwqEaGsRK%2BbgZOKbFucBoSvQ%3D&memo_type=MEMO_HASH",
        ),
        (
            ReturnHashMemo(HASH),
            "memo=IYo%2B81cyTEltB%2FfXsxvlwqEaGsRK%2BbgZOKbFucBoSvQ%3D&memo_type=MEMO_RETURN",
        ),
    ],
)
def test_pay_memos(memo, query):
    uri = PayStellarUri(DESTINATION, memo=memo)
    assert uri.to_uri() == f"{PAY}&{query}"
    assert uri.memo == memo
    assert PayStellarUri.from_uri(uri.to_uri()).memo == memo


def test_pay_without_a_memo():
    assert PayStellarUri(DESTINATION, memo=NoneMemo()).to_uri() == PAY
    assert PayStellarUri.from_uri(PAY).memo == NoneMemo()


def test_pay_memo_without_a_type_is_text():
    # SEP-7 names no default, and other SDKs write text memos this way.
    assert PayStellarUri.from_uri(f"{PAY}&memo=12345").memo == TextMemo("12345")


def test_pay_arguments_that_cannot_be_written():
    with invalid("`amount` is not a number with at most 7 decimal places: '1E-7'"):
        PayStellarUri(DESTINATION, amount="1E-7")
    with invalid("`msg` is longer than 300 characters."):
        PayStellarUri(DESTINATION, message="a" * 301)
    with invalid("`memo` can't be given with a contract `destination`"):
        PayStellarUri(CONTRACT, memo=TextMemo("hi"))
    with invalid("A text memo that isn't UTF-8 can't be written to a URI."):
        PayStellarUri(DESTINATION, memo=TextMemo(b"\xe9"))
    with pytest.raises(TypeError, match="`memo` must be a Memo"):
        PayStellarUri(DESTINATION, memo="hello")  # type: ignore[arg-type]


INVALID_TX = [
    (PAY, "The URI is not a `tx` request."),
    ("web+stellar:tx?callback=url%3Ahttps%3A%2F%2Fexample.com", "`xdr` is missing."),
    ("web+stellar:tx?xdr=AAAA", "`xdr` is not a transaction envelope"),
    ("web+stellar:tx?xdr=", "`xdr` is not a transaction envelope"),
    (f"{TX}&xdr=AAAA", "`xdr` is given more than once."),
    (f"{TX}&pubkey=alice", "`pubkey` is not an account"),
    (f"{TX}&pubkey={MUXED}", "`pubkey` is not an account"),
    (f"{TX}&chain=invoice-238", "`chain` is not a `web+stellar:` URI."),
    (f"{TX}&msg={'a' * 301}", "`msg` is longer than 300 characters."),
    (f"{TX}&origin_domain=example.org", "`origin_domain` and `signature` must"),
]


@pytest.mark.parametrize(("uri", "message"), INVALID_TX)
def test_invalid_tx_uri(uri, message):
    with invalid(message):
        TransactionStellarUri.from_uri(uri)


# --- Signing -------------------------------------------------------------------------


def test_sign_returns_a_signed_copy():
    uri = PayStellarUri(DESTINATION, amount="1")
    signed = uri.sign(SIGNER, "example.org")
    assert uri.origin_domain is None
    assert uri.signature is None
    unsigned = f"{PAY}&amount=1&origin_domain=example.org"
    assert signed.to_uri() == sign_text(unsigned)
    assert signed.origin_domain == "example.org"
    assert signed == uri.sign(SECRET, "example.org")
    signed.verify_signature(SIGNING_KEY)


def test_a_uri_signed_elsewhere_verifies():
    # Another signer may order and encode the parameters its own way, and add some.
    text = sign_text(
        "web+stellar:pay?msg=Hello+(world)!&invoice=42"
        f"&destination={DESTINATION}&origin_domain=example.org"
    )
    uri = PayStellarUri.from_uri(text)
    uri.verify_signature(SIGNING_KEY)
    assert uri.message == "Hello (world)!"
    assert uri.to_uri() == text


def test_the_signature_may_be_anywhere():
    signed = sign_text(f"{PAY}&invoice_signature=42&origin_domain=example.org")
    signature = signed.rpartition("&")[2].replace("signature=", "%73ignature=")
    first = (
        f"web+stellar:pay?{signature}&destination={DESTINATION}"
        "&invoice_signature=42&origin_domain=example.org"
    )
    PayStellarUri.from_uri(first).verify_signature(SIGNING_KEY)


def test_signing_a_received_uri_keeps_its_text():
    received = sign_text(
        f"web+stellar:pay?msg=pay+me&invoice=42&destination={DESTINATION}"
        "&origin_domain=example.org"
    )
    signed = PayStellarUri.from_uri(received).sign(SIGNER, "example.com")
    assert signed.to_uri() == sign_text(
        f"web+stellar:pay?msg=pay+me&invoice=42&destination={DESTINATION}"
        "&origin_domain=example.com"
    )
    signed.verify_signature(SIGNING_KEY)


def test_a_changed_uri_does_not_verify():
    signed = PayStellarUri(DESTINATION, amount="1").sign(SIGNER, "example.org").to_uri()
    for changed in (
        signed.replace("amount=1", "amount=1000"),
        signed.replace("example.org", "example.com"),
        f"{signed}&invoice=42",
    ):
        with pytest.raises(BadSignatureError, match="Signature verification failed"):
            PayStellarUri.from_uri(changed).verify_signature(SIGNING_KEY)
    with invalid("`amount` is given more than once."):
        PayStellarUri.from_uri(f"{signed}&amount=1000")
    with pytest.raises(BadSignatureError, match="Signature verification failed"):
        PayStellarUri.from_uri(signed).verify_signature(DESTINATION)


def test_the_signature_covers_the_text_not_what_it_means():
    signed = sign_text(f"{PAY}&msg=pay+me&origin_domain=example.org")
    PayStellarUri.from_uri(signed).verify_signature(SIGNING_KEY)
    # The same message, spelled another way.
    respelled = PayStellarUri.from_uri(signed.replace("pay+me", "pay%20me"))
    assert respelled.message == "pay me"
    with pytest.raises(BadSignatureError, match="Signature verification failed"):
        respelled.verify_signature(SIGNING_KEY)


def test_verify_signature_needs_a_signature():
    with pytest.raises(BadSignatureError, match="The URI is not signed"):
        PayStellarUri(DESTINATION).verify_signature(SIGNING_KEY)
    # The key is read from a stellar.toml, which may hold anything.
    with pytest.raises(BadSignatureError, match="`signing_key` is not a public key"):
        PayStellarUri.from_uri(SPEC_PAY).verify_signature(SIGNING_KEY[:-1])
    for signature in ("abc", "%C3%A9", "AAAA"):
        text = f"{PAY}&origin_domain=example.org&signature={signature}"
        with pytest.raises(BadSignatureError, match="not a signature"):
            PayStellarUri.from_uri(text).verify_signature(SIGNING_KEY)


@pytest.mark.parametrize(
    "domain",
    [
        "example.org",
        "example.org.",
        "sub.example.co.uk",
        "bücher.de",
        "xn--p1ai.xn--p1ai",
    ],
)
def test_origin_domains(domain):
    uri = PayStellarUri(DESTINATION).sign(SIGNER, domain)
    assert uri.origin_domain == domain
    uri.verify_signature(SIGNING_KEY)


@pytest.mark.parametrize(
    "domain",
    [
        "localhost",
        "127.0.0.1",
        "1.0x7f",
        "127.0.0.1:8080/x?",
        "user@example.org",
        "exa mple.org",
        "-a.example.org",
        "example..org",
        f"{'a' * 64}.org",
        "",
    ],
)
def test_invalid_origin_domains(domain):
    # A wallet fetches the stellar.toml of this domain, so it must be a domain name.
    with invalid("`origin_domain` is not a domain name"):
        PayStellarUri(DESTINATION).sign(SIGNER, domain)
    with invalid("`origin_domain` is not a domain name"):
        PayStellarUri.from_uri(
            f"{PAY}&origin_domain={quote(domain, safe='')}&signature=abc"
        )


def test_tx_chain():
    inner = PayStellarUri(DESTINATION, amount="1").sign(SIGNER, "example.org")
    outer = TransactionStellarUri(
        envelope(), callback="https://multisig.example/cb", chain=inner.to_uri()
    ).sign(SIGNER, "multisig.example")
    received = TransactionStellarUri.from_uri(outer.to_uri())
    received.verify_signature(SIGNING_KEY)
    # The chained request is kept as its text, for the wallet to read if it wants.
    assert received.chain is not None
    assert received.chain == inner.to_uri()
    chained = parse_stellar_uri(received.chain)
    chained.verify_signature(SIGNING_KEY)
    assert chained == inner


# --- Replacements --------------------------------------------------------------------

SPEC_REPLACE = (
    "sourceAccount:X,operations[0].sourceAccount:Y,operations[1].destination:Y;"
    "X:account from where you want to pay fees,"
    "Y:account that needs the trustline and which will receive the new tokens"
)


def test_replace_of_the_sep():
    replace = (
        Replacement(
            identifier="X",
            hint="account from where you want to pay fees",
            fields=("sourceAccount",),
        ),
        Replacement(
            identifier="Y",
            hint="account that needs the trustline and which will receive the new tokens",
            fields=("operations[0].sourceAccount", "operations[1].destination"),
        ),
    )
    text = f"{TX}&replace={quote(SPEC_REPLACE, safe='')}"
    assert TransactionStellarUri.from_uri(text).replace == replace
    assert TransactionStellarUri(envelope(PUBLIC), replace=replace).to_uri() == text


def test_replace_hints_may_hold_colons_and_semicolons():
    replace = [
        Replacement(identifier="X", hint="time: now; or later", fields=["seqNum"])
    ]
    uri = TransactionStellarUri(envelope(), replace=replace)
    assert TransactionStellarUri.from_uri(uri.to_uri()).replace == tuple(replace)
    assert uri.replace[0].fields == ("seqNum",)


@pytest.mark.parametrize(
    ("replace", "message"),
    [
        ("sourceAccount:X", "`replace` has no `;`"),
        ("", "`replace` has no `;`"),
        # The example SEP-7 gives of identifiers that aren't balanced.
        ("sourceAccount:X;Y:The account", "`replace` must have the same identifiers"),
        ("sourceAccount:X;X:a,Y:b", "`replace` must have the same identifiers"),
        ("sourceAccount:X,seqNum:Y;X:a", "`replace` must have the same identifiers"),
        ("sourceAccount:X;X:a,X:b", "`replace` gives the identifier 'X' more than"),
        ("sourceAccount:X,sourceAccount:X;X:a", "`replace` names the field"),
        ("sourceAccount;X:a", "`replace` has an invalid field: 'sourceAccount'"),
        # A comma can't be told from the one between two hints.
        ("sourceAccount:X;X:pay, please", "`replace` has an invalid hint: ' please'"),
        (":X;X:a", "A replacement needs an identifier and fields."),
        ("sourceAccount:;:a", "A replacement needs an identifier and fields."),
        ("memo._present:X;X:a", "`replace` can't name the field 'memo._present'"),
        ("operations.len:X;X:a", "`replace` can't name the field 'operations.len'"),
    ],
)
def test_invalid_replace(replace, message):
    with invalid(message):
        TransactionStellarUri.from_uri(f"{TX}&replace={quote(replace, safe='')}")


def test_replacements_that_cannot_be_written():
    def replacement(**changes):
        values = {"identifier": "X", "hint": "payer", "fields": ("sourceAccount",)}
        return Replacement(**{**values, **changes})

    for changes, message in [
        ({"identifier": ""}, "A replacement needs an identifier and fields."),
        ({"fields": ()}, "A replacement needs an identifier and fields."),
        ({"fields": ("",)}, "A replacement needs an identifier and fields."),
        ({"identifier": "X:Y"}, "can't contain `:`, `,` or `;`: 'X:Y'"),
        ({"fields": ("a,b",)}, "can't contain `:`, `,` or `;`: 'a,b'"),
        ({"fields": ("a;b",)}, "can't contain `:`, `,` or `;`: 'a;b'"),
        ({"hint": "pay, please"}, "A hint can't contain `,`: 'pay, please'"),
        ({"fields": ("memo._present",)}, "can't name the field 'memo._present'"),
    ]:
        with invalid(message):
            replacement(**changes)
    # That rule is for the fields: an identifier is a name of the sender's choosing.
    assert replacement(identifier="account.len").identifier == "account.len"
    # The arguments had another order before, and a string is a sequence too.
    with pytest.raises(TypeError):
        Replacement("sourceAccount", "X", "payer")  # type: ignore[misc]
    with pytest.raises(TypeError, match="`fields` is a sequence of field names"):
        replacement(fields="sourceAccount")
    payer = replacement()
    with invalid("`replace` gives the identifier 'X' more than one hint."):
        TransactionStellarUri(
            envelope(), replace=[payer, replacement(hint="other", fields=("seqNum",))]
        )
    with invalid("`replace` names the field 'sourceAccount' more than once."):
        TransactionStellarUri(envelope(), replace=[payer, replacement(identifier="Y")])


def test_replacement_equal():
    assert REPLACE[0] == Replacement(
        identifier="X",
        hint="account on which to create the trustline",
        fields=["sourceAccount"],
    )
    assert REPLACE[0] != Replacement(identifier="X", hint="", fields=["sourceAccount"])
    assert len({REPLACE[0], REPLACE[0]}) == 1
