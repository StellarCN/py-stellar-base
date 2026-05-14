from __future__ import annotations

from collections.abc import Iterable

from stellar_sdk import xdr as stellar_xdr


def meta_entry(key: str, value: str) -> stellar_xdr.SCMetaEntry:
    return stellar_xdr.SCMetaEntry(
        stellar_xdr.SCMetaKind.SC_META_V0,
        v0=stellar_xdr.SCMetaV0(key.encode(), value.encode()),
    )


def wasm(*sections: bytes) -> bytes:
    return b"\x00asm\x01\x00\x00\x00" + b"".join(sections)


def custom_section(name: str, payload: bytes) -> bytes:
    encoded_name = name.encode()
    section_payload = leb_u32(len(encoded_name)) + encoded_name + payload
    return b"\x00" + leb_u32(len(section_payload)) + section_payload


def leb_u32(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def serialize_entries(entries: Iterable) -> bytes:
    data = b""
    for entry in entries:
        data += entry.to_xdr_bytes()
    return data
