"""tests/services/test_csv_service_params.py"""

import os
import tempfile
from datetime import date
from typing import Any

from api.v1.schemas.invoices.downloads.csv import CsvQueryParam, PpolItem
from core.constant import const
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    InvoiceDetailFactory,
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
    PaymentCodeFactory,
)
from enums import IsOpen, ReceiveRecordStatus, Sort, SortOrder
from exceptions import PeppolHttpException
from fastapi import Response
from models import Invoice, User


def test_get_invoices_id_list() -> list[tuple[CsvQueryParam, int, list[int]]]:
    """get_invoices_id_listテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        isOpen=IsOpen.OPENED,
        inv_no="test_inv_no",
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 条件に合致している請求書が存在
        (
            CsvQueryParam(
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.OPENED,
                inv_no="test_inv_no",
            ),
            1,
            [1],
        )
    ]


def test_get_invoices_id_list_exception() -> list[tuple[CsvQueryParam, int, dict]]:
    """get_invoices_id_list例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        isOpen=IsOpen.UNOPENED,
        inv_no="test_inv_no",
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 条件に合致している請求書が存在しない
        (
            CsvQueryParam(
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.OPENED,
                inv_no="test_inv_no",
            ),
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_SEARCH_RESULT_NOT_FOUND.message,
            },
        )
    ]


def test_csv_replace() -> list[tuple[str, str]]:
    """csv_replaceテストパラメータ"""
    return [
        # case 1 : 改行を含む文字列
        (
            "te\n\rst",
            "test",
        )
    ]


def test_filter_mst_item_with_sort() -> list[tuple[int, list[PpolItem], PpolItem]]:
    """filter_mst_item_with_sortテストパラメータ"""
    return [
        # case 1 : mstSortOrder1を検索
        (
            1,
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                ),
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=2,
                    parentSort=0,
                ),
            ],
            PpolItem(
                btid="IBT-024",
                name="CustomizationID",
                mstSortOrder=1,
                parentSort=0,
            ),
        )
    ]


def test_make_csv_title() -> list[tuple[list[PpolItem], list[str]]]:
    """make_csv_titleテストパラメータ"""
    return [
        # case 1 : "CustomizationID"を抽出
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            ["CustomizationID"],
        ),
    ]


def test_get_item_key() -> list[tuple[PpolItem, list[str]]]:
    """get_item_keyテストパラメータ"""
    return [
        # case 1 : "IBT024"を抽出
        (
            PpolItem(
                btid="IBT-024",
                name="CustomizationID",
                mstSortOrder=1,
                parentSort=0,
            ),
            ["IBT024"],
        )
    ]


def test_get_csv_value() -> list[tuple[PpolItem, dict, str]]:
    """get_csv_valueテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice = InvoiceFactory(
        IBT024="unittestIBT024",
    )
    session.add(invoice)
    session.commit()

    invoice_record = session.query(Invoice).one()

    return [
        # case 1 : IBT-024の値を取得
        (
            PpolItem(
                btid="IBT-024",
                name="CustomizationID",
                mstSortOrder=1,
                parentSort=0,
            ),
            invoice_record.__dict__,
            "unittestIBT024",
        ),
    ]


def test_get_invoice_payment_code() -> list[tuple[dict, int, str | None]]:
    """get_invoice_payment_codeテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )

    session.add(payment_code)
    session.commit()

    return [
        # case 1 : publisherから支払先コードが取得できる
        (
            {"publisher_peppol_scheme_id": 1111, "publisher_peppol_id": "T1234567890"},
            1,
            "unittestPaymentCode",
        ),
        # case 2 : publisherから支払先コードが取得できる(小文字大文字区別なし)
        (
            {"publisher_peppol_scheme_id": 1111, "publisher_peppol_id": "t1234567890"},
            1,
            "unittestPaymentCode",
        ),
        # case 3 : publisherから支払先コードが取得できない(企業情報IDが違う)
        (
            {"publisher_peppol_scheme_id": 1111, "publisher_peppol_id": "T1234567890"},
            999,
            None,
        ),
        # case 3 : publisherから支払先コードが取得できない
        (
            {"publisher_peppol_scheme_id": None, "publisher_peppol_id": "T1234567890"},
            1,
            None,
        ),
    ]


def test_get_csv_value_common() -> list[tuple[PpolItem, Invoice, int, str]]:
    """get_csv_value_commonテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice = InvoiceFactory(
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    session.add(invoice)

    payment_code = PaymentCodeFactory(
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )
    session.add(payment_code)
    session.commit()

    return [
        # case 1 : 該当する支払先コードが存在する
        (
            PpolItem(
                btid="",
                name=const.PAYMENT_CODE_NAME,
                mstSortOrder=1,
                parentSort=0,
            ),
            invoice,
            1,
            "unittestPaymentCode",
        ),
    ]


def test_get_csv_value_common_exception() -> list[tuple[PpolItem, Invoice, int, dict]]:
    """get_csv_value_common例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 該当する支払先コードが存在しない
        (
            PpolItem(
                btid="",
                name=const.PAYMENT_CODE_NAME,
                mstSortOrder=1,
                parentSort=0,
            ),
            invoice,
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.PAYMENT_CODE_NOT_FOUND.message,
            },
        ),
    ]


def test_make_csv_row_for_common() -> list[tuple[list[PpolItem], list[str]]]:
    """make_csv_row_for_commonテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    session.add(invoice)
    session.flush()

    payment_code = PaymentCodeFactory(
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )
    session.add(payment_code)
    session.commit()

    return [
        # case 1 : 支払先コードの値を取得
        (
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            ["unittestPaymentCode"],
        ),
    ]


def test_make_csv_row_for_common_exception() -> list[tuple[list[PpolItem], dict]]:
    """make_csv_row_for_common例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record1 = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record1)
    session.flush()

    invoice = InvoiceFactory(
        invoiceReceiveRecordsId=999,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    session.add(invoice)
    session.flush()

    payment_code = PaymentCodeFactory(
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )
    session.add(payment_code)
    session.commit()

    return [
        # case 1 : 請求書が存在しない
        (
            [
                PpolItem(
                    btid="",
                    name=const.PAYMENT_CODE_NAME,
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        )
    ]


def test_make_csv_row_for_invoice() -> list[tuple[list[PpolItem], list[str]]]:
    """make_csv_row_for_invoiceテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(IBT024="unittestIBT024")
    session.add(invoice)
    session.commit()

    return [
        # case 1 : IBT-024の値を取得
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            ["unittestIBT024"],
        ),
    ]


def test_make_csv_row_for_invoice_exception() -> list[tuple[list[PpolItem], dict]]:
    """make_csv_row_for_invoice例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(invoiceReceiveRecordsId=999, IBT024="unittestIBT024")
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 請請求書が存在しない
        (
            [
                PpolItem(
                    btid="IBT-024",
                    name="CustomizationID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_make_csv_rows_for_detail() -> list[tuple[list[PpolItem], list[list[str]]]]:
    """make_csv_rows_for_detailテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory()
    session.add(invoice)
    session.flush()

    invoice_detail = InvoiceDetailFactory(invoiceId=1, IBT126="unittestIBT126")
    session.add(invoice_detail)
    session.commit()

    return [
        # case 1 : IBT-126の値を取得
        (
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            [["unittestIBT126"]],
        ),
    ]


def test_make_csv_rows_for_detail_exception() -> list[tuple[list[PpolItem], dict]]:
    """make_csv_rows_for_detail例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory()
    session.add(invoice)
    session.flush()

    invoice_detail = InvoiceDetailFactory(invoiceId=999, IBT126="unittestIBT126")
    session.add(invoice_detail)
    session.commit()

    return [
        # case 1 :invoice_idに合致する請求書明細が存在しない
        (
            [
                PpolItem(
                    btid="IBT-126",
                    name="ID",
                    mstSortOrder=1,
                    parentSort=0,
                )
            ],
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_check_request_invoices() -> list[tuple[list[int], list[Any]]]:
    """check_request_invoicesテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    invoice2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T9876543210",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    invoice3 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "ta123456789",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    invoice4 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "ta987654321",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    session.add(invoice1)
    session.add(invoice2)
    session.add(invoice3)
    session.add(invoice4)

    payment_code = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )
    payment_code2 = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:Ta123456789",
        paymentCode="unittestPaymentCode",
    )
    payment_code3 = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:TA987654321",
        paymentCode="unittestPaymentCode",
    )
    session.add(payment_code)
    session.add(payment_code2)
    session.add(payment_code3)
    session.commit()

    return [
        # case 1 : 支払先コード一覧に請求書のcompany_infos_idとpeppol_idの組み合わせに一致するものがある
        ([1], []),
        # case 2 : 支払先コード一覧に請求書のcompany_infos_idとpeppol_idの組み合わせに一致するものがない
        ([2], ["1111:T9876543210"]),
        # case 3 : tの大文字小文字の違いのみの場合一致するものがある
        ([3], []),
        # case 4 : t以外の大文字小文字の違いがある場合一致するものがない
        ([4], ["1111:Ta987654321"]),
    ]


def test_generate_csv_with_fixed_fields() -> list[tuple[CsvQueryParam, User, str, str]]:
    """generate_csv_with_fixed_fieldsテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    invoice2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )
    invoice3 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )
    invoice4 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )

    payment_code = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )

    session.add_all([invoice1, invoice2, invoice3, invoice4, payment_code])
    session.commit()

    # 一時フォルダとCSVファイルパスを生成
    temp_folder = tempfile.mkdtemp()
    temp_csv_path = f"{temp_folder}/test.csv"

    return [
        # case 1 : 指定されたcsvファイルに正常に書き込みが完了
        (
            CsvQueryParam(
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.OPENED,
            ),
            User(companyInfosId=1),
            temp_csv_path,
            temp_csv_path,
        )
    ]


def test_generate_fixed_csv_row() -> list[tuple[Invoice, dict, int, list[str]]]:
    """generate_fixed_csv_rowテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        inv_no="S-82231",
        inv_name=None,
        pay_due_date=date(2001, 10, 7),
        prev_inv_amount=113,
        payment=336,
        adjustment=351838416,
        carryover_new=3,
        inv_without_tax=53255.7,
        inv_tax=19,
        inv_amount=76303301,
        inv_show_amount=196,
        close_date=date(2017, 5, 28),
        remarks="びこう",
        details=[
            {
                "item_qty": 1,
                "item_tax": 100,
                "tax_type": "0",
                "item_name": "商品明細",
                "item_unit": "個",
                "item_price": 1000,
                "item_amount": 1100,
                "item_slip_no": "1",
                "tax_rate_sec": 10,
                "item_sec_code": "BMCD001",
                "item_sec_name": "部門",
                "tax_calc_type": "1",
                "detail_remarks": "備考",
                "input_tax_type": "0",
                "item_free_txt1": "明細の自由項目1",
                "item_free_txt2": "明細の自由項目2",
                "item_free_txt3": "明細の自由項目3",
                "item_free_txt4": "明細の自由項目4",
                "item_free_txt5": "明細の自由項目5",
                "item_free_txt6": "明細の自由項目6",
                "item_free_txt7": "明細の自由項目7",
                "item_free_txt8": "明細の自由項目8",
                "item_free_txt9": "明細の自由項目9",
                "item_prod_code": "SH001",
                "item_slip_date": "2023-12-12",
                "sum_exempt_flg": "0",
                "item_free_txt10": "明細の自由項目10",
                "item_free_txt_l": "明細の自由項目11",
                "reduced_tax_flg": "0",
                "item_without_tax": 1000,
            }
        ],
    )

    payment_code = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )

    session.add(payment_code)
    session.commit()

    return [
        # case 1 : invoiceモデルから正常にcsv行を生成できる
        (
            invoice,
            invoice.details[0],
            1,
            [
                "S-82231",
                "unittestPaymentCode",
                "",
                "2001/10/07",
                "113",
                "336",
                "351838416",
                "3",
                "53255.7",
                "19",
                "76303301",
                "196",
                "2017/05/28",
                "びこう",
                "2023/12/12",
                "1",
                "SH001",
                "商品明細",
                "1",
                "1000",
                "個",
                "1000",
                "100",
                "1100",
                "課税",
                "10%",
                "税抜",
                "BMCD001",
                "部門",
                "備考",
                "",
                "",
            ],
        )
    ]


def test_generate_csv_with_custom_fields() -> list[
    tuple[
        CsvQueryParam,
        User,
        list[PpolItem],
        list[PpolItem],
        list[PpolItem],
        str,
        str,
    ]
]:
    """generate_csv_with_custom_fieldsテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1,
        status=ReceiveRecordStatus.INSERT_OK,
        getTimeTo="2002-01-01 01:02",
    )
    session.add(invoice_receive_record)
    session.flush()

    invoice1 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
    )
    invoice2 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )
    invoice3 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )
    invoice4 = InvoiceFactory(
        invoiceReceiveRecordsId=invoice_receive_record.id,
        publisher={
            "publisher_peppol_id": "T1234567890",
            "publisher_peppol_scheme_id": "1111",
        },
        isOpen=IsOpen.OPENED,
    )

    payment_code = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:T1234567890",
        paymentCode="unittestPaymentCode",
    )

    session.add_all([invoice1, invoice2, invoice3, invoice4, payment_code])
    session.flush()

    invoice_detail1 = InvoiceDetailFactory(invoiceId=invoice1.id)
    invoice_detail2 = InvoiceDetailFactory(invoiceId=invoice2.id)
    invoice_detail3 = InvoiceDetailFactory(invoiceId=invoice3.id)
    invoice_detail4 = InvoiceDetailFactory(invoiceId=invoice4.id)
    session.add_all(
        [invoice_detail1, invoice_detail2, invoice_detail3, invoice_detail4]
    )
    session.commit()

    # 一時フォルダとCSVファイルパスを生成
    temp_folder = tempfile.mkdtemp()
    temp_csv_path = f"{temp_folder}/test.csv"

    return [
        # case 1 : 指定されたcsvファイルに正常に書き込みが完了
        (
            CsvQueryParam(
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.OPENED,
            ),
            User(companyInfosId=1),
            [PpolItem(btid="", name="支払先コード", mstSortOrder=1, parentSort=0)],
            [
                PpolItem(
                    btid="IBT-073",
                    name="請求期間開始日",
                    mstSortOrder=15,
                    parentSort=14,
                ),
                PpolItem(
                    btid="IBT-008",
                    name="課税基準日コード",
                    mstSortOrder=17,
                    parentSort=14,
                ),
                PpolItem(
                    btid="IBT-024",
                    name="ビジネスプロセスタイプ",
                    mstSortOrder=1,
                    parentSort=0,
                ),
            ],
            [
                PpolItem(
                    btid="IBT-134",
                    name="請求書明細行の期間開始日",
                    mstSortOrder=7,
                    parentSort=6,
                ),
                PpolItem(
                    btid="IBT-126", name="請求書明細行ID", mstSortOrder=1, parentSort=0
                ),
            ],
            temp_csv_path,
            temp_csv_path,
        )
    ]


def test_create_csv_response() -> list[tuple[str, str, Response]]:
    """create_csv_responseテストパラメータ"""
    # ファイルの内容を読み取る
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../../storage/for_test/test.csv",
        ),
        mode="r",
        encoding="CP932",
    ) as file:
        content = file.read().encode("CP932", errors="replace")

    return [
        # case 1 : 指定先のファイルパスが存在する
        (
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../../storage/for_test/test.csv",
            ),
            "test.csv",
            Response(
                content=content,
                media_type="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=test.csv",
                },
            ),
        )
    ]
