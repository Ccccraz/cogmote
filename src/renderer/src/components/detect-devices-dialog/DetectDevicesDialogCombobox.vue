<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Combobox,
  ComboboxAnchor,
  ComboboxGroup,
  ComboboxItem,
  ComboboxItemIndicator,
  ComboboxList,
  ComboboxTrigger
} from '@/components/ui/combobox'

import { cn } from '@/lib/utils'
import { ChevronsUpDown, Check } from 'lucide-vue-next' // icons
import { Item } from './types'

const detectMethod = defineModel<Item>('detect-method')

defineProps<{
  detectMethods: Item[]
}>()
</script>

<template>
  <div class="flex justify-between py-4">
    <Label> Detect method: </Label>
    <Combobox v-model="detectMethod" by="label">
      <ComboboxAnchor as-child>
        <ComboboxTrigger as-child>
          <Button variant="outline" class="justify-between">
            {{ detectMethod?.label ?? 'Select method' }}
            <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </ComboboxTrigger>
      </ComboboxAnchor>

      <ComboboxList>
        <ComboboxGroup>
          <ComboboxItem v-for="method in detectMethods" :key="method.value" :value="method">
            {{ method.label }}
            <ComboboxItemIndicator>
              <Check :class="cn('ml-auto h-4 w-4')" />
            </ComboboxItemIndicator>
          </ComboboxItem>
        </ComboboxGroup>
      </ComboboxList>
    </Combobox>
  </div>
</template>
