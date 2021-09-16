# Python SDK Example Documentation

This is a series of examples on how to use this SDK to interact with Stellar Core, To avoid errors after the usual Testnet Reset, a Setup.py file was introduced as describe [HERE](https://github.com/StellarCN/py-stellar-base/issues/407)


## How To Use Examples

After Downloading the repo (You can find Instructions [HERE](https://github.com/StellarCN/py-stellar-base))

    > cd py-stellar-base
    > cd examples
    > python setup.py

This requires you to enter an amount of account you want to create on Testnet(You can continue to use the default amount which is 5)

After the Setup is done, you will have the following in a .stellar_env file in your current working directory;

## * **private keys**
## * **Public Keys**
## * **Asset Object**

## USING THE PRIVATE KEYS
This is by default, used for signing transaction in the example file, you can change them within the example file if you want, they are named "source_key_0", "source_key_1" and so on.

To use any of the Source Key to sign Transaction, You just need to
        
```python
    from e_utils import read_key
    adc = read_key()
    .....

    transaction.sign(adc['source_key_3'])
```

## USING THE PUBLIC KEYS
These public keys are used as disposable public address and are used where you dont need that public key to sign a transaction, mainly as destination account, they are named "destination_acct_0", "destination_acct_1", and so on, reference to their private key is not stored anywhere.

To use any of the Public keys

```python

    from stellar_sdk import Account, Keypair, Network, TransactionBuilder
    from stellar_sdk.sep.txrep import from_txrep, to_txrep
    from e_utils import read_key

    key_func = read_key()
    destination_address = func_key['destination_acct_0']
    ...

    inner_tx = (
    TransactionBuilder(
        source_account=inner_account,
        network_passphrase=network_passphrase,
        base_fee=50,
        v1=True,
    )
    .append_payment_op(destination=destination_address, amount="100", asset_code="XLM")
    .build()
)

```
## USING THE ASSET OBJECT
The Asset created is mainly to be used for sending transaction (other than XLM), placing order on testnet, etc. You can find details about the asset in the **.stellar_env** file in your current workig directory.
* **asset_key** -- This is the private key for the issuing Account
* **asset_code** -- The Asset Code
* **asset_issuer** -- The Asset Issuer
You can change the deafult asset code in the [Setup.py](./setup.py) file.

With this little changes, you can always run the Setup file as describe above to get new keys or in case of testnet reset
