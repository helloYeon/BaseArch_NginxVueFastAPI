<template>
  <h1 class="title">{{ title }}</h1>
</template>

<script lang="ts" setup>
defineProps<{
  title: string
}>()
</script>

<style lang="scss" scoped>
.title {
  border-bottom: 2px solid #22222280;
  color: #222222;
  font-size: 2rem;
  font-weight: bold;
  line-height: 2;
}
</style>
