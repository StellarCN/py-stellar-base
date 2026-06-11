from typing import Any, cast

import pytest

from stellar_sdk import Address, Keypair, Network, scval, utils
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.auth import (
    DelegateSignature,
    authorization_payload_hash,
    authorize_entry,
    authorize_invocation,
    build_authorization_preimage,
    build_with_delegates_entry,
)


def _ed25519_auth_signer(signer: Keypair):
    """Build an AuthorizationSigner that mimics the default Stellar Account shape."""

    def _signer(preimage):
        signature = signer.sign(authorization_payload_hash(preimage))
        return scval.to_vec(
            [
                scval.to_map(
                    {
                        scval.to_symbol("public_key"): scval.to_bytes(
                            signer.raw_public_key()
                        ),
                        scval.to_symbol("signature"): scval.to_bytes(signature),
                    }
                )
            ]
        )

    return _signer


def _sample_invocation(
    contract_id: str = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK",
) -> stellar_xdr.SorobanAuthorizedInvocation:
    return stellar_xdr.SorobanAuthorizedInvocation(
        function=stellar_xdr.SorobanAuthorizedFunction(
            type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
            contract_fn=stellar_xdr.InvokeContractArgs(
                contract_address=Address(contract_id).to_xdr_sc_address(),
                function_name=stellar_xdr.SCSymbol(b"increment"),
                args=[],
            ),
        ),
        sub_invocations=[],
    )


_MUXED_ACCOUNT_ID = (
    "MAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSAAAAAAAAAAE2LP26"
)
_CLAIMABLE_BALANCE_ID = "BAAD6DBUX6J22DMZOHIEZTEQ64CVCHEDRKWZONFEUL5Q26QD7R76RGR4TU"
_LIQUIDITY_POOL_ID = "LA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUPJN"


class TestAuth:
    def test_sign_authorize_entry_with_base64_entry_and_keypair_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(signer.public_key).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry.to_xdr(), signer, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(signer.public_key).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_xdr_entry_and_keypair_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(signer.public_key).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry, signer, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(signer.public_key).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_base64_entry_and_function_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        signer_fn = _ed25519_auth_signer(signer)

        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(signer.public_key).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry.to_xdr(), signer_fn, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(signer.public_key).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_xdr_entry_and_function_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        signer_fn = _ed25519_auth_signer(signer)
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(signer.public_key).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry, signer_fn, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(signer.public_key).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_source_credential_entry(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT,
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry.to_xdr(), signer, valid_until_ledger_sequence, network_passphrase
        )

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT,
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_legacy_tuple_signer_raise(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )

        def signer_fn(preimage):
            return (
                signer.public_key,
                signer.sign(utils.sha256(preimage.to_xdr_bytes())),
            )

        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(Keypair.random().public_key).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        with pytest.raises(
            TypeError,
            match=r"Authorization signer must return a stellar_sdk\.xdr\.SCVal",
        ):
            authorize_entry(
                entry.to_xdr(),
                cast(Any, signer_fn),
                valid_until_ledger_sequence,
                network_passphrase,
            )

    def test_sign_authorize_invocation_with_keypair_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )

        signed_entry = authorize_invocation(
            signer, None, valid_until_ledger_sequence, invocation, network_passphrase
        )

        assert signed_entry.root_invocation == invocation
        assert (
            signed_entry.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        )
        assert signed_entry.credentials.address is not None
        assert (
            signed_entry.credentials.address.address
            == Address(signer.public_key).to_xdr_sc_address()
        )
        assert (
            signed_entry.credentials.address.signature_expiration_ledger.uint32
            == valid_until_ledger_sequence
        )
        assert (
            signed_entry.credentials.address.signature.type
            == stellar_xdr.SCValType.SCV_VEC
        )
        assert signed_entry.credentials.address.signature.vec is not None
        assert len(signed_entry.credentials.address.signature.vec.sc_vec) == 1

    def test_sign_authorize_invocation_with_function_signer(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        signer_fn = _ed25519_auth_signer(signer)
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )

        signed_entry = authorize_invocation(
            signer_fn,
            signer.public_key,
            valid_until_ledger_sequence,
            invocation,
            network_passphrase,
        )

        assert signed_entry.root_invocation == invocation
        assert (
            signed_entry.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        )
        assert signed_entry.credentials.address is not None
        assert (
            signed_entry.credentials.address.address
            == Address(signer.public_key).to_xdr_sc_address()
        )
        assert (
            signed_entry.credentials.address.signature_expiration_ledger.uint32
            == valid_until_ledger_sequence
        )
        assert (
            signed_entry.credentials.address.signature.type
            == stellar_xdr.SCValType.SCV_VEC
        )
        assert signed_entry.credentials.address.signature.vec is not None
        assert len(signed_entry.credentials.address.signature.vec.sc_vec) == 1

    def test_sign_authorize_entry_with_keypair_signer_not_equal_credential_address(
        self,
    ):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credential_address = "GADBBY4WFXKKFJ7CMTG3J5YAUXMQDBILRQ6W3U5IWN5TQFZU4MWZ5T4K"
        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(credential_address).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry.to_xdr(), signer, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(credential_address).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_function_signer_not_equal_credential_address(
        self,
    ):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        signer_fn = _ed25519_auth_signer(signer)

        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

        credential_address = "GADBBY4WFXKKFJ7CMTG3J5YAUXMQDBILRQ6W3U5IWN5TQFZU4MWZ5T4K"
        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(credential_address).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        signed_entry = authorize_entry(
            entry.to_xdr(), signer_fn, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION,
            soroban_authorization=stellar_xdr.HashIDPreimageSorobanAuthorization(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                invocation=invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        expected_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
                address=stellar_xdr.SorobanAddressCredentials(
                    address=Address(credential_address).to_xdr_sc_address(),
                    nonce=stellar_xdr.Int64(123456789),
                    signature_expiration_ledger=stellar_xdr.Uint32(
                        valid_until_ledger_sequence
                    ),
                    signature=scval.to_vec(
                        [
                            scval.to_map(
                                {
                                    scval.to_symbol("public_key"): scval.to_bytes(
                                        signer.raw_public_key()
                                    ),
                                    scval.to_symbol("signature"): scval.to_bytes(
                                        signature
                                    ),
                                }
                            )
                        ]
                    ),
                ),
            ),
            root_invocation=invocation,
        )

        assert expected_entry == signed_entry
        assert id(expected_entry) != id(signed_entry)

    def test_sign_authorize_entry_with_custom_contract_signature(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        custom_signature = scval.to_map(
            {
                scval.to_symbol("bls"): scval.to_bytes(b"bls-signature"),
                scval.to_symbol("webauthn"): scval.to_map(
                    {
                        scval.to_symbol("authenticator_data"): scval.to_bytes(
                            b"authenticator-data"
                        ),
                        scval.to_symbol("client_data_json"): scval.to_bytes(
                            b'{"type":"webauthn.get"}'
                        ),
                        scval.to_symbol("signature"): scval.to_bytes(
                            b"webauthn-signature"
                        ),
                    }
                ),
            }
        )

        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(contract_id).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(contract_id), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)
        seen_preimages: list[stellar_xdr.HashIDPreimage] = []

        signed_entry = authorize_entry(
            entry,
            lambda preimage: seen_preimages.append(preimage) or custom_signature,
            valid_until_ledger_sequence,
            network_passphrase,
        )

        assert signed_entry.credentials.address is not None
        assert signed_entry.credentials.address.signature == custom_signature
        assert (
            signed_entry.credentials.address.signature_expiration_ledger.uint32
            == valid_until_ledger_sequence
        )
        assert len(seen_preimages) == 1

    def test_sign_authorize_invocation_with_contract_address_and_custom_signature(
        self,
    ):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        custom_signature = scval.to_vec(
            [
                scval.to_symbol("passkey"),
                scval.to_bytes(b"webauthn-signature"),
            ]
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(contract_id), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )

        signed_entry = authorize_invocation(
            lambda _: custom_signature,
            contract_id,
            valid_until_ledger_sequence,
            invocation,
            network_passphrase,
        )

        assert signed_entry.credentials.address is not None
        assert (
            signed_entry.credentials.address.address
            == Address(contract_id).to_xdr_sc_address()
        )
        assert signed_entry.credentials.address.signature == custom_signature

    def test_sign_authorize_invocation_accepts_address_instance(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )

        signed_entry = authorize_invocation(
            lambda _: scval.to_bytes(b"sig"),
            Address(contract_id),
            654656,
            invocation,
            Network.TESTNET_NETWORK_PASSPHRASE,
        )

        assert signed_entry.credentials.address is not None
        assert (
            signed_entry.credentials.address.address
            == Address(contract_id).to_xdr_sc_address()
        )

    def test_sign_authorize_invocation_requires_address_for_callable(self):
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(
                        "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                    ).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[],
                ),
            ),
            sub_invocations=[],
        )

        with pytest.raises(ValueError, match=r"`address` is required"):
            authorize_invocation(
                lambda _: scval.to_bytes(b"sig"),
                None,
                654656,
                invocation,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    @pytest.mark.parametrize(
        "address",
        [
            _MUXED_ACCOUNT_ID,
            Address(_CLAIMABLE_BALANCE_ID),
            _LIQUIDITY_POOL_ID,
        ],
    )
    def test_sign_authorize_invocation_rejects_non_account_contract_address(
        self, address
    ):
        with pytest.raises(ValueError, match=r"classic account .* contract"):
            authorize_invocation(
                lambda _: scval.to_bytes(b"sig"),
                address,
                654656,
                _sample_invocation(),
                Network.TESTNET_NETWORK_PASSPHRASE,
            )

    def test_sign_authorize_entry_rejects_non_account_contract_credential_address(
        self,
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
            address=stellar_xdr.SorobanAddressCredentials(
                address=Address(_MUXED_ACCOUNT_ID).to_xdr_sc_address(),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(0),
                signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
            ),
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, _sample_invocation())

        with pytest.raises(ValueError, match=r"classic account .* contract"):
            authorize_entry(
                entry,
                Keypair.random(),
                654656,
                Network.TESTNET_NETWORK_PASSPHRASE,
            )


def _address_credentials(
    address: str, nonce: int = 123456789
) -> stellar_xdr.SorobanAddressCredentials:
    return stellar_xdr.SorobanAddressCredentials(
        address=Address(address).to_xdr_sc_address(),
        nonce=stellar_xdr.Int64(nonce),
        signature_expiration_ledger=stellar_xdr.Uint32(0),
        signature=stellar_xdr.SCVal(type=stellar_xdr.SCValType.SCV_VOID),
    )


def _unsigned_entry(
    address: str,
    credentials_type: stellar_xdr.SorobanCredentialsType,
    invocation: stellar_xdr.SorobanAuthorizedInvocation | None = None,
) -> stellar_xdr.SorobanAuthorizationEntry:
    address_credentials = _address_credentials(address)
    if (
        credentials_type
        == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
    ):
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type, address=address_credentials
        )
    else:
        credentials = stellar_xdr.SorobanCredentials(
            type=credentials_type, address_v2=address_credentials
        )
    return stellar_xdr.SorobanAuthorizationEntry(
        credentials=credentials,
        root_invocation=invocation if invocation is not None else _sample_invocation(),
    )


class TestCap71Auth:
    """CAP-71: address-bound credentials (ADDRESS_V2) and delegated signers."""

    def test_build_authorization_preimage_v2_is_address_bound(self):
        signer = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        preimage = build_authorization_preimage(
            entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )

        assert (
            preimage.type
            == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION_WITH_ADDRESS
        )
        assert preimage.soroban_authorization_with_address is not None
        with_address = preimage.soroban_authorization_with_address
        assert with_address.address == Address(signer.public_key).to_xdr_sc_address()
        assert with_address.nonce == stellar_xdr.Int64(123456789)
        assert with_address.signature_expiration_ledger == stellar_xdr.Uint32(654656)
        assert with_address.invocation == entry.root_invocation

    def test_address_and_v2_payloads_differ(self):
        signer = Keypair.random()
        legacy_entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS,
        )
        v2_entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        legacy_preimage = build_authorization_preimage(
            legacy_entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        v2_preimage = build_authorization_preimage(
            v2_entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )

        assert (
            legacy_preimage.type
            == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION
        )
        assert authorization_payload_hash(
            legacy_preimage
        ) != authorization_payload_hash(v2_preimage)

    def test_with_delegates_preimage_matches_v2_preimage(self):
        signer = Keypair.random()
        v2_entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )
        wrapped = build_with_delegates_entry(
            v2_entry, 654656, [DelegateSignature(Keypair.random().public_key)]
        )

        v2_preimage = build_authorization_preimage(
            v2_entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        wrapped_preimage = build_authorization_preimage(
            wrapped, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )

        # CAP-71-01: every signer of a delegates entry signs the payload bound
        # to the top-level address, which is identical to the V2 payload.
        assert wrapped_preimage.to_xdr_bytes() == v2_preimage.to_xdr_bytes()

    def test_authorize_entry_v2_with_keypair_signer(self):
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        valid_until_ledger_sequence = 654656
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        signed_entry = authorize_entry(
            entry, signer, valid_until_ledger_sequence, network_passphrase
        )

        preimage = stellar_xdr.HashIDPreimage(
            type=stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION_WITH_ADDRESS,
            soroban_authorization_with_address=stellar_xdr.HashIDPreimageSorobanAuthorizationWithAddress(
                network_id=stellar_xdr.Hash(Network(network_passphrase).network_id()),
                nonce=stellar_xdr.Int64(123456789),
                signature_expiration_ledger=stellar_xdr.Uint32(
                    valid_until_ledger_sequence
                ),
                address=Address(signer.public_key).to_xdr_sc_address(),
                invocation=entry.root_invocation,
            ),
        )
        signature = signer.sign(utils.sha256(preimage.to_xdr_bytes()))

        assert signed_entry.credentials.address_v2 is not None
        signed_credentials = signed_entry.credentials.address_v2
        assert signed_credentials.signature_expiration_ledger == stellar_xdr.Uint32(
            valid_until_ledger_sequence
        )
        assert signed_credentials.signature == scval.to_vec(
            [
                scval.to_map(
                    {
                        scval.to_symbol("public_key"): scval.to_bytes(
                            signer.raw_public_key()
                        ),
                        scval.to_symbol("signature"): scval.to_bytes(signature),
                    }
                )
            ]
        )
        # the input entry is left untouched
        assert entry.credentials.address_v2 is not None
        assert (
            entry.credentials.address_v2.signature.type
            == stellar_xdr.SCValType.SCV_VOID
        )

    def test_authorize_entry_v2_with_function_signer_receives_with_address_preimage(
        self,
    ):
        signer = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )
        seen_preimages = []

        def auth_signer(preimage):
            seen_preimages.append(preimage)
            return _ed25519_auth_signer(signer)(preimage)

        signed_entry = authorize_entry(
            entry, auth_signer, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )

        assert len(seen_preimages) == 1
        assert (
            seen_preimages[0].type
            == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION_WITH_ADDRESS
        )
        assert signed_entry.credentials.address_v2 is not None
        assert (
            signed_entry.credentials.address_v2.signature.type
            == stellar_xdr.SCValType.SCV_VEC
        )

    def test_authorize_entry_with_delegates_signs_top_level_by_default(self):
        signer = Keypair.random()
        delegate = Keypair.random()
        entry = build_with_delegates_entry(
            _unsigned_entry(
                signer.public_key,
                stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
            654656,
            [DelegateSignature(delegate.public_key)],
        )

        signed_entry = authorize_entry(
            entry, signer, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )

        assert signed_entry.credentials.address_with_delegates is not None
        with_delegates = signed_entry.credentials.address_with_delegates
        assert (
            with_delegates.address_credentials.signature.type
            == stellar_xdr.SCValType.SCV_VEC
        )
        assert (
            with_delegates.delegates[0].signature.type == stellar_xdr.SCValType.SCV_VOID
        )

    def test_authorize_entry_for_address_fills_matching_delegate(self):
        signer = Keypair.random()
        delegate = Keypair.random()
        nested_delegate = Keypair.random()
        entry = build_with_delegates_entry(
            _unsigned_entry(
                signer.public_key,
                stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
            654656,
            [
                DelegateSignature(
                    delegate.public_key,
                    nested_delegates=[DelegateSignature(nested_delegate.public_key)],
                )
            ],
        )

        signed_entry = authorize_entry(
            entry,
            nested_delegate,
            654656,
            Network.TESTNET_NETWORK_PASSPHRASE,
            for_address=nested_delegate.public_key,
        )

        assert signed_entry.credentials.address_with_delegates is not None
        with_delegates = signed_entry.credentials.address_with_delegates
        # only the nested delegate node was signed
        assert (
            with_delegates.address_credentials.signature.type
            == stellar_xdr.SCValType.SCV_VOID
        )
        assert (
            with_delegates.delegates[0].signature.type == stellar_xdr.SCValType.SCV_VOID
        )
        assert (
            with_delegates.delegates[0].nested_delegates[0].signature.type
            == stellar_xdr.SCValType.SCV_VEC
        )

    def test_authorize_entry_for_address_without_match_raises(self):
        signer = Keypair.random()
        entry = build_with_delegates_entry(
            _unsigned_entry(
                signer.public_key,
                stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
            654656,
            [DelegateSignature(Keypair.random().public_key)],
        )

        with pytest.raises(ValueError, match=r"no credential node for address"):
            authorize_entry(
                entry,
                signer,
                654656,
                Network.TESTNET_NETWORK_PASSPHRASE,
                for_address=Keypair.random().public_key,
            )

    def test_expiration_committed_into_signed_payload(self):
        signer = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        first = authorize_entry(
            entry, signer, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        second = authorize_entry(
            entry, signer, 654657, Network.TESTNET_NETWORK_PASSPHRASE
        )

        assert first.credentials.address_v2 is not None
        assert second.credentials.address_v2 is not None
        assert (
            first.credentials.address_v2.signature
            != second.credentials.address_v2.signature
        )

    def test_authorize_invocation_defaults_to_address(self):
        # ADDRESS_V2 is only valid on Protocol 27+ networks, so the default
        # stays on the legacy, universally valid ADDRESS credentials; V2 is
        # opt-in via credentials_type.
        signer = Keypair.random()

        entry = authorize_invocation(
            signer,
            None,
            654656,
            _sample_invocation(),
            Network.TESTNET_NETWORK_PASSPHRASE,
        )

        assert (
            entry.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS
        )
        assert entry.credentials.address is not None
        assert entry.credentials.address.signature.type == stellar_xdr.SCValType.SCV_VEC

    def test_authorize_invocation_v2_opt_in(self):
        signer = Keypair.random()

        entry = authorize_invocation(
            signer,
            None,
            654656,
            _sample_invocation(),
            Network.TESTNET_NETWORK_PASSPHRASE,
            credentials_type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        assert (
            entry.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2
        )
        assert entry.credentials.address_v2 is not None
        credentials = entry.credentials.address_v2
        assert credentials.address == Address(signer.public_key).to_xdr_sc_address()
        assert credentials.signature_expiration_ledger == stellar_xdr.Uint32(654656)
        # the signature verifies against the address-bound payload
        preimage = build_authorization_preimage(
            entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert credentials.signature.vec is not None
        signature_map = credentials.signature.vec.sc_vec[0].map
        assert signature_map is not None
        signature_bytes = signature_map.sc_map[1].val.bytes
        assert signature_bytes is not None
        signer.verify(authorization_payload_hash(preimage), signature_bytes.sc_bytes)

    def test_authorize_invocation_rejects_with_delegates_credentials_type(self):
        with pytest.raises(ValueError, match=r"build_with_delegates_entry"):
            authorize_invocation(
                Keypair.random(),
                None,
                654656,
                _sample_invocation(),
                Network.TESTNET_NETWORK_PASSPHRASE,
                credentials_type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES,
            )

    def test_build_with_delegates_entry_wraps_and_defaults(self):
        signer = Keypair.random()
        delegate = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        wrapped = build_with_delegates_entry(
            entry, 654656, [DelegateSignature(delegate.public_key)]
        )

        assert (
            wrapped.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES
        )
        assert wrapped.credentials.address_with_delegates is not None
        with_delegates = wrapped.credentials.address_with_delegates
        assert (
            with_delegates.address_credentials.address
            == Address(signer.public_key).to_xdr_sc_address()
        )
        assert with_delegates.address_credentials.nonce == stellar_xdr.Int64(123456789)
        assert with_delegates.address_credentials.signature_expiration_ledger == (
            stellar_xdr.Uint32(654656)
        )
        assert (
            with_delegates.address_credentials.signature.type
            == stellar_xdr.SCValType.SCV_VOID
        )
        assert len(with_delegates.delegates) == 1
        assert (
            with_delegates.delegates[0].address
            == Address(delegate.public_key).to_xdr_sc_address()
        )
        assert (
            with_delegates.delegates[0].signature.type == stellar_xdr.SCValType.SCV_VOID
        )
        assert with_delegates.delegates[0].nested_delegates == []
        assert wrapped.root_invocation == entry.root_invocation
        # the input entry is left untouched
        assert (
            entry.credentials.type
            == stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2
        )

    def test_build_with_delegates_entry_sorts_each_level(self):
        signer = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )
        delegates = [Keypair.random().public_key for _ in range(4)]
        nested = [Keypair.random().public_key for _ in range(3)]

        wrapped = build_with_delegates_entry(
            entry,
            654656,
            [
                DelegateSignature(
                    delegates[0],
                    nested_delegates=[DelegateSignature(address) for address in nested],
                ),
                *[DelegateSignature(address) for address in delegates[1:]],
            ],
        )

        assert wrapped.credentials.address_with_delegates is not None
        top_level = wrapped.credentials.address_with_delegates.delegates
        top_level_keys = [node.address.to_xdr_bytes() for node in top_level]
        assert top_level_keys == sorted(top_level_keys)
        nested_nodes = next(
            node.nested_delegates for node in top_level if node.nested_delegates
        )
        nested_keys = [node.address.to_xdr_bytes() for node in nested_nodes]
        assert len(nested_keys) == 3
        assert nested_keys == sorted(nested_keys)

    def test_build_with_delegates_entry_rejects_duplicate_delegates(self):
        signer = Keypair.random()
        delegate = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        with pytest.raises(ValueError, match=r"Duplicate delegate address"):
            build_with_delegates_entry(
                entry,
                654656,
                [
                    DelegateSignature(delegate.public_key),
                    DelegateSignature(delegate.public_key),
                ],
            )

    def test_build_with_delegates_entry_rejects_wrong_entry_types(self):
        signer = Keypair.random()
        wrapped = build_with_delegates_entry(
            _unsigned_entry(
                signer.public_key,
                stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            ),
            654656,
            [],
        )
        with pytest.raises(ValueError, match=r"SOROBAN_CREDENTIALS_ADDRESS"):
            build_with_delegates_entry(wrapped, 654656, [])

        source_account_entry = stellar_xdr.SorobanAuthorizationEntry(
            credentials=stellar_xdr.SorobanCredentials(
                type=stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_SOURCE_ACCOUNT
            ),
            root_invocation=_sample_invocation(),
        )
        with pytest.raises(ValueError, match=r"SOROBAN_CREDENTIALS_ADDRESS"):
            build_with_delegates_entry(source_account_entry, 654656, [])

    def test_build_with_delegates_entry_rejects_non_account_contract_delegate(self):
        signer = Keypair.random()
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
        )

        with pytest.raises(ValueError, match=r"classic account .* contract"):
            build_with_delegates_entry(
                entry, 654656, [DelegateSignature(_MUXED_ACCOUNT_ID)]
            )

    def test_cross_sdk_vector_v2(self):
        # Vector generated with js-stellar-sdk v16.0.0-rc.1
        # (/tmp script: authorizeEntry over a fixed ADDRESS_V2 entry).
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(
                        "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                    ).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            invocation,
        )

        preimage = build_authorization_preimage(
            entry, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert (
            authorization_payload_hash(preimage).hex()
            == "c5f050b2f21e9856c05c6b4176874f870a5172ba59935cf4048838cfe4df8b23"
        )

        signed_entry = authorize_entry(
            entry, signer, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert signed_entry.to_xdr() == (
            "AAAAAgAAAAAAAAAAWLfEosjyl6qPPSRxKB/fzOyv5I5WYzE+wY4Spz7KmKEAAAAAB1vNFQAJ/UAAAAAQ"
            "AAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgWLfEosjyl6qPPSRx"
            "KB/fzOyv5I5WYzE+wY4Spz7KmKEAAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAXZWzTbs45F1lXnl1"
            "hDKLchL/Cfb3jLo02A1A1t1Jl7eA3OU3/MhtfdNHCsk1SUatxs8MyPjawuQMbV4PGrUWAQAAAAAAAAAB"
            "xYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD19SRje0WVBEAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAA"
            "AAAAAFi3xKLI8peqjz0kcSgf38zsr+SOVmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
        )

    def test_cross_sdk_vector_with_delegates(self):
        # Vector generated with js-stellar-sdk v16.0.0-rc.1: buildWithDelegatesEntry
        # over the fixed ADDRESS_V2 entry of test_cross_sdk_vector_v2 (deliberately
        # unsorted delegates input), then authorizeEntry for the top level and every
        # delegate via forAddress. The shared payload equals the V2 vector payload.
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        delegate_1 = Keypair.from_raw_ed25519_seed(bytes([1] * 32))
        delegate_2 = Keypair.from_raw_ed25519_seed(bytes([2] * 32))
        nested_delegate = Keypair.from_raw_ed25519_seed(bytes([3] * 32))
        assert (
            delegate_1.public_key
            == "GCFIRY65OQE7DFP5KLNS2PF2LVZMUZYJX4OZIEQ36N2IQANUB5XVYOJR"
        )
        assert (
            delegate_2.public_key
            == "GCATS5YOVB6ROX2WUNKGNQ2MP3GMXDMKSG2O4N5CLX3A6W4PZGZZI55U"
        )
        assert (
            nested_delegate.public_key
            == "GDWUSKGGFDI4FRXK5EBTRECZSVQSSWJHHJOGH6JWG3AUMFFMQ435DIAG"
        )
        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(
                        "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
                    ).to_xdr_sc_address(),
                    function_name=stellar_xdr.SCSymbol(b"increment"),
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = _unsigned_entry(
            signer.public_key,
            stellar_xdr.SorobanCredentialsType.SOROBAN_CREDENTIALS_ADDRESS_V2,
            invocation,
        )

        wrapped = build_with_delegates_entry(
            entry,
            654656,
            [
                DelegateSignature(delegate_2.public_key),
                DelegateSignature(
                    delegate_1.public_key,
                    nested_delegates=[DelegateSignature(nested_delegate.public_key)],
                ),
            ],
        )
        assert wrapped.to_xdr() == (
            "AAAAAwAAAAAAAAAAWLfEosjyl6qPPSRxKB/fzOyv5I5WYzE+wY4Spz7KmKEAAAAAB1vNFQAJ/UAAAAAB"
            "AAAAAgAAAAAAAAAAgTl3Dqh9F19Wo1Rmw0x+zMuNipG07jeiXfYPW4/Js5QAAAABAAAAAAAAAAAAAAAA"
            "iojj3XQJ8ZX9UtstPLpdcspnCb8dlBIb83SIAbQPb1wAAAABAAAAAQAAAAAAAAAA7UkoxijRwsbq6QM4"
            "kFmVYSlZJzpcY/k2NsFGFKyHN9EAAAABAAAAAAAAAAAAAAABxYsr+8TwVOcyT2vyDK0+Am5Bu60abSDD"
            "19SRje0WVBEAAAAJaW5jcmVtZW50AAAAAAAAAgAAABIAAAAAAAAAAFi3xKLI8peqjz0kcSgf38zsr+SO"
            "VmMxPsGOEqc+ypihAAAAAwAAAAoAAAAA"
        )

        wrapped_preimage = build_authorization_preimage(
            wrapped, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        assert (
            authorization_payload_hash(wrapped_preimage).hex()
            == "c5f050b2f21e9856c05c6b4176874f870a5172ba59935cf4048838cfe4df8b23"
        )

        signed_entry = authorize_entry(
            wrapped, signer, 654656, Network.TESTNET_NETWORK_PASSPHRASE
        )
        for delegate in (delegate_1, delegate_2, nested_delegate):
            signed_entry = authorize_entry(
                signed_entry,
                delegate,
                654656,
                Network.TESTNET_NETWORK_PASSPHRASE,
                for_address=delegate.public_key,
            )
        assert signed_entry.to_xdr() == (
            "AAAAAwAAAAAAAAAAWLfEosjyl6qPPSRxKB/fzOyv5I5WYzE+wY4Spz7KmKEAAAAAB1vNFQAJ/UAAAAAQ"
            "AAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAgWLfEosjyl6qPPSRx"
            "KB/fzOyv5I5WYzE+wY4Spz7KmKEAAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAXZWzTbs45F1lXnl1"
            "hDKLchL/Cfb3jLo02A1A1t1Jl7eA3OU3/MhtfdNHCsk1SUatxs8MyPjawuQMbV4PGrUWAQAAAAIAAAAA"
            "AAAAAIE5dw6ofRdfVqNUZsNMfszLjYqRtO43ol32D1uPybOUAAAAEAAAAAEAAAABAAAAEQAAAAEAAAAC"
            "AAAADwAAAApwdWJsaWNfa2V5AAAAAAANAAAAIIE5dw6ofRdfVqNUZsNMfszLjYqRtO43ol32D1uPybOU"
            "AAAADwAAAAlzaWduYXR1cmUAAAAAAAANAAAAQPWXWOc0qly69WFxVLxXSqhaODuvEntmVQJgZSPGDb7B"
            "GN3p+SzW5Ulx45KsqGeCoDAap6bndVFjwRehTvdc6wwAAAAAAAAAAAAAAACKiOPddAnxlf1S2y08ul1y"
            "ymcJvx2UEhvzdIgBtA9vXAAAABAAAAABAAAAAQAAABEAAAABAAAAAgAAAA8AAAAKcHVibGljX2tleQAA"
            "AAAADQAAACCKiOPddAnxlf1S2y08ul1yymcJvx2UEhvzdIgBtA9vXAAAAA8AAAAJc2lnbmF0dXJlAAAA"
            "AAAADQAAAEBkJxkBE1yqVMP5QJwOiTTt76EEJQmlzT72IEgE3q23CNjhr17rl900xRDLvw6dO/cKMqd0"
            "TXMNDA7H6wKDut8BAAAAAQAAAAAAAAAA7UkoxijRwsbq6QM4kFmVYSlZJzpcY/k2NsFGFKyHN9EAAAAQ"
            "AAAAAQAAAAEAAAARAAAAAQAAAAIAAAAPAAAACnB1YmxpY19rZXkAAAAAAA0AAAAg7UkoxijRwsbq6QM4"
            "kFmVYSlZJzpcY/k2NsFGFKyHN9EAAAAPAAAACXNpZ25hdHVyZQAAAAAAAA0AAABAPfCE793RWocChKqn"
            "gZ38mc2eyjq+qB6n0FhIPFf9SXJCgjLgSUaPcx+SgDkBXX8z0U+DgR1BgQ2rBJ+8OwtiCwAAAAAAAAAA"
            "AAAAAcWLK/vE8FTnMk9r8gytPgJuQbutGm0gw9fUkY3tFlQRAAAACWluY3JlbWVudAAAAAAAAAIAAAAS"
            "AAAAAAAAAABYt8SiyPKXqo89JHEoH9/M7K/kjlZjMT7BjhKnPsqYoQAAAAMAAAAKAAAAAA=="
        )
