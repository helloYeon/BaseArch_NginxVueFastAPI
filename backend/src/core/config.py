"""core/config.py"""

import os
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from .constant import Constant


class Config(BaseSettings):
    """項目"""

    # DB関連
    DB_HOST: Union[str, None] = None
    DB_DATABASE: Union[str, None] = None
    DB_USERNAME: Union[str, None] = None
    DB_PASSWORD: Union[str, None] = None
    DB_PORT: Union[str, None] = None
    DB_SCHEME: Union[str, None] = None

    # フロントURL
    FQDN_FE: Union[str, None] = None

    # BASE DOMAIN
    BASE_DOMAIN: Union[str, None] = None

    # AWS関連
    AWS_S3_PUBLIC_BUCKET: Union[str, None] = None
    AWS_S3_PRIVATE_BUCKET: Union[str, None] = None
    AWS_DEFAULT_REGION: Union[str, None] = None
    AWS_S3_URL: Union[str, None] = None
    AWS_ACCESS_KEY_ID: Union[str, None] = None
    AWS_SECRET_KEY: Union[str, None] = None

    # OCI関連
    OCI_REGION: Union[str, None] = None
    OCI_STORAGE_ENDPOINT: Union[str, None] = None
    OCI_ACCESS_KEY: Union[str, None] = None
    OCI_SECRET_KEY: Union[str, None] = None

    # アクセスポイント
    IM_ACCESS_POINT_ORIGIN: Union[str, None] = None

    # 認証関連APIオリジン
    AUTH_API_ORIGIN: Union[str, None] = None

    # 認証関連APIヘッダー情報
    AUTH_API_HEADER_IM_ES3_APP_ID: Union[str, None] = None
    AUTH_API_HEADER_IM_ES3_SECRET: Union[str, None] = None
    AUTH_API_HEADER_IM_ES3_VERSION: Union[str, None] = None

    # 認証関連 : パラメータ情報
    AUTH_API_RECEIVE_SERVICE_ID: Union[str, None] = None
    AUTH_API_RECEIVE_OPTION_ID: Union[str, None] = None

    # Oracleデフォルトスキーマ
    DEFAULT_SCHEME: Union[str, None] = None

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
