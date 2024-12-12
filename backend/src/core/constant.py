"""core/constant.py"""

from pydantic import BaseModel


class Constant(BaseModel):
    """コンスタントクラス"""

    # 実行結果
    PROC_RESULT_FAILED: int = 0
    PROC_RESULT_SUCCESS: int = 1

    # 請求書受取の前回取得日時初期設定(2010年1月1日1時1分)
    INIT_LAST_GET_DATE: str = "200101010101"

    # Tag
    INVOICE_TAG: str = "Invoice"
    INVOICE_LINE_TAG: str = "cac:InvoiceLine"

    # 要素をラップするkey名
    XML_VALUE_WRAP_KEY: str = "value"

    # 変換処理データをラップするkey名
    TRANSFORM_DATA_WRAP_KEY: str = "b2b_format_datas"

    # 条件を持つbtId
    AUTO8: str = "AUTO-8"
    IBG24: str = "IBG-24"
    AUTO14: str = "AUTO-14"
    AUTO15: str = "AUTO-15"
    AUTO20: str = "AUTO-20"
    AUTO22: str = "AUTO-22"
    IBG20: str = "IBG-20"
    IBG21: str = "IBG-21"
    AUTO64: str = "AUTO-64"
    IBG37: str = "IBG-37"
    IBG36: str = "IBG-36"
    AUTO87: str = "AUTO-87"
    IBG27: str = "IBG-27"
    IBG28: str = "IBG-28"

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

    # PeppolId正規表現(半角数字4文字:半角英数字)
    PEPPOL_ID_PATTERN: str = "^[0-9]{4}:[0-9a-zA-Z]*$"

    # 共通マスタデータ管理
    PAYMENT_CODE_NAME: str = "支払先コード"

    # 日本の通貨
    CURRENCY_OF_JAPAN: str = "JPY"


# インスタンス
const = Constant()
