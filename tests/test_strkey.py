import stellar_strkey

from stellar_sdk import strkey


def test_reexports_stellar_strkey():
    assert strkey.__all__ == stellar_strkey.__all__
    for name in stellar_strkey.__all__:
        assert getattr(strkey, name) is getattr(stellar_strkey, name)
