<template>
  <div class="error-text">
    <v-icon icon="mdi-alert-outline" size="80" class="mb-4" />
    <slot />
  </div>
</template>

<style lang="scss" scoped>
.error-text {
  font-size: 2.4rem;
  font-weight: bold;
  color: #222222;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateY(-50%) translateX(-50%);
}
</style>
