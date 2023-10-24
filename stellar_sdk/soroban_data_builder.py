from __future__ import annotations

from typing import List, Union

from . import xdr as stellar_xdr

__all__ = ["SorobanDataBuilder"]


class SorobanDataBuilder:
    """Supports building :class:`Memo <stellar_sdk.xdr.SorobanTransactionData>` structures
    with various items set to specific values.

    This is recommended for when you are building :class:`RestoreFootprint <stellar_sdk.operation.RestoreFootprint>`,
    :class:`ExtendFootprintTTL <stellar_sdk.operation.ExtendFootprintTTL>` operations to avoid (re)building
    the entire data structure from scratch.

    By default, an empty instance will be created.
    """

    def __init__(self):
        self._data = stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                read_bytes=stellar_xdr.Uint32(0),
                write_bytes=stellar_xdr.Uint32(0),
                instructions=stellar_xdr.Uint32(0),
            ),
        )

    @classmethod
    def from_xdr(
        cls, soroban_data: Union[str, stellar_xdr.SorobanTransactionData]
    ) -> SorobanDataBuilder:
        """Create a new :class:`SorobanDataBuilder` object from an XDR object.

        :param soroban_data: The XDR object that represents a SorobanTransactionData.
        :return: This builder.
        """
        data = cls()
        if isinstance(soroban_data, str):
            data._data = stellar_xdr.SorobanTransactionData.from_xdr(soroban_data)
        else:
            data._data = stellar_xdr.SorobanTransactionData.from_xdr_bytes(
                soroban_data.to_xdr_bytes()
            )
        return data

    def set_resource_fee(self, fee: int) -> SorobanDataBuilder:
        """Sets the "resource" fee portion of the Soroban data.

        :param fee: The resource fee to set (int64)
        :return: This builder.
        """
        self._data.resource_fee = stellar_xdr.Int64(fee)
        return self

    def set_read_only(
        self, read_only: List[stellar_xdr.LedgerKey]
    ) -> SorobanDataBuilder:
        """Sets the read-only portion of the storage access footprint to be a certain set of ledger keys.

        :param read_only: The read-only ledger keys to set.
        :return: This builder.
        """
        self._data.resources.footprint.read_only = read_only or []
        return self

    def set_read_write(
        self, read_write: List[stellar_xdr.LedgerKey]
    ) -> SorobanDataBuilder:
        """Sets the read-write portion of the storage access footprint to be a certain set of ledger keys.

        :param read_write: The read-write ledger keys to set.
        :return: This builder.
        """
        self._data.resources.footprint.read_write = read_write or []
        return self

    def set_resources(
        self, instructions: int, read_bytes: int, write_bytes: int
    ) -> SorobanDataBuilder:
        """Sets up the resource metrics.

        You should almost NEVER need this, as its often generated / provided to you
        by transaction simulation/preflight from a Soroban RPC server.

        :param instructions: Number of CPU instructions (uint32)
        :param read_bytes: Number of bytes being read (uint32)
        :param write_bytes: Number of bytes being written (uint32)
        :return: This builder.
        """
        self._data.resources.instructions = stellar_xdr.Uint32(instructions)
        self._data.resources.read_bytes = stellar_xdr.Uint32(read_bytes)
        self._data.resources.write_bytes = stellar_xdr.Uint32(write_bytes)
        return self

    def build(self):
        """:return: a copy of the final data structure."""
        return stellar_xdr.SorobanTransactionData.from_xdr_bytes(
            self._data.to_xdr_bytes()
        )
