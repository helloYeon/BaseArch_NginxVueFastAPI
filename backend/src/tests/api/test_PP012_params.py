"""tests/api/test_PP012_params.py"""
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.outputs import BaseItem, ItemResponse
from core.message import messages
from enums import MstIsExistData, MstType, UserIsDisplay
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status

test_PP012 = [
    # case 1 : 出力項目の取得を確認
    (
        [
            BaseItem(
                mstPpolItemsId=1,
                userSortOrder=1,
                userIsDisplay=UserIsDisplay.DISPLAY,
                mstParentSortOrder=0,
                mstBtId="IBT-010",
                mstNameJp="買い手参照",
                mstSortOrder=1,
                mstIsExistData=MstIsExistData.EXIST,
                mstType=MstType.INVOICES,
            )
        ],
        ItemResponse(
            header=Header(code="", message=""),
            payload=[
                BaseItem(
                    mstPpolItemsId=1,
                    userSortOrder=1,
                    userIsDisplay=UserIsDisplay.DISPLAY,
                    mstParentSortOrder=0,
                    mstBtId="IBT-010",
                    mstNameJp="買い手参照",
                    mstSortOrder=1,
                    mstIsExistData=MstIsExistData.EXIST,
                    mstType=MstType.INVOICES,
                )
            ],
        ).model_dump(mode="json"),
    )
]

test_PP012_exception = [
    # case 1 : E0005 mst_ppol_items取得エラー
    (
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_GET_MST_PPOL_ITEMS_MESSAGE,
        ),
        ErrorModel(
            header=Header(
                code=messages.FAILED_GET_MST_PPOL_ITEMS_MESSAGE.code,
                message=messages.FAILED_GET_MST_PPOL_ITEMS_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    # case 2 : E9999 サーバーエラー
    (
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
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
