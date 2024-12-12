"""tests/api/test_PP014_params.py"""
import json
import logging

from api.v1.schemas.admin.access import BaseItem, ItemResponse
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from core.message import messages
from enums import Access
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo, UserAccessControl

test_PP014 = [
    # case 1 : ユーザーアクセス設定テーブルの一覧の取得を確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        [
            BaseItem(
                esCompanyId=1,
                userId=1,
                isDeny=Access.IS_DENY,
                lastName="unittestLastName",
                firstName="unittestFirstName",
                loginId="unittestLoginId",
            )
        ],
        ItemResponse(
            header=Header(code="", message=""),
            payload=[
                BaseItem(
                    esCompanyId=1,
                    userId=1,
                    isDeny=Access.IS_DENY,
                    lastName="unittestLastName",
                    firstName="unittestFirstName",
                    loginId="unittestLoginId",
                )
            ],
        ).model_dump(mode="json"),
    )
]

test_PP014_exception = [
    # case 1 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
    (
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        [1],
        [
            BaseItem(
                esCompanyId=1,
                userId=1,
                isDeny=Access.IS_DENY,
                lastName="unittestLastName",
                firstName="unittestFirstName",
                loginId="unittestLoginId",
            )
        ],
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : E0007 ユーザー情報一括取得APIエラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_GET_USERS_DATA_MESSAGE,
        ),
        ErrorModel(
            header=Header(
                code=messages.FAILED_GET_USERS_DATA_MESSAGE.code,
                message=messages.FAILED_GET_USERS_DATA_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    # case 3 : E0008 user_access_controls更新エラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE,
            extra={
                "response_data": {
                    "error": "test",
                    "es_company_id": 1,
                    "insert_users": json.dumps(
                        UserAccessControl(
                            esCompanyId=1,
                            userId=1,
                            isDeny=Access.IS_DENY,
                            lastName="unittestLastName",
                            firstName="unittestFirstName",
                            loginId="unittestLoginId",
                        ),
                        default=str,
                    ),
                }
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE.code,
                message=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    # case 4 : E9999 サーバーエラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        ErrorModel(
            header=Header(
                code=messages.INTERNAL_SERVER_ERROR.code,
                message=messages.INTERNAL_SERVER_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
]
