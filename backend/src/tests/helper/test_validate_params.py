"""tests/helpers/test_validate_params.py"""

from typing import Any

import pendulum
from fastapi.exceptions import RequestValidationError
from pendulum.datetime import DateTime


def test_create_validate_error_data() -> list[tuple[str, str, list[dict[str, Any]]]]:
    """create_validate_error_dataテスト"""
    return [
        # case 1: メッセージが空の場合
        ("", "", [{"type": "value_error", "loc": ("query", ""), "msg": ""}]),
        # case 2: メッセージが指定された場合
        (
            "message",
            "location",
            [{"type": "value_error", "loc": ("query", "location"), "msg": "message"}],
        ),
    ]


def test_validate_date() -> list[tuple[str, str, DateTime | None]]:
    """validate_dateテスト"""
    return [
        # case 1: 日付が空の場合
        ("", "", None),
        # case 2: 日付が指定された場合
        ("2022-01-01", "", pendulum.datetime(2022, 1, 1)),
    ]


def test_validate_date_exception() -> list[tuple[str, str, dict]]:
    """validate_date例外テスト"""
    return [
        # case 1: 日付が不正な場合
        (
            "2022-01-32",
            "location",
            {
                "exception": RequestValidationError,
                "value": [
                    {
                        "type": "value_error",
                        "loc": ("query", "location"),
                        "msg": "day is out of range for month",
                    }
                ],
            },
        ),
    ]


def test_validate_datetime() -> list[tuple[str, str, DateTime | None]]:
    """validate_datetimeテスト"""
    return [
        # case 1: 日時が空の場合
        ("", "", None),
        # case 2: 日時が指定された場合
        ("2022-01-01 00:00", "", pendulum.datetime(2022, 1, 1)),
    ]


def test_validate_datetime_exception() -> list[tuple[str, str, dict]]:
    """validate_datetime例外テスト"""
    return [
        # case 1: 日時が不正な場合
        (
            "2022-01-32 00:00",
            "location",
            {
                "exception": RequestValidationError,
                "value": [
                    {
                        "type": "value_error",
                        "loc": ("query", "location"),
                        "msg": "day is out of range for month",
                    }
                ],
            },
        ),
    ]


def test_validate_company_infos_id() -> list[tuple[int, list[int], None]]:
    """validate_company_infos_idテスト"""
    return [
        # case 1: 企業情報IDが存在する場合
        (1, [1, 2], None),
    ]


def test_validate_company_infos_id_exception() -> list[tuple[int, list[int], dict]]:
    """validate_company_infos_id例外テスト"""
    return [
        # case 1: 企業情報IDが存在しない場合
        (
            3,
            [1, 2],
            {
                "exception": RequestValidationError,
                "value": [
                    {
                        "type": "value_error",
                        "loc": ("query", "company_infos_id"),
                        "msg": "Not applicable to own company or combined company",
                    }
                ],
            },
        ),
    ]
