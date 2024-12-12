"""tests/services/test_company_service_params.py"""

from api.v1.schemas.company.integrations import BaseItem
from api.v1.schemas.test.test import CompanyInfosBaseItem, CompanyInfosPutRequest
from core.message import MessageModel, messages
from database import TestSessionLocal
from db.factories import CompanyInfoFactory
from enums import IsParent
from exceptions import PeppolHttpException
from models import CompanyInfo


def test_get_company_info() -> list[tuple[int, CompanyInfo]]:
    """get_company_infoテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    companyInfo = CompanyInfoFactory(name="unittestCompany")
    session.add(companyInfo)
    session.commit()

    return [
        # case 1 : 企業情報IDに合致している企業情報が存在
        (1, companyInfo),
    ]


def test_get_company_info_exception() -> list[tuple[int, dict]]:
    """get_company_info例外テストパラメータ"""
    return [
        # case 1 : 企業情報IDに合致している企業情報が存在しない
        (
            999,
            {
                "exception": PeppolHttpException,
                "message": messages.REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR.message,
            },
        ),
    ]


def test_get_integration_company_ids() -> list[tuple[CompanyInfo, list[int]]]:
    """get_integration_company_idsテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    companyInfo = CompanyInfoFactory(name="unittestCompany")
    session.add(companyInfo)
    session.commit()

    return [
        # case 1 : 企業情報に合致している企業のID一覧が存在
        (companyInfo, [1, 1]),
    ]


def test_get_integrations() -> list[tuple[CompanyInfo, list[BaseItem]]]:
    """get_integrationsテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    companyInfo1 = CompanyInfoFactory(esCompanyId=1, name="unittestCompany1")
    session.add(companyInfo1)
    session.flush()
    companyInfo2 = CompanyInfoFactory(esCompanyId=1, name="unittestCompany2")
    session.add(companyInfo2)
    session.commit()

    return [
        # case 1 : 企業情報に合致している結合企業と所属企業情報一覧が存在
        (
            companyInfo1,
            [
                BaseItem(
                    companyInfosId=1, name="unittestCompany1", isParent=IsParent.PARENT
                ),
                BaseItem(
                    companyInfosId=1, name="unittestCompany1", isParent=IsParent.CHILD
                ),
                BaseItem(
                    companyInfosId=2, name="unittestCompany2", isParent=IsParent.CHILD
                ),
            ],
        ),
    ]


def test_get_company_infos() -> list[list[CompanyInfosBaseItem]]:
    """get_company_infosテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    companyInfo1 = CompanyInfoFactory(
        esCompanyId=1, name="unittestCompany1", parentEsCompanyId=1
    )
    session.add(companyInfo1)
    session.flush()
    companyInfo2 = CompanyInfoFactory(
        esCompanyId=1, name="unittestCompany2", parentEsCompanyId=1
    )
    session.add(companyInfo2)
    session.commit()

    return [
        # case 1 : テストデータと一致
        [
            CompanyInfosBaseItem(
                id=companyInfo1.id,
                esCompanyId=companyInfo1.esCompanyId,
                name=companyInfo1.name,
                parentEsCompanyId=companyInfo1.parentEsCompanyId,
            ),
            CompanyInfosBaseItem(
                id=companyInfo2.id,
                esCompanyId=companyInfo2.esCompanyId,
                name=companyInfo2.name,
                parentEsCompanyId=companyInfo2.parentEsCompanyId,
            ),
        ]
    ]


def test_put_company_infos() -> list[tuple[CompanyInfosPutRequest, None]]:
    """put_company_infosテストパラメータ"""
    # テストデータ作成
    session = TestSessionLocal()

    companyInfo = CompanyInfoFactory(
        esCompanyId=1, name="unittestCompany1", parentEsCompanyId=1
    )
    session.add(companyInfo)
    session.commit()

    return [
        # case 1 : 存在している企業情報を更新
        (
            CompanyInfosPutRequest(
                data=[
                    CompanyInfosBaseItem(
                        id=companyInfo.id,
                        esCompanyId=companyInfo.esCompanyId,
                        name="updateName",
                        parentEsCompanyId=companyInfo.parentEsCompanyId,
                    )
                ]
            ),
            None,
        )
    ]
