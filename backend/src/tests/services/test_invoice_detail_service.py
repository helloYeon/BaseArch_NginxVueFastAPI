"""tests/services/test_invoice_detail_service.py"""

import pytest
import test_invoice_detail_service_params
from services.invoice_detail_service import InvoiceDetailService


@pytest.fixture
def invoice_detail_service(override_get_db) -> InvoiceDetailService:
    """InvoiceDetailServiceのインスタンスを返す"""
    service = InvoiceDetailService(override_get_db)

    return service


def test_get_invoice_detail(
    invoice_detail_service: InvoiceDetailService,
) -> None:
    """get_invoice_detailテスト"""
    for (
        invoice_detail_id,
        expected,
    ) in test_invoice_detail_service_params.test_get_invoice_detail():
        result = invoice_detail_service.get_invoice_detail(invoice_detail_id)

        assert result == expected


def test_get_invoice_detail_exception(
    invoice_detail_service: InvoiceDetailService,
) -> None:
    """get_invoice_detail例外テスト"""
    for (
        invoice_detail_id,
        expected,
    ) in test_invoice_detail_service_params.test_get_invoice_detail_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_detail_service.get_invoice_detail(invoice_detail_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
