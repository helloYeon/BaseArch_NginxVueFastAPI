"""tests/helpers/test_is_empty_params.py"""

from typing import Any


def test_is_empty() -> list[tuple[Any, bool]]:
    """is_emptyテスト"""
    return [
        # case 1 : 空文字の場合
        ("", True),
        # case 2 : Noneの場合
        (None, True),
        # case 3 : 半角スペースのみの文字列の場合
        (" ", True),
        # case 4 : 全角スペースのみの文字列の場合
        ("　", True),
        # case 5 : 空ディクショナリの場合
        ({}, True),
        # case 6 : 空配列の場合
        ([], True),
        # case 7 : 半角スペースを含む文字列の場合
        (" a ", False),
        # case 8 : 全角スペースを含む文字列の場合
        ("　a　", False),
        # case 9 : ディクショナリに要素がある場合
        ({"key": "value"}, False),
        # case 10 : 配列に要素がある場合
        ([1, 2, 3], False),
    ]
