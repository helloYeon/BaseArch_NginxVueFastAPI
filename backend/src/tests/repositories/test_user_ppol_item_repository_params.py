"""tests/repositories/test_user_ppol_item_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import MstPpolItemFactory, UserPeppolItemFactory
from enums import MstIsExistData, MstType, UserIsDisplay
from models import MstPpolItem, UserPpolItem


def test_find() -> list[tuple[int, UserPpolItem | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item_record = UserPeppolItemFactory()
    user_ppol_item_deleted_record = UserPeppolItemFactory(deletedAt=pendulum.now())
    session.add_all([user_ppol_item_record, user_ppol_item_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, user_ppol_item_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_all_by_user_id() -> (
    list[tuple[int, list[tuple[MstPpolItem, UserPpolItem]]]]
):
    """get_all_by_user_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record = MstPpolItemFactory(btId="IBT-001")
    mst_ppol_item_record2 = MstPpolItemFactory(btId="IBT-002")
    session.flush()

    user_ppol_item_record = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=mst_ppol_item_record.id
    )
    user_ppol_item_record2 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=mst_ppol_item_record2.id
    )
    user_ppol_item_deleted_record = UserPeppolItemFactory(
        userId=2, mstPpolItemsId=mst_ppol_item_record.id, deletedAt=pendulum.now()
    )
    session.add_all(
        [user_ppol_item_record, user_ppol_item_record2, user_ppol_item_deleted_record]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (
            1,
            [
                (mst_ppol_item_record, user_ppol_item_record),
                (mst_ppol_item_record2, user_ppol_item_record2),
            ],
        ),
        # # case 2 : IDに合致している情報が存在しない
        (999, []),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, []),
    ]


def test_delete_by_user_id() -> list[tuple[int, None]]:
    """delete_by_user_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item_record = UserPeppolItemFactory()
    user_ppol_item_deleted_record = UserPeppolItemFactory(deletedAt=pendulum.now())
    session.add_all([user_ppol_item_record, user_ppol_item_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, None),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_insert_by_user_ppol_items() -> list[tuple[list[UserPpolItem], None]]:
    """insert_by_user_ppol_itemsテスト"""
    user_ppol_item_record = UserPeppolItemFactory()
    user_ppol_item_record2 = UserPeppolItemFactory()

    return [
        # case 1 : 一括登録
        ([user_ppol_item_record, user_ppol_item_record2], None),
    ]


def test_get_all_by_type() -> list[tuple[int, MstType, list[MstPpolItem]]]:
    """get_all_by_typeテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record = MstPpolItemFactory(
        btId="IBT-001",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
    )
    mst_ppol_item_record2 = MstPpolItemFactory(
        btId="IBT-002",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.NONE,
    )
    mst_ppol_item_record3 = MstPpolItemFactory(
        btId="IBT-003",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
    )
    mst_ppol_item_record4 = MstPpolItemFactory(
        btId="IBT-004",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
    )
    mst_ppol_item_record5 = MstPpolItemFactory(
        btId="IBT-005",
        type=MstType.PARTICULARS,
        isExistData=MstIsExistData.EXIST,
    )
    mst_ppol_item_record6 = MstPpolItemFactory(
        btId="IBT-006",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
    )
    session.flush()

    user_ppol_item_record = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=1,
    )
    user_ppol_item_record2 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record2.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=2,
    )
    user_ppol_item_record3 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record3.id,
        isDisplay=UserIsDisplay.HIDDEN,
        sortOrder=3,
    )
    user_ppol_item_record4 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record4.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=4,
    )
    user_ppol_item_record5 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record5.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=5,
    )
    user_ppol_item_record6 = UserPeppolItemFactory(
        userId=1,
        mstPpolItemsId=mst_ppol_item_record6.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=6,
    )
    user_ppol_item_record7 = UserPeppolItemFactory(
        userId=2,
        mstPpolItemsId=mst_ppol_item_record.id,
        isDisplay=UserIsDisplay.DISPLAY,
        sortOrder=7,
    )
    session.add_all(
        [
            user_ppol_item_record,
            user_ppol_item_record2,
            user_ppol_item_record3,
            user_ppol_item_record4,
            user_ppol_item_record5,
            user_ppol_item_record6,
            user_ppol_item_record7,
        ]
    )
    session.commit()

    return [
        # case 1 : IDとtypeに合致している情報が存在
        (
            1,
            MstType.INVOICES,
            [mst_ppol_item_record, mst_ppol_item_record4, mst_ppol_item_record6],
        ),
        # case 2 : IDとtypeに合致している情報が存在
        (1, MstType.PARTICULARS, [mst_ppol_item_record5]),
        # case 3 : IDとtypeに合致している情報が存在
        (2, MstType.INVOICES, [mst_ppol_item_record]),
        # case 4 : typeに合致している情報が存在しない
        (1, MstType.COMMON, []),
        # case 5 : IDに合致している情報が存在しない
        (999, MstType.INVOICES, []),
    ]


def test_get_count() -> list[tuple[int, int]]:
    """get_countテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item_record = UserPeppolItemFactory(userId=1)
    user_ppol_item_record2 = UserPeppolItemFactory(userId=1)
    user_ppol_item_record3 = UserPeppolItemFactory(userId=2)
    user_ppol_item_deleted_record = UserPeppolItemFactory(
        userId=1, deletedAt=pendulum.now()
    )
    session.add_all(
        [
            user_ppol_item_record,
            user_ppol_item_record2,
            user_ppol_item_record3,
            user_ppol_item_deleted_record,
        ]
    )
    session.commit()

    return [
        # case 1 : userIdに合致している情報が存在
        (1, 2),
        # case 2 : userIdに合致している情報が存在
        (2, 1),
        # case 3 : userIdに合致している情報が存在しない
        (999, 0),
    ]
