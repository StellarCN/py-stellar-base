from __future__ import annotations

import os
from pathlib import Path

from .. import xdr as stellar_xdr
from ._wasm import (
    CONTRACT_ENV_META_SECTION_NAME,
    CONTRACT_META_SECTION_NAME,
    CONTRACT_SPEC_SECTION_NAME,
    iter_wasm_custom_sections,
)
from ._xdr_stream import (
    parse_sc_env_meta_entries,
    parse_sc_meta_entries,
    parse_sc_spec_entries,
)
from .contract_meta import ContractMeta
from .contract_spec import ContractSpec
from .exceptions import InvalidWasmError

__all__ = ["ContractInfo"]


class ContractInfo:
    """The :class:`ContractInfo` object, which aggregates Soroban contract
    metadata and interface information.

    ``meta``, ``spec``, and ``env_meta`` are read-only. ``env_meta`` is
    normalized to a tuple in entry order.

    :param meta: The contract metadata.
    :param spec: The contract interface specification.
    :param env_meta: The contract environment metadata entries.
    """

    __slots__ = ("_env_meta", "_meta", "_spec")

    def __init__(
        self,
        meta: ContractMeta,
        spec: ContractSpec,
        env_meta: tuple[stellar_xdr.SCEnvMetaEntry, ...] = (),
    ) -> None:
        self._meta = meta
        self._spec = spec
        self._env_meta = tuple(env_meta)

    @property
    def meta(self) -> ContractMeta:
        """Returns the contract metadata."""
        return self._meta

    @property
    def spec(self) -> ContractSpec:
        """Returns the contract interface specification."""
        return self._spec

    @property
    def env_meta(self) -> tuple[stellar_xdr.SCEnvMetaEntry, ...]:
        """Returns the contract environment metadata entries."""
        return self._env_meta

    @classmethod
    def from_wasm(cls, wasm: bytes) -> "ContractInfo":
        """Creates a :class:`ContractInfo` object from contract Wasm bytes.

        :param wasm: The contract Wasm bytes.
        :return: A :class:`ContractInfo` object.
        :raises InvalidWasmError: If the Wasm module or any introspection section cannot be decoded.
        """
        meta_entries: list[stellar_xdr.SCMetaEntry] = []
        spec_sections: list[bytes] = []
        env_meta: list[stellar_xdr.SCEnvMetaEntry] = []
        for section_name, section in iter_wasm_custom_sections(wasm):
            if section_name == CONTRACT_META_SECTION_NAME:
                meta_entries.extend(parse_sc_meta_entries(section))
            elif section_name == CONTRACT_SPEC_SECTION_NAME:
                spec_sections.append(section)
            elif section_name == CONTRACT_ENV_META_SECTION_NAME:
                env_meta.extend(parse_sc_env_meta_entries(section))

        if len(spec_sections) > 1:
            raise InvalidWasmError(
                f"Invalid Wasm module: expected at most one {CONTRACT_SPEC_SECTION_NAME!r} section."
            )
        spec_entries = parse_sc_spec_entries(spec_sections[0]) if spec_sections else ()
        return cls(
            meta=ContractMeta(tuple(meta_entries)),
            spec=ContractSpec(spec_entries),
            env_meta=tuple(env_meta),
        )

    @classmethod
    def from_wasm_file(cls, path: str | os.PathLike[str]) -> "ContractInfo":
        """Creates a :class:`ContractInfo` object from a contract Wasm file.

        :param path: The path to the contract Wasm file.
        :return: A :class:`ContractInfo` object.
        :raises InvalidWasmError: If the Wasm module or any introspection section cannot be decoded.
        """
        return cls.from_wasm(Path(path).read_bytes())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContractInfo):
            return NotImplemented
        return (
            self.meta == other.meta
            and self.spec == other.spec
            and self.env_meta == other.env_meta
        )

    def __repr__(self) -> str:
        return (
            f"<ContractInfo [meta={self.meta}, spec={self.spec}, "
            f"env_meta={self.env_meta}]>"
        )
