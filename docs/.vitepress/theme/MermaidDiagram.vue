<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'

const props = defineProps<{ code: string }>()
const container = ref<HTMLElement | null>(null)

onMounted(async () => {
  const mermaid = (await import('mermaid')).default
  mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'neutral' })
  await nextTick()
  const id = `mermaid-${Math.random().toString(36).slice(2)}`
  const source = decodeURIComponent(props.code)
  const { svg } = await mermaid.render(id, source)
  if (container.value) container.value.innerHTML = svg
})
</script>

<template>
  <div ref="container" class="mermaid-diagram" role="img" aria-label="流程图" />
</template>
