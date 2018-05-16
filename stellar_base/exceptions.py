class StellarError(Exception):
    def __init__(self, msg):
        super(StellarError, self).__init__(msg)


class ConfigurationError(StellarError):
    pass


class HorizonError(StellarError):
    pass


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

