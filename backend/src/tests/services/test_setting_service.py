"""tests/services/test_setting_service.py"""

import pytest
import test_setting_service_params
from services.setting_service import SettingService


@pytest.fixture
def setting_service(override_get_db) -> SettingService:
    """SettingServiceのインスタンスを返す"""
    service = SettingService(override_get_db)

    return service


def test_get_payment_code_list(setting_service: SettingService) -> None:
    """get_payment_code_listテスト"""
    for (
        company_infos_id,
        expected,
    ) in test_setting_service_params.test_get_payment_code_list():
        result = setting_service.get_payment_code_list(company_infos_id)
        assert result == expected


def test_get_payment_code_list_exception() -> None:
    """get_payment_code_list例外テスト"""
    assert True


def test_put_payment_code_list(setting_service: SettingService) -> None:
    """put_payment_code_listテスト"""
    for (
        request_body,
        expected,
    ) in test_setting_service_params.test_put_payment_code_list():
        result = setting_service.put_payment_code_list(request_body)

        assert result == expected


def test_put_payment_code_list_exception(
    mocker, setting_service: SettingService
) -> None:
    """put_payment_code_list例外テスト"""
    # モックの作成
    mocker.patch.object(
        setting_service.payment_code_repo, "delete_by_company_infos_id"
    ).side_effect = Exception

    for (
        request_body,
        expected,
    ) in test_setting_service_params.test_put_payment_code_list_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            setting_service.put_payment_code_list(request_body)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
