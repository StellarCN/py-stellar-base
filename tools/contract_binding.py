import base64
import dataclasses
from typing import List, Optional, Tuple, Union, Type
from stellar_sdk import xdr


@dataclasses.dataclass
class ContractMetaData:
    """The contract metadata parsed from the Stellar Contract WASM."""

    env_meta_bytes: Optional[bytes] = None
    env_meta: List[xdr.SCEnvMetaEntry] = dataclasses.field(default_factory=list)
    meta_bytes: Optional[bytes] = None
    meta: List[xdr.SCMetaEntry] = dataclasses.field(default_factory=list)
    spec_bytes: Optional[bytes] = None
    spec: List[xdr.SCSpecEntry] = dataclasses.field(default_factory=list)


def parse_contract_metadata(wasm: Union[bytes, str]) -> ContractMetaData:
    """Parse contract metadata from the Stellar Contract WASM.

    :param wasm: The Stellar Contract WASM as bytes or base64 encoded string.
    :return: The parsed contract metadata.
    """
    if isinstance(wasm, str):
        wasm = base64.b64decode(wasm)

    custom_sections = get_custom_sections(wasm)
    metadata = ContractMetaData()
    for name, content in custom_sections:
        if name == "contractenvmetav0":
            metadata.env_meta_bytes = content
            metadata.env_meta = parse_entries(content, xdr.SCEnvMetaEntry)
        if name == "contractspecv0":
            metadata.spec_bytes = content
            metadata.spec = parse_entries(content, xdr.SCSpecEntry)
        if name == "contractmetav0":
            metadata.meta_bytes = content
            metadata.meta = parse_entries(content, xdr.SCMetaEntry)
    return metadata


def leb128_decode(data: bytes, offset: int) -> Tuple[int, int]:
    """Decode a Little Endian Base 128 encoded integer.

    :param data: The data to decode.
    :param offset: The offset to start decoding.
    :return: The decoded integer and the number of bytes read.
    """
    result = 0
    shift = 0
    size = 0
    byte = 0x80
    while byte & 0x80:
        byte = data[offset + size]
        result |= (byte & 0x7F) << shift
        shift += 7
        size += 1
    return result, size


def get_custom_sections(wasm_data: bytes) -> List[Tuple[str, bytes]]:
    """Get the custom sections from the given WebAssembly data.

    :param wasm_data: The WebAssembly data.
    :return: The custom sections as a list of tuples containing the name and content.
    """

    assert wasm_data[:4] == b"\x00asm", "Invalid WebAssembly magic number"
    offset = 8  # Skip past the magic number and version
    custom_sections = []

    while offset < len(wasm_data):
        section_id, section_id_size = leb128_decode(wasm_data, offset)
        offset += section_id_size
        section_len, section_len_size = leb128_decode(wasm_data, offset)
        offset += section_len_size

        if section_id == 0:  # Custom Section
            name_len, size_name_size = leb128_decode(wasm_data, offset)
            offset += size_name_size
            name = wasm_data[offset: offset + name_len].decode("utf-8")
            offset += name_len
            content = wasm_data[
                      offset: offset + section_len - size_name_size - name_len
                      ]
            offset += section_len - size_name_size - name_len
            custom_sections.append((name, content))
        else:
            offset += section_len
    return custom_sections


def parse_entries(
        data: bytes, cls: Type[Union[xdr.SCEnvMetaEntry, xdr.SCMetaEntry, xdr.SCSpecEntry]]
) -> List[Union[xdr.SCEnvMetaEntry, xdr.SCMetaEntry, xdr.SCSpecEntry]]:
    """Parse a list of entries from the given data.

    :param data: The data to parse.
    :param cls: The class to use for parsing.
    :return: The parsed entries.
    """
    entries = []
    offset = 0
    while offset < len(data):
        entry = cls.from_xdr_bytes(data[offset:])
        offset += len(entry.to_xdr_bytes())
        entries.append(entry)
    return entries


def number_to_letter(num: int) -> str:
    if not 1 <= num <= 26:
        raise ValueError("Number must be between 1 and 26")
    return chr(num + 96)


def spec_type_def_to_py(td: xdr.SCSpecTypeDef):
    t = td.type
    if t in (xdr.SCSpecType.SC_SPEC_TYPE_I32, xdr.SCSpecType.SC_SPEC_TYPE_U32,
             xdr.SCSpecType.SC_SPEC_TYPE_I64, xdr.SCSpecType.SC_SPEC_TYPE_U64,
             xdr.SCSpecType.SC_SPEC_TYPE_TIMEPOINT, xdr.SCSpecType.SC_SPEC_TYPE_DURATION,
             xdr.SCSpecType.SC_SPEC_TYPE_U128, xdr.SCSpecType.SC_SPEC_TYPE_I128,
             xdr.SCSpecType.SC_SPEC_TYPE_U256, xdr.SCSpecType.SC_SPEC_TYPE_I256):
        return "int"
    if t == xdr.SCSpecType.SC_SPEC_TYPE_BOOL:
        return "bool"
    if t == xdr.SCSpecType.SC_SPEC_TYPE_VOID:
        return "None"
    if t in (xdr.SCSpecType.SC_SPEC_TYPE_BYTES, xdr.SCSpecType.SC_SPEC_TYPE_STRING):
        return "bytes"
    if t == xdr.SCSpecType.SC_SPEC_TYPE_SYMBOL:
        return "str"
    if t == xdr.SCSpecType.SC_SPEC_TYPE_ADDRESS:
        return "str"  # TODO: and Address
    # TODO: add missing types
    if t == xdr.SCSpecType.SC_SPEC_TYPE_UDT:
        return td.udt.name.decode()
    raise ValueError(f"Unsupported SCValType: {t}")


def r2p(t: xdr.SCValType) -> str:
    if t == xdr.SCValType.SCV_BOOL:
        return "bool"
    elif t == xdr.SCValType.SCV_VOID:
        return "None"
    elif t == xdr.SCValType.SCV_ERROR:
        raise ValueError("SCV_ERROR is not supported")
    elif t == xdr.SCValType.SCV_U32:
        return "int"
    elif t == xdr.SCValType.SCV_I32:
        return "int"
    elif t == xdr.SCValType.SCV_U64:
        return "int"
    elif t == xdr.SCValType.SCV_I64:
        return "int"
    elif t == xdr.SCValType.SCV_TIMEPOINT:
        return "int"
    elif t == xdr.SCValType.SCV_DURATION:
        return "int"
    elif t == xdr.SCValType.SCV_U128:
        return "int"
    elif t == xdr.SCValType.SCV_I128:
        return "int"
    elif t == xdr.SCValType.SCV_U256:
        return "int"
    elif t == xdr.SCValType.SCV_I256:
        return "int"
    elif t == xdr.SCValType.SCV_BYTES:
        return "bytes"
    elif t == xdr.SCValType.SCV_STRING:
        return "bytes"
    elif t == xdr.SCValType.SCV_SYMBOL:
        return "str"
    elif t == xdr.SCValType.SCV_VEC:
        # TODO: remove support?
        return "List"
    elif t == xdr.SCValType.SCV_MAP:
        # TODO: remove support?
        return "Dict"
    elif t == xdr.SCValType.SCV_ADDRESS:
        return "str"  # or Address
    elif t == xdr.SCValType.SCV_CONTRACT_INSTANCE:
        raise ValueError("SCV_CONTRACT_INSTANCE is not supported")
    elif t == xdr.SCValType.SCV_LEDGER_KEY_CONTRACT_INSTANCE:
        raise ValueError("SCV_LEDGER_KEY_CONTRACT_INSTANCE is not supported")
    elif t == xdr.SCValType.SCV_LEDGER_KEY_NONCE:
        raise ValueError("SCV_LEDGER_KEY_NONCE is not supported")
    else:
        raise ValueError(f"Unknown SCValType: {t}")


def render_enum(entry: xdr.SCSpecUDTEnumV0):
    print(f"class {entry.name.decode()}(IntEnum):")
    if entry.doc:
        print(f"    '''{entry.doc.decode()}'''")
    for case in entry.cases:
        print(f"    {case.name.decode()} = {case.value.uint32}")


def render_function(entry: xdr.SCSpecFunctionV0):
    pass


def render_struct(entry: xdr.SCSpecUDTStructV0):
    print(f"class {entry.name.decode()}:")
    if entry.doc:
        print(f"    '''{entry.doc.decode()}'''")
    fields = [(f.name.decode(), spec_type_def_to_py(f.type)) for f in entry.fields]
    print(f"    def __init__(self, {', '.join([f'{name}: {type}' for name, type in fields])}):")
    for name, type in fields:
        print(f"        self.{name} = {name}")


def camel_to_snake(text: str) -> str:
    result = text[0].lower()
    for char in text[1:]:
        if char.isupper():
            result += "_" + char.lower()
        else:
            result += char
    return result


def render_union(entry: xdr.SCSpecUDTUnionV0):
    print(f"class {entry.name.decode()}Kind(IntEnum):")
    case_tuples: List[xdr.SCSpecUDTUnionCaseTupleV0] = []
    for index, case in enumerate(entry.cases):
        if case.kind == xdr.SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_VOID_V0:
            print(f"    {case.void_case.name.decode()} = {index}")
        elif case.kind == xdr.SCSpecUDTUnionCaseV0Kind.SC_SPEC_UDT_UNION_CASE_TUPLE_V0:
            print(f"    {case.tuple_case.name.decode()} = {index}")
            case_tuples.append(case.tuple_case)
        else:
            raise ValueError(f"Unknown union case kind: {case.kind}")

    case_tuples_fields = []
    for case in case_tuples:
        if len(case.type) == 1:
            case_tuples_fields.append((camel_to_snake(case.name.decode()), spec_type_def_to_py(case.type[0])))
        else:
            case_tuples_fields.append((camel_to_snake(case.name.decode()),
                                       f"Tuple[{', '.join([spec_type_def_to_py(t) for t in case.type])}]"))

    print(f"class {entry.name.decode()}:")
    if entry.doc:
        print(f"    '''{entry.doc.decode()}'''")
    print(
        f"    def __init__(self, kind: {entry.name.decode()}Kind, {', '.join([f'{name}: {type}' for name, type in case_tuples_fields])}):")
    print("        self.kind = kind")
    for name, _ in case_tuples_fields:
        print(f"        self.{name} = {name}")


def render_error_enum(entry: xdr.SCSpecUDTErrorEnumV0):
    print(f"class {entry.name.decode()}(IntEnum):")
    if entry.doc:
        print(f"    '''{entry.doc.decode()}'''")
    for case in entry.cases:
        print(f"    {case.name.decode()} = {case.value.uint32}")


if __name__ == '__main__':
    wasm_file = "./test_wasms/target/wasm32-unknown-unknown/release/test_custom_types.wasm"
    with open(wasm_file, "rb") as f:
        wasm = f.read()
    metadata = parse_contract_metadata(wasm)
    specs = metadata.spec
    for spec in specs:
        # print(spec)
        if spec.kind == xdr.SCSpecEntryKind.SC_SPEC_ENTRY_FUNCTION_V0:
            render_function(spec.function_v0)
        elif spec.kind == xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_STRUCT_V0:
            render_struct(spec.udt_struct_v0)
        elif spec.kind == xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_UNION_V0:
            render_union(spec.udt_union_v0)
        elif spec.kind == xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ENUM_V0:
            render_enum(spec.udt_enum_v0)
        elif spec.kind == xdr.SCSpecEntryKind.SC_SPEC_ENTRY_UDT_ERROR_ENUM_V0:
            render_error_enum(spec.udt_error_enum_v0)
        else:
            raise ValueError(f"Unknown spec kind: {spec.kind}")
