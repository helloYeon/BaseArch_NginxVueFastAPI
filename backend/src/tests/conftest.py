"""tests/conftest.py"""

import logging
import os
import re
from typing import Any, Generator

import models
import pytest
from database import TestSessionLocal
from helpers import truncate_and_reset_sequence
from sqlalchemy.orm.session import Session

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


@pytest.fixture(scope="function")
def override_get_db() -> Generator[Session, Any, None]:
    """テスト用のDBセッションを返す"""
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def truncate_tables() -> Generator[None, Any, None]:
    """セッション開始時にすべてのテーブルをトランケートする"""
    _truncate_all_tables()
    yield


def pytest_collection_modifyitems(config, items):
    """CI環境でAWSテストをスキップする"""
    if os.getenv("CI"):
        skip_aws = pytest.mark.skip(reason="Skipping AWS tests in CI environment")
        for item in items:
            if "aws_test" in item.keywords:
                item.add_marker(skip_aws)


def pytest_runtest_teardown(item, nextitem) -> None:
    """テストケース実行後にtruncateする

    Args:
        item: 現在テスト
        nextitem: 次のテスト
    """
    # 現在のテストケースのnodeidを取得
    current_node_id = _extract_node_id(item.nodeid)

    # 次のテストケースのnodeidを取得
    next_node_id = _extract_node_id(nextitem.nodeid) if nextitem else None

    # 各テスト関数がすべてのパラメータで実行された後にテーブルをトランケートする
    if current_node_id != next_node_id:
        _truncate_all_tables()


def _truncate_all_tables() -> None:
    """すべてのテーブルをトランケートする"""
    conn = TestSessionLocal()
    # テーブルのトランケートとシーケンスのリセット
    truncate_and_reset_sequence(conn, models.CompanyInfo)
    truncate_and_reset_sequence(conn, models.InvoiceDetail)
    truncate_and_reset_sequence(conn, models.InvoiceReceiveRecord)
    truncate_and_reset_sequence(conn, models.Invoice)
    truncate_and_reset_sequence(conn, models.PaymentCode)
    truncate_and_reset_sequence(conn, models.UserAccessControl)
    truncate_and_reset_sequence(conn, models.UserPpolItem)
    truncate_and_reset_sequence(conn, models.User)

    conn.close()
    print("\n🍎 Truncated all tables")


def _extract_node_id(nodeid: str) -> str:
    """テストケースのnodeidを抽出する"""
    return re.sub(r"\[.*?\]", "", nodeid.split("::")[1])
