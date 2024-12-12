"""tests/services/test_invoice_service_params.py"""

import pendulum
import requests
from api.v1.schemas.invoice import (
    InvoiceBaseItem,
    InvoiceListItem,
    InvoicesFilter,
    InvoicesListBaseItem,
)
from api.v1.schemas.invoices.peppol import BaseItem, invoiceLineInPeppolDetailItem
from core.constant import const
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    InvoiceDetailFactory,
    InvoiceFactory,
    InvoiceReceiveRecordFactory,
)
from enums import (
    IsConfirmation,
    IsDownload,
    IsOpen,
    Sort,
    SortOrder,
)
from enums.receive_record_status import ReceiveRecordStatus
from exceptions import PeppolHttpException
from fastapi import status
from models import User


def test_get_invoices_list() -> (
    list[tuple[InvoicesFilter, int, list[int], InvoicesListBaseItem]]
):
    """get_invoices_listテストパラメータ"""
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
        # case 1 : 検索条件に合致している請求書が存在
        (
            InvoicesFilter(
                page=1,
                size=10,
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.OPENED,
                inv_no="test_inv_no",
                to_receive_date_time="2002-01-01 01:02",
            ),
            1,
            [1],
            InvoicesListBaseItem(
                page=1,
                pages=1,
                size=10,
                total=1,
                items=[
                    InvoiceListItem(
                        invoiceId=invoice.id,
                        data_type=invoice.data_type,
                        inv_no=invoice.inv_no,
                        publisher=invoice.publisher,
                        pay_due_date=invoice.pay_due_date.strftime(const.DATE_FORMAT),
                        inv_amount=invoice.inv_amount,
                        currencyCode=invoice.IBT005,
                        payment_method=invoice.payment_method,
                        isOpen=invoice.isOpen,
                        isConfirmation=invoice.isConfirmation,
                        isDownload=invoice.isDownload,
                        list_info=invoice.list_info,
                        receiveDateTime=invoice_receive_record.getTimeTo.strftime(
                            const.DATE_TIME_FORMAT
                        ),
                    )
                ],
                lastReceiveDateTime="2002-01-01 01:02",
            ),
        ),
        # case 2 : 検索条件に合致している請求書が存在しない
        (
            InvoicesFilter(
                page=1,
                size=10,
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
                is_open=IsOpen.UNOPENED,
                inv_no="test_inv_no",
                to_receive_date_time="2002-01-01 01:02",
            ),
            1,
            [1],
            InvoicesListBaseItem(
                page=1,
                pages=0,
                size=10,
                total=0,
                items=[],
                lastReceiveDateTime="2002-01-01 01:02",
            ),
        ),
        # case 3 : 存在しないcompany_id
        (
            InvoicesFilter(
                page=1,
                size=10,
                sort=Sort.INVOICE_ID,
                sort_order=SortOrder.ASC,
            ),
            999,
            [999],
            InvoicesListBaseItem(
                page=1,
                pages=0,
                size=10,
                total=0,
                items=[],
                lastReceiveDateTime="",
            ),
        ),
    ]


def test_get_invoices_list_exception() -> list:
    """get_invoices_list例外テストパラメータ"""
    return []


def test_get_invoice() -> list[tuple[int, InvoiceBaseItem]]:
    """get_invoiceテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    invoice_receive_record = InvoiceReceiveRecordFactory.build(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory.build(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.commit()

    return [
        # case 1 : invoice_idに合致している請求書が存在
        (
            invoice.id,
            InvoiceBaseItem(
                isConfirmation=invoice.isConfirmation,
                isDownload=invoice.isDownload,
                currencyCode=invoice.IBT005,
                inv_no=invoice.inv_no,
                invoice_title=invoice.invoice_title,
                list_info=invoice.list_info,
                pay_due_date=(
                    invoice.pay_due_date.strftime(const.DATE_FORMAT)
                    if invoice.pay_due_date is not None
                    else None
                ),
                inv_amount=invoice.inv_amount,
                payment_method=invoice.payment_method,
                publisher=invoice.publisher,
                banks=invoice.banks,
                data_type=invoice.data_type,
                customer=invoice.customer,
                seller_attached_file=invoice.seller_attached_file,
                remarks=invoice.remarks,
                inv_without_tax=invoice.inv_without_tax,
                inv_tax=invoice.inv_tax,
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
                paid_info=invoice.paid_info,
                refund_info=invoice.refund_info,
                additional_info=invoice.additional_info,
                details=invoice.details,
                IBG04=invoice.IBG04,
                IBG07=invoice.IBG07,
            ),
        )
    ]


def test_get_invoice_exception() -> list[tuple[int, dict]]:
    """get_invoice例外テストパラメータ"""
    return [
        # case 1 : invoice_idに合致している請求書が存在しない
        (
            999,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_get_peppol_detail() -> list[tuple[int, BaseItem]]:
    """get_peppol_detailテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal

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
        # case 1 : invoice_idに合致している請求書が存在
        (
            invoice.id,
            BaseItem(
                IBT003=invoice.IBT003,
                IBT001=invoice.IBT001,
                IBT002=invoice.IBT002.strftime(const.DATE_FORMAT),
                IBT009=(
                    invoice.IBT009.strftime(const.DATE_FORMAT)
                    if invoice.IBT009 is not None
                    else None
                ),
                IBT022=invoice.IBT022,
                IBT168=(
                    invoice.IBT168.strftime(const.TIME_FORMAT)
                    if invoice.IBT168 is not None
                    else None
                ),
                IBT005=invoice.IBT005,
                IBT006=invoice.IBT006,
                IBT007=(
                    invoice.IBT007.strftime(const.DATE_FORMAT)
                    if invoice.IBT007 is not None
                    else None
                ),
                IBT010=invoice.IBT010,
                IBG14=invoice.IBG14,
                AUTO12=invoice.AUTO12,
                AUTO7=invoice.AUTO7,
                AUTO2=invoice.AUTO2,
                AUTO5=invoice.AUTO5,
                AUTO4=invoice.AUTO4,
                AUTO6=invoice.AUTO6,
                AUTO8=invoice.AUTO8,
                IBT019=invoice.IBT019,
                IBT024=invoice.IBT024,
                IBT023=invoice.IBT023,
                IBG33=invoice.IBG33,
                IBG03=invoice.IBG03,
                IBG24=invoice.IBG24,
                IBG04=invoice.IBG04,
                IBG07=invoice.IBG07,
                IBG10=invoice.IBG10,
                IBG11=invoice.IBG11,
                IBG13=invoice.IBG13,
                IBG16=invoice.IBG16,
                IBG35=invoice.IBG35,
                IBG20=invoice.IBG20,
                IBG21=invoice.IBG21,
                IBG22=invoice.IBG22,
                AUTO64=invoice.AUTO64,
                IBG37=invoice.IBG37,
                invoiceLineInPeppolDetail=[
                    invoiceLineInPeppolDetailItem(
                        id=invoice_detail.invoiceId,
                        IBT126=invoice_detail.IBT126,
                        IBG31=invoice_detail.IBG31,
                        IBG29=invoice_detail.IBG29,
                        IBT131=invoice_detail.IBT131,
                        IBG26=invoice_detail.IBG26,
                        IBG36=invoice_detail.IBG36,
                    )
                ],
            ),
        )
    ]


def test_get_peppol_detail_exception() -> list[tuple[int, dict]]:
    """get_peppol_detail例外テストパラメータ"""
    return [
        # case 1 : invoice_idに合致している請求書が存在しない
        (
            999,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_insert_invoice_receive_record() -> (
    list[tuple[int, str, str, str, ReceiveRecordStatus, str, str, int]]
):
    """insert_invoice_receive_recordテストパラメータ"""
    return [
        # case 1 : 請求書受取履歴テーブルに正常に登録
        (
            1,
            "unittestApiId",
            "unittestPassword",
            "unittestAuthKey",
            ReceiveRecordStatus.RECEIVE_OK,
            "202405271234",
            "202405271256",
            1,
        )
    ]


def test_update_download_status() -> list[tuple[int, IsDownload, None]]:
    """update_download_statusテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 正常にダウンロードステータスが更新
        (invoice.id, IsDownload.DOWNLOADED, None)
    ]


def test_update_download_status_exception() -> list[tuple[int, IsDownload, dict]]:
    """update_download_status例外テストパラメータ"""
    return [
        # case 1 : invoice_idに合致している請求書が存在しない
        (
            999,
            IsDownload.DOWNLOADED,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_update_confirmation_status() -> list[tuple[int, IsConfirmation, None]]:
    """update_confirmation_statusテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 正常に確認ステータスが更新
        (invoice.id, IsConfirmation.CONFIRMED, None)
    ]


def test_update_confirmation_status_exception() -> (
    list[tuple[int, IsConfirmation, dict]]
):
    """update_confirmation_status例外テストパラメータ"""
    return [
        # case 1 : invoice_idに合致している請求書が存在しない
        (
            999,
            IsConfirmation.CONFIRMED,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_update_open_status() -> list[tuple[int, IsOpen, None]]:
    """update_open_statusテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal

    invoice_receive_record = InvoiceReceiveRecordFactory(
        companyInfosId=1, status=ReceiveRecordStatus.INSERT_OK
    )
    session.add(invoice_receive_record)
    session.flush()
    invoice = InvoiceFactory(invoiceReceiveRecordsId=invoice_receive_record.id)
    session.add(invoice)
    session.commit()

    return [
        # case 1 : 正常に開封ステータスが更新
        (invoice.id, IsOpen.OPENED, None)
    ]


def test_update_open_status_exception() -> list[tuple[int, IsOpen, dict]]:
    """update_open_status例外テストパラメータ"""
    return [
        # case 1 : invoice_idに合致している請求書が存在しない
        (
            999,
            IsOpen.OPENED,
            {
                "exception": PeppolHttpException,
                "message": messages.INVOICE_DATA_NOT_FOUND_MESSAGE.message,
            },
        ),
    ]


def test_update_invoice_receive_record() -> list[tuple[int, ReceiveRecordStatus, None]]:
    """update_invoice_receive_record例外テストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal
    invoice_receive_record1 = InvoiceReceiveRecordFactory(
        id=1, status=ReceiveRecordStatus.INSERT_OK, deletedAt=None
    )
    session.add(invoice_receive_record1)
    session.flush()
    invoice_receive_record2 = InvoiceReceiveRecordFactory(
        id=2, status=ReceiveRecordStatus.INSERT_OK, deletedAt=pendulum.now()
    )
    session.add(invoice_receive_record2)
    session.commit()

    return [
        # case 1 : 存在しているデータに意図通り更新されていることを確認
        (1, ReceiveRecordStatus.RECEIVE_OK, None),
        # case 2 : 存在するが削除されたデータは意図通り更新されないことを確認
        (2, ReceiveRecordStatus.RECEIVE_OK, None),
        # case 3 : 存在しないデータは意図通り更新されないことを確認
        (999, ReceiveRecordStatus.RECEIVE_OK, None),
    ]


def test_raise_receive_exception() -> list[tuple[int, str, str, str, str, str, dict]]:
    """raise_receive_exception例外テストパラメータ"""
    return [
        # case 1 : 受取処理失敗時の例外
        (
            1,
            "unittestApiId",
            "unittestPassword",
            "unittestAuthKey",
            "202405271234",
            "202405271256",
            {
                "exception": PeppolHttpException,
                "message": messages.ZIP_RECEIVE_FAILED_MESSAGE.message,
            },
        ),
    ]


def test_fetch_invoices_zip() -> (
    list[tuple[User, dict[str, str], str, str, requests.Response]]
):
    """fetch_invoices_zipテストパラメータ"""
    receive_response = requests.Response()
    receive_response.status_code = status.HTTP_204_NO_CONTENT  # type: ignore
    return [
        # case 1 : 正常に受取処理
        (
            User(companyInfosId=1),
            {
                "apiId": "apiId",
                "password": "password",
                "authKey": "authKey",
            },
            "202405271234",
            "202405271256",
            receive_response,
        )
    ]


def test_apply_fetch_invoice_receive_state() -> (
    list[tuple[requests.Response, User, dict[str, str], str, str, dict]]
):
    """apply_fetch_invoice_receive_stateテストパラメータ"""
    receive_response = requests.Response()
    receive_response.status_code = status.HTTP_204_NO_CONTENT  # type: ignore
    receive_response2 = requests.Response()
    receive_response2.status_code = status.HTTP_200_OK  # type: ignore

    user = User(companyInfosId=1)

    return [
        # case 1 :204のレスポンスの場合
        (
            receive_response,
            user,
            {
                "peppolId": "peppol_id",
                "apiId": "peppol_api_id",
                "password": "peppol_password",
                "authKey": "peppol_auth_key",
            },
            "200101010101",
            "200401010101",
            {
                "company_infos_id": user.companyInfosId,
                "api_id": "peppol_api_id",
                "password": "peppol_password",
                "auth_key": "peppol_auth_key",
                "status": ReceiveRecordStatus.INSERT_OK,
                "get_time_from": "200101010101",
                "get_time_to": "200401010101",
            },
        ),
        # case 2 :200のレスポンスの場合
        (
            receive_response2,
            user,
            {
                "peppolId": "peppol_id",
                "apiId": "peppol_api_id",
                "password": "peppol_password",
                "authKey": "peppol_auth_key",
            },
            "200101010101",
            "200401010101",
            {
                "company_infos_id": user.companyInfosId,
                "api_id": "peppol_api_id",
                "password": "peppol_password",
                "auth_key": "peppol_auth_key",
                "status": ReceiveRecordStatus.RECEIVE_OK,
                "get_time_from": "200101010101",
                "get_time_to": "200401010101",
            },
        ),
    ]


def test_apply_fetch_invoice_receive_exception() -> list:
    """apply_fetch_invoice_receive_exception例外テストパラメータ"""
    return []
