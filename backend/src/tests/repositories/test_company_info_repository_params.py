"""tests/repositories/test_company_info_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import (
    CompanyInfoFactory,
)
from models import CompanyInfo


def test_find() -> list[tuple[int, CompanyInfo | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    company_info_record = CompanyInfoFactory(esCompanyId=1)
    company_info_deleted_record = CompanyInfoFactory(
        esCompanyId=2, deletedAt=pendulum.now()
    )
    session.add_all([company_info_record, company_info_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (company_info_record.id, company_info_record),
        # # case 2 : IDに合致している情報が存在しない
        (999, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (company_info_deleted_record.id, None),
    ]


def test_is_exist_by_company_id() -> list[tuple[int, bool]]:
    """is_exist_by_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    company_info_record = CompanyInfoFactory()
    session.add_all([company_info_record])
    session.commit()

    return [
        # case 1 : 企業IDに合致している情報が存在
        (company_info_record.esCompanyId, True),
        # case 2 : 企業IDに合致している情報が存在しない
        (999, False),
    ]


def test_get_by_es_company_id() -> list[tuple[int, CompanyInfo | None]]:
    """get_by_es_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    company_info_record = CompanyInfoFactory()
    session.add_all([company_info_record])
    session.commit()

    return [
        # case 1 : 企業IDに合致している情報が存在
        (company_info_record.esCompanyId, company_info_record),
        # case 2 : 企業IDに合致している情報が存在しない
        (999, None),
    ]


def test_upsert_by_es_company_id() -> list[tuple[CompanyInfo, CompanyInfo | None]]:
    """upsert_by_es_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    company_info_record = CompanyInfoFactory(esCompanyId=1)
    company_info_record2 = CompanyInfoFactory(esCompanyId=2)
    session.add_all([company_info_record])
    session.commit()

    return [
        # case 1 : 企業IDに合致している情報が存在する場合更新
        (company_info_record, company_info_record),
        # case 2 : 企業IDに合致している情報が存在しない場合新規作成
        (company_info_record2, company_info_record2),
    ]


def test_get_all_by_parent_es_company_id() -> list[tuple[int, list[CompanyInfo]]]:
    """get_all_by_parent_es_company_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    company_info_record = CompanyInfoFactory(esCompanyId=1, parentEsCompanyId=None)
    company_info_record2 = CompanyInfoFactory(esCompanyId=2, parentEsCompanyId=1)
    company_info_record3 = CompanyInfoFactory(esCompanyId=3, parentEsCompanyId=1)
    company_info_record4 = CompanyInfoFactory(esCompanyId=4, parentEsCompanyId=None)
    session.add_all(
        [
            company_info_record,
            company_info_record2,
            company_info_record3,
            company_info_record4,
        ]
    )
    session.commit()

    return [
        # case 1 : 親企業IDに合致している情報が存在
        (company_info_record.esCompanyId, [company_info_record2, company_info_record3]),
        # case 2 : 親企業IDに合致している情報が存在しない
        (999, []),
    ]
