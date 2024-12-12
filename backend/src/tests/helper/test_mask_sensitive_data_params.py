"""tests/helpers/test_mask_sensitive_data_params.py"""

from typing import Any


def test_mask_sensitive_data() -> list[tuple[Any, str]]:
    """mask_sensitive_dataテスト"""
    return [
        # case 1: 空文字の場合
        ("", ""),
        # case 2: Noneの場合
        (None, ""),
        # case 3: 適当な文字列の場合
        ("sensitive_data", "xxxxxxxxxxxxxx"),
    ]
