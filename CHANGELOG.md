Release History
===============

### Version 1.1.4
Released on May 5, 2019
  - `Horizon.order_book` supports stream.

### Version 1.1.3
Released on April 21, 2019
  - Bugfix: RecursionError during deepcopy on operations object.

### Version 1.1.2
Released on April 17, 2019
  - Upgraded some dependencies.

### Version 1.1.1
Released on April 1, 2019
  - Small bug fixes.

### Version 1.1.0
Released on February 28, 2019
  - Add include_failed parameter to `Horizon.account_operations`, `Horizon.account_transactions`, `Horizon.transactions`,
    `Horizon.transaction_operations`, `Horizon.ledger_operations`, `Horizon.ledger_transactions` 
    and `Horizon.operations` for including failed transactions in the result.
  - Add `Horizon.fee_stats` for getting useful information about fee stats in the last 5 ledgers.
  - Add `Horizon.base_fee` for fetching the current base fee, `Builder` uses it to set the default fee.

### Version 1.0.3 
Released on February 1, 2019
  - Add offset parameter to `Horizon.trade_aggregations` to reflect new changes to the endpoint in horizon-0.15.0

### Version 1.0.2 
Released on December 31, 2018
  - Breaking change: Decode memo_text into bytes internally
  - Bugfix: Raise HorizonError(status_code=http_reply_code) after multiple queries and still failing.

### Version 1.0.1 
Released on December 12, 2018
  - Remove numpy dependency for installation