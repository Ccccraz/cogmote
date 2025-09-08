<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

import Separator from '@/components/ui/separator/Separator.vue'
import { Button } from '@/components/ui/button'
import { Sidebar } from 'lucide-vue-next'
import Dashboardview from './Dashboardview.vue'
import DeviceList from '@/components/DeviceList.vue'

// get the address from the route
const route = useRoute()
const address = computed(() => route.params.address as string)
console.log(address)

// toggle side bar
const needSideBar = ref(true)
const toggleSideBar = (): void => {
  needSideBar.value = !needSideBar.value
}
</script>

<template>
  <div v-if="address != 'undefined'" class="flex-1 flex">
    <div v-if="needSideBar" class="w-48 flex flex-col border-r transition-all duration-300">
      <DeviceList key="device-list" :address="address" />
    </div>
    <div class="flex-1 flex flex-col">
      <div>
        <Button variant="ghost" @click="toggleSideBar">
          <Sidebar class="h-4 w-4" />
        </Button>
      </div>
      <Separator />
      <Dashboardview :key="`dashboard-view-${address}`" :address="address" />
    </div>
  </div>
  <div v-else class="flex-1 flex justify-center items-center">
    <h1 class="text-2xl">No device selected</h1>
  </div>
</template>
