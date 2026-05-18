"""Inspect SEP-46/47/48 contract metadata and spec from Stellar RPC."""

from __future__ import annotations

from collections.abc import Sequence

from stellar_sdk import SorobanServer
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import (
    ContractCodeNotFoundError,
    ContractInstanceNotFoundError,
    ContractWasmRetrievalError,
    SACHasNoWasmError,
)
from stellar_sdk.sep.contract_info import ContractInfo
from stellar_sdk.sep.contract_spec import ContractSpec
from stellar_sdk.sep.exceptions import InvalidWasmError

RPC_SERVER_URL = "https://rpc.lightsail.network"
CONTRACT_ID = "CC75Z72OCE667WVPQOROIWDAGBOXFNJ4VQONQEURL74EYIDLWA4F7FEN"


def main() -> None:
    server = SorobanServer(RPC_SERVER_URL)

    # Fetch once, then parse locally. If you do not need the raw Wasm bytes,
    # ``server.get_contract_info(CONTRACT_ID)`` is the one-line equivalent.
    #
    # Other convenience methods are available too:
    # ``server.get_contract_meta(CONTRACT_ID)``
    # ``server.get_contract_spec(CONTRACT_ID)``
    wasm = server.get_contract_wasm(CONTRACT_ID)
    info = ContractInfo.from_wasm(wasm)

    print(f"RPC: {RPC_SERVER_URL}")
    print(f"Contract: {CONTRACT_ID}")
    print(f"Wasm bytes: {len(wasm):,}")
    print()

    print_meta(info)
    print()
    print_spec(info.spec)
    print()
    print_env_meta(info)


def print_meta(info: ContractInfo) -> None:
    print("SEP-46 metadata")
    print(f"  entries: {len(info.meta)}")

    try:
        items = info.meta.items()
    except InvalidWasmError as exc:
        print(f"  cannot decode metadata as UTF-8: {exc}")
        print("  raw entries:")
        for entry in info.meta:
            print(f"    {entry}")
        return

    if not items:
        print("  no metadata entries")
    for key, value in items:
        print(f"  {key}: {value}")

    supported_seps = info.meta.supported_seps()
    print()
    print("SEP-47 interface discovery")
    if supported_seps:
        print(f"  supported SEPs: {', '.join(map(str, supported_seps))}")
    else:
        print('  no "sep" metadata entries declared')


def print_spec(spec: ContractSpec) -> None:
    print("SEP-48 contract spec")
    print(f"  entries: {len(spec)}")
    print(f"  functions: {len(spec.functions)}")
    print(f"  events: {len(spec.events)}")
    print(f"  structs: {len(spec.structs)}")
    print(f"  unions: {len(spec.unions)}")
    print(f"  enums: {len(spec.enums)}")
    print(f"  error enums: {len(spec.error_enums)}")

    if spec.functions:
        print("  function signatures:")
        for function in spec.functions:
            inputs = _format_function_inputs(function.inputs)
            outputs = ", ".join(_type_name(output) for output in function.outputs)
            if outputs:
                print(f"    {_symbol(function.name)}({inputs}) -> {outputs}")
            else:
                print(f"    {_symbol(function.name)}({inputs})")

    if spec.events:
        print("  events:")
        for event in spec.events:
            params = _format_event_params(event.params)
            print(f"    {_symbol(event.name)}({params})")

    udt_names = [
        *[_text(struct.name) for struct in spec.structs],
        *[_text(union.name) for union in spec.unions],
        *[_text(enum.name) for enum in spec.enums],
        *[_text(error_enum.name) for error_enum in spec.error_enums],
    ]
    if udt_names:
        print(f"  user-defined types: {', '.join(udt_names)}")


def print_env_meta(info: ContractInfo) -> None:
    print("contractenvmetav0")
    if not info.env_meta:
        print("  no environment metadata entries")
        return
    for entry in info.env_meta:
        print(f"  {entry}")


def _format_function_inputs(
    inputs: Sequence[stellar_xdr.SCSpecFunctionInputV0],
) -> str:
    return ", ".join(
        _format_name_and_type(function_input.name, function_input.type)
        for function_input in inputs
    )


def _format_event_params(params: Sequence[stellar_xdr.SCSpecEventParamV0]) -> str:
    return ", ".join(_format_name_and_type(param.name, param.type) for param in params)


def _format_name_and_type(name: bytes, type_def: stellar_xdr.SCSpecTypeDef) -> str:
    return f"{_text(name)}: {_type_name(type_def)}"


def _type_name(type_def: stellar_xdr.SCSpecTypeDef) -> str:
    return type_def.type.name.removeprefix("SC_SPEC_TYPE_").lower()


def _symbol(symbol: stellar_xdr.SCSymbol) -> str:
    return _text(symbol.sc_symbol)


def _text(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError:
        return f"0x{value.hex()}"


if __name__ == "__main__":
    try:
        main()
    except (
        ContractCodeNotFoundError,
        ContractInstanceNotFoundError,
        ContractWasmRetrievalError,
        InvalidWasmError,
        SACHasNoWasmError,
    ) as exc:
        raise SystemExit(f"Could not inspect contract: {exc}") from exc
