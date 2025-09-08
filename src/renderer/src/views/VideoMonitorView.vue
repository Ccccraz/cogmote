<script setup lang="ts">
import Badge from '@/components/ui/badge/Badge.vue'
import VideoMonitor from '@/components/VideoMonitor.vue'
import { useDeviceStore } from '@/stores/device'

const deviceStore = useDeviceStore()
</script>

<template>
  <div class="w-full h-svh overflow-y-auto">
    <div class="grid grid-cols-3 justify-items-center p-4 gap-4">
      <div
        v-for="[address] in deviceStore.devices"
        :key="`video-monitor-view-${address}`"
        class="w-full aspect-16/9 flex flex-col gap-4 p-4 bg-muted/50 border rounded-xl"
      >
        <Badge>{{ deviceStore.getDevice(`${address}`)?.device.hostname }}</Badge>
        <VideoMonitor class="w-full h-full" :address="`${address}`" />
      </div>
    </div>
  </div>
</template>
