import pytest

from stellar_sdk import (
    Account,
    AiohttpClient,
    Keypair,
    Network,
    Server,
    TransactionBuilder,
    Asset,
)
from stellar_sdk.exceptions import BadRequestError
from stellar_sdk.sep.exceptions import AccountRequiresMemoError


class TestAccountMemoRequirements:
    DESTINATION_ACCOUNT_MEMO_REQUIRED_A = (
        "GCMDQXJJGQE6TJ5XUHJMJUUIWECC5S6VANRAOWIQMMV4ALW43JOY2SEB"
    )
    DESTINATION_ACCOUNT_MEMO_REQUIRED_B = (
        "GDUR2DMT5AQ7DJUGBIBB45NKRNQXGRJTWTQ7DPRP37EKBELSMK57RMZK"
    )
    DESTINATION_ACCOUNT_MEMO_REQUIRED_C = (
        "GCS36NBLT6OKYN5EUQOQ7ZZIM6WXXNX5ME4JGTCG3HVZOYXRRMNUHNMM"
    )
    DESTINATION_ACCOUNT_MEMO_REQUIRED_D = (
        "GAKQNN6GNGNPLYBVEDCD5QAIEHAZVNCQET3HAUR4YWQAP5RPBLU2W7UG"
    )
    DESTINATION_ACCOUNT_NO_MEMO_REQUIRED = (
        "GDYC2D4P2SRC5DCEDDK2OUFESSPCTZYLDOEF6NYHR2T7X5GUTEABCQC2"
    )
    DESTINATION_ACCOUNT_NO_FOUND = (
        "GD2OVSQPGD5FBJPMW4YN3FGDJ7JDFKNOMJT35T4H52FLHXJK5MFSR5RA"
    )
    DESTINATION_ACCOUNT_FETCH_ERROR = (
        "GB7WNQUTDLD6YJ4MR3KQN3Y6ZIDIGTA7GRKNH47HOGMP2ETFGRSLD6OG"
    )

    def test_check_memo_required_with_memo_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .add_text_memo("hello, world")
            .build()
        )
        transaction.sign(keypair)
        server.submit_transaction(transaction)

    def test_check_memo_required_with_payment_skip_check_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        server.submit_transaction(transaction, True)

    def test_check_memo_required_with_payment_raise_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(
            AccountRequiresMemoError,
            match="Destination account requires a memo in the transaction.",
        ) as err:
            server.submit_transaction(transaction)
        assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A
        assert err.value.operation_index == 0

    def test_check_memo_required_with_path_payment_strict_receive_raise_sync(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(
            AccountRequiresMemoError,
            match="Destination account requires a memo in the transaction.",
        ) as err:
            server.submit_transaction(transaction)
        assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B
        assert err.value.operation_index == 1

    def test_check_memo_required_with_path_payment_strict_send_raise_sync(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(
            AccountRequiresMemoError,
            match="Destination account requires a memo in the transaction.",
        ) as err:
            server.submit_transaction(transaction)
        assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C
        assert err.value.operation_index == 2

    def test_check_memo_required_with_account_merge_raise_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(
            AccountRequiresMemoError,
            match="Destination account requires a memo in the transaction.",
        ) as err:
            server.submit_transaction(transaction)
        assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D
        assert err.value.operation_index == 3

    def test_check_memo_required_with_two_operation_with_same_destination_sync(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(
            AccountRequiresMemoError,
            match="Destination account requires a memo in the transaction.",
        ) as err:
            server.submit_transaction(transaction)
        assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D
        assert err.value.operation_index == 3

    def test_check_memo_required_with_no_destination_operation_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account).append_manage_data_op("Hello", "world").build()
        )
        transaction.sign(keypair)
        server.submit_transaction(transaction)

    def test_check_memo_required_with_account_not_found_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(self.DESTINATION_ACCOUNT_NO_FOUND, Asset.native(), "10")
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_NO_FOUND,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_NO_FOUND,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_NO_FOUND)
            .build()
        )
        transaction.sign(keypair)
        server.submit_transaction(transaction)

    def test_check_memo_required_with_fetch_account_error_raise_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_FETCH_ERROR, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED)
            .build()
        )
        transaction.sign(keypair)
        with pytest.raises(BadRequestError) as err:
            server.submit_transaction(transaction)
        assert err.value.status == 400

    @pytest.mark.asyncio
    async def test_check_memo_required_with_memo_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .add_text_memo("hello, world")
                .build()
            )
            transaction.sign(keypair)
            await server.submit_transaction(transaction)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_payment_skip_check_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            await server.submit_transaction(transaction, True)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_payment_raise_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(
                AccountRequiresMemoError,
                match="Destination account requires a memo in the transaction.",
            ) as err:
                await server.submit_transaction(transaction)
            assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A
            assert err.value.operation_index == 0

    @pytest.mark.asyncio
    async def test_check_memo_required_with_path_payment_strict_receive_raise_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(
                AccountRequiresMemoError,
                match="Destination account requires a memo in the transaction.",
            ) as err:
                await server.submit_transaction(transaction)
            assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B
            assert err.value.operation_index == 1

    @pytest.mark.asyncio
    async def test_check_memo_required_with_path_payment_strict_send_raise_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(
                AccountRequiresMemoError,
                match="Destination account requires a memo in the transaction.",
            ) as err:
                await server.submit_transaction(transaction)
            assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C
            assert err.value.operation_index == 2

    @pytest.mark.asyncio
    async def test_check_memo_required_with_account_merge_raise_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(
                AccountRequiresMemoError,
                match="Destination account requires a memo in the transaction.",
            ) as err:
                await server.submit_transaction(transaction)
            assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D
            assert err.value.operation_index == 3

    @pytest.mark.asyncio
    async def test_check_memo_required_with_two_operation_with_same_destination_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(
                AccountRequiresMemoError,
                match="Destination account requires a memo in the transaction.",
            ) as err:
                await server.submit_transaction(transaction)
            assert err.value.account_id == self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D
            assert err.value.operation_index == 3

    @pytest.mark.asyncio
    async def test_check_memo_required_with_no_destination_operation_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_manage_data_op("Hello", "world")
                .build()
            )
            transaction.sign(keypair)
            await server.submit_transaction(transaction)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_account_not_found_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_NO_FOUND, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_NO_FOUND,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_NO_FOUND,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_NO_FOUND)
                .build()
            )
            transaction.sign(keypair)
            await server.submit_transaction(transaction)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_fetch_account_error_raise_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_FETCH_ERROR, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED)
                .build()
            )
            transaction.sign(keypair)
            with pytest.raises(BadRequestError) as err:
                await server.submit_transaction(transaction)
            assert err.value.status == 400

    def test_check_memo_required_with_memo_muxed_account_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
            )
            .append_path_payment_strict_receive_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .add_text_memo("hello, world")
            .build()
        )
        transaction.sign(keypair)
        server.submit_transaction(transaction)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_memo_muxed_account_async(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
                )
                .append_path_payment_strict_receive_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .add_text_memo("hello, world")
                .build()
            )
            transaction.sign(keypair)
            await server.submit_transaction(transaction)

    def test_check_memo_required_with_fee_bump_transaction_sync(self, httpserver):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        server = Server(horizon_url)
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        transaction = (
            TransactionBuilder(account, v1=True)
            .append_payment_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
            )
            .append_path_payment_strict_send_op(
                self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                Asset.native(),
                "10",
                Asset(
                    "BTC", "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2"
                ),
                "1",
                [],
            )
            .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
            .add_text_memo("hello, world")
            .build()
        )
        transaction.sign(keypair)
        fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
            fee_source=Keypair.random().public_key,
            base_fee=200,
            inner_transaction_envelope=transaction,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        )
        server.submit_transaction(fee_bump_tx)

    @pytest.mark.asyncio
    async def test_check_memo_required_with_fee_bump_transaction_async(
        self, httpserver
    ):
        self.__inject_mock_server(httpserver)
        horizon_url = httpserver.url_for("/")
        keypair = Keypair.from_secret(
            "SDQXFKA32UVQHUTLYJ42N56ZUEM5PNVVI4XE7EA5QFMLA2DHDCQX3GPY"
        )
        account = Account(keypair.public_key, 1)
        async with Server(horizon_url, AiohttpClient()) as server:
            transaction = (
                TransactionBuilder(account, v1=True)
                .append_payment_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A, Asset.native(), "10"
                )
                .append_path_payment_strict_send_op(
                    self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C,
                    Asset.native(),
                    "10",
                    Asset(
                        "BTC",
                        "GA7GYB3QGLTZNHNGXN3BMANS6TC7KJT3TCGTR763J4JOU4QHKL37RVV2",
                    ),
                    "1",
                    [],
                )
                .append_account_merge_op(self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D)
                .add_text_memo("hello, world")
                .build()
            )
            transaction.sign(keypair)
            fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
                fee_source=Keypair.random().public_key,
                base_fee=200,
                inner_transaction_envelope=transaction,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            )
            await server.submit_transaction(fee_bump_tx)

    def __inject_mock_server(self, httpserver):
        memo_required_response = {"data": {"config.memo_required": "MQ=="}}
        no_memo_required_response = {"data": {}}
        success_transaction_response = {
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
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_MEMO_REQUIRED_A
        ).respond_with_json(memo_required_response)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_MEMO_REQUIRED_B
        ).respond_with_json(memo_required_response)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_MEMO_REQUIRED_C
        ).respond_with_json(memo_required_response)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_MEMO_REQUIRED_D
        ).respond_with_json(memo_required_response)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_NO_MEMO_REQUIRED
        ).respond_with_json(no_memo_required_response)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_NO_FOUND
        ).respond_with_data({}, 404)
        httpserver.expect_request(
            "/accounts/%s" % self.DESTINATION_ACCOUNT_FETCH_ERROR
        ).respond_with_data({}, 400)
        httpserver.expect_request("/transactions").respond_with_json(
            success_transaction_response
        )
