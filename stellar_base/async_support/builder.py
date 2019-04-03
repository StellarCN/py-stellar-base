import binascii

from stellar_base import Keypair
from stellar_base.async_support.horizon import Horizon, HORIZON_LIVE, HORIZON_TEST
from stellar_base.async_support.federation import federation
from stellar_base.exceptions import FederationError, StellarAddressInvalidError, SequenceError
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.builder import Builder as BaseBuilder


class Builder(BaseBuilder):
    """The :class:`Builder` object, which uses the builder pattern to create
    a list of operations in a :class:`Transaction`, ultimately to be submitted
    as a :class:`TransactionEnvelope` to the network via Horizon (see
    :class:`Horizon`).

    :param str secret: The base32 secret seed for the source address.
    :param str address: The base32 source address.
    :param str horizon_uri: The horizon instance to use for submitting the created
        transaction.
    :param str network: The network to connect to for verifying and retrieving
        additional attributes from. 'PUBLIC' is an alias for 'Public Global Stellar Network ; September 2015',
        'TESTNET' is an alias for 'Test SDF Network ; September 2015'. Defaults to TESTNET.
    :param sequence: The sequence number to use for submitting this
        transaction with (must be the *current* sequence number of the source
        account)
    :type sequence: int, str
    :param int fee: Base fee in stroops. The network base fee is obtained by default from the latest ledger.
        Transaction fee is equal to base fee times number of operations in this transaction.
    """

    def __init__(self,
                 secret=None,
                 address=None,
                 horizon_uri=None,
                 network=None,
                 sequence=None,
                 fee=None):
        super().__init__(secret, address, horizon_uri, network, sequence, fee)
        if horizon_uri:
            self.horizon = Horizon(horizon_uri)
        elif self.network == 'PUBLIC':
            self.horizon = Horizon(HORIZON_LIVE)
        else:
            self.horizon = Horizon(HORIZON_TEST)

        if sequence is not None:
            self.sequence = int(sequence)
        else:
            self.sequence = None

    async def federation_payment(self,
                                 fed_address,
                                 amount,
                                 asset_code='XLM',
                                 asset_issuer=None,
                                 source=None,
                                 allow_http=False):
        """Append a :class:`Payment <stellar_base.operation.Payment>` operation
        to the list of operations using federation on the destination address.

        Translates the destination stellar address to an account ID via
        :func:`federation <stellar_base.federation.federation>`, before
        creating a new payment operation via :meth:`append_payment_op`.

        :param str fed_address: A Stellar Address that needs to be translated
            into a valid account ID via federation.
        :param str amount: The amount of the currency to send in the payment.
        :param str asset_code: The asset code for the asset to send.
        :param str asset_issuer: The address of the issuer of the asset.
        :param str source: The source address of the payment.
        :param bool allow_http: When set to `True`, connections to insecure http protocol federation servers
            will be allowed. Must be set to `False` in production. Default: `False`.
        :return: This builder instance.

        """
        fed_info = await federation(
            address_or_id=fed_address, fed_type='name', allow_http=allow_http)
        if not fed_info or not fed_info.get('account_id'):
            raise FederationError(
                'Cannot determine Stellar Address to Account ID translation '
                'via Federation server.')
        self.append_payment_op(fed_info['account_id'], amount, asset_code,
                               asset_issuer, source)
        memo_type = fed_info.get('memo_type')
        if memo_type is not None and memo_type in ('text', 'id', 'hash'):
            getattr(self, 'add_' + memo_type.lower() + '_memo')(fed_info['memo'])

    async def hash(self):
        """Return a hash for this transaction.

        :return: A hash for this transaction.
        :rtype: bytes
        """
        return (await self.gen_te()).hash_meta()

    async def hash_hex(self):
        """Return a hex encoded hash for this transaction.

        :return: A hex encoded hash for this transaction.
        :rtype: str
        """
        return binascii.hexlify(await self.hash()).decode()

    async def gen_tx(self):
        """Generate a :class:`Transaction
        <stellar_base.transaction.Transaction>` object from the list of
        operations contained within this object.

        :return: A transaction representing all of the operations that have
            been appended to this builder.
        :rtype: :class:`Transaction <stellar_base.transaction.Transaction>`

        """
        if self.fee is None:
            self.fee = await self.get_fee()
        if self.sequence is None:
            self.sequence = await self.get_sequence()
        if not self.address:
            raise StellarAddressInvalidError('Transaction does not have any source address.')
        if self.sequence is None:
            raise SequenceError('No sequence is present, maybe not funded?')
        tx = Transaction(
            source=self.address,
            sequence=self.sequence,
            time_bounds=self.time_bounds,
            memo=self.memo,
            fee=self.fee * len(self.ops),
            operations=self.ops)
        self.tx = tx
        return tx

    async def gen_te(self):
        """Generate a :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>` around the
        generated Transaction via the list of operations in this instance.

        :return: A transaction envelope ready to send over the network.
        :rtype: :class:`TransactionEnvelope
            <stellar_base.transaction_envelope.TransactionEnvelope>`

        """
        if self.tx is None:
            await self.gen_tx()
        te = Te(self.tx, network_id=self.network)
        if self.te:
            te.signatures = self.te.signatures
        self.te = te
        return te

    async def gen_xdr(self):
        """Create an XDR object around a newly generated
        :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>`.

        :return: An XDR object representing a newly created transaction
            envelope ready to send over the network.

        """
        if self.tx is None:
            await self.gen_te()
        return self.te.xdr()

    async def gen_compliance_xdr(self):
        """Create an XDR object representing this builder's transaction to be
        sent over via the Compliance protocol (notably, with a sequence number
        of 0).

        Intentionally, the XDR object is returned without any signatures on the
        transaction.

        See `Stellar's documentation on its Compliance Protocol
        <https://www.stellar.org/developers/guides/compliance-protocol.html>`_
        for more information.

        """
        sequence = self.sequence
        self.sequence = -1
        tx = await self.gen_tx()
        tx_xdr = tx.xdr()
        self.sequence = sequence
        return tx_xdr

    async def sign(self, secret=None):
        """Sign the generated :class:`TransactionEnvelope
        <stellar_base.transaction_envelope.TransactionEnvelope>` from the list
        of this builder's operations.

        :param str secret: The secret seed to use if a key pair or secret was
            not provided when this class was originaly instantiated, or if
            another key is being utilized to sign the transaction envelope.

        """
        keypair = self.keypair if not secret else Keypair.from_seed(secret)
        await self.gen_te()
        self.te.sign(keypair)

    async def sign_preimage(self, preimage):
        """Sign the generated transaction envelope using a Hash(x) signature.

        :param preimage: The value to be hashed and used as a signer on the
            transaction envelope.
        :type preimage: str, bytes

        """
        if self.te is None:
            await self.gen_te()
        self.te.sign_hashX(preimage)

    async def submit(self):
        """Submit the generated XDR object of the built transaction envelope to
        Horizon.

        Sends the generated transaction envelope over the wire via this
        builder's :class:`Horizon <stellar_base.horizon.Horizon>` instance.
        Note that you'll typically want to sign the transaction before
        submitting via the sign methods.

        :returns: A dict representing the JSON response from Horizon.

        """
        xdr = await self.gen_xdr()
        return await self.horizon.submit(xdr.decode())

    async def get_sequence(self):
        """Get the sequence number for a given account via Horizon.

        :return: The current sequence number for a given account
        :rtype: int
        """
        if not self.address:
            raise StellarAddressInvalidError('No address provided.')

        address = await self.horizon.account(self.address)
        return int(address.get('sequence'))

    async def get_fee(self):
        return await self.horizon.base_fee()
