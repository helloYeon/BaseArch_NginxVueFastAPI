<template>
  <v-snackbar
    v-model="snackbar"
    location="bottom right"
    origin="bottom right"
    :timeout="-1"
    outlined
  >
    <template v-if="status">
      <div @click="status = csvDownloadStatus.done">処理中です...</div>
    </template>
    <template v-else>
      完了しました
      <a class="link" @click="downloadFile">リンク</a>
    </template>
  </v-snackbar>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const csvDownloadStatus = {
  do: 1,
  done: 0,
} as const

const snackbar = ref(true)
const status = ref<0 | 1>(csvDownloadStatus.do)

// ファイルダウンロード
const downloadFile = () => {
  snackbar.value = false
}
</script>

<style lang="scss" scoped>
.link {
  font-weight: bold;
  color: #b11048;
  cursor: pointer;
}
</style>
