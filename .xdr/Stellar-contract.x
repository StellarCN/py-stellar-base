// Copyright 2022 Stellar Development Foundation and contributors. Licensed
// under the Apache License, Version 2.0. See the COPYING file at the root
// of this distribution or at http://www.apache.org/licenses/LICENSE-2.0

% #include "xdr/Stellar-types.h"
namespace stellar
{

// We fix a maximum of 128 value types in the system for two reasons: we want to
// keep the codes relatively small (<= 8 bits) when bit-packing values into a
// u64 at the environment interface level, so that we keep many bits for
// payloads (small strings, small numeric values, object handles); and then we
// actually want to go one step further and ensure (for code-size) that our
// codes fit in a single ULEB128-code byte, which means we can only use 7 bits.
//
// We also reserve several type codes from this space because we want to _reuse_
// the SCValType codes at the environment interface level (or at least not
// exceed its number-space) but there are more types at that level, assigned to
// optimizations/special case representations of values abstract at this level.

enum SCValType
{
    SCV_BOOL = 0,
    SCV_VOID = 1,
    SCV_STATUS = 2,

    // 32 bits is the smallest type in WASM or XDR; no need for u8/u16.
    SCV_U32 = 3,
    SCV_I32 = 4,

    // 64 bits is naturally supported by both WASM and XDR also.
    SCV_U64 = 5,
    SCV_I64 = 6,

    // Time-related u64 subtypes with their own functions and formatting.
    SCV_TIMEPOINT = 7,
    SCV_DURATION = 8,

    // 128 bits is naturally supported by Rust and we use it for Soroban
    // fixed-point arithmetic prices / balances / similar "quantities". These
    // are represented in XDR as a pair of 2 u64s, unlike {u,i}256 which is
    // represented as an array of 32 bytes.
    SCV_U128 = 9,
    SCV_I128 = 10,

    // 256 bits is the size of sha256 output, ed25519 keys, and the EVM machine
    // word, so for interop use we include this even though it requires a small
    // amount of Rust guest and/or host library code.
    SCV_U256 = 11,
    SCV_I256 = 12,

    // TODO: possibly allocate subtypes of i64, i128 and/or u256 for
    // fixed-precision with a specific number of decimals.

    // Bytes come in 3 flavors, 2 of which have meaningfully different
    // formatting and validity-checking / domain-restriction.
    SCV_BYTES = 13,
    SCV_STRING = 14,
    SCV_SYMBOL = 15,

    // Vecs and maps are just polymorphic containers of other ScVals.
    SCV_VEC = 16,
    SCV_MAP = 17,

    // SCContractExecutable and SCAddressType are types that gets used separately from
    // SCVal so we do not flatten their structures into separate SCVal cases.
    SCV_CONTRACT_EXECUTABLE = 18,
    SCV_ADDRESS = 19,

    // SCV_LEDGER_KEY_CONTRACT_EXECUTABLE and SCV_LEDGER_KEY_NONCE are unique
    // symbolic SCVals used as the key for ledger entries for a contract's code
    // and an address' nonce, respectively.
    SCV_LEDGER_KEY_CONTRACT_EXECUTABLE = 20,
    SCV_LEDGER_KEY_NONCE = 21
};

enum SCStatusType
{
    SST_OK = 0,
    SST_UNKNOWN_ERROR = 1,
    SST_HOST_VALUE_ERROR = 2,
    SST_HOST_OBJECT_ERROR = 3,
    SST_HOST_FUNCTION_ERROR = 4,
    SST_HOST_STORAGE_ERROR = 5,
    SST_HOST_CONTEXT_ERROR = 6,
    SST_VM_ERROR = 7,
    SST_CONTRACT_ERROR = 8,
    SST_HOST_AUTH_ERROR = 9
    // TODO: add more
};

enum SCHostValErrorCode
{
    HOST_VALUE_UNKNOWN_ERROR = 0,
    HOST_VALUE_RESERVED_TAG_VALUE = 1,
    HOST_VALUE_UNEXPECTED_VAL_TYPE = 2,
    HOST_VALUE_U63_OUT_OF_RANGE = 3,
    HOST_VALUE_U32_OUT_OF_RANGE = 4,
    HOST_VALUE_STATIC_UNKNOWN = 5,
    HOST_VALUE_MISSING_OBJECT = 6,
    HOST_VALUE_SYMBOL_TOO_LONG = 7,
    HOST_VALUE_SYMBOL_BAD_CHAR = 8,
    HOST_VALUE_SYMBOL_CONTAINS_NON_UTF8 = 9,
    HOST_VALUE_BITSET_TOO_MANY_BITS = 10,
    HOST_VALUE_STATUS_UNKNOWN = 11
};

enum SCHostObjErrorCode
{
    HOST_OBJECT_UNKNOWN_ERROR = 0,
    HOST_OBJECT_UNKNOWN_REFERENCE = 1,
    HOST_OBJECT_UNEXPECTED_TYPE = 2,
    HOST_OBJECT_OBJECT_COUNT_EXCEEDS_U32_MAX = 3,
    HOST_OBJECT_OBJECT_NOT_EXIST = 4,
    HOST_OBJECT_VEC_INDEX_OUT_OF_BOUND = 5,
    HOST_OBJECT_CONTRACT_HASH_WRONG_LENGTH = 6
};

enum SCHostFnErrorCode
{
    HOST_FN_UNKNOWN_ERROR = 0,
    HOST_FN_UNEXPECTED_HOST_FUNCTION_ACTION = 1,
    HOST_FN_INPUT_ARGS_WRONG_LENGTH = 2,
    HOST_FN_INPUT_ARGS_WRONG_TYPE = 3,
    HOST_FN_INPUT_ARGS_INVALID = 4
};

enum SCHostStorageErrorCode
{
    HOST_STORAGE_UNKNOWN_ERROR = 0,
    HOST_STORAGE_EXPECT_CONTRACT_DATA = 1,
    HOST_STORAGE_READWRITE_ACCESS_TO_READONLY_ENTRY = 2,
    HOST_STORAGE_ACCESS_TO_UNKNOWN_ENTRY = 3,
    HOST_STORAGE_MISSING_KEY_IN_GET = 4,
    HOST_STORAGE_GET_ON_DELETED_KEY = 5
};

enum SCHostAuthErrorCode
{
    HOST_AUTH_UNKNOWN_ERROR = 0,
    HOST_AUTH_NONCE_ERROR = 1,
    HOST_AUTH_DUPLICATE_AUTHORIZATION = 2,
    HOST_AUTH_NOT_AUTHORIZED = 3
};

enum SCHostContextErrorCode
{
    HOST_CONTEXT_UNKNOWN_ERROR = 0,
    HOST_CONTEXT_NO_CONTRACT_RUNNING = 1
};

enum SCVmErrorCode {
    VM_UNKNOWN = 0,
    VM_VALIDATION = 1,
    VM_INSTANTIATION = 2,
    VM_FUNCTION = 3,
    VM_TABLE = 4,
    VM_MEMORY = 5,
    VM_GLOBAL = 6,
    VM_VALUE = 7,
    VM_TRAP_UNREACHABLE = 8,
    VM_TRAP_MEMORY_ACCESS_OUT_OF_BOUNDS = 9,
    VM_TRAP_TABLE_ACCESS_OUT_OF_BOUNDS = 10,
    VM_TRAP_ELEM_UNINITIALIZED = 11,
    VM_TRAP_DIVISION_BY_ZERO = 12,
    VM_TRAP_INTEGER_OVERFLOW = 13,
    VM_TRAP_INVALID_CONVERSION_TO_INT = 14,
    VM_TRAP_STACK_OVERFLOW = 15,
    VM_TRAP_UNEXPECTED_SIGNATURE = 16,
    VM_TRAP_MEM_LIMIT_EXCEEDED = 17,
    VM_TRAP_CPU_LIMIT_EXCEEDED = 18
};

enum SCUnknownErrorCode
{
    UNKNOWN_ERROR_GENERAL = 0,
    UNKNOWN_ERROR_XDR = 1
};

union SCStatus switch (SCStatusType type)
{
case SST_OK:
    void;
case SST_UNKNOWN_ERROR:
    SCUnknownErrorCode unknownCode;
case SST_HOST_VALUE_ERROR:
    SCHostValErrorCode valCode;
case SST_HOST_OBJECT_ERROR:
    SCHostObjErrorCode objCode;
case SST_HOST_FUNCTION_ERROR:
    SCHostFnErrorCode fnCode;
case SST_HOST_STORAGE_ERROR:
    SCHostStorageErrorCode storageCode;
case SST_HOST_CONTEXT_ERROR:
    SCHostContextErrorCode contextCode;
case SST_VM_ERROR:
    SCVmErrorCode vmCode;
case SST_CONTRACT_ERROR:
    uint32 contractCode;
case SST_HOST_AUTH_ERROR:
    SCHostAuthErrorCode authCode;
};

struct UInt128Parts {
    uint64 hi;
    uint64 lo;
};

// A signed int128 has a high sign bit and 127 value bits. We break it into a
// signed high int64 (that carries the sign bit and the high 63 value bits) and
// a low unsigned uint64 that carries the low 64 bits. This will sort in
// generated code in the same order the underlying int128 sorts.
struct Int128Parts {
    int64 hi;
    uint64 lo;
};

struct UInt256Parts {
    uint64 hi_hi;
    uint64 hi_lo;
    uint64 lo_hi;
    uint64 lo_lo;
};

// A signed int256 has a high sign bit and 255 value bits. We break it into a
// signed high int64 (that carries the sign bit and the high 63 value bits) and
// three low unsigned `uint64`s that carry the lower bits. This will sort in
// generated code in the same order the underlying int256 sorts.
struct Int256Parts {
    int64 hi_hi;
    uint64 hi_lo;
    uint64 lo_hi;
    uint64 lo_lo;
};

enum SCContractExecutableType
{
    SCCONTRACT_EXECUTABLE_WASM_REF = 0,
    SCCONTRACT_EXECUTABLE_TOKEN = 1
};

union SCContractExecutable switch (SCContractExecutableType type)
{
case SCCONTRACT_EXECUTABLE_WASM_REF:
    Hash wasm_id;
case SCCONTRACT_EXECUTABLE_TOKEN:
    void;
};

enum SCAddressType
{
    SC_ADDRESS_TYPE_ACCOUNT = 0,
    SC_ADDRESS_TYPE_CONTRACT = 1
};

union SCAddress switch (SCAddressType type)
{
case SC_ADDRESS_TYPE_ACCOUNT:
    AccountID accountId;
case SC_ADDRESS_TYPE_CONTRACT:
    Hash contractId;
};

%struct SCVal;
%struct SCMapEntry;

const SCVAL_LIMIT = 256000;
const SCSYMBOL_LIMIT = 32;

typedef SCVal SCVec<SCVAL_LIMIT>;
typedef SCMapEntry SCMap<SCVAL_LIMIT>;

typedef opaque SCBytes<SCVAL_LIMIT>;
typedef string SCString<SCVAL_LIMIT>;
typedef string SCSymbol<SCSYMBOL_LIMIT>;

struct SCNonceKey {
    SCAddress nonce_address;
};

union SCVal switch (SCValType type)
{

case SCV_BOOL:
    bool b;
case SCV_VOID:
    void;
case SCV_STATUS:
    SCStatus error;

case SCV_U32:
    uint32 u32;
case SCV_I32:
    int32 i32;

case SCV_U64:
    uint64 u64;
case SCV_I64:
    int64 i64;
case SCV_TIMEPOINT:
    TimePoint timepoint;
case SCV_DURATION:
    Duration duration;

case SCV_U128:
    UInt128Parts u128;
case SCV_I128:
    Int128Parts i128;

case SCV_U256:
    UInt256Parts u256;
case SCV_I256:
    Int256Parts i256;

case SCV_BYTES:
    SCBytes bytes;
case SCV_STRING:
    SCString str;
case SCV_SYMBOL:
    SCSymbol sym;

// Vec and Map are recursive so need to live
// behind an option, due to xdrpp limitations.
case SCV_VEC:
    SCVec *vec;
case SCV_MAP:
    SCMap *map;

case SCV_CONTRACT_EXECUTABLE:
    SCContractExecutable exec;
case SCV_ADDRESS:
    SCAddress address;

// Special SCVals reserved for system-constructed contract-data
// ledger keys, not generally usable elsewhere.
case SCV_LEDGER_KEY_CONTRACT_EXECUTABLE:
    void;
case SCV_LEDGER_KEY_NONCE:
    SCNonceKey nonce_key;
};

struct SCMapEntry
{
    SCVal key;
    SCVal val;
};

}
