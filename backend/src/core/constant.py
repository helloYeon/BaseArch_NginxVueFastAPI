"""core/constant.py"""

from pydantic import BaseModel


class Constant(BaseModel):
    """コンスタントクラス"""

    # 実行結果
    PROC_RESULT_FAILED: int = 0
    PROC_RESULT_SUCCESS: int = 1

    # 日付フォーマット
    PENDULUM_DATE_FORMAT: str = "YYYY-MM-DD"
    PENDULUM_DATETIME_FORMAT: str = "YYYY-MM-DD HH:mm"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATE_FORMAT_SLASH: str = "%Y/%m/%d"
    TIME_FORMAT: str = "%H:%M:%S"
    DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M"

    # CSVダウンロード制限数
    LIMIT_CSV_DOWNLOAD: int = 65535

    # 半角英数字正規表現
    ONE_BYTE_ALPHANUMERIC: str = "^[0-9a-zA-Z]*$"


# インスタンス
const = Constant()
