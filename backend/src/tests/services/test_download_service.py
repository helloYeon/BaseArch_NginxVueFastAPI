"""tests/services/test_download_service.py"""

import tempfile

import pytest
import test_download_service_params
from services.download_service import DownloadService


@pytest.fixture
def download_service(override_get_db) -> DownloadService:
    """DownloadServiceのインスタンスを返す"""
    service = DownloadService(override_get_db)

    return service


@pytest.mark.aws_test
def test_download_xml(download_service: DownloadService) -> None:
    """download_xmlテスト"""
    # 一時フォルダを作成
    with tempfile.TemporaryDirectory() as temp_folder:
        for (
            invoice_id,
            company_ids,
            expected,
        ) in test_download_service_params.test_download_xml():
            result = download_service.download_xml(invoice_id, temp_folder, company_ids)
            assert result == expected


@pytest.mark.aws_test
def test_download_xml_exception(download_service: DownloadService) -> None:
    """download_xml例外テスト"""
    # 一時フォルダを作成
    with tempfile.TemporaryDirectory() as temp_folder:
        for (
            invoice_id,
            company_ids,
            expected,
        ) in test_download_service_params.test_download_xml_exception():

            with pytest.raises(expected["exception"]) as exc_info:
                download_service.download_xml(invoice_id, temp_folder, company_ids)

        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_get_preview_data(download_service: DownloadService) -> None:
    """get_preview_dataテスト"""
    for (
        invoice_id,
        expected,
    ) in test_download_service_params.test_get_preview_data():
        assert download_service.get_preview_data(invoice_id) == expected


def test_get_preview_data_exception(download_service: DownloadService) -> None:
    """get_preview_data例外テスト"""
    for (
        invoice_id,
        expected,
    ) in test_download_service_params.test_get_preview_data_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            download_service.get_preview_data(invoice_id)

        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
