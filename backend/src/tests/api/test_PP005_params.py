"""tests/api/test_PP005_params.py"""

import logging

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.downloads.csv import CsvQueryParam, PpolItem
from core.constant import const
from core.message import messages
from enums import (
    Sort,
    SortOrder,
)
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo

test_PP005 = [
    # case 1 : company_infos_id:1のユーザーの検索結果でCSVをダウンロード
    (
        CsvQueryParam(sort=Sort.INVOICE_ID, sort_order=SortOrder.ASC),
        CompanyInfo(id=1, esCompanyId=1, name="test", parentEsCompanyId=None),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        [1],
        [
            [const.PAYMENT_CODE_NAME],
            ["CustomizationID"],
            ["ID"],
        ],
        ["unittestPaymentCode"],
        ["unittestIBT024"],
        [["unittestIBT126"]],
        "支払先コード,CustomizationID,ID\nunittestPaymentCode,unittestIBT024,unittestIBT126\n",
    )
]

test_PP005_exception = [
    (
        # case 1 : I0001: sortパラメーターが存在しない数字
        {
            "sort": 0,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="sort is Input should be 1, 2, 3, 4, 5, 6, 7 or 8",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 2 : I0001: sort_orderパラメーターが存在しない数字
        {
            "sort_order": 2,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="sort_order is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 3 : I0001: free_wordパラメーターが256文字
        {
            "free_word": "テストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテ",  # noqa: E501
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="free_word is String should have at most 255 characters",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 4 : I0001: inv_noパラメーターが256文字
        {
            "inv_no": "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest",  # noqa: E501
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="inv_no is String should have at most 255 characters",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 5: I0001: data_typeパラメーターが存在しない数字
        {"data_type": 0},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data_type is Input should be 1, 2 or 3",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 6: I0001: company_nameが256文字
        {
            "company_name": "テストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテストテ",  # noqa: E501
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="company_name is String should have at most 255 characters",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 7 : I0001: from_issue_dateパラメーターがYYYY-MM-DDの形ではない
        {
            "from_issue_date": 1,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_issue_date is String does not match format YYYY-MM-DD",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 8 : I0001: from_issue_dateパラメーターが存在しない月
        {
            "from_issue_date": "2024-13-31",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_issue_date is month must be in 1..12",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 9 : I0001: from_issue_dateパラメーターが存在しない日付
        {
            "from_issue_date": "2024-12-32",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_issue_date is day is out of range for month",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 10 : I0001: to_issue_dateパラメーターがYYYY-MM-DDの形ではない
        {
            "to_issue_date": 1,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_issue_date is String does not match format YYYY-MM-DD",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 11 : I0001: to_issue_dateパラメーターが存在しない月
        {
            "to_issue_date": "2024-13-31",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_issue_date is month must be in 1..12",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 12 : I0001: to_issue_dateパラメーターが存在しない日付
        {
            "to_issue_date": "2024-12-32",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_issue_date is day is out of range for month",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 13 : I0001: from_issue_dateパラメーターがto_issue_dateパラメーターより過去の日付
        {
            "from_issue_date": "2024-12-31",
            "to_issue_date": "2024-12-30",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_issue_date is Must be a date after from_issue_date",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 14 : I0001: pay_due_dateパラメーターがYYYY-MM-DDの形ではない
        {
            "pay_due_date": 1,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="pay_due_date is String does not match format YYYY-MM-DD",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 15 : I0001: pay_due_dateパラメーターが存在しない月
        {
            "pay_due_date": "2024-13-32",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="pay_due_date is month must be in 1..12",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 16 : I0001: pay_due_dateパラメーターが存在しない日付
        {
            "pay_due_date": "2024-12-32",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="pay_due_date is day is out of range for month",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 17 : I0001: from_inv_amountパラメーターが数字ではない
        {"from_inv_amount": "a"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_inv_amount is Input should be a valid number, unable to parse string as a number",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 18 : I0001: to_inv_amountパラメーターが数字ではない
        {"to_inv_amount": "a"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_inv_amount is Input should be a valid number, unable to parse string as a number",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 19 : I0001: from_inv_amountパラメーターがto_inv_amountパラメーターより低い値
        {"from_inv_amount": 100, "to_inv_amount": 10},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_inv_amount is Must be higher than from_inv_amount.",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 20 : I0001: payment_methodパラメーターが存在しない数字
        {"payment_method": 7},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="payment_method is Input should be 0, 1, 2, 3, 4, 5, 6 or 9",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 21 : I0001: is_openパラメーターが存在しない数字
        {"is_open": 2},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="is_open is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 22 : I0001: is_downloadパラメーターが存在しない数字
        {
            "is_download": 2,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="is_download is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 23 : I0001: is_confirmationパラメーターが存在しない数字
        {
            "is_confirmation": 2,
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="is_confirmation is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 24 : I0001: company_infos_idパラメーターが数字ではない
        {"company_infos_id": "a"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="company_infos_id is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 25 : I0001: from_receive_date_timeパラメーターがYYYY-MM-DD HH:mmの形ではない
        {"from_receive_date_time": 1},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_receive_date_time is String does not match format YYYY-MM-DD HH:mm",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 26 : I0001: from_receive_date_timeパラメーターが存在しない月
        {"from_receive_date_time": "2024-13-31 00:00"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_receive_date_time is month must be in 1..12",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 27 : I0001: from_receive_date_timeパラメーターが存在しない日付
        {"from_receive_date_time": "2024-12-32 00:00"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_receive_date_time is day is out of range for month",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 28 : I0001: from_receive_date_timeパラメーターが存在しない時刻(時)
        {"from_receive_date_time": "2024-12-31 24:00"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_receive_date_time is hour must be in 0..23",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 29 : I0001: from_receive_date_timeパラメーターが存在しない時刻（分）
        {"from_receive_date_time": "2024-12-31 00:60"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="from_receive_date_time is minute must be in 0..59",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 30 : I0001: to_receive_date_timeパラメーターがYYYY-MM-DD HH:mmの形ではない
        {"to_receive_date_time": 1},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_receive_date_time is String does not match format YYYY-MM-DD HH:mm",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 31 : I0001: to_receive_date_timeパラメーターが存在しない日付
        {"to_receive_date_time": "2024-12-32 00:00"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_receive_date_time is day is out of range for month",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 32 : I0001: to_receive_date_timeパラメーターが存在しない時刻(時)
        {"to_receive_date_time": "2024-12-31 24:00"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_receive_date_time is hour must be in 0..23",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 33 : I0001: to_receive_date_timeパラメーターが存在しない時刻（分）
        {"to_receive_date_time": "2024-12-31 00:60"},
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_receive_date_time is minute must be in 0..59",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 34 : I0001: from_receive_date_timeパラメーターがto_receive_date_timeパラメーターより過去の日付
        {
            "from_receive_date_time": "2024-12-31 00:00",
            "to_receive_date_time": "2024-12-30 00:00",
        },
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="to_receive_date_time is Must be a datetime after from_receive_date_time",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 35 : I0002: 該当請求書レコードが存在しない
        {},
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        [1],
        [
            [const.PAYMENT_CODE_NAME],
            ["CustomizationID"],
            ["ID"],
        ],
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
        None,
        None,
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
        # case 36 : I0003: 該当請求書明細レコードが存在しない
        {},
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        [1],
        [
            [const.PAYMENT_CODE_NAME],
            ["CustomizationID"],
            ["ID"],
        ],
        ["unittestPaymentCode"],
        ["unittestIBT024"],
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
        # case 37 : I0004: 指定したcompany_infos_idが所属企業、結合企業に該当しない
        {},
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        None,
        None,
        None,
        None,
        None,
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
        # case 38 : I0005: 支払先コードが存在しない
        {},
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        [1],
        [
            [const.PAYMENT_CODE_NAME],
            ["CustomizationID"],
            ["ID"],
        ],
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.PAYMENT_CODE_NOT_FOUND,
            extra={
                "request_params": {
                    "common_item_name": const.PAYMENT_CODE_NAME,
                    "invoice_record_peppol_id": "1111:test",
                    "company_info_id": 1,
                }
            },
        ),
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.PAYMENT_CODE_NOT_FOUND.code,
                message=messages.PAYMENT_CODE_NOT_FOUND.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 39 : I0006: 指定した請求書受信履歴レコードが存在しない
        {},
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        [1],
        [
            [const.PAYMENT_CODE_NAME],
            ["CustomizationID"],
            ["ID"],
        ],
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_RECEIVE_RECORD_NOT_FOUND_MESSAGE,
            extra={
                "request_params": {
                    "invoice_id": 1,
                    "company_ids": [1],
                }
            },
        ),
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVOICE_RECEIVE_RECORD_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_RECEIVE_RECORD_NOT_FOUND_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 40 : I0007: CSVダウンロード対象の検索結果が0件だった場合
        {},
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
        ),
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_SEARCH_RESULT_NOT_FOUND,
            extra={
                "request_params": {
                    "company_info_id": 1,
                }
            },
        ),
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVOICE_SEARCH_RESULT_NOT_FOUND.code,
                message=messages.INVOICE_SEARCH_RESULT_NOT_FOUND.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 41 : E9999 サーバーエラー
        {},
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        None,
        None,
        None,
        None,
        None,
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
