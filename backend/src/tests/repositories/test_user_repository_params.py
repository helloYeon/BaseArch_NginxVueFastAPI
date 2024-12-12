"""tests/repositories/test_user_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import UserFactory
from enums import CsvDownloadType
from models import User


def test_find() -> list[tuple[int, User | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory()
    user_deleted_record = UserFactory(deletedAt=pendulum.now())
    session.add_all([user_record, user_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, user_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_by_user_id() -> list[tuple[int, User | None]]:
    """get_by_user_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory(userId=1)
    user_deleted_record = UserFactory(userId=2, deletedAt=pendulum.now())
    session.add_all([user_record, user_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, user_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_is_exist_by_user_id() -> list[tuple[int, bool]]:
    """is_exist_by_user_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory(userId=1)
    user_deleted_record = UserFactory(userId=2, deletedAt=pendulum.now())
    session.add_all([user_record, user_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, True),
        # # case 2 : IDに合致している情報が存在しない
        (999, False),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, False),
    ]


def test_upsert_by_key() -> list[tuple[dict, User]]:
    """upsert_by_keyテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory()
    session.add(user_record)
    session.commit()

    return [
        # case 1 : ユーザー情報が存在する場合は更新
        (
            {
                "id": user_record.id,
                "userId": 1,
                "sessionId": "session_id",
                "companyInfosId": 1,
                "lastName": "last_name",
                "firstName": "first_name",
            },
            User(
                id=user_record.id,
                userId=1,
                sessionId="session_id",
                companyInfosId=1,
                lastName="last_name",
                firstName="first_name",
            ),
        ),
        # case 2 : ユーザー情報が存在しない場合は新規登録
        (
            {
                "id": 999,
                "userId": 2,
                "sessionId": "session_id2",
                "companyInfosId": 1,
                "lastName": "last_name2",
                "firstName": "first_name2",
            },
            User(
                id=999,
                userId=2,
                sessionId="session_id2",
                companyInfosId=1,
                lastName="last_name2",
                firstName="first_name2",
                csvDownloadType=2,
            ),
        ),
    ]


def test_upsert_by_user_id() -> list[tuple[User, User]]:
    """upsert_by_user_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory(userId=1)
    session.add(user_record)
    session.commit()

    return [
        # case 1 : ユーザー情報が存在する場合は更新
        (
            User(
                userId=1,
                sessionId="session_id",
                companyInfosId=1,
                lastName="last_name",
                firstName="first_name",
            ),
            User(
                id=user_record.id,
                userId=1,
                sessionId="session_id",
                companyInfosId=1,
                lastName="last_name",
                firstName="first_name",
            ),
        ),
        # case 2 : ユーザー情報が存在しない場合は新規登録
        (
            User(
                userId=2,
                sessionId="session_id2",
                companyInfosId=1,
                lastName="last_name2",
                firstName="first_name2",
            ),
            User(
                id=2,
                userId=2,
                sessionId="session_id2",
                companyInfosId=1,
                lastName="last_name2",
                firstName="first_name2",
            ),
        ),
    ]


def test_patch_user_status() -> list[tuple[int, CsvDownloadType, int]]:
    """patch_user_statusテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_record = UserFactory(userId=1)
    session.add(user_record)
    session.commit()

    return [
        # case 1 : ユーザーステータス更新
        (1, CsvDownloadType.ALL_ITEMS, 1),
        # case 2 : ユーザーステータス更新
        (1, CsvDownloadType.CREATING_YOUR_OWN_INVOICE, 1),
        # case 3 : ユーザー情報が存在しない場合
        (999, CsvDownloadType.ALL_ITEMS, 0),
    ]
