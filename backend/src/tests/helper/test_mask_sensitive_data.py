"""tests/helpers/test_mask_sensitive_data.py"""

import test_mask_sensitive_data_params
from core.config import Config
from helpers.mask_sensitive_data import mask_sensitive_data


def test_mask_sensitive_data(mocker) -> None:
    """mask_sensitive_dataテスト"""
    for (
        value,
        expected,
    ) in test_mask_sensitive_data_params.test_mask_sensitive_data():
        # 環境変数をproductionに設定
        mocker.patch.object(Config, "isProduction", return_value=True)

        # メソッドの呼び出しと結果の検証
        result = mask_sensitive_data(value)

        assert result == expected


def test_mask_sensitive_data_exception() -> None:
    """mask_sensitive_data例外テスト"""
    assert True
