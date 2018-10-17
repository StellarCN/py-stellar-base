# coding:utf-8
from os import path
import pytest

from stellar_base.operation import *
from stellar_base.asset import Asset
from stellar_base.keypair import Keypair
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te


class TestOp:
    source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
    dest = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
    amount = "1"

    def do(self, network, op):
        tx = Transaction(self.source, sequence=1)
        tx.add_operation(op)
        envelope = Te(tx, network_id=network)
        signer = Keypair.from_seed(self.seed)
        envelope.sign(signer)
        envelope_b64 = envelope.xdr()
        return envelope_b64

    def test_createAccount_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAEBBR+eUTPqpyTBLiNMudfSl2AN+oZL9/yp0KE9SyYeIzM2Y7yQH+dGNlwz5PMaaCEGAD+82IZkAPSDyunElc+EP'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAECCSD2qUFQXXfQTC44k3atcc2uiK+7ju0DGxnF/0guN+gRT6p1LcAJy3NQtd8jDDoa7pjoriZlXcVXiTCtyAPMD'
        assert (result == self.do(
            setup.network,
            op=CreateAccount(
                destination=self.dest,
                starting_balance=self.amount,
            )))

    def test_payment_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAlw7SoaRvm53xhs7ztskutJ3MlhBJ0ME2+uSBLiSCNV+wSolCAIIlWlMF376ciT5V9J6iWMcW1hVrZAQSI4cjDw=='
        assert (result == self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset.native(),
                amount=self.amount,
            )))

    def test_payment_short_asset(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQFosJrUliRYKU1jdh/po5Nyi9wiNiJ5Ve76C7Lu/THLxUfe2YKlORKGZ+aBbVe7q8FooQRutmnzbZ5GfIJYeYAk='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQJHNNenCn8ZIQMoYh86u6dVxZ20ZIsPeZFqRlNpzwgp4P5a0w82Q/pcg2vdG5h6xVClY7zKqK1JSIU1/RDlCvA0='
        assert (result == self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset('USD4', self.source),
                amount=self.amount,
            )))

    def test_payment_long_asset(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAACYloAAAAAAAAAAAc0+E2MAAABAE+vwbVK5XVhw3z8qqKW0P6HL7zZdgOSjSl6DVWQicmp2a0un8evaCUDXexCXxUx+UBf/HlowHJdLaXFKmRy5AQ=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAACYloAAAAAAAAAAAc0+E2MAAABAvtmMm0ySPn7q3SXccCPVa/J58MsWiL5ID/LlPRHtPP6A6N6LeLkB2PG0AXUv4d0t5Z29rKzCW3tlaJbGciYAAA=='
        assert (result == self.do(
            setup.network,
            op=Payment(
                source=self.source,
                destination=self.dest,
                asset=Asset('SNACKS789ABC', self.source),
                amount=self.amount,
            )))

    def test_pathPayment_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAIAAAAAAAAAAACYloAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAAAAAAHNPhNjAAAAQFwSz9wwBEWCv9cNnuIq+Jjq36mXBI22f6uj/FZ6LbyLljkckSLkF/AqXcaOoOgY9mZ0NrXsHbA5/chSThtgMgQ='  # TODO
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAIAAAAAAAAAAACYloAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAAAAAAHNPhNjAAAAQI1tBUmMqDa497gw9JJVgucfaiKr2e8VNWg/Pw9jM1d9qNWHBvEHxTLtBDyFKuJEguV1KVS7vBjFznlVCnKC3AI='
        assert (result == self.do(
            setup.network,
            op=PathPayment(
                source=self.source,
                destination=self.dest,
                send_asset=Asset.native(),
                dest_asset=Asset.native(),
                send_max=self.amount,
                dest_amount=self.amount,
                path=[],
            )))

    def test_manageOffer_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAMAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAHNPhNjAAAAQBTg1srmkpv/pFqELvCsSurwRPYRUpH05j1sgDzOZdILCdVpxb3sEvMgim1DXE0VhGXqbgZaQV/Sp2VH5C5RKQI='  # TODO
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAMAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAHNPhNjAAAAQCvR7B7vbXDy1ShEhYhlNzRIZRJ2DSmVhWe5kCDLWf9GTNhiSEfigaVs7UrPSeDWqPUVyzYx7Igu9JG6OL6WMwM='
        assert (result == self.do(
            setup.network,
            op=ManageOffer(
                selling=Asset('beer', self.source),
                buying=Asset('beer', self.dest),
                amount="100",
                price=3.14159,
                offer_id=1,
            )))

    def test_createPassiveOffer_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABzT4TYwAAAEAm4lQf6g7mpnw05syhOt3ub+OmSADhSfLwn/xg6bD+6qwqlpF/xflNYWKU1uQOy4P9e1+SWIGJdR+KWryykS0M'  # TODO
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAFiZWVyAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAADuaygAABMsvAAGGoAAAAAAAAAABzT4TYwAAAECvQiQXbKoZxYnF4qVL8GNBEzECgKUc0lNLJLYF/ML3mwPYkYRyldfxZ8h04P3iSjBmE+3srS05Ncajuy7+qugL'
        assert (result == self.do(
            setup.network,
            op=CreatePassiveOffer(
                selling=Asset('beer', self.source),
                buying=Asset('beer', self.dest),
                amount="100",
                price=3.14159,
            )))

    def test_SetOptions_empty(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc0+E2MAAABAymdhj3dFg+3TcCRILXdUu8ZhG3WOuBmX3YXcYJhYemjCDylQEk31vF8wxB/ntRg4/vmCYC2IwhBtw1mJZ8h+Bw=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAc0+E2MAAABAffce5U9sUC0cmi3ecjVayerdg+btd5u7fw1XguZO5mp3EjlZwATvCGdbSQbzH2wJrddAix8cHUgvJD1DdXr8DQ=='
        assert (result == self.do(setup.network, op=SetOptions()))

    def test_changeTrust_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQL0R9eOS0qesc+HHKQoHMjFUJWvzeQOy+u/7HBHNooo37AOaG85y9jyNoa1D4EduroZmK8vCfCF0V3rn5o9CpgA='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQEMLKLk6BmEehiEqR155eZoHTMf0bFoZcsvTZpv1KDPXkOdyJZlinNR6FHv7Odk/kvxV5pYET+zqrLCJUwhcjgs='
        assert (result == self.do(
            setup.network, op=ChangeTrust(asset=Asset('beer', self.dest), )))

    def test_allowTrust_shortAsset(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABYmVlcgAAAAEAAAAAAAAAAc0+E2MAAABALjUeQvesj2RdHj4xoQc1SFnertuoeSCE13VRJPxwsHPE8JMMM4JPfCXdgqoJ0uFTOPuPEZ0gQNdz1q0/l14HDg=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABYmVlcgAAAAEAAAAAAAAAAc0+E2MAAABAV3Lq9RaWrhckFLidPp3WwDnGmJfY/oTQECxJqinkP0PVgS94egZt6bY9hXNWXNrLePID1XpBzVm8K6plpW6qBw=='
        assert (result == self.do(
            setup.network,
            op=AllowTrust(
                trustor=self.dest,
                asset_code='beer',
                authorize=True,
            )))

    def test_allowTrust_longAsset(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACcG9ja2V0a25pdmVzAAAAAQAAAAAAAAABzT4TYwAAAEBK169VZqBQYUrs+ueQzx/UaANo+7HCdUcpflNvT4e5y7o+T7fxzJ845B3hVr8rrJ27Rz/VVslBWkXmxKoaa8sC'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAcAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACcG9ja2V0a25pdmVzAAAAAQAAAAAAAAABzT4TYwAAAEDGsNazdiNzGOy11OwmnTjRAqZFw3IWasKUrqj7jldElyRYZYILZ56N3PFkIUQXfE4+GI6uiQ3kN8eXQFLXBVUH'
        assert (result == self.do(
            setup.network,
            op=AllowTrust(
                trustor=self.dest,
                asset_code='pocketknives',
                authorize=True,
            )))

    def test_accountMerge_min(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAgAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAc0+E2MAAABADFSYbdlswOKfK4Y02Tz/j5j83c7f5YvLe+QxmXcHSd/W8ika63MsM6CDkDZhjRx4+Nt+mfCKpKbP7j0NPzNhCQ=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAgAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAc0+E2MAAABA0CkEVv6elPyZRDX554X2r51z3L1RFxOpdNNT4VHk8C/zi7pUPv92tJB7jZAExkCFOX0nDPYrb74RXYTzVxSZDg=='
        assert (result == self.do(
            setup.network, op=AccountMerge(destination=self.dest)))

    def test_inflation(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABAL2tfdCYqdtfxvINWVZ0iwcROqxQieoBF9cay5AL2oj2oJDrp3F3sYlHQNJi1orkcMLqsxaGtr6DWdnc0vwIBDg=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAkAAAAAAAAAAc0+E2MAAABAg4Tj3VkLb4/I/BjtdUEoSJRO3plqsw8fApTVazJaYlCafePH3mWcJyQefELPTRlFqbPxyTaQoRD9WK86g0CPAw=='
        assert (result == self.do(setup.network, op=Inflation()))

    def test_manage_data(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAoAAAAiMUtGSEU3dzhCaGFFTkFzd3dyeWFvY2NEYjZxY1Q2RGJZWQAAAAAAAQAAADhHREpWRkRHNU9DVzVQWVdIQjY0TUdUSEdGRjU3RFJSSkVEVUVGREVMMlNMTklPT05IWUpXSEEzWgAAAAAAAAABzT4TYwAAAECUCZhaxDGYHBBGS5UkvEWzrZvpg4zHB3joSkyFIA3GwCKKIwbLJiJrJT2seTcbCe/HOWowvgf3L/zo5LLXoPwH'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAoAAAAiMUtGSEU3dzhCaGFFTkFzd3dyeWFvY2NEYjZxY1Q2RGJZWQAAAAAAAQAAADhHREpWRkRHNU9DVzVQWVdIQjY0TUdUSEdGRjU3RFJSSkVEVUVGREVMMlNMTklPT05IWUpXSEEzWgAAAAAAAAABzT4TYwAAAEAwMGuJaQ2p5FGcFWms7omrCGbph64RslNqNLj5o6SfKFfKviCVbjzVm6FhNA3iOfBcAEPZgnSCcvRsirkiUvwK'
        assert (result == self.do(
            setup.network,
            op=ManageData(
                data_name='1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY',
                data_value=self.source,
            )))

    def test_bump_sequence(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAsAAAAFbsMSkgAAAAAAAAABzT4TYwAAAEDi5k05oazHoWRnj1g55Yhxf3rvJ+CwsuR7rB6BDg4oUuYjGAHV06IufC5pq2N+w/lOo/XegJasnpuXj9CQDZYC'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAsAAAAFbsMSkgAAAAAAAAABzT4TYwAAAEBCy2YhkcyBpz3Wz3BSchLX/0R1GY5aS1LJ3VJigadB8nt6t++/4j/9YEMWWEDl3JhRTOMhPN8SSSs/zK1S1NIM'
        assert (result == self.do(
            setup.network,
            op=BumpSequence(bump_to=23333114514)))


def _load_xdr_and_un_xdr_cases():
    filename = path.join(
        path.dirname(__file__), "txt", "xdr_for_transaction_enveloppe.txt")
    with open(filename, "r") as f:
        for line in f.readlines():
            s, data = line.strip().split(",")
            yield s, str.encode(data)


@pytest.mark.parametrize("name, xdr_data", _load_xdr_and_un_xdr_cases())
def test_xdr_and_un_xdr(name, xdr_data):
    assert xdr_data == Te.from_xdr(xdr_data).xdr()


class TestMultiOp:
    address = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    seed = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
    accounts = [
        {
            'address':
            'GCKMUHUBYSJNEIPMJ2ZHSXGSI7LLROFM5U43SWMRDV7J23HI63M7RW2D',
            'seed': 'SDKGBZFUZZEP3QKAFNLEINQ2MPD5QZJ35ZV7YNS6XCQ4NEHI6ND3ZMWC',
        },
        {
            'address':
            'GBG2TM6PGHAWRBVS37MBGOCQ7H7QQH7N2Y2WVUY7IMCEJ6MSF7LWQNIP',
            'seed': 'SAMM4N3BI447BUSTHPGO5NRHQY2J5QWECMPVHLXHZ3UKENU52UJ7MJLQ',
        },
        {
            'address':
            'GCQEAE6KDHPQMO3AJBRPSFV6FAPFYP27Q3EGE4PY4MZCTIV5RRA3KDBS',
            'seed': 'SDWJCTX6T3NJ6HEPDWFPMP33M2UDBPFKUCN7BIRFQYKXQTLO7NGDEVZE',
        },
    ]
    amount = "20"

    def make_envelope(self, network, *args, **kwargs):
        opts = {'sequence': 1, 'fee': 100 * len(args)}
        for opt, value in kwargs.items():
            opts[opt] = value
        tx = Transaction(self.address, **opts)
        for count, op in enumerate(args):
            tx.add_operation(op)
        envelope = Te(tx, network_id=network)
        signer = Keypair.from_seed(self.seed)
        envelope.sign(signer)
        envelope_b64 = envelope.xdr()
        print(envelope_b64)
        return envelope_b64

    def test_double_create_account(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAAAAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAABfXhAAAAAAAAAAAAc0+E2MAAABAidcFTo+BW8L5rcG+tw1WldkHDs+0uNnMuxu0mCWbhm9tcjKplBkmfXYLn6kLh+ray5Ow6EQClAnDSSEyBarQBQ=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAAAAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAABfXhAAAAAAAAAAAAc0+E2MAAABAfIa9NK/HO/m2mkDAfl5XOM/cGshfsMqw0F1pa9bnBRxv368wSNodbsa22NYfES6jNidDacJkZdfumcpXLwRWDw=='
        assert (result == self.make_envelope(
            setup.network,
            CreateAccount(
                destination=self.accounts[0]['address'],
                starting_balance=self.amount,
            ),
            CreateAccount(
                destination=self.accounts[1]['address'],
                starting_balance="40",
            ),
        ))

    def test_double_payment(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAEAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAAAAAAvrwgAAAAAAAAAAAQAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAAAAAAAF9eEAAAAAAAAAAABzT4TYwAAAEAhTZr3nE2w9LBziL54UuyuEgUa4MJaXfMnZpHpu9+TYgPaDE3M6DNe6Du8ZSSC89LCGfpS1Fs38JB0U5rikmMP'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAyAAAAAAAAAACAAAAAAAAAAAAAAACAAAAAAAAAAEAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAAAAAAAvrwgAAAAAAAAAAAQAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAAAAAAAF9eEAAAAAAAAAAABzT4TYwAAAEAC/EENKQWCZFsKcNMEpWi7TVstQF0JbmBj/+QwkQXW8q/isCHX+UikrhxXJpI5NDKdagnH0godVShWxK1PENAC'
        assert (result == self.make_envelope(
            setup.network,
            Payment(
                destination=self.accounts[0]['address'],
                asset=Asset.native(),
                amount=self.amount,
            ),
            Payment(
                destination=self.accounts[1]['address'],
                asset=Asset.native(),
                amount="40",
            ),
        ))

    def test_mix_1(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAADhAAAAAAAAAACAAAAAAAAAAAAAAAJAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAABAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAAAAAAAL68IAAAAAAAAAAAIAAAAAAAAAAAvrwgAAAAAAoEATyhnfBjtgSGL5Fr4oHlw/X4bIYnH44zIpor2MQbUAAAAAAAAAAAvrwgAAAAAAAAAAAAAAAAMAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFiZWVyAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAFiZWVyAAAAAKBAE8oZ3wY7YEhi+Ra+KB5cP1+GyGJx+OMyKaK9jEG1AAAAADuaygAABMsvAAGGoAAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+H//////////AAAAAAAAAAcAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAABYmVlcgAAAAEAAAAAAAAACAAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAAAAAABzT4TYwAAAECnD5OPLjCC3vjtrsffS0fekR0rEgJZoDvJrOdp2G4LBKWLPsH4ZKVVGiOxPq2akIowWckiYXwZG45/mSLSbloN'
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAADhAAAAAAAAAACAAAAAAAAAAAAAAAJAAAAAAAAAAAAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAAAC+vCAAAAAAAAAAABAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAAAAAAAAL68IAAAAAAAAAAAIAAAAAAAAAAAvrwgAAAAAAoEATyhnfBjtgSGL5Fr4oHlw/X4bIYnH44zIpor2MQbUAAAAAAAAAAAvrwgAAAAAAAAAAAAAAAAMAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFiZWVyAAAAAE2ps88xwWiGst/YEzhQ+f8IH+3WNWrTH0MERPmSL9doAAAAADuaygAABMsvAAGGoAAAAAAAAAABAAAAAAAAAAQAAAABYmVlcgAAAABNqbPPMcFohrLf2BM4UPn/CB/t1jVq0x9DBET5ki/XaAAAAAFiZWVyAAAAAKBAE8oZ3wY7YEhi+Ra+KB5cP1+GyGJx+OMyKaK9jEG1AAAAADuaygAABMsvAAGGoAAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABYmVlcgAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+H//////////AAAAAAAAAAcAAAAAlMoegcSS0iHsTrJ5XNJH1ri4rO05uVmRHX6dbOj22fgAAAABYmVlcgAAAAEAAAAAAAAACAAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAAAAAABzT4TYwAAAEAY0YGZzC1qiKatKCWaCttK1fEs3P4DpVWw2AQCdvVBS4dkCyfxu7N7tpQPEZ4WqXzAiR0D7r5L6f848pmNsgIL'
        assert (result == self.make_envelope(
            setup.network,
            CreateAccount(
                destination=self.accounts[0]['address'],
                starting_balance=self.amount,
            ),
            Payment(
                destination=self.accounts[1]['address'],
                asset=Asset.native(),
                amount=self.amount,
            ),
            PathPayment(
                destination=self.accounts[2]['address'],
                send_asset=Asset.native(),
                dest_asset=Asset.native(),
                send_max=self.amount,
                dest_amount=self.amount,
                path=[],
            ),
            ManageOffer(
                selling=Asset('beer', self.accounts[0]['address']),
                buying=Asset('beer', self.accounts[1]['address']),
                amount="100",
                price=3.14159,
                offer_id=1,
            ),
            CreatePassiveOffer(
                selling=Asset('beer', self.accounts[1]['address']),
                buying=Asset('beer', self.accounts[2]['address']),
                amount="100",
                price=3.14159,
            ), SetOptions(),
            ChangeTrust(
                asset=Asset('beer', self.accounts[0]['address']), ),
            AllowTrust(
                trustor=self.accounts[0]['address'],
                asset_code='beer',
                authorize=True,
            ), AccountMerge(destination=self.accounts[0]['address'], )))

    def test_mix_2(self, setup):
        if setup.type == 'testnet':
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAABkAAAAAAAAAACAAAAAAAAAAAAAAAEAAAAAAAAAAUAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABRVVSAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAjhvJvwQAAAAAAAAAAAAcAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABRVVSAAAAAAEAAAAAAAAAAQAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFFVVIAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjACOG8m/BAAAAAAAAAAAAAc0+E2MAAABAUDuJuoUdHYxE/AmYKN4x+EvI3NpLtAgs9xYq4AJMFVmC2zDIn1J2+o5uIyqYxQW84SW31laWcrY8YkGWPqkeBA=='
        else:
            result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAABkAAAAAAAAAACAAAAAAAAAAAAAAAEAAAAAAAAAAUAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAABRVVSAAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAjhvJvwQAAAAAAAAAAAAcAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABRVVSAAAAAAEAAAAAAAAAAQAAAACUyh6BxJLSIexOsnlc0kfWuLis7Tm5WZEdfp1s6PbZ+AAAAAFFVVIAAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjACOG8m/BAAAAAAAAAAAAAc0+E2MAAABAKHsltQKqjdueu13k7PI7cLg4Tya2aOFH+1Sc9qeK4z0AXxropuRVHhyuriPu/ZXHIRVDvD5xQ0SmMFPVFtU0BA=='
        assert (result == self.make_envelope(
            setup.network,
            SetOptions(set_flags=1),
            ChangeTrust(
                asset=Asset('EUR', self.address), limit="1000000000"),
            AllowTrust(
                authorize=True, asset_code='EUR',
                trustor=self.address),
            Payment(
                destination=self.accounts[0]['address'],
                asset=Asset('EUR', self.address),
                amount="1000000000")))
