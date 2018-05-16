from stellar_base.keypair import Keypair


def test_sep0005():
    # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
    mnemonic = 'illness spike retreat truth genius clock brain pass fit cave bargain toe'
    seed = Keypair.deterministic(mnemonic).seed()
    assert seed == b'SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN'
    address = Keypair.deterministic(mnemonic, index=6).address().decode()
    assert address == 'GBY27SJVFEWR3DUACNBSMJB6T4ZPR4C7ZXSTHT6GMZUDL23LAM5S2PQX'

    mnemonic = 'cable spray genius state float twenty onion head street palace net private method loan turn phrase state blanket interest dry amazing dress blast tube'
    seed = Keypair.deterministic(mnemonic, passphrase='p4ssphr4se').seed()
    assert seed == b'SAFWTGXVS7ELMNCXELFWCFZOPMHUZ5LXNBGUVRCY3FHLFPXK4QPXYP2X'
    address = Keypair.deterministic(mnemonic, passphrase='p4ssphr4se', index=9).address().decode()
    assert address == 'GBOSMFQYKWFDHJWCMCZSMGUMWCZOM4KFMXXS64INDHVCJ2A2JAABCYRR'

    mnemonic = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about'
    seed = Keypair.deterministic(mnemonic).seed()
    assert seed == b'SBUV3MRWKNS6AYKZ6E6MOUVF2OYMON3MIUASWL3JLY5E3ISDJFELYBRZ'
    address = Keypair.deterministic(mnemonic, index=8).address().decode()
    assert address == 'GABTYCZJMCP55SS6I46SR76IHETZDLG4L37MLZRZKQDGBLS5RMP65TSX'
