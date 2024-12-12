<template>
  <div v-show="!loadingStore.loading" :key="$route.fullPath">
    <CommonHeader />
    <v-main>
      <CommonNotice />
      <slot />
    </v-main>
    <!-- TODO: 仮実装モック状態 -->
    <CommonSnackBar v-if="isLocal() || isDevelopment()" />
  </div>

  <CommonLoadingOverlay v-if="loadingStore.loading" />
</template>

<script lang="ts" setup>
import CommonHeader from '@/components/templates/Common/CommonHeader.vue'
import CommonNotice from '@/components/templates/Common/CommonNotice.vue'
import CommonSnackBar from '@/components/templates/Common/CommonSnackBar.vue'
import CommonLoadingOverlay from '@/components/templates/Common/CommonLoadingOverlay.vue'
import { useLoadingStore } from '@/store/loading'
import { isDevelopment, isLocal } from '@/utils'

const loadingStore = useLoadingStore()
</script>
