"""tests/api/test_PP002.py"""

import pytest
import test_PP002_params
from api.v1.schemas.invoice import InvoiceBaseItem
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.invoice_service import InvoiceService


@pytest.mark.skip(
    reason="臨時対応したため、Skip / PEPPOL_RECEIVE-314 外貨での小数点以下の表示(臨時対応)"
)
@pytest.mark.parametrize(
    "invoice_id,mock_get_company_info,mock_get_integration_company_ids,mock_get_invoice,expected",
    test_PP002_params.test_PP002(),
)
def test_PP002(
    invoice_id: int,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_get_invoice: InvoiceBaseItem,
    expected,
    mocker,
    client,
) -> None:
    """PP002APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(InvoiceService, "get_invoice").return_value = mock_get_invoice

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/" + str(invoice_id))

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    invoice_id,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_invoice,
    expected,
    expected_status_code
    """,
    test_PP002_params.test_PP002_exception,
)
def test_PP002_exception(
    invoice_id,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_invoice,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP002API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(InvoiceService, "get_invoice").side_effect = [mock_get_invoice]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/" + str(invoice_id))

    assert result.status_code == expected_status_code
    assert result.json() == expected
