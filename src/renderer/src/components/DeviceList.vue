<script setup lang="ts">
import { useDeviceStore } from '@/stores/device'
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const deviceStore = useDeviceStore()

const addresses = computed(() => Array.from(deviceStore.devices.keys()))
</script>

<template>
  <div class="flex flex-col gap-2 p-2">
    <template v-for="address in addresses" :key="address">
      <router-link class="hover:bg-accent p-4 border rounded-xl" :to="`/device/${address}`">{{
        address
      }}</router-link>
    </template>
  </div>
</template>
