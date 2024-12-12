"""tests/api/test_PP016.py"""

import pytest
import test_PP016_params
from fastapi import status
from services.company_service import CompanyService


@pytest.mark.parametrize(
    "mock_company_info, mock_get_integrations, expected", test_PP016_params.test_PP016
)
def test_PP016(
    mock_company_info, mock_get_integrations, expected, mocker, client
) -> None:
    """PP016APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integrations").return_value = (
        mock_get_integrations
    )

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/company/integrations")

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    "mock_company_info, mock_get_integrations, expected, expected_status_code",
    test_PP016_params.test_PP016_exception,
)
def test_PP016_exception(
    mock_company_info,
    mock_get_integrations,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP016API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integrations").side_effect = [
        mock_get_integrations
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/company/integrations")

    assert result.status_code == expected_status_code
    assert result.json() == expected
