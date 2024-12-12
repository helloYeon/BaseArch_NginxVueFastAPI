<template>
  <CommonErrorTextContent>
    <p>認証・ユーザ情報取得に失敗しました。</p>
  </CommonErrorTextContent>
</template>

<script lang="ts" setup>
import CommonErrorTextContent from '@/components/templates/Common/CommonErrorTextContent.vue'
import { useLoadingStore } from '@/store/loading'
const loadingStore = useLoadingStore()
loadingStore.loading = false
</script>
