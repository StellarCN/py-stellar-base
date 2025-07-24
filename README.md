# Stellar Python SDK

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/StellarCN/py-stellar-base/continuous-integration-workflow.yml?branch=main)](https://github.com/StellarCN/py-stellar-base/actions)
[![Read the Docs](https://img.shields.io/readthedocs/stellar-sdk.svg)](https://stellar-sdk.readthedocs.io/en/latest/)
[![PyPI - Downloads](https://static.pepy.tech/personalized-badge/stellar-sdk?period=total&units=abbreviation&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pypi.python.org/pypi/stellar-sdk)
[![Codecov](https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/main)](https://codecov.io/gh/StellarCN/py-stellar-base)
[![PyPI](https://img.shields.io/pypi/v/stellar-sdk.svg)](https://pypi.python.org/pypi/stellar-sdk)
[![Stellar Protocol](https://img.shields.io/badge/Stellar%20Protocol-23-blue)](https://developers.stellar.org/docs/learn/fundamentals/stellar-consensus-protocol)

py-stellar-base is a Python library for communicating with
a [Stellar Horizon server](https://github.com/stellar/go/tree/master/services/horizon) and [Stellar RPC server](https://developers.stellar.org/docs/data/apis/rpc). It is used for building Stellar apps on Python. It supports **Python 3.9+** as
well as PyPy 3.9+.

It provides:

- a networking layer API for Horizon endpoints.
- a networking layer API for Stellar RPC server methods.
- facilities for building and signing transactions, for communicating with a Stellar Horizon and Stellar RPC instance, and for submitting transactions or querying network history.

## Documentation

py-stellar-base's documentation can be found at https://stellar-sdk.readthedocs.io.

## Installing

```text
pip install --upgrade stellar-sdk
```

If you need to use asynchronous, please use the following command to install the required dependencies.

```text
pip install --upgrade stellar-sdk[aiohttp]
```

If you need to [Shamir backup](https://trezor.io/learn/advanced/standards-proposals/what-is-shamir-backup) support, please use the following command to install the required dependencies.

```
pip install --upgrade stellar-sdk[shamir]
```

We follow [Semantic Versioning 2.0.0](https://semver.org/), and I strongly
recommend that you specify its major version number in the dependency
file to avoid the unknown effects of breaking changes.

## A Simple Example

You can find more examples [here](./examples).

```python
# Alice pay 10.25 XLM to Bob
from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"

server = Server("https://horizon-testnet.stellar.org")
alice_account = server.load_account(alice_keypair.public_key)
base_fee = 100
transaction = (
    TransactionBuilder(
        source_account=alice_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=base_fee,
    )
    .add_text_memo("Hello, Stellar!")
    .append_payment_op(bob_address, Asset.native(), "10.25")
    .set_timeout(30)
    .build()
)
transaction.sign(alice_keypair)
response = server.submit_transaction(transaction)
print(response)
```

## stellar-contract-bindings

stellar-contract-bindings allows you to generate Python bindings for Stellar Soroban smart contracts, it makes calling
Stellar Soroban contracts easier. click [here](https://github.com/lightsail-network/stellar-contract-bindings) for more information.

## stellar-model

stellar-model allows you to parse the JSON returned by Stellar Horizon
into the Python models, click [here](https://github.com/StellarCN/stellar-model) for more information.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.

## Links

- Document: https://stellar-sdk.readthedocs.io
- Code: https://github.com/StellarCN/py-stellar-base
- Examples: https://github.com/StellarCN/py-stellar-base/tree/main/examples
- Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
- License: [Apache License 2.0](https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE)
- Releases: https://pypi.org/project/stellar-sdk/

Thank you to all the people who have already contributed to py-stellar-base!
