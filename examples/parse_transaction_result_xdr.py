"""
This example shows how to parse XDR string into an XDR object.
But please note that if you need to parse a transaction envelope,
please refer to `parse_transaction_envelope.py`
"""

from stellar_sdk.xdr import TransactionResult, TransactionResultResult

result_xdr = "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAADAAAAAAAAAAAAAAABAAAAAD/jlpBCTX53ogvts02Ryn5GjO6gx0qW3/3ARB+gOh/nAAAAADGRC/wAAAAAAAAAAU5VQwAAAAAAR74W04RzO2ryJo94Oi0FUs0KHIVQisRnpe9FWrqvumQAAAAAAEFWjwjgcksQkG4uAAAAAAAAAAAAAAAA"
transaction_result = TransactionResult.from_xdr_base64(result_xdr)
print(transaction_result.fee_charged)
match transaction_result.result:
    case TransactionResultResult.TxSuccess(results):
        print(f"success, {len(results)} operation result(s)")
    case result:
        print(result.code.name)
