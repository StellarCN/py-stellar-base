from typing import Optional

from .operation import Operation
from .utils import check_ed25519_public_key
from ..keypair import Keypair
from ..signer import Signer
from ..strkey import StrKey
from ..xdr import xdr


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
        This allows for setting specific bits without knowledge of existing flags.
        - AUTHORIZATION_REQUIRED = 1
        - AUTHORIZATION_REVOCABLE = 2
        - AUTHORIZATION_IMMUTABLE = 4
    :param set_flags: Indicates which flags to set. For details about the flags,
        please refer to the `accounts doc <https://www.stellar.org/developers/guides/concepts/accounts.html>`_.
        The bit mask integer adds onto the existing flags of the account.
        This allows for setting specific bits without knowledge of existing flags.
        - AUTHORIZATION_REQUIRED = 1
        - AUTHORIZATION_REVOCABLE = 2
        - AUTHORIZATION_IMMUTABLE = 4
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
        clear_flags: int = None,
        set_flags: int = None,
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
    def type_code(cls) -> xdr.OperationType:
        return xdr.OperationType.SET_OPTIONS

    def _to_operation_body(self) -> xdr.OperationBody:
        inflation_dest = (
            Keypair.from_public_key(self.inflation_dest).xdr_account_id()
            if self.inflation_dest is not None
            else None
        )
        home_domain = (
            xdr.String32(bytes(self.home_domain, encoding="utf-8"))
            if self.home_domain is not None
            else None
        )
        clear_flags = None if self.clear_flags is None else xdr.Uint32(self.clear_flags)
        set_flags = None if self.set_flags is None else xdr.Uint32(self.set_flags)
        master_weight = (
            None if self.master_weight is None else xdr.Uint32(self.master_weight)
        )
        low_threshold = (
            None if self.low_threshold is None else xdr.Uint32(self.low_threshold)
        )
        med_threshold = (
            None if self.med_threshold is None else xdr.Uint32(self.med_threshold)
        )
        high_threshold = (
            None if self.high_threshold is None else xdr.Uint32(self.high_threshold)
        )
        signer = None if self.signer is None else self.signer.to_xdr_object()

        set_options_op = xdr.SetOptionsOp(
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
        body = xdr.OperationBody(type=self.type_code(), set_options_op=set_options_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object) -> "SetOptions":
        """Creates a :class:`SetOptions` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        inflation_dest = None
        if operation_xdr_object.body.set_options_op.inflation_dest:
            inflation_dest = StrKey.encode_ed25519_public_key(
                operation_xdr_object.body.set_options_op.inflation_dest.account_id.ed25519.uint256
            )

        clear_flags_xdr = operation_xdr_object.body.set_options_op.clear_flags
        set_flags_xdr = operation_xdr_object.body.set_options_op.set_flags
        master_weight_xdr = operation_xdr_object.body.set_options_op.master_weight
        low_threshold_xdr = operation_xdr_object.body.set_options_op.low_threshold
        med_threshold_xdr = operation_xdr_object.body.set_options_op.med_threshold
        high_threshold_xdr = operation_xdr_object.body.set_options_op.high_threshold
        home_domain_xdr = operation_xdr_object.body.set_options_op.home_domain
        signer_xdr_object = operation_xdr_object.body.set_options_op.signer

        clear_flags = None if clear_flags_xdr is None else clear_flags_xdr.uint32
        set_flags = None if set_flags_xdr is None else set_flags_xdr.uint32
        master_weight = None if master_weight_xdr is None else master_weight_xdr.uint32
        low_threshold = None if low_threshold_xdr is None else low_threshold_xdr.uint32
        med_threshold = None if med_threshold_xdr is None else med_threshold_xdr.uint32
        high_threshold = (
            None if high_threshold_xdr is None else high_threshold_xdr.uint32
        )
        home_domain = None if home_domain_xdr is None else home_domain_xdr.string32
        signer = (
            None
            if signer_xdr_object is None
            else Signer.from_xdr_object(signer_xdr_object)
        )

        if home_domain is not None:
            home_domain = home_domain.decode("utf-8")

        return cls(
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
