<template>
  test
  <pre>{{ response }}</pre>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
const response = ref()
onMounted(async () => {
  console.log('api request')
  const apiUrl = import.meta.env.VITE_API_URL
  const res = await fetch(`${apiUrl}/tests/env`, {
    method: 'GET',
  })
  response.value = await res.json()
  console.log(response.value)
})
</script>
