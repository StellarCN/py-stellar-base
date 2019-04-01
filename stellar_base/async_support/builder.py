from ..builder import Builder as BaseBuilder


class Builder(BaseBuilder):
    def __init__(self,
                 secret=None,
                 address=None,
                 horizon_uri=None,
                 network=None,
                 sequence=None,
                 fee=None):
        super().__init__(secret,
                         address,
                         horizon_uri,
                         network,
                         sequence,
                         fee)
