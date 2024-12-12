import { defineStore } from 'pinia'

interface UserStore {
  lastName: string
  firstName: string
  companyName: string
  userId: number
}

export const useUserStore = defineStore('user', {
  state: (): UserStore => ({
    lastName: '',
    firstName: '',
    companyName: '',
    userId: 0,
  }),
})
