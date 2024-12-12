"""tests/api/test_PP006_params.py"""

import logging
import os

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from core.message import messages
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo


def test_PP006() -> list[tuple[int, CompanyInfo, list[int], str, str]]:
    """PP006APIテストパラメータ"""
    # 期待値
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../storage/for_test/testfile.txt",
        ),
        "rt",
    ) as file:
        expected = file.read()

    return [
        # case 1 : invoice_id:1のxmlファイルダウンロード
        (
            1,
            CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
            [1],
            "../../storage/for_test/testfile.txt",
            expected,
        )
    ]


test_PP006_exception = [
    (
        # case 1 : I0001: invoice_idパラメーターが数値ではない
        "a",
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoice_id is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 2 : I0002: 該当請求書レコードが存在しない
        1,
        CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
        [1],
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
        ErrorModel(
            header=Header(
                code=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 3 : I0004: 指定したcompany_infos_idが所属企業、結合企業に該当しない
        1,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 4 : E0003: ファイル名取得失敗
        1,
        CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_GET_FILE_NAME_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                    "download_folder_path": "download_folder_path",
                },
                "params": {
                    "s3_full_path": "s3_full_path",
                    "filename": "filename",
                },
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.FAILED_GET_FILE_NAME_MESSAGE.code,
                message=messages.FAILED_GET_FILE_NAME_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    (
        # case 5 : E0004: S3 XMLダウンロード失敗
        1,
        CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
        [1],
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.XML_DOWNLOAD_FAILED_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                    "download_folder_path": "download_folder_path",
                },
                "params": {
                    "s3_full_path": "s3_full_path",
                    "filename": "filename",
                    "download_file_path": "download_file_path",
                },
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.XML_DOWNLOAD_FAILED_MESSAGE.code,
                message=messages.XML_DOWNLOAD_FAILED_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    (
        # case 6 : E9999: サーバーエラー
        1,
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        None,
        None,
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
