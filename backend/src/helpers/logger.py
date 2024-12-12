"""helpers/logger.py"""

import json
import logging
import os
import sys
from logging import Formatter, StreamHandler, getLogger
from logging.handlers import TimedRotatingFileHandler

from core.context import uuid_context


class JsonFormatter(Formatter):
    """JSONフォーマッタ"""

    def format(self, record) -> str | None:
        """ロガーフォーマット

        Args:
            record: ログレコード

        Returns:
            str | None: JSON形式のログ
        """
        # botoのデバッグログを除外
        # if record.levelno == logging.DEBUG and "boto" in record.pathname:
        #     return ""

        # レコーダーのコピー
        original_obj = record.__dict__.copy()

        # 項目追加
        obj = {
            "log_level": original_obj.pop("levelname"),
            "uuid": uuid_context.get("uuid"),
        }

        obj.update(original_obj)

        # ログ出力時に不要な情報を削除
        obj.pop("name", None)
        obj.pop("levelno", None)
        obj.pop("args", None)
        obj.pop("exc_info", None)
        obj.pop("created", None)
        obj.pop("relativeCreated", None)

        return json.dumps(obj)


# ロギング設定
logger = getLogger(__name__)

if os.environ.get("APP_ENV") == "prod":
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)

# ストリームハンドラ登録
stream_handle = StreamHandler(sys.stdout)
stream_handle.setFormatter(JsonFormatter())
logger.addHandler(stream_handle)

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# ログファイルの絶対パスを作成
log_file_path = os.path.join(script_dir, "../storage/logs/python.log")

# ファイルハンドラ登録
file_handle = TimedRotatingFileHandler(
    log_file_path, when="D", interval=1, backupCount=10
)
file_handle.setFormatter(JsonFormatter())
logger.addHandler(file_handle)


def debug(message, extra: dict | None = None) -> None:
    """DEBUGログ出力

    Args:
        message (str): ログメッセージ
        extra (dict | None, optional): 追加情報. Defaults to None.
    """
    logger.debug(message, extra={"extra": extra}, stacklevel=2)


def info(message, extra: dict | None = None) -> None:
    """INFOログ出力

    Args:
        message (str): ログメッセージ
        extra (dict | None, optional): 追加情報. Defaults to None.
    """
    logger.info(message, extra={"extra": extra}, stacklevel=2)


def error(message, extra: dict | None = {}) -> None:
    """ERRORログ出力

    Args:
        message (str): ログメッセージ
        extra (dict | None, optional): 追加情報. Defaults to None.
    """
    logger.error(message, extra={"extra": extra}, stacklevel=2)
