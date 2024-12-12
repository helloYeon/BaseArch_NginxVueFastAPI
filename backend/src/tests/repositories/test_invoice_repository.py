"""tests/repositories/test_invoice_repository.py"""

import pytest
import test_invoice_repository_params
from repositories.invoice_repository import InvoiceRepository


@pytest.fixture
def invoice_repository(override_get_db) -> InvoiceRepository:
    """InvoiceRepositoryのインスタンスを返す"""
    repository = InvoiceRepository(override_get_db)

    return repository


def test_find(invoice_repository: InvoiceRepository) -> None:
    """findテスト"""
    for id, expected in test_invoice_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_by_invoice_id_company_ids(invoice_repository: InvoiceRepository) -> None:
    """get_by_invoice_id_company_idsテスト"""
    for (
        invoice_id,
        company_ids,
        expected,
    ) in test_invoice_repository_params.test_get_by_invoice_id_company_ids():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.get_by_invoice_id_company_ids(
            invoice_id, company_ids
        )

        assert result == expected


def test_get_by_invoice_id_company_ids_exception() -> None:
    """get_by_invoice_id_company_ids例外テスト"""
    assert True


def test_get_by_xml_and_company(invoice_repository: InvoiceRepository) -> None:
    """get_by_xml_and_company例外テスト"""
    for (
        xml_filename,
        company_infos_id,
        expected,
    ) in test_invoice_repository_params.test_get_by_xml_and_company():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.get_by_xml_and_company(
            xml_filename, company_infos_id
        )

        assert result == expected


def test_get_by_xml_and_company_exception() -> None:
    """get_by_xml_and_company例外テスト"""
    assert True


def test_update_is_download(invoice_repository: InvoiceRepository) -> None:
    """update_is_downloadテスト"""
    for (
        invoice_id,
        is_download,
        expected,
    ) in test_invoice_repository_params.test_update_is_download():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.update_is_download(invoice_id, is_download)

        assert result == expected


def test_update_is_download_exception() -> None:
    """update_is_download例外テスト"""
    assert True


def test_update_is_confirmation(invoice_repository: InvoiceRepository) -> None:
    """update_is_confirmationテスト"""
    for (
        invoice_id,
        is_download,
        expected,
    ) in test_invoice_repository_params.test_update_is_confirmation():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.update_is_confirmation(invoice_id, is_download)

        assert result == expected


def test_update_is_confirmation_exception() -> None:
    """update_is_confirmation例外テスト"""
    assert True


def test_update_is_open(invoice_repository: InvoiceRepository) -> None:
    """update_is_openテスト"""
    for (
        invoice_id,
        is_download,
        expected,
    ) in test_invoice_repository_params.test_update_is_open():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.update_is_open(invoice_id, is_download)

        assert result == expected


def test_update_is_open_exception() -> None:
    """update_is_open例外テスト"""
    assert True


def test_get_all_by_invoices_filter_company_info_company_ids(
    invoice_repository: InvoiceRepository,
) -> None:
    """get_all_by_invoices_filter_company_info_company_idsテスト"""
    for (
        invoices_filter,
        company_infos_id,
        company_ids,
        expected,
    ) in (
        test_invoice_repository_params.test_get_all_by_invoices_filter_company_info_company_ids()
    ):
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.get_all_by_invoices_filter_company_info_company_ids(
            invoices_filter, company_infos_id, company_ids
        )

        assert result == expected


def test_get_all_by_invoices_filter_company_info_company_ids_exception() -> None:
    """get_all_by_invoices_filter_company_info_company_ids例外テスト"""
    assert True


def test_get_all_by_csv_filter_company_info_company_ids(
    invoice_repository: InvoiceRepository,
) -> None:
    """get_all_by_csv_filter_company_info_company_idsテスト"""
    for (
        csv_filter,
        company_infos_id,
        company_ids,
        expected,
    ) in (
        test_invoice_repository_params.test_get_all_by_csv_filter_company_info_company_ids()
    ):
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.get_all_by_csv_filter_company_info_company_ids(
            csv_filter, company_infos_id, company_ids
        )

        assert result == expected


def test_get_all_by_csv_filter_company_info_company_ids_exception() -> None:
    """get_all_by_csv_filter_company_info_company_ids例外テスト"""
    assert True


def test_insert_by_invoice(invoice_repository: InvoiceRepository) -> None:
    """insert_by_invoiceテスト"""
    for invoice, expected in test_invoice_repository_params.test_insert_by_invoice():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.insert_by_invoice(invoice)

        assert result == expected


def test_insert_by_invoice_exception() -> None:
    """insert_by_invoice例外テスト"""
    assert True


def test_get_all_by_invoice_ids_company_ids(
    invoice_repository: InvoiceRepository,
) -> None:
    """get_all_by_invoice_ids_company_idsテスト"""
    for (
        invoice_ids,
        company_ids,
        expected,
    ) in test_invoice_repository_params.test_get_all_by_invoice_ids_company_ids():
        # メソッドの呼び出しと結果の検証
        result = invoice_repository.get_all_by_invoice_ids_company_ids(
            invoice_ids, company_ids
        )

        assert result == expected
