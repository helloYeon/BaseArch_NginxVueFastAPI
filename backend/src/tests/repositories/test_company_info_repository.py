"""tests/repositories/test_company_info_repository.py"""

import pytest
import test_company_info_repository_params
from repositories.company_info_repository import (
    CompanyInfoRepository,
)


@pytest.fixture
def company_info_repository(
    override_get_db,
) -> CompanyInfoRepository:
    """CompanyInfoRepositoryのインスタンスを返す"""
    repository = CompanyInfoRepository(override_get_db)

    return repository


def test_find(
    company_info_repository: CompanyInfoRepository,
) -> None:
    """findテスト"""
    for id, expected in test_company_info_repository_params.test_find():
        # メソッドの呼び出しと結果の検証
        result = company_info_repository.find(id)

        assert result == expected


def test_find_exception() -> None:
    """find例外テスト"""
    assert True


def test_is_exist_by_company_id(
    company_info_repository: CompanyInfoRepository,
) -> None:
    """is_exist_by_company_idテスト"""
    for (
        company_id,
        expected,
    ) in test_company_info_repository_params.test_is_exist_by_company_id():
        # メソッドの呼び出しと結果の検証
        result = company_info_repository.is_exist_by_company_id(company_id)

        assert result == expected


def test_is_exist_by_company_id_exception() -> None:
    """is_exist_by_company_id例外テスト"""
    assert True


def test_get_by_es_company_id(
    company_info_repository: CompanyInfoRepository,
) -> None:
    """get_by_es_company_idテスト"""
    for (
        es_company_id,
        expected,
    ) in test_company_info_repository_params.test_get_by_es_company_id():
        # メソッドの呼び出しと結果の検証
        result = company_info_repository.get_by_es_company_id(es_company_id)

        assert result == expected


def test_get_by_es_company_id_exception() -> None:
    """get_by_es_company_id例外テスト"""
    assert True


def test_upsert_by_es_company_id(
    company_info_repository: CompanyInfoRepository,
) -> None:
    """upsert_by_es_company_idテスト"""
    for (
        company_info,
        expected,
    ) in test_company_info_repository_params.test_upsert_by_es_company_id():
        # メソッドの呼び出しと結果の検証
        result = company_info_repository.upsert_by_es_company_id(company_info)

        assert result == expected


def test_upsert_by_es_company_id_exception() -> None:
    """upsert_by_es_company_id例外テスト"""
    assert True


def test_get_all_by_parent_es_company_id(
    company_info_repository: CompanyInfoRepository,
) -> None:
    """get_all_by_parent_es_company_idテスト"""
    for (
        es_company_id,
        expected,
    ) in test_company_info_repository_params.test_get_all_by_parent_es_company_id():
        # メソッドの呼び出しと結果の検証
        result = company_info_repository.get_all_by_parent_es_company_id(es_company_id)

        assert result == expected


def test_get_all_by_parent_es_company_id_exception() -> None:
    """get_all_by_parent_es_company_id例外テスト"""
    assert True
