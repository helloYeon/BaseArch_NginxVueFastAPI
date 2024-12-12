"""core/context_user_info.py"""

from contextvars import ContextVar

from models import User

user_info_context: ContextVar[User] = ContextVar("user_info")
