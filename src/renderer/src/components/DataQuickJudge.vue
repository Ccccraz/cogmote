<script setup lang="ts">
import { Separator } from '@/components/ui/separator'
import Badge from './ui/badge/Badge.vue'
import { computed } from 'vue'
import { useTrialDataStore } from '@/stores/trialData'
import { useDeviceStore } from '@/stores/device'

const props = defineProps<{
  address: string
}>()

const trialDataStore = useTrialDataStore()
const deviceStore = useDeviceStore()

trialDataStore.connectSSE(props.address)

const latestData = computed(() => {
  const trialData = trialDataStore.getChannelData(props.address)
  const lastItem = trialData[trialData.length - 1]

  return lastItem
    ? {
        trialID: lastItem['trial_id'],
        correctRate: lastItem['correct_rate']
      }
    : null
})

const correctRateShow = computed(() => Math.round(latestData.value?.correctRate * 100))
const hostname = computed(() => deviceStore.getDevice(props.address)?.device.hostname)
</script>

<template>
  <div class="bg-muted/50 rounded-xl border h-fit p-4 flex flex-col">
    <Badge>{{ hostname }}</Badge>
    <div class="flex justify-center items-center h-24 gap-2 my-auto">
      <div v-if="latestData?.trialID < 10" class="text-8xl font-bold text-red-400">
        {{ latestData?.trialID }}
      </div>
      <div v-else class="text-8xl font-bold text-green-400">
        {{ latestData?.trialID }}
      </div>
      <Separator orientation="vertical" />
      <div v-if="latestData?.correctRate < 50" class="text-8xl font-bold text-red-400">
        {{ correctRateShow }}
      </div>
      <div v-else class="text-8xl font-bold text-green-400">
        {{ correctRateShow }}
      </div>
    </div>
  </div>
</template>
