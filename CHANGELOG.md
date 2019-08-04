Release History
===============

### Version 1.3.1
Released on August 4, 2019
* Add `Builder.challenge_tx` method for building [SEP-10](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md) challenge transaction.

### Version 1.3.0
Released on July 24, 2019
  - Breaking change: fetching data through SSE returns **dict** instead of a **str**.

### Version 1.2.2
Released on June 20, 2019
  - fix(Operation.AllowTrust): AllowTrust.from_xdr_object may generate incorrect asset code.

### Version 1.2.1
Released on June 9, 2019
  - fix(Operation.ChangeTrust): An exception should be thrown when the limit is set to 0(int). ([#206](https://github.com/StellarCN/py-stellar-base/pull/206))

### Version 1.2.0
Released on May 6, 2019
  - Adapt to Protocol v11. [ManageBuyOffer](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/operation.py#L741), 
  [ManageSellOffer](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/operation.py#L830) 
  and [CreatePassiveSellOffer](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/operation.py#L921) are supported.
  - Breaking change: [ManageOffer](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/operation.py#L1236) 
  and [CreatePassiveOffer](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/operation.py#L1244) are marked as deprecated, although you can still use them now, please update your code immediately.
  - The [Builder](https://github.com/StellarCN/py-stellar-base/blob/279aec10663a32662f8fe48c5d20a752f13f5946/stellar_base/builder.py) was also affected by the above changes, added `append_manage_buy_offer_op`, `append_manage_sell_offer_op` and `append_create_passive_sell_offer_op`. `append_manage_offer_op` and `append_create_passive_offer_op` are deprecated.

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
