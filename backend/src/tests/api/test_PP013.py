"""tests/api/test_PP013.py"""

import pytest
import test_PP013_params
from fastapi import status
from services.output_service import OutputService


@pytest.mark.parametrize(
    "mock_put_user_setting, request_json, expected", test_PP013_params.test_PP013
)
def test_PP013(mock_put_user_setting, request_json, expected, mocker, client) -> None:
    """PP013APIテスト"""
    # モックの作成
    mocker.patch.object(OutputService, "put_user_setting").return_value = (
        mock_put_user_setting
    )

    # APIの呼び出しと結果の検証
    result = client.put(
        url="api/v1/invoices/outputs/items/",
        json=request_json,
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    "mock_put_user_setting, request_json, expected, expected_status_code",
    test_PP013_params.test_PP013_exception,
)
def test_PP013_exception(
    mock_put_user_setting, request_json, expected, expected_status_code, mocker, client
) -> None:
    """PP013API例外テスト"""
    # モックの作成
    mocker.patch.object(OutputService, "put_user_setting").side_effect = (
        mock_put_user_setting
    )

    # APIの呼び出しと結果の検証
    result = client.put(
        url="api/v1/invoices/outputs/items/",
        json=request_json,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
