"""tests/repositories/test_mst_ppol_item_repository.py"""

import pytest
import test_mst_ppol_item_repository_params as test_params
from database import TestSessionLocal
from db.seeders.mst_ppol_items import mst_ppol_items_seed
from helpers.rds import truncate_and_reset_sequence
from models import MstPpolItem
from repositories.mst_ppol_item_repository import MstPpolItemRepository


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
    db.close()


@pytest.fixture
def mst_ppol_item_repository(override_get_db) -> MstPpolItemRepository:
    """MstPpolItemRepositoryのインスタンスを返す"""
    repository = MstPpolItemRepository(override_get_db)

    return repository


def test_find(mst_ppol_item_repository: MstPpolItemRepository) -> None:
    """findテスト"""
    for id, expected in test_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = mst_ppol_item_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_get_all(mst_ppol_item_repository: MstPpolItemRepository) -> None:
    """get_allテスト"""
    # メソッドの呼び出しと結果の検証
    for expected in test_params.test_get_all():
        result = mst_ppol_item_repository.get_all()

        assert result == expected


def test_get_all_exception() -> None:
    """get_all例外テスト"""
    assert True


def test_get_all_by_type(mst_ppol_item_repository: MstPpolItemRepository) -> None:
    """get_all_by_typeテスト"""
    for type, expected in test_params.test_get_all_by_type():
        # メソッドの呼び出しと結果の検証
        result = mst_ppol_item_repository.get_all_by_type(type)

        assert result == expected


def test_get_all_by_type_exception() -> None:
    """get_all_by_type例外テスト"""
    assert True


def test_get_all_by_type_exist(mst_ppol_item_repository: MstPpolItemRepository) -> None:
    """get_all_by_type_existテスト"""
    for type, expected in test_params.test_get_all_by_type_exist():
        # メソッドの呼び出しと結果の検証
        result = mst_ppol_item_repository.get_all_by_type_exist(type)

        assert result == expected


def test_get_all_by_type_exist_exception() -> None:
    """get_all_by_type_exist例外テスト"""
    assert True


def test_get_count(mst_ppol_item_repository: MstPpolItemRepository) -> None:
    """get_countテスト"""
    for expected in test_params.test_get_count():
        # メソッドの呼び出しと結果の検証
        result = mst_ppol_item_repository.get_count()

        assert result == expected


def test_get_count_exception() -> None:
    """get_count例外テスト"""
    assert True
