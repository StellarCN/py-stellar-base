
[![Build Status](https://travis-ci.org/StellarCN/py-stellar-base.svg)](https://travis-ci.org/StellarCN/py-stellar-base)

# install
    pip install stellar-base.whl


# usage

## Create a Stellar keypair?
```python
    from stellar_base.keypair import Keypair
    kp = Keypair.random()
```    
**or** 
```python
    from __future__ import unicode_literals
    master = u'中文'.encode('utf-8')
    kp = Keypair.deterministic(master)
```    
then we can get key/secret from random:
 
    publickey = kp.address().decode()
    secret = kp.seed().decode()


let's start with my favourite keypair in TESTNET. 

    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
    
    
    
    
##Account

### base info
```python
    from stellar_base.address import Address
    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    address = Address(address=publickey) 
    # address = Address(address=publickey,network='public') for livenet.
    address.get()
```
now you can check address.`balance` ,`sequence` ,`flags` ,`signers`, `manage_data` etc.

### check payments
`address.payments()`will give you latest 10 payments.

there are three params using for query : `limit`, `order` and `cursor`(paging_token). and the default value for them is 10, asc and 0  

so need check payments after a specific cursor?try `address.payments(cursor='4225135422738433',limit=20,order='asc')`

Horizon have SSE support for push data ,if you really want, use like this: `address.payment(sse=True,cursor='4225135422738433')`

###like check payments, you can check `transactions`,`effects`,`offers`,and `operations`.
remember , offers have not SSE support.

    
## Transaction Builder

### create a Transaction Builder at first

    from stellar_base.builder import Builder
    builder = Builder(secret=secret) 
    # builder = Builder(secret=secret, network='public') for LIVENET.
    
### operations
how about sending Bob a tip?

    bob_address = 'GABCDEFGHIJKLMNOPQRSTUVW'
    builder.append_payment_op(bob_address,'100','XLM')
or

    CNY_ISSUER='GCNYISSUERABCDEFGHIJKLMNOPQ'
    builder.append_payment_op(bob_address,'100','CNY',CNY_ISSUER)
    
### then maybe need carry a message

    builder.add_text_memo('Have a nice day!')  # string length <= 28 bytes
    
### sign & submit
    
    builder.sign()
    builder.submit()

Done.

### sign a multi-sig transaction 

  you get a xdr string (or transaction envelope xdr)from a friend or partner ,which describe a multi-sig transaction . 
  They need you sign on it too. 

    builder = Builder(secret=secret) 
    # or builder = Builder(secret=secret, network='public') for LIVENET.
    builder.import_from_xdr(xdr_string)
    builder.sign()
    builder.to_xdr()  # generate new xdr string 
    # or builder.submit() #submit to stellar network



## A payment example without wrapper

    
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
    msg = TextMemo('Have a nice day!')
    
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
    horizon.submit(xdr)

