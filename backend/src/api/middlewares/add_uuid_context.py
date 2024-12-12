"""api/middlewares/add_uuid_context.py"""

import uuid
from typing import Any

from core import context
from fastapi import Request


async def add_uuid_context(request: Request, call_next) -> Any:
    """UUIDをContextVarにセットする

    Args:
        request (Request): 受信リクエストオブジェクト
        call_next (Callable): 次のミドルウェアまたはエンドポイントハンドラ

    Returns:
        Any: 次のミドルウェアまたはエンドポイントハンドラ
    """
    # uuid 作成
    uid = str(uuid.uuid4())

    # context にセット
    context.uuid_context.set(uid)

    return await call_next(request)
