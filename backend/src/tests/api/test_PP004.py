"""tests/api/test_PP004.py"""

import pytest
import test_PP004_params
from api.v1.schemas.invoices.details import BaseItem
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.invoice_detail_service import InvoiceDetailService


@pytest.mark.parametrize(
    """
    invoice_detail_id,
    mock_get_company_info,
    mock_check_my_invoice_detail,
    mock_get_integration_company_ids,
    mock_get_invoice_detail,expected
    """,
    test_PP004_params.test_PP004(),
)
def test_PP004(
    invoice_detail_id: int,
    mock_get_company_info: CompanyInfo,
    mock_check_my_invoice_detail: None,
    mock_get_integration_company_ids: list[int],
    mock_get_invoice_detail: BaseItem,
    expected,
    mocker,
    client,
) -> None:
    """PP004APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(
        InvoiceDetailService, "check_my_invoice_detail"
    ).return_value = mock_check_my_invoice_detail
    mocker.patch.object(InvoiceDetailService, "get_invoice_detail").return_value = (
        mock_get_invoice_detail
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/details/" + str(invoice_detail_id))

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    invoice_detail_id,
    mock_get_company_info,
    mock_check_my_invoice_detail,
    mock_get_integration_company_ids,
    mock_get_invoice_detail,
    expected,
    expected_status_code
    """,
    test_PP004_params.test_PP004_exception,
)
def test_PP004_exception(
    invoice_detail_id,
    mock_get_company_info,
    mock_check_my_invoice_detail,
    mock_get_integration_company_ids,
    mock_get_invoice_detail,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP004API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(InvoiceDetailService, "check_my_invoice_detail").side_effect = [
        mock_check_my_invoice_detail
    ]
    mocker.patch.object(InvoiceDetailService, "get_invoice_detail").side_effect = [
        mock_get_invoice_detail
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/details/" + str(invoice_detail_id))

    assert result.status_code == expected_status_code
    assert result.json() == expected
