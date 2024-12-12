"""core/context.py"""

from contextvars import ContextVar
from typing import Optional

uuid_context: ContextVar[Optional[str]] = ContextVar("uuid", default=None)
