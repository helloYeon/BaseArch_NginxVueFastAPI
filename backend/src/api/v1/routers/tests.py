"""/api/v1/routers/tests/tests.py"""

import os
import sys
from typing import Any

import api.v1.schemas.error_schema as error_schema
import helpers
import pendulum
from api.v1.schemas.base_schema import Header, PayloadObject
from api.v1.schemas.http.receive import ReceiveModel
from api.v1.schemas.test.test import (
    CompanyInfosItemResponse,
    CompanyInfosPutRequest,
    CompanyInfosPutResponse,
    CompanyInfosPutResponseItem,
    S3uploadResponse,
    S3uploadResponseItem,
)
from core.config import config
from core.constant import const
from core.context import uuid_context
from core.context_user_info import user_info_context
from core.message import MessageModel
from database import get_db
from dependencies import verify_session
from dependencies.services import (
    depend_company_service,
)
from exceptions.peppol_http_exception import PeppolHttpException
from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from handlers.logging_context_route import LoggingContextRoute
from helpers import logger
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/v1/tests",
    tags=["tests"],
    route_class=LoggingContextRoute,
)


@router.get("/env", name="環境変数を確認")
def get_env() -> dict[str, Any]:
    """環境変数を確認

    Returns:
        dict[str, Any]: 全ての環境変数
    """
    return {
        "os.environ": dict(config),
        "APP_ENV": os.environ.get("APP_ENV"),
        "DB_USERNAME": os.environ.get("DB_USERNAME"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_DATABASE": os.environ.get("DB_DATABASE"),
        "DB_PORT": os.environ.get("DB_PORT"),
        "PATH": sys.path,
    }
