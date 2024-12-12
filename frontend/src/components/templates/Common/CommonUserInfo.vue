<template>
  <v-card class="user-info">
    <v-card-text class="user-info__company">
      {{ userStore.companyName }}
    </v-card-text>
    <v-card-text class="user-info__name">
      {{ `${userStore.lastName} ${userStore.firstName}` }}
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import { setUserInfo } from '@/plugins/utils'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

setUserInfo()
</script>

<style lang="scss" scoped>
.user-info {
  padding: 16px;
  text-align: center;
  border: 1px solid #b11048;

  &__company {
    font-size: 1.4rem;
    font-weight: bold;
    color: #222222;
  }

  &__name {
    font-size: 1.4rem;
    font-weight: bold;
    color: #b11048;
  }
}
</style>
