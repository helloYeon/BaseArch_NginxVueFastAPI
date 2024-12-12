"""tests/api/test_PP021_params.py"""

import logging

import api.v1.schemas.users.me as me_schema
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from core.constant import const
from core.message import messages
from enums.csv_download_type import CsvDownloadType
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status

test_PP021 = [
    # case 1 : csvDownloadTypeを正常更新
    (
        {"csvDownloadType": CsvDownloadType.ALL_ITEMS},
        None,
        me_schema.PatchResponse(
            payload=me_schema.PatchResponseItem(success=const.PROC_RESULT_SUCCESS)
        ).model_dump(mode="json"),
    ),
]

test_PP021_exception = [
    # case 1 : I0001: リクエストがない
    (
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="request body is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001: リクエストが空json
    (
        {},
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="request body is Value error, More than 1 item is required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0001: csvDownloadTypeが規定値ではない
    (
        {"csvDownloadType": 3},
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="csvDownloadType is Input should be 1 or 2",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 4 : E0001: ユーザーが存在しない
    (
        {"csvDownloadType": CsvDownloadType.ALL_ITEMS},
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.NOT_EXIST_USER,
            extra={
                "request_params": {
                    "user_id": 1,
                }
            },
        ),
        ErrorModel(
            header=Header(
                code=messages.NOT_EXIST_USER.code,
                message=messages.NOT_EXIST_USER.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
]
