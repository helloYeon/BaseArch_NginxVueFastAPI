"""exceptions/peppol_http_exception.py"""

import logging

from core.message import MessageModel
from fastapi import status


class PeppolHttpException(Exception):
    """PeppolHttpException

    Peppol HTTP操作に特化した例外を表すクラス

    Args:
        http_code (int, optional): HTTPステータスコード。デフォルトは500
        log_level (str, optional): ログレベル。デフォルトはERROR
        message_model (MessageModel, optional): エラーメッセージモデル。デフォルトは空のモデル
        message (str, optional): エラーメッセージ。デフォルトはNone
        extra (dict, optional): その他の追加情報。デフォルトは空の辞書
    """

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        log_level: str = logging.getLevelName(logging.ERROR),
        message_model: MessageModel = MessageModel(code="", message=""),
        message: str | None = None,
        extra: dict = {},
    ) -> None:
        self.status_code = status_code
        self.log_level = log_level

        self.code = message_model.code
        self.message = message_model.message

        if message is not None:
            self.message = message

        self.extra = extra
