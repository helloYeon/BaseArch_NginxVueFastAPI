"""tests/repositories/test_user_repository.py"""

import pytest
import test_user_repository_params
from repositories.user_repository import UserRepository


@pytest.fixture
def user_repository(override_get_db) -> UserRepository:
    """UserRepositoryのインスタンスを返す"""
    repository = UserRepository(override_get_db)

    return repository


def test_find(user_repository: UserRepository) -> None:
    """findテスト"""
    for id, expected in test_user_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = user_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_by_user_id(user_repository: UserRepository) -> None:
    """get_by_user_idテスト"""
    for user_id, expected in test_user_repository_params.test_get_by_user_id():
        # メソッドの呼び出しと結果の検証
        result = user_repository.get_by_user_id(user_id)

        assert result == expected


def test_get_by_user_id_exception() -> None:
    """get_by_user_id例外テスト"""
    assert True


def test_is_exist_by_user_id(user_repository: UserRepository) -> None:
    """is_exist_by_user_idテスト"""
    for user_id, expected in test_user_repository_params.test_is_exist_by_user_id():
        # メソッドの呼び出しと結果の検証
        result = user_repository.is_exist_by_user_id(user_id)

        assert result == expected


def test_is_exist_by_user_id_exception() -> None:
    """is_exist_by_user_id例外テスト"""
    assert True


@pytest.mark.skip(
    reason="現在使用していないメソッドのため、Skip / PEPPOL_RECEIVE-508 OCI移行 : Oracleに合わせてユニットテスト修正"
)
def test_upsert_by_key(user_repository: UserRepository) -> None:
    """upsert_by_keyテスト"""
    for user_data, expected in test_user_repository_params.test_upsert_by_key():
        # メソッドの呼び出しと結果の検証
        result = user_repository.upsert_by_key(user_data)

        if result is None:
            return

        assert result.id == expected.id
        assert result.userId == expected.userId
        assert result.sessionId == expected.sessionId
        assert result.companyInfosId == expected.companyInfosId
        assert result.lastName == expected.lastName
        assert result.firstName == expected.firstName


def test_upsert_by_key_exception() -> None:
    """upsert_by_key例外テスト"""
    assert True


def test_upsert_by_user_id(user_repository: UserRepository) -> None:
    """upsert_by_user_idテスト"""
    for user_info, expected in test_user_repository_params.test_upsert_by_user_id():
        # メソッドの呼び出しと結果の検証
        result = user_repository.upsert_by_user_id(user_info)

        if result is None:
            return

        assert result.id == expected.id
        assert result.userId == expected.userId
        assert result.sessionId == expected.sessionId
        assert result.companyInfosId == expected.companyInfosId
        assert result.lastName == expected.lastName
        assert result.firstName == expected.firstName


def test_upsert_by_user_id_exception() -> None:
    """upsert_by_user_id例外テスト"""
    assert True


def test_patch_user_status(user_repository: UserRepository) -> None:
    """patch_user_statusテスト"""
    for (
        user_id,
        csv_download_type,
        expected,
    ) in test_user_repository_params.test_patch_user_status():
        # メソッドの呼び出しと結果の検証
        result = user_repository.patch_user_status(user_id, csv_download_type)

        assert result.rowcount == expected


def test_path_user_status_exception() -> None:
    """patch_user_status例外テスト"""
    assert True
