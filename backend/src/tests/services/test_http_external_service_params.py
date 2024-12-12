"""tests/services/test_user_service_params.py"""

from typing import Any

from fastapi import status


def test_get_session_verified() -> list[Any]:
    """[認証] 31. セッション検証API

    HttpAuthenticateService.get_session_verified()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            [
                "result",
                "userId",
                "esCompanyId",
                "isProxyLogin",
                "proxyLoginLimitOff",
                "proxyLoginEmployeeCode",
            ],
        ),
    ]


def test_get_session_verified_exception() -> list[Any]:
    """[認証] 31. セッション検証API

    HttpAuthenticateService.get_session_verified_exception()の例外テストパラメータ
    """
    return []


def test_get_user_info() -> list[Any]:
    """[認証] 40. ユーザー情報取得API

    HttpAuthenticateService.get_user_info()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["userId", "loginId", "lastName", "firstName", "esCompanyId"],
        ),
    ]


def test_get_user_info_exception() -> list[Any]:
    """[認証] 40. ユーザー情報取得API

    HttpAuthenticateService.get_user_info()の例外テストパラメータ
    """
    return []


def test_get_service_activation() -> list[Any]:
    """[認証] 41. サービスアクティベーション情報取得API

    HttpAuthenticateService.get_service_activation()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["esCompanyId", "plan", "serviceId"],
        ),
    ]


def test_get_service_activation_exception() -> list[Any]:
    """[認証] 41. サービスアクティベーション情報取得API

    HttpAuthenticateService.get_service_activation()の例外テストパラメータ
    """
    return []


def test_get_option_activation() -> list[Any]:
    """[認証] 42. オプションアクティベーション情報取得API

    HttpAuthenticateService.get_option_activation()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["esCompanyId", "message", "optionId", "serviceId"],
        ),
    ]


def test_get_option_activation_exception() -> list[Any]:
    """[認証] 42. オプションアクティベーション情報取得API

    HttpAuthenticateService.get_option_activation()の例外テストパラメータ
    """
    return []


def test_get_company_info() -> list[Any]:
    """[認証] 50. 企業情報取得API

    HttpAuthenticateService.get_company_info()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["esCompanyId", "companyName"],
        ),
    ]


def test_get_company_info_exception() -> list[Any]:
    """[認証] 50. 企業情報取得API

    HttpAuthenticateService.get_company_info()の例外テストパラメータ
    """
    return []


def test_get_peppol_id_mapping_info() -> list[Any]:
    """[認証] 100. 企業・Peppol ID紐づけ情報取得API

    HttpAuthenticateService.get_peppol_id_mapping_info()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["esCompanyId", "peppolId"],
        ),
    ]


def test_get_peppol_id_mapping_info_exception() -> list[Any]:
    """[認証] 50. 企業情報取得API

    HttpAuthenticateService.get_peppol_id_mapping_info()の例外テストパラメータ
    """
    return []


def test_get_peppol_id_related_info() -> list[Any]:
    """[認証] 110. Peppol ID情報取得API

    HttpAuthenticateService.get_peppol_id_related_info()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            ["peppolId", "apiId", "password", "authKey"],
        ),
    ]


def test_get_peppol_id_related_info_exception() -> list[Any]:
    """[認証] 110. Peppol ID情報取得API

    HttpAuthenticateService.get_peppol_id_related_info()の例外テストパラメータ
    """
    return []


def test_get_bulk_user_info() -> list[Any]:
    """[認証] 200. ユーザー情報一括取得API

    HttpAuthenticateService.get_bulk_user_info()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (
            status.HTTP_200_OK,
            [
                "userId",
                "loginId",
                "lastName",
                "firstName",
                "esCompanyId",
                "createDate",
                "updateDate",
            ],
        ),
    ]


def test_get_bulk_user_info_exception() -> list[Any]:
    """[認証] 200. ユーザー情報一括取得API

    HttpAuthenticateService.test_get_bulk_user_info_exception()の例外テストパラメータ
    """
    return []


def test_post_receive() -> list[Any]:
    """[受取] 1. API_アクセスポイント連携（受取）API

    HttpAccessPointService.post_receive()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (status.HTTP_200_OK, "application/octet-stream"),
    ]


def test_post_receive_exception() -> list[Any]:
    """[受取] 1. API_アクセスポイント連携（受取）API

    HttpAccessPointService.post_receive()の例外テストパラメータ
    """
    return []


def test_post_transform() -> list[Any]:
    """[受取] 2. 請求書・通知書データ変換(受取)API

    HttpAccessPointService.post_transform()のテストパラメータ
    """
    return [
        # case 1 : 疎通確認
        (status.HTTP_200_OK, "application/json"),
    ]


def test_post_transform_exception() -> list[Any]:
    """[受取] 2. 請求書・通知書データ変換(受取)API

    HttpAccessPointService.post_transform()の例外テストパラメータ
    """
    return []
