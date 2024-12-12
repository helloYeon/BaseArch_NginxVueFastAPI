<template>
  <v-row>
    <v-col>
      <v-row no-gutters class="list-content">
        <v-col>
          <v-list
            v-model:selected="selectedUserIdComputed"
            density="compact"
            select-strategy="classic"
            class="list"
          >
            <v-list-item class="list__header">
              <v-row>
                <v-col class="list__header__title" @click="sort">
                  {{ allowUserList ? '利用可能ユーザー' : '利用不可ユーザー' }}
                  <span class="sort" :class="sortClass()">
                    <v-icon end icon="mdi-menu-up menu-up-icon" />
                    <v-icon end icon="mdi-menu-down menu-down-icon" />
                  </span>
                </v-col>
              </v-row>
            </v-list-item>
            <v-divider thickness="3"></v-divider>
            <v-list-item
              v-for="user in users"
              :key="user.userId"
              :value="user"
              density="compact"
              color="primary"
            >
              {{ user.lastName }} {{ user.firstName }}
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { UserAccessItem } from '@/codegen'
import { useAuthUserStore, AuthUserSortOrder } from '@/store/authUser'

interface SettingsAuthListProps {
  users: UserAccessItem[]
  selectedUsers: UserAccessItem[]
  allowUserList: boolean
}
interface SettingsAuthListEmits {
  (e: 'update:selectedUsers', userId: UserAccessItem[]): void
  (e: 'sort'): void
}

const props = defineProps<SettingsAuthListProps>()
const emit = defineEmits<SettingsAuthListEmits>()

const authUserStore = useAuthUserStore()

const selectedUserIdComputed = computed({
  get: () => props.selectedUsers,
  set: (value) => emit('update:selectedUsers', value),
})

// ソート利用時のcss制御
const sortClass = () => {
  if (props.allowUserList) {
    return {
      asc: authUserStore.allowUserListSortOrder === AuthUserSortOrder.ASC,
      desc: authUserStore.allowUserListSortOrder === AuthUserSortOrder.DESC,
    }
  } else {
    return {
      asc: authUserStore.denyUserListSortOrder === AuthUserSortOrder.ASC,
      desc: authUserStore.denyUserListSortOrder === AuthUserSortOrder.DESC,
    }
  }
}

// ソートの値をstoreにセットする
const sort = () => {
  if (props.allowUserList) {
    authUserStore.allowUserListSortOrder =
      authUserStore.allowUserListSortOrder === AuthUserSortOrder.ASC
        ? AuthUserSortOrder.DESC
        : AuthUserSortOrder.ASC
  } else {
    authUserStore.denyUserListSortOrder =
      authUserStore.denyUserListSortOrder === AuthUserSortOrder.ASC
        ? AuthUserSortOrder.DESC
        : AuthUserSortOrder.ASC
  }
  emit('sort')
}
</script>

<style lang="scss" scoped>
.list-content {
  background-color: #fff;
}

.list {
  height: 400px;
  overflow-y: auto;
  &__header {
    &__title {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    .sort {
      display: flex;
      flex-direction: column;
      .menu-up-icon {
        bottom: -6px;
      }
      .menu-down-icon {
        top: -6px;
      }
      &.desc .menu-up-icon {
        opacity: 0.3;
      }
      &.asc .menu-down-icon {
        opacity: 0.3;
      }
    }
  }
}
</style>
