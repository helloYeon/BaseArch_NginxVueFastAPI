"""tests/api/test_PP017.py"""

import pytest
import test_PP017_params
from fastapi import status
from services.company_service import CompanyService
from services.setting_service import SettingService


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_integration_company_ids,
    mock_payment_code_list,
    mock_company_infos_id,
    expected
    """,
    test_PP017_params.test_PP017,
)
def test_PP017(
    mock_company_info,
    mock_integration_company_ids,
    mock_payment_code_list,
    mock_company_infos_id,
    expected,
    mocker,
    client,
) -> None:
    """PP017APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_integration_company_ids
    )
    mocker.patch.object(SettingService, "get_payment_code_list").return_value = (
        mock_payment_code_list
    )

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/setting/payment_code?company_infos_id=" + str(mock_company_infos_id)
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_integration_company_ids,
    mock_payment_code_list,
    mock_company_infos_id,
    expected,
    expected_status_code
    """,
    test_PP017_params.test_PP017_exception,
)
def test_PP017_exception(
    mock_company_info,
    mock_integration_company_ids,
    mock_payment_code_list,
    mock_company_infos_id,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP017API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_integration_company_ids
    ]
    mocker.patch.object(SettingService, "get_payment_code_list").side_effect = [
        mock_payment_code_list
    ]

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/setting/payment_code?company_infos_id=" + str(mock_company_infos_id)
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
