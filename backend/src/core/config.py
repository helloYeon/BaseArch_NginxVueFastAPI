"""core/config.py"""

import os
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constant import Constant


class Config(BaseSettings):
    """項目"""

    # フロントURL
    FQDN_FE: Union[str, None] = None

    # BASE DOMAIN
    BASE_DOMAIN: Union[str, None] = None

    # コンスタント
    CONSTANT: Constant = Constant()

    # class Config:
    #     """envファイルから自動読み込む"""

    #     # 小文字・大文字区別を行う
    #     case_sensitive = True

    #     # ファイル名
    #     env_file = ".env." + os.environ["APP_ENV"]

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env." + os.environ["APP_ENV"]
    )

    @classmethod
    def isLocal(cls) -> bool:
        """ローカル環境かどうか

        Returns:
            bool: 判定結果
        """
        return os.environ["APP_ENV"] == "local"

    def isCloudEnv(self) -> bool:
        """クラウド環境かどうか

        Returns:
            bool: 判定結果
        """
        return not self.isLocal()

    @classmethod
    def isDevelopment(cls) -> bool:
        """開発環境かどうか

        Returns:
            bool: 判定結果
        """
        return os.environ["APP_ENV"] == "development"

    @classmethod
    def isProduction(cls) -> bool:
        """本番環境かどうか

        Returns:
            bool: 判定結果
        """
        return os.environ["APP_ENV"] == "production"


# インスタンス
config = Config()
