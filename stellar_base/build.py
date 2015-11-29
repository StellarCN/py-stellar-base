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

    def append_create_account_op(self, destination, starting_balance, source=None):
        opts = {
            'source': source,
            'destination': destination,
            'starting_balance': int(starting_balance * 10 ** 7)
        }
        op = CreateAccount(opts)
        self.append_op(op)

    def append_trust_op(self, destination, code, limit=None, source=None):
        line = Asset(code, destination)
        if limit:
            limit = int(limit * 10 ** 7)
        opts = {
            'source': source,
            'asset': line,
            'limit': limit
        }
        op = ChangeTrust(opts)
        self.append_op(op)

    def append_payment_op(self, destination, amount, asset_type='XLM',
                          asset_issuer=None, source=None):
        asset = Asset(code=asset_type, issuer=asset_issuer)
        opts = {
            'source': source,
            'destination': destination,
            'asset': asset,
            'amount': int(amount * 10 ** 7)
        }
        op = Payment(opts)
        self.append_op(op)

    def append_path_payment_op(self, destination, send_code, send_issuer, send_max,
                               dest_code, dest_issuer, dest_amount, path, source=None):
        """

        :param path: a list of asset tuple which contains code and issuer, [(code,issuer),(code,issuer)]
        """
        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for p in path:
            assets.append(Asset(p[0],p[1]))

        opts = {
            'source': source,
            'destination': destination,
            'send_asset': send_asset,
            'send_max': int(send_max * 10 ** 7),
            'dest_asset': dest_asset,
            'dest_amount': int(dest_amount * 10 ** 7),
            'path': assets
        }
        op = Payment(opts)
        self.append_op(op)

    def append_allow_trust_op(self, trustor, asset_code, authorize, source=None):
        opts = {
            'source': source,
            'trustor': trustor,
            'asset_code': asset_code,
            'authorize': authorize
        }
        op = AllowTrust(opts)
        self.append_op(op)

    def append_set_options_op(self, inflation_dest=None,clear_flags=None, set_flags=None,
                              master_weight=None, low_threshold=None, med_threshold=None,
                              high_threshold=None, home_domain=None, signer_address=None,
                              signer_weight=None, source=None,
                              ):
        opts = {
            'source': source,
            'inflation_dest': inflation_dest,
            'clear_flags': clear_flags,
            'set_flags': set_flags,
            'master_weight': master_weight,
            'low_threshold': low_threshold,
            'med_threshold': med_threshold,
            'high_threshold': high_threshold,
            'home_domain': bytearray(home_domain, encoding='utf-8'),
            'signer_address': signer_address,
            'signer_weight': signer_weight
        }
        op = SetOptions(opts)
        self.append_op(op)

    def append_manage_offer_op(self, selling_code, selling_issuer,
                               buying_code, buying_issuer,
                               amount, price, offer_id=0, source=None):
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)

        opts = {
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': amount,
            'price': price,
            'offer_id': offer_id,

        }
        op = ManageOffer(opts)
        self.append_op(op)

    def append_create_passive_offer_op(self, selling_code, selling_issuer,
                                       buying_code, buying_issuer,
                                       amount, price, source=None):
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)

        opts = {
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': amount,
            'price': price,
        }
        op = CreatePassiveOffer(opts)
        self.append_op(op)

    def append_account_merge_op(self, destination, source=None):

        opts = {
            'source': source,
            'destination': destination
        }
        op = AccountMerge(opts)
        self.append_op(op)

    def append_inflation_op(self,source=None):
        opts = {'source': source}
        op = Inflation(opts)
        self.append_op(op)

    def add_memo(self, memo):
        self.memo = memo

    def add_text_memo(self, memo_text):
        memo_text = TextMemo(memo_text)
        self.add_memo(memo_text)

    def add_id_memo(self, memo_id):
        memo_id = IdMemo(memo_id)
        self.add_memo(memo_id)

    def add_hash_memo(self, memo_hash):
        memo_hash = HashMemo(memo_hash)
        self.add_memo(memo_hash)

    def add_ret_hash_memo(self, memo_return):
        memo_return = RetHashMemo(memo_return)
        self.add_memo(memo_return)

    def add_time_bounds(self, time_bounds):
        self.time_bounds.append(time_bounds)

    def gen_tx(self):
        if not self.sequence:
            raise Exception('have no sequence,maybe not funded?')
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
            raise Exception('sorry' + ret['status'] + ret['extras']['result_codes']['operations'][0])

    def get_sequence(self, address):
        try:
            account = self.horizon.account(address)
        except:
            raise Exception('network problem')

        return account.get('sequence')
