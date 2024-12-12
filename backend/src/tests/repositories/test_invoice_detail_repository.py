"""tests/repositories/test_invoice_detail_repository.py"""

import pytest
import test_invoice_detail_repository_params
from repositories.invoice_detail_repository import InvoiceDetailRepository


@pytest.fixture
def invoice_detail_repository(override_get_db) -> InvoiceDetailRepository:
    """InvoiceDetailRepositoryのインスタンスを返す"""
    repository = InvoiceDetailRepository(override_get_db)

    return repository


def test_find(invoice_detail_repository: InvoiceDetailRepository) -> None:
    """findテスト"""
    for id, expected in test_invoice_detail_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = invoice_detail_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_by_invoice_detail_id_company_ids(
    invoice_detail_repository: InvoiceDetailRepository,
) -> None:
    """get_by_invoice_detail_id_company_idsテスト"""
    for (
        invoice_detail_id,
        company_ids,
        expected,
    ) in (
        test_invoice_detail_repository_params.test_get_by_invoice_detail_id_company_ids()
    ):
        # メソッドの呼び出しと結果の検証
        result = invoice_detail_repository.get_by_invoice_detail_id_company_ids(
            invoice_detail_id, company_ids
        )

        assert result == expected


def test_get_by_invoice_detail_id_company_ids_exception() -> None:
    """get_by_invoice_detail_id_company_ids例外テスト"""
    assert True


def test_get_all_by_invoice_id_company_ids(
    invoice_detail_repository: InvoiceDetailRepository,
) -> None:
    """get_all_by_invoice_id_company_idsテスト"""
    for (
        invoice_id,
        company_ids,
        expected,
    ) in test_invoice_detail_repository_params.test_get_all_by_invoice_id_company_ids():
        # メソッドの呼び出しと結果の検証
        result = invoice_detail_repository.get_all_by_invoice_id_company_ids(
            invoice_id, company_ids
        )

        assert result == expected


def test_get_all_by_invoice_id_company_ids_exception() -> None:
    """get_all_by_invoice_id_company_ids例外テスト"""
    assert True


def test_insert_by_invoice_details(
    invoice_detail_repository: InvoiceDetailRepository,
) -> None:
    """insert_by_invoice_detailsテスト"""
    for (
        invoice_details,
        expected,
    ) in test_invoice_detail_repository_params.test_insert_by_invoice_details():
        # メソッドの呼び出しと結果の検証
        result = invoice_detail_repository.insert_by_invoice_details(invoice_details)

        assert result == expected


def test_insert_by_invoice_details_exception() -> None:
    """insert_by_invoice_details例外テスト"""
    assert True
