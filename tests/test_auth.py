from typing import Any, cast

import pytest

from stellar_sdk import Address, Keypair, Network, scval, utils
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.auth import (
    authorization_payload_hash,
    authorize_entry,
    authorize_invocation,
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
        signer_fn = lambda preimage: (
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
