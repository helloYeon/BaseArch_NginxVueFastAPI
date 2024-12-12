import { defineStore } from 'pinia'

interface NoticeStore {
  message: string[]
}

export const useNoticeStore = defineStore('notice', {
  state: (): NoticeStore => ({
    message: [],
  }),
  getters: {
    getMessage: (state) => state.message,
  },
  actions: {
    setMessage(message: string) {
      this.message.push(message)
    },
  },
})
