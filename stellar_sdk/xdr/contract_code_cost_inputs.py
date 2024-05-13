# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
from __future__ import annotations

import base64

from xdrlib3 import Packer, Unpacker

from .extension_point import ExtensionPoint
from .uint32 import Uint32

__all__ = ["ContractCodeCostInputs"]


class ContractCodeCostInputs:
    """
    XDR Source Code::

        struct ContractCodeCostInputs {
            ExtensionPoint ext;
            uint32 nInstructions;
            uint32 nFunctions;
            uint32 nGlobals;
            uint32 nTableEntries;
            uint32 nTypes;
            uint32 nDataSegments;
            uint32 nElemSegments;
            uint32 nImports;
            uint32 nExports;
            uint32 nDataSegmentBytes;
        };
    """

    def __init__(
        self,
        ext: ExtensionPoint,
        n_instructions: Uint32,
        n_functions: Uint32,
        n_globals: Uint32,
        n_table_entries: Uint32,
        n_types: Uint32,
        n_data_segments: Uint32,
        n_elem_segments: Uint32,
        n_imports: Uint32,
        n_exports: Uint32,
        n_data_segment_bytes: Uint32,
    ) -> None:
        self.ext = ext
        self.n_instructions = n_instructions
        self.n_functions = n_functions
        self.n_globals = n_globals
        self.n_table_entries = n_table_entries
        self.n_types = n_types
        self.n_data_segments = n_data_segments
        self.n_elem_segments = n_elem_segments
        self.n_imports = n_imports
        self.n_exports = n_exports
        self.n_data_segment_bytes = n_data_segment_bytes

    def pack(self, packer: Packer) -> None:
        self.ext.pack(packer)
        self.n_instructions.pack(packer)
        self.n_functions.pack(packer)
        self.n_globals.pack(packer)
        self.n_table_entries.pack(packer)
        self.n_types.pack(packer)
        self.n_data_segments.pack(packer)
        self.n_elem_segments.pack(packer)
        self.n_imports.pack(packer)
        self.n_exports.pack(packer)
        self.n_data_segment_bytes.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> ContractCodeCostInputs:
        ext = ExtensionPoint.unpack(unpacker)
        n_instructions = Uint32.unpack(unpacker)
        n_functions = Uint32.unpack(unpacker)
        n_globals = Uint32.unpack(unpacker)
        n_table_entries = Uint32.unpack(unpacker)
        n_types = Uint32.unpack(unpacker)
        n_data_segments = Uint32.unpack(unpacker)
        n_elem_segments = Uint32.unpack(unpacker)
        n_imports = Uint32.unpack(unpacker)
        n_exports = Uint32.unpack(unpacker)
        n_data_segment_bytes = Uint32.unpack(unpacker)
        return cls(
            ext=ext,
            n_instructions=n_instructions,
            n_functions=n_functions,
            n_globals=n_globals,
            n_table_entries=n_table_entries,
            n_types=n_types,
            n_data_segments=n_data_segments,
            n_elem_segments=n_elem_segments,
            n_imports=n_imports,
            n_exports=n_exports,
            n_data_segment_bytes=n_data_segment_bytes,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> ContractCodeCostInputs:
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> ContractCodeCostInputs:
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __hash__(self):
        return hash(
            (
                self.ext,
                self.n_instructions,
                self.n_functions,
                self.n_globals,
                self.n_table_entries,
                self.n_types,
                self.n_data_segments,
                self.n_elem_segments,
                self.n_imports,
                self.n_exports,
                self.n_data_segment_bytes,
            )
        )

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ext == other.ext
            and self.n_instructions == other.n_instructions
            and self.n_functions == other.n_functions
            and self.n_globals == other.n_globals
            and self.n_table_entries == other.n_table_entries
            and self.n_types == other.n_types
            and self.n_data_segments == other.n_data_segments
            and self.n_elem_segments == other.n_elem_segments
            and self.n_imports == other.n_imports
            and self.n_exports == other.n_exports
            and self.n_data_segment_bytes == other.n_data_segment_bytes
        )

    def __repr__(self):
        out = [
            f"ext={self.ext}",
            f"n_instructions={self.n_instructions}",
            f"n_functions={self.n_functions}",
            f"n_globals={self.n_globals}",
            f"n_table_entries={self.n_table_entries}",
            f"n_types={self.n_types}",
            f"n_data_segments={self.n_data_segments}",
            f"n_elem_segments={self.n_elem_segments}",
            f"n_imports={self.n_imports}",
            f"n_exports={self.n_exports}",
            f"n_data_segment_bytes={self.n_data_segment_bytes}",
        ]
        return f"<ContractCodeCostInputs [{', '.join(out)}]>"
