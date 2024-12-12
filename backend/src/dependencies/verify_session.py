"""dependencies/session.py"""

import logging
from typing import Callable, Optional

import core
from core.context_user_info import user_info_context
from dependencies.services import depend_user_service
from enums import SessionResult
from exceptions import PeppolHttpException
from fastapi import Cookie, Depends, Request, status
from helpers import logger
from services.http_authenticate_service import HttpAuthenticateService as Http
from services.user_service import UserService


async def verify_session(
    request: Request,
    session_id: Optional[str] = Cookie(default=None, alias="cookies%5Fcomputer%5Fes"),
    user_service: UserService = Depends(depend_user_service),
) -> None:
    """セッションIDを検証する

    Args:
        request (Request): リクエスト
        session_id (Optional[str], optional): クッキーセッションID.
        user_service (UserService, optional): ユーザーサービス. Defaults to Depends(depend_user_service).

    Raises:
        raise_peppol_http_exception: PeppolHttpException(401)
    """
    # user_info_context.set(user_service.get_user(1))
    # return

    # クッキーがない場合は認証エラー
    if session_id is None:
        raise PeppolHttpException(
            log_level=logging.getLevelName(logging.INFO),
            status_code=status.HTTP_401_UNAUTHORIZED,
            message_model=core.messages.AUTH_NOT_FOUND,
        )

    # 31. セッション検証API
    session_info = (
        Http.get_session_verified(session_id)
        .send(
            json={
                # ローカルの場合アドグローブ東京IPを送信
                "ipAddress": (
                    "39.110.235.25"
                    if core.config.isLocal()
                    else request.headers.get("x-forwarded-for", "").split(",")[0]
                )
            },
            handle_error=raise_session_exception,
        )  # type: ignore
        .get_response()
        .json()
    )

    # resultをチェックする
    check_session_result(session_info["result"])

    # 40. ユーザー情報取得API
    user_info = (
        Http.get_user_info(session_info["userId"])
        .send(handle_error=raise_peppol_http_exception)  # type: ignore
        .get_response()
        .json()
    )

    # 41. サービスアクティベーション情報取得API
    service_activation = (
        Http.get_service_activation(user_info["esCompanyId"])
        .send(handle_error=raise_peppol_http_exception)  # type: ignore
        .get_response()
        .json()
    )

    # activation状況をチェックする
    check_activation_state(service_activation)

    # 42. オプションアクティベーション情報取得API / オプションアクティベーションなしのため、404をスロー
    (
        Http.get_option_activation(user_info["esCompanyId"])
        .send(handle_error=raise_peppol_http_exception)  # type: ignore
        .get_response()
        .json()
    )

    # 50. 企業情報取得API
    company_info = (
        Http.get_company_info(user_info["esCompanyId"])
        .send(handle_error=raise_peppol_http_exception)  # type: ignore
        .get_response()
        .json()
    )

    # 企業情報及びユーザー情報をDBに登録もしくは更新
    user_info = user_service.upsert_login_info(
        {
            "userId": user_info["userId"],
            "sessionId": session_id,
            "esCompanyId": user_info["esCompanyId"],
            "lastName": user_info["lastName"],
            "firstName": user_info["firstName"],
            "companyName": company_info["companyName"],
        }
    )

    company_info = user_service.get_user_company(user_info.userId)

    # アクセス不可ユーザーに設定されていれば認証エラー
    if user_service.is_deny_user(company_info.esCompanyId, user_info.userId):
        raise_peppol_http_exception()

    # ユーザー情報をコンテキストにセット
    user_info_context.set(user_info)

    # リクエストステートにユーザー情報と企業情報をセット
    request.state.user_info = user_info.__dict__
    request.state.company_info = company_info.__dict__


def raise_peppol_http_exception(
    write_log: Optional[Callable] = None,
    exception: Optional[Exception] = None,
) -> PeppolHttpException:
    """PeppolHttpExceptionを返す

    Args:
        write_log (Optional[Callable], optional): ログ出力. Defaults to None.
        exception (Optional[Exception], optional): 外接例外

    Raises:
        PeppolHttpException: 認証エラー

    """
    if write_log:
        write_log()

    raise PeppolHttpException(
        log_level=logging.getLevelName(logging.INFO),
        status_code=status.HTTP_401_UNAUTHORIZED,
        message_model=core.messages.USER_AUTHENTICATION_FAILED,
    )


def raise_session_exception() -> None:
    """セッション検証APIの例外処理

    Raises:
        PeppolHttpException: 認証エラー
    """
    if Http.get_response().status_code == status.HTTP_404_NOT_FOUND:
        raise PeppolHttpException(
            log_level=logging.getLevelName(logging.INFO),
            status_code=status.HTTP_401_UNAUTHORIZED,
            message_model=core.messages.AUTH_NOT_FOUND,
        )

    raise PeppolHttpException(
        log_level=logging.getLevelName(logging.ERROR),
        status_code=status.HTTP_401_UNAUTHORIZED,
        message_model=core.messages.USER_AUTHENTICATION_FAILED,
    )


def check_session_result(result: str) -> None:
    """セッション検証APIのresultチェック

    Args:
        result (str): result

    Raises:
        PeppolHttpException: 認証エラー
    """
    if result == SessionResult.VALID:
        # セッションは有効
        return

    message_model = core.messages.USER_AUTHENTICATION_FAILED

    # 異常系の場合
    if result == SessionResult.IP_ADDRESS_NOT_ALLOWED:
        # 許可されていないIPアドレスからのアクセス
        message_model = core.messages.AUTH_IP_ADDRESS_NOT_ALLOWED
    elif result == SessionResult.SESSION_TIMED_OUT:
        # セッションタイムアウト
        message_model = core.messages.AUTH_SESSION_TIMED_OUT
    elif result == SessionResult.PASSWORD_EXPIRED:
        # パスワード有効期限切れ
        message_model = core.messages.AUTH_PASSWORD_EXPIRED
    elif result == SessionResult.LOGOUT_FORCED:
        # 強制ログアウト
        message_model = core.messages.AUTH_LOGOUT_FORCED

    raise PeppolHttpException(
        log_level=logging.getLevelName(logging.INFO),
        status_code=status.HTTP_401_UNAUTHORIZED,
        message_model=message_model,
    )


def check_activation_state(activation_state: dict) -> None:
    """アクティベーション状態を確認し、無料の場合、認証エラーをスルー
        有料状態は「plan:paid」
        上記以外は全て無料とする

    Args:
        activation_state (dict): アクティベーション状態を表す辞書

    """
    if activation_state["plan"] != "paid":
        raise_peppol_http_exception()
