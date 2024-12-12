"""tests/helpers/test_is_empty.py"""

import test_is_empty_params
from helpers.is_empty import is_empty


def test_is_empty() -> None:
    """is_emptyテスト"""
    for (
        value,
        expected,
    ) in test_is_empty_params.test_is_empty():
        # メソッドの呼び出しと結果の検証
        result = is_empty(value)

        assert result == expected


def test_is_empty_exception() -> None:
    """is_empty例外テスト"""
    assert True
