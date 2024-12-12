<template>
  <v-footer elevation="4" app class="footer">
    <v-container>
      <v-row justify="end">
        <v-col cols="auto">
          <CommonFixedFooterButtons
            :is-hidden-cancel-button="isHiddenCancelButton"
            @cancel-event="emit('cancelEvent')"
            @save-event="emit('saveEvent')"
          />
        </v-col>
      </v-row>
    </v-container>

    <v-divider />

    <CommonCopyright />
  </v-footer>
</template>

<script lang="ts" setup>
import CommonCopyright from '@/components/templates/Common/CommonCopyright.vue'
import CommonFixedFooterButtons from './CommonFixedFooterButtons.vue'

interface CommonFixedFooterProps {
  isHiddenCancelButton: boolean
}

interface CommonFixedFooterEmits {
  (e: 'cancelEvent'): void
  (e: 'saveEvent'): void
}

defineProps<CommonFixedFooterProps>()
const emit = defineEmits<CommonFixedFooterEmits>()
</script>

<style lang="scss" scoped>
.footer {
  display: block;
  padding: 0;
  border-top: 1px solid #e0e0e0;
  min-width: 727px;
}
</style>
