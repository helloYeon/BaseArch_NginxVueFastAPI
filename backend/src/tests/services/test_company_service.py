"""tests/services/test_company_service.py"""

import pytest
import test_company_service_params
from services.company_service import CompanyService


@pytest.fixture
def company_service(override_get_db) -> CompanyService:
    """CompanyServiceのインスタンスを返す"""
    service = CompanyService(override_get_db)

    return service


def test_get_company_info(company_service: CompanyService) -> None:
    """get_company_infoテスト"""
    for (
        company_info_id,
        expected,
    ) in test_company_service_params.test_get_company_info():
        result = company_service.get_company_info(company_info_id)

        assert result == expected


def test_get_company_info_exception(
    company_service: CompanyService,
) -> None:
    """get_company_info例外テスト"""
    for (
        company_info_id,
        expected,
    ) in test_company_service_params.test_get_company_info_exception():
        with pytest.raises(expected["exception"]) as exc_info:
            company_service.get_company_info(company_info_id)
        assert exc_info.type == expected["exception"]
        assert exc_info.value.message == expected["message"]


def test_get_integration_company_ids(company_service: CompanyService) -> None:
    """get_integration_company_idsテスト"""
    for (
        company_info,
        expected,
    ) in test_company_service_params.test_get_integration_company_ids():
        result = company_service.get_integration_company_ids(company_info)

        assert result == expected


def test_get_integration_company_ids_exception() -> None:
    """get_integration_company_ids例外テスト"""
    assert True


def test_get_integrations(company_service: CompanyService) -> None:
    """get_integrationsテスト"""
    for (
        company_info,
        expected,
    ) in test_company_service_params.test_get_integrations():
        result = company_service.get_integrations(company_info)

        assert result == expected


def test_get_integrations_exception() -> None:
    """get_integrations例外テスト"""
    assert True


def test_get_company_infos(company_service: CompanyService) -> None:
    """get_company_infosテスト"""
    for expected in test_company_service_params.test_get_company_infos():
        result = company_service.get_company_infos()

        assert result == expected


def test_get_company_exception() -> None:
    """get_company例外テスト"""
    assert True


def test_put_company_infos(company_service: CompanyService) -> None:
    """put_company_infosテスト"""
    for request, expected in test_company_service_params.test_put_company_infos():
        result = company_service.put_company_infos(request)

        assert result == expected


def test_put_company_infos_exception() -> None:
    """put_company_infos例外テスト"""
    assert True
