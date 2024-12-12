"""tests/api/test_PP013_params.py"""
from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from api.v1.schemas.invoices.outputs import PutResponse, PutResponseItem
from core.constant import const
from core.message import messages
from enums import MstIsExistData, MstType, UserIsDisplay
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import status

test_PP013 = [
    # case 1 : 正常に出力項目が更新されることの確認
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        PutResponse(
            header=Header(code="", message=""),
            payload=PutResponseItem(success=const.PROC_RESULT_SUCCESS),
        ).model_dump(mode="json"),
    )
]

test_PP013_exception = [
    # case 1 : I0001 mstPpolItemsIdパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": "test",
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 2 : I0001 userSortOrderパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": "test",
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 3 : I0001 userIsDisplayパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": "test",
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 4 : I0001 userIsDisplayパラメーターが存在しない数字
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": 2,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 5 : I0001 mstParentSortOrderパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": "test",
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 6 : I0001 mstBtIdパラメーターが数値
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": 1,
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 7 : I0001 mstNameJpパラメーターが数値
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": 0,
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid string",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 8 : I0001 mstSortOrderパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": "test",
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be a valid integer, unable to parse string as an integer",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 9 : I0001 mstIsExistDataパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": "test",
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 10 : I0001 mstIsExistDataパラメーターが存在しない数字
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": 2,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 0 or 1",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 11 : I0001 mstTypeパラメーターが文字列
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": "test",
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 1, 2 or 3",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 12 : I0001 mstTypeパラメーターが存在しない数字
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": 0,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Input should be 1, 2 or 3",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 13 : I0001 mstPpolItemsIdパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 14 : I0001 userSortOrderパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 15 : I0001 userIsDisplayパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 16 : I0001 mstParentSortOrderパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 17 : I0001 mstBtIdパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 18 : I0001 mstNameJpパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 19 : I0001 mstSortOrderパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 20 : I0001 mstIsExistDataパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 21 : I0001 mstTypeパラメーターが存在しない
    (
        None,
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 22 : I0001 dataの中身の全てのパラメーターが存在しない
    (
        None,
        {"data": [{}]},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 23 : I0001 dataパラメーターが存在しない
    (
        None,
        {},
        ErrorModel(
            header=Header(
                code=messages.INVALID_PARAMETER.code,
                message="data is Field required",
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    # case 24 : E0006 user_ppol_items更新エラー
    (
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.FAILED_UPDATE_USER_PPOL_ITEMS_MESSAGE,
            extra={
                "response_data": {
                    "error": "error",
                    "insert_user_ppol_items": [
                        {
                            "userId": 1,
                            "mstPpolItemsId": 1,
                            "sortOrder": 1,
                            "isDisplay": UserIsDisplay.DISPLAY,
                        }
                    ],
                }
            },
        ),
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
        },
        ErrorModel(
            header=Header(
                code=messages.FAILED_UPDATE_USER_PPOL_ITEMS_MESSAGE.code,
                message=messages.FAILED_UPDATE_USER_PPOL_ITEMS_MESSAGE.message,
            ),
            payload=None,
        ).model_dump(mode="json"),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ),
    # case 25 : E9999 サーバーエラー
    (
        PeppolHttpException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_model=messages.INTERNAL_SERVER_ERROR,
        ),
        {
            "data": [
                {
                    "mstPpolItemsId": 1,
                    "userSortOrder": 1,
                    "userIsDisplay": UserIsDisplay.DISPLAY,
                    "mstParentSortOrder": 0,
                    "mstBtId": "IBT-010",
                    "mstNameJp": "買い手参照",
                    "mstSortOrder": 1,
                    "mstIsExistData": MstIsExistData.EXIST,
                    "mstType": MstType.INVOICES,
                }
            ]
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
