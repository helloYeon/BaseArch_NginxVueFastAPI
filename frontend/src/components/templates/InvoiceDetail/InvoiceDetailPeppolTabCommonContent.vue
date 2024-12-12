<template>
  <v-expansion-panels
    v-model="panel"
    multiple
    selected-class=".selected"
    class="mt-8"
  >
    <v-expansion-panel>
      <v-expansion-panel-title
        color="#F7EFEF"
        expand-icon="mdi-plus"
        collapse-icon="mdi-minus"
        class="title"
      >
        <p class="title__text">{{ title }}</p>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <slot />
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

interface PeppolCommonContentProps {
  title: string
}

defineProps<PeppolCommonContentProps>()

const panel = ref([0])
</script>

<style lang="scss" scoped>
.title {
  font-size: 1.4rem;
  font-weight: bold;

  &__text {
    color: #222222;
  }
}

.v-expansion-panel-title--active {
  :deep(.v-expansion-panel-title__overlay) {
    opacity: 0;
  }
}
</style>
