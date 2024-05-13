import warnings
from enum import IntFlag
from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..keypair import Keypair
from ..muxed_account import MuxedAccount
from ..signer import Signer
from ..strkey import StrKey
from ..utils import raise_if_not_valid_ed25519_public_key
from .operation import Operation

__all__ = ["AuthorizationFlag", "SetOptions"]


class AuthorizationFlag(IntFlag):
    """Indicates which flags to set. For details about the flags,
    please refer to the `Control Access to an Asset - Flag <https://developers.stellar.org/docs/issuing-assets/control-asset-access/#flags>`__.
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
    doc <https://developers.stellar.org/docs/glossary/multisig/>`_.

    When updating signers or other thresholds, the threshold of this operation
    is high.

    Threshold: Medium or High

    See `Set Options <https://developers.stellar.org/docs/start/list-of-operations/#set-options>`_ for more information.

    :param inflation_dest: Account of the inflation destination.
    :param clear_flags: Indicates which flags to clear. For details about the flags,
        please refer to the `Control Access to an Asset - Flag <https://developers.stellar.org/docs/issuing-assets/control-asset-access/#flags>`__.
        The `bit mask <https://en.wikipedia.org/wiki/Bit_field>`_ integer subtracts from the existing flags of the account.
        This allows for setting specific bits without knowledge of existing flags, you can also use
        :class:`stellar_sdk.operation.set_options.AuthorizationFlag`

        * AUTHORIZATION_REQUIRED = 1
        * AUTHORIZATION_REVOCABLE = 2
        * AUTHORIZATION_IMMUTABLE = 4
        * AUTHORIZATION_CLAWBACK_ENABLED = 8

    :param set_flags: Indicates which flags to set. For details about the flags,
        please refer to the `Control Access to an Asset - Flag <https://developers.stellar.org/docs/issuing-assets/control-asset-access/#flags>`__.
        The bit mask integer adds onto the existing flags of the account.
        This allows for setting specific bits without knowledge of existing flags, you can also use
        :class:`stellar_sdk.operation.set_options.AuthorizationFlag`

        * AUTHORIZATION_REQUIRED = 1
        * AUTHORIZATION_REVOCABLE = 2
        * AUTHORIZATION_IMMUTABLE = 4
        * AUTHORIZATION_CLAWBACK_ENABLED = 8

    :param master_weight: A number from 0-255 (inclusive) representing the weight of the master key.
        If the weight of the master key is updated to 0, it is effectively disabled.
    :param low_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a low threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
    :param med_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a medium threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
    :param high_threshold: A number from 0-255 (inclusive) representing the threshold this account sets on all
        operations it performs that have `a high threshold <https://developers.stellar.org/docs/glossary/multisig/>`_.
    :param home_domain: sets the home domain used for
        reverse `federation <https://developers.stellar.org/docs/glossary/federation/>`_ lookup.
    :param signer: Add, update, or remove a signer from the account.
    :param source: The source account for the operation. Defaults to the transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.SET_OPTIONS
    )

    def __init__(
        self,
        inflation_dest: str = None,
        clear_flags: Union[int, AuthorizationFlag] = None,
        set_flags: Union[int, AuthorizationFlag] = None,
        master_weight: int = None,
        low_threshold: int = None,
        med_threshold: int = None,
        high_threshold: int = None,
        signer: Signer = None,
        home_domain: str = None,
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        if set_flags is not None and not isinstance(set_flags, AuthorizationFlag):
            warnings.warn(
                "`set_flags` is a int, we recommend using AuthorizationFlag.",
                DeprecationWarning,
            )
            set_flags = AuthorizationFlag(set_flags)

        if clear_flags is not None and not isinstance(clear_flags, AuthorizationFlag):
            warnings.warn(
                "`clear_flags` is a int, we recommend using AuthorizationFlag.",
                DeprecationWarning,
            )
            clear_flags = AuthorizationFlag(clear_flags)

        self.inflation_dest = inflation_dest
        self.clear_flags: Optional[AuthorizationFlag] = clear_flags
        self.set_flags: Optional[AuthorizationFlag] = set_flags
        self.master_weight: Optional[int] = master_weight
        self.low_threshold: Optional[int] = low_threshold
        self.med_threshold: Optional[int] = med_threshold
        self.high_threshold: Optional[int] = high_threshold
        self.home_domain: Optional[str] = home_domain
        self.signer: Optional[Signer] = signer
        if self.inflation_dest is not None:
            raise_if_not_valid_ed25519_public_key(self.inflation_dest, "inflation_dest")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        inflation_dest = (
            Keypair.from_public_key(self.inflation_dest).xdr_account_id()
            if self.inflation_dest is not None
            else None
        )
        home_domain = (
            stellar_xdr.String32(bytes(self.home_domain, encoding="utf-8"))
            if self.home_domain is not None
            else None
        )
        clear_flags = (
            None
            if self.clear_flags is None
            else stellar_xdr.Uint32(self.clear_flags.value)
        )
        set_flags = (
            None if self.set_flags is None else stellar_xdr.Uint32(self.set_flags.value)
        )
        master_weight = (
            None
            if self.master_weight is None
            else stellar_xdr.Uint32(self.master_weight)
        )
        low_threshold = (
            None
            if self.low_threshold is None
            else stellar_xdr.Uint32(self.low_threshold)
        )
        med_threshold = (
            None
            if self.med_threshold is None
            else stellar_xdr.Uint32(self.med_threshold)
        )
        high_threshold = (
            None
            if self.high_threshold is None
            else stellar_xdr.Uint32(self.high_threshold)
        )
        signer = None if self.signer is None else self.signer.to_xdr_object()

        set_options_op = stellar_xdr.SetOptionsOp(
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
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, set_options_op=set_options_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object) -> "SetOptions":
        """Creates a :class:`SetOptions` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)

        inflation_dest = None
        if xdr_object.body.set_options_op.inflation_dest:
            inflation_dest = StrKey.encode_ed25519_public_key(
                xdr_object.body.set_options_op.inflation_dest.account_id.ed25519.uint256
            )

        clear_flags_xdr = xdr_object.body.set_options_op.clear_flags
        set_flags_xdr = xdr_object.body.set_options_op.set_flags
        master_weight_xdr = xdr_object.body.set_options_op.master_weight
        low_threshold_xdr = xdr_object.body.set_options_op.low_threshold
        med_threshold_xdr = xdr_object.body.set_options_op.med_threshold
        high_threshold_xdr = xdr_object.body.set_options_op.high_threshold
        home_domain_xdr = xdr_object.body.set_options_op.home_domain
        signer_xdr_object = xdr_object.body.set_options_op.signer

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
        return op

    def __repr__(self):
        return (
            f"<SetOptions [inflation_dest={self.inflation_dest}, "
            f"clear_flags={self.clear_flags}, "
            f"set_flags={self.set_flags}, "
            f"master_weight={self.master_weight}, "
            f"low_threshold={self.low_threshold}, "
            f"med_threshold={self.med_threshold}, "
            f"high_threshold={self.high_threshold}, "
            f"signer={self.signer}, "
            f"home_domain={self.home_domain}, "
            f"source={self.source}]>"
        )
