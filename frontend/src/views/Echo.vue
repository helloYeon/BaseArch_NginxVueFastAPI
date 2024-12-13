<template>
  echo
  <pre>{{ response }}</pre>
  <a href="echo"></a>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

console.log(route.query)
const response = ref()
onMounted(async () => {
  console.log('api request')

  // クエリパラメータを取得
  const queryParams = route.query
  const apiUrl = import.meta.env.VITE_API_URL

  // クエリパラメータをURLに追加
  const queryString = new URLSearchParams(
    queryParams as Record<string, string>
  ).toString()

  const requestUrl = `${apiUrl}/tests/echo?${queryString}`
  console.log(`Request URL: ${requestUrl}`)
  // APIリクエストの送信
  const res = await fetch(requestUrl, {
    method: 'GET',
  })
  response.value = await res.json()
  console.log(response.value)
})
</script>
