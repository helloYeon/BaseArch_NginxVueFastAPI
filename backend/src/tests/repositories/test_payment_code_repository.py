"""tests/repositories/test_payment_code_repository.py"""

import pytest
import test_payment_code_repository_params
from repositories.payment_code_repository import PaymentCodeRepository


@pytest.fixture
def payment_code_repository(override_get_db) -> PaymentCodeRepository:
    """PaymentCodeRepositoryのインスタンスを返す"""
    repository = PaymentCodeRepository(override_get_db)

    return repository


def test_find(payment_code_repository: PaymentCodeRepository) -> None:
    """findテスト"""
    for id, expected in test_payment_code_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_all_by_company_ids(payment_code_repository: PaymentCodeRepository) -> None:
    """get_all_by_company_idsテスト"""
    for (
        company_ids,
        expected,
    ) in test_payment_code_repository_params.test_get_all_by_company_ids():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.get_all_by_company_ids(company_ids)

        assert result == expected


def test_get_all_by_company_ids_exception() -> None:
    """get_all_by_company_ids例外テスト"""
    assert True


def test_get_all_by_company_infos_id(
    payment_code_repository: PaymentCodeRepository,
) -> None:
    """get_all_by_company_infos_idテスト"""
    for (
        company_infos_id,
        expected,
    ) in test_payment_code_repository_params.test_get_all_by_company_infos_id():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.get_all_by_company_infos_id(company_infos_id)

        assert result == expected


def test_get_all_by_company_infos_id_exception() -> None:
    """get_all_by_company_infos_id例外テスト"""
    assert True


def test_delete_by_company_infos_id(
    payment_code_repository: PaymentCodeRepository,
) -> None:
    """delete_by_company_infos_idテスト"""
    for (
        company_infos_id,
        expected,
    ) in test_payment_code_repository_params.test_delete_by_company_infos_id():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.delete_by_company_infos_id(company_infos_id)

        assert result == expected


def test_delete_by_company_infos_id_exception() -> None:
    """delete_by_company_infos_id例外テスト"""
    assert True


def test_insert_by_payment_codes(
    payment_code_repository: PaymentCodeRepository,
) -> None:
    """insert_by_payment_codesテスト"""
    for (
        payment_codes,
        expected,
    ) in test_payment_code_repository_params.test_insert_by_payment_codes():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.insert_by_payment_codes(payment_codes)

        assert result == expected


def test_insert_by_payment_codes_exception() -> None:
    """insert_by_payment_codes例外テスト"""
    assert True


def test_get_by_peppol_id_company_infos_id(
    payment_code_repository: PaymentCodeRepository,
) -> None:
    """get_by_peppol_id_company_infos_idテスト"""
    for (
        peppol_id,
        company_infos_id,
        expected,
    ) in test_payment_code_repository_params.test_get_by_peppol_id_company_infos_id():
        # メソッドの呼び出しと結果の検証
        result = payment_code_repository.get_by_peppol_id_company_infos_id(
            peppol_id, company_infos_id
        )

        assert result == expected


def test_get_by_peppol_id_company_infos_id_exception() -> None:
    """get_by_peppol_id_company_infos_id例外テスト"""
    assert True
