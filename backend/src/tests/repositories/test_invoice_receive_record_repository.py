"""tests/repositories/test_invoice_receive_record_repository.py"""

import pytest
import test_invoice_receive_record_repository_params
from repositories.invoice_receive_record_repository import (
    InvoiceReceiveRecordRepository,
)


@pytest.fixture
def invoice_receive_record_repository(
    override_get_db,
) -> InvoiceReceiveRecordRepository:
    """InvoiceReceiveRecordRepositoryのインスタンスを返す"""
    repository = InvoiceReceiveRecordRepository(override_get_db)

    return repository


def test_find(
    invoice_receive_record_repository: InvoiceReceiveRecordRepository,
) -> None:
    """findテスト"""
    for id, expected in test_invoice_receive_record_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = invoice_receive_record_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_by_company_infos_id_status(
    invoice_receive_record_repository: InvoiceReceiveRecordRepository,
) -> None:
    """get_by_company_infos_id_statusテスト"""
    for (
        company_infos_id,
        status,
        expected,
    ) in (
        test_invoice_receive_record_repository_params.test_get_by_company_infos_id_status()
    ):
        # メソッドの呼び出しと結果の検証
        result = invoice_receive_record_repository.get_by_company_infos_id_status(
            company_infos_id, status
        )

        assert result == expected


def test_get_by_company_infos_id_status_exception() -> None:
    """get_by_company_infos_id_status例外テスト"""
    assert True


def test_insert_by_invoice_receive_record(
    invoice_receive_record_repository: InvoiceReceiveRecordRepository,
) -> None:
    """insert_by_invoice_receive_recordテスト"""
    for (
        invoice_receive_record,
        expected,
    ) in (
        test_invoice_receive_record_repository_params.test_insert_by_invoice_receive_record()
    ):
        # メソッドの呼び出しと結果の検証
        result = invoice_receive_record_repository.insert_by_invoice_receive_record(
            invoice_receive_record
        )

        assert result == expected


def test_insert_by_invoice_receive_record_exception() -> None:
    """insert_by_invoice_receive_record例外テスト"""
    assert True


def test_update_status(
    invoice_receive_record_repository: InvoiceReceiveRecordRepository,
) -> None:
    """update_statusテスト"""
    for (
        id,
        status,
        expected,
    ) in test_invoice_receive_record_repository_params.test_update_status():
        # メソッドの呼び出しと結果の検証
        result = invoice_receive_record_repository.update_status(id, status)

        assert result == expected


def test_update_status_exception() -> None:
    """update_status例外テスト"""
    assert True
