"""tests/api/test_PP009_params.py"""

import logging

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.status import PutResponse, PutResponseItem
from core.constant import const
from core.message import messages
from enums import IsDownload
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo

test_PP009 = [
    # case 1 : 正常にステータス更新が実行されることの確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"invoiceId": 1, "isDownload": IsDownload.DOWNLOADED},
        PutResponse(
            header=Header(code="", message=""),
            payload=PutResponseItem(success=const.PROC_RESULT_SUCCESS),
        ).model_dump(mode="json"),
    )
]

test_PP009_exception = [
    # case 1 : I0001 invoiceIdパラメーターが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"invoiceId": "test", "isDownload": IsDownload.DOWNLOADED},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoiceId is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001 isDownloadパラメーターが存在しない数字
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"invoiceId": 1, "isDownload": 2},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="isDownload is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0001 isDownloadパラメーターが文字列
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"invoiceId": 1, "isDownload": "test"},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="isDownload is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 4 : I0001 invoiceIdパラメーターが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"isDownload": IsDownload.DOWNLOADED},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoiceId is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 5 : I0001 isDownloadパラメーターが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {"invoiceId": 1},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="isDownload is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 6 : I0001 全てのパラメーターが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        None,
        {},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoiceId is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 7 : I0002 該当請求書レコードが存在しない
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_DATA_NOT_FOUND_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                }
            },
        ),
        {"invoiceId": 999, "isDownload": IsDownload.DOWNLOADED},
        ErrorModel(
            header=Header(
                code=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 8 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
    (
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        [1],
        None,
        None,
        {"invoiceId": 1, "isDownload": IsDownload.DOWNLOADED},
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 9 : E9999 サーバーエラー
    (
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        [1],
        None,
        None,
        {"invoiceId": 1, "isDownload": IsDownload.DOWNLOADED},
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
