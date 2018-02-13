# coding:utf-8

from nose.tools import raises
from stellar_base.memo import *
from stellar_base.operation import *
from stellar_base.asset import Asset
from stellar_base.transaction_envelope import TransactionEnvelope as Te


class TestOp:
    def __init__(self):
        self.source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
        self.seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
        self.dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
        self.seq = 1
        self.fee = 100
        self.amount = "1"

    def do(self, op):
        from stellar_base.transaction import Transaction
        from stellar_base.keypair import Keypair
        from stellar_base.transaction_envelope import TransactionEnvelope as Te
        tx = Transaction(source=self.source, opts={'sequence': self.seq})
        tx.add_operation(operation=op)
        envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
        signer = Keypair.from_seed(seed=self.seed)
        envelope.sign(keypair=signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_to_xdr_amount(self):
        assert (Operation.to_xdr_amount("20") == 20 * 10 ** 7)
        assert (Operation.to_xdr_amount("0.1234567") == 1234567)

    @raises(Exception)
    def test_to_xdr_amount_inexact(self):
        Operation.to_xdr_amount("0.12345678")

    @raises(Exception)
    def test_to_xdr_amount_not_number(self):
        Operation.to_xdr_amount("test")

    @raises(Exception)
    def test_to_xdr_amount_not_string(self):
        Operation.to_xdr_amount(0.1234)

    def test_from_xdr_amount(self):
        assert (Operation.from_xdr_amount(10 ** 7) == "1")
        assert (Operation.from_xdr_amount(20 * 10 ** 7) == "20")
        assert (Operation.from_xdr_amount(1234567) == "0.1234567")
        assert (Operation.from_xdr_amount(112345678) == "11.2345678")

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
            'amount': "100",
            'price': 3.14159,
            'offer_id': 1,
        })))

    def test_createPassiveOffer_min(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABzT4TYwAAAEAm4lQf6g7mpnw05syhOt3ub+OmSADhSfLwn/xg6bD+6qwqlpF/xflNYWKU1uQOy4P9e1+SWIGJdR+KWryykS0M'  # TODO
        assert (result == self.do(op=CreatePassiveOffer({
            'selling': Asset('beer', self.source),
            'buying': Asset('beer', self.dest),
            'amount': "100",
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

    def test_manage_data(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAoAAAAiMUtGSEU3dzhCaGFFTkFzd3dyeWFvY2NEYjZxY1Q2RGJZWQAAAAAAAQAAADhHREpWRkRHNU9DVzVQWVdIQjY0TUdUSEdGRjU3RFJSSkVEVUVGREVMMlNMTklPT05IWUpXSEEzWgAAAAAAAAABzT4TYwAAAECUCZhaxDGYHBBGS5UkvEWzrZvpg4zHB3joSkyFIA3GwCKKIwbLJiJrJT2seTcbCe/HOWowvgf3L/zo5LLXoPwH'
        assert (result == self.do(op=ManageData({
            'data_name': '1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
            'data_value': self.source,
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
            'sequence': self.seq,
            'memo': TextMemo('testing'),
        }))

    def test_textMemo_unicode(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAMdMSTxaF0xKvFhsSjAAAAAQAAAAAAAAAJAAAAAAAAAAHNPhNjAAAAQLW0BjNvpw3FWZwrXHWmno436IrqDQLzPD7wWsVBdrp+VG244GTfSJfUYJwaOiiqEt93G7KTUIc/HLxO8saMeAo='
        assert (result == self.do(op={
            'sequence': self.seq,
            'memo': TextMemo('tēštīņģ'),
        }))


class TestunXdr:
    def test_allowTrust_shortAsset_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACcG9ja2V0a25pdmVzAAAAAQAAAAAAAAABzT4TYwAAAEBK169VZqBQYUrs+ueQzx/UaANo+7HCdUcpflNvT4e5y7o+T7fxzJ845B3hVr8rrJ27Rz/VVslBWkXmxKoaa8sC'
        assert (result == Te.from_xdr(result).xdr())

    def test_createAccount_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAEBBR+eUTPqpyTBLiNMudfSl2AN+oZL9/yp0KE9SyYeIzM2Y7yQH+dGNlwz5PMaaCEGAD+82IZkAPSDyunElc+EP'
        assert (result == Te.from_xdr(result).xdr())

    def test_payment_short_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
        assert (result == Te.from_xdr(result).xdr())

    def test_pathPayment_min_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAIAAAAAAAAAAACYloAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAAAAAAHNPhNjAAAAQFwSz9wwBEWCv9cNnuIq+Jjq36mXBI22f6uj/FZ6LbyLljkckSLkF/AqXcaOoOgY9mZ0NrXsHbA5/chSThtgMgQ='  # TODO
        assert (result == Te.from_xdr(result).xdr())

    def test_changeTrust_min_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQL0R9eOS0qesc+HHKQoHMjFUJWvzeQOy+u/7HBHNooo37AOaG85y9jyNoa1D4EduroZmK8vCfCF0V3rn5o9CpgA='
        assert (result == Te.from_xdr(result).xdr())

    def test_accountMerge_min_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAgAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAc0+E2MAAABADFSYbdlswOKfK4Y02Tz/j5j83c7f5YvLe+QxmXcHSd/W8ika63MsM6CDkDZhjRx4+Nt+mfCKpKbP7j0NPzNhCQ=='
        assert (result == Te.from_xdr(result).xdr())

    def test_inflation_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABAL2tfdCYqdtfxvINWVZ0iwcROqxQieoBF9cay5AL2oj2oJDrp3F3sYlHQNJi1orkcMLqsxaGtr6DWdnc0vwIBDg=='
        assert (result == Te.from_xdr(result).xdr())

    def test_createPassiveOffer_min_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABzT4TYwAAAEAm4lQf6g7mpnw05syhOt3ub+OmSADhSfLwn/xg6bD+6qwqlpF/xflNYWKU1uQOy4P9e1+SWIGJdR+KWryykS0M'  # TODO
        assert (result == Te.from_xdr(result).xdr())

    def test_manageOffer_min_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAMAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAHNPhNjAAAAQBTg1srmkpv/pFqELvCsSurwRPYRUpH05j1sgDzOZdILCdVpxb3sEvMgim1DXE0VhGXqbgZaQV/Sp2VH5C5RKQI='  # TODO
        print(result)
        print(Te.from_xdr(result).xdr())

    def test_SetOptions_empty_unXdr(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc0+E2MAAABAymdhj3dFg+3TcCRILXdUu8ZhG3WOuBmX3YXcYJhYemjCDylQEk31vF8wxB/ntRg4/vmCYC2IwhBtw1mJZ8h+Bw=='
        assert (result == Te.from_xdr(result).xdr())


class TestMultiOp:
    def __init__(self):
        self.address = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
        self.seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
        self.accounts = [
            {
                'address': 'GCKMUHUBYSJNEIPMJ2ZHSXGSI7LLROFM5U43SWMRDV7J23HI63M7RW2D',
                'seed': 'SDKGBZFUZZEP3QKAFNLEINQ2MPD5QZJ35ZV7YNS6XCQ4NEHI6ND3ZMWC',
            },
            {
                'address': 'GBG2TM6PGHAWRBVS37MBGOCQ7H7QQH7N2Y2WVUY7IMCEJ6MSF7LWQNIP',
                'seed': 'SAMM4N3BI447BUSTHPGO5NRHQY2J5QWECMPVHLXHZ3UKENU52UJ7MJLQ',
            },
            {
                'address': 'GCQEAE6KDHPQMO3AJBRPSFV6FAPFYP27Q3EGE4PY4MZCTIV5RRA3KDBS',
                'seed': 'SDWJCTX6T3NJ6HEPDWFPMP33M2UDBPFKUCN7BIRFQYKXQTLO7NGDEVZE',
            },
        ]
        self.seq = 1
        self.fee = 100
        self.amount = "20"

    def make_envelope(self, *args, **kwargs):
        from stellar_base.transaction import Transaction
        from stellar_base.keypair import Keypair
        from stellar_base.transaction_envelope import TransactionEnvelope as Te
        opts = {
            'sequence': self.seq,
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
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_double_create_account(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAAAAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAABfXhAAAAAAAAAAAAc0+E2MAAABAidcFTo+BW8L5rcG+tw1WldkHDs+0uNnMuxu0mCWbhm9tcjKplBkmfXYLn6kLh+ray5Ow6EQClAnDSSEyBarQBQ=='
        assert (result == self.make_envelope(
            CreateAccount({
                'destination': self.accounts[0]['address'],
                'starting_balance': self.amount,
            }),
            CreateAccount({
                'destination': self.accounts[1]['address'],
                'starting_balance': "40",
            }),
        ))

    def test_double_payment(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAEAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAAAAAAvrwgAAAAAAAAAAAQAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAAAAAAAF9eEAAAAAAAAAAABzT4TYwAAAEAhTZr3nE2w9LBziL54UuyuEgUa4MJaXfMnZpHpu9+TYgPaDE3M6DNe6Du8ZSSC89LCGfpS1Fs38JB0U5rikmMP'
        assert (result == self.make_envelope(
            Payment({
                'destination': self.accounts[0]['address'],
                'asset': Asset.native(),
                'amount': self.amount,
            }),
            Payment({
                'destination': self.accounts[1]['address'],
                'asset': Asset.native(),
                'amount': "40",
            }),
        ))

    def test_mix_1(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAADhAAAAAAAAAACAAAAAAAAAAAAAAAJAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAABAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAAAAAAAL68IAAAAAAAAAAAIAAAAAAAAAAAvrwgAAAAAAoEATyhnfBjtgSGL5Fr4oHlw/X4bIYnH44zIpor2MQbUAAAAAAAAAAAvrwgAAAAAAAAAAAAAAAAMAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFiZWVyAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAFiZWVyAAAAAKBAE8oZ3wY7YEhi+Ra+KB5cP1+GyGJx+OMyKaK9jEG1AAAAADuaygAABMsvAAGGoAAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+H//////////AAAAAAAAAAcAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAABYmVlcgAAAAEAAAAAAAAACAAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAAAAAABzT4TYwAAAECnD5OPLjCC3vjtrsffS0fekR0rEgJZoDvJrOdp2G4LBKWLPsH4ZKVVGiOxPq2akIowWckiYXwZG45/mSLSbloN'
        assert (result == self.make_envelope(
            CreateAccount({
                'destination': self.accounts[0]['address'],
                'starting_balance': self.amount,
            }),
            Payment({
                'destination': self.accounts[1]['address'],
                'asset': Asset.native(),
                'amount': self.amount,
            }),
            PathPayment({
                'destination': self.accounts[2]['address'],
                'send_asset': Asset.native(),
                'dest_asset': Asset.native(),
                'send_max': self.amount,
                'dest_amount': self.amount,
                'path': [],
            }),
            ManageOffer({
                'selling': Asset('beer', self.accounts[0]['address']),
                'buying': Asset('beer', self.accounts[1]['address']),
                'amount': "100",
                'price': 3.14159,
                'offer_id': 1,
            }),
            CreatePassiveOffer({
                'selling': Asset('beer', self.accounts[1]['address']),
                'buying': Asset('beer', self.accounts[2]['address']),
                'amount': "100",
                'price': 3.14159,
            }),
            SetOptions({
            }),
            ChangeTrust({
                'asset': Asset('beer', self.accounts[0]['address']),
            }),
            AllowTrust({
                'trustor': self.accounts[0]['address'],
                'asset_code': 'beer',
                'authorize': True,
            }),
            AccountMerge({
                'destination': self.accounts[0]['address'],
            })
        ))

    def test_mix_2(self):
        result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAABkAAAAAAAAAACAAAAAAAAAAAAAAAEAAAAAAAAAAUAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABRVVSAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TY3//////////AAAAAAAAAAcAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABRVVSAAAAAAEAAAAAAAAAAQAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFFVVIAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjACOG8m/BAAAAAAAAAAAAAc0+E2MAAABAF6FAYEQK+zQ/hqifpyOElc2FJTIEvpEaMnImRMpfoDrnjFBXz3SRCGZawizJUPVkAWoCxIth4pbqmX4UfGGaCQ=='
        assert (result == self.make_envelope(
            SetOptions({
                'set_flags': 1
            }),
            ChangeTrust({
                'asset': Asset('EUR', self.address),
                'amount': "1000000000"
            }),
            AllowTrust({
                'authorize': True,
                'asset_code': 'EUR',
                'trustor': self.address
            }),
            Payment({
                'destination': self.accounts[0]['address'],
                'asset': Asset('EUR', self.address),
                'amount': "1000000000"
            })
        ))
