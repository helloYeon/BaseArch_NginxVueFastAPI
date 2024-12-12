"""tests/api/test_PP015_params.py"""
import json
import logging

from api.v1.schemas.admin.access import PostResponse, PostResponseItem
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from core.constant import const
from core.message import messages
from enums import Access
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo, UserAccessControl

test_PP015 = [
    # case 1 : ユーザーアクセス可否設定の更新を確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        PostResponse(
            header=Header(code="", message=""),
            payload=PostResponseItem(success=const.PROC_RESULT_SUCCESS),
        ).model_dump(mode="json"),
    )
]

test_PP015_exception = [
    # case 1 : I0001 esCompanyIdパラメータが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": "test",
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001 userIdパラメータが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": "test",
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0001 isDenyパラメータが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": "test",
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 4 : I0001 isDenyパラメータが存在しない数字
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": 2,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 5 : I0001 lastNameパラメータが数値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": 1,
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 6 : I0001 firstNameパラメータが数値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": 1,
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 7 : I0001 loginIdパラメータが数値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": 1,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 8 : I0001 esCompanyIdパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 9 : I0001 userIdパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 10 : I0001 isDenyパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 11 : I0001 lastNameパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 12 : I0001 firstNameパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 13 : I0001 loginIdパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 14 : I0001 dataの全てのパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {"data": [{}]},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 15 : I0001 dataパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        None,
        {},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 16 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
    (
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        None,
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 17 : E0008 user_access_controls更新エラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE,
            extra={
                "response_data": {
                    "error": "error",
                    "es_company_id": 1,
                    "insert_users": [
                        json.dumps(
                            UserAccessControl(
                                esCompanyId=1,
                                userId=1,
                                isDeny=Access.IS_DENY,
                                lastName="unittestLastName",
                                firstName="unittestFirstName",
                                loginId="unittestLoginId",
                            ),
                            default=str,
                        )
                    ],
                }
            },
        ),
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE.code,
                message=messages.FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    # case 18 : E9999 サーバーエラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        {
            "data": [
                {
                    "esCompanyId": 1,
                    "userId": 1,
                    "isDeny": Access.IS_DENY,
                    "lastName": "unittestLastName",
                    "firstName": "unittestFirstName",
                    "loginId": "unittestLoginId",
                }
            ]
        },
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
