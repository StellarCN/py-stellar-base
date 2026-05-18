"""Response payloads and helpers used by tests backed by the local httpserver."""

TRANSACTION_XDR = (
    "AAAAAHI7fpgo+b7tgpiFyYWimjV7L7IOYLwmQS7k7F8SronXAAAAZAE+QT4AAAAJAAAAAQAAAA"
    "AAAAAAAAAAAF1MG8cAAAAAAAAAAQAAAAAAAAAAAAAAAOvi1O/HEn+QgZJw+EMZBtwvTVNmpgvE"
    "9p8IRfwp0GY4AAAAAAExLQAAAAAAAAAAARKuidcAAABAJVc1ASGp35hUquGNbzzSqWPoTG0zgc"
    "89zc4p+19QkgbPqsdyEfHs7+ng9VJA49YneEXRa6Fv7pfKpEigb3VTCg=="
)
TRANSACTION_HASH = "c1d2d2b16afb3313cea19f9854ffc095a18baf2d04508ef6d367a72928231084"

BAD_REQUEST = {
    "type": "https://stellar.org/horizon-errors/bad_request",
    "title": "Bad Request",
    "status": 400,
    "detail": "The request you sent was invalid in some way.",
    "extras": {
        "invalid_field": "account_id",
        "reason": "Account ID must start with `G` and contain 56 alphanum characters",
    },
}
NOT_FOUND = {
    "type": "https://stellar.org/horizon-errors/not_found",
    "title": "Resource Missing",
    "status": 404,
    "detail": (
        "The resource at the url requested was not found.  This "
        "usually occurs for one of two reasons:  The url requested is not valid, "
        "or no data in our database could be found with the parameters provided."
    ),
}


def account(account_id: str) -> dict:
    return {
        "id": account_id,
        "account_id": account_id,
        "sequence": "123456789",
        "thresholds": {
            "low_threshold": 1,
            "med_threshold": 2,
            "high_threshold": 3,
        },
    }


def ledger(base_fee: int = 100) -> dict:
    return {"_embedded": {"records": [{"base_fee_in_stroops": str(base_fee)}]}}


def submit_transaction(xdr: str = TRANSACTION_XDR) -> dict:
    return {"envelope_xdr": xdr}


def submit_transaction_async(tx_hash: str) -> dict:
    return {"tx_status": "PENDING", "hash": tx_hash}


def stream_body() -> str:
    return (
        'id: 1\ndata: "hello"\n\n'
        'id: 2\ndata: {"id": "1"}\n\n'
        'id: 3\ndata: {"id": "2"}\n\n'
    )
