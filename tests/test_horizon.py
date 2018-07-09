# encoding: utf-8
from stellar_base.keypair import Keypair
from stellar_base.operation import *
from stellar_base.horizon import Horizon
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te


def make_envelope(network, horizon, address, seed, *args, **kwargs):
    opts = {
        'sequence': horizon.account(address)['sequence'],
        'fee': 100 * len(args)
    }
    for opt, value in kwargs.items():
        opts[opt] = value
    tx = Transaction(address, **opts)
    for count, op in enumerate(args):
        tx.add_operation(op)
    envelope = Te(tx, network_id=network)
    signer = Keypair.from_seed(seed)
    envelope.sign(signer)
    envelope_xdr = envelope.xdr()
    return envelope_xdr


def test_submit(setup, helpers):
    kp = Keypair.random()
    address = kp.address().decode()
    seed = kp.seed()

    helpers.fund_account(setup, address)

    horizon = Horizon(setup.horizon_endpoint_uri)

    envelope_xdr = make_envelope(setup.network, horizon, address, seed,
                                 Payment(
                                     destination=address,
                                     asset=Asset.native(),
                                     amount="0.0001618"))
    response = horizon.submit(envelope_xdr)
    assert 'hash' in response
