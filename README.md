# py-stellar-base

[![Build Status](https://travis-ci.org/StellarCN/py-stellar-base.svg)](https://travis-ci.org/StellarCN/py-stellar-base)
[![PyPI](https://img.shields.io/pypi/v/stellar-base.svg)](https://pypi.python.org/pypi/stellar-base)
[![Read the Docs](https://img.shields.io/readthedocs/pip.svg)](https://stellar-base.readthedocs.io)

py-stellar-sdk is a Python library for communicating with a [Stellar Horizon server](https://github.com/stellar/go/tree/master/services/horizon). It is used for building Stellar apps on Python.

## Documentation
The documentation is hosted on [Read the Docs](https://stellar-base.readthedocs.io/).

## Quick Start

### 1. Install
#### 1.1 Install from pypi (Recommended)
```bash
pip install stellar-base
```

#### 1.2 Install from latest source code
The latest code may be unstable.
```bash
pip install git+git://github.com/StellarCN/py-stellar-base
```

### 2. Create a Stellar key pair
There are two methods for generating a key pair in `py-stellar-base`.

#### 2.1 Random generation
```python
from stellar_base.keypair import Keypair
kp = Keypair.random()
```

#### 2.2 Deterministic generation
In this method the key pair is deterministically generated from a mnemonic string, also known as "seed phrase".
First we generate a Unicode mnemonic string:
```python
from stellar_base.utils import StellarMnemonic
sm = StellarMnemonic("chinese") # here we use chinese, but default language is 'english'
m = sm.generate()
# or m = u'域 监 惜 国 期 碱 珍 继 造 监 剥 电' (must add u'' before the string if using Python 2)
```
The call `sm.generate()` prints out the generated mnemonic string, which is a phrase made of random words separated by
spaces. You should either write this phrase down or memorize it. Do not share your mnemonic string with anyone.

Now we use the mnemonic string `m` to generate the key pair:
```python
kp = Keypair.deterministic(m, lang='chinese')
```
And we can use the mnemonic string `m` to generate multiple key pairs:
```python
kp1 = Keypair.deterministic(m, lang='chinese', index=1)
kp2 = Keypair.deterministic(m, lang='chinese', index=2)
```
After the key pair generation, we can get a public key and a seed from it:
```python
publickey = kp.address().decode()
seed = kp.seed().decode()
```
The public key is also your account address. If someone needs to send you a transaction, you should share with them this key.
The seed is your secret. For safety, please keep it local and never send it through the Internet.

Whenever we forget/lose the public key, we can regenerate the key pair from the seed:
```python
from stellar_base.keypair import Keypair
kp = Keypair.from_seed(seed)
```
If we forget/lose both the public key and the seed, we can regenerate the key pair from the mnemonic string:
```python
from stellar_base.keypair import Keypair
seed_phrase = '...' # the word sequence that you wrote down or memorized
kp = Keypair.deterministic(seed_phrase, lang='chinese')
```

This is my favorite key pair in TESTNET, let's use them in the following steps.
```python
publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
seed = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
```

### 3. Create Account
After the key pair generation, you have already got the address, but it is not activated until someone transfers at least 1 lumen into it.

#### 3.1 Testnet
If you want to play in the Stellar test network, you can ask our Friendbot to create an account for you as shown below:
```python
import requests
publickey = kp.address().decode()
r = requests.get('https://friendbot.stellar.org/?addr=' + publickey)
```
#### 3.2 Livenet
On the other hand, if you would like to create an account in the livenet, you should buy some Stellar Lumens from an exchange. When you withdraw the Lumens into your new account, the exchange will automatically create the account for you.
However, if you want to create an account from another account of your own, you may run the following code:
```python
from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.operation import CreateAccount, Payment
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.memo import TextMemo
from stellar_base.horizon import horizon_livenet

# This creates a new Horizon Livenet instance
horizon = horizon_livenet()

# This is the seed (the StrKey representation of the secret seed that
# generates your private key from your original account that is funding the
# new account in the create account operation. You'll need the seed in order
# to sign off on the transaction. This is the source account.
old_account_seed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
old_account_keypair = Keypair.from_seed(old_account_seed)

# This is the new account ID (the StrKey representation of your newly
# created public key). This is the destination account.
new_account_addr = "GXXX"

amount = '1' # Your new account minimum balance (in XLM) to transfer over
# create the CreateAccount operation
op = CreateAccount(
    destination=new_account_addr,
    starting_balance=amount
)
# create a memo
memo = TextMemo('Hello, Stellar!')

# Get the current sequence of the source account by contacting Horizon. You
# should also check the response for errors!
# Python 3
sequence = horizon.account(old_account_keypair.address().decode()).get('sequence')
# Python 2
# sequence = horizon.account(old_account_keypair.address()).get('sequence')

# Create a transaction with our single create account operation, with the
# default fee of 100 stroops as of this writing (0.00001 XLM)
tx = Transaction(
    source=kp.address().decode(),
    sequence=sequence,
    memo=memo,
    operations=[
        op,
    ],
)
# Build a transaction envelope, ready to be signed.
envelope = Te(tx=tx, network_id="PUBLIC")

# Sign the transaction envelope with the source keypair
envelope.sign(old_account_keypair)

# Submit the transaction to Horizon
te_xdr = envelope.xdr()
response = horizon.submit(te_xdr)
```
Then, you can check the status of this operation with the response.

### 4. Check account
#### 4.1 Basic info
After creating the account, we may check the basic information of the account.
```python
from stellar_base.address import Address
publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
address = Address(address=publickey) # address = Address(address=publickey,network='public') for livenet
address.get() # get the updated information
```
Now you can check the address `balance`, `sequence`, `flags`, `signers`, `data` etc.
```python
print("Balances: {}".format(address.balances))
print("Sequence Number: {}".format(address.sequence))
print("Flags: {}".format(address.flags))
print("Signers: {}".format(address.signers))
print("Data: {}".format(address.data))
```

#### 4.2 Check payments
We can check the most recent payments by:
`address.payments()`

We can use three parameters to customize the query: `limit`, `order`, and `cursor` (`paging_token`), and the default value for them are respectively: `limit=10, order="asc", cursor=0`.

So if you need to check payments after a specific cursor, try:
`address.payments(cursor='4225135422738433', limit=20, order='asc')`

Horizon has SSE support for push data, if you really want to, use it like this: `address.payments(sse=True, cursor='4225135422738433')`

#### 4.3 Check others
Just like payments, we can check `transactions`, `effects`, `offers`, and `operations` by:
```python
address.transactions()
address.effects()
address.offers()
address.operations()
```
By the way, offers do not have SSE support.

### 5. Building transaction
We can build a transaction with a wrapper or from scratch.

#### 5.1 Build with a wrapper
```python
from stellar_base.builder import Builder
seed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
builder = Builder(secret=seed) # builder = Builder(secret=seed, network='public') for LIVENET
```
How about sending Bob a payment?
```python
bob_address = 'GXXX'
builder.append_payment_op(bob_address, 100, 'XLM')
```
Or if you want to pay him with CNY:
```python
CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'# Just a Stellar address which issues asset CNY
builder.append_payment_op(bob_address, 100, 'CNY', CNY_ISSUER)
```
And maybe you need to carry a message:
```python
builder.add_text_memo('Buy yourself a beer!') # string length <= 28 bytes
```
At last, sign & submit
 ```python
builder.sign()
builder.submit()
```
Done.

Sometimes, we need to deal with multi-signature transactions. Especially when you get a xdr string (or transaction envelope xdr) from a friend or partner, which describes a multi-sig transaction. They may need you to sign on it too.
```python
builder = Builder(secret=seed) # or builder = Builder(secret=secret, network='public') for LIVENET.
builder.import_from_xdr(xdr_string) # the xdr_string come from your friend
builder.sign()
builder.gen_xdr() # generate new xdr string
# or builder.submit() # submit to Stellar network
```

#### 5.2 Build from scratch
```python
from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.operation import Payment
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.memo import TextMemo
from stellar_base.horizon import horizon_testnet, horizon_livenet

alice_seed = 'SAZJ3EDATROKTNNN4WZBZPRC34AN5WR43VEHAFKT5D66UEZTKDNKUHOK'
bob_address = 'GDLP3SP4WP72L4BAJWZUDZ6SAYE4NAWILT5WQDS7RWC4XCUNUQDRB2A4'
CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
amount = '100'

Alice = Keypair.from_seed(alice_seed)
horizon = horizon_testnet() # horizon = horizon_livenet() for LIVENET

asset = Asset('CNY', CNY_ISSUER)
# create op
op = Payment(
    # source=Alice.address().decode(),
    destination=bob_address,
    asset=asset,
    amount=amount
)
# create a memo
msg = TextMemo('Buy yourself a beer !')

# get sequence of Alice
# Python 3
sequence = horizon.account(Alice.address().decode('utf-8')).get('sequence')
# Python 2
# sequence = horizon.account(Alice.address()).get('sequence')

# construct Tx
tx = Transaction(
    source=Alice.address().decode(),
    sequence=sequence,
    # time_bounds = {'minTime': 1531000000, 'maxTime': 1531234600},
    memo=msg,
    fee=100,
    operations=[
        op,
    ],
)

# build envelope
envelope = Te(tx=tx, network_id="TESTNET") # envelope = Te(tx=tx, network_id="PUBLIC"}) for LIVENET
# sign
envelope.sign(Alice)
# submit
xdr = envelope.xdr()
response = horizon.submit(xdr)
```
