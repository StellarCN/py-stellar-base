[![Build Status](https://travis-ci.org/StellarCN/py-stellar-base.svg)](https://travis-ci.org/StellarCN/py-stellar-base)

# Installation
    pip install stellar-base
# Quick Start
## 1. Create a Stellar keypair
There are 2 methods for generating a keypair in py-stellar-base. 
### 1.1 Random generation
```python
    from stellar_base.keypair import Keypair
    kp = Keypair.random()
```    
### 1.2 Deterministic generation
Or we may generate from a particular unicode string:
```python
    from stellar_base.utils import StellarMnemonic
    sm = StellarMnemoic() # default language is 'english'
    m = sm.generate() # or m = '域 监 惜 国 期 碱 珍 继 造 监 剥 电'
    kp = Keypair.deterministic(m,lang='english')
```
Cautions: Please be very careful if you try to use the second method. Because anyone happends to come up with the same string with you would have the access to the generated account. And this coincidence is very likely to happend if you used
a comman phrase/word/numbers. Therefore, random generation is recommanded.

After the keypair generation, we can get publickey/seed from it:
 ```python
    publickey = kp.address().decode()
    seed = kp.seed().decode()
```    
The publickey is also your account address. If someone need to send you a transaction, you should tell him this publickey.
The seed is your secret.For savety,please keep it local and never send it through the Internet.

Whenever we forget/lost your publickey,we can regenerate the keypair from the seed:

```python
    from stellar_base.keypair import Keypair
    kp = Keypair.from_seed(seed)
```   
This is my favourite keypair in TESTNET,let's use them in the following steps.
```python
    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    seed = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
```   
    
## 2.Create Account

After the keypair generation, you have already got the address, but it is not activated until someone transfer 20 lumen into it. 
### 2.1 Testnet
If you want to play in the stellar test network, you can ask our Friendbot to create an account for you as shown below:
```python
    import requests
    publickey=kp.address().decode()
    r=requests.get('https://horizon-testnet.stellar.org/friendbot?addr='+publickey)
```
### 2.2 Livenet
On the other hand, if you would like to create an account in the livenet, you should buy some stellar lumens from an exchange. When you withdraw the lumens into your new account, the exchange will automatically create the account for you.
However,if you want to create an account from another account of your own, you may run the following code:
```python
    from stellar_base.keypair import Keypair
    from stellar_base.asset import Asset
    from stellar_base.operation import Payment
    from stellar_base.operation import CreateAccount
    from stellar_base.transaction import Transaction
    from stellar_base.transaction_envelope import TransactionEnvelope as Te
    from stellar_base.memo import TextMemo
    from stellar_base.horizon import horizon_testnet, horizon_livenet
    
    oldAccountSeed="SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
    newAccountAddress="XXX"
    amount = '25' # Any amount higher than 20
    kp=Keypair.from_seed(oldAccountSeed)
    horizon = horizon_livenet()
    asset = Asset("XLM")
    # create op 
    op = CreateAccount({
    'destination': newAccountAddress,
    'starting_balance': amount
    })
    # create a memo
    msg = TextMemo('')
    # get sequence of new account address
    sequence = horizon.account(kp.address()).get('sequence')
    # construct the transaction
    tx = Transaction(
        source=kp.address().decode(),
        opts={
            'sequence': sequence,
            # 'timeBounds': [],
            'memo': msg,
            #'fee': 100,
            'operations': [
                op,
            ],
         },
    )
    # build envelope
    envelope = Te(tx=tx, opts={"network_id": "PUBLIC"})
    # sign 
    envelope.sign(kp)
    # submit
    xdr = envelope.xdr()
    response=horizon.submit(xdr)
    
```
Then, you can check the status of this operation with the response.

## 3. Check account
### 3.1 Basic info
After creating the account, we may check the basic information of the account.

```python
    from stellar_base.address import Address
    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    address = Address(address=publickey) # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
```
Now you can check address.`balance` ,`sequence` ,`flags` ,`signers`, `data` etc.
```python
    print "balances: " + address.balances
    print "sequence: " + address.sequence
    print "flags: " + address.flags
    print "signers: " + address.signers
    print "data: " + address.data
```

### 3.2 Check payments
We can check the most recent payments by:
`address.payments()`
We can use three params to customize query : `limit`, `order` and `cursor`(paging_token), and the default value for them are respectively `limit=10,order="asc",cursor=0`.

So if you need to check payments after a specific cursor, try:
`address.payments(cursor='4225135422738433',limit=20,order='asc')`

Horizon have SSE support for push data ,if you really want, use like this: `address.payment(sse=True,cursor='4225135422738433')`

### 3.3 Check others
Just like payments, we can check `transactions`,`effects`,`offers`,and `operations` by:
```python
     address.transactions()
     address.effects()
     address.offers()
     address.operations()
```
By the way, offers have not SSE support.

    
## 4. Building transaction
We can build a transaction with a wrapper or from scratch.

### 4.1 Build with a wrapper
```python
    from stellar_base.builder import Builder
    seed="SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
    builder = Builder(secret=seed) # builder = Builder(secret=seed, network='public') for LIVENET
```
How about sending Bob a payment?
```python
    bob_address = 'XXX'
    builder.append_payment_op(bob_address,'100','XLM')
```  
Or if you want to pay him with CNY:
```python
    CNY_ISSUER='ABC'
    builder.append_payment_op(bob_address,'100','CNY',CNY_ISSUER)
```    
Then maybe need to carry a message:
```python
    builder.add_text_memo('Buy yourself a beer!')  # string length <= 28 bytes
```    
At last, sign & submit
 ```python   
    builder.sign()
    builder.submit()
```
Done.

Sometimes, we need to deal with multi-signature transaction. Especially when you get a xdr string (or transaction envelope xdr)from a friend or partner ,which describe a multi-sig transaction.They may need you to sign on it too. 
```python
    builder = Builder(secret=seed) # or builder = Builder(secret=secret, network='public') for LIVENET.
    builder.import_from_xdr(xdr_string) # the xdr_string come from your friend
    builder.sign()
    builder.to_xdr()  # generate new xdr string 
    # or builder.submit() #submit to stellar network
```


### 4.2 Build from scratch
```python   
    from stellar_base.keypair import Keypair
    from stellar_base.asset import Asset
    from stellar_base.operation import Payment
    from stellar_base.transaction import Transaction
    from stellar_base.transaction_envelope import TransactionEnvelope as Te
    from stellar_base.memo import TextMemo
    from stellar_base.horizon import horizon_testnet, horizon_pubic
    
    alice_seed = 'SAZJ3EDATROKTNNN4WZBZPRC34AN5WR43VEHAFKT5D66UEZTKDNKUHOK'
    bob_address = 'GDLP3SP4WP72L4BAJWZUDZ6SAYE4NAWILT5WQDS7RWC4XCUNUQDRB2A4'
    CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    amount = '100'
    
    Alice = Keypair.from_seed(alice_seed)
    horizon = horizon_testnet()
    
    asset = Asset('CNY', CNY_ISSUER) 
    # create op 
    op = Payment({
        # 'source' : Alice.address().decode(),
        'destination': bob_address,
        'asset': asset,
        'amount': amount
    })
    # create a memo
    msg = TextMemo('Buy yourself a beer !')
    
    # get sequence of Alice
    sequence = horizon.account(Alice.address()).get('sequence') 
    
    # construct Tx
    tx = Transaction(
        source=Alice.address().decode(),
        opts={
            'sequence': sequence,
            # 'timeBounds': [],
            'memo': msg,
            # 'fee': 100,
            'operations': [
                op,
            ],
        },
    )
    
    
    # build envelope
    envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
    # sign 
    envelope.sign(Alice)
    # submit
    xdr = envelope.xdr()
    response=horizon.submit(xdr)
```