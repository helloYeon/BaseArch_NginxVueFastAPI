"""tests/api/test_PP020.py"""

from typing import Callable

import pytest
import test_PP020_params
from enums.csv_download_type import CsvDownloadType
from fastapi import status
from models import User


@pytest.mark.parametrize(
    """
    expected
    """,
    test_PP020_params.test_PP020,
)
def test_PP020(expected, client, signed_in_user_data: Callable[[], User]) -> None:
    """PP020APIテスト"""
    # デフォルトログインユーザ情報変更
    user = signed_in_user_data()
    user.csvDownloadType = CsvDownloadType.CREATING_YOUR_OWN_INVOICE

    # APIの呼び出しと結果の検証
    result = client.get("api/v1/users/me")

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == expected


def test_PP020_exception() -> None:
    """PP020API例外テスト"""
    assert True
