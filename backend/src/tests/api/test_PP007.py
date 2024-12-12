"""tests/api/test_PP007.py"""

import pytest
import test_PP007_params
from fastapi import status
from services.company_service import CompanyService
from services.download_service import DownloadService


@pytest.mark.skip(
    reason="臨時対応したため、Skip / PEPPOL_RECEIVE-314 外貨での小数点以下の表示(臨時対応)"
)
@pytest.mark.parametrize(
    "invoice_id, mock_company_info, mock_integration_company_ids, mock_preview_data, expected",
    test_PP007_params.test_PP007(),
)
def test_PP007(
    invoice_id,
    mock_company_info,
    mock_integration_company_ids,
    mock_preview_data,
    expected,
    mocker,
    client,
) -> None:
    """PP007APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_integration_company_ids
    )
    mocker.patch.object(DownloadService, "get_preview_data").return_value = (
        mock_preview_data
    )
    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/downloads/previews/" + str(invoice_id))

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    "invoice_id, mock_company_info, mock_integration_company_ids, mock_preview_data, expected,expected_status_code",
    test_PP007_params.test_PP007_exception,
)
def test_PP007_exception(
    invoice_id,
    mock_company_info,
    mock_integration_company_ids,
    mock_preview_data,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP007API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_integration_company_ids
    ]
    mocker.patch.object(DownloadService, "get_preview_data").side_effect = [
        mock_preview_data
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/downloads/previews/" + str(invoice_id))

    assert result.status_code == expected_status_code
    assert result.json() == expected
