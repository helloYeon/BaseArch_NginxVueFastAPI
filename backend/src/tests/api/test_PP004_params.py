"""tests/api/test_PP004_params.py"""

import logging
from typing import Any

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.details import BaseItem
from core.message import messages
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo, InvoiceDetail


def test_PP004() -> (
    list[tuple[int, CompanyInfo, None, list[int], BaseItem, dict[str, Any]]]
):
    """PP004APIテストパラメータ"""
    mock_invoice_detail = InvoiceDetail(
        id=1,
        IBT126="unittestIBT126",
        IBT127="unittestIBT127",
        AUTO87={
            "IBT-128": {"value": "AB-123", "schemeID": "147"},
            "AUTO-88": "130",
        },
        IBT129={"value": "55", "unitCode": "H87"},
        IBT131={"value": "250000", "currencyID": "JPY"},
        AUTO82={"IBT-132": "1", "AUTO-83": {"IBT-183": "1"}},
        IBT133="unittestIBT133",
        IBG26={"IBT-134": "2023-09-15", "IBT-135": "2023-09-15"},
        AUTO84={"AUTO-85": "010", "AUTO-86": {"IBT-184": "789"}},
        IBG36={"IBT-188": "D001-1", "IBT-189": "12345"},
        IBG27=[
            {
                "AUTO-89": False,
                "IBT-140": "95",
                "IBT-139": "値引",
                "IBT-138": "10",
                "IBT-136": {"value": "1500", "currencyID": "JPY"},
                "IBT-137": {"value": "1500", "currencyID": "JPY"},
            }
        ],
        IBG28=[
            {
                "AUTO-92": True,
                "IBT-145": "CG",
                "IBT-144": "クリーニング",
                "IBT-143": "10",
                "IBT-141": {"value": "1500", "currencyID": "JPY"},
                "IBT-142": {"value": "1500", "currencyID": "JPY"},
            }
        ],
        IBG31={
            "IBT-154": "",
            "IBT-153": "デスクチェア",
            "AUTO-95": {"IBT-156": "b-13214"},
            "AUTO-96": {"IBT-155": "97iugug876"},
            "AUTO-97": {"IBT-157": {"value": "4503994155481", "schemeID": "147"}},
            "AUTO-98": {"IBT-159": "JP"},
            "AUTO-99": [
                {
                    "IBT-158": {
                        "value": "86776",
                        "listID": "TST",
                        "listVersionID": "19.05.01",
                    }
                }
            ],
            "IBG-30": [
                {
                    "IBT-151": "S",
                    "IBT-152": "10",
                    "IBT-166": {"value": "0", "currencyID": "JPY"},
                    "AUTO-101": {"IBT-167": "VAT"},
                }
            ],
            "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "脚"}],
        },
        IBG29={
            "IBT-146": {"value": "50000", "currencyID": "JPY"},
            "IBT-149": {"value": "1", "unitCode": "H87"},
            "AUTO-103": {
                "AUTO-104": False,
                "IBT-147": {"value": "100", "currencyID": "JPY"},
                "IBT-148": {"value": "600", "currencyID": "JPY"},
            },
        },
    )

    return [
        # case 1 : invoice_detail_id:1の請求書明細を取得
        (
            1,
            CompanyInfo(
                id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
            ),
            None,
            [1],
            BaseItem(
                IBT126=mock_invoice_detail.IBT126,
                IBT127=mock_invoice_detail.IBT127,
                AUTO87=mock_invoice_detail.AUTO87,
                IBT129=mock_invoice_detail.IBT129,
                IBT131=mock_invoice_detail.IBT131,
                AUTO82=mock_invoice_detail.AUTO82,
                IBT133=mock_invoice_detail.IBT133,
                IBG26=mock_invoice_detail.IBG26,
                AUTO84=mock_invoice_detail.AUTO84,
                IBG36=mock_invoice_detail.IBG36,
                IBG27=mock_invoice_detail.IBG27,
                IBG28=mock_invoice_detail.IBG28,
                IBG31=mock_invoice_detail.IBG31,
                IBG29=mock_invoice_detail.IBG29,
            ),
            {
                "header": {"code": "", "message": ""},
                "payload": {
                    "IBT-126": "unittestIBT126",
                    "IBT-127": "unittestIBT127",
                    "AUTO-87": {
                        "IBT-128": {"value": "AB-123", "schemeID": "147"},
                        "AUTO-88": "130",
                    },
                    "IBT-129": {"value": "55", "unitCode": "H87"},
                    "IBT-131": {"value": "250000", "currencyID": "JPY"},
                    "AUTO-82": {"IBT-132": "1", "AUTO-83": {"IBT-183": "1"}},
                    "IBT-133": "unittestIBT133",
                    "IBG-26": {"IBT-134": "2023-09-15", "IBT-135": "2023-09-15"},
                    "AUTO-84": {"AUTO-85": "010", "AUTO-86": {"IBT-184": "789"}},
                    "IBG-36": {"IBT-188": "D001-1", "IBT-189": "12345"},
                    "IBG-27": [
                        {
                            "AUTO-89": False,
                            "IBT-140": "95",
                            "IBT-139": "値引",
                            "IBT-138": "10",
                            "IBT-136": {"value": "1500", "currencyID": "JPY"},
                            "IBT-137": {"value": "1500", "currencyID": "JPY"},
                        }
                    ],
                    "IBG-28": [
                        {
                            "AUTO-92": True,
                            "IBT-145": "CG",
                            "IBT-144": "クリーニング",
                            "IBT-143": "10",
                            "IBT-141": {"value": "1500", "currencyID": "JPY"},
                            "IBT-142": {"value": "1500", "currencyID": "JPY"},
                        }
                    ],
                    "IBG-31": {
                        "IBT-154": "",
                        "IBT-153": "デスクチェア",
                        "AUTO-95": {"IBT-156": "b-13214"},
                        "AUTO-96": {"IBT-155": "97iugug876"},
                        "AUTO-97": {
                            "IBT-157": {"value": "4503994155481", "schemeID": "147"}
                        },
                        "AUTO-98": {"IBT-159": "JP"},
                        "AUTO-99": [
                            {
                                "IBT-158": {
                                    "value": "86776",
                                    "listID": "TST",
                                    "listVersionID": "19.05.01",
                                }
                            }
                        ],
                        "IBG-30": [
                            {
                                "IBT-151": "S",
                                "IBT-152": "10",
                                "IBT-166": {"value": "0", "currencyID": "JPY"},
                                "AUTO-101": {"IBT-167": "VAT"},
                            }
                        ],
                        "IBG-32": [{"IBT-160": "表示単位名称", "IBT-161": "脚"}],
                    },
                    "IBG-29": {
                        "IBT-146": {"value": "50000", "currencyID": "JPY"},
                        "IBT-149": {"value": "1", "unitCode": "H87"},
                        "AUTO-103": {
                            "AUTO-104": False,
                            "IBT-147": {"value": "100", "currencyID": "JPY"},
                            "IBT-148": {"value": "600", "currencyID": "JPY"},
                        },
                    },
                },
            },
        )
    ]


test_PP004_exception = [
    (
        # case 1 : I0001: invoice_detail_idパラメーターが数値ではない
        "a",
        None,
        None,
        None,
        None,
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="invoice_detail_id is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        # case 2 : I0003: 該当請求書明細レコードが存在しない
        1,
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [1],
        None,
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE,
            extra={"request_params": {"company_infos_id": 1}},
        ),
        ErrorModel(
            header=Header(
                code=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.code,
                message=messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.message,
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
        # case 4 : E9999: サーバーエラー
        1,
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
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
