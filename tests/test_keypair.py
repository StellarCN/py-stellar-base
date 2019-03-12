from unittest import TestCase

import pytest
from pytest import raises

from stellar_base.keypair import Keypair
from stellar_base.exceptions import MissingSigningKeyError, NotValidParamError, BadSignatureError


class KeypairTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mnemonic = ('illness spike retreat truth genius clock brain pass '
                        'fit cave bargain toe')
        cls.keypair0 = Keypair.deterministic(cls.mnemonic)
        cls.sign_data = "hello".encode()
        cls.signature = b"\xa3[\xd8Z\xa3\x8a\xb3h'\xdf0\x0e\xf3\xff\x19C\xdf\xc6\xfb\xfb\xe4\xd9\x8c\x9f\x99\xbdU\x11\xf6.\xb1`\x815\xe9\xcd\x81\x006\xe0&\xb3 \x98\xe4w\xe0\x15`\x92s\xd3;h\xc1\x10P&\xec\xbf=\x17\xc5\x07"

    def test_from_seed(self):
        keypair = Keypair.from_seed(self.keypair0.seed())
        assert self.keypair0.address() == keypair.address()

    def test_sign_missing_signing_key_raise(self):
        keypair = Keypair.from_address(self.keypair0.address())
        raises(MissingSigningKeyError, keypair.sign, "")

    def test_init_wrong_type_key_raise(self):
        raises(NotValidParamError, Keypair, self.mnemonic)

    def test_xdr(self):
        assert self.keypair0.xdr() == b'AAAAAONyaDCgtgy19SyETP/NTu1l66XBVeibJkEVYnJOceVE'

    def test_sign(self):
        assert self.keypair0.sign("hello".encode()) == self.signature

    def test_verify(self):
        assert self.keypair0.verify(self.sign_data, self.signature) is None

    def test_bad_signature_raise(self):
        with pytest.raises(BadSignatureError, match="Signature verification failed."):
            self.keypair0.verify(self.sign_data + " ".encode(), self.signature)

    def test_old_style_base58_keypair(self):
        seed = 'sfjCwvnEU9HuTDtJB8f8sn4Z4fLMT7p3DiJQvCTHf1pJ1JYxeQP'
        address = 'gHAXa8zgoJJ4cyJbrdt6LxuwJaU3oTqouv'
        kp = Keypair.from_base58_seed(seed)
        assert kp.to_old_address() == address
        assert kp.to_old_seed() == seed


class Sep0005Test(TestCase):
    # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
    @classmethod
    def setUpClass(cls):
        cls.case_data = (
            # Test 1 Mnemonic (12 words):
            {'mnemonic': 'illness spike retreat truth genius clock brain pass fit cave bargain toe',
             'passphrase': '',
             'accounts': (('GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6',
                           'SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN'),
                          ('GBAW5XGWORWVFE2XTJYDTLDHXTY2Q2MO73HYCGB3XMFMQ562Q2W2GJQX',
                           'SCEPFFWGAG5P2VX5DHIYK3XEMZYLTYWIPWYEKXFHSK25RVMIUNJ7CTIS'),
                          ('GAY5PRAHJ2HIYBYCLZXTHID6SPVELOOYH2LBPH3LD4RUMXUW3DOYTLXW',
                           'SDAILLEZCSA67DUEP3XUPZJ7NYG7KGVRM46XA7K5QWWUIGADUZCZWTJP'),
                          ('GAOD5NRAEORFE34G5D4EOSKIJB6V4Z2FGPBCJNQI6MNICVITE6CSYIAE',
                           'SBMWLNV75BPI2VB4G27RWOMABVRTSSF7352CCYGVELZDSHCXWCYFKXIX'),
                          ('GBCUXLFLSL2JE3NWLHAWXQZN6SQC6577YMAU3M3BEMWKYPFWXBSRCWV4',
                           'SCPCY3CEHMOP2TADSV2ERNNZBNHBGP4V32VGOORIEV6QJLXD5NMCJUXI'),
                          ('GBRQY5JFN5UBG5PGOSUOL4M6D7VRMAYU6WW2ZWXBMCKB7GPT3YCBU2XZ',
                           'SCK27SFHI3WUDOEMJREV7ZJQG34SCBR6YWCE6OLEXUS2VVYTSNGCRS6X'),
                          ('GBY27SJVFEWR3DUACNBSMJB6T4ZPR4C7ZXSTHT6GMZUDL23LAM5S2PQX',
                           'SDJ4WDPOQAJYR3YIAJOJP3E6E4BMRB7VZ4QAEGCP7EYVDW6NQD3LRJMZ'),
                          ('GAY7T23Z34DWLSTEAUKVBPHHBUE4E3EMZBAQSLV6ZHS764U3TKUSNJOF',
                           'SA3HXJUCE2N27TBIZ5JRBLEBF3TLPQEBINP47E6BTMIWW2RJ5UKR2B3L'),
                          ('GDJTCF62UUYSAFAVIXHPRBR4AUZV6NYJR75INVDXLLRZLZQ62S44443R',
                           'SCD5OSHUUC75MSJG44BAT3HFZL2HZMMQ5M4GPDL7KA6HJHV3FLMUJAME'),
                          ('GBTVYYDIYWGUQUTKX6ZMLGSZGMTESJYJKJWAATGZGITA25ZB6T5REF44',
                           'SCJGVMJ66WAUHQHNLMWDFGY2E72QKSI3XGSBYV6BANDFUFE7VY4XNXXR'))},
            # Test 2 Mnemonic (15 words):
            {
                'mnemonic': 'resource asthma orphan phone ice canvas fire useful arch jewel impose vague theory cushion top',
                'passphrase': '',
                'accounts': (('GAVXVW5MCK7Q66RIBWZZKZEDQTRXWCZUP4DIIFXCCENGW2P6W4OA34RH',
                              'SAKS7I2PNDBE5SJSUSU2XLJ7K5XJ3V3K4UDFAHMSBQYPOKE247VHAGDB'),
                             ('GDFCYVCICATX5YPJUDS22KM2GW5QU2KKSPPPT2IC5AQIU6TP3BZSLR5K',
                              'SAZ2H5GLAVWCUWNPQMB6I3OHRI63T2ACUUAWSH7NAGYYPXGIOPLPW3Q4'),
                             ('GAUA3XK3SGEQFNCBM423WIM5WCZ4CR4ZDPDFCYSFLCTODGGGJMPOHAAE',
                              'SDVSSLPL76I33DKAI4LFTOAKCHJNCXUERGPCMVFT655Z4GRLWM6ZZTSC'),
                             ('GAH3S77QXTAPZ77REY6LGFIJ2XWVXFOKXHCFLA6HQTL3POLVZJDHHUDM',
                              'SCH56YSGOBYVBC6DO3ZI2PY62GBVXT4SEJSXJOBQYGC2GCEZSB5PEVBZ'),
                             ('GCSCZVGV2Y3EQ2RATJ7TE6PVWTW5OH5SMG754AF6W6YM3KJF7RMNPB4Y',
                              'SBWBM73VUNBGBMFD4E2BA7Q756AKVEAAVTQH34RYEUFD6X64VYL5KXQ2'),
                             ('GDKWYAJE3W6PWCXDZNMFNFQSPTF6BUDANE6OVRYMJKBYNGL62VKKCNCC',
                              'SAVS4CDQZI6PSA5DPCC42S5WLKYIPKXPCJSFYY4N3VDK25T2XX2BTGVX'),
                             ('GCDTVB4XDLNX22HI5GUWHBXJFBCPB6JNU6ZON7E57FA3LFURS74CWDJH',
                              'SDFC7WZT3GDQVQUQMXN7TC7UWDW5E3GSMFPHUT2TSTQ7RKWTRA4PLBAL'),
                             ('GBTDPL5S4IOUQHDLCZ7I2UXJ2TEHO6DYIQ3F2P5OOP3IS7JSJI4UMHQJ',
                              'SA6UO2FIYC6AS2MSDECLR6F7NKCJTG67F7R4LV2GYB4HCZYXJZRLPOBB'),
                             ('GD3KWA24OIM7V3MZKDAVSLN3NBHGKVURNJ72ZCTAJSDTF7RIGFXPW5FQ',
                              'SBDNHDDICLLMBIDZ2IF2D3LH44OVUGGAVHQVQ6BZQI5IQO6AB6KNJCOV'),
                             ('GB3C6RRQB3V7EPDXEDJCMTS45LVDLSZQ46PTIGKZUY37DXXEOAKJIWSV',
                              'SDHRG2J34MGDAYHMOVKVJC6LX2QZMCTIKRO5I4JQ6BJQ36KVL6QUTT72'))},
            # Test 3 Mnemonic (24 words):
            {
                'mnemonic': 'bench hurt jump file august wise shallow faculty impulse spring exact slush thunder author capable act festival slice deposit sauce coconut afford frown better',
                'passphrase': '',
                'accounts': (('GC3MMSXBWHL6CPOAVERSJITX7BH76YU252WGLUOM5CJX3E7UCYZBTPJQ',
                              'SAEWIVK3VLNEJ3WEJRZXQGDAS5NVG2BYSYDFRSH4GKVTS5RXNVED5AX7'),
                             ('GB3MTYFXPBZBUINVG72XR7AQ6P2I32CYSXWNRKJ2PV5H5C7EAM5YYISO',
                              'SBKSABCPDWXDFSZISAVJ5XKVIEWV4M5O3KBRRLSPY3COQI7ZP423FYB4'),
                             ('GDYF7GIHS2TRGJ5WW4MZ4ELIUIBINRNYPPAWVQBPLAZXC2JRDI4DGAKU',
                              'SD5CCQAFRIPB3BWBHQYQ5SC66IB2AVMFNWWPBYGSUXVRZNCIRJ7IHESQ'),
                             ('GAFLH7DGM3VXFVUID7JUKSGOYG52ZRAQPZHQASVCEQERYC5I4PPJUWBD',
                              'SBSGSAIKEF7JYQWQSGXKB4SRHNSKDXTEI33WZDRR6UHYQCQ5I6ZGZQPK'),
                             ('GAXG3LWEXWCAWUABRO6SMAEUKJXLB5BBX6J2KMHFRIWKAMDJKCFGS3NN',
                              'SBIZH53PIRFTPI73JG7QYA3YAINOAT2XMNAUARB3QOWWVZVBAROHGXWM'),
                             ('GA6RUD4DZ2NEMAQY4VZJ4C6K6VSEYEJITNSLUQKLCFHJ2JOGC5UCGCFQ',
                              'SCVM6ZNVRUOP4NMCMMKLTVBEMAF2THIOMHPYSSMPCD2ZU7VDPARQQ6OY'),
                             ('GCUDW6ZF5SCGCMS3QUTELZ6LSAH6IVVXNRPRLAUNJ2XYLCA7KH7ZCVQS',
                              'SBSHUZQNC45IAIRSAHMWJEJ35RY7YNW6SMOEBZHTMMG64NKV7Y52ZEO2'),
                             ('GBJ646Q524WGBN5X5NOAPIF5VQCR2WZCN6QZIDOSY6VA2PMHJ2X636G4',
                              'SC2QO2K2B4EBNBJMBZIKOYSHEX4EZAZNIF4UNLH63AQYV6BE7SMYWC6E'),
                             ('GDHX4LU6YBSXGYTR7SX2P4ZYZSN24VXNJBVAFOB2GEBKNN3I54IYSRM4',
                              'SCGMC5AHAAVB3D4JXQPCORWW37T44XJZUNPEMLRW6DCOEARY3H5MAQST'),
                             ('GDXOY6HXPIDT2QD352CH7VWX257PHVFR72COWQ74QE3TEV4PK2KCKZX7',
                              'SCPA5OX4EYINOPAUEQCPY6TJMYICUS5M7TVXYKWXR3G5ZRAJXY3C37GF'))},
            # Test 4 Mnemonic (24 words + BIP 39 passphrase):
            {
                'mnemonic': 'cable spray genius state float twenty onion head street palace net private method loan turn phrase state blanket interest dry amazing dress blast tube',
                'passphrase': 'p4ssphr4se',
                'accounts': (('GDAHPZ2NSYIIHZXM56Y36SBVTV5QKFIZGYMMBHOU53ETUSWTP62B63EQ',
                              'SAFWTGXVS7ELMNCXELFWCFZOPMHUZ5LXNBGUVRCY3FHLFPXK4QPXYP2X'),
                             ('GDY47CJARRHHL66JH3RJURDYXAMIQ5DMXZLP3TDAUJ6IN2GUOFX4OJOC',
                              'SBQPDFUGLMWJYEYXFRM5TQX3AX2BR47WKI4FDS7EJQUSEUUVY72MZPJF'),
                             ('GCLAQF5H5LGJ2A6ACOMNEHSWYDJ3VKVBUBHDWFGRBEPAVZ56L4D7JJID',
                              'SAF2LXRW6FOSVQNC4HHIIDURZL4SCGCG7UEGG23ZQG6Q2DKIGMPZV6BZ'),
                             ('GBC36J4KG7ZSIQ5UOSJFQNUP4IBRN6LVUFAHQWT2ODEQ7Y3ASWC5ZN3B',
                              'SDCCVBIYZDMXOR4VPC3IYMIPODNEDZCS44LDN7B5ZWECIE57N3BTV4GQ'),
                             ('GA6NHA4KPH5LFYD6LZH35SIX3DU5CWU3GX6GCKPJPPTQCCQPP627E3CB',
                              'SA5TRXTO7BG2Z6QTQT3O2LC7A7DLZZ2RBTGUNCTG346PLVSSHXPNDVNT'),
                             ('GBOWMXTLABFNEWO34UJNSJJNVEF6ESLCNNS36S5SX46UZT2MNYJOLA5L',
                              'SDEOED2KPHV355YNOLLDLVQB7HDPQVIGKXCAJMA3HTM4325ZHFZSKKUC'),
                             ('GBL3F5JUZN3SQKZ7SL4XSXEJI2SNSVGO6WZWNJLG666WOJHNDDLEXTSZ',
                              'SDYNO6TLFNV3IM6THLNGUG5FII4ET2H7NH3KCT6OAHIUSHKR4XBEEI6A'),
                             ('GA5XPPWXL22HFFL5K5CE37CEPUHXYGSP3NNWGM6IK6K4C3EFHZFKSAND',
                              'SDXMJXAY45W3WEFWMYEPLPIF4CXAD5ECQ37XKMGY5EKLM472SSRJXCYD'),
                             ('GDS5I7L7LWFUVSYVAOHXJET2565MGGHJ4VHGVJXIKVKNO5D4JWXIZ3XU',
                              'SAIZA26BUP55TDCJ4U7I2MSQEAJDPDSZSBKBPWQTD5OQZQSJAGNN2IQB'),
                             ('GBOSMFQYKWFDHJWCMCZSMGUMWCZOM4KFMXXS64INDHVCJ2A2JAABCYRR',
                              'SDXDYPDNRMGOF25AWYYKPHFAD3M54IT7LCLG7RWTGR3TS32A4HTUXNOS'))},
            # Test 5 Mnemonic (12 words - entropy bytes: 00000000000000000000000000000000):
            {
                'mnemonic': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about',
                'passphrase': '',
                'accounts': (('GB3JDWCQJCWMJ3IILWIGDTQJJC5567PGVEVXSCVPEQOTDN64VJBDQBYX',
                              'SBUV3MRWKNS6AYKZ6E6MOUVF2OYMON3MIUASWL3JLY5E3ISDJFELYBRZ'),
                             ('GDVSYYTUAJ3ACHTPQNSTQBDQ4LDHQCMNY4FCEQH5TJUMSSLWQSTG42MV',
                              'SCHDCVCWGAKGIMTORV6K5DYYV3BY4WG3RA4M6MCBGJLHUCWU2MC6DL66'),
                             ('GBFPWBTN4AXHPWPTQVQBP4KRZ2YVYYOGRMV2PEYL2OBPPJDP7LECEVHR',
                              'SAPLVTLUXSDLFRDGCCFLPDZMTCEVMP3ZXTM74EBJCVKZKM34LGQPF7K3'),
                             ('GCCCOWAKYVFY5M6SYHOW33TSNC7Z5IBRUEU2XQVVT34CIZU7CXZ4OQ4O',
                              'SDQYXOP2EAUZP4YOEQ5BUJIQ3RDSP5XV4ZFI6C5Y3QCD5Y63LWPXT7PW'),
                             ('GCQ3J35MKPKJX7JDXRHC5YTXTULFMCBMZ5IC63EDR66QA3LO7264ZL7Q',
                              'SCT7DUHYZD6DRCETT6M73GWKFJI4D56P3SNWNWNJ7ANLJZS6XIFYYXSB'),
                             ('GDTA7622ZA5PW7F7JL7NOEFGW62M7GW2GY764EQC2TUJ42YJQE2A3QUL',
                              'SDTWG5AFDI6GRQNLPWOC7IYS7AKOGMI2GX4OXTBTZHHYPMNZ2PX4ONWU'),
                             ('GD7A7EACTPTBCYCURD43IEZXGIBCEXNBHN3OFWV2FOX67XKUIGRCTBNU',
                              'SDJMWY4KFRS4PTA5WBFVCPS2GKYLXOMCLQSBNEIBG7KRGHNQOM25KMCP'),
                             ('GAF4AGPVLQXFKEWQV3DZU5YEFU6YP7XJHAEEQH4G3R664MSF77FLLRK3',
                              'SDOJH5JRCNGT57QTPTJEQGBEBZJPXE7XUDYDB24VTOPP7PH3ALKHAHFG'),
                             ('GABTYCZJMCP55SS6I46SR76IHETZDLG4L37MLZRZKQDGBLS5RMP65TSX',
                              'SC6N6GYQ2VA4T7CUP2BWGBRT2P6L2HQSZIUNQRHNDLISF6ND7TW4P4ER'),
                             ('GAKFARYSPI33KUJE7HYLT47DCX2PFWJ77W3LZMRBPSGPGYPMSDBE7W7X',
                              'SALJ5LPBTXCFML2CQ7ORP7WJNJOZSVBVRQAAODMVHMUF4P4XXFZB7MKY'))}
        )

    def test_sep0005(self):
        for data in self.case_data:
            for i in range(len(data['accounts'])):
                kp = Keypair.deterministic(mnemonic=data['mnemonic'], passphrase=data['passphrase'], index=i)
                assert data['accounts'][i] == (kp.address().decode(), kp.seed().decode())
