"""tests/helpers/test_extract_filename_from_path_params.py"""


def test_extract_filename_from_path() -> list[tuple[str, str]]:
    """extract_filename_from_pathテスト"""
    return [
        # case 1 : ファイル名がある場合
        ("/path/to/file.txt", "file.txt"),
        # case 2 : ファイル名がない場合
        ("/path/to/dir/", ""),
        # case 3 : ファイル名が空文字の場合
        ("", ""),
    ]
