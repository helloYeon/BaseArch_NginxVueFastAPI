"""tests/api/test_PP006.py"""

import os
import shutil

import pytest
import test_PP006_params
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.download_service import DownloadService


def mock_download_xml(file_path, download_folder_path) -> str:
    """download_xmlモック"""
    # download_xml()内のS3からtempフォルダへのダウンロード部分をモック化
    shutil.copy2(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            file_path,
        ),
        download_folder_path,
    )
    # ファイル名をreturn_valueに設定
    return "testfile.txt"


@pytest.mark.parametrize(
    "invoice_id,mock_get_company_info,mock_get_integration_company_ids,mock_file_path,expected",
    test_PP006_params.test_PP006(),
)
def test_PP006(
    invoice_id: int,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_file_path: str,
    expected,
    mocker,
    client,
) -> None:
    """PP006APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(DownloadService, "download_xml").side_effect = (
        lambda invoice_id, download_folder_path, company_ids: mock_download_xml(
            mock_file_path, download_folder_path
        )
    )
    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/downloads/xmls?invoice_id=" + str(invoice_id))

    assert result.status_code == status.HTTP_200_OK
    assert result.content.decode("UTF-8") == expected


@pytest.mark.parametrize(
    "invoice_id,mock_get_company_info,mock_get_integration_company_ids,mock_download_xml,expected,expected_status_code",
    test_PP006_params.test_PP006_exception,
)
def test_PP006_exception(
    invoice_id: int,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_download_xml: str,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP006API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(DownloadService, "download_xml").side_effect = [
        mock_download_xml
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/downloads/xmls?invoice_id=" + str(invoice_id))

    assert result.status_code == expected_status_code
    assert result.json() == expected
