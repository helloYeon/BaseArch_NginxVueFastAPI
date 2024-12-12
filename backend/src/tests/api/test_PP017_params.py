"""tests/api/test_PP017_params.py"""
import logging

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.setting.payment_code import BaseItem, GetResponseItem, ItemResponse
from core.message import messages
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo

test_PP017 = [
    # case 1 : 支払先コード一覧の取得確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        GetResponseItem(
            companyInfosId=1,
            items=[
                BaseItem(
                    peppolId="1234:unittestPeppolId", paymentCode="testPaymentCode"
                )
            ],
        ),
        1,
        ItemResponse(
            header=Header(code="", message=""),
            payload=GetResponseItem(
                companyInfosId=1,
                items=[
                    BaseItem(
                        peppolId="1234:unittestPeppolId", paymentCode="testPaymentCode"
                    )
                ],
            ),
        ).model_dump(mode="json"),
    )
]

test_PP017_exception = [
    # case 1 : I0001 company_infos_idパラメータが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        GetResponseItem(
            companyInfosId=1,
            items=[
                BaseItem(
                    peppolId="1234:unittestPeppolId", paymentCode="testPaymentCode"
                )
            ],
        ),
        "test",
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="company_infos_id is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001 company_infos_idパラメータの値が統合企業と所属企業のIDに存在しない値
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        GetResponseItem(
            companyInfosId=1,
            items=[
                BaseItem(
                    peppolId="1234:unittestPeppolId", paymentCode="testPaymentCode"
                )
            ],
        ),
        999,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="company_infos_id is Not applicable to own company or combined company",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
    (
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        [1],
        GetResponseItem(
            companyInfosId=1,
            items=[
                BaseItem(
                    peppolId="1234:unittestPeppolId", paymentCode="testPaymentCode"
                )
            ],
        ),
        1,
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
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
        1,
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
