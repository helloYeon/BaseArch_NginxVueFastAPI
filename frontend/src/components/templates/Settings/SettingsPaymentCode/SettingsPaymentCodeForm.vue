<template>
  <v-row>
    <v-col>
      <v-row no-gutters class="form">
        <v-col align-self="center">
          <v-row>
            <v-col>
              <label for="peppol-id">Peppol ID</label>
              <v-text-field
                id="peppol-id"
                v-model="peppolIdComputed"
                clearable
                hide-details="auto"
                variant="outlined"
                :error-messages="peppolIdErrorMessage"
                class="form__text-field"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <label for="payment-code">支払先コード</label>
              <v-text-field
                id="payment-code"
                v-model="paymentCodeComputed"
                clearable
                hide-details="auto"
                variant="outlined"
                :error-messages="paymentCodeErrorMessage"
                class="form__text-field"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface SettingsPaymentCodeFormProps {
  peppolId: string
  paymentCode: string
  peppolIdErrorMessage: string
  paymentCodeErrorMessage: string
}
interface SettingsPaymentCodeFormEmits {
  (e: 'update:peppolId', peppolid: string): void
  (e: 'update:paymentCode', paymentCode: string): void
}

const props = defineProps<SettingsPaymentCodeFormProps>()
const emit = defineEmits<SettingsPaymentCodeFormEmits>()

const peppolIdComputed = computed({
  get: () => props.peppolId,
  set: (value) => emit('update:peppolId', value ?? ''),
})
const paymentCodeComputed = computed({
  get: () => props.paymentCode,
  set: (value) => emit('update:paymentCode', value ?? ''),
})
</script>

<style lang="scss" scoped>
.form {
  height: 400px;
  padding: 16px;
  background-color: #fff;
}
</style>
