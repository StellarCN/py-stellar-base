# coding: utf-8

# from stellar_base.asset import Asset
from .horizon import HORIZON_LIVE, HORIZON_TEST
from .horizon import Horizon
from .keypair import Keypair
from .memo import *
from .network import NETWORKS, Network
from .operation import *
from .transaction import Transaction
from .transaction_envelope import TransactionEnvelope as Te
from .utils import SignatureExistError
from .federation import *


class Builder(object):
    """ build transaction and submit to horizon.

    """

    def __init__(self, secret=None, address=None, horizon=None, network=None, sequence=None):
        if secret:
            self.key_pair = Keypair.from_seed(secret)
            self.address = self.key_pair.address().decode()
        else:
            self.key_pair = None
            self.address = None

        if address is None and secret is None:
            raise Exception('No Stellar address afforded.')
        if address is not None and secret is None:
            self.address = address
            self.key_pair = None

        if network is None or network.upper() != 'PUBLIC':
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
        elif self.address:
            self.sequence = self.get_sequence()
        else:
            self.sequence = None

        self.ops = []
        self.time_bounds = []
        self.memo = NoneMemo()
        self.fee = None
        self.tx = None
        self.te = None

    def append_op(self, operation):
        if operation not in self.ops:
            self.ops.append(operation)
        return self

    def append_create_account_op(self, destination, starting_balance, source=None):
        opts = {
            'source': source,
            'destination': destination,
            'starting_balance': str(starting_balance)
        }
        op = CreateAccount(opts)
        return self.append_op(op)

    def append_trust_op(self, destination, code, limit=None, source=None):
        line = Asset(code, destination)
        if limit is not None:
            limit = str(limit)
        opts = {
            'source': source,
            'asset': line,
            'limit': limit
        }
        op = ChangeTrust(opts)
        return self.append_op(op)

    def append_payment_op(self, destination, amount, asset_type='XLM',
                          asset_issuer=None, source=None):
        asset = Asset(code=asset_type, issuer=asset_issuer)
        opts = {
            'source': source,
            'destination': destination,
            'asset': asset,
            'amount': str(amount)
        }
        op = Payment(opts)
        return self.append_op(op)

    def append_path_payment_op(self, destination, send_code, send_issuer, send_max,
                               dest_code, dest_issuer, dest_amount, path, source=None):
        # path: a list of asset tuple which contains code and issuer, [(code,issuer),(code,issuer)]
        # for native asset you can delivery ('xlm','')
        send_asset = Asset(send_code, send_issuer)
        dest_asset = Asset(dest_code, dest_issuer)

        assets = []
        for p in path:
            assets.append(Asset(p[0], p[1]))

        opts = {
            'source': source,
            'destination': destination,
            'send_asset': send_asset,
            'send_max': str(send_max),
            'dest_asset': dest_asset,
            'dest_amount': str(dest_amount),
            'path': assets
        }
        op = PathPayment(opts)
        return self.append_op(op)

    def append_allow_trust_op(self, trustor, asset_code, authorize, source=None):
        opts = {
            'source': source,
            'trustor': trustor,
            'asset_code': asset_code,
            'authorize': authorize
        }
        op = AllowTrust(opts)
        return self.append_op(op)

    def append_set_options_op(self, inflation_dest=None, clear_flags=None, set_flags=None,
                              master_weight=None, low_threshold=None, med_threshold=None,
                              high_threshold=None, home_domain=None, signer_address=None,
                              signer_type=None, signer_weight=None, source=None,
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
            'home_domain': bytearray(home_domain, encoding='utf-8') if home_domain else None,
            'signer_address': signer_address,
            'signer_type': signer_type,
            'signer_weight': signer_weight
        }
        op = SetOptions(opts)
        return self.append_op(op)

    def append_hashx_signer(self, hashx, signer_weight, source=None):
        return self.append_set_options_op(signer_address=hashx, signer_type='hashX', signer_weight=signer_weight,
                                          source=source)

    def append_pre_auth_tx_signer(self, pre_auth_tx, signer_weight, source=None):
        return self.append_set_options_op(signer_address=pre_auth_tx, signer_type='preAuthTx',
                                          signer_weight=signer_weight, source=source)

    def append_manage_offer_op(self, selling_code, selling_issuer,
                               buying_code, buying_issuer,
                               amount, price, offer_id=0, source=None):
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)

        opts = {
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': str(amount),
            'price': price,
            'offer_id': offer_id,

        }
        op = ManageOffer(opts)
        return self.append_op(op)

    def append_create_passive_offer_op(self, selling_code, selling_issuer,
                                       buying_code, buying_issuer,
                                       amount, price, source=None):
        selling = Asset(selling_code, selling_issuer)
        buying = Asset(buying_code, buying_issuer)

        opts = {
            'source': source,
            'selling': selling,
            'buying': buying,
            'amount': str(amount),
            'price': price,
        }
        op = CreatePassiveOffer(opts)
        return self.append_op(op)

    def append_account_merge_op(self, destination, source=None):

        opts = {
            'source': source,
            'destination': destination
        }
        op = AccountMerge(opts)
        return self.append_op(op)

    def append_inflation_op(self, source=None):
        opts = {'source': source}
        op = Inflation(opts)
        return self.append_op(op)

    def append_manage_data_op(self, data_name, data_value, source=None):
        opts = {
            'source': source,
            'data_name': data_name,
            'data_value': data_value
        }
        op = ManageData(opts)
        return self.append_op(op)

    def add_memo(self, memo):
        self.memo = memo
        return self

    def add_text_memo(self, memo_text):
        memo_text = TextMemo(memo_text)
        return self.add_memo(memo_text)

    def add_id_memo(self, memo_id):
        memo_id = IdMemo(memo_id)
        return self.add_memo(memo_id)

    def add_hash_memo(self, memo_hash):
        memo_hash = HashMemo(memo_hash)
        return self.add_memo(memo_hash)

    def add_ret_hash_memo(self, memo_return):
        memo_return = RetHashMemo(memo_return)
        return self.add_memo(memo_return)

    def add_time_bounds(self, time_bounds):
        return self.time_bounds.append(time_bounds)

    def federation_payment(self, fed_address, amount, asset_type='XLM',
                           asset_issuer=None, source=None):
        fed_info = federation(fed_address, 'name')
        if not fed_info:
            raise FederationError('can not get valid federation response. ')
        self.append_payment_op(fed_info['account_id'], amount, asset_type,
                               asset_issuer, source)
        memo_type = fed_info.get('memo_type')
        if memo_type is not None and memo_type in ('text', 'id', 'hash'):
            getattr(self, 'add_' + memo_type + '_memo')(fed_info['memo'])

    def gen_tx(self):
        if not self.address:
            raise Exception('Transaction does not have any source address ')
        if not self.sequence:
            raise Exception('have no sequence, maybe not funded?')
        tx = Transaction(
            self.address,
            opts={
                'sequence': self.sequence,
                'timeBounds': self.time_bounds,
                'memo': self.memo,
                'fee': self.fee if self.fee else 100 * len(self.ops),
                'operations': self.ops,
            },
        )
        self.tx = tx
        return tx

    def gen_te(self):
        if self.tx is None:
            self.gen_tx()
        te = Te(self.tx, opts={'network_id': self.network})
        if self.te:
            te.signatures = self.te.signatures
        self.te = te
        return te

    def gen_xdr(self):
        if self.tx is None:
            self.gen_te()
        return self.te.xdr()

    def gen_compliance_xdr(self):
        sequence = self.sequence
        self.sequence = '-1'  # sequence number shoule be '0' here. so the pass one is '-1'
        tx_xdr = self.gen_tx().xdr()
        self.sequence = sequence
        return tx_xdr

    def import_from_xdr(self, xdr):
        te = Te.from_xdr(xdr)
        te.network_id = Network(NETWORKS[self.network]).network_id()
        self.te = te
        self.tx = te.tx  # with a different source or not .
        self.ops = te.tx.operations
        self.address = te.tx.source
        self.sequence = te.tx.sequence - 1
        self.time_bounds = te.tx.time_bounds
        self.memo = te.tx.memo

    def sign(self, secret=None):
        key_pair = self.key_pair if not secret else Keypair.from_seed(secret)

        self.gen_te()

        try:
            self.te.sign(key_pair)
        except SignatureExistError:
            raise

    def sign_preimage(self, preimage):
        ''' preimage must be a unicode string
        '''
        if self.te is None:
            self.gen_te()
        try:
            self.te.sign_hashX(preimage)
        except SignatureExistError:
            raise

    def submit(self):
        try:
            return self.horizon.submit(self.gen_xdr())
        except Exception as e:
            raise e
            # raise Exception('network problem')

    def next_builder(self):
        sequence = str(int(self.sequence) + 1)
        next_builder = Builder(horizon=self.horizon.horizon, network=self.network, sequence=sequence)
        next_builder.address = self.address
        next_builder.key_pair = self.key_pair
        return next_builder

    def get_sequence(self):
        if not self.address:
            raise Exception('no address provided')
        try:
            address = self.horizon.account(self.address)
        except:
            raise Exception('network problem')

        return address.get('sequence')
