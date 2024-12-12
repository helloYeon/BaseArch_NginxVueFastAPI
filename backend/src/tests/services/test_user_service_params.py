"""tests/services/test_user_service_params.py"""

from typing import Any

import enums
import pendulum
from api.v1.schemas.invoices.downloads.csv import PpolItem
from api.v1.schemas.users.me import PatchUserStatusRequest
from core.constant import const
from core.message import messages
from database import TestSessionLocal
from db.factories import (
    CompanyInfoFactory,
    InvoiceReceiveRecordFactory,
    UserFactory,
    UserPeppolItemFactory,
)
from enums import (
    CsvDownloadType,
    ReceiveRecordStatus,
    UserIsDisplay,
)
from exceptions.peppol_http_exception import PeppolHttpException


def test_get_user() -> list[Any]:
    """UserService.get_user()のテストパラメータ"""
    # テストデータ準備
    test_data = [
        UserFactory.build(userId=1, deletedAt=None),
        UserFactory.build(userId=2, deletedAt=pendulum.now()),
        UserFactory.build(userId=7, deletedAt=None),
    ]

    return [
        # case 1 : 存在するユーザ
        (1, UserFactory.build(userId=1, deletedAt=None), test_data),
        # case 2 : 存在するが削除されたユーザ
        (2, None, test_data),
        # case 3 : そもそも存在しないユーザ
        (999, None, test_data),
    ]


def test_get_user_exception() -> list[Any]:
    """UserService.get_user()の例外テストパラメータ"""
    return []


def test_get_user_company() -> list[Any]:
    """UserService.get_user()のテストパラメータ"""
    # テストデータ準備
    infos = {
        "user1": {"userId": 1, "companyInfosId": 1},
        "user2": {"userId": 2, "companyInfosId": 2},
        "company1": {"esCompanyId": 1, "deletedAt": None},
        "company2": {"esCompanyId": 2, "deletedAt": pendulum.now()},
    }

    test_data = [
        UserFactory.build(**infos["user1"]),
        UserFactory.build(**infos["user2"]),
        CompanyInfoFactory.build(**infos["company1"]),
        CompanyInfoFactory.build(**infos["company2"]),
    ]

    return [
        # case 1 : 存在する会社情報
        (1, CompanyInfoFactory.build(**infos["company1"]), test_data),
        # case 2 : 存在するが削除された会社
        (2, None, test_data),
    ]


def test_get_user_company_exception() -> list[Any]:
    """UserService.get_user_company()の例外テストパラメータ"""
    return [
        # case 1 : 存在しないユーザ
        {
            "args": {
                "user_id": 999,
            },
            "expected": {
                "exception": PeppolHttpException,
                "message": messages.NOT_EXIST_USER.message,
            },
        }
    ]


def test_get_user_last_record_date() -> list[Any]:
    """UserService.get_user_last_record_date()のテストパラメータ"""
    now = pendulum.now()
    # テストデータ準備
    infos = {
        "company1-target": {
            "companyInfosId": 1,
            "status": ReceiveRecordStatus.INSERT_OK,
            "getTimeTo": now,
        },
        "company1-before": {
            "companyInfosId": 1,
            "status": ReceiveRecordStatus.INSERT_OK,
            "getTimeTo": now.add(seconds=-1),
        },
        "company1-order_status": {
            "companyInfosId": 1,
            "status": ReceiveRecordStatus.RECEIVE_OK,
            "getTimeTo": now,
        },
        "company1-deleted": {
            "companyInfosId": 1,
            "status": ReceiveRecordStatus.INSERT_OK,
            "getTimeTo": now,
            "deletedAt": pendulum.now(),
        },
        "company2-target": {
            "companyInfosId": 2,
            "status": ReceiveRecordStatus.INSERT_OK,
            "getTimeTo": now.add(minutes=-10),
        },
    }

    with TestSessionLocal() as session:
        session.add_all(
            [InvoiceReceiveRecordFactory(**info) for info in infos.values()]
        )
        session.commit()

    return [
        # case 1 : 登録OK・最新
        (
            1,
            pendulum.instance(infos["company1-target"]["getTimeTo"]).format(
                "YYYYMMDDHHmm"
            ),
        ),
        # case 2 : case1とは別会社 登録OK
        (
            2,
            pendulum.instance(infos["company2-target"]["getTimeTo"]).format(
                "YYYYMMDDHHmm"
            ),
        ),
        # case 3 : 存在しない会社・まだ履歴がない会社
        (999, const.INIT_LAST_GET_DATE),
    ]


def test_get_user_last_record_date_exception() -> list[Any]:
    """UserService.get_user_last_record_date()の例外テストパラメータ"""
    return []


def is_exist_user() -> list[Any]:
    """UserService.is_exist_userのテストパラメータ"""
    # テストデータ準備
    infos = [
        {"userId": 1, "deletedAt": None},
        {"userId": 2, "deletedAt": pendulum.now()},
    ]

    with TestSessionLocal() as session:
        session.add_all([UserFactory(**info) for info in infos])
        session.commit()

    return [
        # case 1 : 存在するユーザ
        {
            "args": {
                "user_id": 1,
            },
            "expected": True,
        },
        # case 2 : 存在するが削除されたユーザ
        {
            "args": {
                "user_id": 2,
            },
            "expected": False,
        },
        # case 3 : 存在しないユーザ
        {
            "args": {
                "user_id": 999,
            },
            "expected": False,
        },
    ]


def test_is_exist_user_exception() -> list[Any]:
    """UserService.is_exist_user()の例外テストパラメータ"""
    return []


def test_upsert_login_info() -> list[Any]:
    """UserService.upsert_login_infoののテストパラメータ"""

    # テストデータ作成
    def create_test_data(
        user_id,
        session_id,
        es_company_id,
        new_first_name=None,
        new_company_name=None,
    ):

        first_name = "first_name" if new_first_name is None else new_first_name
        company_name = "first_name" if new_company_name is None else new_company_name
        return (
            {
                "userId": user_id,
                "sessionId": session_id,
                "esCompanyId": es_company_id,
                "lastName": "last_name",
                "firstName": first_name,
                "companyName": company_name,
            },
            UserFactory.build(
                userId=user_id,
                sessionId=session_id,
                companyInfosId=es_company_id,
                lastName="last_name",
                firstName=first_name,
            ),
        )

    # case 1のデータを登録
    case1 = {"user_id": 1, "session_id": "case 1", "es_company_id": 2}
    (info, _) = create_test_data(**case1)
    session = TestSessionLocal()
    company_info = CompanyInfoFactory(
        esCompanyId=info["esCompanyId"],
        name=info["companyName"],
    )
    session.add(company_info)
    session.flush()
    session.add(
        UserFactory(
            userId=info["userId"],
            sessionId=info["sessionId"],
            lastName=info["lastName"],
            firstName=info["firstName"],
            companyInfosId=company_info.id,
        )
    )
    session.commit()

    # テストデータ準備
    return [
        # case 1 : 既存データの更新（update）
        create_test_data(
            **case1,
            new_first_name="case1_new_first_name",
            new_company_name="case1_new_company_name",
        ),
        # case 2 : 新規登録
        create_test_data(
            user_id=2,
            session_id="case 2",
            es_company_id=2,
        ),
    ]


def test_upsert_login_info_exception() -> list[Any]:
    """UserService.upsert_login_infoののテストパラメータ()の例外テストパラメータ"""
    return [
        # case 1 : ユーザアップデートで例外発生
        (
            {
                "userId": 1,
                "sessionId": "session_1",
                "esCompanyId": 1,
                "lastName": "last_name",
                "firstName": "first_name",
                "companyName": "company_name",
            },
            {
                "mock_function": "user_repo.upsert_by_user_id",
                "mock_side_effect": Exception,
                "expected_message": messages.FAILED_UPSERT_USER.message,
            },
        ),
        # case 2 : 会社アップデートで例外発生
        (
            {
                "userId": 2,
                "sessionId": "session_2",
                "esCompanyId": 2,
                "lastName": "last_name",
                "firstName": "first_name",
                "companyName": "company_name",
            },
            {
                "mock_function": "company_info_repo.upsert_by_es_company_id",
                "mock_side_effect": Exception,
                "expected_message": messages.FAILED_UPSERT_COMPANY.message,
            },
        ),
    ]


def test_get_user_ppol_setting() -> list[
    tuple[
        int,
        int,
        tuple[dict[str, PpolItem], dict[str, PpolItem], dict[str, PpolItem]],
    ]
]:
    """get_user_ppol_settingテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    user_ppol_item1 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=1, sortOrder=2, isDisplay=UserIsDisplay.DISPLAY
    )
    user_ppol_item2 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=2, sortOrder=3, isDisplay=UserIsDisplay.DISPLAY
    )
    user_ppol_item3 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=3, sortOrder=1, isDisplay=UserIsDisplay.DISPLAY
    )
    not_get_user_ppol_item1 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=4, sortOrder=4, isDisplay=UserIsDisplay.HIDDEN
    )

    user_ppol_item4 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=236, sortOrder=4, isDisplay=UserIsDisplay.DISPLAY
    )
    user_ppol_item5 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=237, sortOrder=2, isDisplay=UserIsDisplay.DISPLAY
    )
    not_get_user_ppol_item2 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=241, sortOrder=1, isDisplay=UserIsDisplay.DISPLAY
    )

    user_ppol_item6 = UserPeppolItemFactory(
        userId=1, mstPpolItemsId=301, sortOrder=1, isDisplay=UserIsDisplay.DISPLAY
    )

    session.add_all(
        [
            user_ppol_item1,
            user_ppol_item2,
            user_ppol_item3,
            not_get_user_ppol_item1,
            user_ppol_item4,
            user_ppol_item5,
            not_get_user_ppol_item2,
            user_ppol_item6,
        ]
    )
    session.commit()

    return [
        # case 1 : mstデータから正常にPpolItemの形に変形できる
        (
            999,  # 今回はmstデータを使用するためのモック設定
            1,
            # 結果は各タプルフィールドの配列の最初と最後を比較する
            (
                {
                    "first": PpolItem(
                        btid="IBT-024",
                        name="ビジネスプロセスタイプ",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="IBT-115",
                        name="差引請求金額",
                        mstSortOrder=235,
                        parentSort=227,
                    ),
                },
                {
                    "first": PpolItem(
                        btid="IBT-126",
                        name="請求書明細行ID",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="IBT-148",
                        name="品目単価(値引前)(税抜き)",
                        mstSortOrder=65,
                        parentSort=62,
                    ),
                },
                {
                    "first": PpolItem(
                        btid="",
                        name="支払先コード",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="",
                        name="支払先コード",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                },
            ),
        ),
        # case 2 : userデータから正常にPpolItemの形に変形できる
        (
            8,  # 今回はuserデータを使用するためのモック設定
            1,
            # 結果は各タプルフィールドの配列の最初と最後を比較する
            (
                {
                    "first": PpolItem(
                        btid="IBT-001",
                        name="請求書番号",
                        mstSortOrder=3,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="IBT-023",
                        name="仕様ID",
                        mstSortOrder=2,
                        parentSort=0,
                    ),
                },
                {
                    "first": PpolItem(
                        btid="IBT-127",
                        name="請求書明細行注釈",
                        mstSortOrder=2,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="IBT-126",
                        name="請求書明細行ID",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                },
                {
                    "first": PpolItem(
                        btid="",
                        name="支払先コード",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                    "last": PpolItem(
                        btid="",
                        name="支払先コード",
                        mstSortOrder=1,
                        parentSort=0,
                    ),
                },
            ),
        ),
    ]


def test_is_deny_user() -> list[Any]:
    """UserService.is_deny_userののテストパラメータ"""
    return [
        # case 1 : アクセス不可ユーザ
        (
            1,
            1,
            enums.Access.IS_DENY,
            enums.Access.IS_DENY,
        ),
        # case 2 : アクセス可ユーザ
        (
            2,
            2,
            enums.Access.IS_ALLOW,
            enums.Access.IS_ALLOW,
        ),
    ]


def test_is_deny_user_exception() -> list[Any]:
    """UserService.is_deny_userののテストパラメータ()の例外テストパラメータ"""
    return []


def test_patch_user_status() -> list[tuple[int, PatchUserStatusRequest, None]]:
    """patch_user_statusテストパラメータ"""
    session = TestSessionLocal()

    user = UserFactory()
    session.add(user)
    session.commit()

    return [
        # case 1 : 存在しているユーザーのステータスを更新
        (
            user.id,
            PatchUserStatusRequest(
                csvDownloadType=CsvDownloadType.CREATING_YOUR_OWN_INVOICE
            ),
            None,
        ),
    ]


def test_patch_user_status_exception() -> (
    list[tuple[int, PatchUserStatusRequest, dict[str, Any]]]
):
    """patch_user_status例外テストパラメータ"""
    return [
        # case 1 : 存在していないユーザーのステータスを更新
        (
            999,
            PatchUserStatusRequest(
                csvDownloadType=CsvDownloadType.CREATING_YOUR_OWN_INVOICE
            ),
            {
                "exception": PeppolHttpException,
                "message": messages.NOT_EXIST_USER.message,
            },
        )
    ]
