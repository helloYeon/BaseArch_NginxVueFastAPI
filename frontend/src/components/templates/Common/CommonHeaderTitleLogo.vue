<template>
  <v-sheet width="240" class="header__logo">
    <v-img src="@/assets/logo_b2bpf.png" />
  </v-sheet>
  <v-list-item class="header__title">Peppol連携 受取</v-list-item>
</template>

<style lang="scss" scoped>
.header {
  &__logo {
    margin: 8px auto 0;
  }

  &__title {
    margin-top: 4px;
    font-size: 2.4rem;
    font-weight: bold;
    color: #222222;
    text-align: center;
  }
}
</style>
