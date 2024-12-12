import { AuthErrorCode } from '@/codegen'
import { defineStore } from 'pinia'

interface ErrorDialog {
  errorDialog: boolean
  authErrorCode?: AuthErrorCode
  receiveApi500Error: boolean
}

export const useErrorDialogStore = defineStore('errorDialog', {
  state: (): ErrorDialog => ({
    errorDialog: false,
    receiveApi500Error: false,
  }),
  getters: {
    getErrorDialog: (state) => state.errorDialog,
  },
  actions: {
    setErrorDialog(errorDialog: boolean) {
      this.errorDialog = errorDialog
    },
  },
})
