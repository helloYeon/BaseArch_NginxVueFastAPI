"""/api/v1/routers/tests/tests.py"""

import os
import socket
import sys
from typing import Any

from core.config import config
from fastapi import APIRouter, Request
from handlers.logging_context_route import LoggingContextRoute
from helpers import logger

router = APIRouter(
    prefix="/api/v1/tests",
    tags=["tests"],
    route_class=LoggingContextRoute,
)


@router.get("/env", name="環境変数を確認")
def get_env(request: Request) -> dict[str, Any]:
    """環境変数を確認

    Returns:
        dict[str, Any]: 全ての環境変数
    """
    # リクエストのIPアドレス
    client_ip = request.client.host

    # サーバーのマシンのIPアドレス
    try:
        server_ip = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        logger.error(f"IPアドレスの取得に失敗しました: {e}")
        server_ip = "IP取得失敗"

    logger.info("info test")
    logger.error("error test")

    return {
        # "os.environ": dict(config),
        "APP_ENV": os.environ.get("APP_ENV"),
        "Client IP": client_ip,
        "Server IP": server_ip,
        "os.environ": dict(os.environ),
        "PATH": sys.path,
    }
