from collections.abc import AsyncIterator

import pytest
from pytest_httpserver import HTTPServer

from stellar_sdk import (
    Account,
    AiohttpClient,
    Asset,
    Keypair,
    Network,
    Server,
    ServerAsync,
    TransactionBuilder,
)
from stellar_sdk.exceptions import BadRequestError
from stellar_sdk.sep.exceptions import AccountRequiresMemoError
from stellar_sdk.transaction_envelope import TransactionEnvelope
from tests.helpers import resolve

KEYPAIR = Keypair.from_secret(
    "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
)
BTC = Asset("BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2")

MEMO_REQUIRED_A = "GCMDQXJJGQE6TJ5XUHJMJUUIWECC5S6VANRAOWIQMMV4ALW43JOY2SEB"
MEMO_REQUIRED_B = "GDUR2DMT5AQ7DJUGBIBB45NKRNQXGRJTWTQ7DPRP37EKBELSMK57RMZK"
MEMO_REQUIRED_C = "GCS36NBLT6OKYN5EUQOQ7ZZIM6WXXNX5ME4JGTCG3HVZOYXRRMNUHNMM"
MEMO_REQUIRED_D = "GAKQNN6GNGNPLYBVEDCD5QAIEHAZVNCQET3HAUR4YWQAP5RPBLU2W7UG"
NO_MEMO_REQUIRED = "GDYC2D4P2SRC5DCEDDK2OUFESSPCTZYLDOEF6NYHR2T7X5GUTEABCQC2"
NOT_FOUND = "GD2OVSQPGD5FBJPMW4YN3FGDJ7JDFKNOMJT35T4H52FLHXJK5MFSR5RA"
FETCH_ERROR = "GB7WNQUTDLD6YJ4MR3KQN3Y6ZIDIGTA7GRKNH47HOGMP2ETFGRSLD6OG"

SUCCESS_TRANSACTION_RESPONSE = {
    "_links": {
        "transaction": {
            "href": "https://horizon.stellar.org/transactions/1c5e36aa26d2f26e80f886ed05d58cbed75d3b40f1d94cea7fcd804c9154183f"
        }
    },
    "hash": "1c5e36aa26d2f26e80f886ed05d58cbed75d3b40f1d94cea7fcd804c9154183f",
    "ledger": 28916099,
    "envelope_xdr": "AAAAAKWf3Ku1NA5YWP+QuXt13+a6Z+Nj4mw9QkPuTxa8uTLpAAAAZAExaGoAAABEAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAA/A3VgdrrNXg/PCe/EBfZDHjYt9pfY6f5TtWc+Uej6agAAAABRFJBAAAAAACSqQIEEE0lvhYFPsJxdYVz5AxNoDraze8VLZsFvaBKywAAAAAACIuAAAAAAAAAAAG8uTLpAAAAQDiVRV8laDbHy/EG6AXhkMOD5AICcTRZYQPw37C3I2DBCWRrjS3r+nsm+C20dqXNrzIYT1G77KFZcBzSis0YCQc=",
    "result_xdr": "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAA=",
    "result_meta_xdr": "AAAAAQAAAAIAAAADAbk5gwAAAAAAAAAApZ/cq7U0DlhY/5C5e3Xf5rpn42PibD1CQ+5PFry5MukAAAAAAPQJcAExaGoAAABDAAAAAQAAAAEAAAAANlpgrn2zruLzED+4q1QzmnE7X3HhGRq7qInv0I8hSDEAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAbk5gwAAAAAAAAAApZ/cq7U0DlhY/5C5e3Xf5rpn42PibD1CQ+5PFry5MukAAAAAAPQJcAExaGoAAABEAAAAAQAAAAEAAAAANlpgrn2zruLzED+4q1QzmnE7X3HhGRq7qInv0I8hSDEAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAABAAAAAMBuTmDAAAAAQAAAAD8DdWB2us1eD88J78QF9kMeNi32l9jp/lO1Zz5R6PpqAAAAAFEUkEAAAAAAJKpAgQQTSW+FgU+wnF1hXPkDE2gOtrN7xUtmwW9oErLAAAAADLqDsB85mxQ4oQAAAAAAAEAAAAAAAAAAAAAAAEBuTmDAAAAAQAAAAD8DdWB2us1eD88J78QF9kMeNi32l9jp/lO1Zz5R6PpqAAAAAFEUkEAAAAAAJKpAgQQTSW+FgU+wnF1hXPkDE2gOtrN7xUtmwW9oErLAAAAADLymkB85mxQ4oQAAAAAAAEAAAAAAAAAAAAAAAMBuCrnAAAAAQAAAACln9yrtTQOWFj/kLl7dd/mumfjY+JsPUJD7k8WvLky6QAAAAFEUkEAAAAAAJKpAgQQTSW+FgU+wnF1hXPkDE2gOtrN7xUtmwW9oErLAAAAAAYNrsB//////////wAAAAEAAAAAAAAAAAAAAAEBuTmDAAAAAQAAAACln9yrtTQOWFj/kLl7dd/mumfjY+JsPUJD7k8WvLky6QAAAAFEUkEAAAAAAJKpAgQQTSW+FgU+wnF1hXPkDE2gOtrN7xUtmwW9oErLAAAAAAYFI0B//////////wAAAAEAAAAAAAAAAA==",
}


def _account_check_requests(httpserver: HTTPServer) -> list[str]:
    """Paths of the GET /accounts/... memo-requirement checks actually issued."""
    return [
        request.path
        for request, _ in httpserver.log
        if request.method == "GET" and request.path.startswith("/accounts/")
    ]


def _inject_mock_server(httpserver: HTTPServer) -> None:
    memo_required_response = {"data": {"config.memo_required": "MQ=="}}
    no_memo_required_response: dict[str, dict[str, str]] = {"data": {}}
    for account_id in (
        MEMO_REQUIRED_A,
        MEMO_REQUIRED_B,
        MEMO_REQUIRED_C,
        MEMO_REQUIRED_D,
    ):
        httpserver.expect_request(f"/accounts/{account_id}").respond_with_json(
            memo_required_response
        )
    httpserver.expect_request(f"/accounts/{NO_MEMO_REQUIRED}").respond_with_json(
        no_memo_required_response
    )
    httpserver.expect_request(f"/accounts/{NOT_FOUND}").respond_with_data("", 404)
    httpserver.expect_request(f"/accounts/{FETCH_ERROR}").respond_with_data("", 400)
    httpserver.expect_request("/transactions").respond_with_json(
        SUCCESS_TRANSACTION_RESPONSE
    )


@pytest.fixture(params=["sync", "async"])
async def memo_server(
    request: pytest.FixtureRequest, httpserver: HTTPServer
) -> AsyncIterator[Server | ServerAsync]:
    _inject_mock_server(httpserver)
    horizon_url = httpserver.url_for("/")
    if request.param == "sync":
        with Server(horizon_url) as server:
            yield server
    else:
        async with ServerAsync(horizon_url, AiohttpClient()) as server:
            yield server


def build_transaction(
    payment_dest: str,
    path_payment_receive_dest: str,
    path_payment_send_dest: str,
    account_merge_dest: str,
    memo: str | None = None,
) -> TransactionEnvelope:
    builder = (
        TransactionBuilder(Account(KEYPAIR.public_key, 1))
        .append_payment_op(payment_dest, Asset.native(), "10")
        .append_path_payment_strict_receive_op(
            path_payment_receive_dest, Asset.native(), "10", BTC, "1", []
        )
        .append_path_payment_strict_send_op(
            path_payment_send_dest, Asset.native(), "10", BTC, "1", []
        )
        .append_account_merge_op(account_merge_dest)
    )
    if memo is not None:
        builder.add_text_memo(memo)
    transaction = builder.build()
    transaction.sign(KEYPAIR)
    return transaction


class TestAccountMemoRequirements:
    async def test_check_memo_required_with_memo(self, memo_server, httpserver):
        transaction = build_transaction(
            MEMO_REQUIRED_A,
            MEMO_REQUIRED_B,
            MEMO_REQUIRED_C,
            MEMO_REQUIRED_D,
            memo="hello, world",
        )
        resp = await resolve(memo_server.submit_transaction(transaction))
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]
        # A transaction with a memo skips the per-destination account checks.
        assert _account_check_requests(httpserver) == []

    async def test_check_memo_required_with_payment_skip_check(
        self, memo_server, httpserver
    ):
        transaction = build_transaction(
            MEMO_REQUIRED_A, MEMO_REQUIRED_B, MEMO_REQUIRED_C, MEMO_REQUIRED_D
        )
        resp = await resolve(memo_server.submit_transaction(transaction, True))
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]
        assert _account_check_requests(httpserver) == []

    @pytest.mark.parametrize(
        ("destinations", "expected_account_id", "expected_operation_index"),
        [
            pytest.param(
                (MEMO_REQUIRED_A, MEMO_REQUIRED_B, MEMO_REQUIRED_C, MEMO_REQUIRED_D),
                MEMO_REQUIRED_A,
                0,
                id="payment",
            ),
            pytest.param(
                (NO_MEMO_REQUIRED, MEMO_REQUIRED_B, MEMO_REQUIRED_C, MEMO_REQUIRED_D),
                MEMO_REQUIRED_B,
                1,
                id="path_payment_strict_receive",
            ),
            pytest.param(
                (NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, MEMO_REQUIRED_C, MEMO_REQUIRED_D),
                MEMO_REQUIRED_C,
                2,
                id="path_payment_strict_send",
            ),
            pytest.param(
                (NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, MEMO_REQUIRED_D),
                MEMO_REQUIRED_D,
                3,
                id="account_merge",
            ),
        ],
    )
    async def test_check_memo_required_raise(
        self,
        memo_server,
        destinations,
        expected_account_id,
        expected_operation_index,
    ):
        transaction = build_transaction(*destinations)
        with pytest.raises(
            AccountRequiresMemoError,
            match=r"Destination account requires a memo in the transaction.",
        ) as err:
            await resolve(memo_server.submit_transaction(transaction))
        assert err.value.account_id == expected_account_id
        assert err.value.operation_index == expected_operation_index

    async def test_check_memo_required_checks_each_destination_once(
        self, memo_server, httpserver
    ):
        """A destination repeated across operations is only fetched once."""
        transaction = build_transaction(
            NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, MEMO_REQUIRED_D
        )
        with pytest.raises(
            AccountRequiresMemoError,
            match=r"Destination account requires a memo in the transaction.",
        ) as err:
            await resolve(memo_server.submit_transaction(transaction))
        assert err.value.account_id == MEMO_REQUIRED_D
        assert err.value.operation_index == 3
        assert _account_check_requests(httpserver) == [
            f"/accounts/{NO_MEMO_REQUIRED}",
            f"/accounts/{MEMO_REQUIRED_D}",
        ]

    async def test_check_memo_required_with_no_destination_operation(
        self, memo_server, httpserver
    ):
        transaction = (
            TransactionBuilder(Account(KEYPAIR.public_key, 1))
            .append_manage_data_op("Hello", "world")
            .build()
        )
        transaction.sign(KEYPAIR)
        resp = await resolve(memo_server.submit_transaction(transaction))
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]
        assert _account_check_requests(httpserver) == []

    async def test_check_memo_required_with_account_not_found(
        self, memo_server, httpserver
    ):
        transaction = build_transaction(NOT_FOUND, NOT_FOUND, NOT_FOUND, NOT_FOUND)
        resp = await resolve(memo_server.submit_transaction(transaction))
        # Unknown destinations are treated as not requiring a memo.
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]
        assert f"/accounts/{NOT_FOUND}" in _account_check_requests(httpserver)

    async def test_check_memo_required_with_fetch_account_error_raise(
        self, memo_server
    ):
        transaction = build_transaction(
            FETCH_ERROR, NO_MEMO_REQUIRED, NO_MEMO_REQUIRED, NO_MEMO_REQUIRED
        )
        with pytest.raises(BadRequestError) as err:
            await resolve(memo_server.submit_transaction(transaction))
        assert err.value.status == 400

    async def test_check_memo_required_with_memo_muxed_account(self, memo_server):
        transaction = build_transaction(
            MEMO_REQUIRED_A,
            MEMO_REQUIRED_B,
            MEMO_REQUIRED_C,
            MEMO_REQUIRED_D,
            memo="hello, world",
        )
        resp = await resolve(memo_server.submit_transaction(transaction))
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]

    async def test_check_memo_required_with_fee_bump_transaction(self, memo_server):
        transaction = (
            TransactionBuilder(Account(KEYPAIR.public_key, 1), v1=True)
            .append_payment_op(MEMO_REQUIRED_A, Asset.native(), "10")
            .append_path_payment_strict_send_op(
                MEMO_REQUIRED_C, Asset.native(), "10", BTC, "1", []
            )
            .append_account_merge_op(MEMO_REQUIRED_D)
            .add_text_memo("hello, world")
            .build()
        )
        transaction.sign(KEYPAIR)
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source=Keypair.from_secret(
                "SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6"
            ).public_key,
            base_fee=200,
            inner_transaction_envelope=transaction,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        )
        resp = await resolve(memo_server.submit_transaction(fee_bump_tx))
        assert resp["hash"] == SUCCESS_TRANSACTION_RESPONSE["hash"]
