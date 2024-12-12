<template>
  <v-container>
    <PageTitle title="権限設定" />
    <v-row class="setting-auth">
      <v-col>
        <SettingsAuthList
          v-model:selected-users="selectedAllowUsers"
          :users="accessAllowUsers"
          allow-user-list
          @sort="emit('allowUserListSort')"
        />
      </v-col>

      <v-col align-self="center" cols="auto">
        <CommonControlButtons @add="addUser" @delete="deleteUser" />
      </v-col>

      <v-col>
        <SettingsAuthList
          v-model:selected-users="selectedDenyUsers"
          :users="accessDenyUsers"
          :allow-user-list="false"
          @sort="emit('dennyUserListSort')"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { IsDeny, UserAccessItem } from '@/codegen'
import PageTitle from '@/components/parts/PageTitle.vue'
import SettingsAuthList from '@/components/templates/Settings/SettingsAuth/SettingsAuthList.vue'
import CommonControlButtons from '@/components/templates/Common/CommonControlButtons.vue'

interface SettingsAuthProps {
  accessAllowUsers: UserAccessItem[]
  accessDenyUsers: UserAccessItem[]
}

interface SettingsAuthEmits {
  (e: 'update:accessAllowUsers', accessAllowUsers: UserAccessItem[]): void
  (e: 'update:accessDenyUsers', accessDenyUsers: UserAccessItem[]): void
  (e: 'allowUserListSort'): void
  (e: 'dennyUserListSort'): void
}

const props = defineProps<SettingsAuthProps>()
const emit = defineEmits<SettingsAuthEmits>()

const selectedAllowUsers = ref<UserAccessItem[]>([])
const selectedDenyUsers = ref<UserAccessItem[]>([])

const accessAllowUsersComputed = computed({
  get: () => props.accessAllowUsers,
  set: (value) => emit('update:accessAllowUsers', value),
})
const accessDenyUsersComputed = computed({
  get: () => props.accessDenyUsers,
  set: (value) => emit('update:accessDenyUsers', value),
})

// 利用不可配列から利用可能配列に追加
const addUser = () => {
  if (!selectedDenyUsers.value.length) return

  const updateList = accessDenyUsersComputed.value.filter(
    (user) =>
      !selectedDenyUsers.value.some((selectedUser) => selectedUser === user)
  )

  accessDenyUsersComputed.value = updateList

  // ユーザーを利用可能配列に追加
  selectedDenyUsers.value.forEach((user) =>
    accessAllowUsersComputed.value.unshift({ ...user, isDeny: IsDeny.IS_ALLOW })
  )

  selectedDenyUsers.value = []
}

// 利用可能配列から利用不可配列に追加
const deleteUser = () => {
  if (!selectedAllowUsers.value.length) return

  const updateList = accessAllowUsersComputed.value.filter(
    (user) =>
      !selectedAllowUsers.value.some((selectedUser) => selectedUser === user)
  )

  accessAllowUsersComputed.value = updateList

  // ユーザーを利用不可配列に追加
  selectedAllowUsers.value.forEach((user) =>
    accessDenyUsersComputed.value.unshift({ ...user, isDeny: IsDeny.IS_DENY })
  )

  selectedAllowUsers.value = []
}
</script>

<style lang="scss" scoped>
.setting-auth {
  background-color: #cccccc;
  margin: 32px 0 0;
}
</style>
