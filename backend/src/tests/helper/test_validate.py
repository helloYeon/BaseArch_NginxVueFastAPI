"""tests/helpers/test_validate.py"""

import helpers.validate as validate
import pytest
import test_validate_params


def test_create_validate_error_data() -> None:
    """create_validate_error_dataテスト"""
    for (
        message,
        location,
        expected,
    ) in test_validate_params.test_create_validate_error_data():
        result = validate.create_validate_error_data(message, location)

        assert result == expected


def test_create_validate_error_data_exception() -> None:
    """create_validate_error_data例外テスト"""
    assert True


def test_validate_date() -> None:
    """validate_dateテスト"""
    for (
        date_str,
        location,
        expected,
    ) in test_validate_params.test_validate_date():
        result = validate.validate_date(date_str, location)

        assert result == expected


def test_validate_date_exception() -> None:
    """validate_date例外テスト"""
    for (
        date_str,
        location,
        expected,
    ) in test_validate_params.test_validate_date_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            validate.validate_date(date_str, location)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.args[0] == expected["value"]


def test_validate_datetime() -> None:
    """validate_datetimeテスト"""
    for (
        datetime_str,
        location,
        expected,
    ) in test_validate_params.test_validate_datetime():
        result = validate.validate_datetime(datetime_str, location)

        assert result == expected


def test_validate_datetime_exception() -> None:
    """validate_datetime例外テスト"""
    for (
        datetime_str,
        location,
        expected,
    ) in test_validate_params.test_validate_datetime_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            validate.validate_datetime(datetime_str, location)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.args[0] == expected["value"]


def test_validate_company_infos_id() -> None:
    """validate_company_infos_idテスト"""
    for (
        company_infos_id,
        company_ids,
        expected,
    ) in test_validate_params.test_validate_company_infos_id():
        result = validate.validate_company_infos_id(company_infos_id, company_ids)

        assert result == expected


def test_validate_company_infos_id_exception() -> None:
    """validate_company_infos_id例外テスト"""
    for (
        company_infos_id,
        company_ids,
        expected,
    ) in test_validate_params.test_validate_company_infos_id_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            validate.validate_company_infos_id(company_infos_id, company_ids)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.args[0] == expected["value"]
