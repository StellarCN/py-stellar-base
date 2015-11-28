# encoding: utf-8

# from stellar_base.asset import Asset
from .horizon import Horizon
from .keypair import Keypair
from .memo import *
from .network import NETWORKS, Network
from .operation import *
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope as Te

HORIZON_LIVE = "https://horizon.stellar.org"
HORIZON_TEST = "https://horizon-testnet.stellar.org"


class Builder(object):
    """

    """

    def __init__(self, secret, horizon=None, network=None, sequence=None):
        self.key_pair = Keypair.from_seed(secret)
        self.account = self.key_pair.address().decode()

        if network != 'PUBLIC':
            self.network = 'TESTNET'
        else:
            self.network = 'PUBLIC'
        if horizon:
            self.horizon = Horizon(horizon)
        elif self.network == 'PUBLIC':
            self.horizon = Horizon(HORIZON_LIVE)
        else:
            self.horizon = Horizon(HORIZON_TEST)
        if sequence:
            self.sequence = sequence
        else:
            self.sequence = self.get_sequence(self.account)

        self.ops = []
        self.time_bounds = []
        self.memo = NoneMemo()
        self.fee = None
        self.tx = None
        self.te = None

    def append_op(self, operation):
        if operation not in self.ops:
            self.ops.append(operation)

    def append_create_account_op(self, destination, starting_balance, address=None):
        opts = {
            'source': address,
            'destination': destination,
            'starting_balance': int(starting_balance * 10 ** 7)
        }
        op = CreateAccount(opts)
        self.append_op(op)

    def append_trust_op(self, destination, code, limit=None, address=None):
        line = Asset(code, destination)
        if limit:
            limit *= 10 ** 7
        opts = {
            'source': address,
            'asset': line,
            'limit': limit
        }
        op = ChangeTrust(opts)
        self.append_op(op)

    def append_payment_op(self, destination, amount, asset_type='XLM',
                          asset_issuer=None, address=None):
        asset = Asset(code=asset_type, issuer=asset_issuer)
        opts = {
            'source': address,
            'destination': destination,
            'asset': asset,
            'amount': int(amount * 10 ** 7)
        }
        op = Payment(opts)
        self.append_op(op)

    def add_memo(self, memo):
        self.memo = memo

    def add_time_bounds(self, time_bounds):
        self.time_bounds.append(time_bounds)

    def gen_tx(self):
        tx = Transaction(
            self.account,
            opts={
                'sequence': self.sequence,
                'time_Bounds': self.time_bounds,
                'memo': self.memo,
                'fee': self.fee if self.fee else 100 * len(self.ops),
                'operations': self.ops,
            },
        )
        self.tx = tx
        return tx

    def gen_te(self):
        self.gen_tx()
        te = Te(self.tx, opts={'network_id': self.network})
        if self.te:
            te.signatures = self.te.signatures
        self.te = te
        return te

    def gen_xdr(self):
        self.sign()
        return self.te.xdr()

    def import_from_xdr(self, xdr):
        te = Te.from_xdr(xdr)
        te.network_id = Network(NETWORKS[self.network]).network_id()
        self.te = te
        self.tx = te.tx  # with a different source or not .
        self.ops = te.tx.operations
        self.account = te.tx.source
        print(self.account)
        self.sequence = te.tx.sequence - 1
        self.time_bounds = te.tx.time_bounds
        self.memo = te.tx.memo

    def sign(self, secret=None):
        self.gen_te()
        if secret:
            self.te.sign(Keypair.from_seed(secret))
        else:
            self.te.sign(self.key_pair)

    def submit(self):
        try:
            ret = self.horizon.submit(self.gen_xdr())
        except:
            raise Exception('network problem')

        if 'hash' in ret:
            return ret['hash']
        else:
            print(ret)
            raise Exception('sorry' +  ret['status'] + ret['extras']['result_codes']['operations'][0])

    # TODO need catch error
    def get_sequence(self, address):
        return self.horizon.account(address)['sequence']
