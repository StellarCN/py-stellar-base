from nose.tools import raises
from stellar_base.asset import Asset
from stellar_base.stellarxdr import Xdr


class TestAsset:
    def __init__(self):
        self.source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'

    def test_native(self):
        assert 'XLM' == Asset.native().code
        assert None == Asset.native().issuer

    def test_is_native(self):
        native = Asset('XLM')
        cny = Asset('CNY', self.source)
        assert native.is_native()
        assert not cny.is_native()

    def test_to_xdr_object(self):
        cny = Asset('CNY', self.source)
        assert isinstance(cny.to_xdr_object(), Xdr.types.Asset)

    @raises(Exception)
    def test_too_long(self):
        Asset('123456789012TooLong', self.source)

    @raises(Exception)
    def test_no_issuer(self):
        Asset('beer', None)

    def test_xdr(self):
        xdr = b'AAAAAUNOWQAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M='
        cny = Asset('CNY', self.source)
        assert xdr == cny.xdr()

    def test_unxdr(self):
        cny = Asset('CNY', self.source)
        xdr = cny.xdr()
        cny_x = Asset.from_xdr(xdr)
        assert cny == cny_x
