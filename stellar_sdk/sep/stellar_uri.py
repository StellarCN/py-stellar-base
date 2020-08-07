"""
SEP: 0007
Title: URI Scheme to facilitate delegated signing
Author: Nikhil Saraf (Lightyear.io / SDF)
Status: Active
Created: 2018-05-07
Updated: 2020-03-03
Version: 2.0.0
"""

import abc
import base64
from typing import Optional, List, Union
from urllib.parse import urlencode, quote

from ..asset import Asset
from ..exceptions import ValueError
from ..keypair import Keypair
from ..memo import Memo, NoneMemo, IdMemo, TextMemo, HashMemo, ReturnHashMemo
from ..transaction_envelope import TransactionEnvelope

__all__ = ["PayStellarUri", "TransactionStellarUri", "Replacement"]

STELLAR_SCHEME: str = "web+stellar"


class StellarUri(object, metaclass=abc.ABCMeta):
    def __init__(self, signature: Optional[str] = None):
        self.signature = signature

    @abc.abstractmethod
    def to_uri(self) -> str:
        raise NotImplementedError("The method has not been implemented.")

    @property
    def _signature_payload(self) -> bytes:
        data = self.to_uri()
        if self.signature:
            data = data[: data.find("&signature=")]
        # https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#request-signing
        sign_data = b"\0" * 35 + b"\4" + b"stellar.sep.7 - URI Scheme" + data.encode()
        return sign_data

    def sign(self, signer: Union[Keypair, str]) -> None:
        """Sign the URI.

        :param signer: The account used to sign this transaction, it should be the secret key of `URI_REQUEST_SIGNING_KEY`.
        """
        if isinstance(signer, str):
            signer = Keypair.from_secret(signer)
        sign_data = self._signature_payload
        signature = signer.sign(sign_data)
        self.signature = base64.b64encode(signature).decode()


class PayStellarUri(StellarUri):
    """A request for a payment to be signed.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-pay>`_

    :param destination: A valid account ID or payment address.
    :param amount: Amount that destination will receive.
    :param asset: Asset destination will receive.
    :param memo: A memo to attach to the transaction.
    :param callback: The uri to post the transaction to after signing.
    :param message: An message for displaying to the user.
    :param network_passphrase: The passphrase of the target network.
    :param origin_domain: A fully qualified domain name that specifies the originating domain of the URI request.
    :param signature: A base64 encode signature of the hash of the URI request.
    """

    def __init__(
        self,
        destination: str,
        amount: Optional[str] = None,
        asset: Optional[Asset] = None,
        memo: Optional[Memo] = None,
        callback: Optional[str] = None,
        message: Optional[str] = None,
        network_passphrase: Optional[str] = None,
        origin_domain: Optional[str] = None,
        signature: Optional[str] = None,
    ) -> None:
        super().__init__(signature)
        if message is not None and len(message) > 300:
            raise ValueError("Message must not exceed 300 characters.")

        self.asset_code = None
        self.asset_issuer = None
        self._asset = asset
        if asset:
            self.asset_code = asset.code
            self.asset_issuer = asset.issuer

        self.memo = None
        self.memo_type = None
        self._memo = memo
        if memo and not isinstance(memo, NoneMemo):
            if isinstance(memo, TextMemo):
                self.memo = memo.memo_text
                self.memo_type = "MEMO_TEXT"
            elif isinstance(memo, IdMemo):
                self.memo = memo.memo_id
                self.memo_type = "MEMO_ID"
            elif isinstance(memo, HashMemo):
                self.memo = base64.b64encode(memo.memo_hash).decode()
                self.memo_type = "MEMO_HASH"
            elif isinstance(memo, ReturnHashMemo):
                self.memo = base64.b64encode(memo.memo_return).decode()
                self.memo_type = "MEMO_RETURN"
            else:
                raise ValueError("Invalid memo.")
        self.destination = destination
        self.amount = amount
        self.callback = callback
        self.msg = message
        self.network_passphrase = network_passphrase
        self.origin_domain = origin_domain

    def to_uri(self) -> str:
        """Generate the request URI.
        """
        query_params = dict()
        query_params["destination"] = self.destination
        if self.amount is not None:
            query_params["amount"] = self.amount
        if self.amount is not None:
            query_params["amount"] = self.amount
        if self._asset is not None and not self._asset.is_native():
            query_params["asset_code"] = self.asset_code
            query_params["asset_issuer"] = self.asset_issuer
        if self._memo is not None and not isinstance(self._memo, NoneMemo):
            query_params["memo"] = self.memo
            query_params["memo_type"] = self.memo_type
        if self.callback is not None:
            query_params["callback"] = "url:" + self.callback
        if self.msg is not None:
            query_params["msg"] = self.msg
        if self.network_passphrase is not None:
            query_params["network_passphrase"] = self.network_passphrase
        if self.origin_domain is not None:
            query_params["origin_domain"] = self.origin_domain
        if self.signature is not None:
            query_params["signature"] = self.signature
        return f"{STELLAR_SCHEME}:pay?{urlencode(query_params, quote_via=quote)}"

    def __str__(self):
        return (
            f"<PayStellarUri [destination={self.destination}, amount={self.amount}, "
            f"asset_code={self.asset_code}, asset_issuer={self.asset_issuer}, "
            f"memo={self.memo}, memo_type={self.memo_type}, callback={self.callback}, "
            f"msg={self.msg}, network_passphrase={self.network_passphrase}, "
            f"origin_domain={self.origin_domain}, signature={self.signature}]>"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.destination == other.destination
            and self.amount == other.amount
            and self.asset_code == other.asset_code
            and self.asset_issuer == other.asset_issuer
            and self.memo == other.memo
            and self.memo_type == other.memo_type
            and self.callback == other.callback
            and self.msg == other.msg
            and self.network_passphrase == other.network_passphrase
            and self.origin_domain == other.origin_domain
            and self.signature == other.signature
        )


class Replacement:
    def __init__(
        self, txrep_tx_field_name: str, reference_identifier: str, hint: str
    ) -> None:
        """Used to represent a single replacement.

        Example:
            >>> r1 = Replacement("sourceAccount", "X", "account on which to create the trustline")
            >>> r2 = Replacement("seqNum", "Y", "sequence for sourceAccount")
            >>> replacements = [r1, r2]

        See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`_

        :param txrep_tx_field_name: Txrep tx field name.
        :param reference_identifier: Reference identifier.
        :param hint: A brief and clear explanation of the context for the `reference_identifier`.

        """
        self.txrep_tx_field_name = txrep_tx_field_name
        self.reference_identifier = reference_identifier
        self.hint = hint

    def __str__(self):
        return (
            f"<Replacement [txrep_tx_field_name={self.txrep_tx_field_name}, "
            f"reference_identifier={self.reference_identifier}, "
            f"hint={self.hint}]>"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.txrep_tx_field_name == other.txrep_tx_field_name
            and self.reference_identifier == other.reference_identifier
            and self.hint == other.hint
        )


class TransactionStellarUri(StellarUri):
    """A request for a transaction to be signed.

    See `SEP-0007 <https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0007.md#operation-tx>`_

    :param transaction_envelope: Transaction waiting to be signed.
    :param replace: A value that identifies the fields to be replaced in the xdr using the Txrep (SEP-0011) representation.
    :param callback: The uri to post the transaction to after signing.
    :param pubkey: Specify which public key you want the URI handler to sign for.
    :param message: An message for displaying to the user.
    :param network_passphrase: The passphrase of the target network.
    :param origin_domain: A fully qualified domain name that specifies the originating domain of the URI request.
    :param signature: A base64 encode signature of the hash of the URI request.
    """

    def __init__(
        self,
        transaction_envelope: TransactionEnvelope,
        replace: Optional[List[Replacement]] = None,
        callback: Optional[str] = None,
        pubkey: Optional[str] = None,
        message: Optional[str] = None,
        network_passphrase: Optional[str] = None,
        origin_domain: Optional[str] = None,
        signature: Optional[str] = None,
    ) -> None:
        super().__init__(signature)
        if message is not None and len(message) > 300:
            raise ValueError("Message must not exceed 300 characters.")

        self.transaction_envelope = transaction_envelope
        self.replace = replace
        self.callback = callback
        self.pubkey = pubkey
        self.msg = message
        self.network_passphrase = network_passphrase
        self.origin_domain = origin_domain

    @property
    def _replace(self) -> Optional[str]:
        if self.replace is None:
            return None
        replaces = []
        hits = dict()
        for i in self.replace:
            hits[i.reference_identifier] = i.hint
            replaces.append(i.txrep_tx_field_name + ":" + i.reference_identifier)
        return (
            ",".join(replaces) + ";" + ",".join([k + ":" + v for k, v in hits.items()])
        )

    def to_uri(self) -> str:
        """Generate the request URI.
        """
        query_params = dict()
        query_params["xdr"] = self.transaction_envelope.to_xdr()
        if self.callback is not None:
            query_params["callback"] = "url:" + self.callback
        if self.replace is not None:
            query_params["replace"] = self._replace
        if self.pubkey is not None:
            query_params["pubkey"] = self.pubkey
        if self.msg is not None:
            query_params["msg"] = self.msg
        if self.network_passphrase is not None:
            query_params["network_passphrase"] = self.network_passphrase
        if self.origin_domain is not None:
            query_params["origin_domain"] = self.origin_domain
        if self.signature is not None:
            query_params["signature"] = self.signature
        return f"{STELLAR_SCHEME}:tx?{urlencode(query_params, quote_via=quote)}"

    def __str__(self):
        return (
            f"<TransactionStellarUri [xdr={self.transaction_envelope.to_xdr()}, replace={self.replace}, "
            f"callback={self.callback}, pubkey={self.pubkey}, "
            f"msg={self.msg}, network_passphrase={self.network_passphrase}, "
            f"origin_domain={self.origin_domain}, signature={self.signature}]>"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return (
            self.transaction_envelope == other.transaction_envelope
            and self.replace == other.replace
            and self.callback == other.callback
            and self.pubkey == other.pubkey
            and self.msg == other.msg
            and self.network_passphrase == other.network_passphrase
            and self.origin_domain == other.origin_domain
            and self.signature == other.signature
        )
