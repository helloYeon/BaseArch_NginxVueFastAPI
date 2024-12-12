"""tests/api/test_PP008.py"""

import json

import helpers
import pytest
import test_PP008_params
from core.constant import const
from db.factories import (
    CompanyInfoFactory,
    InvoiceFactory,
)
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture
from services.company_service import CompanyService
from services.http_access_point_service import HttpAccessPointService
from services.http_authenticate_service import HttpAuthenticateService
from services.invoice_service import InvoiceService
from services.receive_service import ReceiveService
from services.s3_service import S3Service
from services.user_service import UserService
from sqlalchemy import text
from sqlalchemy.orm.session import Session


@pytest.mark.parametrize(
    """
    mock_get_company_info,
    mock_access_get_response,
    expected_response,
    expected_count
    """,
    test_PP008_params.test_PP008(),
)
def test_PP008(
    mock_get_company_info,
    mock_access_get_response,
    expected_response,
    expected_count,
    mocker: MockerFixture,
    client: TestClient,
    override_get_db: Session,
) -> None:
    """PP008APIテスト"""
    m_object = mocker.patch.object

    m_object(CompanyService, "get_company_info").return_value = mock_get_company_info

    m_object(InvoiceService, "fetch_invoices_zip").return_value = (
        mock_access_get_response
    )

    m_object(S3Service, "upload_file_s3").return_value = const.PROC_RESULT_SUCCESS

    m_object(ReceiveService, "fetch_peppol_id_info").return_value = {
        "peppolId": "0001:test0000000001",
        "apiId": "apiId1",
        "password": "pw001",
        "authKey": "authKey1",
    }

    # JSONファイルのパスを取得
    json_file_path = helpers.get_storage_path("for_test/base_json_data_1.json")

    # JSONファイルを読み込んで辞書に変換
    with open(json_file_path, "r") as file:
        json_data = json.load(file)

    m_object(ReceiveService, "xml_data_transform_request").return_value = {
        "b2b_format_datas": json_data
    }

    # APIの呼び出しと結果の検証
    result = client.post("api/v1/invoices/receives")

    # 処理後正規化されたデータ件数を確認
    invoice_cnt = override_get_db.execute(
        text("SELECT count(1) AS cnt FROM invoices")
    ).fetchone()

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected_response
    assert invoice_cnt is not None and invoice_cnt[0] == expected_count


@pytest.mark.parametrize(
    """
    mock_get_company_info,
    mock_access_get_response,
    expected_response,
    expected_count
    """,
    test_PP008_params.test_PP008_duplicated(),
)
def test_PP008_duplicated(
    mock_get_company_info,
    mock_access_get_response,
    expected_response,
    expected_count,
    mocker: MockerFixture,
    client: TestClient,
    override_get_db: Session,
) -> None:
    """PP008APIテスト"""
    session = override_get_db

    # 重複ファイルテストのため、一部ファイル事前登録
    for filename in [
        "standard_invoices_1.xml",
        "standard_invoices_2.xml",
        "standard_invoices_3.xml",
        "standard_invoices_4.xml",
    ]:
        session.add(InvoiceFactory(originXmlFileName=filename))
        session.commit()

    m_object = mocker.patch.object

    m_object(CompanyService, "get_company_info").return_value = mock_get_company_info

    m_object(InvoiceService, "fetch_invoices_zip").return_value = (
        mock_access_get_response
    )

    m_object(S3Service, "upload_file_s3").return_value = const.PROC_RESULT_SUCCESS

    m_object(ReceiveService, "fetch_peppol_id_info").return_value = {
        "peppolId": "0001:test0000000001",
        "apiId": "apiId1",
        "password": "pw001",
        "authKey": "authKey1",
    }

    # JSONファイルのパスを取得
    json_file_path = helpers.get_storage_path("for_test/base_json_data_1.json")

    # JSONファイルを読み込んで辞書に変換
    with open(json_file_path, "r") as file:
        json_data = json.load(file)

    m_object(ReceiveService, "xml_data_transform_request").return_value = {
        "b2b_format_datas": json_data
    }

    # APIの呼び出しと結果の検証
    result = client.post("api/v1/invoices/receives")

    # 処理後正規化されたデータ件数を確認
    invoice_cnt = override_get_db.execute(
        text("SELECT count(1) AS cnt FROM invoices")
    ).fetchone()

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected_response
    assert invoice_cnt is not None and invoice_cnt[0] == expected_count


@pytest.mark.parametrize(
    """
    mock_get_company_info,
    mock_get_user_last_record_date,
    mock_auth_get_response,
    mock_access_get_response,
    mock_insert_invoice_receive_record,
    mock_upload_file_s3,
    mock_update_invoice_receive_record,
    mock_zip_data_shaping,
    expected,
    expected_status_code
    """,
    test_PP008_params.test_PP008_exception(),
)
def test_PP008_exception(
    mock_get_company_info,
    mock_get_user_last_record_date,
    mock_auth_get_response,
    mock_access_get_response,
    mock_insert_invoice_receive_record,
    mock_upload_file_s3,
    mock_update_invoice_receive_record,
    mock_zip_data_shaping,
    expected,
    expected_status_code,
    mocker: MockerFixture,
    client: TestClient,
) -> None:
    """PP008API例外テスト"""
    mocker.patch.object(CompanyService, "get_company_info").side_effect = (
        mock_get_company_info
    )

    mocker.patch.object(UserService, "get_user_last_record_date").side_effect = (
        mock_get_user_last_record_date
    )
    mocker.patch.object(HttpAuthenticateService, "send").return_value = (
        HttpAuthenticateService
    )
    mocker.patch.object(
        HttpAuthenticateService, "get_response"
    ).return_value.json.side_effect = mock_auth_get_response
    mocker.patch.object(HttpAccessPointService, "send").return_value = (
        HttpAccessPointService
    )
    mocker.patch.object(HttpAccessPointService, "get_response").side_effect = (
        mock_access_get_response
    )
    mocker.patch.object(InvoiceService, "insert_invoice_receive_record").side_effect = (
        mock_insert_invoice_receive_record
    )
    mocker.patch.object(S3Service, "upload_file_s3").side_effect = mock_upload_file_s3
    mocker.patch.object(InvoiceService, "update_invoice_receive_record").side_effect = (
        mock_update_invoice_receive_record
    )
    mocker.patch.object(ReceiveService, "zip_data_shaping").side_effect = (
        mock_zip_data_shaping
    )

    # APIの呼び出しと結果の検証
    result = client.post("api/v1/invoices/receives")

    assert result.status_code == expected_status_code
    assert result.json() == expected
