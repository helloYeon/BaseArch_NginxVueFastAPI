"""tests/api/test_PP021.py"""

import pytest
import test_PP021_params
from fastapi import status
from services.user_service import UserService


@pytest.mark.parametrize(
    """
    request_body,
    mock_patch_user_status,
    expected
    """,
    test_PP021_params.test_PP021,
)
def test_PP021(
    request_body,
    mock_patch_user_status,
    expected,
    mocker,
    client,
) -> None:
    """PP021APIテスト"""
    # モックの作成
    mocker.patch.object(UserService, "patch_user_status").return_value = (
        mock_patch_user_status
    )

    # APIの呼び出しと結果の検証
    result = client.patch(
        "api/v1/users/me/status",
        json=request_body,
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    request_body,
    mock_patch_user_status,
    expected,
    expected_status_code
    """,
    test_PP021_params.test_PP021_exception,
)
def test_PP021_exception(
    request_body,
    mock_patch_user_status,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP021API例外テスト"""
    # モックの作成
    mocker.patch.object(UserService, "patch_user_status").side_effect = [
        mock_patch_user_status
    ]

    # APIの呼び出しと結果の検証
    result = client.patch(
        "api/v1/users/me/status",
        json=request_body,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
