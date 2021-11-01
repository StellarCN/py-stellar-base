import pytest

from stellar_sdk import AuthorizationFlag, MuxedAccount, Operation, SetOptions, Signer
from stellar_sdk.utils import sha256


class TestSetOptions:
    AUTHORIZATION_REQUIRED = 1
    AUTHORIZATION_REVOCABLE = 2
    AUTHORIZATION_IMMUTABLE = 4
    AUTHORIZATION_CLAWBACK_ENABLED = 8

    @pytest.mark.parametrize(
        "inflation_dest, clear_flags, set_flags, master_weight, low_threshold, med_threshold, high_threshold, home_domain, signer, source, xdr",
        [
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                AUTHORIZATION_REVOCABLE | AUTHORIZATION_IMMUTABLE,
                AUTHORIZATION_REQUIRED,
                0,
                1,
                2,
                3,
                "www.example.com",
                Signer.ed25519_public_key(
                    "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7", 1
                ),
                None,
                "AAAAAAAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAYAAAABAAAAAQAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAgAAAAEAAAADAAAAAQAAAA93d3cuZXhhbXBsZS5jb20AAAAAAQAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAE=",
            ),
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                AuthorizationFlag.AUTHORIZATION_REVOCABLE
                | AuthorizationFlag.AUTHORIZATION_IMMUTABLE,
                AuthorizationFlag.AUTHORIZATION_REQUIRED,
                0,
                1,
                2,
                3,
                "www.example.com",
                Signer.ed25519_public_key(
                    "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7", 1
                ),
                None,
                "AAAAAAAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAYAAAABAAAAAQAAAAEAAAAAAAAAAQAAAAEAAAABAAAAAgAAAAEAAAADAAAAAQAAAA93d3cuZXhhbXBsZS5jb20AAAAAAQAAAADNTrgPO19O0EsnYjSc333yWGLKEVxLyu1kfKjCKOz9ewAAAAE=",
            ),
            (
                "GDGU5OAPHNPU5UCLE5RDJHG7PXZFQYWKCFOEXSXNMR6KRQRI5T6XXCD7",
                AUTHORIZATION_REQUIRED | AUTHORIZATION_REVOCABLE,
                AUTHORIZATION_REVOCABLE,
                3,
                2,
                4,
                6,
                None,
                Signer.pre_auth_tx(sha256(b"PRE_AUTH_TX"), 2),
                "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV",
                "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAAAUAAAABAAAAAM1OuA87X07QSydiNJzfffJYYsoRXEvK7WR8qMIo7P17AAAAAQAAAAMAAAABAAAAAgAAAAEAAAADAAAAAQAAAAIAAAABAAAABAAAAAEAAAAGAAAAAAAAAAEAAAAB96nlNnQ/Aq5uCbYXnGJN/EXa76Y2RQP6S1wP8lOEL1UAAAAC",
            ),
            (
                None,
                None,
                None,
                0,
                255,
                255,
                255,
                "overcat.me",
                Signer.sha256_hash(sha256(b"SHA256_HASH"), 0),
                None,
                "AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAD/AAAAAQAAAP8AAAABAAAA/wAAAAEAAAAKb3ZlcmNhdC5tZQAAAAAAAQAAAALB1I1O+GEAV87X3eYN/uAYDIDzP5mY4SVTEQFFYFq6nwAAAAA=",
            ),
            (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "AAAAAAAAAAUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
            ),
        ],
    )
    def test_to_xdr(
        self,
        inflation_dest,
        clear_flags,
        set_flags,
        master_weight,
        low_threshold,
        med_threshold,
        high_threshold,
        home_domain,
        signer,
        source,
        xdr,
    ):
        op = SetOptions(
            inflation_dest,
            clear_flags,
            set_flags,
            master_weight,
            low_threshold,
            med_threshold,
            high_threshold,
            signer,
            home_domain,
            source,
        )
        xdr_obj = op.to_xdr_object()
        assert xdr_obj.to_xdr() == xdr
        from_instance = Operation.from_xdr_object(xdr_obj)
        assert isinstance(from_instance, SetOptions)
        if source:
            assert from_instance.source == MuxedAccount.from_account(source)
        else:
            assert from_instance.source is None
        if clear_flags is not None:
            assert isinstance(from_instance.clear_flags, AuthorizationFlag)
        if set_flags is not None:
            assert isinstance(from_instance.set_flags, AuthorizationFlag)
        assert from_instance.clear_flags == clear_flags
        assert from_instance.set_flags == set_flags
        assert from_instance.master_weight == master_weight
        assert from_instance.low_threshold == low_threshold
        assert from_instance.med_threshold == med_threshold
        assert from_instance.high_threshold == high_threshold
        assert from_instance.signer == signer
        assert from_instance.home_domain == home_domain

    def test_invalid_inflation_dest_raise(self):
        key = "GCEZWKCA5VLDNRLN3RPRJMRZOX3Z6G5CHCGSNFHEYVXM3XOJMINVALID"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "inflation_dest" is not a valid ed25519 public key: {key}',
        ):
            SetOptions(inflation_dest=key)
