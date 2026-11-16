import stellar_xdr

from stellar_sdk import xdr


def test_reexports_stellar_xdr():
    assert xdr.__all__ == stellar_xdr.__all__
    for name in stellar_xdr.__all__:
        assert getattr(xdr, name) is getattr(stellar_xdr, name)
