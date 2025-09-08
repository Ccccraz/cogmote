<script setup lang="ts">
import { useDeviceStore } from '@/stores/device'
import { RouterLink } from 'vue-router'

defineProps<{
  address: string
}>()

const deviceStore = useDeviceStore()
</script>

<template>
  <div class="flex flex-col gap-2 p-2">
    <template v-for="[target, device] in deviceStore.devices" :key="`device-list-${target}`">
      <RouterLink
        v-if="device.status != 'offline'"
        class="hover:bg-accent p-4 border rounded-xl"
        :class="{ 'bg-accent': target === address }"
        :to="`/device/${target}`"
      >
        {{ target }}
      </RouterLink>
    </template>
  </div>
</template>
