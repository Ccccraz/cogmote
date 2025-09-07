<script setup lang="ts">
import { Separator } from '@/components/ui/separator'
import Badge from './ui/badge/Badge.vue'
import { computed } from 'vue'
const props = defineProps<{
  hostname?: string
  trialId: number
  correctRate: number
}>()

const correctRateShow = computed(() => Math.round(props.correctRate * 100))
</script>

<template>
  <div class="bg-muted/50 rounded-xl border h-fit p-4 flex flex-col">
    <Badge>{{ hostname }}</Badge>
    <div class="flex justify-center items-center h-24 gap-2 my-auto">
      <div v-if="trialId < 10" class="text-8xl font-bold text-red-400">
        {{ trialId }}
      </div>
      <div v-else class="text-8xl font-bold text-green-400">
        {{ trialId }}
      </div>
      <Separator orientation="vertical" />
      <div v-if="correctRate < 50" class="text-8xl font-bold text-red-400">
        {{ correctRateShow }}
      </div>
      <div v-else class="text-8xl font-bold text-green-400">
        {{ correctRateShow }}
      </div>
    </div>
  </div>
</template>
