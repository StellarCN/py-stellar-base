# coding:utf-8

from stellar_base.memo import *
from stellar_base.operation import *
from stellar_base.asset import Asset


class TestOp:
    def __init__(self):
        self.source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
        self.seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
        self.dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
        self.seq = 1
        self.fee = 100
        self.amount = 10 * 10 ** 6

    def do(self, op):
        from stellar_base.transaction import Transaction
        from stellar_base.keypair import Keypair
        from stellar_base.transaction_envelope import TransactionEnvelope as Te
        tx = Transaction(source=self.source, opts={'seqNum': self.seq})
        tx.add_operation(operation=op)
        envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
        signer = Keypair.from_seed(seed=self.seed)
        envelope.sign(keypair=signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_createAccount_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAEBBR+eUTPqpyTBLiNMudfSl2AN+oZL9/yp0KE9SyYeIzM2Y7yQH+dGNlwz5PMaaCEGAD+82IZkAPSDyunElc+EP'
        assert (result == self.do(op=CreateAccount({
            'destination': self.dest,
            'starting_balance': self.amount,
        })))

    def test_payment_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
        assert (result == self.do(op=Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset.native(),
            'amount': self.amount,
        })))

    def test_payment_short_asset(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQFosJrUliRYKU1jdh/po5Nyi9wiNiJ5Ve76C7Lu/THLxUfe2YKlORKGZ+aBbVe7q8FooQRutmnzbZ5GfIJYeYAk='
        assert (result == self.do(op=Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset('USD4', self.source),
            'amount': self.amount,
        })))

    def test_payment_long_asset(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAACYloAAAAAAAAAAAc0+E2MAAABAE+vwbVK5XVhw3z8qqKW0P6HL7zZdgOSjSl6DVWQicmp2a0un8evaCUDXexCXxUx+UBf/HlowHJdLaXFKmRy5AQ=='
        assert (result == self.do(op=Payment({
            'source': self.source,
            'destination': self.dest,
            'asset': Asset('SNACKS789ABC', self.source),
            'amount': self.amount,
        })))

    def test_pathPayment_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAIAAAAAAAAAAACYloAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAAAAAAHNPhNjAAAAQFwSz9wwBEWCv9cNnuIq+Jjq36mXBI22f6uj/FZ6LbyLljkckSLkF/AqXcaOoOgY9mZ0NrXsHbA5/chSThtgMgQ='  # TODO
        assert (result == self.do(op=PathPayment({
            'source': self.source,
            'destination': self.dest,
            'send_asset': Asset.native(),
            'dest_asset': Asset.native(),
            'send_max': self.amount,
            'dest_amount': self.amount,
            'path': [],
        })))

    def test_manageOffer_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAMAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAHNPhNjAAAAQBTg1srmkpv/pFqELvCsSurwRPYRUpH05j1sgDzOZdILCdVpxb3sEvMgim1DXE0VhGXqbgZaQV/Sp2VH5C5RKQI='  # TODO
        assert (result == self.do(op=ManageOffer({
            'selling': Asset('beer', self.source),
            'buying': Asset('beer', self.dest),
            'amount': 100 * 10**7,
            'price': 3.14159,
            'offerId': 1,
        })))

    def test_createPassiveOffer_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABzT4TYwAAAEAm4lQf6g7mpnw05syhOt3ub+OmSADhSfLwn/xg6bD+6qwqlpF/xflNYWKU1uQOy4P9e1+SWIGJdR+KWryykS0M'  # TODO
        assert (result == self.do(op=CreatePassiveOffer({
            'selling': Asset('beer', self.source),
            'buying': Asset('beer', self.dest),
            'amount': 100* 10**7,
            'price': 3.14159,
        })))

    def test_SetOptions_empty(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc0+E2MAAABAymdhj3dFg+3TcCRILXdUu8ZhG3WOuBmX3YXcYJhYemjCDylQEk31vF8wxB/ntRg4/vmCYC2IwhBtw1mJZ8h+Bw=='
        assert (result == self.do(op=SetOptions({
        })))

    def test_changeTrust_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQL0R9eOS0qesc+HHKQoHMjFUJWvzeQOy+u/7HBHNooo37AOaG85y9jyNoa1D4EduroZmK8vCfCF0V3rn5o9CpgA='
        assert (result == self.do(op=ChangeTrust({
            'asset': Asset('beer', self.dest),
        })))

    def test_allowTrust_shortAsset(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABYmVlcgAAAAEAAAAAAAAAAc0+E2MAAABALjUeQvesj2RdHj4xoQc1SFnertuoeSCE13VRJPxwsHPE8JMMM4JPfCXdgqoJ0uFTOPuPEZ0gQNdz1q0/l14HDg=='
        assert (result == self.do(op=AllowTrust({
            'trustor': self.dest,
            'asset_code': 'beer',
            'authorize': True,
        })))

    def test_allowTrust_longAsset(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACcG9ja2V0a25pdmVzAAAAAQAAAAAAAAABzT4TYwAAAEBK169VZqBQYUrs+ueQzx/UaANo+7HCdUcpflNvT4e5y7o+T7fxzJ845B3hVr8rrJ27Rz/VVslBWkXmxKoaa8sC'
        assert (result == self.do(op=AllowTrust({
            'trustor': self.dest,
            'asset_code': 'pocketknives',
            'authorize': True,
        })))

    def test_accountMerge_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAgAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAc0+E2MAAABADFSYbdlswOKfK4Y02Tz/j5j83c7f5YvLe+QxmXcHSd/W8ika63MsM6CDkDZhjRx4+Nt+mfCKpKbP7j0NPzNhCQ=='
        assert (result == self.do(op=AccountMerge({
            'destination': self.dest,
        })))

    def test_inflation(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABAL2tfdCYqdtfxvINWVZ0iwcROqxQieoBF9cay5AL2oj2oJDrp3F3sYlHQNJi1orkcMLqsxaGtr6DWdnc0vwIBDg=='
        assert (result == self.do(op=Inflation({
        })))


class TestTx:
    def __init__(self):
        self.source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
        self.seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
        self.dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
        self.seq = 1
        self.fee = 100
        self.amount = 10 * 10 ** 6

    def do(self, op):
        from stellar_base.transaction import Transaction
        from stellar_base.keypair import Keypair
        from stellar_base.transaction_envelope import TransactionEnvelope as Te
        tx = Transaction(source=self.source, opts=op)
        tx.add_operation(operation=Inflation({}))
        envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
        signer = Keypair.from_seed(seed=self.seed)
        envelope.sign(keypair=signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_textMemo_ascii(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAHdGVzdGluZwAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABA0nGC1i7CxTIJYNZKgo067Tr6JTCZTIU5Jwa2kpNMR7ayPohKVTaO53kojTn0c+NftXaogRZvz4/9etdOhDhlDQ=='
        assert (result == self.do(op={
            'seqNum': self.seq,
            'memo': TextMemo('testing'),
        }))

    def test_textMemo_unicode(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAMdMSTxaF0xKvFhsSjAAAAAQAAAAAAAAAJAAAAAAAAAAHNPhNjAAAAQLW0BjNvpw3FWZwrXHWmno436IrqDQLzPD7wWsVBdrp+VG244GTfSJfUYJwaOiiqEt93G7KTUIc/HLxO8saMeAo='
        assert (result == self.do(op={
            'seqNum': self.seq,
            'memo': TextMemo('tēštīņģ'),
        }))
