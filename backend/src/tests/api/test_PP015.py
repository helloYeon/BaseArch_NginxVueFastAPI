"""tests/api/test_PP015.py"""

import pytest
import test_PP015_params
from fastapi import status
from services.admin_service import AdminService
from services.company_service import CompanyService


@pytest.mark.parametrize(
    "mock_company_info, mock_post_admin_access_setting, request_json, expected",
    test_PP015_params.test_PP015,
)
def test_PP015(
    mock_company_info,
    mock_post_admin_access_setting,
    request_json,
    expected,
    mocker,
    client,
) -> None:
    """PP015APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(AdminService, "post_admin_access_setting").return_value = (
        mock_post_admin_access_setting
    )

    # APIの呼び出しと結果の検証
    result = client.post(
        url="api/v1/admin/access",
        json=request_json,
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_post_admin_access_setting,
    request_json,
    expected,
    expected_status_code
    """,
    test_PP015_params.test_PP015_exception,
)
def test_PP015_exception(
    mock_company_info,
    mock_post_admin_access_setting,
    request_json,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP015API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(AdminService, "post_admin_access_setting").side_effect = [
        mock_post_admin_access_setting
    ]

    # APIの呼び出しと結果の検証
    result = client.post(
        url="api/v1/admin/access",
        json=request_json,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
