"""load_env.py"""

import os
from os.path import dirname, join

from dotenv import load_dotenv

# 環境変数ファイルのパスを取得
dotenv_path = join(dirname(__file__), f".env.{os.environ.get('APP_ENV')}")

# 環境別.envファイルの読み込み
load_dotenv(dotenv_path, verbose=True, override=True)
