<template>
  <v-dialog v-model="isActiveComputed" min-width="30%" width="unset">
    <CommonErrorDialogCard
      v-if="
        !errorDialogStore.authErrorCode && !errorDialogStore.receiveApi500Error
      "
      card-text="入力内容に不備があります"
      @dialog-button="emit('closeDialog')"
    />
    <CommonErrorDialogCard
      v-if="errorDialogStore.authErrorCode === AuthErrorCode.E9013"
      card-text="セッションがタイムアウトされました"
      button-text="再ログインする"
      @dialog-button="transitionLogin"
    />
    <CommonErrorDialogCard
      v-if="errorDialogStore.authErrorCode === AuthErrorCode.E9014"
      card-text="パスワードの有効期限が切れました"
      button-text="パスワードを変更する"
      @dialog-button="transitionPassword"
    />
    <CommonErrorDialogCard
      v-if="errorDialogStore.authErrorCode === AuthErrorCode.E9015"
      card-text="ログアウトされました"
      button-text="再ログインする"
      @dialog-button="transitionLogin"
    />
    <CommonErrorDialogCard
      v-if="errorDialogStore.receiveApi500Error"
      card-text="エラーが発生しました。再度お試しください。"
      @dialog-button="emit('closeDialog')"
    />
  </v-dialog>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import CommonErrorDialogCard from './CommonErrorDialogCard.vue'
import { useErrorDialogStore } from '@/store/errorDialog'
import { AuthErrorCode } from '@/codegen'
import { transitionLogin, transitionPassword } from '@/plugins/utils'

interface DialogProps {
  isActive: boolean
}

interface DialogEmits {
  (e: 'update:isActive', isActive: boolean): void
  (e: 'closeDialog'): void
}

const props = defineProps<DialogProps>()
const emit = defineEmits<DialogEmits>()

const errorDialogStore = useErrorDialogStore()

const isActiveComputed = computed({
  get: () => props.isActive,
  set: (value: boolean) => {
    emit('update:isActive', value)
  },
})
</script>

<style lang="scss" scoped>
.card {
  color: #222222;
}
</style>
