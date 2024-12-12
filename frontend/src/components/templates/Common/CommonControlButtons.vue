<template>
  <v-row>
    <v-col>
      <v-btn class="button" variant="outlined" @click="emit('add')">
        ← 追加
      </v-btn>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-btn class="button mt-2" variant="outlined" @click="emit('delete')">
        削除 →
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
interface SettingsAuthEmits {
  (e: 'add'): void
  (e: 'delete'): void
}

const emit = defineEmits<SettingsAuthEmits>()
</script>

<style lang="scss" scoped>
.button {
  font-size: 2rem;
  font-weight: bold;
  color: #222222;
  height: 60px;
  width: 200px;
  background-color: #ffffff;
}
</style>
