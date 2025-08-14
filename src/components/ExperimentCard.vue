<script setup lang="ts">
import { useExperimentStore } from "@/stores/experiment";
import { DeviceInfo } from "@/types/device";

const props = defineProps<{
  device: DeviceInfo;
}>();

const experimentStore = useExperimentStore();

experimentStore.fetchExperiments(props.device.address);
</script>

<template>
  <div>
    <div v-for="experimentRecord in experimentStore.experimentRecords">
      {{ experimentRecord.experiment.nickname }}
    </div>
  </div>
</template>
