<script setup lang="ts">
import { use } from "echarts/core";
import { LineChart } from "echarts/charts";
import { GridComponent } from "echarts/components";
import { SVGRenderer } from "echarts/renderers";
import VChart from "vue-echarts";
import type { ComposeOption } from "echarts/core";
import type { LineSeriesOption } from "echarts/charts";
import type { GridComponentOption } from "echarts/components";

use([GridComponent, LineChart, SVGRenderer]);

type EChartsOption = ComposeOption<GridComponentOption | LineSeriesOption>;

const option: EChartsOption = {
  xAxis: {
    type: "category",
    data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
  yAxis: {
    type: "value",
  },
  series: [
    {
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      type: "line",
      smooth: true,
    },
  ],
};
</script>

<template>
  <div class="border rounded-xl bg-muted/50 p-4">
    <v-chart :option="option" autoresize />
  </div>
</template>
