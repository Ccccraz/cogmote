<script setup lang="ts">
import { useDeviceStore } from "@/stores/device";
import DeviceCard from "@/components/DeviceCard.vue";
import { Plus } from "lucide-vue-next";
import DetectCogmoteGODialog from "@/components/DetectCogmoteGODialog.vue";

import { Button } from "@/components/ui/button";

const deviceStore = useDeviceStore();
</script>

<template>
  <div class="flex-1 flex flex-col">
    <div
      class="m-4 mb-0 p-2 border bg-muted/50 rounded-xl flex justify-end items-center gap-2"
    >
      <DetectCogmoteGODialog />
      <Button @click="deviceStore.fetchDevices(['localhost'])">
        <Plus />
      </Button>
    </div>
    <div class="flex-1 overflow-y-auto">
      <div class="grid grid-cols-4 justify-center gap-4 p-4">
        <template v-for="[address, device] in deviceStore.devices">
          <RouterLink :to="`/device/${address}`">
            <DeviceCard :address="address" :device="device" />
          </RouterLink>
        </template>
      </div>
    </div>
  </div>
</template>
