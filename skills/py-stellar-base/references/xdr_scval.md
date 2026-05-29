# XDR, SCVal & TxRep

## SCVal conversion (`stellar_sdk.scval`)

Soroban contract arguments and return values are `SCVal` XDR objects. Build them with
`scval.to_*` and read them with `scval.from_*` (or `scval.to_native` for a best-effort
Python value).

```python
from stellar_sdk import scval

# To SCVal (for contract arguments)
scval.to_bool(True)
scval.to_void()
scval.to_uint32(7); scval.to_int32(-7)
scval.to_uint64(7); scval.to_int64(-7)
scval.to_uint128(7); scval.to_int128(-7)
scval.to_uint256(7); scval.to_int256(-7)
scval.to_timepoint(1700000000); scval.to_duration(3600)
scval.to_bytes(b"\x01\x02")
scval.to_string("hello"); scval.to_symbol("increment")
scval.to_address("G...")          # account or contract address
scval.to_vec([scval.to_uint32(1), scval.to_uint32(2)])
scval.to_map({scval.to_symbol("k"): scval.to_uint32(1)})
scval.to_struct({"field": scval.to_uint32(1)})
scval.to_enum("Variant", scval.to_uint32(1))
scval.to_tuple_struct([scval.to_uint32(1), scval.to_symbol("x")])
```

```python
# From SCVal (parsing results)
scval.from_uint32(v); scval.from_int128(v)
scval.from_string(v)   # -> bytes; .decode() for str
scval.from_symbol(v); scval.from_address(v)
scval.from_vec(v); scval.from_map(v); scval.from_struct(v)
scval.to_native(v)     # recursive best-effort conversion to Python types
```

## Addresses

```python
from stellar_sdk import Address

addr = Address("G...")           # account or "C..." contract
sc_val = addr.to_xdr_sc_val()    # SCVal for contract args
back = Address.from_xdr_sc_val(sc_val)
```

## Transaction XDR

```python
from stellar_sdk import TransactionEnvelope, Network

xdr = tx.to_xdr()
te = TransactionEnvelope.from_xdr(xdr, Network.PUBLIC_NETWORK_PASSPHRASE)
```

Lower-level XDR types live in `stellar_sdk.xdr` (e.g. `stellar_sdk.xdr.TransactionMeta`,
`stellar_sdk.xdr.SCVal`). Most carry `.from_xdr(...)` / `.to_xdr()` for base64, and
`.from_xdr_bytes(...)` / `.to_xdr_bytes()` for raw bytes. Use these to debug result/meta
XDR, e.g. decoding a `result_meta_xdr` returned by Soroban RPC.

## TxRep (SEP-11, human-readable transactions)

```python
from stellar_sdk.sep.txrep import to_txrep, from_txrep
from stellar_sdk import Network

text = to_txrep(transaction_envelope)
envelope = from_txrep(text, Network.TESTNET_NETWORK_PASSPHRASE)
```

## SEP-51 JSON

XDR base classes support JSON encoding/decoding (SEP-51) in addition to base64/bytes,
useful for inspecting structures in a readable form.
