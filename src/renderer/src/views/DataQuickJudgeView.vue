<script setup lang="ts">
import DataQuickJudge from '@/components/DataQuickJudge.vue'
import { useDeviceStore } from '@/stores/device'
const deviceStore = useDeviceStore()
</script>

<template>
  <div class="w-full h-svh overflow-y-auto">
    <div class="grid grid-cols-3 gap-4 p-4">
      <DataQuickJudge
        v-for="[address, device] in deviceStore.devices"
        :key="`data-quick-judge-${address}`"
        :hostname="`${device.device.hostname}`"
        :trial-id="120"
        :correct-rate="48.5"
      />
    </div>
  </div>
</template>
