# encoding: utf-8
import os
import time

import mock
import pytest

from stellar_base import memo
from stellar_base.builder import Builder
from stellar_base.exceptions import InvalidSep10ChallengeError, NoStellarSecretOrAddressError, FederationError
from stellar_base.horizon import horizon_testnet, horizon_livenet, Horizon
from stellar_base.keypair import Keypair
from stellar_base.operation import ManageData


@pytest.fixture(scope='module')
def test_data(setup, helpers):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    cold = Keypair.random()
    cold_secret = cold.seed()
    cold_account = cold.address().decode()
    helpers.fund_account(setup, cold_account)

    return Struct(cold_secret=cold_secret, cold_account=cold_account)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def json(self):
            import json
            return json.loads(self.text)

    if args[0] == 'https://www.fed-domain.com/federation' and \
            kwargs['params'] == {'q': 'fed*fed-domain.com', 'type': 'name'}:
        return MockResponse('{"account_id": "GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES",  \
                              "memo_type": "text", "memo": "hello memo", \
                              "stellar_address": "1CqDFDxR9Tv696j86PwtyxhA5p9ev1EviJ*naobtc.com"}', \
                            200)
    if args[0] == 'https://fed-domain.com/.well-known/stellar.toml':
        return MockResponse('FEDERATION_SERVER="https://www.fed-domain.com/federation"\n  \
                             [[CURRENCIES]]  \n   code="BTC"     \n\
                             issuer="GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"', \
                            200)
    return MockResponse({}, 404)


class TestBuilder(object):
    def test_builder_append_ops(self):
        alice_secret = 'SDIMY25XL2TDSUZNM42Y2WLA2E2R52EV3GR6MXCPVTBSWJLN6MLX6JZV'
        bob_account = 'GBZ5VJD6VMQMRDSMCCZAF23K5VIGBHXJQQYLLYQOEIZB4AUJNMFN5R3U'

        builder = Builder(secret=alice_secret, sequence=938635037769728, fee=100)
        builder. \
            append_create_account_op(destination=bob_account, starting_balance='10'). \
            append_change_trust_op(asset_code='BEER', asset_issuer=bob_account, limit='1000'). \
            append_payment_op(destination=bob_account, asset_code='XLM', amount='100'). \
            append_path_payment_op(destination=bob_account, send_code='BEER',
                                   send_issuer=bob_account,
                                   send_max='100', dest_code='XLM', dest_issuer=None, dest_amount='100',
                                   path=[('HELLO', bob_account)]). \
            append_allow_trust_op(trustor=bob_account, asset_code='MOE', authorize=True). \
            append_set_options_op(set_flags=7, home_domain='stellar.org'). \
            append_hashx_signer(
            hashx=b"\xe7\xd40j:>pH\xa0\x11\x90(q\x88\xa0IV\xf6\xa9\xc90\x15H&\xeb\xcd\x03\t\x93\x1f'8",
            signer_weight=1). \
            append_pre_auth_tx_signer(
            pre_auth_tx=b"\x95\xe5\xbb\x95\x15\xd9\x9f\x82\x9d\xf9\x93\xc3'\x8e\xeb\xf1\nj!\xda\xa4\xa1\xe4\xf2<6cG}\x17\x97\xfe",
            signer_weight=1). \
            append_manage_sell_offer_op(selling_code='XLM', selling_issuer=None, buying_code='BEER',
                                        buying_issuer=bob_account, amount='1', price='10', offer_id=0). \
            append_manage_buy_offer_op(selling_code='XLM', selling_issuer=None, buying_code='BEER',
                                       buying_issuer=bob_account, amount='1', price='10', offer_id=0). \
            append_create_passive_sell_offer_op(selling_code='XLM', selling_issuer=None, buying_code='BEER',
                                                buying_issuer=bob_account, amount='1', price={'n': 10, 'd': 1}). \
            append_account_merge_op(destination=bob_account). \
            append_inflation_op(). \
            append_manage_data_op(data_name='hello', data_value='world'). \
            append_bump_sequence_op(bump_to=938635037769749). \
            add_text_memo("hello, stellar"). \
            add_time_bounds({'minTime': 1534392138, 'maxTime': 1534392238})
        assert builder.hash_hex() == 'f646a891ed9ecde6f98bf7fb1afcb52acbc73aabd08f9390c61fdfc8f426815f'
        builder.sign()
        assert builder.gen_xdr().decode() == 'AAAAAP4sA2cn9oggk4cfzPLqZVfpSEhmindW2FQofl5b0SjDAAAF3AADVa8AAAABAAAAAQAAAABbdPdKAAAAAFt0964AAAABAAAADmhlbGxvLCBzdGVsbGFyAAAAAAAPAAAAAAAAAAAAAAAAc9qkfqsgyI5MELIC62rtUGCe6YQwteIOIjIeAolrCt4AAAAABfXhAAAAAAAAAAAGAAAAAUJFRVIAAAAAc9qkfqsgyI5MELIC62rtUGCe6YQwteIOIjIeAolrCt4AAAACVAvkAAAAAAAAAAABAAAAAHPapH6rIMiOTBCyAutq7VBgnumEMLXiDiIyHgKJawreAAAAAAAAAAA7msoAAAAAAAAAAAIAAAABQkVFUgAAAABz2qR+qyDIjkwQsgLrau1QYJ7phDC14g4iMh4CiWsK3gAAAAA7msoAAAAAAHPapH6rIMiOTBCyAutq7VBgnumEMLXiDiIyHgKJawreAAAAAAAAAAA7msoAAAAAAQAAAAJIRUxMTwAAAAAAAAAAAAAAc9qkfqsgyI5MELIC62rtUGCe6YQwteIOIjIeAolrCt4AAAAAAAAABwAAAABz2qR+qyDIjkwQsgLrau1QYJ7phDC14g4iMh4CiWsK3gAAAAFNT0UAAAAAAQAAAAAAAAAFAAAAAAAAAAAAAAABAAAABwAAAAAAAAAAAAAAAAAAAAAAAAABAAAAC3N0ZWxsYXIub3JnAAAAAAAAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAALn1DBqOj5wSKARkChxiKBJVvapyTAVSCbrzQMJkx8nOAAAAAEAAAAAAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAGV5buVFdmfgp35k8MnjuvxCmoh2qSh5PI8NmNHfReX/gAAAAEAAAAAAAAAAwAAAAAAAAABQkVFUgAAAABz2qR+qyDIjkwQsgLrau1QYJ7phDC14g4iMh4CiWsK3gAAAAAAmJaAAAAACgAAAAEAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAFCRUVSAAAAAHPapH6rIMiOTBCyAutq7VBgnumEMLXiDiIyHgKJawreAAAAAACYloAAAAAKAAAAAQAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAUJFRVIAAAAAc9qkfqsgyI5MELIC62rtUGCe6YQwteIOIjIeAolrCt4AAAAAAJiWgAAAAAoAAAABAAAAAAAAAAgAAAAAc9qkfqsgyI5MELIC62rtUGCe6YQwteIOIjIeAolrCt4AAAAAAAAACQAAAAAAAAAKAAAABWhlbGxvAAAAAAAAAQAAAAV3b3JsZAAAAAAAAAAAAAALAANVrwAAABUAAAAAAAAAAVvRKMMAAABAM1rhFzh2mbT283+lJsqeckCxnO9vC0m8ADTbyUbFXNJNAfSpI23W/kS69wgeq8qp/1knDpkn72b6e6Eac9coCw=='

    def test_no_stellar_secret_or_address_error_raise(self):
        with pytest.raises(NoStellarSecretOrAddressError):
            Builder()

    def test_custom_fee(self, test_data):
        builder = Builder(test_data.cold_secret, sequence=1, fee=150)
        assert builder.fee == 150

    def test_add_memo(self, test_data):
        builder = Builder(test_data.cold_secret, sequence=1, fee=100)

        builder.add_text_memo("hello")
        assert builder.memo == memo.TextMemo("hello")

        builder.add_id_memo(123123)
        assert builder.memo == memo.IdMemo(123123)

        hash = b"\x95\xe5\xbb\x95\x15\xd9\x9f\x82\x9d\xf9\x93\xc3'\x8e\xeb\xf1\nj!\xda\xa4\xa1\xe4\xf2<6cG}\x17\x97\xfe"
        builder.add_hash_memo(hash)
        assert builder.memo == memo.HashMemo(hash)
        builder.add_ret_hash_memo(hash)
        assert builder.memo == memo.RetHashMemo(hash)

    def test_builder_xdr(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, horizon_uri=setup.horizon_endpoint_uri, network=setup.network) \
            .append_manage_data_op("hello", "world")
        builder.sign()
        response = builder.submit()
        assert response.get('hash') == builder.hash_hex()

    def test_import_from_xdr(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, sequence=1, horizon_uri=setup.horizon_endpoint_uri,
                          network=setup.network) \
            .append_manage_data_op("hello", "world") \
            .add_time_bounds({'minTime': 1534392138, 'maxTime': 1534392238})
        builder.sign()
        old_xdr = builder.gen_xdr()
        old_hash = builder.hash()
        new_hash = Builder(secret=test_data.cold_secret).import_from_xdr(old_xdr).hash()
        assert new_hash == old_hash

    def test_import_from_xdr_custom_network(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, sequence=1, horizon_uri=setup.horizon_endpoint_uri,
                          network='CUSTOM_NETWORK') \
            .append_manage_data_op("hello", "world")
        builder.sign()
        old_xdr = builder.gen_xdr()
        old_hash = builder.hash()
        new_hash = Builder(secret=test_data.cold_secret, network='CUSTOM_NETWORK').import_from_xdr(old_xdr).hash()
        assert new_hash == old_hash

    def test_next_builder(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, sequence=1, horizon_uri=setup.horizon_endpoint_uri,
                          network=setup.network) \
            .append_manage_data_op("hello", "world")
        builder.sign()
        next_builder = builder.next_builder()
        assert next_builder.keypair == builder.keypair
        assert next_builder.horizon.horizon_uri == builder.horizon.horizon_uri
        assert next_builder.address == builder.address
        assert next_builder.network == builder.network
        assert next_builder.fee == builder.fee
        assert next_builder.sequence == builder.sequence + 1

    def test_gen_compliance_xdr(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, sequence=100, horizon_uri=setup.horizon_endpoint_uri,
                          network=setup.network) \
            .append_manage_data_op("hello", "world")
        xdr = builder.gen_compliance_xdr()
        builder_seq_zero = Builder(secret=test_data.cold_secret, sequence=-1, horizon_uri=setup.horizon_endpoint_uri,
                                   network=setup.network) \
            .append_manage_data_op("hello", "world")
        assert xdr == builder_seq_zero.gen_tx().xdr()
        assert builder.sequence == 100

    @mock.patch(
        'stellar_base.federation.requests.get',
        side_effect=mocked_requests_get)
    def test_federation_payment(self, setup):
        builder_fed = Builder(address='GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES', sequence=100)
        builder_fed.federation_payment(fed_address="fed*fed-domain.com", amount="100.5", asset_code="XLM")
        builder = Builder(address='GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES',
                          sequence=100).add_text_memo("hello memo").append_payment_op(
            destination='GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES',
            asset_code='XLM', amount="100.5")
        assert builder_fed.hash() == builder.hash()

    @mock.patch(
        'stellar_base.federation.requests.get',
        side_effect=mocked_requests_get)
    def test_federation_payment_not_found_raise(self, setup):
        builder_fed = Builder(address='GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES', sequence=100)
        with pytest.raises(FederationError,
                           match='Cannot determine Stellar Address to Account ID translation via Federation server.'):
            builder_fed.federation_payment(fed_address="bad*fed-domain.com", amount="100.5", asset_code="XLM")

    def test_network_and_horizon(self, setup, test_data):
        builder = Builder(secret=test_data.cold_secret, sequence=100, network='MOE')
        assert builder.network == 'MOE'
        assert builder.horizon.horizon_uri == horizon_testnet().horizon_uri

        builder = Builder(secret=test_data.cold_secret, sequence=100, network='testnet')
        assert builder.network == 'TESTNET'
        assert builder.horizon.horizon_uri == horizon_testnet().horizon_uri

        builder = Builder(secret=test_data.cold_secret, sequence=100, network='public')
        assert builder.network == 'PUBLIC'
        assert builder.horizon.horizon_uri == horizon_livenet().horizon_uri

        builder = Builder(secret=test_data.cold_secret, sequence=100, network='public',
                          horizon_uri=setup.horizon_endpoint_uri)
        assert builder.network == 'PUBLIC'
        assert builder.horizon.horizon_uri == Horizon(horizon_uri=setup.horizon_endpoint_uri).horizon_uri

    def test_challenge_tx(self):
        server_kp = Keypair.random()
        client_account_id = "GBDIT5GUJ7R5BXO3GJHFXJ6AZ5UQK6MNOIDMPQUSMXLIHTUNR2Q5CFNF"
        timeout = 600
        network = 'TESTNET'
        archor_name = "SDF"

        tx = Builder.challenge_tx(server_secret=server_kp.seed().decode(),
                                  client_account_id=client_account_id,
                                  archor_name=archor_name,
                                  network=network,
                                  timeout=timeout)
        assert len(tx.ops) == 1
        op = tx.ops[0]
        assert isinstance(op, ManageData)
        assert op.data_name == "SDF auth"
        assert len(op.data_value) == 64
        assert op.source == client_account_id

        now = int(time.time())
        assert now - 3 < tx.time_bounds['minTime'] < now + 3
        assert tx.time_bounds['maxTime'] - tx.time_bounds['minTime'] == timeout
        assert tx.keypair == server_kp
        assert tx.sequence == -1

    def test_verify_challenge_tx(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'Public Global Stellar Network ; September 2015'
        archor_name = "SDF"

        challenge = Builder.challenge_tx(server_secret=server_kp.seed().decode(),
                                         client_account_id=client_kp.address().decode(),
                                         archor_name=archor_name,
                                         network=network,
                                         timeout=timeout)
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='Public Global Stellar Network ; September 2015',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                    'Public Global Stellar Network ; September 2015')

    def test_verify_challenge_tx_sequence_not_zero(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()

        challenge = Builder(server_kp.seed().decode(), sequence=10086, fee=100)
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='Public Global Stellar Network ; September 2015',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError, match="The transaction sequence number should be zero."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'Public Global Stellar Network ; September 2015')

    def test_verify_challenge_tx_source_is_different_to_server_account_id(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network = 'TESTNET'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="Transaction source account is not equal to server's account."):
            Builder.verify_challenge_tx(challenge_tx, Keypair.random().address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_donot_contain_any_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)

        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError, match="Transaction requires a single ManageData operation."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_donot_contain_managedata_operation(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        challenge.append_bump_sequence_op(12, source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)

        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError, match="Operation type should be ManageData."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_operation_does_not_contain_the_source_account(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce)
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)

        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError, match="Operation should have a source account."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_operation_value_is_not_a_64_bytes_base64_string(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        nonce = os.urandom(32)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)

        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="Operation value should be a 64 bytes base64 random string."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_server(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)

        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="transaction not signed by server: {}".format(server_kp.address().decode())):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_transaction_is_not_signed_by_the_client(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': now + timeout})
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="transaction not signed by client: {}".format(client_kp.address().decode())):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_dont_contains_timebound(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="Transaction requires timebounds."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_contains_infinite_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now, 'maxTime': 0})
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="Transaction requires non-infinite timebounds."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')

    def test_verify_challenge_tx_not_within_range_of_the_specified_timebounds(self):
        server_kp = Keypair.random()
        client_kp = Keypair.random()
        timeout = 600
        network = 'TESTNET'
        archor_name = 'sdf'

        challenge = Builder(server_kp.seed().decode(), network=network, sequence=-1, fee=100)
        now = int(time.time())
        challenge.add_time_bounds({'minTime': now - 100, 'maxTime': now - 20})
        nonce = os.urandom(64)
        challenge.append_manage_data_op(data_name='{} auth'.format(archor_name), data_value=nonce,
                                        source=client_kp.address().decode())
        challenge.sign()
        challenge_tx_server_signed = challenge.gen_xdr()

        transaction = Builder(client_kp.seed().decode(), network='TESTNET',
                              sequence=0, fee=100)
        transaction.import_from_xdr(challenge_tx_server_signed)
        transaction.sign()
        challenge_tx = transaction.gen_xdr()
        with pytest.raises(InvalidSep10ChallengeError,
                           match="Transaction is not within range of the specified timebounds."):
            Builder.verify_challenge_tx(challenge_tx, server_kp.address().decode(),
                                        'TESTNET')
