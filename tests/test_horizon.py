# encoding: utf-8
import requests
import json
from stellar_base.keypair import Keypair
from stellar_base.memo import *
from stellar_base.operation import *
from stellar_base.builder import HORIZON_TEST
from stellar_base.horizon import Horizon

horizon = Horizon()


class TestMethods:
    def __init__(self):
        kp = Keypair.random()
        self.fee = 100
        self.address = kp.address().decode('ascii')
        self.seed = kp.seed().decode('ascii') or None

        fund(self.address)

    def make_envelope(self, *args, **kwargs):
        from stellar_base.transaction import Transaction
        from stellar_base.keypair import Keypair
        from stellar_base.transaction_envelope import TransactionEnvelope as Te
        opts = {
            'sequence': horizon.account(self.address)['sequence'],
            'fee': self.fee * len(args)
        }
        for opt, value in kwargs.items():
            opts[opt] = value
        tx = Transaction(source=self.address, opts=opts)
        for count, op in enumerate(args):
            tx.add_operation(operation=op)
        envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
        signer = Keypair.from_seed(seed=self.seed)
        envelope.sign(keypair=signer)
        envelope_xdr = envelope.xdr()
        print(envelope_xdr)
        return envelope_xdr

    def test_submit(self):
        envelope_xdr = self.make_envelope(Payment({
            'destination': self.address,
            'asset': Asset.native(),
            'amount': "0.0001618"
        }))
        response = horizon.submit(envelope_xdr)
        assert 'hash' in response


def fund(address):
    for attempt in range(3):
        r = requests.get(HORIZON_TEST + '/friendbot?addr=' +
                         address)  # Get 10000 lumens
        t = r.text
        try:
            assert 'hash' in json.loads(
                t) or 'op_already_exists' in json.loads(t)
            return True
        except AssertionError:
            pass
    raise Exception("fund failed")
