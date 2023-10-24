from stellar_sdk import Keypair
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.soroban_data_builder import SorobanDataBuilder


class TestSorobanDataBuilder:
    empty_instance = stellar_xdr.SorobanTransactionData(
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

    def test_init(self):
        builder = SorobanDataBuilder()
        assert builder._data == self.empty_instance
        assert builder.build() == self.empty_instance

    def test_from_xdr_object(self):
        xdr_obj = stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                read_bytes=stellar_xdr.Uint32(2),
                write_bytes=stellar_xdr.Uint32(3),
                instructions=stellar_xdr.Uint32(4),
            ),
        )
        builder = SorobanDataBuilder.from_xdr(xdr_obj)
        assert builder._data == xdr_obj
        assert builder.build() == xdr_obj
        assert id(builder._data) != id(xdr_obj)

    def test_from_xdr_base64(self):
        xdr_obj = stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                read_bytes=stellar_xdr.Uint32(2),
                write_bytes=stellar_xdr.Uint32(3),
                instructions=stellar_xdr.Uint32(4),
            ),
        )
        builder = SorobanDataBuilder.from_xdr(xdr_obj.to_xdr())
        assert builder._data == xdr_obj
        assert builder.build() == xdr_obj
        assert id(builder._data) != id(xdr_obj)

    def test_set_resource_fee(self):
        builder = SorobanDataBuilder()
        builder.set_resource_fee(100)
        assert builder.build().resource_fee.int64 == 100

    def test_set_resources(self):
        data = SorobanDataBuilder().set_resources(1, 2, 3).build()
        assert data == stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[],
                ),
                instructions=stellar_xdr.Uint32(1),
                read_bytes=stellar_xdr.Uint32(2),
                write_bytes=stellar_xdr.Uint32(3),
            ),
        )

    def test_set_read_only(self):
        ledger_key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.ACCOUNT,
            account=stellar_xdr.LedgerKeyAccount(
                Keypair.from_public_key(
                    "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
                ).xdr_account_id()
            ),
        )
        data = SorobanDataBuilder().set_read_only([ledger_key]).build()
        assert data == stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[ledger_key],
                    read_write=[],
                ),
                read_bytes=stellar_xdr.Uint32(0),
                write_bytes=stellar_xdr.Uint32(0),
                instructions=stellar_xdr.Uint32(0),
            ),
        )

    def test_set_read_write(self):
        ledger_key = stellar_xdr.LedgerKey(
            stellar_xdr.LedgerEntryType.ACCOUNT,
            account=stellar_xdr.LedgerKeyAccount(
                Keypair.from_public_key(
                    "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
                ).xdr_account_id()
            ),
        )
        data = SorobanDataBuilder().set_read_write([ledger_key]).build()
        assert data == stellar_xdr.SorobanTransactionData(
            ext=stellar_xdr.ExtensionPoint(0),
            resource_fee=stellar_xdr.Int64(0),
            resources=stellar_xdr.SorobanResources(
                footprint=stellar_xdr.LedgerFootprint(
                    read_only=[],
                    read_write=[ledger_key],
                ),
                read_bytes=stellar_xdr.Uint32(0),
                write_bytes=stellar_xdr.Uint32(0),
                instructions=stellar_xdr.Uint32(0),
            ),
        )

    def test_copy(self):
        builder = SorobanDataBuilder()
        assert builder._data == self.empty_instance
        assert builder.build() == self.empty_instance
        assert id(builder._data) != id(builder.build())
