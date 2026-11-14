from __future__ import annotations

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
            ext=stellar_xdr.SorobanTransactionDataExt.V0(),
            resource_fee=0,
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                disk_read_bytes=0,
                write_bytes=0,
                instructions=0,
            ),
        )

    @classmethod
    def from_xdr(
        cls, soroban_data: str | stellar_xdr.SorobanTransactionData
    ) -> SorobanDataBuilder:
        """Create a new :class:`SorobanDataBuilder` object from an XDR object.

        :param soroban_data: The XDR object that represents a SorobanTransactionData.
        :return: This builder.
        """
        data = cls()
        if isinstance(soroban_data, str):
            data._data = stellar_xdr.SorobanTransactionData.from_xdr_base64(
                soroban_data
            )
        else:
            data._data = soroban_data
        return data

    def set_resource_fee(self, fee: int) -> SorobanDataBuilder:
        """Sets the "resource" fee portion of the Soroban data.

        :param fee: The resource fee to set (int64)
        :return: This builder.
        """
        self._data = stellar_xdr.replace(self._data, resource_fee=fee)
        return self

    def set_read_only(
        self, read_only: list[stellar_xdr.LedgerKey.Any]
    ) -> SorobanDataBuilder:
        """Sets the read-only portion of the storage access footprint to be a certain set of ledger keys.

        :param read_only: The read-only ledger keys to set.
        :return: This builder.
        """
        self._set_footprint(read_only=read_only or [])
        return self

    def set_read_write(
        self, read_write: list[stellar_xdr.LedgerKey.Any]
    ) -> SorobanDataBuilder:
        """Sets the read-write portion of the storage access footprint to be a certain set of ledger keys.

        :param read_write: The read-write ledger keys to set.
        :return: This builder.
        """
        self._set_footprint(read_write=read_write or [])
        return self

    def set_resources(
        self, instructions: int, disk_read_bytes: int, write_bytes: int
    ) -> SorobanDataBuilder:
        """Sets up the resource metrics.

        You should almost NEVER need this, as its often generated / provided to you
        by transaction simulation/preflight from a Soroban RPC server.

        :param instructions: Number of CPU instructions (uint32)
        :param disk_read_bytes: Number of bytes being read from disk (uint32)
        :param write_bytes: Number of bytes being written to disk and memory (uint32)
        :return: This builder.
        """
        resources = stellar_xdr.replace(
            self._data.resources,
            instructions=instructions,
            disk_read_bytes=disk_read_bytes,
            write_bytes=write_bytes,
        )
        self._data = stellar_xdr.replace(self._data, resources=resources)
        return self

    def build(self) -> stellar_xdr.SorobanTransactionData:
        """:return: the final data structure."""
        return self._data

    def _set_footprint(self, **changes: list[stellar_xdr.LedgerKey.Any]) -> None:
        resources = self._data.resources
        footprint = stellar_xdr.replace(resources.footprint, **changes)
        resources = stellar_xdr.replace(resources, footprint=footprint)
        self._data = stellar_xdr.replace(self._data, resources=resources)
