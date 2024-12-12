"""tests/services/test_admin_service_params.py"""

import pytest
import test_admin_service_params
from models import UserAccessControl
from services.admin_service import AdminService
from services.http_authenticate_service import HttpAuthenticateService


@pytest.fixture
def admin_service(override_get_db) -> AdminService:
    """AdminServiceのインスタンスを返す"""
    service = AdminService(override_get_db)

    return service


def test_fetch_bulk_user_info(admin_service: AdminService, mocker) -> None:
    """_fetch_bulk_user_infoテスト"""
    for (
        es_company_id,
        users,
        mock_res_users,
        expected,
    ) in test_admin_service_params.test_fetch_bulk_user_info():
        # モックの作成
        mocker.patch.object(HttpAuthenticateService, "send").return_value = (
            HttpAuthenticateService
        )
        mocker.patch.object(
            HttpAuthenticateService, "get_response"
        ).return_value.json.side_effect = mock_res_users

        # メソッドの呼び出しと結果の検証
        result = admin_service._fetch_bulk_user_info(es_company_id, users)

        assert result == expected


def test_fetch_bulk_user_info_exception() -> None:
    """_fetch_bulk_user_info例外テスト"""
    assert True


def test_get_admin_access_setting(
    admin_service: AdminService, mocker, override_get_db
) -> None:
    """get_admin_access_settingテスト"""
    # モックの作成
    mocker.patch.object(HttpAuthenticateService, "send").return_value = (
        HttpAuthenticateService
    )

    for (
        es_company_id,
        expected,
    ) in test_admin_service_params.test_get_admin_access_setting():

        # 外接の戻り値設定
        mocker.patch.object(
            HttpAuthenticateService, "get_response"
        ).return_value.json.return_value = {
            "users": [
                {
                    "userId": user.userId,
                    "loginId": user.loginId,
                    "lastName": user.lastName,
                    "firstName": user.firstName,
                    "esCompanyId": user.esCompanyId,
                }
                for user in expected
            ]
        }

        result = admin_service.get_admin_access_setting(es_company_id)

        assert result == expected


def test_get_admin_access_setting_exception() -> None:
    """get_admin_access_setting例外テスト"""
    assert True


def test_post_admin_access_setting(
    admin_service: AdminService, override_get_db
) -> None:
    """post_admin_access_settingテスト"""
    for (
        request,
        es_company_id,
        expected_user_access_control,
    ) in test_admin_service_params.test_post_admin_access_setting():

        admin_service.post_admin_access_setting(request, es_company_id)

        # 確認クエリ実行
        result = (
            override_get_db.query(UserAccessControl)
            .filter(
                UserAccessControl.esCompanyId == es_company_id,
                UserAccessControl.deletedAt.is_(None),
            )
            .one_or_none()
        )

        assert result.esCompanyId == expected_user_access_control.esCompanyId
        assert result.userId == expected_user_access_control.userId
        assert result.isDeny == expected_user_access_control.isDeny
        assert result.lastName == expected_user_access_control.lastName
        assert result.firstName == expected_user_access_control.firstName
        assert result.loginId == expected_user_access_control.loginId


def test_post_admin_access_setting_exception() -> None:
    """post_admin_access_setting例外テスト"""
    assert True


def test_raise_get_bulk_user_info_error(admin_service: AdminService) -> None:
    """raise_get_bulk_user_info_errorテスト"""
    for (expected,) in test_admin_service_params.test_raise_get_bulk_user_info_error():
        with pytest.raises(expected["exception"]) as exc_info:
            admin_service.raise_get_bulk_user_info_error()
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
