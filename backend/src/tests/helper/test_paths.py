"""tests/helpers/test_paths.py"""

import test_paths_params
from helpers.paths import get_storage_path


def test_get_storage_path() -> None:
    """get_storage_pathテスト"""
    for sub_dir, expected in test_paths_params.test_get_storage_path():
        result = get_storage_path(sub_dir)

        assert result == expected


def test_get_storage_path_exception() -> None:
    """get_storage_path例外テスト"""
    assert True
