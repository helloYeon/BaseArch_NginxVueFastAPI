"""tests/api/test_PP003.py"""

import pytest
import test_PP003_params
from api.v1.schemas.invoices.peppol import BaseItem
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.invoice_service import InvoiceService


@pytest.mark.parametrize(
    """
    invoice_id,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_my_invoice,
    mock_get_peppol_detail,
    expected
    """,
    test_PP003_params.test_PP003(),
)
def test_PP003(
    invoice_id: int,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_check_my_invoice: None,
    mock_get_peppol_detail: BaseItem,
    expected,
    mocker,
    client,
) -> None:
    """PP003APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(InvoiceService, "check_my_invoice").return_value = (
        mock_check_my_invoice
    )
    mocker.patch.object(InvoiceService, "get_peppol_detail").return_value = (
        mock_get_peppol_detail
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/peppol/" + str(invoice_id))

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    invoice_id,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_my_invoice,
    mock_get_peppol_detail,
    expected,
    expected_status_code
    """,
    test_PP003_params.test_PP003_exception,
)
def test_PP003_exception(
    invoice_id,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_my_invoice,
    mock_get_peppol_detail,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP003API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(InvoiceService, "check_my_invoice").return_value = (
        mock_check_my_invoice
    )
    mocker.patch.object(InvoiceService, "get_peppol_detail").side_effect = [
        mock_get_peppol_detail
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/peppol/" + str(invoice_id))

    assert result.status_code == expected_status_code
    assert result.json() == expected
