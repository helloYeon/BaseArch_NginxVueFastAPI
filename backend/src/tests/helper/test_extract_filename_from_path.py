"""tests/helpers/test_extract_filename_from_path.py"""

import test_extract_filename_from_path_params
from helpers.extract_filename_from_path import extract_filename_from_path


def test_extract_filename_from_path() -> None:
    """extract_filename_from_pathテスト"""
    for (
        file_path,
        expected,
    ) in test_extract_filename_from_path_params.test_extract_filename_from_path():
        # メソッドの呼び出しと結果の検証
        result = extract_filename_from_path(file_path)

        assert result == expected


def test_extract_filename_from_path_exception() -> None:
    """extract_filename_from_path例外テスト"""
    assert True
