"""
This example shows how to parse XDR string into an XDR object.
But please note that if you need to parse a transaction envelope,
please refer to `parse_transaction_envelope.py`
"""
from stellar_sdk.xdr import TransactionResult

result_xdr = "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAADAAAAAAAAAAAAAAABAAAAAD/jlpBCTX53ogvts02Ryn5GjO6gx0qW3/3ARB+gOh/nAAAAADGRC/wAAAAAAAAAAU5VQwAAAAAAR74W04RzO2ryJo94Oi0FUs0KHIVQisRnpe9FWrqvumQAAAAAAEFWjwjgcksQkG4uAAAAAAAAAAAAAAAA"
transaction_result = TransactionResult.from_xdr(result_xdr)
print(transaction_result.fee_charged)
print(transaction_result.result.code)
