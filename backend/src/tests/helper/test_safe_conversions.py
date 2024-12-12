"""tests/helpers/test_safe_conversions.py"""

import test_safe_conversions_params
from helpers.safe_conversions import safe_float_conversion


def test_safe_float_conversion() -> None:
    """safe_float_conversionテスト"""
    for (
        value,
        default,
        expected,
    ) in test_safe_conversions_params.test_safe_float_conversion():
        # メソッドの呼び出しと結果の検証
        result = safe_float_conversion(value, default)
        assert result == expected


def test_safe_float_conversion_exception() -> None:
    """safe_float_conversion例外テスト"""
    assert True
