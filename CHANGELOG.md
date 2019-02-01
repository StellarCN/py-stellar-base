Release History
===============

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