.. _xdr:

***
XDR
***

XDR, also known as External Data Representation, is used throughout the
Stellar network and protocol. The ledger, transactions, results, history, and
even the messages passed between computers running stellar-core are encoded
using XDR.

:ref:`stellar_sdk_xdr` module provides a complete ability to build and parse XDR.

This example shows how to parse XDR string into an XDR object.

.. literalinclude:: ../../examples/parse_transaction_result_xdr.py
   :language: python
   :linenos:
