"""tests/services/test_invoice_service.py"""

import pytest
import test_invoice_service_params
from services.http_access_point_service import HttpAccessPointService
from services.http_external_service import HttpExternalService
from services.invoice_service import InvoiceService


@pytest.fixture
def invoice_service(override_get_db) -> InvoiceService:
    """InvoiceServiceのインスタンスを返す"""
    service = InvoiceService(override_get_db)

    return service


def test_get_invoices_list(
    invoice_service: InvoiceService,
) -> None:
    """get_invoices_listテスト"""
    for (
        invoices_filter,
        company_infos_id,
        company_ids,
        expected,
    ) in test_invoice_service_params.test_get_invoices_list():
        result = invoice_service.get_invoices_list(
            invoices_filter, company_infos_id, company_ids
        )

        assert result == expected


def test_get_invoices_list_exception() -> None:
    """get_invoices_list例外テスト"""
    assert True


def test_get_invoice(
    invoice_service: InvoiceService,
) -> None:
    """get_invoiceテスト"""
    for (
        invoice_id,
        expected,
    ) in test_invoice_service_params.test_get_invoice():
        result = invoice_service.get_invoice(invoice_id)

        assert result == expected


def test_get_invoice_exception(invoice_service: InvoiceService) -> None:
    """get_invoice例外テスト"""
    for (
        invoice_id,
        expected,
    ) in test_invoice_service_params.test_get_invoice_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.get_invoice(invoice_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_get_peppol_detail(
    invoice_service: InvoiceService,
) -> None:
    """get_peppol_detailテスト"""
    for (
        invoice_id,
        expected,
    ) in test_invoice_service_params.test_get_peppol_detail():
        result = invoice_service.get_peppol_detail(invoice_id)

        assert result == expected


def test_get_peppol_detail_exception(
    invoice_service: InvoiceService,
) -> None:
    """get_peppol_detail例外テスト"""
    for (
        invoice_id,
        expected,
    ) in test_invoice_service_params.test_get_peppol_detail_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.get_peppol_detail(invoice_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_insert_invoice_receive_record(
    invoice_service: InvoiceService,
) -> None:
    """insert_invoice_receive_recordテスト"""
    for (
        company_infos_id,
        api_id,
        password,
        auth_key,
        status,
        get_time_from,
        get_time_to,
        expected,
    ) in test_invoice_service_params.test_insert_invoice_receive_record():
        result = invoice_service.insert_invoice_receive_record(
            company_infos_id,
            api_id,
            password,
            auth_key,
            status,
            get_time_from,
            get_time_to,
        )

        assert result == expected


def test_insert_invoice_receive_record_exception() -> None:
    """insert_invoice_receive_record例外テスト"""
    assert True


def test_update_download_status(
    invoice_service: InvoiceService,
) -> None:
    """update_download_statusテスト"""
    for (
        invoice_id,
        is_download,
        expected,
    ) in test_invoice_service_params.test_update_download_status():
        result = invoice_service.update_download_status(invoice_id, is_download)

        assert result == expected


def test_update_download_status_exception(invoice_service: InvoiceService) -> None:
    """update_download_status例外テスト"""
    for (
        invoice_id,
        is_download,
        expected,
    ) in test_invoice_service_params.test_update_download_status_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.update_download_status(invoice_id, is_download)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_update_confirmation_status(
    invoice_service: InvoiceService,
) -> None:
    """update_confirmation_statusテスト"""
    for (
        invoice_id,
        is_confirmation,
        expected,
    ) in test_invoice_service_params.test_update_confirmation_status():
        result = invoice_service.update_confirmation_status(invoice_id, is_confirmation)

        assert result == expected


def test_update_confirmation_status_exception(invoice_service: InvoiceService) -> None:
    """update_confirmation_status例外テスト"""
    for (
        invoice_id,
        is_confirmation,
        expected,
    ) in test_invoice_service_params.test_update_confirmation_status_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.update_confirmation_status(invoice_id, is_confirmation)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_update_open_status(
    invoice_service: InvoiceService,
) -> None:
    """update_open_statusテスト"""
    for (
        invoice_id,
        is_open,
        expected,
    ) in test_invoice_service_params.test_update_open_status():
        result = invoice_service.update_open_status(invoice_id, is_open)

        assert result == expected


def test_update_open_status_exception(invoice_service: InvoiceService) -> None:
    """update_open_status例外テスト"""
    for (
        invoice_id,
        is_open,
        expected,
    ) in test_invoice_service_params.test_update_open_status_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.update_open_status(invoice_id, is_open)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_update_invoice_receive_record(
    invoice_service: InvoiceService, override_get_db
) -> None:
    """update_invoice_receive_recordテスト"""
    for (
        receive_record_id,
        status,
        expected,
    ) in test_invoice_service_params.test_update_invoice_receive_record():
        result = invoice_service.update_invoice_receive_record(
            receive_record_id, status
        )

        assert result == expected


def test_update_invoice_receive_record_exception() -> None:
    """update_invoice_receive_record例外テスト"""
    assert True


def test_raise_receive_exception(mocker, invoice_service: InvoiceService) -> None:
    """raise_receive_exceptionテスト"""
    # モックの作成
    mocker.patch.object(HttpExternalService, "send").return_value = HttpExternalService
    mocker.patch.object(
        HttpExternalService, "get_response"
    ).return_value.json.return_value = "unittestErrorReason"

    for (
        company_infos_id,
        api_id,
        password,
        auth_key,
        get_time_from,
        get_time_to,
        expected,
    ) in test_invoice_service_params.test_raise_receive_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            invoice_service.raise_receive_exception(
                company_infos_id, api_id, password, auth_key, get_time_from, get_time_to
            )
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_fetch_invoices_zip(mocker, invoice_service: InvoiceService) -> None:
    """fetch_invoices_zipテスト"""
    for (
        user_info,
        peppol_id_info,
        last_get_date,
        now,
        expected,
    ) in test_invoice_service_params.test_fetch_invoices_zip():
        # モックの作成
        mocker.patch.object(HttpAccessPointService, "send").return_value = (
            HttpAccessPointService
        )
        mocker.patch.object(HttpExternalService, "get_response").return_value = expected

        # メソッドの呼び出しと結果の検証
        result = invoice_service.fetch_invoices_zip(
            user_info,
            peppol_id_info,
            last_get_date,
            now,
        )

        assert result == expected


def test_fetch_invoices_zip_exception() -> None:
    """fetch_invoices_zip例外テスト"""
    assert True


def test_apply_fetch_invoice_receive_state(
    mocker,
    invoice_service: InvoiceService,
) -> None:
    """apply_fetch_invoice_receive_stateテスト"""
    for (
        receive_response,
        user_info,
        peppol_id_info,
        last_get_date,
        now,
        expected,
    ) in test_invoice_service_params.test_apply_fetch_invoice_receive_state():
        mocker.patch.object(
            invoice_service, "insert_invoice_receive_record"
        ).return_value = 1

        result = invoice_service.apply_fetch_invoice_receive_state(
            receive_response, user_info, peppol_id_info, last_get_date, now
        )

        # insert_invoice_receive_recordメソッドが指定された引数で呼ばれることを確認
        invoice_service.insert_invoice_receive_record.assert_called_once_with(
            expected["company_infos_id"],
            expected["api_id"],
            expected["password"],
            expected["auth_key"],
            expected["status"],
            expected["get_time_from"],
            expected["get_time_to"],
        )

        assert result == 1


def test_apply_fetch_invoice_receive_state_exception() -> None:
    """apply_fetch_invoice_receive_state例外テスト"""
    assert True
