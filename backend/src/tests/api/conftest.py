"""tests/api/conftest.py"""

from typing import Callable, Dict, Generator

import pytest
from core.context_user_info import user_info_context
from dependencies import verify_session
from enums.csv_download_type import CsvDownloadType
from fastapi.testclient import TestClient
from main import app
from models import User

DEFAULT_SIGNED_IN_USER = User(
    id=1,
    userId=1,
    sessionId="1",
    companyInfosId=1,
    lastName="unit",
    firstName="test",
    csvDownloadType=CsvDownloadType.ALL_ITEMS,
)


async def mock_verify_session() -> None:
    """verify_sessionモック化"""
    # ユーザー情報をコンテキストにセット
    user_info_context.set(DEFAULT_SIGNED_IN_USER)


@pytest.fixture(scope="module")
def signed_in_user_data() -> Callable[[], User]:
    """ログインユーザデータ"""

    def _signed_user() -> User:
        return DEFAULT_SIGNED_IN_USER

    return _signed_user


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """TestClientセットアップ"""
    app.dependency_overrides[verify_session] = mock_verify_session

    yield TestClient(app)

    app.dependency_overrides.pop(verify_session)
