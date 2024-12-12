"""tests/api/test_PP005.py"""

import pytest
import test_PP005_params
from api.v1.schemas.invoices.downloads.csv import CsvQueryParam, PpolItem
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.csv_service import CsvService
from services.user_service import UserService


@pytest.mark.parametrize(
    """
    csv_param,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_user_ppol_setting,
    mock_get_invoices_id_list,
    mock_make_csv_title,
    mock_make_csv_row_for_common,
    mock_make_csv_row_for_invoice,
    mock_make_csv_rows_for_detail,
    expected
    """,
    test_PP005_params.test_PP005,
)
def test_PP005(
    csv_param: CsvQueryParam,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_get_user_ppol_setting: tuple[list[PpolItem], list[PpolItem], list[PpolItem]],
    mock_get_invoices_id_list: list[int],
    mock_make_csv_title: list[str],
    mock_make_csv_row_for_common: list[str],
    mock_make_csv_row_for_invoice: list[str],
    mock_make_csv_rows_for_detail: list[list[str]],
    expected,
    mocker,
    client,
) -> None:
    """PP005APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(UserService, "get_user_ppol_setting").return_value = (
        mock_get_user_ppol_setting
    )
    mocker.patch.object(CsvService, "get_invoices_id_list").return_value = (
        mock_get_invoices_id_list
    )
    mocker.patch.object(CsvService, "make_csv_title").side_effect = mock_make_csv_title
    mocker.patch.object(CsvService, "make_csv_row_for_common").return_value = (
        mock_make_csv_row_for_common
    )
    mocker.patch.object(CsvService, "make_csv_row_for_invoice").return_value = (
        mock_make_csv_row_for_invoice
    )
    mocker.patch.object(CsvService, "make_csv_rows_for_detail").return_value = (
        mock_make_csv_rows_for_detail
    )

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/invoices/downloads/csvs",
        params=csv_param.model_dump(exclude_unset=True),
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.content.decode("CP932") == expected


@pytest.mark.parametrize(
    """
    csv_param,mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_user_ppol_setting,
    mock_get_invoices_id_list,
    mock_make_csv_title,
    mock_make_csv_row_for_common,
    mock_make_csv_row_for_invoice,
    mock_make_csv_rows_for_detail,
    expected,
    expected_status_code
    """,
    test_PP005_params.test_PP005_exception,
)
def test_PP005_exception(
    csv_param,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_user_ppol_setting,
    mock_get_invoices_id_list,
    mock_make_csv_title,
    mock_make_csv_row_for_common,
    mock_make_csv_row_for_invoice,
    mock_make_csv_rows_for_detail,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP005API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(UserService, "get_user_ppol_setting").side_effect = [
        mock_get_user_ppol_setting
    ]
    mocker.patch.object(CsvService, "get_invoices_id_list").side_effect = [
        mock_get_invoices_id_list
    ]
    mocker.patch.object(CsvService, "make_csv_title").side_effect = mock_make_csv_title
    mocker.patch.object(CsvService, "make_csv_row_for_common").side_effect = [
        mock_make_csv_row_for_common
    ]
    mocker.patch.object(CsvService, "make_csv_row_for_invoice").side_effect = [
        mock_make_csv_row_for_invoice
    ]
    mocker.patch.object(CsvService, "make_csv_rows_for_detail").side_effect = [
        mock_make_csv_rows_for_detail
    ]

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/invoices/downloads/csvs",
        params=csv_param,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
