"""tests/api/test_PP009.py"""

import pytest
import test_PP009_params
from fastapi import status
from services.company_service import CompanyService
from services.invoice_service import InvoiceService


@pytest.mark.parametrize(
    "mock_company_info, mock_company_ids, mock_check_my_invoice, mock_update_download_status, request_json, expected",
    test_PP009_params.test_PP009,
)
def test_PP009(
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_download_status,
    request_json,
    expected,
    mocker,
    client,
) -> None:
    """PP009APIテスト"""
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

    mocker.patch.object(InvoiceService, "update_download_status").return_value = (
        mock_update_download_status
    )

    # APIの呼び出しと結果の検証
    result = client.put(url="api/v1/invoices/status/download", json=request_json)

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_download_status,
    request_json,
    expected,
    expected_status_code
    """,
    test_PP009_params.test_PP009_exception,
)
def test_PP009_exception(
    mock_company_info,
    mock_company_ids,
    mock_check_my_invoice,
    mock_update_download_status,
    request_json,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP009API例外テスト"""
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
    mocker.patch.object(InvoiceService, "update_download_status").side_effect = [
        mock_update_download_status
    ]

    # APIの呼び出しと結果の検証
    result = client.put(url="api/v1/invoices/status/download", json=request_json)

    assert result.status_code == expected_status_code
    assert result.json() == expected
