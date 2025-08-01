// Copyright 2015 Stellar Development Foundation and contributors. Licensed
// under the Apache License, Version 2.0. See the COPYING file at the root
// of this distribution or at http://www.apache.org/licenses/LICENSE-2.0

namespace stellar
{

typedef opaque Hash[32];
typedef opaque uint256[32];

typedef unsigned int uint32;
typedef int int32;

typedef unsigned hyper uint64;
typedef hyper int64;

typedef uint64 TimePoint;
typedef uint64 Duration;

// An ExtensionPoint is always marshaled as a 32-bit 0 value.  At a
// later point, it can be replaced by a different union so as to
// extend a structure.
union ExtensionPoint switch (int v)
{
case 0:
    void;
};

enum CryptoKeyType
{
    KEY_TYPE_ED25519 = 0,
    KEY_TYPE_PRE_AUTH_TX = 1,
    KEY_TYPE_HASH_X = 2,
    KEY_TYPE_ED25519_SIGNED_PAYLOAD = 3,
    // MUXED enum values for supported type are derived from the enum values
    // above by ORing them with 0x100
    KEY_TYPE_MUXED_ED25519 = 0x100
};

enum PublicKeyType
{
    PUBLIC_KEY_TYPE_ED25519 = KEY_TYPE_ED25519
};

enum SignerKeyType
{
    SIGNER_KEY_TYPE_ED25519 = KEY_TYPE_ED25519,
    SIGNER_KEY_TYPE_PRE_AUTH_TX = KEY_TYPE_PRE_AUTH_TX,
    SIGNER_KEY_TYPE_HASH_X = KEY_TYPE_HASH_X,
    SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD = KEY_TYPE_ED25519_SIGNED_PAYLOAD
};

union PublicKey switch (PublicKeyType type)
{
case PUBLIC_KEY_TYPE_ED25519:
    uint256 ed25519;
};

union SignerKey switch (SignerKeyType type)
{
case SIGNER_KEY_TYPE_ED25519:
    uint256 ed25519;
case SIGNER_KEY_TYPE_PRE_AUTH_TX:
    /* SHA-256 Hash of TransactionSignaturePayload structure */
    uint256 preAuthTx;
case SIGNER_KEY_TYPE_HASH_X:
    /* Hash of random 256 bit preimage X */
    uint256 hashX;
case SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD:
    struct
    {
        /* Public key that must sign the payload. */
        uint256 ed25519;
        /* Payload to be raw signed by ed25519. */
        opaque payload<64>;
    } ed25519SignedPayload;
};

// variable size as the size depends on the signature scheme used
typedef opaque Signature<64>;

typedef opaque SignatureHint[4];

typedef PublicKey NodeID;
typedef PublicKey AccountID;

typedef Hash ContractID;

struct Curve25519Secret
{
    opaque key[32];
};

struct Curve25519Public
{
    opaque key[32];
};

struct HmacSha256Key
{
    opaque key[32];
};

struct HmacSha256Mac
{
    opaque mac[32];
};

struct ShortHashSeed
{
    opaque seed[16];
};

enum BinaryFuseFilterType
{
    BINARY_FUSE_FILTER_8_BIT = 0,
    BINARY_FUSE_FILTER_16_BIT = 1,
    BINARY_FUSE_FILTER_32_BIT = 2
};

struct SerializedBinaryFuseFilter
{
    BinaryFuseFilterType type;

    // Seed used to hash input to filter
    ShortHashSeed inputHashSeed;

    // Seed used for internal filter hash operations
    ShortHashSeed filterSeed;
    uint32 segmentLength;
    uint32 segementLengthMask;
    uint32 segmentCount;
    uint32 segmentCountLength;
    uint32 fingerprintLength; // Length in terms of element count, not bytes

    // Array of uint8_t, uint16_t, or uint32_t depending on filter type
    opaque fingerprints<>;
};

typedef Hash PoolID; // SHA256(LiquidityPoolParameters)

enum ClaimableBalanceIDType
{
    CLAIMABLE_BALANCE_ID_TYPE_V0 = 0
};

union ClaimableBalanceID switch (ClaimableBalanceIDType type)
{
case CLAIMABLE_BALANCE_ID_TYPE_V0:
    Hash v0;
};
}