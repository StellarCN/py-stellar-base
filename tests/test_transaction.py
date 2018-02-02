# coding: utf-8
from stellar_base.memo import *
from stellar_base.operation import *


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
