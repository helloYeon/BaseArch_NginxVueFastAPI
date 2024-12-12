"""tests/services/test_output_service_params.py"""

from typing import Any

from api.v1.schemas.invoices.outputs import BaseItem, PutRequest
from core.message import messages
from database import TestSessionLocal
from db.factories import UserPeppolItemFactory
from enums import (
    MstIsExistData,
    MstType,
    UserIsDisplay,
)
from exceptions import PeppolHttpException


def test_get_user_setting() -> list[tuple[int, list[BaseItem]]]:
    """get_user_settingテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item1 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=1,
        sortOrder=2,
        isDisplay=UserIsDisplay.DISPLAY,
    )
    user_ppol_item2 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=2,
        sortOrder=3,
        isDisplay=UserIsDisplay.DISPLAY,
    )
    user_ppol_item3 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=3,
        sortOrder=1,
        isDisplay=UserIsDisplay.DISPLAY,
    )
    session.add(user_ppol_item1)
    session.add(user_ppol_item2)
    session.add(user_ppol_item3)
    session.commit()

    return [
        (
            # case 1: user1の設定を取得
            1,
            [
                BaseItem(
                    mstPpolItemsId=1,
                    userSortOrder=2,
                    userIsDisplay=UserIsDisplay.DISPLAY,
                    mstParentSortOrder=0,
                    mstBtId="IBT-024",
                    mstNameJp="ビジネスプロセスタイプ",
                    mstSortOrder=1,
                    mstIsExistData=MstIsExistData.EXIST,
                    mstType=MstType.INVOICES,
                ),
                BaseItem(
                    mstPpolItemsId=2,
                    userSortOrder=3,
                    userIsDisplay=UserIsDisplay.DISPLAY,
                    mstParentSortOrder=0,
                    mstBtId="IBT-023",
                    mstNameJp="仕様ID",
                    mstSortOrder=2,
                    mstIsExistData=MstIsExistData.EXIST,
                    mstType=MstType.INVOICES,
                ),
                BaseItem(
                    mstPpolItemsId=3,
                    userSortOrder=1,
                    userIsDisplay=UserIsDisplay.DISPLAY,
                    mstParentSortOrder=0,
                    mstBtId="IBT-001",
                    mstNameJp="請求書番号",
                    mstSortOrder=3,
                    mstIsExistData=MstIsExistData.EXIST,
                    mstType=MstType.INVOICES,
                ),
            ],
        ),
    ]


def test_get_user_setting_exception() -> list[tuple[int, dict[str, Any]]]:
    """get_user_setting例外テストパラメータ"""
    return [
        (
            # mst_ppol_itemsが空の時
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.FAILED_GET_MST_PPOL_ITEMS_MESSAGE.message,
            },
        )
    ]


def test_put_user_setting() -> list[tuple[PutRequest, int, None]]:
    """put_user_settingテストパラメータ"""
    return [
        (
            PutRequest(
                data=[
                    BaseItem(
                        mstPpolItemsId=1,
                        userSortOrder=2,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-024",
                        mstNameJp="ビジネスプロセスタイプ",
                        mstSortOrder=1,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                    BaseItem(
                        mstPpolItemsId=2,
                        userSortOrder=3,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-023",
                        mstNameJp="仕様ID",
                        mstSortOrder=2,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                    BaseItem(
                        mstPpolItemsId=3,
                        userSortOrder=1,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-001",
                        mstNameJp="請求書番号",
                        mstSortOrder=3,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                ],
            ),
            1,
            None,
        )
    ]


def test_put_user_setting_exception() -> list[tuple[PutRequest, int, dict[str, Any]]]:
    """put_user_setting例外テストパラメータ"""
    return [
        (
            # case 1: dbエラー
            PutRequest(
                data=[
                    BaseItem(
                        mstPpolItemsId=1,
                        userSortOrder=2,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-024",
                        mstNameJp="ビジネスプロセスタイプ",
                        mstSortOrder=1,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                    BaseItem(
                        mstPpolItemsId=2,
                        userSortOrder=3,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-023",
                        mstNameJp="仕様ID",
                        mstSortOrder=2,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                    BaseItem(
                        mstPpolItemsId=3,
                        userSortOrder=1,
                        userIsDisplay=UserIsDisplay.DISPLAY,
                        mstParentSortOrder=0,
                        mstBtId="IBT-001",
                        mstNameJp="請求書番号",
                        mstSortOrder=3,
                        mstIsExistData=MstIsExistData.EXIST,
                        mstType=MstType.INVOICES,
                    ),
                ]
            ),
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.FAILED_UPDATE_USER_PPOL_ITEMS_MESSAGE.message,
            },
        )
    ]


def test_check_user_setting_payment_code() -> list[tuple[int, bool]]:
    """check_user_setting_payment_codeテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=301,
        sortOrder=1,
        isDisplay=UserIsDisplay.DISPLAY,
    )
    session.add(user_ppol_item)
    session.commit()

    return [
        # case 1: user1の設定を取得
        (1, True)
    ]


def test_check_user_setting_payment_code_exception() -> (
    list[tuple[int, dict[str, Any]]]
):
    """check_user_setting_payment_code例外テストパラメータ"""
    return [
        (
            # case 1: mst_ppol_itemsが空の時
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.FAILED_GET_MST_PPOL_ITEMS_MESSAGE.message,
            },
        )
    ]
