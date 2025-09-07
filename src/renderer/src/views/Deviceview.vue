<script setup lang="ts">
import ExperimentCard from '@/components/ExperimentCard.vue'
import { useDeviceStore } from '@/stores/device'
import { DeviceInfo } from '@/types/device'
import { useRoute } from 'vue-router'
const route = useRoute()
const address = route.params.address as string

const deviceStore = useDeviceStore()
const device = deviceStore.getDevice(address) as DeviceInfo
</script>

<template>
  <ExperimentCard :device="device" />
</template>
