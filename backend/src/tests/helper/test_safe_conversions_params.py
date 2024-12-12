"""tests/helpers/test_safe_conversions_params.py"""

from typing import Any


def test_safe_float_conversion() -> list[tuple[str | int | float | None, Any, Any]]:
    """safe_float_conversionテストパラメータ"""
    return [
        # case 1 : valueがstr
        ("1.0", 0, 1.0),
        # case 2 : valueがNone
        (None, None, None),
        # case 3 : valueがint
        (1, 0, 1.0),
        # case 4 : valueがfloat
        (1.0, 0, 1.0),
        # case 5 : valueが文字列
        ("test", 0, 0),
    ]
