<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  address?: string
}>()

const webrtcUrl = computed(() => `http://${props.address}:8889/mystream/`)
</script>

<template>
  <iframe class="pointer-events-none" :src="webrtcUrl" scrolling="no"></iframe>
</template>
