"""tests/api/test_PP019.py"""

import pytest
import test_PP019_params
from api.v1.schemas.invoices.downloads.csv import CsvQueryParam
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.csv_service import CsvService
from services.output_service import OutputService


@pytest.mark.parametrize(
    """
    csv_param,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_user_setting_payment_code,
    mock_get_invoices_id_list,
    mock_check_request_invoices,
    expected
    """,
    test_PP019_params.test_PP019,
)
def test_PP019(
    csv_param: CsvQueryParam,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_check_user_setting_payment_code: bool,
    mock_get_invoices_id_list: list[int],
    mock_check_request_invoices: list[str],
    expected,
    mocker,
    client,
) -> None:
    """PP019APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(
        OutputService, "check_user_setting_payment_code"
    ).return_value = mock_check_user_setting_payment_code
    mocker.patch.object(CsvService, "get_invoices_id_list").return_value = (
        mock_get_invoices_id_list
    )
    mocker.patch.object(CsvService, "check_request_invoices").return_value = (
        mock_check_request_invoices
    )

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/invoices/downloads/csvs/checks",
        params=csv_param.model_dump(exclude_unset=True),
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    csv_param,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_user_setting_payment_code,
    mock_get_invoices_id_list,
    mock_check_request_invoices,
    expected,
    expected_status_code,
    """,
    test_PP019_params.test_PP019_exception,
)
def test_PP019_exception(
    csv_param,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_check_user_setting_payment_code,
    mock_get_invoices_id_list,
    mock_check_request_invoices,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP019API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(
        OutputService, "check_user_setting_payment_code"
    ).side_effect = [mock_check_user_setting_payment_code]
    mocker.patch.object(CsvService, "get_invoices_id_list").side_effect = [
        mock_get_invoices_id_list
    ]
    mocker.patch.object(CsvService, "check_request_invoices").side_effect = [
        mock_check_request_invoices
    ]

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/invoices/downloads/csvs/checks",
        params=csv_param,
    )

    assert result.status_code == expected_status_code
    assert result.json() == expected
