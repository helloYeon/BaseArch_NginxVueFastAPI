"""tests/test_output_service.py"""

import pytest
import test_output_service_params
from enums import MstIsExistData, MstType
from models import MstPpolItem
from services.output_service import OutputService


@pytest.fixture
def output_service(override_get_db) -> OutputService:
    """OutputServiceのインスタンスを返す"""
    service = OutputService(override_get_db)

    return service


def test_get_user_setting(mocker, output_service: OutputService) -> None:
    """get_user_settingテスト"""
    # モックの作成
    # mst_ppol_itemsの値の量が多いため、モックで代用
    mocker.patch.object(output_service.mst_ppol_item_repo, "get_all").return_value = [
        MstPpolItem(
            id=1,
            parentSortOrder=0,
            btId="IBT-024",
            nameEn="CustomizationID",
            nameJp="ビジネスプロセスタイプ",
            nameFull="cbc:CustomizationID",
            condition="",
            sortOrder=1,
            isExistData=MstIsExistData.EXIST,
            type=MstType.INVOICES,
            model=1,
        ),
        MstPpolItem(
            id=2,
            parentSortOrder=0,
            btId="IBT-023",
            nameEn="ProfileID",
            nameJp="仕様ID",
            nameFull="cbc:ProfileID",
            condition="",
            sortOrder=2,
            isExistData=MstIsExistData.EXIST,
            type=MstType.INVOICES,
            model=1,
        ),
        MstPpolItem(
            id=3,
            parentSortOrder=0,
            btId="IBT-001",
            nameEn="ID",
            nameJp="請求書番号",
            nameFull="cbc:ID",
            condition="",
            sortOrder=3,
            isExistData=MstIsExistData.EXIST,
            type=MstType.INVOICES,
            model=1,
        ),
    ]

    for user_id, expected in test_output_service_params.test_get_user_setting():
        result = output_service.get_user_setting(user_id)

        assert result == expected


def test_get_user_setting_exception(mocker, output_service: OutputService) -> None:
    """get_user_setting例外テスト"""
    # モックの作成
    mocker.patch.object(output_service.mst_ppol_item_repo, "get_all").return_value = []

    for (
        user_id,
        expected,
    ) in test_output_service_params.test_get_user_setting_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            output_service.get_user_setting(user_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_put_user_setting(output_service: OutputService) -> None:
    """put_user_settingテスト"""
    for (
        request_body,
        user_id,
        expected,
    ) in test_output_service_params.test_put_user_setting():
        result = output_service.put_user_setting(request_body, user_id)

        assert result == expected


def test_put_user_setting_exception(mocker, output_service: OutputService) -> None:
    """put_user_setting例外テスト"""
    # モックの作成
    mocker.patch.object(
        output_service.user_ppol_item_repo, "delete_by_user_id"
    ).side_effect = Exception

    for (
        request_body,
        user_id,
        expected,
    ) in test_output_service_params.test_put_user_setting_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            output_service.put_user_setting(request_body, user_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_check_user_setting_payment_code(mocker, output_service: OutputService) -> None:
    """check_user_setting_payment_codeテスト"""
    # モックの作成
    mocker.patch.object(output_service.mst_ppol_item_repo, "get_count").return_value = 1
    mocker.patch.object(
        output_service.user_ppol_item_repo, "get_count"
    ).return_value = 1

    for (
        user_id,
        expected,
    ) in test_output_service_params.test_check_user_setting_payment_code():
        result = output_service.check_user_setting_payment_code(user_id)

        assert result == expected


def test_check_user_setting_payment_code_exception(
    mocker, output_service: OutputService
) -> None:
    """check_user_setting_payment_code例外テスト"""
    # モックの作成
    mocker.patch.object(output_service.mst_ppol_item_repo, "get_count").return_value = 0

    for (
        user_id,
        expected,
    ) in test_output_service_params.test_check_user_setting_payment_code_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            output_service.check_user_setting_payment_code(user_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
