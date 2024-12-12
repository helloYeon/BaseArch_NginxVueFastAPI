"""tests/services/test_s3_service.py"""

import os
import tempfile

import pytest
import test_s3_service_params
from services.s3_service import S3Service


@pytest.fixture
def s3_service() -> S3Service:
    """S3Serviceのインスタンスを返す"""
    service = S3Service()

    return service


@pytest.mark.aws_test
def test_upload_file_s3(s3_service: S3Service) -> None:
    """upload_file_s3テスト"""
    for (
        Filename,
        Bucket,
        Key,
        expected,
    ) in test_s3_service_params.test_upload_file_s3():
        result = s3_service.upload_file_s3(Filename, Bucket, Key)

        assert result == expected


@pytest.mark.aws_test
def test_upload_file_s3_exception(mocker, s3_service: S3Service) -> None:
    """upload_file_s3例外テスト"""
    # モックの作成
    mocker.patch.object(s3_service.s3, "upload_file").side_effect = Exception

    for (
        Filename,
        Bucket,
        Key,
        expected,
    ) in test_s3_service_params.test_upload_file_s3_exception():
        result = s3_service.upload_file_s3(Filename, Bucket, Key)

        assert result == expected


@pytest.mark.aws_test
def test_download_file_s3(mocker, s3_service: S3Service) -> None:
    """download_file_s3テスト"""
    # 一時フォルダを作成
    with tempfile.TemporaryDirectory() as temp_folder:
        for (
            bucket,
            key,
            download_file_path,
            expected,
        ) in test_s3_service_params.test_download_file_s3():
            result = s3_service.download_file_s3(
                bucket, key, os.path.join(temp_folder, download_file_path)
            )

            assert result == expected


@pytest.mark.aws_test
def test_download_file_s3_exception(mocker, s3_service: S3Service) -> None:
    """download_file_s3例外テスト"""
    # モックの作成
    mocker.patch.object(s3_service.s3, "download_file").side_effect = Exception

    # 一時フォルダを作成
    with tempfile.TemporaryDirectory() as temp_folder:
        for (
            bucket,
            key,
            download_file_path,
            expected,
        ) in test_s3_service_params.test_download_file_s3_exception():
            result = s3_service.download_file_s3(
                bucket, key, os.path.join(temp_folder, download_file_path)
            )

            assert result == expected
