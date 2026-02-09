enum MessageType
{
    ERROR_MSG,    
    HELLO,
    DONT_HAVE,

    GET_PEERS,   // gets a list of peers this guy knows about        
    PEERS,

    GET_TX_SET,  // gets a particular txset by hash        
    TX_SET,    

    GET_VALIDATIONS, // gets validations for a given ledger hash        
    VALIDATIONS,    

    TRANSACTION, //pass on a tx you have heard about        
    JSON_TRANSACTION,

    // FBA        
    GET_FBA_QUORUMSET,        
    FBA_QUORUMSET,    
    FBA_MESSAGE
};

enum Color {
    RED=0,  
    GREEN=1,  
    BLUE=2  
};


enum Color2 {
    RED2=RED,  
    GREEN2=1,  
    BLUE2=2  
};

enum Color3 {
    RED_1=1,
    RED_2_TWO=2,
    RED_3=3
};
