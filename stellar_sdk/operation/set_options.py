from enum import IntFlag
from typing import List, Optional, Union

from .operation import Operation
from .utils import check_ed25519_public_key
from ..keypair import Keypair
from ..signer import Signer
from ..strkey import StrKey
from ..utils import pack_xdr_array, unpack_xdr_array
from ..xdr import Xdr

__all__ = ["Flag", "SetOptions"]


class Flag(IntFlag):
    """Indicates which flags to set. For details about the flags,
    please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`_.
    The bit mask integer adds onto the existing flags of the account.
    """

    AUTHORIZATION_REQUIRED = 1
    AUTHORIZATION_REVOCABLE = 2
    AUTHORIZATION_IMMUTABLE = 4
    AUTHORIZATION_CLAWBACK_ENABLED = 8


class SetOptions(Operation):
    """The :class:`SetOptions` object, which represents a SetOptions operation
    on Stellar's network.

    This operation sets the options for an account.

    For more information on the signing options, please refer to the `multi-sig
    doc <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.

    When updating signers or other thresholds, the threshold of this operation
    is high.

    Threshold: Medium or High

    :param inflation_dest: Account of the inflation destination.
    :param clear_flags: Indicates which flags to clear. For details about the flags,
        please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`_.
        The `bit mask <https://en.wikipedia.org/wiki/Bit_field>`_ integer subtracts from the existing flags of the account.
        This allows for setting specific bits without knowledge of existing flags, you can also use
        :class:`stellar_sdk.operation.set_options.Flag`
        - AUTHORIZATION_REQUIRED = 1
        - AUTHORIZATION_REVOCABLE = 2
        - AUTHORIZATION_IMMUTABLE = 4
        - AUTHORIZATION_CLAWBACK_ENABLED = 8
    :param set_flags: Indicates which flags to set. For details about the flags,
        please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`_.
        The bit mask integer adds onto the existing flags of the account.
        This allows for setting specific bits without knowledge of existing flags, you can also use
        :class:`stellar_sdk.operation.set_options.Flag`
        - AUTHORIZATION_REQUIRED = 1
        - AUTHORIZATION_REVOCABLE = 2
        - AUTHORIZATION_IMMUTABLE = 4
        - AUTHORIZATION_CLAWBACK_ENABLED = 8
    :param master_weight: A number from 0-255 (inclusive) representing the weight of the master key.
        If the weight of the master key is updated to 0, it is effectively disabled.
    :param low_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a low threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
    :param med_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a medium threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
    :param high_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a high threshold <https://www.stellar.org/developers/guides/concepts/multi-sig.html>`_.
    :param home_domain: sets the home domain used for
        reverse `federation <https://www.stellar.org/developers/guides/concepts/federation.html>`_ lookup.
    :param signer: Add, update, or remove a signer from the account.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(
        self,
        inflation_dest: str = None,
        clear_flags: Union[int, Flag] = None,
        set_flags: Union[int, Flag] = None,
        master_weight: int = None,
        low_threshold: int = None,
        med_threshold: int = None,
        high_threshold: int = None,
        signer: Signer = None,
        home_domain: str = None,
        source: str = None,
    ) -> None:
        super().__init__(source)
        if inflation_dest is not None:
            check_ed25519_public_key(inflation_dest)

        if isinstance(set_flags, Flag):
            set_flags = set_flags.value

        if isinstance(clear_flags, Flag):
            clear_flags = clear_flags.value

        self.inflation_dest: str = inflation_dest
        self.clear_flags: int = clear_flags
        self.set_flags: int = set_flags
        self.master_weight: int = master_weight
        self.low_threshold: int = low_threshold
        self.med_threshold: int = med_threshold
        self.high_threshold: int = high_threshold
        self.home_domain: str = home_domain
        self.signer: Optional[Signer] = signer

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.SET_OPTIONS

    def _to_operation_body(self) -> Xdr.nullclass:
        if self.inflation_dest is not None:
            inflation_dest = [
                Keypair.from_public_key(self.inflation_dest).xdr_account_id()
            ]
        else:
            inflation_dest = []

        home_domain: List[bytes] = []
        if self.home_domain:
            home_domain = pack_xdr_array(bytes(self.home_domain, encoding="utf-8"))

        clear_flags = pack_xdr_array(self.clear_flags)
        set_flags = pack_xdr_array(self.set_flags)
        master_weight = pack_xdr_array(self.master_weight)
        low_threshold = pack_xdr_array(self.low_threshold)
        med_threshold = pack_xdr_array(self.med_threshold)
        high_threshold = pack_xdr_array(self.high_threshold)

        signer: List[Xdr.types.Signer] = []
        if self.signer:
            signer = [self.signer.to_xdr_object()]

        set_options_op = Xdr.types.SetOptionsOp(
            inflation_dest,
            clear_flags,
            set_flags,
            master_weight,
            low_threshold,
            med_threshold,
            high_threshold,
            home_domain,
            signer,
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.SET_OPTIONS
        body.setOptionsOp = set_options_op
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object) -> "SetOptions":
        """Creates a :class:`SetOptions` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        inflation_dest = None
        if operation_xdr_object.body.setOptionsOp.inflationDest:
            inflation_dest = StrKey.encode_ed25519_public_key(
                operation_xdr_object.body.setOptionsOp.inflationDest[0].ed25519
            )

        clear_flags = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.clearFlags
        )  # list
        set_flags = unpack_xdr_array(operation_xdr_object.body.setOptionsOp.setFlags)
        master_weight = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.masterWeight
        )
        low_threshold = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.lowThreshold
        )
        med_threshold = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.medThreshold
        )
        high_threshold = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.highThreshold
        )
        home_domain = unpack_xdr_array(
            operation_xdr_object.body.setOptionsOp.homeDomain
        )

        if home_domain:
            home_domain = home_domain.decode("utf-8")

        signer = None
        signer_xdr_object = operation_xdr_object.body.setOptionsOp.signer
        if signer_xdr_object:
            signer = Signer.from_xdr_object(signer_xdr_object[0])

        op = cls(
            inflation_dest=inflation_dest,
            clear_flags=clear_flags,
            set_flags=set_flags,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            signer=signer,
            source=source,
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
