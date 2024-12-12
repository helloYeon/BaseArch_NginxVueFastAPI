"""tests/services/test_download_service_params.py"""

from typing import Any

from api.v1.schemas.invoices.downloads.previews import BaseItem
from core.constant import const
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
)
from enums import ReceiveRecordStatus
from exceptions.peppol_http_exception import PeppolHttpException


def test_download_xml() -> list[tuple[int, list[int], str]]:
    """download_xmlテストパラメータ"""
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
        s3FullPath="tests/testfile.txt",
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : ファイル取得成功
        (1, [1], "testfile.txt")
    ]


def test_download_xml_exception() -> list[tuple[int, list[int], dict[str, Any]]]:
    """download_xml例外テストパラメータ"""
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
        s3FullPath="tests/exception_testfile.txt",
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 存在しないinvoice_idを指定
        (
            999,
            [1],
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
        # case 2 : 存在しないcompany_idsを指定
        (
            1,
            [999],
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
        # case 3 : ファイル取得失敗
        (
            1,
            [1],
            {
                "exception": PeppolHttpException,
                "message": messages.XML_DOWNLOAD_FAILED_MESSAGE.message,
            },
        ),
    ]


def test_get_preview_data() -> list[tuple[int, BaseItem]]:
    """get_preview_dataテストパラメータ"""
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
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : invoice_id: 1のプレビュー用データ取得
        (
            1,
            BaseItem(
                data_type=invoice.data_type,
                currencyCode=invoice.IBT005,
                customer=invoice.customer,
                publisher=invoice.publisher,
                contact=invoice.contact,
                list_info=invoice.list_info,
                inv_no=invoice.inv_no,
                close_date=(
                    invoice.close_date.strftime(const.DATE_FORMAT)
                    if invoice.close_date is not None
                    else None
                ),
                pay_due_date=(
                    invoice.pay_due_date.strftime(const.DATE_FORMAT)
                    if invoice.pay_due_date is not None
                    else None
                ),
                inv_amount=invoice.inv_amount,
                inv_name=invoice.inv_name,
                prev_inv_amount=invoice.prev_inv_amount,
                payment=invoice.payment,
                adjustment=invoice.adjustment,
                carryover_new=invoice.carryover_new,
                inv_without_tax=invoice.inv_without_tax,
                inv_tax=invoice.inv_tax,
                inv_show_amount=invoice.inv_show_amount,
                inv_without_tax_tr10=invoice.inv_without_tax_tr10,
                inv_without_tax_tr8=invoice.inv_without_tax_tr8,
                inv_without_tax_tr8_reduced=invoice.inv_without_tax_tr8_reduced,
                inv_without_tax_tr5=invoice.inv_without_tax_tr5,
                inv_without_tax_tr0=invoice.inv_without_tax_tr0,
                inv_without_tax_free=invoice.inv_without_tax_free,
                inv_without_tax_non=invoice.inv_without_tax_non,
                inv_without_tax_exemption=invoice.inv_without_tax_exemption,
                inv_tax_tr10=invoice.inv_tax_tr10,
                inv_tax_tr8=invoice.inv_tax_tr8,
                inv_tax_tr8_reduced=invoice.inv_tax_tr8_reduced,
                inv_tax_tr5=invoice.inv_tax_tr5,
                inv_tax_tr0=invoice.inv_tax_tr0,
                inv_tax_free=invoice.inv_tax_free,
                inv_tax_non=invoice.inv_tax_non,
                inv_tax_exemption=invoice.inv_tax_exemption,
                inv_amount_tr10=invoice.inv_amount_tr10,
                inv_amount_tr8=invoice.inv_amount_tr8,
                inv_amount_tr8_reduced=invoice.inv_amount_tr8_reduced,
                inv_amount_tr5=invoice.inv_amount_tr5,
                inv_amount_tr0=invoice.inv_amount_tr0,
                inv_amount_free=invoice.inv_amount_free,
                inv_amount_non=invoice.inv_amount_non,
                inv_amount_exemption=invoice.inv_amount_exemption,
                payment_method=invoice.payment_method,
                banks=invoice.banks,
                remarks=invoice.remarks,
                details=invoice.details,
            ),
        )
    ]


def test_get_preview_data_exception() -> list[tuple[int, dict[str, Any]]]:
    """get_preview_data例外テストパラメータ"""
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
    )
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 存在しないinvoice_idを指定
        (
            999,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]
