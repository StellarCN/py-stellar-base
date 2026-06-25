from stellar_sdk.soroban_rpc import (
    GetSACBalanceResponse,
    LedgerEntryResult,
    SACBalanceEntry,
)


def test_from_ledger_entry_result_returns_none_for_non_contract_data():
    ledger_entry_result = LedgerEntryResult.model_validate(
        {
            "key": "AAAAAAAAAACynni6I2ACEzWuORVM1b2y0k1ZDni0W6JlC/Ad/mfCSg==",
            "xdr": "AAAAAAAAAACynni6I2ACEzWuORVM1b2y0k1ZDni0W6JlC/Ad/mfCSgAAABdIdugAAAAAnwAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAA",
            "lastModifiedLedgerSeq": 159,
            "liveUntilLedgerSeq": 288,
        }
    )

    response = GetSACBalanceResponse.from_ledger_entry_result(
        ledger_entry_result, latest_ledger=7943
    )

    assert response == GetSACBalanceResponse(
        latest_ledger=7943, balance_entry=None
    )


def test_from_ledger_entry_result_returns_balance_entry_for_contract_data():
    latest_ledger = 57387047
    last_modified_ledger = 57386587
    live_until_ledger = 57904987
    ledger_entry_result = LedgerEntryResult.model_validate(
        {
            "key": "AAAABgAAAAAAAAABJbT82FmuwvpjSEOMSJs8PBDJi20hvk/TyzDLaJU++XcAAAAQAAAAAQAAAAIAAAAPAAAAB0JhbGFuY2UAAAAAEgAAAAEltPzYWa7C+mNIQ4xImzw8EMmLbSG+T9PLMMtolT75dwAAAAEAAAARAAAAAQAAAAMAAAAPAAAABmFtb3VudAAAAAAACgAAAAAAAAAAAAAAABFKkyUAAAAPAAAACmF1dGhvcml6ZWQAAAAAAAAAAAABAAAADwAAAAhjbGF3YmFjawAAAAAAAAAA",
            "xdr": "AAAABgAAAAAAAAABJbT82FmuwvpjSEOMSJs8PBDJi20hvk/TyzDLaJU++XcAAAAQAAAAAQAAAAIAAAAPAAAAB0JhbGFuY2UAAAAAEgAAAAEltPzYWa7C+mNIQ4xImzw8EMmLbSG+T9PLMMtolT75dwAAAAEAAAARAAAAAQAAAAMAAAAPAAAABmFtb3VudAAAAAAACgAAAAAAAAAAAAAAABFKkyUAAAAPAAAACmF1dGhvcml6ZWQAAAAAAAAAAAABAAAADwAAAAhjbGF3YmFjawAAAAAAAAAA",
            "lastModifiedLedgerSeq": last_modified_ledger,
            "liveUntilLedgerSeq": live_until_ledger,
        }
    )

    response = GetSACBalanceResponse.from_ledger_entry_result(
        ledger_entry_result, latest_ledger=latest_ledger
    )

    assert response == GetSACBalanceResponse(
        latest_ledger=latest_ledger,
        balance_entry=SACBalanceEntry(
            amount=290100005,
            authorized=True,
            clawback=False,
            last_modified_ledger=last_modified_ledger,
            live_until_ledger=live_until_ledger,
        ),
    )
