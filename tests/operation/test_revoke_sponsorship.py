import pytest

from stellar_sdk import Asset, LiquidityPoolId, Operation, RevokeSponsorship, SignerKey
from stellar_sdk.operation.revoke_sponsorship import Data, Offer
from stellar_sdk.operation.revoke_sponsorship import Signer as RevokeSponsorshipSigner
from stellar_sdk.operation.revoke_sponsorship import TrustLine


class TestRevokeSponsorship:
    def test_account_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAAAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQ=="

        op = RevokeSponsorship.revoke_account_sponsorship(account_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_account_with_invalid_account_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSG"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "account_id" is not a valid ed25519 public key: {account_id}',
        ):
            RevokeSponsorship.revoke_account_sponsorship(account_id, source)

    def test_trustline_xdr_with_asset(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset = Asset("CAT", "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC")
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAQAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAFDQVQAAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_trustline_xdr_with_invalid_account_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7"
        asset = Asset("CAT", "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC")
        with pytest.raises(
            ValueError,
            match=f'Value of argument "account_id" is not a valid ed25519 public key: {account_id}',
        ):
            RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)

    def test_trustline_xdr_with_liquidity_pool_id(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset = LiquidityPoolId(
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAQAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAPdexq4McJzMQ3b7G+XhwqoPC+9eM4ire037L9PM4D6xw=="

        op = RevokeSponsorship.revoke_trustline_sponsorship(account_id, asset, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_offer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        offer_id = 12345
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAgAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAAAAAADA5"

        op = RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_offer_with_invalid_seller_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSG"
        offer_id = 12345
        with pytest.raises(
            ValueError,
            match=f'Value of argument "seller_id" is not a valid ed25519 public key: {seller_id}',
        ):
            RevokeSponsorship.revoke_offer_sponsorship(seller_id, offer_id, source)

    def test_date_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        data_name = "Stellar Python SDK"
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAAAwAAAAB0OKzisegg6DLiIxxowYKqBRLupojJsXKjr1azOP28GQAAABJTdGVsbGFyIFB5dGhvbiBTREsAAA=="

        op = RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_date_with_invalid_account_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6B"
        data_name = "Stellar Python SDK"
        with pytest.raises(
            ValueError,
            match=f'Value of argument "account_id" is not a valid ed25519 public key: {account_id}',
        ):
            RevokeSponsorship.revoke_data_sponsorship(account_id, data_name, source)

    def test_claimable_balance_id_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f5be"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAABAAAAADaDVfafUhQ5/wQ0qnQ68cx96+0BXTAM5WxfUkUm5H1vg=="

        op = RevokeSponsorship.revoke_claimable_balance_sponsorship(balance_id, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_claimable_balance_id_with_invalid_claimable_balance_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        balance_id = (
            "00000000da0d57da7d4850e7fc10d2a9d0ebc731f7afb40574c03395b17d49149b91f"
        )
        with pytest.raises(
            ValueError,
            match=f'Value of argument "claimable_balance_id" is not a valid balance id: {balance_id}',
        ):
            RevokeSponsorship.revoke_claimable_balance_sponsorship(balance_id, source)

    def test_liquidity_pool(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAAAAAAABd17GrgxwnMxDdvsb5eHCqg8L714ziKt7Tfsv08zgPrH"

        op = RevokeSponsorship.revoke_liquidity_pool_sponsorship(
            liquidity_pool_id, source
        )
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_liquidity_pool_with_invalid_liquidity_pool_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        liquidity_pool_id = (
            "dd7b1ab831c273310ddbec6f97870aa83c2fbd78ce22aded37ecbf4f3380fac7invalid"
        )
        with pytest.raises(
            ValueError,
            match=f'Value of argument "liquidity_pool_id" is not a valid hash: {liquidity_pool_id}',
        ):
            RevokeSponsorship.revoke_liquidity_pool_sponsorship(
                liquidity_pool_id, source
            )

    def test_signer_xdr(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        signer_key = SignerKey.ed25519_public_key(
            "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC"
        )
        xdr = "AAAAAQAAAADX7fRsY6KTqIc8EIDyr8M9gxGPW6ODnZoZDgo6l1ymwwAAABIAAAABAAAAAHQ4rOKx6CDoMuIjHGjBgqoFEu6miMmxcqOvVrM4/bwZAAAAAImHF95q/7Wv0UPkh++WcIkobMpLgYu4lWqjaLYRxRCx"

        op = RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)
        assert op.to_xdr_object().to_xdr() == xdr
        restore_op = Operation.from_xdr_object(op.to_xdr_object())
        assert restore_op == op
        assert restore_op.to_xdr_object().to_xdr() == xdr

    def test_signer_with_invalid_account_id_raise(self):
        source = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account_id = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BS"
        signer_key = SignerKey.ed25519_public_key(
            "GCEYOF66NL73LL6RIPSIP34WOCESQ3GKJOAYXOEVNKRWRNQRYUILCQWC"
        )
        with pytest.raises(
            ValueError,
            match=f'Value of argument "account_id" is not a valid ed25519 public key: {account_id}',
        ):
            RevokeSponsorship.revoke_signer_sponsorship(account_id, signer_key, source)

    def test_trustline_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        asset1 = Asset.native()
        asset2 = Asset(
            "TEST", "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        )
        assert TrustLine(account1, asset1) == TrustLine(account1, asset1)
        assert TrustLine(account1, asset1) != TrustLine(account1, asset2)
        assert TrustLine(account1, asset1) != TrustLine(account2, asset1)

    def test_offer_equal(self):
        seller1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        seller2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        offer_id1 = 0
        offer_id2 = 1
        assert Offer(seller1, offer_id1) == Offer(seller1, offer_id1)
        assert Offer(seller1, offer_id1) != Offer(seller1, offer_id2)
        assert Offer(seller1, offer_id1) != Offer(seller2, offer_id1)

    def test_data_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        data_name1 = "data_name1"
        data_name2 = "data_name2"
        assert Data(account1, data_name1) == Data(account1, data_name1)
        assert Data(account1, data_name1) != Data(account1, data_name2)
        assert Data(account1, data_name1) != Data(account2, data_name1)

    def test_signer_equal(self):
        account1 = "GDL635DMMORJHKEHHQIIB4VPYM6YGEMPLORYHHM2DEHAUOUXLSTMHQDV"
        account2 = "GB2DRLHCWHUCB2BS4IRRY2GBQKVAKEXOU2EMTMLSUOXVNMZY7W6BSGZ7"
        signer1 = SignerKey.ed25519_public_key(account1)
        signer2 = SignerKey.ed25519_public_key(account2)
        assert RevokeSponsorshipSigner(account1, signer1) == RevokeSponsorshipSigner(
            account1, signer1
        )
        assert RevokeSponsorshipSigner(account1, signer1) != RevokeSponsorshipSigner(
            account1, signer2
        )
        assert RevokeSponsorshipSigner(account1, signer1) != RevokeSponsorshipSigner(
            account2, signer1
        )
