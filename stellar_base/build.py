# encoding: utf-8

from stellar_base.operation import *
from stellar_base.asset import Asset
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Envelope
from stellar_base.keypair import Keypair
from stellar_base.horizon import Horizon


def create_account_op_build(destination,starting_balance):
    opts = {'destination':destination, 'starting_balance':starting_balance}
    return CreateAccount(opts)


def pay_op_build(destination, amount, asset_type='XLM', asset_issuer=None, address=None):
    asset = Asset(code=asset_type, issuer=asset_issuer)
    opts = {'source': address, 'destination': destination, 'asset': asset, 'amount': amount}
    return Payment(opts)


def tx_build(address, operation, seq=None, time_bounds=None, memo=None, fee=None):
    if seq is None:
        seq = get_sequence(address)
    # TODO memo to Memo()
    opts = dict(seqNum=seq, timeBounds=time_bounds, memo=memo, fee=fee)
    tx = Transaction(address, opts)
    tx.add_operation(operation)
    return tx


def te_xdr_build(tx, secret):
    envelope = Envelope(tx)
    signer = Keypair.from_seed(secret)
    envelope.sign(signer)
    re = envelope.xdr()
    return re


def get_sequence(address):
    h = Horizon()
    account = h.account(address)
    try:
        return account['sequence']
    except:
        return False
