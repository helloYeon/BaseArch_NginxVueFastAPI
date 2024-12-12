"""tests/api/test_PP016_params.py"""

import logging

from api.v1.schemas.base_schema import Header
from api.v1.schemas.company.integrations import BaseItem, ItemResponse
from api.v1.schemas.error_schema import ErrorModel
from core.message import messages
from enums import IsParent
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status
from models import CompanyInfo

test_PP016 = [
    # case 1 : 結合企業と所属企業情報一覧の取得確認
    (
        CompanyInfo(
            id=1, esCompanyId=1, name="unittestCompanyName1", parentEsCompanyId=1
        ),
        [BaseItem(companyInfosId=1, name="unittestName", isParent=IsParent.PARENT)],
        ItemResponse(
            header=Header(code="", message=""),
            payload=[
                BaseItem(
                    companyInfosId=1, name="unittestName", isParent=IsParent.PARENT
                )
            ],
        ).model_dump(mode="json"),
    )
]

test_PP016_exception = [
    (
        # case 1 : I0004 指定したcompany_infos_idが所属企業、結合企業に該当しない
        PeppolHttpException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            log_level=logging.getLevelName(logging.INFO),
            message_model=messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR,
            extra={"request_params": {"company_infos_id": 1}},
        ),
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
        # case 1 : E9999 サーバーエラー
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
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
