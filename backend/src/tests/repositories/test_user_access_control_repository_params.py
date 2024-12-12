"""tests/repositories/test_user_access_control_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import UserAccessControlFactory
from enums import Access
from models import UserAccessControl


def test_find() -> list[tuple[int, UserAccessControl | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = UserAccessControlFactory()
    payment_code_deleted_record = UserAccessControlFactory(deletedAt=pendulum.now())
    session.add_all([payment_code_record, payment_code_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, payment_code_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_get_all_by_es_company_id() -> list[tuple[int, list[UserAccessControl]]]:
    """get_all_by_es_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_access_control_record = UserAccessControlFactory(esCompanyId=1)
    user_access_control_record2 = UserAccessControlFactory(esCompanyId=1)
    user_access_control_deleted_record = UserAccessControlFactory(
        esCompanyId=2, deletedAt=pendulum.now()
    )
    session.add_all(
        [
            user_access_control_record,
            user_access_control_record2,
            user_access_control_deleted_record,
        ]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, [user_access_control_record, user_access_control_record2]),
        # # case 2 : IDに合致している情報が存在しない
        (999, []),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, []),
    ]


def test_get_by_es_company_id_user_id_is_deny() -> (
    list[tuple[int, int, Access, UserAccessControl | None]]
):
    """get_by_es_company_id_user_id_is_denyテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_access_control_record = UserAccessControlFactory(
        esCompanyId=1, userId=1, isDeny=True
    )
    user_access_control_deleted_record = UserAccessControlFactory(
        esCompanyId=2, userId=2, isDeny=True, deletedAt=pendulum.now()
    )
    session.add_all([user_access_control_record, user_access_control_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, 1, Access.IS_DENY, user_access_control_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, 999, Access.IS_DENY, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, 2, Access.IS_DENY, None),
        # case 4 : アクセス可否が異なる
        (1, 1, Access.IS_ALLOW, None),
    ]


def test_delete_by_es_company_id() -> list[tuple[int, None]]:
    """delete_by_es_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    user_access_control_record = UserAccessControlFactory(esCompanyId=1)
    user_access_control_record2 = UserAccessControlFactory(esCompanyId=1)
    user_access_control_deleted_record = UserAccessControlFactory(
        esCompanyId=2, deletedAt=pendulum.now()
    )
    session.add_all(
        [
            user_access_control_record,
            user_access_control_record2,
            user_access_control_deleted_record,
        ]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, None),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, None),
    ]


def test_insert_by_user_ppol_items() -> list[tuple[list[UserAccessControl], None]]:
    """insert_by_user_ppol_itemsテスト"""
    user_access_control_record = UserAccessControlFactory()
    user_access_control_record2 = UserAccessControlFactory()

    return [
        # case 1 : 登録できる
        ([user_access_control_record, user_access_control_record2], None),
    ]
