"""tests/services/test_invoice_detail_service_params.py"""

import pendulum
from api.v1.schemas.invoices.details import BaseItem
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    InvoiceDetailFactory,
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
)
from enums.receive_record_status import ReceiveRecordStatus
from exceptions import PeppolHttpException


def test_get_invoice_detail() -> list[tuple[int, BaseItem]]:
    """get_invoice_detailテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.flush()
    invoice_detail = InvoiceDetailFactory(invoiceId=invoice.id)
    session.add(invoice_detail)
    session.commit()

    return [
        # case 1 : invoice_detailに合致している請求書明細が存在
        (
            invoice_detail.id,
            BaseItem(
                IBT126=invoice_detail.IBT126,
                IBT127=invoice_detail.IBT127,
                AUTO87=invoice_detail.AUTO87,
                IBT129=invoice_detail.IBT129,
                IBT131=invoice_detail.IBT131,
                AUTO82=invoice_detail.AUTO82,
                IBT133=invoice_detail.IBT133,
                IBG26=invoice_detail.IBG26,
                AUTO84=invoice_detail.AUTO84,
                IBG36=invoice_detail.IBG36,
                IBG27=invoice_detail.IBG27,
                IBG28=invoice_detail.IBG28,
                IBG31=invoice_detail.IBG31,
                IBG29=invoice_detail.IBG29,
            ),
        )
    ]


def test_get_invoice_detail_exception() -> list[tuple[int, dict]]:
    """get_invoice_detail例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()
    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.flush()
    invoice_detail = InvoiceDetailFactory(
        invoiceId=invoice.id, deletedAt=pendulum.now()
    )
    session.add(invoice_detail)
    session.commit()

    return [
        # case 1 : invoice_detail_idが合致していない
        (
            999,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
        # case 3 : company_idsが合致しているが削除されている
        (
            1,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]
