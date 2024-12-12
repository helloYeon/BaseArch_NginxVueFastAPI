import {
  GetInvoicesDataTypeEnum,
  GetInvoicesIsConfirmationEnum,
  GetInvoicesIsDownloadEnum,
  GetInvoicesIsOpenEnum,
  GetInvoicesPaymentMethodEnum,
  GetInvoicesRequest,
  GetInvoicesSortEnum,
  GetInvoicesSortOrderEnum,
} from '@/codegen'
import { defineStore } from 'pinia'
import { useCookies } from 'vue3-cookies'
import { INVOICE_LIST_SIZE, INVOICE_LIST_DEFAULT_SIZE } from '@/const/const'

interface GetInvoicesRequestStore {
  page: number
  size: number
  sort?: GetInvoicesSortEnum
  sortOrder?: GetInvoicesSortOrderEnum
  freeWord?: string
  invNo?: string
  dataType?: GetInvoicesDataTypeEnum
  companyName?: string
  fromIssueDate?: string
  toIssueDate?: string
  payDueDate?: string
  fromInvAmount?: number
  toInvAmount?: number
  paymentMethod?: GetInvoicesPaymentMethodEnum
  isOpen?: GetInvoicesIsOpenEnum
  isDownload?: GetInvoicesIsDownloadEnum
  isConfirmation?: GetInvoicesIsConfirmationEnum
  companyInfosId?: number
  fromReceiveDateTime?: string
  toReceiveDateTime?: string

  requestedPage: number
  requestedSize: number
  requestedSort?: GetInvoicesSortEnum
  requestedSortOrder?: GetInvoicesSortOrderEnum
  requestedFreeWord?: string
  requestedInvNo?: string
  requestedDataType?: GetInvoicesDataTypeEnum
  requestedCompanyName?: string
  requestedFromIssueDate?: string
  requestedToIssueDate?: string
  requestedPayDueDate?: string
  requestedFromInvAmount?: number
  requestedToInvAmount?: number
  requestedPaymentMethod?: GetInvoicesPaymentMethodEnum
  requestedIsOpen?: GetInvoicesIsOpenEnum
  requestedIsDownload?: GetInvoicesIsDownloadEnum
  requestedIsConfirmation?: GetInvoicesIsConfirmationEnum
  requestedCompanyInfosId?: number
  requestedFromReceiveDateTime?: string
  requestedToReceiveDateTime?: string
}

export const useGetInvoicesRequestStore = defineStore('request', {
  state: (): GetInvoicesRequestStore => ({
    page: 1,
    size: Number(useCookies().cookies.get(INVOICE_LIST_SIZE))
      ? Number(useCookies().cookies.get(INVOICE_LIST_SIZE))
      : INVOICE_LIST_DEFAULT_SIZE,
    sort: GetInvoicesSortEnum.INVOICEID,
    sortOrder: GetInvoicesSortOrderEnum.ASC,
    requestedPage: 1,
    requestedSize: Number(useCookies().cookies.get(INVOICE_LIST_SIZE))
      ? Number(useCookies().cookies.get(INVOICE_LIST_SIZE))
      : INVOICE_LIST_DEFAULT_SIZE,
  }),
  getters: {
    // 今回検索条件取得
    getRequest: (state): GetInvoicesRequest => {
      return {
        page: state.page,
        size: state.size,
        sort: state.sort,
        sortOrder: state.sortOrder,
        freeWord: state.freeWord,
        invNo: state.invNo,
        dataType: state.dataType,
        companyName: state.companyName,
        fromIssueDate: state.fromIssueDate,
        toIssueDate: state.toIssueDate,
        payDueDate: state.payDueDate,
        fromInvAmount: state.fromInvAmount,
        toInvAmount: state.toInvAmount,
        paymentMethod: state.paymentMethod,
        isOpen: state.isOpen,
        isDownload: state.isDownload,
        isConfirmation: state.isConfirmation,
        companyInfosId: state.companyInfosId,
        fromReceiveDateTime: state.fromReceiveDateTime,
        toReceiveDateTime: state.toReceiveDateTime,
      }
    },
    // 前回検索条件取得
    getRequested: (state): GetInvoicesRequest => {
      return {
        page: state.requestedPage,
        size: state.requestedSize,
        sort: state.requestedSort,
        sortOrder: state.requestedSortOrder,
        freeWord: state.requestedFreeWord,
        invNo: state.requestedInvNo,
        dataType: state.requestedDataType,
        companyName: state.requestedCompanyName,
        fromIssueDate: state.requestedFromIssueDate,
        toIssueDate: state.requestedToIssueDate,
        payDueDate: state.requestedPayDueDate,
        fromInvAmount: state.requestedFromInvAmount,
        toInvAmount: state.requestedToInvAmount,
        paymentMethod: state.requestedPaymentMethod,
        isOpen: state.requestedIsOpen,
        isDownload: state.requestedIsDownload,
        isConfirmation: state.requestedIsConfirmation,
        companyInfosId: state.requestedCompanyInfosId,
        fromReceiveDateTime: state.requestedFromReceiveDateTime,
        toReceiveDateTime: state.requestedToReceiveDateTime,
      }
    },
  },
  actions: {
    // 今回検索条件に前回検索条件をセット
    setRequest() {
      this.page = this.requestedPage
      this.size = this.requestedSize
      this.sort = this.requestedSort
      this.sortOrder = this.requestedSortOrder
      this.freeWord = this.requestedFreeWord
      this.invNo = this.requestedInvNo
      this.dataType = this.requestedDataType
      this.companyName = this.requestedCompanyName
      this.fromIssueDate = this.requestedFromIssueDate
      this.toIssueDate = this.requestedToIssueDate
      this.payDueDate = this.requestedPayDueDate
      this.fromInvAmount = this.requestedFromInvAmount
      this.toInvAmount = this.requestedToInvAmount
      this.paymentMethod = this.requestedPaymentMethod
      this.isOpen = this.requestedIsOpen
      this.isDownload = this.requestedIsDownload
      this.isConfirmation = this.requestedIsConfirmation
      this.companyInfosId = this.requestedCompanyInfosId
      this.fromReceiveDateTime = this.requestedFromReceiveDateTime
      this.toReceiveDateTime = this.requestedToReceiveDateTime
    },
    // 前回検索条件に今回検索条件をセット
    setRequested() {
      this.requestedPage = this.page
      this.requestedSize = this.size
      this.requestedSort = this.sort
      this.requestedSortOrder = this.sortOrder
      this.requestedFreeWord = this.freeWord
      this.requestedInvNo = this.invNo
      this.requestedDataType = this.dataType
      this.requestedCompanyName = this.companyName
      this.requestedFromIssueDate = this.fromIssueDate
      this.requestedToIssueDate = this.toIssueDate
      this.requestedPayDueDate = this.payDueDate
      this.requestedFromInvAmount = this.fromInvAmount
      this.requestedToInvAmount = this.toInvAmount
      this.requestedPaymentMethod = this.paymentMethod
      this.requestedIsOpen = this.isOpen
      this.requestedIsDownload = this.isDownload
      this.requestedIsConfirmation = this.isConfirmation
      this.requestedCompanyInfosId = this.companyInfosId
      this.requestedFromReceiveDateTime = this.fromReceiveDateTime
      this.requestedToReceiveDateTime = this.toReceiveDateTime
    },
  },
})
