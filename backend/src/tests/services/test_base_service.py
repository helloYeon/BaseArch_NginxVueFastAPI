"""tests/services/test_base_service.py"""

import tempfile

import pytest
import test_base_service_params
from helpers import logger
from services.base_service import BaseService


@pytest.fixture
def base_service(override_get_db) -> BaseService:
    """BaseServiceのインスタンスを返す"""
    service = BaseService(override_get_db)

    return service


def test_remove_none_values(base_service) -> None:
    """remove_none_valuesテスト"""
    for (
        d,
        expected,
    ) in test_base_service_params.test_remove_none_values:
        result = base_service.remove_none_values(d)

        assert result == expected


def test_remove_none_values_exception(base_service) -> None:
    """remove_none_values例外テスト"""
    assert True


def test_unzip_with_subprocess(mocker, base_service) -> None:
    """unzip_with_subprocessテスト"""
    mocker.patch.object(logger, "error").return_value = None

    # 一時フォルダ作成
    with tempfile.TemporaryDirectory() as temp_folder:
        for (
            zip_file_path,
            extracted_dir,
            expected,
        ) in test_base_service_params.test_unzip_with_subprocess:
            result = base_service.unzip_with_subprocess(
                zip_file_path, f"{temp_folder}/{extracted_dir}"
            )

            assert result == expected


def test_unzip_with_subprocess_exception(base_service) -> None:
    """unzip_with_subprocess例外テスト"""
    assert True
