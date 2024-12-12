"""tests/repositories/test_user_access_control_repository.py"""

import pytest
import test_user_access_control_repository_params
from repositories.user_access_control_repository import UserAccessControlRepository


@pytest.fixture
def user_access_control_repository(override_get_db) -> UserAccessControlRepository:
    """UserAccessControlRepositoryのインスタンスを返す"""
    repository = UserAccessControlRepository(override_get_db)

    return repository


def test_find(user_access_control_repository: UserAccessControlRepository) -> None:
    """findテスト"""
    for id, expected in test_user_access_control_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = user_access_control_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_all_by_es_company_id(
    user_access_control_repository: UserAccessControlRepository,
) -> None:
    """get_all_by_es_company_idテスト"""
    for (
        es_company_id,
        expected,
    ) in test_user_access_control_repository_params.test_get_all_by_es_company_id():
        # メソッドの呼び出しと結果の検証
        result = user_access_control_repository.get_all_by_es_company_id(es_company_id)

        assert result == expected


def test_get_all_by_es_company_id_exception() -> None:
    """get_all_by_es_company_id例外テスト"""
    assert True


def test_get_by_es_company_id_user_id_is_deny(
    user_access_control_repository: UserAccessControlRepository,
) -> None:
    """get_by_es_company_id_user_id_is_denyテスト"""
    for (
        es_company_id,
        user_id,
        is_deny,
        expected,
    ) in (
        test_user_access_control_repository_params.test_get_by_es_company_id_user_id_is_deny()
    ):
        # メソッドの呼び出しと結果の検証
        result = user_access_control_repository.get_by_es_company_id_user_id_is_deny(
            es_company_id, user_id, is_deny
        )

        assert result == expected


def test_get_by_es_company_id_user_id_is_deny_exception() -> None:
    """get_by_es_company_id_user_id_is_deny例外テスト"""
    assert True


def test_delete_by_es_company_id(
    user_access_control_repository: UserAccessControlRepository,
) -> None:
    """delete_by_es_company_idテスト"""
    for (
        es_company_id,
        expected,
    ) in test_user_access_control_repository_params.test_delete_by_es_company_id():
        # メソッドの呼び出しと結果の検証
        result = user_access_control_repository.delete_by_es_company_id(es_company_id)

        assert result == expected


def test_delete_by_es_company_id_exception() -> None:
    """delete_by_es_company_id例外テスト"""
    assert True


def test_insert_by_user_ppol_items(
    user_access_control_repository: UserAccessControlRepository,
) -> None:
    """insert_by_user_ppol_itemsテスト"""
    for (
        user_access_controls,
        expected,
    ) in test_user_access_control_repository_params.test_insert_by_user_ppol_items():
        # メソッドの呼び出しと結果の検証
        result = user_access_control_repository.insert_by_user_ppol_items(
            user_access_controls
        )

        assert result == expected


def test_insert_by_user_ppol_items_exception() -> None:
    """insert_by_user_ppol_items例外テスト"""
    assert True
