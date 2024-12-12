"""tests/services/test_setting_service_params.py"""

from typing import Any

from api.v1.schemas.setting.payment_code import BaseItem, GetResponseItem, PutRequest
from core.message import messages
from database import TestSessionLocal
from db.factories import PaymentCodeFactory
from exceptions import PeppolHttpException


def test_get_payment_code_list() -> list[tuple[int, GetResponseItem]]:
    """get_payment_code_listテストパラメータ"""
    session = TestSessionLocal()

    payment_code = PaymentCodeFactory(
        companyInfosId=1, peppolId="1234:unittestPeppolId", paymentCode="unittest"
    )
    session.add(payment_code)
    session.commit()

    return [
        (
            # case 1: companyInfosId1の支払先コードを取得
            1,
            GetResponseItem(
                companyInfosId=1,
                items=[
                    BaseItem(peppolId="1234:unittestPeppolId", paymentCode="unittest")
                ],
            ),
        )
    ]


def test_put_payment_code_list() -> list[tuple[PutRequest, None]]:
    """put_payment_code_listテストパラメータ"""
    return [
        (
            # case 1: 1件登録
            PutRequest(
                companyInfosId=1,
                items=[
                    BaseItem(peppolId="1234:unittestPeppolId", paymentCode="unittest")
                ],
            ),
            None,
        )
    ]


def test_put_payment_code_list_exception() -> list[tuple[PutRequest, dict[str, Any]]]:
    """put_payment_code_list例外テストパラメータ"""
    session = TestSessionLocal()

    payment_code = PaymentCodeFactory(
        companyInfosId=1, peppolId="1234:unittestPeppolId", paymentCode="unittest"
    )
    session.add(payment_code)
    session.commit()

    return [
        (
            # case1: dbエラー
            PutRequest(
                companyInfosId=1,
                items=[
                    BaseItem(peppolId="1234:unittestPeppolId", paymentCode="unittest")
                ],
            ),
            {
                "exception": PeppolHttpException,
                "message": messages.FAILED_UPDATE_PAYMENT_CODES_MESSAGE.message,
            },
        )
    ]
