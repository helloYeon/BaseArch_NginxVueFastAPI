"""api/middlewares/cors.py"""

import os

from core.config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> None:
    """CORSを設定する

    Args:
        app (FastAPI): FastAPI
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if config.isLocal() else [os.environ["FQDN_FE"]],
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "HEAD", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition", "Access-Control-Allow-Origin"],
    )
