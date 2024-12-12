"""tests/api/test_PP018.py"""

import pytest
import test_PP018_params
from fastapi import status
from models import PaymentCode
from services.company_service import CompanyService
from services.setting_service import SettingService


@pytest.mark.parametrize(
    "mock_company_info, mock_integration_company_ids, mock_put_payment_code_list, request_json, expected",
    test_PP018_params.test_PP018,
)
def test_PP018(
    mock_company_info,
    mock_integration_company_ids,
    mock_put_payment_code_list,
    request_json,
    expected,
    mocker,
    client,
) -> None:
    """PP018APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_integration_company_ids
    )
    mocker.patch.object(SettingService, "put_payment_code_list").return_value = (
        mock_put_payment_code_list
    )

    # APIの呼び出しと結果の検証
    result = client.put(
        url="api/v1/setting/payment_code",
        json=request_json,
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    mock_company_info,
    mock_integration_company_ids,
    mock_put_payment_code_list,
    request_json,
    expected,
    expected_status_code
    """,
    test_PP018_params.test_PP018_exception,
)
def test_PP018_exception(
    mock_company_info,
    mock_integration_company_ids,
    mock_put_payment_code_list,
    request_json,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP018API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_integration_company_ids
    ]
    mocker.patch.object(SettingService, "put_payment_code_list").side_effect = [
        mock_put_payment_code_list
    ]

    # APIの呼び出しと結果の検証
    result = client.put(
        url="api/v1/setting/payment_code",
        json=request_json,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
