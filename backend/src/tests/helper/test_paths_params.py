"""tests/helpers/test_paths_params.py"""

from helpers.paths import root_path


def test_get_storage_path() -> list[tuple[str, str]]:
    """get_storage_pathテスト"""
    return [
        # case 1 : サブディレクトリが空の場合
        ("", f"{root_path}/storage/"),
        # case 2 : サブディレクトリが指定された場合
        ("sub_dir", f"{root_path}/storage/sub_dir"),
    ]
