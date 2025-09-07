<script setup lang="ts">
import { useDeviceStore } from '@/stores/device'
import { RefreshCcw } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import DeviceCard from '@/components/DeviceCard.vue'
import DetectCogmoteGODialog from '@/components/detect-devices-dialog/DetectDevicesDialog.vue'

const deviceStore = useDeviceStore()
</script>

<template>
  <div class="flex-1 flex flex-col">
    <div class="p-2 border-b-1 flex justify-end items-center gap-2">
      <Button @click="deviceStore.reconnectDevice()">
        <RefreshCcw />
      </Button>
      <DetectCogmoteGODialog />
    </div>
    <div class="flex-1 overflow-y-auto">
      <div class="grid grid-cols-4 justify-center gap-4 p-4">
        <RouterLink
          v-for="[address] in deviceStore.devices"
          :key="`device-card-${address}`"
          :to="`/device/${address}`"
        >
          <DeviceCard :address="address" />
        </RouterLink>
      </div>
    </div>
  </div>
</template>
