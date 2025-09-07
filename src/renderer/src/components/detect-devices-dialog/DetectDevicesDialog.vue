<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog'

import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Search, Loader2 } from 'lucide-vue-next' // icons
import { useDetectDevices } from './detectDevices'
import { useDeviceStore } from '@/stores/device'
import DetectDevicesCombobox from './DetectDevicesDialogCombobox.vue'
import { computed, ref, Ref } from 'vue'
import { Item } from './types'

const { genIpList, genDomainList, detect, detectDomain } = useDetectDevices()

const deviceStore = useDeviceStore()
const ipParts = ref<string[]>(['192', '168', '1', '*'])
const domainParts = ref<string[]>(['cog', '1', 'cloud.lab'])

const detectMethods: Item[] = [
  { value: 'ip', label: 'IP Range' },
  { value: 'domain', label: 'Domain Name' }
]

const detectMethod: Ref<Item> = ref<Item>({
  value: 'ip',
  label: 'IP Range'
})

const ipList = computed(() => genIpList(ipParts.value))
const domainList = computed(() => genDomainList(domainParts.value))
</script>

<template>
  <Dialog>
    <DialogTrigger as-child>
      <Button>
        <Search />
      </Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-[618px]">
      <DialogHeader>
        <DialogTitle> Detect cogmoteGO </DialogTitle>
        <DialogDescription> Set the IP range to be automatically detected </DialogDescription>
      </DialogHeader>
      <DetectDevicesCombobox v-model:detect-method="detectMethod" :detect-methods="detectMethods" />

      <div v-if="detectMethod.value === 'ip'" class="grid gap-4 py-4">
        <div class="grid grid-cols-5 items-center gap-4">
          <Label> Range: </Label>
          <Input
            v-for="(_, index) in ipParts"
            :key="`ip-part-${index}`"
            v-model="ipParts[index]"
            type="text"
            class="text-center"
            maxlength="3"
          >
          </Input>
        </div>
      </div>

      <div v-if="detectMethod.value === 'domain'" class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label> Domain name: </Label>
          <Input
            v-for="(_, index) in domainParts"
            :key="`domain-part-${index}`"
            v-model="domainParts[index]"
            type="text"
            class="text-center"
          />
        </div>
      </div>

      <DialogFooter>
        <Button @click="'id' === detectMethod.value ? detect(ipList) : detectDomain(domainList)">
          <Loader2 v-if="deviceStore.loading" class="animate-spin" /> Detect
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
