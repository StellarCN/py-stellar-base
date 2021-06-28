# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from typing import List
from xdrlib import Packer, Unpacker

from .hash import Hash
from .int64 import Int64
from .ledger_header_ext import LedgerHeaderExt
from .stellar_value import StellarValue
from .uint32 import Uint32
from .uint64 import Uint64
from ..exceptions import ValueError

__all__ = ["LedgerHeader"]


class LedgerHeader:
    """
    XDR Source Code
    ----------------------------------------------------------------
    struct LedgerHeader
    {
        uint32 ledgerVersion;    // the protocol version of the ledger
        Hash previousLedgerHash; // hash of the previous ledger header
        StellarValue scpValue;   // what consensus agreed to
        Hash txSetResultHash;    // the TransactionResultSet that led to this ledger
        Hash bucketListHash;     // hash of the ledger state

        uint32 ledgerSeq; // sequence number of this ledger

        int64 totalCoins; // total number of stroops in existence.
                          // 10,000,000 stroops in 1 XLM

        int64 feePool;       // fees burned since last inflation run
        uint32 inflationSeq; // inflation sequence number

        uint64 idPool; // last used global ID, used for generating objects

        uint32 baseFee;     // base fee per operation in stroops
        uint32 baseReserve; // account base reserve in stroops

        uint32 maxTxSetSize; // maximum size a transaction set can be

        Hash skipList[4]; // hashes of ledgers in the past. allows you to jump back
                          // in time without walking the chain back ledger by ledger
                          // each slot contains the oldest ledger that is mod of
                          // either 50  5000  50000 or 500000 depending on index
                          // skipList[0] mod(50), skipList[1] mod(5000), etc

        // reserved for future use
        union switch (int v)
        {
        case 0:
            void;
        }
        ext;
    };
    ----------------------------------------------------------------
    """

    def __init__(
        self,
        ledger_version: Uint32,
        previous_ledger_hash: Hash,
        scp_value: StellarValue,
        tx_set_result_hash: Hash,
        bucket_list_hash: Hash,
        ledger_seq: Uint32,
        total_coins: Int64,
        fee_pool: Int64,
        inflation_seq: Uint32,
        id_pool: Uint64,
        base_fee: Uint32,
        base_reserve: Uint32,
        max_tx_set_size: Uint32,
        skip_list: List[Hash],
        ext: LedgerHeaderExt,
    ) -> None:
        if skip_list and len(skip_list) != 4:
            raise ValueError(
                f"The length of `skip_list` should be 4, but got {len(skip_list)}."
            )
        self.ledger_version = ledger_version
        self.previous_ledger_hash = previous_ledger_hash
        self.scp_value = scp_value
        self.tx_set_result_hash = tx_set_result_hash
        self.bucket_list_hash = bucket_list_hash
        self.ledger_seq = ledger_seq
        self.total_coins = total_coins
        self.fee_pool = fee_pool
        self.inflation_seq = inflation_seq
        self.id_pool = id_pool
        self.base_fee = base_fee
        self.base_reserve = base_reserve
        self.max_tx_set_size = max_tx_set_size
        self.skip_list = skip_list
        self.ext = ext

    def pack(self, packer: Packer) -> None:
        self.ledger_version.pack(packer)
        self.previous_ledger_hash.pack(packer)
        self.scp_value.pack(packer)
        self.tx_set_result_hash.pack(packer)
        self.bucket_list_hash.pack(packer)
        self.ledger_seq.pack(packer)
        self.total_coins.pack(packer)
        self.fee_pool.pack(packer)
        self.inflation_seq.pack(packer)
        self.id_pool.pack(packer)
        self.base_fee.pack(packer)
        self.base_reserve.pack(packer)
        self.max_tx_set_size.pack(packer)
        packer.pack_uint(4)
        for skip_list in self.skip_list:
            skip_list.pack(packer)
        self.ext.pack(packer)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "LedgerHeader":
        ledger_version = Uint32.unpack(unpacker)
        previous_ledger_hash = Hash.unpack(unpacker)
        scp_value = StellarValue.unpack(unpacker)
        tx_set_result_hash = Hash.unpack(unpacker)
        bucket_list_hash = Hash.unpack(unpacker)
        ledger_seq = Uint32.unpack(unpacker)
        total_coins = Int64.unpack(unpacker)
        fee_pool = Int64.unpack(unpacker)
        inflation_seq = Uint32.unpack(unpacker)
        id_pool = Uint64.unpack(unpacker)
        base_fee = Uint32.unpack(unpacker)
        base_reserve = Uint32.unpack(unpacker)
        max_tx_set_size = Uint32.unpack(unpacker)
        length = unpacker.unpack_uint()
        skip_list = []
        for _ in range(length):
            skip_list.append(Hash.unpack(unpacker))
        ext = LedgerHeaderExt.unpack(unpacker)
        return cls(
            ledger_version=ledger_version,
            previous_ledger_hash=previous_ledger_hash,
            scp_value=scp_value,
            tx_set_result_hash=tx_set_result_hash,
            bucket_list_hash=bucket_list_hash,
            ledger_seq=ledger_seq,
            total_coins=total_coins,
            fee_pool=fee_pool,
            inflation_seq=inflation_seq,
            id_pool=id_pool,
            base_fee=base_fee,
            base_reserve=base_reserve,
            max_tx_set_size=max_tx_set_size,
            skip_list=skip_list,
            ext=ext,
        )

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "LedgerHeader":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "LedgerHeader":
        xdr_bytes = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr_bytes)

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.ledger_version == other.ledger_version
            and self.previous_ledger_hash == other.previous_ledger_hash
            and self.scp_value == other.scp_value
            and self.tx_set_result_hash == other.tx_set_result_hash
            and self.bucket_list_hash == other.bucket_list_hash
            and self.ledger_seq == other.ledger_seq
            and self.total_coins == other.total_coins
            and self.fee_pool == other.fee_pool
            and self.inflation_seq == other.inflation_seq
            and self.id_pool == other.id_pool
            and self.base_fee == other.base_fee
            and self.base_reserve == other.base_reserve
            and self.max_tx_set_size == other.max_tx_set_size
            and self.skip_list == other.skip_list
            and self.ext == other.ext
        )

    def __str__(self):
        out = [
            f"ledger_version={self.ledger_version}",
            f"previous_ledger_hash={self.previous_ledger_hash}",
            f"scp_value={self.scp_value}",
            f"tx_set_result_hash={self.tx_set_result_hash}",
            f"bucket_list_hash={self.bucket_list_hash}",
            f"ledger_seq={self.ledger_seq}",
            f"total_coins={self.total_coins}",
            f"fee_pool={self.fee_pool}",
            f"inflation_seq={self.inflation_seq}",
            f"id_pool={self.id_pool}",
            f"base_fee={self.base_fee}",
            f"base_reserve={self.base_reserve}",
            f"max_tx_set_size={self.max_tx_set_size}",
            f"skip_list={self.skip_list}",
            f"ext={self.ext}",
        ]
        return f"<LedgerHeader {[', '.join(out)]}>"
