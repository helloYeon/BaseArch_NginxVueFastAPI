"""tests/services/test_user_service.py"""

from unittest.mock import MagicMock

import exceptions
import models
import pytest
import test_user_service_params as params
from db.factories import (
    UserAccessControlFactory,
)
from enums.receive_record_status import ReceiveRecordStatus
from fastapi import status
from services.user_service import UserService
from sqlalchemy import func
from sqlalchemy.orm.session import Session


@pytest.fixture
def user_service(override_get_db) -> UserService:
    """UserServiceのインスタンスを返す"""
    service = UserService(override_get_db)

    return service


@pytest.mark.parametrize("user_id, expected, test_data", params.test_get_user())
def test_get_user(
    user_id,
    expected,
    test_data,
    user_service: UserService,
    override_get_db,
) -> None:
    """Test for user_service.get_user function."""
    # テストデータの登録
    override_get_db.add_all(test_data)
    override_get_db.commit()

    # ユーザー情報取得
    user = user_service.get_user(user_id)

    # テスト結果の検証
    if user is None:
        assert expected is None
    else:
        assert user.userId == expected.userId
        assert user.deletedAt == expected.deletedAt


def test_get_user_exception(user_service: UserService) -> None:
    """Test for user_service.get_user function to handle exceptions."""
    pass


@pytest.mark.parametrize("userId, expected, test_data", params.test_get_user_company())
def test_get_user_company(
    userId, expected, test_data, user_service: UserService, override_get_db
) -> None:
    """Test for user_service.get_user function."""
    # テストデータの登録
    override_get_db.add_all(test_data)
    override_get_db.commit()

    # 会社情報取得
    company = user_service.get_user_company(userId)

    # テスト結果の検証
    if company is None:
        assert expected is None
    else:
        assert company.esCompanyId == expected.esCompanyId
        assert company.deletedAt == expected.deletedAt


def test_get_user_company_exception(user_service: UserService) -> None:
    """Test for user_service.get_user function to handle exceptions."""
    for case in params.test_get_user_company_exception():
        user_id = case["args"]["user_id"]
        expected_exception = case["expected"]["exception"]
        expected_message = case["expected"]["message"]

        with pytest.raises(expected_exception) as exc_info:
            # 会社情報取得
            user_service.get_user_company(user_id)

        # テスト結果の検証
        assert exc_info.type == expected_exception
        assert str(exc_info.value.message) == expected_message


def test_get_user_last_record_date(user_service: UserService) -> None:
    """Test for user_service.get_user_last_record_date function."""
    for company_infos_id, expected in params.test_get_user_last_record_date():

        # 前回取得日時取得
        ret = user_service.get_user_last_record_date(
            company_infos_id, ReceiveRecordStatus.INSERT_OK
        )

        # テスト結果の検証
        assert ret == expected


def test_get_user_last_record_date_exception(user_service: UserService) -> None:
    """Test for user_service.get_user_last_record_date function to handle exceptions."""
    pass


def test_is_exist_user(user_service: UserService) -> None:
    """Test for user_service.is_exist_user function."""
    for case in params.is_exist_user():
        user_id = case["args"]["user_id"]
        expected = case["expected"]

        # テスト結果の検証
        assert user_service.is_exist_user(user_id) == expected


def test_is_exist_user_exception(user_service: UserService) -> None:
    """Test for user_service.is_exist_user function to handle exceptions."""
    pass


def test_upsert_login_info(user_service: UserService, override_get_db: Session) -> None:
    """Test for user_service.upsert_login_info function."""
    from models import CompanyInfo, User

    for data, expected in params.test_upsert_login_info():

        # テスト対象処理の実行
        result_user_info = user_service.upsert_login_info(data)

        # 処理結果の検証
        result_company_info = (
            override_get_db.query(
                User.userId, CompanyInfo.esCompanyId, CompanyInfo.name
            )
            .join(CompanyInfo, User.companyInfosId == CompanyInfo.id)
            .filter(User.deletedAt.is_(None))
            .first()
        )

        # テスト結果の検証
        assert (
            result_user_info is not None and result_company_info is not None
        ), "Result is None"

        # ユーザー情報の検証
        assert result_user_info.userId == expected.userId
        assert result_user_info.sessionId == expected.sessionId

        # 会社情報の検証
        assert result_company_info.esCompanyId == data["esCompanyId"]
        assert result_company_info.name == data["companyName"]


def test_upsert_login_info_exception(
    user_service: UserService, override_get_db: Session
) -> None:
    """Test for user_service.upsert_login_info function to handle exceptions."""
    for data, expected in params.test_upsert_login_info_exception():

        # モック対象の関数名、モック時に発生させる例外、期待されるエラーメッセージを取得
        mock_function = expected["mock_function"]
        mock_side_effect = expected["mock_side_effect"]
        expected_message = expected["expected_message"]

        # company_info_repo.upsert_by_es_company_id と user_repo.upsert_by_user_id をモック化
        user_service.company_info_repo.upsert_by_es_company_id = MagicMock(
            return_value=models.CompanyInfo()
        )
        user_service.user_repo.upsert_by_user_id = MagicMock(return_value=models.User())

        # モック対象の関数に例外を発生させるモックを設定
        components = mock_function.split(".")
        setattr(
            getattr(user_service, components[0]),
            components[1],
            MagicMock(side_effect=mock_side_effect),
        )

        # テスト対象処理の実行
        with pytest.raises(exceptions.PeppolHttpException) as exc_info:
            user_service.upsert_login_info(data)

        # テスト結果の検証値
        assert exc_info.value.message == expected_message
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert exc_info.value.extra["params"]["user_id"] == data["userId"]
        assert exc_info.value.extra["params"]["esCompanyId"] == data["esCompanyId"]

        # ロールバックの検証
        assert (
            override_get_db.query(func.count(1))
            .select_from(models.User)
            .filter(models.User.deletedAt.is_(None))
            .scalar()
        ) == 0

        assert (
            override_get_db.query(func.count(1))
            .select_from(models.CompanyInfo)
            .filter(models.CompanyInfo.deletedAt.is_(None))
            .scalar()
        ) == 0


def test_get_user_ppol_setting(mocker, user_service: UserService) -> None:
    """get_user_ppol_settingテスト"""
    for (
        mock_get_count,
        user_id,
        expected,
    ) in params.test_get_user_ppol_setting():
        # モックの作成
        # 処理の条件をモックで切り替える
        mocker.patch.object(
            user_service.mst_ppol_item_repo, "get_count"
        ).return_value = mock_get_count
        result = user_service.get_user_ppol_setting(user_id)
        (invoice_item, detail_item, common_item) = result
        (expected_invoice_item, expected_detail_item, expected_common_item) = expected

        # 配列の最初と最後を比較する
        assert invoice_item[0] == expected_invoice_item["first"]
        assert invoice_item[-1] == expected_invoice_item["last"]
        assert detail_item[0] == expected_detail_item["first"]
        assert detail_item[-1] == expected_detail_item["last"]
        assert common_item[0] == expected_common_item["first"]
        assert common_item[-1] == expected_common_item["last"]


def test_get_user_ppol_setting_exception() -> None:
    """get_user_ppol_setting例外テスト"""
    pass


@pytest.mark.parametrize(
    "user_id, es_company_id, is_deny, expected",
    params.test_is_deny_user(),
    ids=["case 1", "case 2"],
)
def test_is_deny_user(
    user_id,
    es_company_id,
    is_deny,
    expected,
    user_service: UserService,
    override_get_db: Session,
) -> None:
    """Test for user_service.is_deny_user function."""
    # テストデータの登録
    session = override_get_db
    session.add(
        UserAccessControlFactory(
            userId=user_id, esCompanyId=es_company_id, isDeny=is_deny
        )
    )
    session.commit

    # テスト対象処理の実行
    ret = user_service.is_deny_user(es_company_id, user_id)

    # テスト結果の検証
    assert ret == expected


@pytest.mark.parametrize("", params.test_is_deny_user_exception())
def test_is_deny_user_exception(
    user_service: UserService, override_get_db: Session
) -> None:
    """Test for user_service.is_deny_user function to handle exceptions."""
    pass


def test_patch_user_status(user_service: UserService) -> None:
    """patch_user_statusテスト"""
    for (
        user_id,
        request_body,
        expected,
    ) in params.test_patch_user_status():
        result = user_service.patch_user_status(user_id, request_body)
        assert result == expected


def test_patch_user_status_exception(user_service: UserService) -> None:
    """patch_user_status例外テスト"""
    for (
        user_id,
        request_body,
        expected,
    ) in params.test_patch_user_status_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            user_service.patch_user_status(user_id, request_body)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]
