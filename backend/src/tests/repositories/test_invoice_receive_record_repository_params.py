"""tests/repositories/test_invoice_receive_record_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import InvoiceReceiveRecordFactory
from enums import ReceiveRecordStatus
from models import InvoiceReceiveRecord


def test_find() -> list[tuple[int, InvoiceReceiveRecord | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory()
    invoice_receive_deleted_record = InvoiceReceiveRecordFactory(
        deletedAt=pendulum.now()
    )
    session.add_all([invoice_receive_record, invoice_receive_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, invoice_receive_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_by_company_infos_id_status() -> (
    list[tuple[int, ReceiveRecordStatus, InvoiceReceiveRecord | None]]
):
    """get_by_company_infos_id_statusテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2001-01-01 01:01",
    )
    invoice_receive_record2 = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2001-01-01 01:02",
    )
    invoice_receive_record3 = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.RECEIVE_NG,
        getTimeTo="2001-01-01 01:03",
    )
    invoice_receive_record4 = InvoiceReceiveRecordFactory(
        companyInfosId=2,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2001-01-01 01:04",
    )
    invoice_receive_deleted_record = InvoiceReceiveRecordFactory(
        deletedAt=pendulum.now()
    )
    session.add_all(
        [
            invoice_receive_record,
            invoice_receive_record2,
            invoice_receive_record3,
            invoice_receive_record4,
            invoice_receive_deleted_record,
        ]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, ReceiveRecordStatus.INSERT_OK, invoice_receive_record2),
        # # case 2 : IDに合致している情報が存在しない
        (999, ReceiveRecordStatus.INSERT_OK, None),
    ]


def test_insert_by_invoice_receive_record() -> (
    list[tuple[InvoiceReceiveRecord, InvoiceReceiveRecord]]
):
    """insert_by_invoice_receive_recordテスト"""
    invoice_receive_record = InvoiceReceiveRecordFactory()

    return [
        # case 1 : 登録できる
        (invoice_receive_record, invoice_receive_record),
    ]


def test_update_status() -> list[tuple[int, ReceiveRecordStatus, None]]:
    """update_statusテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory()
    session.add(invoice_receive_record)
    session.commit()

    return [
        # case 1 : ステータスを更新できる
        (invoice_receive_record.id, ReceiveRecordStatus.RECEIVE_OK, None),
    ]
