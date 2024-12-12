import {
  INVOICE_DATA_TYPE_STATUS,
  INVOICE_PaymentMethod_STATUS,
  JPY_CURRENCY,
  OTHER_CURRENCY_MARK,
  ROUTE_NAMES,
  USD_CURRENCY,
} from '@/const/const'
import router from '@/router'
import { format, formatDistanceToNowStrict } from 'date-fns'
import { ja } from 'date-fns/locale'
import type { Locale, LocalizedOptions } from 'date-fns/types.js'
import { useUserStore } from '@/store/user'
import { useCookies } from 'vue3-cookies'
import {
  COOKIE_LAST_NAME_KEY,
  COOKIE_FIRST_NAME_KEY,
  COOKIE_COMPANY_NAME_KEY,
  COOKIE_USER_ID_KEY,
} from '@/const/const'
import { useErrorDialogStore } from '@/store/errorDialog'
import { useGetInvoicesRequestStore } from '@/store/getInvoicesRequest'
import { AuthErrorCode } from '@/codegen'
import { useLoadingStore } from '@/store/loading'

/**
 * ロケールを指定するためのオプション
 *
 * @type {LocalizedOptions<keyof Locale>}
 */
const option: LocalizedOptions<keyof Locale> = { locale: ja }

/**
 * 現在の日付時刻を取得
 *
 * @export
 * @return {string} 現在の日付と時刻
 */
export function getCurrentDateTime(): string {
  return format(new Date(), 'yyyyMMddHHmmss', option)
}

/**
 * 日付フォーマット変換
 * 何もない場合は空文字を返す
 *
 * @export
 * @param {(Date | string | null | undefined)} date 変換前日付
 * @param {string} [formatStr='yyyy/MM/dd'] 変換する文字列(Default: yyyy/MM/dd)
 * @return {string} 変換後日付または空文字
 */
export function formatDate(
  date: Date | string | null | undefined,
  formatStr: string = 'yyyy/MM/dd'
): string {
  if (!date) return ''
  return format(date, formatStr, option)
}

/**
 * 数字を文字列型の数字に変換
 * 何もない場合は空文字を返す
 *
 * @export
 * @param {(number | null | undefined)} num 数字
 * @return {string} 文字列型の数字または空文字
 */
export function numToStrNum(num: number | null | undefined): string {
  return num?.toLocaleString() ?? ''
}

/**
 * 文字列の数値をカンマ付き数値に変換
 * 何もない場合は空文字を返す
 *
 * @export
 * @param {(string | null | undefined)} strNum 文字列型の数字
 * @returns {string} カンマ付き文字列型数値または空文字
 */
export function strNumToLocaleStringNum(
  strNum: string | null | undefined
): string {
  if (!strNum) return ''
  return Number(strNum).toLocaleString()
}

/**
 * 請求書タイプ名取得
 *
 * @export
 * @param {number} dataTypeValue 請求書タイプ
 * @return {string} 請求書タイプ名
 */
export function dataTypeTitle(dataTypeValue: number): string {
  return (
    INVOICE_DATA_TYPE_STATUS.find(
      (dataType) => dataType.value === dataTypeValue
    )?.title ?? ''
  )
}

/**
 * 支払方法名取得
 *
 * @export
 * @param {(number | null)} paymentMethodValue 支払方法
 * @return {string} 支払方法名
 */
export function paymentMethodTitle(paymentMethodValue: number | null): string {
  return (
    INVOICE_PaymentMethod_STATUS.find(
      (paymentMethod) => paymentMethod.value === paymentMethodValue
    )?.title ?? ''
  )
}

/**
 * Cookieのユーザー情報をuserStoreにセットする
 *
 * @export
 */
export async function setUserInfo() {
  const cookies = useCookies().cookies
  const userStore = useUserStore()

  // ユーザー情報セット
  userStore.lastName = cookies.get(COOKIE_LAST_NAME_KEY) ?? ''
  userStore.firstName = cookies.get(COOKIE_FIRST_NAME_KEY) ?? ''
  userStore.companyName = cookies.get(COOKIE_COMPANY_NAME_KEY) ?? ''
  userStore.userId = Number(cookies.get(COOKIE_USER_ID_KEY)) || 0
}

/**
 * Blob形式のファイルのダウンロードを行う
 *
 * @export
 * @param {Blob} file ファイルの中身
 * @param {string} fileName ファイル名
 */
export function createDownloadFile(file: Blob, fileName: string) {
  const url = window.URL.createObjectURL(file)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  link.click()
}

/**
 * 引数と現在時間からの距離を取得する
 *
 * @export
 * @param {string} date 任意の日付に変換できる文字列
 * @returns {string} 'yyyy/MM/dd HH:mm（○○秒前・○○分前・○○日前・○○か月前・○○年前）
 */
export function getDistanceToNow(date: string): string {
  if (!date) return ''
  return `${formatDate(date, 'yyyy/MM/dd HH:mm')}（${formatDistanceToNowStrict(date, { ...option, addSuffix: true })}）`
}

/**
 * 外部のログインブリッジエンドポイントへ遷移する
 *
 * @export
 */
export function transitionLogin() {
  window.location.href = import.meta.env.VITE_LOGIN_BRIDGE_URL
}

/**
 * 外部のパスワード変更画面へ遷移する
 *
 * @export
 */
export function transitionPassword() {
  window.location.href = import.meta.env.VITE_CHANGE_PASSWORD_URL
}

/**
 * エラーモーダルを開く
 *
 * @export
 * @param {?AuthErrorCode} [code] 認証系エラーコード
 */
export function openErrorDialog(code?: AuthErrorCode) {
  const loaderStore = useLoadingStore()
  const errorDialogStore = useErrorDialogStore()
  const requestStore = useGetInvoicesRequestStore()

  loaderStore.loading = false
  errorDialogStore.authErrorCode = code
  errorDialogStore.setErrorDialog(true)
  requestStore.$reset()
  router.push({ name: ROUTE_NAMES.INVOICE_LIST })
}

/**
 * 請求書通貨コードから通貨記号を取得する
 *
 * @export
 * @param {string} currencyCode 通貨コード
 * @returns {string} 通貨記号(JPY: ¥, USD: $, その他: (外貨))
 */
export function currencyMark(currencyCode: string): string {
  if (currencyCode === JPY_CURRENCY.CODE) return JPY_CURRENCY.MARK
  if (currencyCode === USD_CURRENCY.CODE) return USD_CURRENCY.MARK
  return OTHER_CURRENCY_MARK
}

/**
 * 請求書通貨コード込み通貨を表示する
 *
 * @export
 * @param {string} currencyCode 通貨コード
 * @param {(number | null | undefined)} item 数字
 * @returns {string} 通貨記号(JPY: ¥, USD: $, その他: (外貨)) + 金額
 */
export function formatPrice(
  currencyCode: string,
  item: number | null | undefined
): string {
  return currencyMark(currencyCode) + numToStrNum(item)
}
