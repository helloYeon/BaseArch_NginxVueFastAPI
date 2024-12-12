"""load_env.py"""

import os
from os.path import dirname, join

from dotenv import load_dotenv

# 環境変数ファイルのパスを取得
dotenv_path = join(dirname(__file__), f".env.{os.environ.get('APP_ENV')}")

# 環境別.envファイルの読み込み
load_dotenv(dotenv_path, verbose=True, override=True)

# 環境変数の名前をリストとして定義
env_vars = [
    "APP_ENV",
    "DB_USERNAME",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_DATABASE",
    "DB_PORT",
    "DB_SCHEME",
]

# 環境変数を取得し、それぞれの名前と値を辞書に格納
env = {var: os.environ.get(var) for var in env_vars}
