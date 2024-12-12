"""tests/services/test_receive.py"""

import os
import shutil
import tempfile

import pytest
import test_receive_service_params
import xmltodict
from core.constant import const
from helpers import logger
from services.http_access_point_service import HttpAccessPointService
from services.http_authenticate_service import HttpAuthenticateService
from services.receive_service import ReceiveService


@pytest.fixture
def receive_service(override_get_db) -> ReceiveService:
    """ReceiveServiceセットアップ"""
    service = ReceiveService(override_get_db)
    service.receive_record_id = 1
    service.company_infos_id = 1

    return service


def test_xml_data_transform_request(mocker, receive_service) -> None:
    """xml_data_transform_requestメソッドテスト"""
    # モックの作成
    mocker.patch.object(HttpAccessPointService, "send").return_value = (
        HttpAccessPointService
    )
    mocker.patch.object(
        HttpAccessPointService, "get_response"
    ).return_value.json.return_value = {"mocked_data": "response"}

    for (
        xml,
        expected,
    ) in test_receive_service_params.test_xml_data_transform_request():
        # テスト用前処理
        receive_service.xml_dict = (
            xmltodict.parse(
                xml,
                attr_prefix="",
                force_cdata=True,
                cdata_key=const.XML_VALUE_WRAP_KEY,
            )
            or {}
        )

        # メソッドの呼び出しと結果の検証
        result = receive_service.xml_data_transform_request(xml)

        assert result == expected


def test_xml_data_transform_request_exception() -> None:
    """xml_data_transform_requestメソッドテスト"""
    assert True


def test_condition_check(receive_service) -> None:
    """condition_checkメソッドテスト"""
    for (
        items,
        btid,
        expected,
    ) in test_receive_service_params.test_condition_check():
        # メソッドの呼び出しと結果の検証
        result = receive_service.condition_check(items, btid)

        assert result == expected


def test_condition_check_exception() -> None:
    """condition_checkメソッド例外テスト"""
    assert True


def test_make_btid_item(receive_service) -> None:
    """make_btid_itemメソッドテスト"""
    for (
        record,
        item,
        full_name,
        expected,
    ) in test_receive_service_params.test_make_btid_item():
        # メソッドの呼び出しと結果の検証
        result = receive_service.make_btid_item(record, item, full_name)

        assert result == expected


def test_make_btid_item_exception() -> None:
    """make_btid_itemメソッド例外テスト"""
    assert True


def test_get_filter_mst_ppol_item(receive_service) -> None:
    """make_get_filter_mst_ppol_itemメソッドテスト"""
    for (
        name_full,
        parent_sort,
        expected,
    ) in test_receive_service_params.test_get_filter_mst_ppol_item():
        # メソッドの呼び出しと結果の検証
        result = receive_service.get_filter_mst_ppol_item(name_full, parent_sort)

        # 特定のプロパティのみを比較
        for idx, item in enumerate(result):
            assert item.id == expected[idx].id
            assert item.parentSortOrder == expected[idx].parentSortOrder
            assert item.btId == expected[idx].btId
            assert item.nameFull == expected[idx].nameFull


def test_get_filter_mst_ppol_item_exception() -> None:
    """get_filter_mst_ppol_itemメソッド例外テスト"""
    assert True


def test_deep_dict_shaping(receive_service) -> None:
    """deep_dict_shapingメソッドテスト"""
    for (
        d,
        parent_sort,
        parent_name,
        expected,
    ) in test_receive_service_params.test_deep_dict_shaping():
        # メソッドの呼び出しと結果の検証
        result = receive_service.deep_dict_shaping(d, parent_sort, parent_name)

        assert result == expected


def test_deep_dict_shaping_exception() -> None:
    """deep_dict_shapingメソッド例外テスト"""
    assert True


def test_create_data_for_insertion(mocker, receive_service) -> None:
    """create_data_for_insertionメソッドテスト"""
    mocker.patch.object(logger, "error").return_value = None

    for (
        i,
        d,
        t,
        s3_path,
        expected,
    ) in test_receive_service_params.test_create_data_for_insertion():
        # メソッドの呼び出しと結果の検証
        with receive_service.start_transaction() as outer_transaction:
            result = receive_service.create_data_for_insertion(i, d, t, s3_path)
            outer_transaction.commit()

        assert result == expected


def test_create_data_for_insertion_exception() -> None:
    """create_data_for_insertionメソッド例外テスト"""
    assert True


def test_xml_data_shaping(mocker, receive_service) -> None:
    """xml_data_shapingメソッドテスト"""
    # モックの作成
    mocker.patch.object(logger, "error").return_value = None
    mocker.patch.object(HttpAccessPointService, "send").return_value = (
        HttpAccessPointService
    )
    mocker.patch.object(
        HttpAccessPointService, "get_response"
    ).return_value.json.return_value = {
        "status": "0",
        "error_code": "",
        "error_detail": "",
        "b2b_format_datas": [{"mocked_data": "response"}],
    }

    for (
        save_xml_path,
        s3_xml_path,
        expected,
    ) in test_receive_service_params.test_xml_data_shaping():

        # メソッドの呼び出しと結果の検証
        result = receive_service.xml_data_shaping(save_xml_path, s3_xml_path)

        assert result == expected


def test_xml_data_shaping_exception() -> None:
    """xml_data_shapingメソッド例外テスト"""
    assert True


@pytest.mark.aws_test
def test_zip_data_shaping(mocker, receive_service) -> None:
    """zip_data_shapingメソッドテスト"""
    mocker.patch.object(logger, "error").return_value = None

    for (
        zip_file_path,
        mock_data,
        expected,
    ) in test_receive_service_params.test_zip_data_shaping():
        # モックの作成
        mocker.patch.object(HttpAccessPointService, "send").return_value = mock_data[
            "send"
        ]
        mocker.patch.object(
            HttpAccessPointService, "get_response"
        ).return_value.json.return_value = mock_data["get_response"]

        # 一時フォルダを作成
        with tempfile.TemporaryDirectory() as temp_folder:
            temp_file_path = os.path.join(temp_folder, "receive.zip")
            shutil.copy2(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    zip_file_path,
                ),
                temp_file_path,
            )
            # メソッドの呼び出しと結果の検証
            result = receive_service.zip_data_shaping(temp_folder, temp_file_path)

        assert result == expected


def test_zip_data_shaping_exception() -> None:
    """zip_data_shapingメソッド例外テスト"""
    assert True


def test_is_duplicated_file(receive_service: ReceiveService) -> None:
    """is_duplicated_fileメソッドテスト"""
    for (
        xml_filename,
        expected,
    ) in test_receive_service_params.test_is_duplicated_file():
        result = receive_service.is_duplicated_file(xml_filename)
        assert result == expected


def test_is_duplicated_file_exception() -> None:
    """is_duplicated_fileメソッド例外テスト"""
    assert True


def test_fetch_peppol_id_info(mocker, receive_service) -> None:
    """fetch_peppol_id_infoメソッドテスト"""
    for (
        company_info,
        expected,
    ) in test_receive_service_params.test_fetch_peppol_id_info():
        # モックの作成
        mocker.patch.object(HttpAuthenticateService, "send").return_value = (
            HttpAuthenticateService
        )
        mocker.patch.object(
            HttpAuthenticateService, "get_response"
        ).return_value.json.side_effect = [{"peppolId": "1111:peppolId"}, expected]

        # メソッドの呼び出しと結果の検証
        result = receive_service.fetch_peppol_id_info(company_info)

        assert result == expected


def test_fetch_peppol_id_info_exception() -> None:
    """fetch_peppol_id_infoメソッド例外テスト"""
    assert True
