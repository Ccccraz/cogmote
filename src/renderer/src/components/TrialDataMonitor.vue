<script lang="ts" setup>
import { DeviceInfo } from '@/types/device'
import { useTrialDataStore } from '@/stores/trialData'
import { computed, ref, watch, onMounted, nextTick } from 'vue'
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

const data = ref<object[]>([])
const columns = ref<object[]>([])

const tableRef = ref<TableV2Instance>()

function scrollToBottom(): void {
  if (data.value.length > 0) {
    tableRef.value?.scrollToRow(data.value.length - 1)
  }
}

const latestData = computed(() => {
  const trialData = trialDataStore.getChannelData(address)
  return trialData?.length > 0 ? trialData[trialData.length - 1] : null
})

watch(
  latestData,
  (newData) => {
    if (newData) {
      data.value.push({
        id: `row-${data.value.length}`,
        parentId: null,
        ...newData
      })

      if (columns.value.length === 0) {
        columns.value = createColumns(newData)
      }

      nextTick(() => {
        scrollToBottom()
      })
    }
  },
  { immediate: true }
)

onMounted(() => {
  trialDataStore.connectSSE(address, channel)

  const trialData = trialDataStore.getChannelData(address)
  if (trialData) {
    data.value = trialData.map((data, index) => ({
      id: `row-${index}`,
      parentId: null,
      ...data
    }))
  }

  if (data.value.length > 0 && columns.value.length === 0) {
    columns.value = createColumns(data.value[0])
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
