# coding:utf-8
import copy
import os
import sys
import mock
import pytest

from stellar_base.operation import *
from stellar_base.asset import Asset
from stellar_base.exceptions import NotValidParamError

DEST = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
SOURCE = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'


@pytest.mark.parametrize("s, error_type", [
    ("0.12345678", NotValidParamError),
    ("test", NotValidParamError),
    (0.1234, NotValidParamError),
])
def test_to_xdr_amount_raise(s, error_type):
    if sys.version_info.major == 2:
        error_type = Exception
    with pytest.raises(error_type):
        Operation.to_xdr_amount(s)


@pytest.mark.parametrize("num, s", [
    (10 ** 7, "1"),
    (20 * 10 ** 7, "20"),
    (1234567, "0.1234567"),
    (112345678, "11.2345678"),
])
def test_from_and_to_xdr_amount(num, s):
    assert s == Operation.from_xdr_amount(num)
    assert num == Operation.to_xdr_amount(s)


def _load_operations():
    amount = "1"
    return [
        ("create_account_min",
         CreateAccount(
             source=SOURCE, destination=DEST, starting_balance=amount)),
        ("payment_min",
         Payment(
             source=SOURCE,
             destination=DEST,
             asset=Asset.native(),
             amount=amount,
         )),
        ("payment_short_asset",
         Payment(
             source=SOURCE,
             destination=DEST,
             asset=Asset('USD4', SOURCE),
             amount=amount,
         )),
        ("payment_long_asset",
         Payment(
             source=SOURCE,
             destination=DEST,
             asset=Asset('SNACKS789ABC', SOURCE),
             amount=amount,
         )),
        ("path_payment_min",
         PathPayment(
             source=SOURCE,
             destination=DEST,
             send_asset=Asset.native(),
             dest_asset=Asset.native(),
             send_max=amount,
             dest_amount=amount,
             path=[],
         )),
        ("path_payment",
         PathPayment(
             destination=DEST,
             send_asset=Asset.native(),
             dest_asset=Asset.native(),
             send_max=amount,
             dest_amount=amount,
             path=[Asset('MOE', DEST)],
         )),
        ("allow_trust_short_asset",
         AllowTrust(
             source=SOURCE,
             trustor=DEST,
             asset_code='beer',
             authorize=True,
         )),
        ("allow_trust_long_asset",
         AllowTrust(
             source=SOURCE,
             trustor=DEST,
             asset_code='pocketknives',
             authorize=True,
         )),
        ("manage_offer_min",
         ManageOffer(
             selling=Asset('beer', SOURCE),
             buying=Asset('beer', DEST),
             amount="100",
             price=3.14159,
             offer_id=1,
             source=SOURCE
         )),
        ("manage_offer_dict_price",
         ManageOffer(
             selling=Asset('beer', SOURCE),
             buying=Asset('beer', DEST),
             amount="100",
             price={
                 'n': 314159,
                 'd': 100000
             },
             offer_id=1,
         )),
        ("create_passive_offer_min",
         CreatePassiveOffer(
             selling=Asset('beer', SOURCE),
             buying=Asset('beer', DEST),
             amount="100",
             price=3.14159,
             source=SOURCE
         )),
        ("create_passive_dict_offer",
         CreatePassiveOffer(
             selling=Asset('beer', SOURCE),
             buying=Asset('beer', DEST),
             amount="100",
             price={
                 'n': 314159,
                 'd': 100000
             }
         )),
        ("set_options_empty", SetOptions()),
        ("set_options_ed25519PublicKey",
         SetOptions(signer_type='ed25519PublicKey', signer_address=DEST, signer_weight=1)),
        ("set_options_hashX", SetOptions(signer_type='hashX', signer_address=os.urandom(32), signer_weight=2)),
        ("set_options_preAuthTx", SetOptions(signer_type='preAuthTx', signer_address=os.urandom(32), signer_weight=3)),
        ("set_options_inflation_dest",
         SetOptions(inflation_dest=DEST, source=SOURCE)),
        ("change_trust_min",
         ChangeTrust(source=SOURCE, asset=Asset('beer', DEST), limit='100')),
        ("change_trust_default_limit",
         ChangeTrust(source=SOURCE, asset=Asset('beer', DEST))),
        ("account_merge_min", AccountMerge(
            source=SOURCE,
            destination=DEST,
        )),
        ("inflation", Inflation(source=SOURCE)),
        ("manage_data",
         ManageData(
             source=SOURCE,
             data_name='1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
             data_value=SOURCE,
         )),
        ("manage_data_none",
         ManageData(
             data_name='1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
             data_value=None,
         )),
        ("bump_sequence", BumpSequence(
            source=SOURCE,
            bump_to=23333114514
        )),
        ("bump_sequence_no_source", BumpSequence(
            bump_to=23333114514
        ))
    ]


@pytest.mark.parametrize("name, operation", _load_operations())
def test_operation(name, operation):
    operation_restored = Operation.from_xdr(operation.xdr())
    assert operation == operation_restored
    original = dict(operation.__dict__)
    original.pop("body")
    restored = dict(operation_restored.__dict__)
    restored.pop("body")
    if name == 'manage_offer_dict_price' or name == 'create_passive_dict_offer':
        original['price'] = float(original['price']['n']) / float(
            original['price']['d'])
    if name == 'manage_data':  # return `bytes` now
        if not isinstance(original['data_value'], bytes):
            original['data_value'] = bytes(original['data_value'], 'utf-8')
    assert original == restored


def test_from_xdr_object_raise():
    operation = mock.MagicMock(type=2561)
    pytest.raises(NotImplementedError, Operation.from_xdr_object, operation)


def test_manage_data_too_long_raises():
    msg = 'Data and value should be <= 64 bytes \(ascii encoded\).'
    with pytest.raises(NotValidParamError, match=msg):
        ManageData(
            data_name='1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
            data_value='1234567890' * 7)


def test_manage_offer_dict_price_raises():
    msg = "You need pass `price` params as `str` or `{'n': numerator, 'd': denominator}`"
    with pytest.raises(NotValidParamError, match=msg):
        ManageOffer(
            selling=Asset('beer', SOURCE),
            buying=Asset('beer', DEST),
            amount="100",
            price={},
            offer_id=1,
        ).xdr()


def test_set_options_signer_raises():
    op = SetOptions(signer_address=SOURCE)
    assert op == SetOptions(signer_address=SOURCE, signer_type='ed25519PublicKey')

    with pytest.raises(StellarAddressInvalidError, match='Must be a valid stellar address if not give signer_type'):
        SetOptions(signer_address=SOURCE + 'ERROR')

    with pytest.raises(NotValidParamError,
                       match='Invalid signer type, sign_type should be ed25519PublicKey, hashX or preAuthTx'):
        SetOptions(signer_address=SOURCE, signer_type='bad_type')


def test_deepcopy():
    payment = Payment(SOURCE, Asset('XLM'), '1')
    payment_copy1 = copy.deepcopy(payment)
    xdr = payment.xdr()
    payment_copy2 = copy.deepcopy(payment)
    assert payment_copy1.xdr() == payment_copy2.xdr() == xdr
