import pytest

from stellar_sdk import Address, Keypair, Network, scval, utils
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.auth import authorize_entry, authorize_invocation


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
                    function_name=scval.to_symbol("increment").sym,
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
                    function_name=scval.to_symbol("increment").sym,
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
        signer_fn = lambda preimage: (
            signer.public_key,
            signer.sign(utils.sha256(preimage.to_xdr_bytes())),
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
                    function_name=scval.to_symbol("increment").sym,
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
        signer_fn = lambda preimage: (
            signer.public_key,
            signer.sign(utils.sha256(preimage.to_xdr_bytes())),
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
                    function_name=scval.to_symbol("increment").sym,
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
                    function_name=scval.to_symbol("increment").sym,
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

    def test_sign_authorize_entry_with_signature_mismatch_raise(self):
        contract_id = "CDCYWK73YTYFJZZSJ5V7EDFNHYBG4QN3VUNG2IGD27KJDDPNCZKBCBXK"
        signer = Keypair.from_secret(
            "SAEZSI6DY7AXJFIYA4PM6SIBNEYYXIEM2MSOTHFGKHDW32MBQ7KVO6EN"
        )
        signer_fn = lambda preimage: (
            signer.public_key,
            signer.sign(utils.sha256(preimage.to_xdr_bytes() + b"invalid")),
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
                    function_name=scval.to_symbol("increment").sym,
                    args=[scval.to_address(signer.public_key), scval.to_uint32(10)],
                ),
            ),
            sub_invocations=[],
        )
        entry = stellar_xdr.SorobanAuthorizationEntry(credentials, invocation)

        with pytest.raises(ValueError, match="signature doesn't match payload."):
            authorize_entry(
                entry.to_xdr(),
                signer_fn,
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
                    function_name=scval.to_symbol("increment").sym,
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
        assert len(signed_entry.credentials.address.signature.vec.sc_vec) == 1

    def test_sign_authorize_invocation_with_function_signer(self):
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

        invocation = stellar_xdr.SorobanAuthorizedInvocation(
            function=stellar_xdr.SorobanAuthorizedFunction(
                type=stellar_xdr.SorobanAuthorizedFunctionType.SOROBAN_AUTHORIZED_FUNCTION_TYPE_CONTRACT_FN,
                contract_fn=stellar_xdr.InvokeContractArgs(
                    contract_address=Address(contract_id).to_xdr_sc_address(),
                    function_name=scval.to_symbol("increment").sym,
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
                    function_name=scval.to_symbol("increment").sym,
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
        signer_fn = lambda preimage: (
            signer.public_key,
            signer.sign(utils.sha256(preimage.to_xdr_bytes())),
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
                    function_name=scval.to_symbol("increment").sym,
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
