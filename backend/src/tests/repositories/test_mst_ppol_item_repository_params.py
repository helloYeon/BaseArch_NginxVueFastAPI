"""tests/repositories/test_mst_item_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import MstPpolItemFactory
from enums import MstIsExistData, MstType
from models import MstPpolItem


def test_find() -> list[tuple[int, MstPpolItem | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record = MstPpolItemFactory(btId="IBT-001")
    mst_ppol_item_deleted_record = MstPpolItemFactory(
        btId="ITB-999", deletedAt=pendulum.now()
    )
    session.add_all([mst_ppol_item_record, mst_ppol_item_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, mst_ppol_item_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_all() -> list[list[MstPpolItem]]:
    """get_allテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record1 = MstPpolItemFactory(btId="IBT-001")
    mst_ppol_item_record2 = MstPpolItemFactory(btId="IBT-002")
    mst_ppol_item_deleted_records = MstPpolItemFactory(
        btId="ITB-999", deletedAt=pendulum.now()
    )
    session.add_all(
        [mst_ppol_item_record1, mst_ppol_item_record2, mst_ppol_item_deleted_records]
    )
    session.commit()

    return [
        # case 1 : 全ての情報が取得できる
        ([mst_ppol_item_record1, mst_ppol_item_record2]),
    ]


def test_get_all_by_type() -> list[tuple[MstType, list[MstPpolItem]]]:
    """get_all_by_typeテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record_invoice1 = MstPpolItemFactory(
        btId="IBT-001", type=MstType.INVOICES, sortOrder=1
    )
    mst_ppol_item_record_invoice2 = MstPpolItemFactory(
        btId="IBT-002", type=MstType.INVOICES, sortOrder=2
    )
    mst_ppol_item_record_particulars1 = MstPpolItemFactory(
        btId="ITB-101", type=MstType.PARTICULARS, sortOrder=3
    )
    session.add_all(
        [
            mst_ppol_item_record_invoice1,
            mst_ppol_item_record_invoice2,
            mst_ppol_item_record_particulars1,
        ]
    )
    session.commit()

    return [
        # case 1 : 指定したMSTTypeの情報が取得できる(INVOICES)
        (
            MstType.INVOICES,
            [mst_ppol_item_record_invoice1, mst_ppol_item_record_invoice2],
        ),
        # case 2 : 指定したMSTTypeの情報が取得できる(PARTICULARS)
        (MstType.PARTICULARS, [mst_ppol_item_record_particulars1]),
    ]


def test_get_all_by_type_exist() -> list[tuple[MstType, list[MstPpolItem]]]:
    """get_all_by_type_existテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record_invoice1 = MstPpolItemFactory(
        btId="IBT-001",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
        sortOrder=1,
    )
    mst_ppol_item_record_invoice2 = MstPpolItemFactory(
        btId="IBT-002",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.NONE,
        sortOrder=2,
    )
    mst_ppol_item_record_invoice3 = MstPpolItemFactory(
        btId="IBT-003",
        type=MstType.INVOICES,
        isExistData=MstIsExistData.EXIST,
        sortOrder=3,
    )
    mst_ppol_item_record_particulars1 = MstPpolItemFactory(
        btId="ITB-101",
        type=MstType.PARTICULARS,
        isExistData=MstIsExistData.NONE,
        sortOrder=4,
    )
    mst_ppol_item_record_particulars2 = MstPpolItemFactory(
        btId="ITB-102",
        type=MstType.PARTICULARS,
        isExistData=MstIsExistData.EXIST,
        sortOrder=5,
    )
    session.add_all(
        [
            mst_ppol_item_record_invoice1,
            mst_ppol_item_record_invoice2,
            mst_ppol_item_record_invoice3,
            mst_ppol_item_record_particulars1,
            mst_ppol_item_record_particulars2,
        ]
    )
    session.commit()

    return [
        # case 1 : 指定したMSTTypeの情報が取得できる(INVOICES)
        (
            MstType.INVOICES,
            [mst_ppol_item_record_invoice1, mst_ppol_item_record_invoice3],
        ),
        # case 2 : 指定したMSTTypeの情報が取得できる(PARTICULARS)
        (
            MstType.PARTICULARS,
            [mst_ppol_item_record_particulars2],
        ),
    ]


def test_get_count() -> list[int]:
    """get_countテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    mst_ppol_item_record1 = MstPpolItemFactory(btId="IBT-001")
    mst_ppol_item_record2 = MstPpolItemFactory(btId="IBT-002")
    mst_ppol_item_deleted_records = MstPpolItemFactory(
        btId="ITB-999", deletedAt=pendulum.now()
    )
    session.add_all(
        [mst_ppol_item_record1, mst_ppol_item_record2, mst_ppol_item_deleted_records]
    )
    session.commit()

    return [
        # case 1 : 全ての情報の数を取得できる
        (2),
    ]
