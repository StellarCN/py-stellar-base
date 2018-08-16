class StellarError(Exception):
    def __init__(self, msg):
        super(StellarError, self).__init__(msg)


class ConfigurationError(StellarError):
    pass


class HorizonError(StellarError):
    def __init__(self, msg):
        super(HorizonError, self).__init__(msg)
        self.message = msg


class XdrLengthError(StellarError):
    pass


class PreimageLengthError(StellarError):
    pass


class SignatureExistError(StellarError):
    pass


class DecodeError(StellarError):
    pass


class AccountNotExistError(StellarError):
    pass


class NotValidParamError(StellarError):
    pass


class MnemonicError(StellarError):
    pass


class MissingSigningKeyError(StellarError):
    pass


class FederationError(Exception):
    """A :exc:`FederationError` that represents an issue stemming from
    Stellar Federation.

    """
