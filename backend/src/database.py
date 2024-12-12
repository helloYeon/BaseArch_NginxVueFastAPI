"""database.py"""

import json
import logging
import os
import sys
from contextlib import contextmanager
from logging import Formatter, StreamHandler, getLogger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Generator

from core.config import config
from core.context import uuid_context
from helpers import logger as hLogger
from load_env import env
from sqlalchemy import create_engine, event

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.orm.session import Session


class JsonFormatter(Formatter):
    """JSON形式でログを出力するためのフォーマッタ"""

    def format(self, record):
        """ログレコードをJSON形式に変換する

        Args:
            record: ログレコード

        Returns:
            str: JSON形式のログ
        """
        obj = record.__dict__.copy()

        obj["log_level"] = record.levelname
        # obj["uuid"] = uuid_context.get("uuid")

        # # 削除する属性のリスト
        obj.pop("levelno", None)
        obj.pop("levelname", None)

        if "args" in obj:
            obj["args"] = str(obj["args"])

        return json.dumps(obj)


# file handle設定
if config.isLocal():
    # ロギング設定
    logger = getLogger("sqlalchemy.engine")
    logger.setLevel(logging.INFO)

    # stream handle設定
    stream_handle = StreamHandler(sys.stdout)
    stream_handle.setFormatter(JsonFormatter())
    logger.addHandler(stream_handle)

    file = os.path.join(Path(__file__).parent, "storage/logs/sql.log")
    file_handle = TimedRotatingFileHandler(file, when="D", interval=1, backupCount=1)
    file_handle.setFormatter(JsonFormatter())
    logger.addHandler(file_handle)

# DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
#     env["DB_USERNAME"],
#     env["DB_PASSWORD"],
#     env["DB_HOST"],
#     env["DB_DATABASE"],
# )
DATABASE = "oracle+cx_oracle://%s:%s@%s:%s/?service_name=%s" % (
    env["DB_USERNAME"],
    env["DB_PASSWORD"],
    env["DB_HOST"],
    env["DB_PORT"],
    env["DB_DATABASE"],
)
# SQLAlchemy 用の engine を作成
engine = create_engine(
    DATABASE,
    echo=False,
    pool_pre_ping=True,
    pool_size=120,
    max_overflow=50,
)


def set_schema(dbapi_connection, connection_record):
    """デフォルトスキーマを設定するためのリスナーを追加"""
    with dbapi_connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = {}".format(env["DB_SCHEME"]))


event.listen(engine, "connect", set_schema)

# engine = engine.execution_options(isolation_level="AUTOCOMMIT")

# SQLAlchemy 用の session を作成
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# テスト用の session を作成(ほんちゃんAPPの場合は使用しない)
TestSessionLocal = scoped_session(sessionmaker(autoflush=True, bind=engine))

# SQLAlchemy のモデルで使用する
Base = declarative_base()

# # モデルで使用する query プロパティ
# Base.query = SessionLocal.query_property()


# @contextmanager
def get_db() -> Generator[Session, Any, None]:
    """Dependency Injection

    Yields:
        Generator[Session, Any, None]: DBセッション
    """
    # db = None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
