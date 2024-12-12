"""core/message.py"""

from pydantic import BaseModel


class MessageModel(BaseModel):
    """メッセージモデル"""

    code: str
    message: str


class Messages(BaseModel):
    """メッセージクラス"""

    # パラメーターが不正
    INVALID_PARAMETER: MessageModel = MessageModel(
        code="I0001", message="The parameters are invalid"
    )

    # to_issue_dateがfrom_issue_dateより過去の時
    FROM_ISSUE_DATE_VALIDATION_ERROR_MESSAGE: MessageModel = MessageModel(
        code="I0001", message="Must be a date after from_issue_date"
    )

    # to_inv_amount < from_inv_amountの時
    FROM_INV_AMOUNT_VALIDATION_ERROR_MESSAGE: MessageModel = MessageModel(
        code="I0001", message="Must be higher than from_inv_amount."
    )

    # to_receive_date_timeがfrom_receive_date_timeより過去の時
    FROM_RECEIVE_DATE_TIME_VALIDATION_ERROR_MESSAGE: MessageModel = MessageModel(
        code="I0001", message="Must be a datetime after from_receive_date_time"
    )

    # ユーザーアクセス可否更新リクエストでdataの中身が存在しない
    USER_ACCESS_CONTROL_DATA_NOT_FOUND_MESSAGE: MessageModel = MessageModel(
        code="I0001", message="Empty"
    )

    # 支払先コード一覧更新リクエストで自身のcompany_infos_idとは異なるcompany_infos_idが含まれている
    PAYMENT_CODES_REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR: MessageModel = (
        MessageModel(code="I0001", message="Contains multiple companyInfosId")
    )

    # 支払先コード一覧更新リクエストでpeppolIdが重複している
    PAYMENT_CODES_REQUEST_PEPPOL_ID_DUPLICATE: MessageModel = MessageModel(
        code="I0001", message="Duplicate"
    )

    # 支払先コード一覧更新リクエストでpeppolIdがパターンに一致しない
    PAYMENT_CODES_REQUEST_PEPPOL_ID_VALIDATION_ERROR: MessageModel = MessageModel(
        code="I0001",
        message="Must be pattern '{four-digit number}:{one-byte alphanumeric characters}' ",
    )

    # 支払先コード一覧更新リクエストでpaymentCodeが15文字以下でない
    PAYMENT_CODES_REQUEST_PAYMENT_CODE_LENGTH_VALIDATION_ERROR: MessageModel = (
        MessageModel(
            code="I0001",
            message="Must be less than 15 characters",
        )
    )

    # 支払先コード一覧更新リクエストでpaymentCodeに半角英数字以外の文字が含まれている
    PAYMENT_CODES_REQUEST_PAYMENT_CODE_CHARACTER_VALIDATION_ERROR: MessageModel = (
        MessageModel(
            code="I0001",
            message="Must be one-byte alphanumeric characters only",
        )
    )

    # 空のリクエストボディが送信された
    BODY_NO_ITEM: MessageModel = MessageModel(
        code="I0001",
        message="More than 1 item is required",
    )

    # 該当請求書レコードが存在しない
    INVOICE_DATA_NOT_FOUND_MESSAGE: MessageModel = MessageModel(
        code="I0002", message="Invoice data not found"
    )
    # 該当請求書明細レコードが存在しない
    INVOICE_DETAIL_DATA_NOT_FOUND_MESSAGE: MessageModel = MessageModel(
        code="I0003", message="Invoice detail data not found"
    )

    # 指定したcompany_infos_idが所属企業、結合企業に該当しない
    REQUEST_COMPANY_INFOS_ID_VALIDATION_ERROR: MessageModel = MessageModel(
        code="I0004",
        message="Not applicable to own company or combined company",
    )

    # 支払先コードが存在しない
    PAYMENT_CODE_NOT_FOUND: MessageModel = MessageModel(
        code="I0005", message="PaymentCode is not found"
    )

    # 指定した請求書受信履歴レコードが存在しない
    INVOICE_RECEIVE_RECORD_NOT_FOUND_MESSAGE: MessageModel = MessageModel(
        code="I0006", message="Invoice Receive Record not found"
    )

    # CSVダウンロード対象の検索結果が0件だった場合
    INVOICE_SEARCH_RESULT_NOT_FOUND: MessageModel = MessageModel(
        code="I0007", message="Invoice search returned 0 results"
    )

    # ユーザーが存在しない
    NOT_EXIST_USER: MessageModel = MessageModel(
        code="E0001", message="User does not exist"
    )

    # S3アップロード失敗
    XML_UPLOAD_FAILED_MESSAGE: MessageModel = MessageModel(
        code="E0002", message="Failed to upload XML to S3"
    )

    # ファイル名取得失敗
    FAILED_GET_FILE_NAME_MESSAGE: MessageModel = MessageModel(
        code="E0003", message="Failed get filename"
    )

    # S3 XMLダウンロード失敗
    XML_DOWNLOAD_FAILED_MESSAGE: MessageModel = MessageModel(
        code="E0004", message="Failed to download XML from S3"
    )

    # mst_ppol_items取得エラー
    FAILED_GET_MST_PPOL_ITEMS_MESSAGE: MessageModel = MessageModel(
        code="E0005", message="Failed get csv item data"
    )
    # user_ppol_items更新エラー
    FAILED_UPDATE_USER_PPOL_ITEMS_MESSAGE: MessageModel = MessageModel(
        code="E0006", message="Failed update csv item data"
    )

    # ユーザー情報一括取得APIエラー
    FAILED_GET_USERS_DATA_MESSAGE: MessageModel = MessageModel(
        code="E0007", message="Failed get users data"
    )

    # user_access_controls更新エラー
    FAILED_UPDATE_USER_ACCESS_CONTROLS_MESSAGE: MessageModel = MessageModel(
        code="E0008", message="Failed update users data"
    )

    # payment_codes更新エラー
    FAILED_UPDATE_PAYMENT_CODES_MESSAGE: MessageModel = MessageModel(
        code="E0009", message="Failed update PaymentCodes"
    )

    # invoice_receive_record.id取得失敗
    FAILED_INSERT_INVOICE_RECEIVE_RECORD: MessageModel = MessageModel(
        code="E0010", message="Failed insert InvoiceReceiveRecord"
    )

    # 企業情報登録・更新失敗
    FAILED_UPSERT_COMPANY: MessageModel = MessageModel(
        code="E0011", message="Failed upsert CompanyInfo"
    )

    # ユーザー情報登録・更新失敗
    FAILED_UPSERT_USER: MessageModel = MessageModel(
        code="E0012", message="Failed upsert User"
    )

    # ZIP受け取り失敗
    ZIP_RECEIVE_FAILED_MESSAGE: MessageModel = MessageModel(
        code="E9001", message="Failed to receive ZIP"
    )

    # データ変換失敗
    XML_TRANSFORM_FAILED_MESSAGE: MessageModel = MessageModel(
        code="E9002", message="Failed to transform XML"
    )

    # ユーザ認証失敗
    USER_AUTHENTICATION_FAILED: MessageModel = MessageModel(
        code="E9011", message="User authentication failed (BtoB external API)"
    )

    AUTH_IP_ADDRESS_NOT_ALLOWED: MessageModel = MessageModel(
        code="E9012", message="User authentication failed (BtoB external API)"
    )

    AUTH_SESSION_TIMED_OUT: MessageModel = MessageModel(
        code="E9013", message="User authentication failed (BtoB external API)"
    )

    AUTH_PASSWORD_EXPIRED: MessageModel = MessageModel(
        code="E9014", message="User authentication failed (BtoB external API)"
    )

    AUTH_LOGOUT_FORCED: MessageModel = MessageModel(
        code="E9015", message="User authentication failed (BtoB external API)"
    )

    AUTH_NOT_FOUND: MessageModel = MessageModel(
        code="E9016", message="User authentication failed (BtoB external API)"
    )

    # 外部API呼び出しエラー
    EXTERNAL_API_CALL_ERROR: MessageModel = MessageModel(
        code="E9004", message="External API call error"
    )

    # サーバーエラー
    INTERNAL_SERVER_ERROR: MessageModel = MessageModel(
        code="E9999", message="Internal server error"
    )


# インスタンス
messages = Messages()
