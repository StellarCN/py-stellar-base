# Python SDK Example Documentation

This is a series of examples on how to use this SDK to interact with Stellar Core, To avoid errors after the usual Testnet Reset, a Setup.py file was introduced as describe [HERE](https://github.com/StellarCN/py-stellar-base/issues/407)


## How To Use Examples

After Downloading the repo (You can find Instructions [HERE](https://github.com/StellarCN/py-stellar-base))

    > cd py-stellar-base
    > cd examples
    > python setup.py

This requires you to enter an amount of account you want to create on Testnet(You can continue to use the default amount which is 5)

After the Setup is done, you will have the following in a .stellar_env file in your current working directory;

5 private keys - This is by default used for signing transaction in the example file, you can change them within the example file if you want, they are named "source_key_0", "source_key_1", "source_key_2", "source_key_3", "source_key_4" 

To use any of the Source Key to sign Transaction, You just need to;
    
    
    from e_utils import read_key
    adc = read_key()
    .....

    transaction.sign(adc['source_key_3'])
    

5 Public Keys - This public keys are used as disposable public address and are used where you dont need that public key to sign a transaction, mainly as destination account, they are named "destination_acct_0", "destination_acct_1", "destination_acct_2", "destination_acct_3", "destination_acct_4"


    from stellar_sdk import Account, Keypair, Network, TransactionBuilder
    from stellar_sdk.sep.txrep import from_txrep, to_txrep
    from e_utils import read_key

    key_func = read_key()
    source_secret_key = key_func['source_key_0']

    source_keypair = Keypair.from_secret(source_secret_key)
    source_public_key = source_keypair.public_key

    receiver_public_key = key_func['destination_acct_0']
    source_account = Account(source_public_key, 12345)

With this little changes, you can always run the Setup file as describe above to get new keys
