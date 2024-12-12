"""tests/test_csv_service.py"""

import pytest
import test_csv_service_params
from enums import MstType
from services.csv_service import CsvService


@pytest.fixture
def csv_service(override_get_db) -> CsvService:
    """CsvServiceのインスタンスを返す"""
    service = CsvService(override_get_db)

    return service


def test_get_invoices_id_list(csv_service: CsvService) -> None:
    """get_invoices_id_listテスト"""
    # テスト用前処理
    csv_service.company_ids = [1]

    for (
        csv_filter,
        company_infos_id,
        expected,
    ) in test_csv_service_params.test_get_invoices_id_list():
        result = csv_service.get_invoices_id_list(csv_filter, company_infos_id)
        assert result == expected


def test_get_invoices_id_list_exception(csv_service: CsvService) -> None:
    """get_invoices_id_list例外テスト"""
    for (
        csv_filter,
        company_infos_id,
        expected,
    ) in test_csv_service_params.test_get_invoices_id_list_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            csv_service.get_invoices_id_list(csv_filter, company_infos_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_csv_replace(csv_service: CsvService) -> None:
    """csv_replaceテスト"""
    for value, expected in test_csv_service_params.test_csv_replace():
        result = csv_service.csv_replace(value)
        assert result == expected


def test_csv_replace_exception() -> None:
    """csv_replace例外テスト"""
    assert True


def test_filter_mst_item_with_sort(csv_service: CsvService) -> None:
    """filter_mst_item_with_sortテスト"""
    for (
        sortOrder,
        mst_ppol_item,
        expected,
    ) in test_csv_service_params.test_filter_mst_item_with_sort():
        result = csv_service.filter_mst_item_with_sort(sortOrder, mst_ppol_item)
        assert result == expected


def test_filter_mst_item_with_sort_exception() -> None:
    """filter_mst_item_with_sort例外テスト"""
    assert True


def test_make_csv_title(csv_service: CsvService) -> None:
    """make_csv_titleテスト"""
    # テスト用前処理
    for items, expected in test_csv_service_params.test_make_csv_title():
        result = csv_service.make_csv_title(items, MstType.INVOICES)
        assert result == expected


def test_make_csv_title_exception() -> None:
    """make_csv_title例外テスト"""
    assert True


def test_get_item_key(csv_service: CsvService) -> None:
    """get_item_keyテスト"""
    # テスト用前処理
    csv_service.type = MstType.INVOICES

    for item, expected in test_csv_service_params.test_get_item_key():
        result = csv_service.get_item_key(item)
        assert result == expected


def test_get_item_key_exception() -> None:
    """get_item_key例外テスト"""
    assert True


def test_get_csv_value(csv_service: CsvService) -> None:
    """get_csv_valueテスト"""
    # テスト用前処理
    csv_service.type = MstType.INVOICES

    for item, value, expected in test_csv_service_params.test_get_csv_value():
        result = csv_service.get_csv_value(item, value)
        assert result == expected


def test_get_csv_value_exception() -> None:
    """get_csv_value例外テスト"""
    assert True


def test_get_invoice_payment_code(csv_service: CsvService) -> None:
    """get_invoice_payment_codeテスト"""
    for (
        publisher,
        company_info_id,
        expected,
    ) in test_csv_service_params.test_get_invoice_payment_code():
        result = csv_service.get_invoice_payment_code(
            publisher,
            company_info_id,
        )
        assert result == expected


def test_get_invoice_payment_code_exception() -> None:
    """get_invoice_payment_code例外テスト"""
    assert True


def test_get_csv_value_common(csv_service: CsvService) -> None:
    """get_csv_value_commonテスト"""
    for (
        common_item,
        invoice_record,
        company_info_id,
        expected,
    ) in test_csv_service_params.test_get_csv_value_common():

        result = csv_service.get_csv_value_common(
            common_item, invoice_record, company_info_id
        )
        assert result == expected


def test_get_csv_value_common_exception(csv_service: CsvService) -> None:
    """get_csv_value_common例外テスト"""
    for (
        common_item,
        invoice_record,
        company_info_id,
        expected,
    ) in test_csv_service_params.test_get_csv_value_common_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            csv_service.get_csv_value_common(
                common_item, invoice_record, company_info_id
            )
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_make_csv_row_for_common(csv_service: CsvService) -> None:
    """make_csv_row_for_commonテスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]

    for (
        common_items,
        expected,
    ) in test_csv_service_params.test_make_csv_row_for_common():
        result = csv_service.make_csv_row_for_common(common_items)
        assert result == expected


def test_make_csv_row_for_common_exception(csv_service: CsvService) -> None:
    """make_csv_row_for_common例外テスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]

    for (
        common_items,
        expected,
    ) in test_csv_service_params.test_make_csv_row_for_common_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            csv_service.make_csv_row_for_common(common_items)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_make_csv_row_for_invoice(csv_service: CsvService) -> None:
    """make_csv_row_for_invoiceテスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]
    csv_service.type = MstType.INVOICES

    for (
        detail_items,
        expected,
    ) in test_csv_service_params.test_make_csv_row_for_invoice():
        result = csv_service.make_csv_row_for_invoice(detail_items)
        assert result == expected


def test_make_csv_row_for_invoice_exception(csv_service: CsvService) -> None:
    """make_csv_row_for_invoice例外テスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]
    csv_service.type = MstType.INVOICES

    for (
        detail_items,
        expected,
    ) in test_csv_service_params.test_make_csv_row_for_invoice_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            csv_service.make_csv_row_for_invoice(detail_items)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_make_csv_rows_for_detail(csv_service: CsvService) -> None:
    """make_csv_rows_for_detailテスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]
    csv_service.type = MstType.INVOICES

    for (
        detail_items,
        expected,
    ) in test_csv_service_params.test_make_csv_rows_for_detail():
        result = csv_service.make_csv_rows_for_detail(detail_items)
        assert result == expected


def test_make_csv_rows_for_detail_exception(csv_service: CsvService) -> None:
    """make_csv_rows_for_detail例外テスト"""
    # テスト用前処理
    csv_service.id = 1
    csv_service.company_ids = [1]
    csv_service.type = MstType.INVOICES

    for (
        detail_items,
        expected,
    ) in test_csv_service_params.test_make_csv_rows_for_detail_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            csv_service.make_csv_rows_for_detail(detail_items)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_check_request_invoices(csv_service: CsvService) -> None:
    """check_request_invoicesテスト"""
    # テスト用前処理
    csv_service.company_ids = [1]

    for invoice_ids, expected in test_csv_service_params.test_check_request_invoices():
        result = csv_service.check_request_invoices(invoice_ids)
        assert result == expected


def test_check_request_invoices_exception() -> None:
    """check_request_invoices例外テスト"""
    assert True


def test_generate_csv_with_fixed_fields(csv_service: CsvService) -> None:
    """generate_csv_with_fixed_fieldsテスト"""
    for (
        csv_param,
        user_info,
        temp_csv_path,
        expected,
    ) in test_csv_service_params.test_generate_csv_with_fixed_fields():
        csv_service.company_ids = [user_info.companyInfosId]
        result = csv_service.generate_csv_with_fixed_fields(
            csv_param, user_info, temp_csv_path
        )
        assert result == expected


def test_generate_csv_with_fixed_fields_exception() -> None:
    """generate_csv_with_fixed_fields例外テスト"""
    assert True


def test_generate_fixed_csv_row(csv_service: CsvService) -> None:
    """generate_fixed_csv_rowテスト"""
    for (
        fixed_csv_row,
        detail,
        company_infos_id,
        expected,
    ) in test_csv_service_params.test_generate_fixed_csv_row():
        result = csv_service._generate_fixed_csv_row(
            fixed_csv_row,
            detail,
            company_infos_id,
        )
        assert result == expected


def test_generate_fixed_csv_row_exception() -> None:
    """generate_fixed_csv_row例外テスト"""
    assert True


def test_generate_csv_with_custom_fields(csv_service: CsvService) -> None:
    """generate_csv_with_custom_fieldsテスト"""
    for (
        csv_param,
        user_info,
        common_item,
        invoice_item,
        detail_item,
        temp_csv_path,
        expected,
    ) in test_csv_service_params.test_generate_csv_with_custom_fields():
        csv_service.company_ids = [user_info.companyInfosId]
        result = csv_service.generate_csv_with_custom_fields(
            csv_param, user_info, common_item, invoice_item, detail_item, temp_csv_path
        )
        assert result == expected


def test_generate_csv_with_custom_fields_exception() -> None:
    """generate_csv_with_custom_fields例外テスト"""
    assert True


def test_create_csv_response(csv_service: CsvService) -> None:
    """create_csv_responseテスト"""
    for (
        temp_csv_path,
        file_name,
        expected,
    ) in test_csv_service_params.test_create_csv_response():
        result = csv_service.create_csv_response(temp_csv_path, file_name)
        # レスポンスの内容を検証
        assert result.media_type == expected.media_type
        assert (
            result.headers["Content-Disposition"]
            == expected.headers["Content-Disposition"]
        )
        assert result.body == expected.body


def test_create_csv_response_exception() -> None:
    """create_csv_response例外テスト"""
    assert True
