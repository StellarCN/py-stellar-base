




typedef opaque Hash[32];
typedef opaque uint256[32];

typedef unsigned int uint32;
typedef int int32;

typedef unsigned hyper uint64;
typedef hyper int64;

enum CryptoKeyType
{
    KEY_TYPE_ED25519 = 0
};

union PublicKey switch (CryptoKeyType type)
{
case KEY_TYPE_ED25519:
    uint256 ed25519;
};


typedef opaque Signature<64>;

typedef opaque SignatureHint[4];

typedef PublicKey NodeID;

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





%#include "xdr/Stellar-types.h"


typedef opaque Value<>;

struct SCPBallot
{
    uint32 counter; 
    Value value;    
};

enum SCPStatementType
{
    SCP_ST_PREPARE = 0,
    SCP_ST_CONFIRM = 1,
    SCP_ST_EXTERNALIZE = 2,
    SCP_ST_NOMINATE = 3
};

struct SCPNomination
{
    Hash quorumSetHash; 
    Value votes<>;      
    Value accepted<>;   
};

struct SCPStatement
{
    NodeID nodeID;    
    uint64 slotIndex; 

    union switch (SCPStatementType type)
    {
    case SCP_ST_PREPARE:
        struct
        {
            Hash quorumSetHash;       
            SCPBallot ballot;         
            SCPBallot* prepared;      
            SCPBallot* preparedPrime; 
            uint32 nC;                
            uint32 nP;                
        } prepare;
    case SCP_ST_CONFIRM:
        struct
        {
            Hash quorumSetHash; 
            uint32 nPrepared;   
            SCPBallot commit;   
            uint32 nP;          
        } confirm;
    case SCP_ST_EXTERNALIZE:
        struct
        {
            SCPBallot commit; 
            uint32 nP;        
            
            
            Hash commitQuorumSetHash; 
        } externalize;
    case SCP_ST_NOMINATE:
        SCPNomination nominate;
    }
    pledges;
};

struct SCPEnvelope
{
    SCPStatement statement;
    Signature signature;
};



struct SCPQuorumSet
{
    uint32 threshold;
    PublicKey validators<>;
    SCPQuorumSet innerSets<>;
};




%#include "xdr/Stellar-transaction.h"


typedef opaque UpgradeType<128>;

/* StellarValue is the value used by SCP to reach consensus on a given ledger
*/
struct StellarValue
{
    Hash txSetHash;   
    uint64 closeTime; 

    
    
    
    
    
    UpgradeType upgrades<6>;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

/* The LedgerHeader is the highest level structure representing the
 * state of a ledger, cryptographically linked to previous ledgers.
*/
struct LedgerHeader
{
    uint32 ledgerVersion;    
    Hash previousLedgerHash; 
    StellarValue scpValue;   
    Hash txSetResultHash;    
    Hash bucketListHash;     

    uint32 ledgerSeq; 

    int64 totalCoins; 
                      

    int64 feePool;       
    uint32 inflationSeq; 

    uint64 idPool; 

    uint32 baseFee;     
    uint32 baseReserve; 

    uint32 maxTxSetSize; 

    Hash skipList[4]; 
                      
                      
                      
                      

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

/* Ledger upgrades
note that the `upgrades` field from StellarValue is normalized such that
it only contains one entry per LedgerUpgradeType, and entries are sorted
in ascending order
*/
enum LedgerUpgradeType
{
    LEDGER_UPGRADE_VERSION = 1,
    LEDGER_UPGRADE_BASE_FEE = 2,
    LEDGER_UPGRADE_MAX_TX_SET_SIZE = 3
};

union LedgerUpgrade switch (LedgerUpgradeType type)
{
case LEDGER_UPGRADE_VERSION:
    uint32 newLedgerVersion; 
case LEDGER_UPGRADE_BASE_FEE:
    uint32 newBaseFee; 
case LEDGER_UPGRADE_MAX_TX_SET_SIZE:
    uint32 newMaxTxSetSize; 
};

/* Entries used to define the bucket list */

union LedgerKey switch (LedgerEntryType type)
{
case ACCOUNT:
    struct
    {
        AccountID accountID;
    } account;

case TRUSTLINE:
    struct
    {
        AccountID accountID;
        Asset asset;
    } trustLine;

case OFFER:
    struct
    {
        AccountID sellerID;
        uint64 offerID;
    } offer;
};

enum BucketEntryType
{
    LIVEENTRY = 0,
    DEADENTRY = 1
};

union BucketEntry switch (BucketEntryType type)
{
case LIVEENTRY:
    LedgerEntry liveEntry;

case DEADENTRY:
    LedgerKey deadEntry;
};



const MAX_TX_PER_LEDGER = 5000;
struct TransactionSet
{
    Hash previousLedgerHash;
    TransactionEnvelope txs<MAX_TX_PER_LEDGER>;
};

struct TransactionResultPair
{
    Hash transactionHash;
    TransactionResult result; 
};


struct TransactionResultSet
{
    TransactionResultPair results<MAX_TX_PER_LEDGER>;
};



struct TransactionHistoryEntry
{
    uint32 ledgerSeq;
    TransactionSet txSet;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

struct TransactionHistoryResultEntry
{
    uint32 ledgerSeq;
    TransactionResultSet txResultSet;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

struct LedgerHeaderHistoryEntry
{
    Hash hash;
    LedgerHeader header;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};



enum LedgerEntryChangeType
{
    LEDGER_ENTRY_CREATED = 0, 
    LEDGER_ENTRY_UPDATED = 1, 
    LEDGER_ENTRY_REMOVED = 2  
};

union LedgerEntryChange switch (LedgerEntryChangeType type)
{
case LEDGER_ENTRY_CREATED:
    LedgerEntry created;
case LEDGER_ENTRY_UPDATED:
    LedgerEntry updated;
case LEDGER_ENTRY_REMOVED:
    LedgerKey removed;
};

typedef LedgerEntryChange LedgerEntryChanges<>;

struct OperationMeta
{
    LedgerEntryChanges changes;
};

union TransactionMeta switch (int v)
{
case 0:
    OperationMeta operations<>;
};




%#include "xdr/Stellar-types.h"


typedef PublicKey AccountID;
typedef opaque Thresholds[4];
typedef string string32<32>;
typedef uint64 SequenceNumber;

enum AssetType
{
    ASSET_TYPE_NATIVE = 0,
    ASSET_TYPE_CREDIT_ALPHANUM4 = 1,
    ASSET_TYPE_CREDIT_ALPHANUM12 = 2
};

union Asset switch (AssetType type)
{
case ASSET_TYPE_NATIVE: 
    void;

case ASSET_TYPE_CREDIT_ALPHANUM4:
    struct
    {
        opaque assetCode[4]; 
        AccountID issuer;
    } alphaNum4;

case ASSET_TYPE_CREDIT_ALPHANUM12:
    struct
    {
        opaque assetCode[12]; 
        AccountID issuer;
    } alphaNum12;

    
};


struct Price
{
    int32 n; 
    int32 d; 
};



enum ThresholdIndexes
{
    THRESHOLD_MASTER_WEIGHT = 0,
    THRESHOLD_LOW = 1,
    THRESHOLD_MED = 2,
    THRESHOLD_HIGH = 3
};

enum LedgerEntryType
{
    ACCOUNT = 0,
    TRUSTLINE = 1,
    OFFER = 2
};

struct Signer
{
    AccountID pubKey;
    uint32 weight; 
};

enum AccountFlags
{ 

    
    
    
    AUTH_REQUIRED_FLAG = 0x1,
    
    
    AUTH_REVOCABLE_FLAG = 0x2,
    
    AUTH_IMMUTABLE_FLAG = 0x4
};

/* AccountEntry

    Main entry representing a user in Stellar. All transactions are
    performed using an account.

    Other ledger entries created require an account.

*/

struct AccountEntry
{
    AccountID accountID;      
    int64 balance;            
    SequenceNumber seqNum;    
    uint32 numSubEntries;     
                              
    AccountID* inflationDest; 
    uint32 flags;             

    string32 homeDomain; 

    
    
    Thresholds thresholds;

    Signer signers<20>; 

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

/* TrustLineEntry
    A trust line represents a specific trust relationship with
    a credit/issuer (limit, authorization)
    as well as the balance.
*/

enum TrustLineFlags
{
    
    AUTHORIZED_FLAG = 1
};

struct TrustLineEntry
{
    AccountID accountID; 
    Asset asset;         
    int64 balance;       
                         

    int64 limit;  
    uint32 flags; 

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

enum OfferEntryFlags
{
    
    PASSIVE_FLAG = 1
};

/* OfferEntry
    An offer is the building block of the offer book, they are automatically
    claimed by payments when the price set by the owner is met.

    For example an Offer is selling 10A where 1A is priced at 1.5B

*/
struct OfferEntry
{
    AccountID sellerID;
    uint64 offerID;
    Asset selling; 
    Asset buying;  
    int64 amount;  

    /* price for this offer:
        price of A in terms of B
        price=AmountB/AmountA=priceNumerator/priceDenominator
        price is after fees
    */
    Price price;
    uint32 flags; 

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

struct LedgerEntry
{
    uint32 lastModifiedLedgerSeq; 

    union switch (LedgerEntryType type)
    {
    case ACCOUNT:
        AccountEntry account;
    case TRUSTLINE:
        TrustLineEntry trustLine;
    case OFFER:
        OfferEntry offer;
    }
    data;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};




enum EnvelopeType
{
    ENVELOPE_TYPE_SCP = 1,
    ENVELOPE_TYPE_TX = 2,
    ENVELOPE_TYPE_AUTH = 3
};




%#include "xdr/Stellar-ledger.h"


enum ErrorCode
{
    ERR_MISC = 0, 
    ERR_DATA = 1, 
    ERR_CONF = 2, 
    ERR_AUTH = 3, 
    ERR_LOAD = 4  
};

struct Error
{
    ErrorCode code;
    string msg<100>;
};

struct AuthCert
{
    Curve25519Public pubkey;
    uint64 expiration;
    Signature sig;
};

struct Hello
{
    uint32 ledgerVersion;
    uint32 overlayVersion;
    Hash networkID;
    string versionStr<100>;
    int listeningPort;
    NodeID peerID;
    AuthCert cert;
    uint256 nonce;
};

struct Auth
{
    
    
    int unused;
};

enum IPAddrType
{
    IPv4 = 0,
    IPv6 = 1
};

struct PeerAddress
{
    union switch (IPAddrType type)
    {
    case IPv4:
        opaque ipv4[4];
    case IPv6:
        opaque ipv6[16];
    } ip;
    uint32 port;
    uint32 numFailures;
};

enum MessageType
{
    ERROR_MSG = 0,
    HELLO = 1,
    AUTH = 2,
    DONT_HAVE = 3,

    GET_PEERS = 4, 
    PEERS = 5,

    GET_TX_SET = 6, 
    TX_SET = 7,

    TRANSACTION = 8, 

    
    GET_SCP_QUORUMSET = 9,
    SCP_QUORUMSET = 10,
    SCP_MESSAGE = 11
};

struct DontHave
{
    MessageType type;
    uint256 reqHash;
};

union StellarMessage switch (MessageType type)
{
case ERROR_MSG:
    Error error;
case HELLO:
    Hello hello;
case AUTH:
    Auth auth;
case DONT_HAVE:
    DontHave dontHave;
case GET_PEERS:
    void;
case PEERS:
    PeerAddress peers<>;

case GET_TX_SET:
    uint256 txSetHash;
case TX_SET:
    TransactionSet txSet;

case TRANSACTION:
    TransactionEnvelope transaction;


case GET_SCP_QUORUMSET:
    uint256 qSetHash;
case SCP_QUORUMSET:
    SCPQuorumSet qSet;
case SCP_MESSAGE:
    SCPEnvelope envelope;
};

struct AuthenticatedMessage
{
   uint64 sequence;
   StellarMessage message;
   HmacSha256Mac mac;
};





%#include "xdr/Stellar-ledger-entries.h"


struct DecoratedSignature
{
    SignatureHint hint;  
    Signature signature; 
};

enum OperationType
{
    CREATE_ACCOUNT = 0,
    PAYMENT = 1,
    PATH_PAYMENT = 2,
    MANAGE_OFFER = 3,
    CREATE_PASSIVE_OFFER = 4,
    SET_OPTIONS = 5,
    CHANGE_TRUST = 6,
    ALLOW_TRUST = 7,
    ACCOUNT_MERGE = 8,
    INFLATION = 9
};

/* CreateAccount
Creates and funds a new account with the specified starting balance.

Threshold: med

Result: CreateAccountResult

*/

struct CreateAccountOp
{
    AccountID destination; 
    int64 startingBalance; 
};

/* Payment

    Send an amount in specified asset to a destination account.

    Threshold: med

    Result: PaymentResult
*/
struct PaymentOp
{
    AccountID destination; 
    Asset asset;           
    int64 amount;          
};

/* PathPayment

send an amount to a destination account through a path.
(up to sendMax, sendAsset)
(X0, Path[0]) .. (Xn, Path[n])
(destAmount, destAsset)

Threshold: med

Result: PathPaymentResult
*/
struct PathPaymentOp
{
    Asset sendAsset; 
    int64 sendMax;   
                     
                     

    AccountID destination; 
    Asset destAsset;       
    int64 destAmount;      

    Asset path<5>; 
};

/* Creates, updates or deletes an offer

Threshold: med

Result: ManageOfferResult

*/
struct ManageOfferOp
{
    Asset selling;
    Asset buying;
    int64 amount; 
    Price price;  

    
    uint64 offerID;
};

/* Creates an offer that doesn't take offers of the same price

Threshold: med

Result: CreatePassiveOfferResult

*/
struct CreatePassiveOfferOp
{
    Asset selling; 
    Asset buying;  
    int64 amount;  
    Price price;   
};

/* Set Account Options

    updates "AccountEntry" fields.
    note: updating thresholds or signers requires high threshold

    Threshold: med or high

    Result: SetOptionsResult
*/

struct SetOptionsOp
{
    AccountID* inflationDest; 

    uint32* clearFlags; 
    uint32* setFlags;   

    
    uint32* masterWeight; 
    uint32* lowThreshold;
    uint32* medThreshold;
    uint32* highThreshold;

    string32* homeDomain; 

    
    
    Signer* signer;
};

/* Creates, updates or deletes a trust line

    Threshold: med

    Result: ChangeTrustResult

*/
struct ChangeTrustOp
{
    Asset line;

    
    int64 limit;
};

/* Updates the "authorized" flag of an existing trust line
   this is called by the issuer of the related asset.

   note that authorize can only be set (and not cleared) if
   the issuer account does not have the AUTH_REVOCABLE_FLAG set
   Threshold: low

   Result: AllowTrustResult
*/
struct AllowTrustOp
{
    AccountID trustor;
    union switch (AssetType type)
    {
    
    case ASSET_TYPE_CREDIT_ALPHANUM4:
        opaque assetCode4[4];

    case ASSET_TYPE_CREDIT_ALPHANUM12:
        opaque assetCode12[12];

        
    }
    asset;

    bool authorize;
};

/* Inflation
    Runs inflation

Threshold: low

Result: InflationResult

*/

/* AccountMerge
    Transfers native balance to destination account.

    Threshold: high

    Result : AccountMergeResult
*/

/* An operation is the lowest unit of work that a transaction does */
struct Operation
{
    
    
    
    AccountID* sourceAccount;

    union switch (OperationType type)
    {
    case CREATE_ACCOUNT:
        CreateAccountOp createAccountOp;
    case PAYMENT:
        PaymentOp paymentOp;
    case PATH_PAYMENT:
        PathPaymentOp pathPaymentOp;
    case MANAGE_OFFER:
        ManageOfferOp manageOfferOp;
    case CREATE_PASSIVE_OFFER:
        CreatePassiveOfferOp createPassiveOfferOp;
    case SET_OPTIONS:
        SetOptionsOp setOptionsOp;
    case CHANGE_TRUST:
        ChangeTrustOp changeTrustOp;
    case ALLOW_TRUST:
        AllowTrustOp allowTrustOp;
    case ACCOUNT_MERGE:
        AccountID destination;
    case INFLATION:
        void;
    }
    body;
};

enum MemoType
{
    MEMO_NONE = 0,
    MEMO_TEXT = 1,
    MEMO_ID = 2,
    MEMO_HASH = 3,
    MEMO_RETURN = 4
};

union Memo switch (MemoType type)
{
case MEMO_NONE:
    void;
case MEMO_TEXT:
    string text<28>;
case MEMO_ID:
    uint64 id;
case MEMO_HASH:
    Hash hash; 
case MEMO_RETURN:
    Hash retHash; 
};

struct TimeBounds
{
    uint64 minTime;
    uint64 maxTime;
};

/* a transaction is a container for a set of operations
    - is executed by an account
    - fees are collected from the account
    - operations are executed in order as one ACID transaction
          either all operations are applied or none are
          if any returns a failing code
*/

struct Transaction
{
    
    AccountID sourceAccount;

    
    uint32 fee;

    
    SequenceNumber seqNum;

    
    TimeBounds* timeBounds;

    Memo memo;

    Operation operations<100>;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};

/* A TransactionEnvelope wraps a transaction with signatures. */
struct TransactionEnvelope
{
    Transaction tx;
    DecoratedSignature signatures<20>;
};

/* Operation Results section */

/* This result is used when offers are taken during an operation */
struct ClaimOfferAtom
{
    
    AccountID sellerID; 
    uint64 offerID;

    
    Asset assetSold;
    int64 amountSold;

    
    Asset assetBought;
    int64 amountBought;
};

/******* CreateAccount Result ********/

enum CreateAccountResultCode
{
    
    CREATE_ACCOUNT_SUCCESS = 0, 

    
    CREATE_ACCOUNT_MALFORMED = -1,   
    CREATE_ACCOUNT_UNDERFUNDED = -2, 
    CREATE_ACCOUNT_LOW_RESERVE =
        -3, 
    CREATE_ACCOUNT_ALREADY_EXIST = -4 
};

union CreateAccountResult switch (CreateAccountResultCode code)
{
case CREATE_ACCOUNT_SUCCESS:
    void;
default:
    void;
};

/******* Payment Result ********/

enum PaymentResultCode
{
    
    PAYMENT_SUCCESS = 0, 

    
    PAYMENT_MALFORMED = -1,          
    PAYMENT_UNDERFUNDED = -2,        
    PAYMENT_SRC_NO_TRUST = -3,       
    PAYMENT_SRC_NOT_AUTHORIZED = -4, 
    PAYMENT_NO_DESTINATION = -5,     
    PAYMENT_NO_TRUST = -6,       
    PAYMENT_NOT_AUTHORIZED = -7, 
    PAYMENT_LINE_FULL = -8,      
    PAYMENT_NO_ISSUER = -9       
};

union PaymentResult switch (PaymentResultCode code)
{
case PAYMENT_SUCCESS:
    void;
default:
    void;
};

/******* Payment Result ********/

enum PathPaymentResultCode
{
    
    PATH_PAYMENT_SUCCESS = 0, 

    
    PATH_PAYMENT_MALFORMED = -1,          
    PATH_PAYMENT_UNDERFUNDED = -2,        
    PATH_PAYMENT_SRC_NO_TRUST = -3,       
    PATH_PAYMENT_SRC_NOT_AUTHORIZED = -4, 
    PATH_PAYMENT_NO_DESTINATION = -5,     
    PATH_PAYMENT_NO_TRUST = -6,           
    PATH_PAYMENT_NOT_AUTHORIZED = -7,     
    PATH_PAYMENT_LINE_FULL = -8,          
    PATH_PAYMENT_NO_ISSUER = -9,          
    PATH_PAYMENT_TOO_FEW_OFFERS = -10,    
    PATH_PAYMENT_OFFER_CROSS_SELF = -11,  
    PATH_PAYMENT_OVER_SENDMAX = -12       
};

struct SimplePaymentResult
{
    AccountID destination;
    Asset asset;
    int64 amount;
};

union PathPaymentResult switch (PathPaymentResultCode code)
{
case PATH_PAYMENT_SUCCESS:
    struct
    {
        ClaimOfferAtom offers<>;
        SimplePaymentResult last;
    } success;
case PATH_PAYMENT_NO_ISSUER:
    Asset noIssuer; 
default:
    void;
};

/******* ManageOffer Result ********/

enum ManageOfferResultCode
{
    
    MANAGE_OFFER_SUCCESS = 0,

    
    MANAGE_OFFER_MALFORMED = -1,     
    MANAGE_OFFER_SELL_NO_TRUST = -2, 
    MANAGE_OFFER_BUY_NO_TRUST = -3,  
    MANAGE_OFFER_SELL_NOT_AUTHORIZED = -4, 
    MANAGE_OFFER_BUY_NOT_AUTHORIZED = -5,  
    MANAGE_OFFER_LINE_FULL = -6,      
    MANAGE_OFFER_UNDERFUNDED = -7,    
    MANAGE_OFFER_CROSS_SELF = -8,     
    MANAGE_OFFER_SELL_NO_ISSUER = -9, 
    MANAGE_OFFER_BUY_NO_ISSUER = -10, 

    
    MANAGE_OFFER_NOT_FOUND = -11, 

    MANAGE_OFFER_LOW_RESERVE = -12 
};

enum ManageOfferEffect
{
    MANAGE_OFFER_CREATED = 0,
    MANAGE_OFFER_UPDATED = 1,
    MANAGE_OFFER_DELETED = 2
};

struct ManageOfferSuccessResult
{
    
    ClaimOfferAtom offersClaimed<>;

    union switch (ManageOfferEffect effect)
    {
    case MANAGE_OFFER_CREATED:
    case MANAGE_OFFER_UPDATED:
        OfferEntry offer;
    default:
        void;
    }
    offer;
};

union ManageOfferResult switch (ManageOfferResultCode code)
{
case MANAGE_OFFER_SUCCESS:
    ManageOfferSuccessResult success;
default:
    void;
};

/******* SetOptions Result ********/

enum SetOptionsResultCode
{
    
    SET_OPTIONS_SUCCESS = 0,
    
    SET_OPTIONS_LOW_RESERVE = -1,      
    SET_OPTIONS_TOO_MANY_SIGNERS = -2, 
    SET_OPTIONS_BAD_FLAGS = -3,        
    SET_OPTIONS_INVALID_INFLATION = -4,      
    SET_OPTIONS_CANT_CHANGE = -5,            
    SET_OPTIONS_UNKNOWN_FLAG = -6,           
    SET_OPTIONS_THRESHOLD_OUT_OF_RANGE = -7, 
    SET_OPTIONS_BAD_SIGNER = -8,             
    SET_OPTIONS_INVALID_HOME_DOMAIN = -9     
};

union SetOptionsResult switch (SetOptionsResultCode code)
{
case SET_OPTIONS_SUCCESS:
    void;
default:
    void;
};

/******* ChangeTrust Result ********/

enum ChangeTrustResultCode
{
    
    CHANGE_TRUST_SUCCESS = 0,
    
    CHANGE_TRUST_MALFORMED = -1,     
    CHANGE_TRUST_NO_ISSUER = -2,     
    CHANGE_TRUST_INVALID_LIMIT = -3, 
                                     
    CHANGE_TRUST_LOW_RESERVE = -4 
};

union ChangeTrustResult switch (ChangeTrustResultCode code)
{
case CHANGE_TRUST_SUCCESS:
    void;
default:
    void;
};

/******* AllowTrust Result ********/

enum AllowTrustResultCode
{
    
    ALLOW_TRUST_SUCCESS = 0,
    
    ALLOW_TRUST_MALFORMED = -1,     
    ALLOW_TRUST_NO_TRUST_LINE = -2, 
                                    
    ALLOW_TRUST_TRUST_NOT_REQUIRED = -3,
    ALLOW_TRUST_CANT_REVOKE = -4 
};

union AllowTrustResult switch (AllowTrustResultCode code)
{
case ALLOW_TRUST_SUCCESS:
    void;
default:
    void;
};

/******* AccountMerge Result ********/

enum AccountMergeResultCode
{
    
    ACCOUNT_MERGE_SUCCESS = 0,
    
    ACCOUNT_MERGE_MALFORMED = -1,      
    ACCOUNT_MERGE_NO_ACCOUNT = -2,     
    ACCOUNT_MERGE_IMMUTABLE_SET = -3,  
    ACCOUNT_MERGE_HAS_SUB_ENTRIES = -4 
};

union AccountMergeResult switch (AccountMergeResultCode code)
{
case ACCOUNT_MERGE_SUCCESS:
    int64 sourceAccountBalance; 
default:
    void;
};

/******* Inflation Result ********/

enum InflationResultCode
{
    
    INFLATION_SUCCESS = 0,
    
    INFLATION_NOT_TIME = -1
};

struct InflationPayout 
{
    AccountID destination;
    int64 amount;
};

union InflationResult switch (InflationResultCode code)
{
case INFLATION_SUCCESS:
    InflationPayout payouts<>;
default:
    void;
};

/* High level Operation Result */

enum OperationResultCode
{
    opINNER = 0, 

    opBAD_AUTH = -1,  
    opNO_ACCOUNT = -2 
};

union OperationResult switch (OperationResultCode code)
{
case opINNER:
    union switch (OperationType type)
    {
    case CREATE_ACCOUNT:
        CreateAccountResult createAccountResult;
    case PAYMENT:
        PaymentResult paymentResult;
    case PATH_PAYMENT:
        PathPaymentResult pathPaymentResult;
    case MANAGE_OFFER:
        ManageOfferResult manageOfferResult;
    case CREATE_PASSIVE_OFFER:
        ManageOfferResult createPassiveOfferResult;
    case SET_OPTIONS:
        SetOptionsResult setOptionsResult;
    case CHANGE_TRUST:
        ChangeTrustResult changeTrustResult;
    case ALLOW_TRUST:
        AllowTrustResult allowTrustResult;
    case ACCOUNT_MERGE:
        AccountMergeResult accountMergeResult;
    case INFLATION:
        InflationResult inflationResult;
    }
    tr;
default:
    void;
};

enum TransactionResultCode
{
    txSUCCESS = 0, 

    txFAILED = -1, 

    txTOO_EARLY = -2,         
    txTOO_LATE = -3,          
    txMISSING_OPERATION = -4, 
    txBAD_SEQ = -5,           

    txBAD_AUTH = -6,             
    txINSUFFICIENT_BALANCE = -7, 
    txNO_ACCOUNT = -8,           
    txINSUFFICIENT_FEE = -9,     
    txBAD_AUTH_EXTRA = -10,      
    txINTERNAL_ERROR = -11       
};

struct TransactionResult
{
    int64 feeCharged; 

    union switch (TransactionResultCode code)
    {
    case txSUCCESS:
    case txFAILED:
        OperationResult results<>;
    default:
        void;
    }
    result;

    
    union switch (int v)
    {
    case 0:
        void;
    }
    ext;
};
