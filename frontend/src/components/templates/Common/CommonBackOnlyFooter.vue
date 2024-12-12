<template>
  <v-footer elevation="4" app class="footer">
    <v-container>
      <v-row>
        <v-col>
          <BackButton />
        </v-col>
      </v-row>
    </v-container>

    <v-divider />

    <CommonCopyright />
  </v-footer>
</template>

<script lang="ts" setup>
import CommonCopyright from '@/components/templates/Common/CommonCopyright.vue'
import BackButton from '@/components/parts/BackButton.vue'
</script>

<style lang="scss" scoped>
.footer {
  display: block;
  padding: 0;
  border-top: 1px solid #e0e0e0;
  min-width: 727px;
}
</style>
