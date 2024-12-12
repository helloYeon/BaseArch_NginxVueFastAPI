"""main.py"""

from api import middlewares
from api.v1 import routers
from fastapi import FastAPI
from handlers import (
    custom_exception_handler,
)
from handlers.logging_context_route import LoggingContextRoute

# FastAPI
app = FastAPI(
    root_path="/peppolreceive",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    # debug=True,
)

# リクエスト処理ロギング
app.router.route_class = LoggingContextRoute

# middleware corsを追加
middlewares.setup_cors(app)

# middleware uuid_contextを追加
app.middleware("http")(middlewares.add_uuid_context)


# 疎通・テスト用
app.include_router(routers.tests.router)


# ヘルスチェック
@app.get("/api/v1/hc", tags=["etc"])
def health_check() -> None:
    """ヘルスチェック"""
    pass
