"""tests/api/test_PP011.py"""

import pytest
import test_PP011_params
from fastapi import status
from services.company_service import CompanyService
from services.invoice_service import InvoiceService


@pytest.mark.parametrize(
    "mock_company_info, mock_company_ids, mock_check_my_invoice, mock_update_open_status, request_json, expected",
    test_PP011_params.test_PP011,
)
def test_PP011(
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_open_status,
    request_json,
    expected,
    mocker,
    client,
) -> None:
    """PP011APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_company_ids
    )
    mocker.patch.object(InvoiceService, "check_my_invoice").return_value = (
        mock_check_my_invoice
    )
    mocker.patch.object(InvoiceService, "update_open_status").return_value = (
        mock_update_open_status
    )

    # APIの呼び出しと結果の検証
    result = client.put(url="api/v1/invoices/status/open", json=request_json)

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_open_status,
    request_json,
    expected,
    expected_status_code
    """,
    test_PP011_params.test_PP011_exception,
)
def test_PP011_exception(
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_open_status,
    request_json,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP011API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = (
        mock_company_ids
    )
    mocker.patch.object(InvoiceService, "check_my_invoice").return_value = (
        mock_check_my_invoice
    )
    mocker.patch.object(InvoiceService, "update_open_status").side_effect = [
        mock_update_open_status
    ]

    # APIの呼び出しと結果の検証
    result = client.put(url="api/v1/invoices/status/open", json=request_json)

    assert result.status_code == expected_status_code
    assert result.json() == expected
