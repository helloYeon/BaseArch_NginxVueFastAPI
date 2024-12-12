"""tests/api/test_PP014.py"""

import pytest
import test_PP014_params
from fastapi import status
from services.admin_service import AdminService
from services.company_service import CompanyService


@pytest.mark.parametrize(
    "mock_company_info, mock_integration_company_ids, mock_admin_access_setting, expected",
    test_PP014_params.test_PP014,
)
def test_PP014(
    mock_company_info,
    mock_integration_company_ids,
    mock_admin_access_setting,
    expected,
    mocker,
    client,
) -> None:
    """PP014APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_integration_company_ids
    )
    mocker.patch.object(AdminService, "get_admin_access_setting").return_value = (
        mock_admin_access_setting
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/admin/access")

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_integration_company_ids,
    mock_admin_access_setting,
    expected,
    expected_status_code
    """,
    test_PP014_params.test_PP014_exception,
)
def test_PP014_exception(
    mock_company_info,
    mock_integration_company_ids,
    mock_admin_access_setting,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP014API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_integration_company_ids
    ]
    mocker.patch.object(AdminService, "get_admin_access_setting").side_effect = [
        mock_admin_access_setting
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/admin/access")

    assert result.status_code == expected_status_code
    assert result.json() == expected
