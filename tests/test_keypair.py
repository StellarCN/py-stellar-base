import itertools

import pytest
import shamir_mnemonic

from stellar_sdk import Keypair, StrKey
from stellar_sdk.exceptions import (
    BadSignatureError,
    Ed25519PublicKeyInvalidError,
    Ed25519SecretSeedInvalidError,
    MissingEd25519SecretSeedError,
)
from stellar_sdk.sep.mnemonic import Language, StellarMnemonic

SEP_5_CASES = (
    {
        "mnemonic": "illness spike retreat truth genius clock brain pass fit cave bargain toe",
        "passphrase": "",
        "accounts": (
            (
                "GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6",
                "SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN",
            ),
            (
                "GBAW5XGWORWVFE2XTJYDTLDHXTY2Q2MO73HYCGB3XMFMQ562Q2W2GJQX",
                "SCEPFFWGAG5P2VX5DHIYK3XEMZYLTYWIPWYEKXFHSK25RVMIUNJ7CTIS",
            ),
            (
                "GAY5PRAHJ2HIYBYCLZXTHID6SPVELOOYH2LBPH3LD4RUMXUW3DOYTLXW",
                "SDAILLEZCSA67DUEP3XUPZJ7NYG7KGVRM46XA7K5QWWUIGADUZCZWTJP",
            ),
            (
                "GAOD5NRAEORFE34G5D4EOSKIJB6V4Z2FGPBCJNQI6MNICVITE6CSYIAE",
                "SBMWLNV75BPI2VB4G27RWOMABVRTSSF7352CCYGVELZDSHCXWCYFKXIX",
            ),
            (
                "GBCUXLFLSL2JE3NWLHAWXQZN6SQC6577YMAU3M3BEMWKYPFWXBSRCWV4",
                "SCPCY3CEHMOP2TADSV2ERNNZBNHBGP4V32VGOORIEV6QJLXD5NMCJUXI",
            ),
            (
                "GBRQY5JFN5UBG5PGOSUOL4M6D7VRMAYU6WW2ZWXBMCKB7GPT3YCBU2XZ",
                "SCK27SFHI3WUDOEMJREV7ZJQG34SCBR6YWCE6OLEXUS2VVYTSNGCRS6X",
            ),
            (
                "GBY27SJVFEWR3DUACNBSMJB6T4ZPR4C7ZXSTHT6GMZUDL23LAM5S2PQX",
                "SDJ4WDPOQAJYR3YIAJOJP3E6E4BMRB7VZ4QAEGCP7EYVDW6NQD3LRJMZ",
            ),
            (
                "GAY7T23Z34DWLSTEAUKVBPHHBUE4E3EMZBAQSLV6ZHS764U3TKUSNJOF",
                "SA3HXJUCE2N27TBIZ5JRBLEBF3TLPQEBINP47E6BTMIWW2RJ5UKR2B3L",
            ),
            (
                "GDJTCF62UUYSAFAVIXHPRBR4AUZV6NYJR75INVDXLLRZLZQ62S44443R",
                "SCD5OSHUUC75MSJG44BAT3HFZL2HZMMQ5M4GPDL7KA6HJHV3FLMUJAME",
            ),
            (
                "GBTVYYDIYWGUQUTKX6ZMLGSZGMTESJYJKJWAATGZGITA25ZB6T5REF44",
                "SCJGVMJ66WAUHQHNLMWDFGY2E72QKSI3XGSBYV6BANDFUFE7VY4XNXXR",
            ),
        ),
    },
    {
        "mnemonic": "resource asthma orphan phone ice canvas fire useful arch jewel impose vague theory cushion top",
        "passphrase": "",
        "accounts": (
            (
                "GAVXVW5MCK7Q66RIBWZZKZEDQTRXWCZUP4DIIFXCCENGW2P6W4OA34RH",
                "SAKS7I2PNDBE5SJSUSU2XLJ7K5XJ3V3K4UDFAHMSBQYPOKE247VHAGDB",
            ),
            (
                "GDFCYVCICATX5YPJUDS22KM2GW5QU2KKSPPPT2IC5AQIU6TP3BZSLR5K",
                "SAZ2H5GLAVWCUWNPQMB6I3OHRI63T2ACUUAWSH7NAGYYPXGIOPLPW3Q4",
            ),
            (
                "GAUA3XK3SGEQFNCBM423WIM5WCZ4CR4ZDPDFCYSFLCTODGGGJMPOHAAE",
                "SDVSSLPL76I33DKAI4LFTOAKCHJNCXUERGPCMVFT655Z4GRLWM6ZZTSC",
            ),
            (
                "GAH3S77QXTAPZ77REY6LGFIJ2XWVXFOKXHCFLA6HQTL3POLVZJDHHUDM",
                "SCH56YSGOBYVBC6DO3ZI2PY62GBVXT4SEJSXJOBQYGC2GCEZSB5PEVBZ",
            ),
            (
                "GCSCZVGV2Y3EQ2RATJ7TE6PVWTW5OH5SMG754AF6W6YM3KJF7RMNPB4Y",
                "SBWBM73VUNBGBMFD4E2BA7Q756AKVEAAVTQH34RYEUFD6X64VYL5KXQ2",
            ),
            (
                "GDKWYAJE3W6PWCXDZNMFNFQSPTF6BUDANE6OVRYMJKBYNGL62VKKCNCC",
                "SAVS4CDQZI6PSA5DPCC42S5WLKYIPKXPCJSFYY4N3VDK25T2XX2BTGVX",
            ),
            (
                "GCDTVB4XDLNX22HI5GUWHBXJFBCPB6JNU6ZON7E57FA3LFURS74CWDJH",
                "SDFC7WZT3GDQVQUQMXN7TC7UWDW5E3GSMFPHUT2TSTQ7RKWTRA4PLBAL",
            ),
            (
                "GBTDPL5S4IOUQHDLCZ7I2UXJ2TEHO6DYIQ3F2P5OOP3IS7JSJI4UMHQJ",
                "SA6UO2FIYC6AS2MSDECLR6F7NKCJTG67F7R4LV2GYB4HCZYXJZRLPOBB",
            ),
            (
                "GD3KWA24OIM7V3MZKDAVSLN3NBHGKVURNJ72ZCTAJSDTF7RIGFXPW5FQ",
                "SBDNHDDICLLMBIDZ2IF2D3LH44OVUGGAVHQVQ6BZQI5IQO6AB6KNJCOV",
            ),
            (
                "GB3C6RRQB3V7EPDXEDJCMTS45LVDLSZQ46PTIGKZUY37DXXEOAKJIWSV",
                "SDHRG2J34MGDAYHMOVKVJC6LX2QZMCTIKRO5I4JQ6BJQ36KVL6QUTT72",
            ),
        ),
    },
    {
        "mnemonic": "bench hurt jump file august wise shallow faculty impulse spring exact slush thunder author capable act festival slice deposit sauce coconut afford frown better",
        "passphrase": "",
        "accounts": (
            (
                "GC3MMSXBWHL6CPOAVERSJITX7BH76YU252WGLUOM5CJX3E7UCYZBTPJQ",
                "SAEWIVK3VLNEJ3WEJRZXQGDAS5NVG2BYSYDFRSH4GKVTS5RXNVED5AX7",
            ),
            (
                "GB3MTYFXPBZBUINVG72XR7AQ6P2I32CYSXWNRKJ2PV5H5C7EAM5YYISO",
                "SBKSABCPDWXDFSZISAVJ5XKVIEWV4M5O3KBRRLSPY3COQI7ZP423FYB4",
            ),
            (
                "GDYF7GIHS2TRGJ5WW4MZ4ELIUIBINRNYPPAWVQBPLAZXC2JRDI4DGAKU",
                "SD5CCQAFRIPB3BWBHQYQ5SC66IB2AVMFNWWPBYGSUXVRZNCIRJ7IHESQ",
            ),
            (
                "GAFLH7DGM3VXFVUID7JUKSGOYG52ZRAQPZHQASVCEQERYC5I4PPJUWBD",
                "SBSGSAIKEF7JYQWQSGXKB4SRHNSKDXTEI33WZDRR6UHYQCQ5I6ZGZQPK",
            ),
            (
                "GAXG3LWEXWCAWUABRO6SMAEUKJXLB5BBX6J2KMHFRIWKAMDJKCFGS3NN",
                "SBIZH53PIRFTPI73JG7QYA3YAINOAT2XMNAUARB3QOWWVZVBAROHGXWM",
            ),
            (
                "GA6RUD4DZ2NEMAQY4VZJ4C6K6VSEYEJITNSLUQKLCFHJ2JOGC5UCGCFQ",
                "SCVM6ZNVRUOP4NMCMMKLTVBEMAF2THIOMHPYSSMPCD2ZU7VDPARQQ6OY",
            ),
            (
                "GCUDW6ZF5SCGCMS3QUTELZ6LSAH6IVVXNRPRLAUNJ2XYLCA7KH7ZCVQS",
                "SBSHUZQNC45IAIRSAHMWJEJ35RY7YNW6SMOEBZHTMMG64NKV7Y52ZEO2",
            ),
            (
                "GBJ646Q524WGBN5X5NOAPIF5VQCR2WZCN6QZIDOSY6VA2PMHJ2X636G4",
                "SC2QO2K2B4EBNBJMBZIKOYSHEX4EZAZNIF4UNLH63AQYV6BE7SMYWC6E",
            ),
            (
                "GDHX4LU6YBSXGYTR7SX2P4ZYZSN24VXNJBVAFOB2GEBKNN3I54IYSRM4",
                "SCGMC5AHAAVB3D4JXQPCORWW37T44XJZUNPEMLRW6DCOEARY3H5MAQST",
            ),
            (
                "GDXOY6HXPIDT2QD352CH7VWX257PHVFR72COWQ74QE3TEV4PK2KCKZX7",
                "SCPA5OX4EYINOPAUEQCPY6TJMYICUS5M7TVXYKWXR3G5ZRAJXY3C37GF",
            ),
        ),
    },
    {
        "mnemonic": "cable spray genius state float twenty onion head street palace net private method loan turn phrase state blanket interest dry amazing dress blast tube",
        "passphrase": "p4ssphr4se",
        "accounts": (
            (
                "GDAHPZ2NSYIIHZXM56Y36SBVTV5QKFIZGYMMBHOU53ETUSWTP62B63EQ",
                "SAFWTGXVS7ELMNCXELFWCFZOPMHUZ5LXNBGUVRCY3FHLFPXK4QPXYP2X",
            ),
            (
                "GDY47CJARRHHL66JH3RJURDYXAMIQ5DMXZLP3TDAUJ6IN2GUOFX4OJOC",
                "SBQPDFUGLMWJYEYXFRM5TQX3AX2BR47WKI4FDS7EJQUSEUUVY72MZPJF",
            ),
            (
                "GCLAQF5H5LGJ2A6ACOMNEHSWYDJ3VKVBUBHDWFGRBEPAVZ56L4D7JJID",
                "SAF2LXRW6FOSVQNC4HHIIDURZL4SCGCG7UEGG23ZQG6Q2DKIGMPZV6BZ",
            ),
            (
                "GBC36J4KG7ZSIQ5UOSJFQNUP4IBRN6LVUFAHQWT2ODEQ7Y3ASWC5ZN3B",
                "SDCCVBIYZDMXOR4VPC3IYMIPODNEDZCS44LDN7B5ZWECIE57N3BTV4GQ",
            ),
            (
                "GA6NHA4KPH5LFYD6LZH35SIX3DU5CWU3GX6GCKPJPPTQCCQPP627E3CB",
                "SA5TRXTO7BG2Z6QTQT3O2LC7A7DLZZ2RBTGUNCTG346PLVSSHXPNDVNT",
            ),
            (
                "GBOWMXTLABFNEWO34UJNSJJNVEF6ESLCNNS36S5SX46UZT2MNYJOLA5L",
                "SDEOED2KPHV355YNOLLDLVQB7HDPQVIGKXCAJMA3HTM4325ZHFZSKKUC",
            ),
            (
                "GBL3F5JUZN3SQKZ7SL4XSXEJI2SNSVGO6WZWNJLG666WOJHNDDLEXTSZ",
                "SDYNO6TLFNV3IM6THLNGUG5FII4ET2H7NH3KCT6OAHIUSHKR4XBEEI6A",
            ),
            (
                "GA5XPPWXL22HFFL5K5CE37CEPUHXYGSP3NNWGM6IK6K4C3EFHZFKSAND",
                "SDXMJXAY45W3WEFWMYEPLPIF4CXAD5ECQ37XKMGY5EKLM472SSRJXCYD",
            ),
            (
                "GDS5I7L7LWFUVSYVAOHXJET2565MGGHJ4VHGVJXIKVKNO5D4JWXIZ3XU",
                "SAIZA26BUP55TDCJ4U7I2MSQEAJDPDSZSBKBPWQTD5OQZQSJAGNN2IQB",
            ),
            (
                "GBOSMFQYKWFDHJWCMCZSMGUMWCZOM4KFMXXS64INDHVCJ2A2JAABCYRR",
                "SDXDYPDNRMGOF25AWYYKPHFAD3M54IT7LCLG7RWTGR3TS32A4HTUXNOS",
            ),
        ),
    },
    {
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        "passphrase": "",
        "accounts": (
            (
                "GB3JDWCQJCWMJ3IILWIGDTQJJC5567PGVEVXSCVPEQOTDN64VJBDQBYX",
                "SBUV3MRWKNS6AYKZ6E6MOUVF2OYMON3MIUASWL3JLY5E3ISDJFELYBRZ",
            ),
            (
                "GDVSYYTUAJ3ACHTPQNSTQBDQ4LDHQCMNY4FCEQH5TJUMSSLWQSTG42MV",
                "SCHDCVCWGAKGIMTORV6K5DYYV3BY4WG3RA4M6MCBGJLHUCWU2MC6DL66",
            ),
            (
                "GBFPWBTN4AXHPWPTQVQBP4KRZ2YVYYOGRMV2PEYL2OBPPJDP7LECEVHR",
                "SAPLVTLUXSDLFRDGCCFLPDZMTCEVMP3ZXTM74EBJCVKZKM34LGQPF7K3",
            ),
            (
                "GCCCOWAKYVFY5M6SYHOW33TSNC7Z5IBRUEU2XQVVT34CIZU7CXZ4OQ4O",
                "SDQYXOP2EAUZP4YOEQ5BUJIQ3RDSP5XV4ZFI6C5Y3QCD5Y63LWPXT7PW",
            ),
            (
                "GCQ3J35MKPKJX7JDXRHC5YTXTULFMCBMZ5IC63EDR66QA3LO7264ZL7Q",
                "SCT7DUHYZD6DRCETT6M73GWKFJI4D56P3SNWNWNJ7ANLJZS6XIFYYXSB",
            ),
            (
                "GDTA7622ZA5PW7F7JL7NOEFGW62M7GW2GY764EQC2TUJ42YJQE2A3QUL",
                "SDTWG5AFDI6GRQNLPWOC7IYS7AKOGMI2GX4OXTBTZHHYPMNZ2PX4ONWU",
            ),
            (
                "GD7A7EACTPTBCYCURD43IEZXGIBCEXNBHN3OFWV2FOX67XKUIGRCTBNU",
                "SDJMWY4KFRS4PTA5WBFVCPS2GKYLXOMCLQSBNEIBG7KRGHNQOM25KMCP",
            ),
            (
                "GAF4AGPVLQXFKEWQV3DZU5YEFU6YP7XJHAEEQH4G3R664MSF77FLLRK3",
                "SDOJH5JRCNGT57QTPTJEQGBEBZJPXE7XUDYDB24VTOPP7PH3ALKHAHFG",
            ),
            (
                "GABTYCZJMCP55SS6I46SR76IHETZDLG4L37MLZRZKQDGBLS5RMP65TSX",
                "SC6N6GYQ2VA4T7CUP2BWGBRT2P6L2HQSZIUNQRHNDLISF6ND7TW4P4ER",
            ),
            (
                "GAKFARYSPI33KUJE7HYLT47DCX2PFWJ77W3LZMRBPSGPGYPMSDBE7W7X",
                "SALJ5LPBTXCFML2CQ7ORP7WJNJOZSVBVRQAAODMVHMUF4P4XXFZB7MKY",
            ),
        ),
    },
)


class TestKeypair:
    def test_create_random(self):
        kp = Keypair.random()
        public_key = kp.public_key
        secret = kp.secret
        assert StrKey.is_valid_ed25519_public_key(public_key)
        assert StrKey.is_valid_ed25519_secret_seed(secret)
        assert kp.can_sign() is True

    def test_create_from_secret(self):
        secret = "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        kp = Keypair.from_secret(secret)
        assert isinstance(kp, Keypair)
        assert (
            kp.public_key == "GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7"
        )
        assert kp.secret == secret

    @pytest.mark.parametrize(
        "invalid_secret",
        [
            "",
            "hello",
            "SBWUBZ3SIPLLF5CCXLWUB2Z6UBTYAW34KVXOLRQ5HDAZG4ZY7MHNBWJ1",
            "masterpassphrasemasterpassphrase",
            "gsYRSEQhTffqA9opPepAENCr2WG6z5iBHHubxxbRzWaHf8FBWcu",
        ],
    )
    def test_create_from_invalid_secret_raise(self, invalid_secret):
        with pytest.raises(
            Ed25519SecretSeedInvalidError,
            match="Invalid Ed25519 Secret Seed: {}".format(invalid_secret),
        ):
            Keypair.from_secret(invalid_secret)

    def test_create_from_public_key(self):
        public_key = "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        kp = Keypair.from_public_key(public_key)
        assert isinstance(kp, Keypair)
        assert (
            kp.public_key == "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        assert (
            kp.raw_public_key().hex()
            == "2e3c35010749c1de3d9a5bdd6a31c12458768da5ce87cca6aad63ebbaaef7432"
        )

    @pytest.mark.parametrize(
        "invalid_public_key",
        [
            "",
            "hello" "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DFBAD",
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5Z"
            "masterpassphrasemasterpassphrase",
            "gsYRSEQhTffqA9opPepAENCr2WG6z5iBHHubxxbRzWaHf8FBWcu",
        ],
    )
    def test_create_from_invalid_public_key_raise(self, invalid_public_key):
        with pytest.raises(
            Ed25519PublicKeyInvalidError,
            match="Invalid Ed25519 Public Key: {}".format(invalid_public_key),
        ):
            Keypair.from_public_key(invalid_public_key)

    def test_can_sign(self):
        can_sign_kp = Keypair.from_secret(
            "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        )
        can_not_sign_kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        assert can_sign_kp.can_sign() is True
        assert can_not_sign_kp.can_sign() is False

    def test_sign_without_secret_raise(self):
        data = b"Hello, Stellar!"
        can_not_sign_kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        with pytest.raises(
            MissingEd25519SecretSeedError,
            match="The keypair does not contain secret seed. Use Keypair.from_secret, "
            "Keypair.random or Keypair.from_mnemonic_phrase to create a new keypair with a secret seed.",
        ):
            can_not_sign_kp.sign(data)

    def test_get_raw_secret_key_without_secret_raise(self):
        can_not_sign_kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        with pytest.raises(
            MissingEd25519SecretSeedError,
            match="The keypair does not contain secret seed. Use Keypair.from_secret, "
            "Keypair.random or Keypair.from_mnemonic_phrase to create a new keypair with a secret seed.",
        ):
            can_not_sign_kp.raw_secret_key()

    def test_sign_and_verify(self):
        kp = Keypair.from_secret(
            "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B"
        )
        data = b"Hello, overcat!"
        signature = kp.sign(data)
        assert (
            signature.hex()
            == "ff7c4346977144019e7be0c12c033e99f412e70361924e298e6152dd924c88f2"
            "725c60c56067f20c35a8ff29c936b983f652b4df2d9de8f2851605df2f680c06"
        )
        kp.verify(data, signature)

    def test_verify_failed_raise(self):
        kp = Keypair.from_secret(
            "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B"
        )
        data = b"Hello, Stellar!"
        signature = kp.sign(data)
        with pytest.raises(BadSignatureError, match="Signature verification failed."):
            kp.verify(data, signature + b"failed")
        with pytest.raises(BadSignatureError, match="Signature verification failed."):
            kp.verify(b"test_verify_failed", signature)

    @pytest.mark.parametrize(
        "secret, hint",
        [
            ("SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36", "0bfad134"),
            ("SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B", "4ab84399"),
            ("SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6", "091e5da1"),
        ],
    )
    def test_signature_hint_with_secret(self, secret, hint):
        assert Keypair.from_secret(secret).signature_hint().hex() == hint

    @pytest.mark.parametrize(
        "public_key, hint",
        [
            ("GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7", "0bfad134"),
            ("GD4UGX3TOGNPUOFHT64JR65P6CYIEGDOJKY234UGCNMB2ASKXBBZTAM6", "4ab84399"),
            ("GBRF6PKZYP4J4WI2A3NF4CGF23SL34GRKA5LTQZCQFEUT2YJDZO2COXH", "091e5da1"),
        ],
    )
    def test_signature_hint_with_public_key(self, public_key, hint):
        assert Keypair.from_public_key(public_key).signature_hint().hex() == hint

    def test_read_secret_without_secret_raise(self):
        kp = Keypair.from_public_key(
            "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"
        )
        with pytest.raises(MissingEd25519SecretSeedError):
            _ = kp.secret

    def test_set_keypair_secret_raise(self):
        secret = "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        kp = Keypair.from_secret(secret)
        with pytest.raises(
            AttributeError,
            match="Please use `Keypair.from_secret` to generate a new Keypair object.",
        ):
            kp.secret = "SAMWF63FZ5ZNHY75SNYNAFMWTL5FPBMIV7DLB3UDAVLL7DKPI5ZFS2S6"

        with pytest.raises(
            AttributeError,
            match="Please use `Keypair.from_public_key` to generate a new Keypair object.",
        ):
            kp.public_key = "GAXDYNIBA5E4DXR5TJN522RRYESFQ5UNUXHIPTFGVLLD5O5K552DF5ZH"

    @pytest.mark.parametrize(
        "kp1, kp2, equal",
        [
            (
                "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36",
                "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36",
                True,
            ),
            (
                "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B",
                "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36",
                False,
            ),
        ],
    )
    def test_equals(self, kp1, kp2, equal):
        kp1 = Keypair.from_secret(
            "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        )  # GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7
        kp2 = Keypair.from_secret(
            "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        )
        kp3 = Keypair.from_secret(
            "SAQVS3IPN6U3TBMTXQH32ZESY7SUOZGLEFBH6XWMA6DVNPJ4CLO5M54B"
        )
        kp4 = Keypair.from_public_key(
            "GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7"
        )
        kp5 = Keypair.from_public_key(
            "GDFQVQCYYB7GKCGSCUSIQYXTPLV5YJ3XWDMWGQMDNM4EAXAL7LITIBQ7"
        )
        kp6 = Keypair.from_public_key(
            "GD4UGX3TOGNPUOFHT64JR65P6CYIEGDOJKY234UGCNMB2ASKXBBZTAM6"
        )
        assert kp1 == kp2
        assert kp1 != kp3
        assert kp1 != kp4
        assert kp4 == kp5
        assert kp4 != kp6

    @pytest.mark.parametrize(
        "language, strength, length",
        [
            (Language.CHINESE_SIMPLIFIED, 128, 12),
            ("english", 128, 12),
            ("chinese_simplified", 128, 12),
            (Language.ENGLISH, 128, 12),
            (Language.ENGLISH, 160, 15),
            (Language.ENGLISH, 192, 18),
            (Language.ENGLISH, 224, 21),
            (Language.ENGLISH, 256, 24),
        ],
    )
    def test_generate_mnemonic_phrase(self, language, strength, length):
        # TODO: assert language type
        mnemonic_phrase = Keypair.generate_mnemonic_phrase(language, strength)
        assert len(mnemonic_phrase.split(" ")) == length

    def test_generate_mnemonic_phrase_unsupported_language_raise(self):
        with pytest.raises(ValueError, match="This language is not supported."):
            Keypair.generate_mnemonic_phrase("unsupported_language")

    def test_generate_mnemonic_phrase_invalid_strength_raise(self):
        strength = 1024
        with pytest.raises(
            ValueError,
            match=r"Strength should be one of the following \(128, 160, 192, 224, 256\), but it is not \(%d\)."
            % strength,
        ):
            Keypair.generate_mnemonic_phrase(strength=strength)

    def test_from_mnemonic_phrase(self):
        for data in SEP_5_CASES:
            for i in range(len(data["accounts"])):
                kp = Keypair.from_mnemonic_phrase(
                    mnemonic_phrase=data["mnemonic"],
                    passphrase=data["passphrase"],
                    index=i,
                )
                assert data["accounts"][i] == (kp.public_key, kp.secret)

    @pytest.mark.parametrize(
        "mnemonic, language",
        [
            (
                "usual canvas judge video wall ride rookie together enhance able evoke one",
                Language.CHINESE_SIMPLIFIED,
            ),
            (
                "invalid_mnemonic canvas judge video wall ride rookie together enhance able evoke one",
                Language.ENGLISH,
            ),
            (
                "usual canvas judge video wall ride rookie together enhance able evoke",
                Language.ENGLISH,
            ),
            (
                "胸泉谈新钉励确连球遇孤资氯递陪壤框碧折锋慌拖射潮",
                Language.CHINESE_SIMPLIFIED,
            ),
        ],
    )
    def test_invalid_mnemonic_raise(self, mnemonic, language):
        with pytest.raises(
            ValueError,
            match="Invalid mnemonic, please check if the mnemonic is correct, "
            "or if the language is set correctly.",
        ):
            assert Keypair.from_mnemonic_phrase(
                mnemonic_phrase=mnemonic, language=language
            )

    @pytest.mark.parametrize(
        "public_key, index",
        [
            (
                "GDZ4GYLVRLM2E6CGCOVYXAYMXJJAV3IHDXU6RUHX5AJVYS4AE6R6CHPJ",
                0,
            ),  # m/44h/148h/0h
            ("GCMZKXAAPQ3TDY5P7QDUVJBW66R2DGT7AM6MA3MCQENIF37E25U2PEK3", 1),
            ("GCF7DAVTXXVQPOSB5TCA2CIFT7DZIPK23NCOV3RJ6FTYTZM6S6RPPACM", 100),
        ],
    )
    def test_from_shamir_mnemonic_phrases(self, public_key, index):
        # generated from Trezor Safe 3
        shares = [
            "glimpse buyer academic acid branch sled disaster sunlight material junction float emperor intend priority scene trash remember radar prospect dryer",
            "glimpse buyer academic agency burden payroll alpha oven large amount smear forward pharmacy symbolic junk axle exercise segment frequent axle",
            "glimpse buyer academic always careful become dance teaspoon daisy orange careful steady boundary exceed robin remind software grin space advocate",
        ]
        passphrase = "9012"

        for perms in itertools.permutations(shares, 2):
            kp = Keypair.from_shamir_mnemonic_phrases(
                perms, index=index, passphrase=passphrase
            )
            assert kp.public_key == public_key

    def test_raise_from_shamir_mnemonic_phrases(self):
        shares = [
            "glimpse buyer academic acid branch sled disaster sunlight material junction float emperor intend priority scene trash remember radar prospect dryer",
            "glimpse buyer academic agency burden payroll alpha oven large amount smear forward pharmacy symbolic junk axle exercise segment frequent axle",
            "glimpse buyer academic always careful become dance teaspoon daisy orange careful steady boundary exceed robin remind software grin space advocate",
        ]
        _ = Keypair.from_shamir_mnemonic_phrases(shares[:-1])  # validate good run

        with pytest.raises(ValueError, match="Wrong number of mnemonics"):
            Keypair.from_shamir_mnemonic_phrases(shares)

        with pytest.raises(ValueError, match="Wrong number of mnemonics"):
            Keypair.from_shamir_mnemonic_phrases([shares[0]])

        with pytest.raises(ValueError, match="mnemonic word"):
            Keypair.from_shamir_mnemonic_phrases([shares[0], shares[1] + "a"])

        # remove first word
        shares_1 = "buyer academic agency burden payroll alpha oven large amount smear forward pharmacy symbolic junk axle exercise segment frequent axle"
        with pytest.raises(ValueError, match="mnemonic length"):
            Keypair.from_shamir_mnemonic_phrases([shares[0], shares_1])

        # another first word
        shares_1 = "acid buyer academic agency burden payroll alpha oven large amount smear forward pharmacy symbolic junk axle exercise segment frequent axle"
        with pytest.raises(ValueError, match="mnemonic checksum"):
            Keypair.from_shamir_mnemonic_phrases([shares[0], shares_1])

    @pytest.mark.parametrize(
        "member_threshold, member_count, strength, n_words, passphrase",
        [
            (1, 1, 128, 20, ""),
            (1, 1, 128, 20, "abcde"),
            (2, 3, 256, 33, "0"),
            (3, 4, 128, 20, ""),
        ],
    )
    def test_generate_shamir_mnemonic_phrases(
        self, member_threshold, member_count, strength, n_words, passphrase
    ):
        mnemonic_phrases = Keypair.generate_shamir_mnemonic_phrases(
            member_threshold=member_threshold,
            member_count=member_count,
            passphrase=passphrase,
            strength=strength,
        )

        assert len(mnemonic_phrases) == member_count
        for member in mnemonic_phrases:
            assert len(member.split(" ")) == n_words

        for perms in itertools.permutations(mnemonic_phrases, member_threshold):
            Keypair.from_shamir_mnemonic_phrases(
                mnemonic_phrases=perms, passphrase=passphrase
            )

    @pytest.mark.parametrize(
        "member_threshold, member_count, strength, err_msg",
        [
            (0, 1, 128, "threshold must be a positive"),
            (1, 2, 128, "multiple member shares with member threshold 1"),
            (2, 1, 128, "threshold must not exceed the number of shares"),
            (3, 1000, 128, "shares must not exceed 16"),
            (1, 1, 42, "Strength should be"),
        ],
    )
    def test_raise_generate_shamir_mnemonic_phrases(
        self, member_threshold, member_count, strength, err_msg
    ):
        with pytest.raises(ValueError, match=err_msg):
            Keypair.generate_shamir_mnemonic_phrases(
                member_threshold=member_threshold,
                member_count=member_count,
                strength=strength,
            )

    def test_shamir_sep5(self):
        for case in SEP_5_CASES:
            mnemonic, passphrase, accounts = (
                case["mnemonic"],
                case["passphrase"],
                case["accounts"],
            )

            # Entropy from mnemonic
            seed_raw = StellarMnemonic().to_bip39_seed(mnemonic, passphrase=passphrase)

            # Shamir from the entropy
            shamir_phrases = shamir_mnemonic.generate_mnemonics(
                group_threshold=1,
                groups=[(2, 3)],
                master_secret=seed_raw,
                passphrase=passphrase.encode(),
            )[0]

            # consistency checks
            for perms in itertools.permutations(shamir_phrases, 2):
                for idx in range(10):
                    reconstructed_kp = Keypair.from_shamir_mnemonic_phrases(
                        mnemonic_phrases=perms, passphrase=passphrase, index=idx
                    )

                    kp = Keypair.from_mnemonic_phrase(
                        mnemonic_phrase=mnemonic, passphrase=passphrase, index=idx
                    )
                    assert reconstructed_kp.public_key == kp.public_key
                    assert reconstructed_kp.secret == kp.secret

                    assert reconstructed_kp.public_key == accounts[idx][0]
                    assert reconstructed_kp.secret == accounts[idx][1]

    def test_xdr_public_key(self):
        public_key = "GBRF6PKZYP4J4WI2A3NF4CGF23SL34GRKA5LTQZCQFEUT2YJDZO2COXH"
        kp = Keypair.from_public_key(public_key)
        assert (
            kp.xdr_public_key().to_xdr()
            == "AAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2h"
        )

    def test_xdr_account_id(self):
        public_key = "GBRF6PKZYP4J4WI2A3NF4CGF23SL34GRKA5LTQZCQFEUT2YJDZO2COXH"
        kp = Keypair.from_public_key(public_key)
        assert (
            kp.xdr_account_id().to_xdr()
            == "AAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2h"
        )

    def test_xdr_muxed_account(self):
        public_key = "GBRF6PKZYP4J4WI2A3NF4CGF23SL34GRKA5LTQZCQFEUT2YJDZO2COXH"
        kp = Keypair.from_public_key(public_key)
        assert (
            kp.xdr_muxed_account().to_xdr()
            == "AAAAAGJfPVnD+J5ZGgbaXgjF1uS98NFQOrnDIoFJSesJHl2h"
        )

    def test_sign_decorated(self):
        data = b"Hello, Stellar!"
        kp = Keypair.from_secret(
            "SD7X7LEHBNMUIKQGKPARG5TDJNBHKC346OUARHGZL5ITC6IJPXHILY36"
        )
        sign_decorated = kp.sign_decorated(data)
        assert sign_decorated.signature_hint == kp.signature_hint()
        assert sign_decorated.signature == kp.sign(data)

    @pytest.mark.parametrize(
        "payload, hint",
        [
            (b"cat!!!", [0x22, 0xDD, 0x24, 0xD6]),
            (b"cat!", [0x35, 0x9D, 0x71, 0xD6]),
            (b"cat", [0x35, 0x9D, 0x71, 0xF7]),
            (b"", [0x56, 0xFC, 0x05, 0xF7]),
        ],
    )
    def test_sign_decorated_for_payload(self, payload, hint):
        kp = Keypair.from_secret(
            "SDHOAMBNLGCE2MV5ZKIVZAQD3VCLGP53P3OBSBI6UN5L5XZI5TKHFQL4"
        )
        sign_decorated = kp.sign_payload_decorated(payload)
        assert sign_decorated.signature_hint == bytes(hint)
        assert sign_decorated.signature == kp.sign(payload)
