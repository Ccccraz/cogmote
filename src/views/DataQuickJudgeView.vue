<script setup lang="ts">
import DataQuickJudge from "@/components/DataQuickJudge.vue";
import { useDeviceStore } from "@/stores/device";
const deviceStore = useDeviceStore();
</script>

<template>
  <div class="w-full h-svh overflow-y-auto">
    <div class="grid grid-cols-3 gap-4 p-4">
      <template v-for="[_, device] in deviceStore.devices">
        <DataQuickJudge
          :hostname="`${device.device.hostname}`"
          :trialID="120"
          :correctRate="48.5"
        />
      </template>
    </div>
  </div>
</template>
