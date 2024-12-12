"""tests/services/test_s3_service_params.py"""

import os

from core.config import config
from core.constant import const


def test_upload_file_s3() -> list[tuple[str, str, str, int]]:
    """upload_file_s3テストパラメータ"""
    return [
        # case1: アップロード成功
        (
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../storage/for_test/testfile.txt",
            ),
            config.AWS_S3_PRIVATE_BUCKET or "",
            "tests/testfile.txt",
            const.PROC_RESULT_SUCCESS,
        ),
    ]


def test_upload_file_s3_exception() -> list[tuple[str, str, str, int]]:
    """upload_file_s3例外テストパラメータ"""
    return [
        # case1: アップロード失敗
        (
            "testFileName.zip",
            config.AWS_S3_PRIVATE_BUCKET or "",
            "tests/testfile.txt",
            const.PROC_RESULT_FAILED,
        ),
    ]


def test_download_file_s3() -> list[tuple[str, str, str, int]]:
    """download_file_s3テストパラメータ"""
    return [
        # case1: ダウンロード成功
        (
            config.AWS_S3_PRIVATE_BUCKET or "",
            "tests/testfile.txt",
            "testfile.txt",
            const.PROC_RESULT_SUCCESS,
        ),
    ]


def test_download_file_s3_exception() -> list[tuple[str, str, str, int]]:
    """download_file_s3例外テストパラメータ"""
    return [
        # case1: ダウンロード失敗
        (
            config.AWS_S3_PRIVATE_BUCKET or "",
            "tests/testfile.txt",
            "testfile.txt",
            const.PROC_RESULT_FAILED,
        ),
    ]
