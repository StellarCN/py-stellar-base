
enum AccountFlags
{ // masks for each flag
    AUTH_REQUIRED_FLAG = 0x1
};

/* AccountEntry

    Main entry representing a user in Stellar. All transactions are performed
    using an account.

    Other ledger entries created require an account.

*/