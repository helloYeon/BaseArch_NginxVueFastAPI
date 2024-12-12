<template>
  <v-btn
    class="icon ml-1 mr-1"
    height="28px"
    min-width="24px"
    rounded="sm"
    :title="title"
    :disabled="apiProgressStore.download"
    variant="plain"
  >
    <v-icon :icon="icon" size="20" color="#f9f9fa" />
  </v-btn>
</template>

<script lang="ts" setup>
import { useApiProgressStore } from '@/store/apiProgress'

interface PreviewIconButtonProps {
  title: string
  icon: string
}

defineProps<PreviewIconButtonProps>()

const apiProgressStore = useApiProgressStore()
</script>
