"""tests/repositories/test_invoice_repository_params.py"""

from typing import Any, Tuple

import pendulum
from api.v1.schemas.invoice import InvoicesFilter
from api.v1.schemas.invoices.downloads.csv import CsvQueryParam
from database import TestSessionLocal
from db.factories import InvoiceFactory, InvoiceReceiveRecordFactory
from enums import (
    DataType,
    IsConfirmation,
    IsDownload,
    IsOpen,
    PaymentMethod,
    Sort,
    SortOrder,
)
from models import Invoice, InvoiceReceiveRecord


def test_find() -> list[tuple[int, Invoice | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_record = InvoiceFactory()
    invoice_deleted_record = InvoiceFactory(deletedAt=pendulum.now())
    session.add_all([invoice_record, invoice_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, invoice_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_by_invoice_id_company_ids() -> list[tuple[int, list[int], Invoice | None]]:
    """get_by_invoice_id_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)

    session.flush()

    invoice_record1 = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add_all([invoice_record1])
    session.commit()

    return [
        # case 1 : IDと企業情報IDに合致している情報が存在
        (1, [1], invoice_record1),
        # case 2 : IDに合致している情報が存在しない
        (999, [1], None),
        # case 3 : 企業情報IDに合致している情報が存在しない
        (1, [999], None),
    ]


def test_get_by_xml_and_company() -> list[tuple[str, int, Invoice | None]]:
    """get_by_xml_and_companyテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)

    session.flush()

    invoice_record1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id, originXmlFileName="test.xml"
    )
    session.add_all([invoice_record1])
    session.commit()

    return [
        # case 1 : XMLファイル名と企業情報IDに合致している情報が存在
        ("test.xml", 1, invoice_record1),
        # case 2 : XMLファイル名に合致している情報が存在しない
        ("test_not_found.xml", 1, None),
        # case 3 : 企業情報IDに合致している情報が存在しない
        ("test.xml", 999, None),
    ]


def test_update_is_download() -> list[tuple[int, IsDownload, Invoice | None]]:
    """update_is_downloadテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)

    session.flush()

    invoice_record = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        isDownload=IsDownload.NOT_DOWNLOADED,
    )
    session.add_all([invoice_record])
    session.commit()

    return [
        # case 1 : ダウンロードフラグを更新
        (1, IsDownload.DOWNLOADED, invoice_record),
        # case 2 : IDに合致している情報が存在しない
        (999, IsDownload.DOWNLOADED, None),
    ]


def test_update_is_confirmation() -> list[tuple[int, IsConfirmation, Invoice | None]]:
    """update_is_confirmationテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)

    session.flush()

    invoice_record = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        isConfirmation=IsConfirmation.UNCONFIRMED,
    )
    session.add_all([invoice_record])
    session.commit()

    return [
        # case 1 : 確認可否を更新
        (1, IsConfirmation.CONFIRMED, invoice_record),
        # case 2 : IDに合致している情報が存在しない
        (999, IsConfirmation.CONFIRMED, None),
    ]


def test_update_is_open() -> list[tuple[int, IsOpen, Invoice | None]]:
    """update_is_openテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(companyInfosId=1)

    session.flush()

    invoice_record = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        isOpen=IsOpen.UNOPENED,
    )
    session.add_all([invoice_record])
    session.commit()

    return [
        # case 1 :開封可否を更新
        (1, IsOpen.OPENED, invoice_record),
        # case 2 : IDに合致している情報が存在しない
        (999, IsOpen.OPENED, None),
    ]


def test_get_all_by_invoices_filter_company_info_company_ids() -> (
    list[tuple[InvoicesFilter, int, list[int], dict[str, Any]]]
):
    """get_all_by_invoices_filter_company_info_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record1 = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        getTimeFrom="2001-01-01 01:01",
        getTimeTo="2002-01-01 01:02",
    )
    invoice_receive_record2 = InvoiceReceiveRecordFactory(
        companyInfosId=2,
        getTimeFrom="2001-01-01 01:01",
        getTimeTo="2002-01-01 01:02",
    )

    session.flush()
    invoice_record1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test1",
        inv_no="1",
        inv_amount=1500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        data_type=DataType.STANDARD,
        inv_no="2",
        inv_amount=2500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
    )
    invoice_record3 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test3",
        inv_no="3",
        inv_amount=3500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.SELF_BILLING,
    )
    invoice_record4 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test4",
        inv_no="4",
        inv_amount=4500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record5 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test5",
        inv_no="5",
        inv_amount=5500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record6 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test6",
        inv_no="6",
        inv_amount=6500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record7 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test7",
        inv_no="7",
        inv_amount=7500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record8 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test8",
        inv_no="8",
        inv_amount=8500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record9 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test9",
        inv_no="9",
        inv_amount=9500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record10 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test10",
        inv_no="10",
        inv_amount=10500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    session.add_all(
        [
            invoice_record1,
            invoice_record2,
            invoice_record3,
            invoice_record4,
            invoice_record5,
            invoice_record6,
            invoice_record7,
            invoice_record8,
            invoice_record9,
            invoice_record10,
        ]
    )
    session.commit()

    return [
        # case 1 : 企業情報IDに合致している情報が存在
        (
            InvoicesFilter(
                company_infos_id=1,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 5,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record4, invoice_receive_record1),
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record8, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
        # case 2 : 企業情報IDに合致している情報が存在
        (
            InvoicesFilter(
                company_infos_id=2,
                page=1,
                size=10,
            ),
            2,
            [2],
            {
                "page": 1,
                "size": 10,
                "total": 5,
                "pages": 1,
                "items": [
                    (invoice_record2, invoice_receive_record2),
                    (invoice_record3, invoice_receive_record2),
                    (invoice_record6, invoice_receive_record2),
                    (invoice_record7, invoice_receive_record2),
                    (invoice_record10, invoice_receive_record2),
                ],
            },
        ),
        # case 3 : 企業情報IDに合致している情報が存在しない
        (
            InvoicesFilter(
                company_infos_id=3,
                page=1,
                size=10,
            ),
            3,
            [3],
            {"page": 1, "size": 10, "total": 0, "pages": 0, "items": []},
        ),
        # case 5 : フリーワードに合致している情報が存在
        (
            InvoicesFilter(
                free_word="test1",
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 1,
                "pages": 1,
                "items": [(invoice_record1, invoice_receive_record1)],
            },
        ),
        # case 6 : 請求書番号に合致している情報が存在
        (
            InvoicesFilter(
                inv_no="1",
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 1,
                "pages": 1,
                "items": [(invoice_record1, invoice_receive_record1)],
            },
        ),
        # case 7 : 請求書タイプに合致している情報が存在
        (
            InvoicesFilter(
                data_type=DataType.STANDARD,
                page=1,
                size=10,
            ),
            2,
            [2],
            {
                "page": 1,
                "size": 10,
                "total": 4,
                "pages": 1,
                "items": [
                    (invoice_record2, invoice_receive_record2),
                    (invoice_record6, invoice_receive_record2),
                    (invoice_record7, invoice_receive_record2),
                    (invoice_record10, invoice_receive_record2),
                ],
            },
        ),
        # case 9 : 請求金額からに合致している情報が存在
        (
            InvoicesFilter(
                from_inv_amount=5000,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 3,
                "pages": 1,
                "items": [
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record8, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
        # case 10 : 請求金額までに合致している情報が存在
        (
            InvoicesFilter(
                to_inv_amount=1500,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 1,
                "pages": 1,
                "items": [(invoice_record1, invoice_receive_record1)],
            },
        ),
        # case 11 : 支払方法に合致している情報が存在
        (
            InvoicesFilter(
                payment_method=PaymentMethod.CREDIT_CARD,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 2,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record4, invoice_receive_record1),
                ],
            },
        ),
        # case 12 : 開封可否に合致している情報が存在
        (
            InvoicesFilter(
                is_open=IsOpen.OPENED,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 3,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
        # case 13 : ダウンロード可否に合致している情報が存在
        (
            InvoicesFilter(
                is_download=IsDownload.DOWNLOADED,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 3,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
        # case 14 : 確認可否に合致している情報が存在
        (
            InvoicesFilter(
                is_confirmation=IsConfirmation.CONFIRMED,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 3,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
        # case 15 : 受信日時からに合致している情報が存在しない
        (
            InvoicesFilter(
                from_receive_date_time="2024-12-30 00:00",
                sort=Sort.RECEIVE_DATE_TIME,
                sort_order=SortOrder.ASC,
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 0,
                "pages": 0,
                "items": [],
            },
        ),
        # case 16 : 受信日時までに合致している情報が存在
        (
            InvoicesFilter(
                to_receive_date_time="2024-12-31 23:59",
                page=1,
                size=10,
            ),
            1,
            [1],
            {
                "page": 1,
                "size": 10,
                "total": 5,
                "pages": 1,
                "items": [
                    (invoice_record1, invoice_receive_record1),
                    (invoice_record4, invoice_receive_record1),
                    (invoice_record5, invoice_receive_record1),
                    (invoice_record8, invoice_receive_record1),
                    (invoice_record9, invoice_receive_record1),
                ],
            },
        ),
    ]


def test_get_all_by_csv_filter_company_info_company_ids() -> (
    list[tuple[CsvQueryParam, int, list[int], list[Tuple[Any]]]]
):
    """get_all_by_csv_filter_company_info_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record1 = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        getTimeFrom="2001-01-01 01:01",
        getTimeTo="2002-01-01 01:02",
    )
    invoice_receive_record2 = InvoiceReceiveRecordFactory(
        companyInfosId=2,
        getTimeFrom="2001-01-01 01:01",
        getTimeTo="2002-01-01 01:02",
    )

    session.flush()
    invoice_record1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test1",
        inv_no="1",
        inv_amount=1500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        data_type=DataType.STANDARD,
        inv_no="2",
        inv_amount=2500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
    )
    invoice_record3 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test3",
        inv_no="3",
        inv_amount=3500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.SELF_BILLING,
    )
    invoice_record4 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test4",
        inv_no="4",
        inv_amount=4500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record5 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test5",
        inv_no="5",
        inv_amount=5500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record6 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test6",
        inv_no="6",
        inv_amount=6500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record7 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test7",
        inv_no="7",
        inv_amount=7500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record8 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test8",
        inv_no="8",
        inv_amount=8500,
        payment_method=PaymentMethod.BANK_TRANSFER,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record9 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
        remarks="test9",
        inv_no="9",
        inv_amount=9500,
        payment_method=PaymentMethod.CASH,
        isOpen=IsOpen.OPENED,
        isDownload=IsDownload.DOWNLOADED,
        isConfirmation=IsConfirmation.CONFIRMED,
        data_type=DataType.STANDARD,
    )
    invoice_record10 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
        remarks="test10",
        inv_no="10",
        inv_amount=10500,
        payment_method=PaymentMethod.CREDIT_CARD,
        isOpen=IsOpen.UNOPENED,
        isDownload=IsDownload.NOT_DOWNLOADED,
        isConfirmation=IsConfirmation.UNCONFIRMED,
        data_type=DataType.STANDARD,
    )
    session.add_all(
        [
            invoice_record1,
            invoice_record2,
            invoice_record3,
            invoice_record4,
            invoice_record5,
            invoice_record6,
            invoice_record7,
            invoice_record8,
            invoice_record9,
            invoice_record10,
        ]
    )
    session.commit()

    return [
        # case 1 : 企業情報IDに合致している情報が存在
        (
            CsvQueryParam(
                company_infos_id=1,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record4.id,),
                (invoice_record5.id,),
                (invoice_record8.id,),
                (invoice_record9.id,),
            ],
        ),
        # case 2 : 企業情報IDに合致している情報が存在
        (
            CsvQueryParam(
                company_infos_id=2,
            ),
            2,
            [2],
            [
                (invoice_record2.id,),
                (invoice_record3.id,),
                (invoice_record6.id,),
                (invoice_record7.id,),
                (invoice_record10.id,),
            ],
        ),
        # case 3 : 企業情報IDに合致している情報が存在しない
        (
            CsvQueryParam(
                company_infos_id=3,
            ),
            3,
            [3],
            [],
        ),
        # case 5 : フリーワードに合致している情報が存在
        (
            CsvQueryParam(
                free_word="test1",
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
            ],
        ),
        # case 6 : 請求書番号に合致している情報が存在
        (
            CsvQueryParam(
                inv_no="1",
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
            ],
        ),
        # case 7 : 請求書タイプに合致している情報が存在
        (
            CsvQueryParam(
                data_type=DataType.STANDARD,
            ),
            2,
            [2],
            [
                (invoice_record2.id,),
                (invoice_record6.id,),
                (invoice_record7.id,),
                (invoice_record10.id,),
            ],
        ),
        # case 9 : 請求金額からに合致している情報が存在
        (
            CsvQueryParam(
                from_inv_amount=5000,
            ),
            1,
            [1],
            [
                (invoice_record5.id,),
                (invoice_record8.id,),
                (invoice_record9.id,),
            ],
        ),
        # case 10 : 請求金額までに合致している情報が存在
        (
            CsvQueryParam(
                to_inv_amount=1500,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
            ],
        ),
        # case 11 : 支払方法に合致している情報が存在
        (
            CsvQueryParam(
                payment_method=PaymentMethod.CREDIT_CARD,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record4.id,),
            ],
        ),
        # case 12 : 開封可否に合致している情報が存在
        (
            CsvQueryParam(
                is_open=IsOpen.OPENED,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record5.id,),
                (invoice_record9.id,),
            ],
        ),
        # case 13 : ダウンロード可否に合致している情報が存在
        (
            CsvQueryParam(
                is_download=IsDownload.DOWNLOADED,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record5.id,),
                (invoice_record9.id,),
            ],
        ),
        # case 14 : 確認可否に合致している情報が存在
        (
            CsvQueryParam(
                is_confirmation=IsConfirmation.CONFIRMED,
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record5.id,),
                (invoice_record9.id,),
            ],
        ),
        # case 15 : 受信日時からに合致している情報が存在しない
        (
            CsvQueryParam(
                from_receive_date_time="2024-12-30 00:00",
                sort=Sort.RECEIVE_DATE_TIME,
                sort_order=SortOrder.ASC,
            ),
            1,
            [1],
            [],
        ),
        # case 16 : 受信日時までに合致している情報が存在
        (
            CsvQueryParam(
                to_receive_date_time="2024-12-31 23:59",
            ),
            1,
            [1],
            [
                (invoice_record1.id,),
                (invoice_record4.id,),
                (invoice_record5.id,),
                (invoice_record8.id,),
                (invoice_record9.id,),
            ],
        ),
    ]


def test_insert_by_invoice() -> list[tuple[Invoice, Invoice]]:
    """insert_by_invoiceテスト"""
    invoice_receive_record = InvoiceReceiveRecordFactory()

    return [
        # case 1 : 請求書情報を登録
        (invoice_receive_record, invoice_receive_record),
    ]


def test_get_all_by_invoice_ids_company_ids() -> (
    list[tuple[list[int], list[int], list[Tuple[Invoice, InvoiceReceiveRecord]]]]
):
    """get_all_by_invoice_ids_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record1 = InvoiceReceiveRecordFactory(companyInfosId=1)
    invoice_receive_record2 = InvoiceReceiveRecordFactory(companyInfosId=2)

    session.flush()
    invoice_record1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record1.id,
    )
    invoice_record2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record2.id,
    )
    session.add_all([invoice_record1, invoice_record2])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (
            [1, 2],
            [1, 2],
            [
                (invoice_record1, invoice_receive_record1),
                (invoice_record2, invoice_receive_record2),
            ],
        ),
        # case 2 : IDに合致している情報が存在しない
        ([999], [1], []),
        # case 3 : 企業情報IDに合致している情報が存在しない
        ([1], [999], []),
    ]
