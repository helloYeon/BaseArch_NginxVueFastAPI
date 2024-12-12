"""tests/api/test_PP001.py"""

from typing import Any

import pytest
import test_PP001_params
from api.v1.schemas.invoice import (
    InvoicesFilter,
    InvoicesListBaseItem,
)
from fastapi import status
from models import CompanyInfo
from services.company_service import CompanyService
from services.invoice_service import InvoiceService


@pytest.mark.skip(
    reason="臨時対応したため、Skip / PEPPOL_RECEIVE-314 外貨での小数点以下の表示(臨時対応)"
)
@pytest.mark.parametrize(
    "request_params,mock_get_company_info,mock_get_integration_company_ids,mock_get_invoices_list,expected",
    test_PP001_params.test_PP001,
)
def test_PP001(
    request_params: InvoicesFilter,
    mock_get_company_info: CompanyInfo,
    mock_get_integration_company_ids: list[int],
    mock_get_invoices_list: InvoicesListBaseItem,
    expected: dict[str, Any],
    mocker,
    client,
) -> None:
    """PP001APIテスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").return_value = (
        mock_get_company_info
    )
    mocker.patch.object(CompanyService, "get_integration_company_ids").return_value = (
        mock_get_integration_company_ids
    )
    mocker.patch.object(InvoiceService, "get_invoices_list").return_value = (
        mock_get_invoices_list
    )

    # APIの呼び出しと結果の検証
    result = client.get(
        "api/v1/invoices", params=request_params.model_dump(exclude_unset=True)
    )

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


@pytest.mark.parametrize(
    """
    request_params,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_invoices_list,
    expected,
    expected_status_code
    """,
    test_PP001_params.test_PP001_exception,
)
def test_PP001_exception(
    request_params,
    mock_get_company_info,
    mock_get_integration_company_ids,
    mock_get_invoices_list,
    expected,
    expected_status_code,
    mocker,
    client,
) -> None:
    """PP001API例外テスト"""
    # モックの作成
    mocker.patch.object(CompanyService, "get_company_info").side_effect = [
        mock_get_company_info
    ]
    mocker.patch.object(CompanyService, "get_integration_company_ids").side_effect = [
        mock_get_integration_company_ids
    ]
    mocker.patch.object(InvoiceService, "get_invoices_list").side_effect = [
        mock_get_invoices_list
    ]

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/invoices", params=request_params)

    assert result.status_code == expected_status_code
    assert result.json() == expected
