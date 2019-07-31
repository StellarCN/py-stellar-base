from enum import Enum

from .operation import Operation

from ..keypair import Keypair
from ..strkey import StrKey
from ..stellarxdr import Xdr
from ..utils import pack_xdr_array, unpack_xdr_array


class SetOptions(Operation):
    class SignerType(Enum):
        ED25519_PUBLIC_KEY = 'ed25519_public_key'
        PRE_AUTH_TX = 'pre_auth_tx'
        SHA256_HASH = 'sha256_hash'

    class AuthFlag:
        AUTHORIZATION_REQUIRED = 1
        AUTHORIZATION_REVOCABLE = 2
        AUTHORIZATION_IMMUTABLE = 4

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.SET_OPTIONS

    def __init__(self,
                 inflation_dest: str = None,
                 clear_flags: int = None,
                 set_flags: int = None,
                 master_weight: int = None,
                 low_threshold: int = None,
                 med_threshold: int = None,
                 high_threshold: int = None,
                 signer_type: 'SetOptions.SignerType' = None,
                 signer_key: str = None,
                 signer_weight: int = None,
                 home_domain: str = None,
                 source: str = None) -> None:
        super().__init__(source)
        super(SetOptions, self).__init__(source)
        self.inflation_dest = inflation_dest
        self.clear_flags = clear_flags
        self.set_flags = set_flags
        self.master_weight = master_weight
        self.low_threshold = low_threshold
        self.med_threshold = med_threshold
        self.high_threshold = high_threshold
        self.home_domain = home_domain

        self.signer_type, self.signer_key, self.signer_weight = SetOptions._setup_signer(signer_type, signer_key,
                                                                                         signer_weight)

    def to_operation_body(self) -> Xdr.nullclass():

        if self.inflation_dest is not None:
            inflation_dest = [Keypair.from_public_key(self.inflation_dest).xdr_account_id()]
        else:
            inflation_dest = []

        home_domain = []
        if self.home_domain:
            home_domain = pack_xdr_array(bytes(self.home_domain, encoding='utf-8'))

        clear_flags = pack_xdr_array(self.clear_flags)
        set_flags = pack_xdr_array(self.set_flags)
        master_weight = pack_xdr_array(self.master_weight)
        low_threshold = pack_xdr_array(self.low_threshold)
        med_threshold = pack_xdr_array(self.med_threshold)
        high_threshold = pack_xdr_array(self.high_threshold)

        signer = []
        if self.signer_type:
            signer = [Xdr.types.Signer(SetOptions._to_signer_key_xdr_object(self.signer_type,
                                                                            self.signer_key), self.signer_weight)]

        set_options_op = Xdr.types.SetOptionsOp(
            inflation_dest, clear_flags, set_flags,
            master_weight, low_threshold, med_threshold,
            high_threshold, home_domain, signer)
        body = Xdr.nullclass()
        body.type = Xdr.const.SET_OPTIONS
        body.setOptionsOp = set_options_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object):

        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        inflation_dest = None
        if op_xdr_object.body.setOptionsOp.inflationDest:
            inflation_dest = StrKey.encode_ed25519_public_key(op_xdr_object.body.setOptionsOp.inflationDest[0].ed25519)

        clear_flags = unpack_xdr_array(op_xdr_object.body.setOptionsOp.clearFlags)  # list
        set_flags = unpack_xdr_array(op_xdr_object.body.setOptionsOp.setFlags)
        master_weight = unpack_xdr_array(op_xdr_object.body.setOptionsOp.masterWeight)
        low_threshold = unpack_xdr_array(op_xdr_object.body.setOptionsOp.lowThreshold)
        med_threshold = unpack_xdr_array(op_xdr_object.body.setOptionsOp.medThreshold)
        high_threshold = unpack_xdr_array(op_xdr_object.body.setOptionsOp.highThreshold)
        home_domain = unpack_xdr_array(op_xdr_object.body.setOptionsOp.homeDomain)

        if home_domain:
            home_domain = home_domain.decode('utf-8')

        signer_key = None
        signer_type = None
        signer_weight = None
        if op_xdr_object.body.setOptionsOp.signer:
            key = op_xdr_object.body.setOptionsOp.signer[0].key
            if key.type == Xdr.const.SIGNER_KEY_TYPE_ED25519:
                signer_key = StrKey.encode_ed25519_public_key(key.ed25519)
                signer_type = SetOptions.SignerType.ED25519_PUBLIC_KEY
            if key.type == Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX:
                signer_key = key.preAuthTx
                signer_type = SetOptions.SignerType.PRE_AUTH_TX
            if key.type == Xdr.const.SIGNER_KEY_TYPE_HASH_X:
                signer_key = key.hashX
                signer_type = SetOptions.SignerType.SHA256_HASH

            signer_weight = op_xdr_object.body.setOptionsOp.signer[0].weight

        return cls(
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            signer_key=signer_key,
            signer_type=signer_type,
            signer_weight=signer_weight,
            source=source)

    @staticmethod
    def _setup_signer(signer_type: 'SetOptions.SignerType' = None,
                      signer_key: str = None,
                      signer_weight: str = None) -> ('SetOptions.SignerType', str, str):
        signer_arguments = (signer_key, signer_type, signer_weight)
        if all(v is not None for v in signer_arguments) == all(v is None for v in signer_arguments):
            raise ValueError(
                "If you want to set up signer, you must provide signer_type, signer_key and signer_weight.")

        if signer_type is None:
            return None, None, None

        if signer_type == SetOptions.SignerType.ED25519_PUBLIC_KEY:
            StrKey.is_valid_ed25519_public_key(signer_key)
        elif signer_type == SetOptions.SignerType.SHA256_HASH:
            pass
        elif signer_type == SetOptions.SignerType.PRE_AUTH_TX:
            pass
        else:
            raise ValueError('Invalid signer type, sign_type should be SetOptions.SignerType.ED25519_PUBLIC_KEY, '
                             'SetOptions.SHA256_HASH.ED25519_PUBLIC_KEY or SetOptions.SignerType.PRE_AUTH_TX')
        return signer_type, signer_key, signer_weight

    @staticmethod
    def _to_signer_key_xdr_object(signer_type, signer_key):
        if signer_type == SetOptions.SignerType.ED25519_PUBLIC_KEY:
            return Xdr.types.SignerKey(Xdr.const.SIGNER_KEY_TYPE_ED25519,
                                       ed25519=StrKey.decode_ed25519_public_key(signer_key))
        if signer_type == SetOptions.SignerType.SHA256_HASH:
            return Xdr.types.SignerKey(
                Xdr.const.SIGNER_KEY_TYPE_HASH_X, hashX=signer_key)
        if signer_type == SetOptions.SignerType.PRE_AUTH_TX:
            return Xdr.types.SignerKey(
                Xdr.const.SIGNER_KEY_TYPE_PRE_AUTH_TX, preAuthTx=signer_key)
