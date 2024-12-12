<template>
  <v-app>
    <component :is="$route.meta.layout || 'div'">
      <router-view />
    </component>
  </v-app>
</template>

<script setup lang="ts"></script>
