from __future__ import annotations

import pytest

from stellar_sdk.sep._xdr_stream import (
    _parse_xdr_stream,
    parse_sc_meta_entries,
    serialize_sc_env_meta_entries,
    serialize_sc_meta_entries,
)
from stellar_sdk.sep.exceptions import InvalidWasmError

from .contract_introspection_helpers import meta_entry


def test_xdr_stream_round_trip():
    entries = (meta_entry("key", "value"), meta_entry("other", "value"))
    data = serialize_sc_meta_entries(entries)

    assert parse_sc_meta_entries(data) == entries
    assert serialize_sc_env_meta_entries(()) == b""


def test_xdr_stream_rejects_non_bytes():
    with pytest.raises(TypeError, match="data must be bytes"):
        parse_sc_meta_entries("not bytes")  # type: ignore[arg-type]


def test_xdr_stream_rejects_decoders_that_make_no_progress():
    with pytest.raises(InvalidWasmError, match="made no progress"):
        _parse_xdr_stream(b"\x00", lambda unpacker: meta_entry("key", "value"), "test")


def test_xdr_stream_rejects_trailing_bytes():
    data = serialize_sc_meta_entries([meta_entry("key", "value")])

    with pytest.raises(InvalidWasmError, match="Invalid XDR stream"):
        parse_sc_meta_entries(data + b"\x00")
