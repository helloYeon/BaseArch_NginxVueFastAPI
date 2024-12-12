import {
  MstType,
  DataType,
  PaymentMethod,
  IsOpen,
  IsConfirmation,
  IsDownload,
  CsvDownloadType,
} from '@/codegen'

// ルート名管理
const ROUTE_NAMES = {
  INVOICE_LIST: 'InvoiceList',
  INVOICE_DETAIL: 'InvoiceDetail',
  SETTINGS: 'Settings',
  UNAUTHORIZED: '401Unauthorized',
  NOT_FOUND: '404NotFound',
  INTERNAL_SERVER_ERROR: 'InternalServerError',
} as const

// 通知CSVファイルの各情報のindex
const CSV_START_DATE_INDEX = 0
const CSV_START_TIME_INDEX = 1
const CSV_END_DATE_INDEX = 2
const CSV_END_TIME_INDEX = 3
const CSV_TEXT_INDEX = 4

// 日本円の請求書通貨
const JPY_CURRENCY = {
  CODE: 'JPY',
  MARK: '¥',
} as const
// ドルの請求書通貨
const USD_CURRENCY = {
  CODE: 'USD',
  MARK: '$',
} as const
// その他の請求書通貨マーク
const OTHER_CURRENCY_MARK = '(外貨)'

// 一覧表示数cookie
const INVOICE_LIST_SIZE = 'invoiceListSize'
const INVOICE_LIST_DEFAULT_SIZE = 10

// 一覧表示数選択管理
const INVOICE_LIST_SIZE_STATUS = [
  { title: '10', value: 10 },
  { title: '20', value: 20 },
  { title: '30', value: 30 },
  { title: '40', value: 40 },
  { title: '50', value: 50 },
  { title: '100', value: 100 },
] as const

// 一覧検索バリデーションメッセージ管理
const INVOICE_LIST_VALIDATION_MESSAGES = {
  MAX_LENGTH: '255文字以下で入力してください',
  INTEGER: '整数で入力してください',
  MIN_NUMBER: '0以上の数字を入れてください',
  NUMBER_TYPE: '半角数字を入力してください',
  TO_INV_AMOUNT: '左の請求金額以上の値を入力してください',
  TO_ISSUE_DATE: '開始日以降の日付を選択してください',
  TO_RECEIVE_DATE_TIME: '左の受信日時以降の日時を選択してください',
} as const

// 設定項目TYPE
const INVOICE_DETAIL_TYPE = {
  VALUE: MstType.INVOICES,
  NAME: '請求出力内容',
} as const
const PARTICULARS_TYPE = {
  VALUE: MstType.PARTICULARS,
  NAME: '明細出力内容',
} as const
const COMMON_TYPE = {
  VALUE: 3,
  NAME: '共通出力内容',
} as const

// 請求書DataType管理
const INVOICE_QUALIFIEDINVOICE_TEXT = '適格請求書'
const INVOICE_PURCHASESTATEMENT_TEXT = '仕入明細書'
const INVOICE_ITEMIZEDINVOICE_TEXT = '区分記載請求書'
const INVOICE_DATA_TYPE_STATUS = [
  { title: INVOICE_QUALIFIEDINVOICE_TEXT, value: DataType.QUALIFIEDINVOICE },
  { title: INVOICE_PURCHASESTATEMENT_TEXT, value: DataType.PURCHASESTATEMENT },
  { title: INVOICE_ITEMIZEDINVOICE_TEXT, value: DataType.ITEMIZEDINVOICE },
] as const

// 請求書PaymentMethod管理
const INVOICE_CREDITTRANSFER_TEXT = '銀行振込'
const INVOICE_DEBITTRANSFER_TEXT = '口座振替'
const INVOICE_CASH_TEXT = '現金'
const INVOICE_DRAFT_TEXT = '手形'
const INVOICE_CREDITCARD_TEXT = 'クレジットカード'
const INVOICE_CHEQUE_TEXT = '小切手'
const INVOICE_CONVENIENCESTORESETTLEMENT_TEXT = 'コンビニ決済'
const INVOICE_OTHER_TEXT = 'その他'
const INVOICE_PaymentMethod_STATUS = [
  { title: INVOICE_CREDITTRANSFER_TEXT, value: PaymentMethod.CREDITTRANSFER },
  { title: INVOICE_DEBITTRANSFER_TEXT, value: PaymentMethod.DEBITTRANSFER },
  { title: INVOICE_CASH_TEXT, value: PaymentMethod.CASH },
  { title: INVOICE_DRAFT_TEXT, value: PaymentMethod.DRAFT },
  { title: INVOICE_CREDITCARD_TEXT, value: PaymentMethod.CREDITCARD },
  { title: INVOICE_CHEQUE_TEXT, value: PaymentMethod.CHEQUE },
  {
    title: INVOICE_CONVENIENCESTORESETTLEMENT_TEXT,
    value: PaymentMethod.CONVENIENCESTORESETTLEMENT,
  },
  { title: INVOICE_OTHER_TEXT, value: PaymentMethod.OTHER },
] as const

// 請求書ステータス管理
const INVOICE_OPEN_TEXT = '開封済'
const INVOICE_UNOPENED_TEXT = '未開封'
const INVOICE_OPEN_STATUS = [
  { title: INVOICE_OPEN_TEXT, value: IsOpen.OPENED },
  { title: INVOICE_UNOPENED_TEXT, value: IsOpen.UNOPENED },
] as const
const INVOICE_CONFIRMED_TEXT = '確認済'
const INVOICE_UNCONFIRMED_TEXT = '未確認'
const INVOICE_CONFIRMATION_STATUS = [
  { title: INVOICE_CONFIRMED_TEXT, value: IsConfirmation.CONFIRMED },
  { title: INVOICE_UNCONFIRMED_TEXT, value: IsConfirmation.UNCONFIRMED },
] as const
const INVOICE_DOWNLOADED_TEXT = 'ダウンロード済み'
const INVOICE_UNDOWNLOADED_TEXT = '未ダウンロード'
const INVOICE_DOWNLOAD_STATUS = [
  { title: INVOICE_DOWNLOADED_TEXT, value: IsDownload.DOWNLOADED },
  { title: INVOICE_UNDOWNLOADED_TEXT, value: IsDownload.UNDOWNLOADED },
] as const

// PDFサイズアイテム管理
const PDF_SIZE_ITEMS = [
  { text: '50%', value: 0.5 },
  { text: '75%', value: 0.75 },
  { text: '100%', value: 1 },
  { text: '125%', value: 1.25 },
  { text: '150%', value: 1.5 },
  { text: '175%', value: 1.75 },
  { text: '200%', value: 2 },
  { text: '225%', value: 2.25 },
  { text: '250%', value: 2.5 },
  { text: '275%', value: 2.75 },
  { text: '300%', value: 3 },
  { text: '325%', value: 3.25 },
  { text: '350%', value: 3.5 },
  { text: '375%', value: 3.75 },
  { text: '400%', value: 4 },
] as const

// ユーザー情報のcookieキー
const COOKIE_LAST_NAME_KEY = 'lastName'
const COOKIE_FIRST_NAME_KEY = 'firstName'
const COOKIE_COMPANY_NAME_KEY = 'companyName'
const COOKIE_USER_ID_KEY = 'userId'

// CSV出力設定ステータス管理
const SETTINGS_CSV_ALL_ITEMS = '全項目（自由選択）'
const SETTINGS_CSV_CREATING_YOUR_OWN_INVOICE =
  '請求書（自社作成）標準フォーマット'
const SETTINGS_CSV_FORMAT_STATUS = [
  {
    title: SETTINGS_CSV_CREATING_YOUR_OWN_INVOICE,
    value: CsvDownloadType.CREATINGYOUROWNINVOICE,
  },
  {
    title: SETTINGS_CSV_ALL_ITEMS,
    value: CsvDownloadType.ALLITEMS,
  },
] as const

// 支払先コードフォームエラーメッセージ
const PEPPOL_ID_ERROR_MESSAGE =
  'Peppol IDを「半角数字4桁:半角英数字」で入力してください'
const PEPPOL_ID_ERROR_MESSAGE_DUPL = 'Peppol IDが重複しています'
const PAYMENT_CODE_ERROR_MESSAGE =
  '支払先コードを「半角英数字15文字以下」で入力してください'

const PEPPOL_ID_PATTERN = /^[0-9]{4}:[0-9a-zA-Z]+$/
const PAYMENT_CODE_PATTERN = /^[0-9a-zA-Z]{1,15}$/

export {
  ROUTE_NAMES,
  CSV_START_DATE_INDEX,
  CSV_START_TIME_INDEX,
  CSV_END_DATE_INDEX,
  CSV_END_TIME_INDEX,
  CSV_TEXT_INDEX,
  JPY_CURRENCY,
  USD_CURRENCY,
  OTHER_CURRENCY_MARK,
  INVOICE_LIST_SIZE,
  INVOICE_LIST_DEFAULT_SIZE,
  INVOICE_LIST_SIZE_STATUS,
  INVOICE_LIST_VALIDATION_MESSAGES,
  INVOICE_DETAIL_TYPE,
  PARTICULARS_TYPE,
  COMMON_TYPE,
  INVOICE_DATA_TYPE_STATUS,
  INVOICE_PaymentMethod_STATUS,
  INVOICE_OPEN_STATUS,
  INVOICE_CONFIRMATION_STATUS,
  INVOICE_DOWNLOAD_STATUS,
  PDF_SIZE_ITEMS,
  COOKIE_LAST_NAME_KEY,
  COOKIE_FIRST_NAME_KEY,
  COOKIE_COMPANY_NAME_KEY,
  COOKIE_USER_ID_KEY,
  SETTINGS_CSV_FORMAT_STATUS,
  PEPPOL_ID_ERROR_MESSAGE,
  PEPPOL_ID_ERROR_MESSAGE_DUPL,
  PAYMENT_CODE_ERROR_MESSAGE,
  PEPPOL_ID_PATTERN,
  PAYMENT_CODE_PATTERN,
}
