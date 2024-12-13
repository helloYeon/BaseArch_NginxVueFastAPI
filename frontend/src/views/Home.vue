<template>
  test
  <pre>{{ response }}</pre>
  <button @click="getEcho">button</button>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const response = ref()

const getEcho = () => {
  router.push({
    path: '/echo',
    query: {
      hoge: 'test',
      piyo: 'test2',
    },
  })
}

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
