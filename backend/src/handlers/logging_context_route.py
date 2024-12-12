"""handlers/logging_context_route.py"""

import json
import logging
import sys
import traceback
from typing import Callable, Optional, Union

import pendulum
from core.context import uuid_context
from exceptions import PeppolHttpException
from fastapi import Request, Response
from fastapi import status as fastapi_status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from helpers import logger
from starlette.exceptions import HTTPException as StarletteHTTPException


class LoggingContextRoute(APIRoute):
    """APIRouteを継承し、ログフォーマットを変更"""

    def get_route_handler(self) -> Callable:
        """APIRouteのget_route_handlerをオーバーライト

        Returns:
            Callable: カスタムハンドラ
        """
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Union[Response, None]:
            """カスタムハンドラ

            Args:
                request (Request): リクエスト

            Returns:
                Union[Response, None]: レスポンス
            """
            response = None

            # ロギング項目を定義
            record = {}

            # fmt:off
            record["log_level"]        = logging.getLevelName(logging.INFO)
            record["uuid"]             = uuid_context.get("uuid")
            record["message"]          = None # エラーメッセージまたは詳細
            record["request_method"]   = None # リクエストメソッド
            record["request_uri"]      = None # リクエストパス
            record["proc_time"]        = None # リクエストの処理時間（秒）
            record["request_headers"]  = None # リクエストヘッダ
            record["request_body"]     = None # リクエストボディ
            record["response_headers"] = None # レスポンスヘッダ
            record["response_body"]    = None # レスポンスボディ
            record["traceback"]        = None # エラー発生時のスタックトレース
            record["http_status"]      = None # レスポンスのHTTPステータスコード
            record["remote_addr"]      = None # アクセス元 IP アドレス
            record["request_date"]     = None # リクエストを受け取った日時
            record["extra"]            = None # その他追加情報
            # fmt:on

            # ログ リクエスト関連ロギング
            await self._logging_request(request, record)

            # 処理にかかる時間を計測
            before = pendulum.now().timestamp()

            try:
                # リクエスト処理開始
                response = await self._execute_request(
                    request, original_route_handler, record
                )
            finally:
                # レスポンス情報記録
                await self._logging_response(response, record)

                # リクエストを受け取った日時
                record["request_date"] = pendulum.from_timestamp(
                    before, tz="Asia/Tokyo"
                ).format("YYYY-MM-DD HH:mm:ss")

                # リクエストの処理時間（秒）
                record["proc_time"] = str(round(pendulum.now().timestamp() - before, 4))

                # ストリームハンドラに独自のFormatterを設定
                stream_handler = logging.StreamHandler(sys.stdout)
                stream_handler.setFormatter(logging.Formatter("%(message)s"))

                # ファイルハンドラに独自のFormatterを設定
                file_handle = logger.file_handle
                file_handle.setFormatter(logging.Formatter("%(message)s"))

                # custom_route_handler内専用のロガーを作成
                custom_logger = logging.getLogger(__name__)
                custom_logger.handlers.clear()  # ハンドラをクリア
                custom_logger.propagate = False  # 設定の継承を停止
                custom_logger.setLevel(logging.INFO)

                # ハンドラを追加
                custom_logger.addHandler(stream_handler)
                custom_logger.addHandler(file_handle)

                # ログ出力
                custom_logger.info(json.dumps(record))

            return response

        return custom_route_handler

    async def _logging_request(
        self, request: Request, record: dict
    ) -> Optional[Response]:
        """リクエスト関連ロギング
            request_body
            request_headers
            request_uri
            request_method

        Args:
            request (Request): リクエスト
            record (dict): ロギング項目

        Returns:
            Optional[Response]: Response
        """
        if await (body := request.body()):
            try:
                # is jsonの場合
                record["request_body"] = await request.json()
            except json.JSONDecodeError:
                # not jsonの場合
                record["request_body"] = (await body).decode("utf-8")

        # fmt:off
        record["request_headers"] = {k.decode("utf-8"): v.decode("utf-8") for (k, v) in request.headers.raw}
        record["request_uri"]     = request.url.path
        record["request_method"]  = request.method
        record["remote_addr"]     = request.client.host if request.client else None
        # fmt:on

    async def _logging_response(
        self, response: Union[Response, None], record: dict
    ) -> Response:
        """レスポンス関連のロギング
        status
        response_headers
        response_body

        Args:
            response (Union[Response, None]): レスポンス
            record (dict): ロギング項目

        Returns:
            Response: レスポンス
        """
        if response is None:
            return JSONResponse({})

        # fmt:off
        record["http_status"]      = response.status_code
        record["response_headers"] = {k.decode("utf-8"): v.decode("utf-8") for (k, v) in response.headers.raw}
        record["response_body"]    = (
            response.body.decode("utf-8")
            if response.headers.get("content-type") == "application/json"
            else "{}"
        )
        # fmt:on

        try:
            record["response_body"] = json.loads(record["response_body"])
        except json.JSONDecodeError:
            pass

        return response

    async def _execute_request(
        self, request: Request, route_handler: Callable, record: dict
    ) -> Response:
        """リクエスト処理開始

        Args:
            request (Request): リクエスト
            route_handler (Callable): ハンドラ
            record (dict): ロギング項目

        Returns:
            Response: レスポンス
        """
        try:
            response: Response = await route_handler(request)
        except StarletteHTTPException as exc:
            # fmt:off
            record["log_level"]    = logging.getLevelName(logging.ERROR)
            record["http_status"]  = exc.status_code
            record["message"]      = exc.detail
            # fmt:on
            raise
        except RequestValidationError as exc:
            # fmt:off
            record["log_level"] = logging.getLevelName(logging.INFO)
            record["message"]   = str(exc)
            # fmt:on
            raise
        except PeppolHttpException as exc:
            # fmt:off
            record["log_level"]   = exc.log_level
            record["message"]     = exc.message
            record["http_status"] = exc.status_code
            record["extra"]       = exc.extra
            # fmt:on
            raise
        except Exception as exc:
            # fmt:off
            record["log_level"]   = logging.getLevelName(logging.ERROR)
            record["message"]     = str(exc)
            record["http_status"] = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
            # fmt:on
            raise
        finally:
            record["traceback"] = traceback.format_exc().splitlines()

        return response
