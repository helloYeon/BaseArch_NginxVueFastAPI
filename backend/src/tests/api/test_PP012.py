"""tests/api/test_PP012.py"""

import pytest
import test_PP012_params
from fastapi import status
from services.output_service import OutputService


@pytest.mark.parametrize("mock_user_setting, expected", test_PP012_params.test_PP012)
def test_PP012(mock_user_setting, expected, mocker, client) -> None:
    """PP012APIテスト"""
    # モックの作成
    mocker.patch.object(OutputService, "get_user_setting").return_value = (
        mock_user_setting
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/outputs/items")

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    "mock_user_setting, expected, expected_status_code",
    test_PP012_params.test_PP012_exception,
)
def test_PP012_exception(
    mock_user_setting, expected, expected_status_code, mocker, client
) -> None:
    """PP012API例外テスト"""
    # モックの作成
    mocker.patch.object(OutputService, "get_user_setting").side_effect = (
        mock_user_setting
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices/outputs/items")

    assert result.status_code == expected_status_code
    assert result.json() == expected
