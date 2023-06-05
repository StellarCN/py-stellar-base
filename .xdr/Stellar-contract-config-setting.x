%#include "xdr/Stellar-types.h"

namespace stellar {
// "Compute" settings for contracts (instructions and memory).
struct ConfigSettingContractComputeV0
{
    // Maximum instructions per ledger
    int64 ledgerMaxInstructions;
    // Maximum instructions per transaction
    int64 txMaxInstructions;
    // Cost of 10000 instructions
    int64 feeRatePerInstructionsIncrement;

    // Memory limit per transaction. Unlike instructions, there is no fee
    // for memory, just the limit.
    uint32 txMemoryLimit;
};

// Ledger access settings for contracts.
struct ConfigSettingContractLedgerCostV0
{
    // Maximum number of ledger entry read operations per ledger
    uint32 ledgerMaxReadLedgerEntries;
    // Maximum number of bytes that can be read per ledger
    uint32 ledgerMaxReadBytes;
    // Maximum number of ledger entry write operations per ledger
    uint32 ledgerMaxWriteLedgerEntries;
    // Maximum number of bytes that can be written per ledger
    uint32 ledgerMaxWriteBytes;

    // Maximum number of ledger entry read operations per transaction
    uint32 txMaxReadLedgerEntries;
    // Maximum number of bytes that can be read per transaction
    uint32 txMaxReadBytes;
    // Maximum number of ledger entry write operations per transaction
    uint32 txMaxWriteLedgerEntries;
    // Maximum number of bytes that can be written per transaction
    uint32 txMaxWriteBytes;

    int64 feeReadLedgerEntry;  // Fee per ledger entry read
    int64 feeWriteLedgerEntry; // Fee per ledger entry write

    int64 feeRead1KB;  // Fee for reading 1KB    
    int64 feeWrite1KB; // Fee for writing 1KB

    // Bucket list fees grow slowly up to that size
    int64 bucketListSizeBytes;
    // Fee rate in stroops when the bucket list is empty
    int64 bucketListFeeRateLow;
    // Fee rate in stroops when the bucket list reached bucketListSizeBytes
    int64 bucketListFeeRateHigh;
    // Rate multiplier for any additional data past the first bucketListSizeBytes
    uint32 bucketListGrowthFactor;
};

// Historical data (pushed to core archives) settings for contracts.
struct ConfigSettingContractHistoricalDataV0
{
    int64 feeHistorical1KB; // Fee for storing 1KB in archives
};

// Meta data (pushed to downstream systems) settings for contracts.
struct ConfigSettingContractMetaDataV0
{
    // Maximum size of extended meta data produced by a transaction
    uint32 txMaxExtendedMetaDataSizeBytes;
    // Fee for generating 1KB of extended meta data
    int64 feeExtendedMetaData1KB;
};

// Bandwidth related data settings for contracts
struct ConfigSettingContractBandwidthV0
{
    // Maximum size in bytes to propagate per ledger
    uint32 ledgerMaxPropagateSizeBytes;
    // Maximum size in bytes for a transaction
    uint32 txMaxSizeBytes;

    // Fee for propagating 1KB of data
    int64 feePropagateData1KB;
};

enum ContractCostType {
    // Cost of running 1 wasm instruction
    WasmInsnExec = 0,
    // Cost of growing wasm linear memory by 1 page
    WasmMemAlloc = 1,
    // Cost of allocating a chuck of host memory (in bytes)
    HostMemAlloc = 2,
    // Cost of copying a chuck of bytes into a pre-allocated host memory
    HostMemCpy = 3,
    // Cost of comparing two slices of host memory
    HostMemCmp = 4,
    // Cost of a host function invocation, not including the actual work done by the function
    InvokeHostFunction = 5,
    // Cost of visiting a host object from the host object storage
    // Only thing to make sure is the guest can't visitObject repeatly without incurring some charges elsewhere.
    VisitObject = 6,
    // Tracks a single Val (RawVal or primative Object like U64) <=> ScVal
    // conversion cost. Most of these Val counterparts in ScVal (except e.g.
    // Symbol) consumes a single int64 and therefore is a constant overhead.
    ValXdrConv = 7,
    // Cost of serializing an xdr object to bytes
    ValSer = 8,
    // Cost of deserializing an xdr object from bytes
    ValDeser = 9,
    // Cost of computing the sha256 hash from bytes
    ComputeSha256Hash = 10,
    // Cost of computing the ed25519 pubkey from bytes
    ComputeEd25519PubKey = 11,
    // Cost of accessing an entry in a Map.
    MapEntry = 12,
    // Cost of accessing an entry in a Vec
    VecEntry = 13,
    // Cost of guarding a frame, which involves pushing and poping a frame and capturing a rollback point.
    GuardFrame = 14,
    // Cost of verifying ed25519 signature of a payload.
    VerifyEd25519Sig = 15,
    // Cost of reading a slice of vm linear memory
    VmMemRead = 16,
    // Cost of writing to a slice of vm linear memory
    VmMemWrite = 17,
    // Cost of instantiation a VM from wasm bytes code.
    VmInstantiation = 18,
    // Roundtrip cost of invoking a VM function from the host.
    InvokeVmFunction = 19,
    // Cost of charging a value to the budgeting system.
    ChargeBudget = 20
};

struct ContractCostParamEntry {
    int64 constTerm;
    int64 linearTerm;
    // use `ext` to add more terms (e.g. higher order polynomials) in the future
    ExtensionPoint ext;
};

// limits the ContractCostParams size to 20kB
const CONTRACT_COST_COUNT_LIMIT = 1024;

typedef ContractCostParamEntry ContractCostParams<CONTRACT_COST_COUNT_LIMIT>;

// Identifiers of all the network settings.
enum ConfigSettingID
{
    CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES = 0,
    CONFIG_SETTING_CONTRACT_COMPUTE_V0 = 1,
    CONFIG_SETTING_CONTRACT_LEDGER_COST_V0 = 2,
    CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0 = 3,
    CONFIG_SETTING_CONTRACT_META_DATA_V0 = 4,
    CONFIG_SETTING_CONTRACT_BANDWIDTH_V0 = 5,
    CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS = 6,
    CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES = 7,
    CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES = 8,
    CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES = 9
};

union ConfigSettingEntry switch (ConfigSettingID configSettingID)
{
case CONFIG_SETTING_CONTRACT_MAX_SIZE_BYTES:
    uint32 contractMaxSizeBytes;
case CONFIG_SETTING_CONTRACT_COMPUTE_V0:
    ConfigSettingContractComputeV0 contractCompute;
case CONFIG_SETTING_CONTRACT_LEDGER_COST_V0:
    ConfigSettingContractLedgerCostV0 contractLedgerCost;
case CONFIG_SETTING_CONTRACT_HISTORICAL_DATA_V0:
    ConfigSettingContractHistoricalDataV0 contractHistoricalData;
case CONFIG_SETTING_CONTRACT_META_DATA_V0:
    ConfigSettingContractMetaDataV0 contractMetaData;
case CONFIG_SETTING_CONTRACT_BANDWIDTH_V0:
    ConfigSettingContractBandwidthV0 contractBandwidth;
case CONFIG_SETTING_CONTRACT_COST_PARAMS_CPU_INSTRUCTIONS:
    ContractCostParams contractCostParamsCpuInsns;
case CONFIG_SETTING_CONTRACT_COST_PARAMS_MEMORY_BYTES:
    ContractCostParams contractCostParamsMemBytes;
case CONFIG_SETTING_CONTRACT_DATA_KEY_SIZE_BYTES:
    uint32 contractDataKeySizeBytes;
case CONFIG_SETTING_CONTRACT_DATA_ENTRY_SIZE_BYTES:
    uint32 contractDataEntrySizeBytes;
};
}