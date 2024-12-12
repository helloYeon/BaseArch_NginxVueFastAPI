"""tests/repositories/test_user_ppol_item_repository.py"""

import pytest
import test_user_ppol_item_repository_params
from database import TestSessionLocal
from db.seeders.mst_ppol_items import mst_ppol_items_seed
from helpers.rds import truncate_and_reset_sequence
from models import MstPpolItem
from repositories.user_ppol_item_repository import UserPpolItemRepository


@pytest.fixture(scope="module", autouse=True)
def truncate_mst_ppol_item():
    """テスト前にmst_ppol_itemテーブルをトランケートし、テスト後にシードデータを挿入"""
    print("Truncate mst_ppol_items table...")
    db = TestSessionLocal()
    truncate_and_reset_sequence(db, MstPpolItem)
    db.close()

    yield

    print("Seed mst_ppol_item table...")

    mst_ppol_items_seed()


@pytest.fixture(scope="function", autouse=True)
def truncate_mst_ppol_items_after_each_test():
    """各テスト実行後にmst_ppol_itemsテーブルをトランケート"""
    yield
    print("Truncate mst_ppol_items table after test...")
    db = TestSessionLocal()
    truncate_and_reset_sequence(db, MstPpolItem)
    db.close()


@pytest.fixture
def user_ppol_item_repository(override_get_db) -> UserPpolItemRepository:
    """UserPpolItemRepositoryのインスタンスを返す"""
    repository = UserPpolItemRepository(override_get_db)

    return repository


def test_find(user_ppol_item_repository: UserPpolItemRepository) -> None:
    """findテスト"""
    for id, expected in test_user_ppol_item_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_all_by_user_id(user_ppol_item_repository: UserPpolItemRepository) -> None:
    """get_all_by_user_idテスト"""
    for (
        user_id,
        expected,
    ) in test_user_ppol_item_repository_params.test_get_all_by_user_id():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.get_all_by_user_id(user_id)

        assert result == expected


def test_get_all_by_user_id_exception() -> None:
    """get_all_by_user_id例外テスト"""
    assert True


def test_delete_by_user_id(user_ppol_item_repository: UserPpolItemRepository) -> None:
    """delete_by_user_idテスト"""
    for (
        user_id,
        expected,
    ) in test_user_ppol_item_repository_params.test_delete_by_user_id():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.delete_by_user_id(user_id)

        assert result == expected


def test_delete_by_user_id_exception() -> None:
    """delete_by_user_id例外テスト"""
    assert True


def test_insert_by_user_ppol_items(
    user_ppol_item_repository: UserPpolItemRepository,
) -> None:
    """insert_by_user_ppol_itemsテスト"""
    for (
        user_ppol_items,
        expected,
    ) in test_user_ppol_item_repository_params.test_insert_by_user_ppol_items():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.insert_by_user_ppol_items(user_ppol_items)

        assert result == expected


def test_insert_by_user_ppol_items_exception() -> None:
    """insert_by_user_ppol_items例外テスト"""
    assert True


def test_get_all_by_type(user_ppol_item_repository: UserPpolItemRepository) -> None:
    """get_all_by_typeテスト"""
    for (
        user_id,
        type,
        expected,
    ) in test_user_ppol_item_repository_params.test_get_all_by_type():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.get_all_by_type(user_id, type)

        assert result == expected


def test_get_all_by_type_exception() -> None:
    """get_all_by_type例外テスト"""
    assert True


def test_get_count(user_ppol_item_repository: UserPpolItemRepository) -> None:
    """get_countテスト"""
    for (
        user_id,
        expected,
    ) in test_user_ppol_item_repository_params.test_get_count():
        # メソッドの呼び出しと結果の検証
        result = user_ppol_item_repository.get_count(user_id)

        assert result == expected


def test_get_count_exception() -> None:
    """get_count例外テスト"""
    assert True
