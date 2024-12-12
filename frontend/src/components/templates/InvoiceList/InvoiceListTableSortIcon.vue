<template>
  <div class="d-flex flex-column">
    <v-icon icon="mdi-menu-up menu-up-icon" />
    <v-icon icon="mdi-menu-down menu-down-icon" />
  </div>
</template>

<style lang="scss" scoped>
.menu-up-icon {
  bottom: -5px;
}
.menu-down-icon {
  top: -5px;
}
.desc .menu-up-icon {
  opacity: 0.3;
}
.asc .menu-down-icon {
  opacity: 0.3;
}
</style>
