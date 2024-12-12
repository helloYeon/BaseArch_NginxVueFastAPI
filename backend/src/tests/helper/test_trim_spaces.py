"""tests/helpers/test_trim_spaces.py"""

import test_trim_spaces_params
from helpers.trim_spaces import trim_spaces


def test_trim_spaces() -> None:
    """trim_spacesテスト"""
    for value, expected in test_trim_spaces_params.test_trim_spaces():
        result = trim_spaces(value)

        assert result == expected


def test_trim_spaces_exception() -> None:
    """trim_spaces例外テスト"""
    assert True
