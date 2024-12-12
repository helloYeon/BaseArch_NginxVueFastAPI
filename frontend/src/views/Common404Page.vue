<template>
  <CommonErrorTextContent>
    <p>URLが間違っているか<br />削除された可能性があります。</p>
  </CommonErrorTextContent>
</template>

<script lang="ts" setup>
import CommonErrorTextContent from '@/components/templates/Common/CommonErrorTextContent.vue'
import { useLoadingStore } from '@/store/loading'
const loadingStore = useLoadingStore()
loadingStore.loading = false
</script>
