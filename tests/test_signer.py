from stellar_sdk.signer import Signer


class TestSigner:
    def test_to_xdr_ed25519_public_key(self):
        key = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
        weight = 1
        signer = Signer.ed25519_public_key(key, weight)
        xdr = "AAAAAOvi1O/HEn+QgZJw+EMZBtwvTVNmpgvE9p8IRfwp0GY4AAAAAQ=="
        assert signer.to_xdr() == xdr

        from_instance = Signer.from_xdr(xdr)
        assert isinstance(from_instance, Signer)
        assert from_instance == signer

    def test_to_xdr_pre_auth_tx(self):
        key = b"\xed\xe25\xbb\x02\xceat\xce\xe0\xd1\xa8\xd3\x080p\xda_\xbd0\x9d3\x7f_\xc0hv\xc5\xaa\xe7v\x08"
        weight = 1
        signer = Signer.pre_auth_tx(key, weight)
        xdr = "AAAAAe3iNbsCzmF0zuDRqNMIMHDaX70wnTN/X8BodsWq53YIAAAAAQ=="
        assert signer.to_xdr() == xdr

        from_instance = Signer.from_xdr(xdr)
        assert isinstance(from_instance, Signer)
        assert from_instance == signer

    def test_to_xdr_sha256_hash(self):
        key = b"\xed\xe25\xbb\x02\xceat\xce\xe0\xd1\xa8\xd3\x080p\xda_\xbd0\x9d3\x7f_\xc0hv\xc5\xaa\xe7v\x08"
        weight = 1
        signer = Signer.sha256_hash(key, weight)
        xdr = "AAAAAu3iNbsCzmF0zuDRqNMIMHDaX70wnTN/X8BodsWq53YIAAAAAQ=="
        assert signer.to_xdr() == xdr
        from_instance = Signer.from_xdr(xdr)
        assert isinstance(from_instance, Signer)
        assert from_instance == signer

    def test_equals(self):
        key1 = "GDV6FVHPY4JH7EEBSJYPQQYZA3OC6TKTM2TAXRHWT4EEL7BJ2BTDQT5D"
        key2 = "GCLTVFJLOSF4C6HFLI4TQD2U6QSUJ2PZWFPLD3NDNUEO54MOIPHNQULB"
        weight = 1
        signer1 = Signer.ed25519_public_key(key1, weight)
        signer2 = Signer.ed25519_public_key(key2, weight)
        signer3 = Signer.ed25519_public_key(key2, weight)
        assert signer1 != signer2
        assert signer2 == signer3
        assert signer1 != "BAD TYPE"
