import { defineStore } from 'pinia'

export enum AuthUserSortOrder {
  ASC = 0,
  DESC = 1,
}

interface AuthUserStore {
  allowUserListSortOrder: AuthUserSortOrder
  denyUserListSortOrder: AuthUserSortOrder
}

export const useAuthUserStore = defineStore('authUser', {
  state: (): AuthUserStore => ({
    allowUserListSortOrder: AuthUserSortOrder.ASC,
    denyUserListSortOrder: AuthUserSortOrder.ASC,
  }),
})
