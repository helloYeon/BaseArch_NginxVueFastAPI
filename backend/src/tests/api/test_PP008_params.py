"""tests/api/test_PP008_params.py"""

import logging
import os

import helpers
import requests
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.receives import ResponseItem, ResponseModel
from core.constant import const
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    CompanyInfoFactory,
    InvoiceFactory,
)
from enums import ReceiveRecordStatus
from exceptions import PeppolHttpException
from fastapi import status
from models import CompanyInfo
from requests import Response


def receive_zip_filepath1() -> str:
    """テスト用のZIPファイルのパスを取得
    中身:
        Length      Date    Time    Name
        ---------  ---------- -----   ----
        48218  05-17-2024 14:38   storage/for_test/receive1/standard_invoices_1.xml
        43465  05-17-2024 14:38   storage/for_test/receive1/standard_invoices_2.xml
        48224  05-17-2024 14:38   storage/for_test/receive1/standard_invoices_3.xml
        48230  05-17-2024 14:38   storage/for_test/receive1/standard_invoices_4.xml
    """
    return helpers.get_storage_path("for_test/receive1.zip")


def receive_zip_filepath2() -> str:
    """テスト用のZIPファイルのパスを取得
    中身:
        Length      Date    Time    Name
        ---------  ---------- -----   ----
        48218  05-17-2024 14:38   storage/for_test/receive2/standard_invoices_1.xml
        48224  05-17-2024 14:38   storage/for_test/receive2/standard_invoices_3.xml
        48230  05-17-2024 14:38   storage/for_test/receive2/standard_invoices_5.xml
        43465  05-17-2024 14:38   storage/for_test/receive2/standard_invoices_6.xml
    """
    return helpers.get_storage_path("for_test/receive2.zip")


def create_response(
    status_code: int, content: bytes | None = None
) -> requests.Response:
    """指定されたステータスコードとコンテンツを持つResponseオブジェクトを作成する"""
    response = requests.Response()
    response.status_code = status_code  # type: ignore
    if content:
        response._content = content  # バイナリデータをセット
    return response


def test_PP008() -> list[
    tuple[
        CompanyInfo,
        Response,
        dict,
        int,
    ]
]:
    """test_PP008パラメータ"""
    # zipファイルをバイナリ形式で読み込む
    with open(receive_zip_filepath1(), "rb") as file:
        zip_content1 = file.read()
    return [
        # case 1 : 処理成功(ZIPファイルを正常に取得)
        (
            # mock_get_company_info
            CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
            # mock_access_get_response
            create_response(status.HTTP_200_OK, zip_content1),
            # expected_response
            ResponseModel(
                header=Header(code="", message=""),
                payload=ResponseItem(success=const.PROC_RESULT_SUCCESS),
            ).model_dump(mode="json"),
            # expected_count
            4,
        ),
        # case 2 : 処理成功(ZIPファイルが空)
        (
            # mock_get_company_info
            CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
            # mock_access_get_response
            create_response(status.HTTP_204_NO_CONTENT),
            # expected_response
            ResponseModel(
                header=Header(code="", message=""),
                payload=ResponseItem(success=const.PROC_RESULT_SUCCESS),
            ).model_dump(mode="json"),
            # expected_count
            4,
        ),
    ]


def test_PP008_duplicated() -> list[
    tuple[
        CompanyInfo,
        Response,
        dict,
        int,
    ]
]:
    """test_PP008パラメータ"""
    # zipファイルをバイナリ形式で読み込む
    with open(receive_zip_filepath2(), "rb") as file:
        zip_content2 = file.read()

    return [
        # case 1 : 処理成功(ZIPファイルを正常に取得)
        (
            # mock_get_company_info
            CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
            # mock_access_get_response
            create_response(status.HTTP_200_OK, zip_content2),
            # expected_response
            ResponseModel(
                header=Header(code="", message=""),
                payload=ResponseItem(success=const.PROC_RESULT_SUCCESS),
            ).model_dump(mode="json"),
            # expected_count
            6,
        ),
    ]


def test_PP008_exception() -> list[
    tuple[
        list[CompanyInfo | PeppolHttpException],
        list[str],
        list,
        list[Response | PeppolHttpException],
        list[int],
        list[int],
        list[None],
        list[ReceiveRecordStatus],
        dict,
        int,
    ]
]:
    """test_PP008_exceptionパラメータ"""
    # zipファイルをバイナリ形式で読み込む
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../storage/for_test/receive.zip",
        ),
        "rb",
    ) as file:
        zip_content = file.read()

    response = requests.Response()
    response._content = zip_content

    return [
        # case 1 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
        (
            [
                PeppolHttpException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    log_level=logging.getLevelName(logging.INFO),
                    message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
                    extra={"request_params": {"company_infos_id": 1}},
                )
            ],
            [const.INIT_LAST_GET_DATE],
            [
                {
                    "esCompanyId": 1,
                    "peppolId": "0001:test0000000001",
                },
                {
                    "peppolId": "0001:test0000000001",
                    "apiId": "testApiId",
                    "password": "testPassword",
                    "authKey": "testAuthKey",
                },
            ],
            [response],
            [1],
            [const.PROC_RESULT_SUCCESS],
            [None, None],
            [ReceiveRecordStatus.TRANSFORM_NG],
            ErrorModel(
                header=Header(
                    code=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.code,
                    message=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
                ),
                payload=None,
            ).model_dump(mode="json"),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        # case 2 : E0002 S3アップロード失敗
        (
            [CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None)],
            [const.INIT_LAST_GET_DATE],
            [
                {
                    "esCompanyId": 1,
                    "peppolId": "0001:test0000000001",
                },
                {
                    "peppolId": "0001:test0000000001",
                    "apiId": "testApiId",
                    "password": "testPassword",
                    "authKey": "testAuthKey",
                },
            ],
            [response],
            [1],
            [const.PROC_RESULT_FAILED],
            [None, None],
            [ReceiveRecordStatus.TRANSFORM_NG],
            ErrorModel(
                header=Header(
                    code=messages.XML_UPLOAD_FAILED_MESSAGE.code,
                    message=messages.XML_UPLOAD_FAILED_MESSAGE.message,
                ),
                payload=None,
            ).model_dump(mode="json"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        # case 3 : E9001 ZIP受け取り失敗
        (
            [CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None)],
            [const.INIT_LAST_GET_DATE],
            [
                {
                    "esCompanyId": 1,
                    "peppolId": "0001:test0000000001",
                },
                {
                    "peppolId": "0001:test0000000001",
                    "apiId": "testApiId",
                    "password": "testPassword",
                    "authKey": "testAuthKey",
                },
            ],
            [
                PeppolHttpException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message_model=messages.ZIP_RECEIVE_FAILED_MESSAGE,
                )
            ],
            [1],
            [const.PROC_RESULT_SUCCESS],
            [None, None],
            [ReceiveRecordStatus.TRANSFORM_NG],
            ErrorModel(
                header=Header(
                    code=messages.ZIP_RECEIVE_FAILED_MESSAGE.code,
                    message=messages.ZIP_RECEIVE_FAILED_MESSAGE.message,
                ),
                payload=None,
            ).model_dump(mode="json"),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        # case 3 : E9999 変換処理失敗
        (
            [CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None)],
            [const.INIT_LAST_GET_DATE],
            [
                {
                    "esCompanyId": 1,
                    "peppolId": "0001:test0000000001",
                },
                {
                    "peppolId": "0001:test0000000001",
                    "apiId": "testApiId",
                    "password": "testPassword",
                    "authKey": "testAuthKey",
                },
            ],
            [response],
            [1],
            [const.PROC_RESULT_SUCCESS],
            [None, None],
            [ReceiveRecordStatus.INSERT_NG],
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
