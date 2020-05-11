# Two ledgers average time + 1 sec
DEFAULT_GET_TIMEOUT_SECONDS = 11

# https://github.com/stellar/go/blob/7c4596db1ad107f770bd6e5a694ea5129440cb1e/services/horizon/internal/txsub/system.go#L314
_HORIZON_SUBMIT_TRANSACTION_API_TIMEOUT_SECONDS = 30
# POST is only used for submitting transactions to Horizon. Therefore we take the Horizon value with some grace.
DEFAULT_POST_TIMEOUT_SECONDS = _HORIZON_SUBMIT_TRANSACTION_API_TIMEOUT_SECONDS * 1.1
