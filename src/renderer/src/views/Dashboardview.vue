<script setup lang="ts">
import VideoMonitor from '@/components/VideoMonitor.vue'
import DataQuickJudge from '@/components/DataQuickJudge.vue'
import LinePlotter from '@/components/LinePlotter.vue'
import TrialDataMonitor from '@/components/TrialDataMonitor.vue'
import { useDeviceStore } from '@/stores/device'
import { DeviceInfo } from '@/types/device'

const props = defineProps<{
  address: string
}>()

const deviceStore = useDeviceStore()
const device = deviceStore.getDevice(props.address) as DeviceInfo
</script>

<template>
  <div class="flex-1 grid grid-cols-4 grid-rows-4 gap-4 p-4">
    <DataQuickJudge
      :key="`dashboard-quick-judge-${address}`"
      class="w-full h-full row-start-1 row-end-2 col-start-1 col-end-2"
      :address="address"
    />
    <LinePlotter
      :key="`dashboard-line-plotter-${address}`"
      class="w-full h-full row-start-2 row-end-4 col-start-1 col-end-2"
    />
    <VideoMonitor
      :key="`dashboard-video-monitor-${address}`"
      class="w-full h-full row-start-1 row-end-4 col-start-2 col-end-5 rounded-xl border bg-muted/50"
      :address="device?.address"
    />
    <TrialDataMonitor
      :key="`dashboard-data-monitor-${address}`"
      class="col-start-1 col-end-5 row-start-4"
      :device="device"
    />
  </div>
</template>
