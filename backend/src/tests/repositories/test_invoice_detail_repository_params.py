"""tests/repositories/test_invoice_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import (
    InvoiceDetailFactory,
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
)
from models import InvoiceDetail


def test_find() -> list[tuple[int, InvoiceDetail | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_detail_record = InvoiceDetailFactory()
    invoice_detail_deleted_record = InvoiceDetailFactory(deletedAt=pendulum.now())
    session.add_all([invoice_detail_record, invoice_detail_deleted_record])
    session.commit()

    return [
        # case 1 : 請求書明細IDに合致している情報が存在
        (1, invoice_detail_record),
        # # case 2 : 請求書明細IDに合致している情報が存在しない
        (999, None),
        # case 3 : 請求書明細IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_by_invoice_detail_id_company_ids() -> (
    list[tuple[int, list[int], InvoiceDetail | None]]
):
    """get_by_invoice_detail_id_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)
    session.flush()

    invoice_record1 = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.flush()

    invoice_detail = InvoiceDetailFactory(invoiceId=invoice_record1.id)
    session.add_all([invoice_detail])
    session.commit()

    return [
        # case 1 : 請求書明細IDに合致している情報が存在
        (invoice_detail.id, [invoice_receive_record.companyInfosId], invoice_detail),
        # case 2 : 請求書明細IDに合致している情報が存在しない
        (999, [invoice_receive_record.companyInfosId], None),
        # case 3 : 所属・結合企業情報IDに合致している情報が存在しない
        (invoice_detail.id, [999], None),
    ]


def test_get_all_by_invoice_id_company_ids() -> (
    list[tuple[int, list[int], list[InvoiceDetail]]]
):
    """get_all_by_invoice_id_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)
    session.flush()

    invoice_record1 = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.flush()

    invoice_detail1 = InvoiceDetailFactory(invoiceId=invoice_record1.id)
    invoice_detail2 = InvoiceDetailFactory(invoiceId=invoice_record1.id)
    invoice_detail3 = InvoiceDetailFactory(invoiceId=888)
    session.add_all([invoice_detail1, invoice_detail2, invoice_detail3])
    session.commit()

    return [
        # case 1 : 請求書IDに合致している情報が存在
        (
            invoice_record1.id,
            [invoice_receive_record.companyInfosId],
            [invoice_detail1, invoice_detail2],
        ),
        # case 2 : 請求書IDに合致している情報が存在しない
        (999, [invoice_receive_record.companyInfosId], []),
        # case 3 : 所属・結合企業情報IDに合致している情報が存在しない
        (invoice_record1.id, [999], []),
    ]


def test_insert_by_invoice_details() -> list[tuple[list[InvoiceDetail], None]]:
    """insert_by_invoice_detailsテスト"""
    invoice_detail1 = InvoiceDetailFactory(invoiceId=1)
    invoice_detail2 = InvoiceDetailFactory(invoiceId=1)

    return [
        # case 1 : 請求書明細情報を登録できる
        ([invoice_detail1, invoice_detail2], None),
    ]
