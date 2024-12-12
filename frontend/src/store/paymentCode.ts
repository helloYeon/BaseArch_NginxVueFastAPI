import { defineStore } from 'pinia'

export enum PaymentCodeSort {
  PeppolId = 'peppolId',
  PaymentCode = 'paymentCode',
}

export enum PaymentCodeSortOrder {
  ASC = 0,
  DESC = 1,
}

interface PaymentCodeStore {
  companyInfosId?: number
  sort: PaymentCodeSort
  sortOrder: PaymentCodeSortOrder
}

export const usePaymentCodeStore = defineStore('paymentCode', {
  state: (): PaymentCodeStore => ({
    sort: PaymentCodeSort.PeppolId,
    sortOrder: PaymentCodeSortOrder.ASC,
  }),
})
