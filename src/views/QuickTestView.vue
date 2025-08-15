<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { useTrialDataStore } from "@/stores/trialData";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const channel = "default"

const trialDataStore = useTrialDataStore();
const connect = async () => {
  try {
    await trialDataStore.connectSSE(
      route.params.address as string,
      channel,
    )
  } catch (err) {
    console.error('failed to connect to device: ', err)
  }
}

const trialData = computed(() => 
  trialDataStore.getChannelData(route.params.address as string, channel)
);

</script>

<template>
  <div class="w-full h-svh overflow-y-auto flex justify-center items-center">
    <Button @click="connect">Get</Button>
    <div v-for="data in trialData" :key="data.id">
      {{ data }}
    </div>
  </div>
</template>
