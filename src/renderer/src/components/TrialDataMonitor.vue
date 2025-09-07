<script lang="ts" setup>
import { DeviceInfo } from '@/types/device'
import { useTrialDataStore } from '@/stores/trialData'
import { onMounted, ref } from 'vue'
import { TableV2Instance } from 'element-plus'

const props = defineProps<{
  device: DeviceInfo
}>()

const address = props.device.address
const channel = 'default'

const trialDataStore = useTrialDataStore()

const createColumns = (
  trialData: object,
  props?: object
): {
  key: string
  dataKey: string
  title: string
  width: number
}[] => {
  const keys = Object.keys(trialData)
  return keys.map((key, columnIndex) => ({
    ...props,
    key: `${columnIndex}`,
    dataKey: key,
    title: key
      .split('_')
      .map((word) => word[0].toUpperCase() + word.slice(1))
      .join(' '),
    width: 150
  }))
}

const data = ref<unknown[]>([])
const columns = ref<unknown[]>([])

const tableRef = ref<TableV2Instance>()

function scrollByRows(row: number): void {
  tableRef.value?.scrollToRow(row)
}

onMounted(async () => {
  try {
    await trialDataStore.connectSSE(address, channel, (newData) => {
      data.value.push({
        id: `row-${data.value.length}`,
        parentId: null,
        ...newData
      })

      if (data.value.length > 0 && columns.value.length === 0) {
        columns.value = createColumns(newData)
      }

      scrollByRows(data.value.length)
    })
  } catch (err) {
    console.error('failed to connect to device: ', err)
  }
})
</script>

<template>
  <div
    style="--el-bg-color: var(--color-muted) 100%"
    class="flex-1 pr-4 pl-4 border rounded-xl bg-muted/50"
  >
    <el-auto-resizer>
      <template #default="{ height, width }">
        <el-table-v2
          ref="tableRef"
          :columns="columns"
          :data="data"
          :width="width"
          :height="height"
          fixed
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<style scoped>
.bg-el-bg {
  --el-bg-color: var(--color-muted);
}
</style>
