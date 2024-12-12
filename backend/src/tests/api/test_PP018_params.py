"""tests/api/test_PP018_params.py"""
import logging

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.setting.payment_code import PutResponse, PutResponseItem
from core.constant import const
from core.message import messages
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo

test_PP018 = [
    # case 1 : 正常に支払先コード一覧が更新されることの確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {"peppolId": "1234:unittestPeppolId", "paymentCode": "testPaymentCode"},
            ],
        },
        PutResponse(
            header=Header(code="", message=""),
            payload=PutResponseItem(success=const.PROC_RESULT_SUCCESS),
        ).model_dump(mode="json"),
    )
]


test_PP018_exception = [
    # case 1 : I0001 companyInfosIdパラメータが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": "test",
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="companyInfosId is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001 companyInfosIdパラメータをlistに含まれていないidを指定
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 2,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="company_infos_id is Not applicable to own company or combined company",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0001 peppolIdパラメータが数値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": 1,
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 4 : I0001 peppolIdパラメータの数字4桁部分が３桁のみ
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "123:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="peppolId is Must be pattern '{four-digit number}:{one-byte alphanumeric characters}' ",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 5 : I0001 peppolIdパラメータの数字4桁部分が5桁
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "12345:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="peppolId is Must be pattern '{four-digit number}:{one-byte alphanumeric characters}' ",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 6 : I0001 peppolIdパラメータの右側が半角英数字以外の文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:テスト",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="peppolId is Must be pattern '{four-digit number}:{one-byte alphanumeric characters}' ",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 7 : I0001 paymentCodeパラメータが数値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": 1,
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 8 : I0001 支払先コード一覧更新リクエストでpaymentCodeが15文字以下でない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testtesttesttest",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="paymentCode is Must be less than 15 characters",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 9 : I0001 支払先コード一覧更新リクエストでpaymentCodeに半角英数字以外の文字が含まれている
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "テスト",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="paymentCode is Must be one-byte alphanumeric characters only",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 10 : I0001 companyInfosIdパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="companyInfosId is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 11 : I0001 peppolIdパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 12 : I0001 paymentCodeパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 13 : I0001 peppolIdパラメータとpaymentCodeパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [{}],
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 14 : I0001 itemsパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {
            "companyInfosId": 1,
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="items is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 15 : I0001 全てのパラメータが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        {},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="companyInfosId is Field required",
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
        [1],
        None,
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
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
    # case 17 : E0009 payment_codes更新エラー
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_UPDATE_PAYMENT_CODES_MESSAGE,
            extra={
                "response_data": {
                    "error": "error",
                    "insert_payment_codes": [
                        {
                            "companyInfosId": 1,
                            "peppolId": "1234:unittestPeppolId",
                            "paymentCode": "testPaymentCode",
                        }
                    ],
                }
            },
        ),
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
        },
        ErrorModel(
            header=Header(
                code=messages.FAILED_UPDATE_PAYMENT_CODES_MESSAGE.code,
                message=messages.FAILED_UPDATE_PAYMENT_CODES_MESSAGE.message,
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
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        {
            "companyInfosId": 1,
            "items": [
                {
                    "peppolId": "1234:unittestPeppolId",
                    "paymentCode": "testPaymentCode",
                },
            ],
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
