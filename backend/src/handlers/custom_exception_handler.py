"""handlers/peppol_http_exception_handler.py"""

from api.v1.schemas.base_schema import Header
from api.v1.schemas.error_schema import ErrorModel
from core.message import messages
from fastapi import Request
from fastapi import status as fastapi_status
from fastapi.responses import JSONResponse


def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """PeppolHttpExceptionハンドラ
    Args:
        request (Request)   : リクエスト情報を含むオブジェクト
        exc     (Exception) : PeppolHttpExceptionの詳細を含む例外

    Returns:
        JSONResponse | Response: エラーメッセージを含むJSONレスポンス
    """
    return JSONResponse(
        status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorModel(
            header=Header(code=messages.INTERNAL_SERVER_ERROR.code, message=str(exc)),
        ).model_dump(),
    )
