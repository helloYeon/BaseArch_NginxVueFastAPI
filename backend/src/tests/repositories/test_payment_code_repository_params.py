"""tests/repositories/test_payment_code_repository_params.py"""

import pendulum
from database import TestSessionLocal
from db.factories import PaymentCodeFactory
from models import PaymentCode


def test_find() -> list[tuple[int, PaymentCode | None]]:
    """findテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = PaymentCodeFactory(companyInfosId=1, peppolId="1111:test")
    payment_code_deleted_record = PaymentCodeFactory(
        companyInfosId=2, peppolId="2222:test", deletedAt=pendulum.now()
    )
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


def test_get_all_by_company_ids() -> list[tuple[list[int], list[PaymentCode]]]:
    """get_all_by_company_idsテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = PaymentCodeFactory(companyInfosId=1, peppolId="1111:test")
    payment_code_record2 = PaymentCodeFactory(companyInfosId=1, peppolId="2222:test")
    payment_code_deleted_record = PaymentCodeFactory(
        companyInfosId=2, peppolId="3333:test", deletedAt=pendulum.now()
    )
    session.add_all(
        [payment_code_record, payment_code_record2, payment_code_deleted_record]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        ([1], [payment_code_record, payment_code_record2]),
        # # case 2 : IDに合致している情報が存在しない
        ([999], []),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        ([2], []),
    ]


def test_get_all_by_company_infos_id() -> list[tuple[int, list[PaymentCode]]]:
    """get_all_by_company_infos_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = PaymentCodeFactory(companyInfosId=1, peppolId="1111:test")
    payment_code_record2 = PaymentCodeFactory(companyInfosId=1, peppolId="2222:test")
    payment_code_deleted_record = PaymentCodeFactory(
        companyInfosId=2, peppolId="3333:test", deletedAt=pendulum.now()
    )
    session.add_all(
        [payment_code_record, payment_code_record2, payment_code_deleted_record]
    )
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        (1, [payment_code_record, payment_code_record2]),
        # # case 2 : IDに合致している情報が存在しない
        (999, []),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        (2, []),
    ]


def test_delete_by_company_infos_id() -> list[tuple[int, None]]:
    """delete_by_company_infos_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = PaymentCodeFactory(companyInfosId=1, peppolId="1111:test")
    payment_code_record2 = PaymentCodeFactory(companyInfosId=1, peppolId="2222:test")
    payment_code_deleted_record = PaymentCodeFactory(
        companyInfosId=2, peppolId="3333:test", deletedAt=pendulum.now()
    )
    session.add_all(
        [payment_code_record, payment_code_record2, payment_code_deleted_record]
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


def test_insert_by_payment_codes() -> list[tuple[list[PaymentCode], None]]:
    """insert_by_payment_codesテスト"""
    payment_code_record = PaymentCodeFactory(companyInfosId=1, peppolId="1111:test")
    payment_code_record2 = PaymentCodeFactory(companyInfosId=2, peppolId="2222:test")

    return [
        # case 1 : 登録できる
        ([payment_code_record, payment_code_record2], None),
    ]


def test_get_by_peppol_id_company_infos_id() -> (
    list[tuple[str, int, PaymentCode | None]]
):
    """get_by_peppol_id_company_infos_idテスト"""
    # テストデータ作成
    session = TestSessionLocal()

    payment_code_record = PaymentCodeFactory(
        companyInfosId=1,
        peppolId="1111:test",
    )
    payment_code_deleted_record = PaymentCodeFactory(
        companyInfosId=1, peppolId="3333:test", deletedAt=pendulum.now()
    )
    session.add_all([payment_code_record, payment_code_deleted_record])
    session.commit()

    return [
        # case 1 : IDに合致している情報が存在
        ("1111:test", 1, payment_code_record),
        # # case 2 : IDに合致している情報が存在しない
        ("2222:test", 1, None),
        # case 3 : IDに合致している情報が存在（論理削除済み）
        ("3333:test", 1, None),
    ]
