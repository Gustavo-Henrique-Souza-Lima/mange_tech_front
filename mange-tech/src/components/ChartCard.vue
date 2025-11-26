<!-- src/components/ChartCard.vue -->
<template>
  <div class="bg-white p-5 rounded-lg border border-gray-200">
    <h3 class="text-sm font-semibold text-gray-700 mb-4">{{ title }}</h3>
    <div class="h-64">
      <component :is="chartComponent" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Doughnut, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  LineElement,
  PointElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  LineElement,
  PointElement
)

const props = defineProps({
  title: String,
  type: {
    type: String,
    default: 'bar' // 'bar', 'doughnut', 'line'
  },
  data: Object,
  options: Object
})

const chartComponent = computed(() => {
  const components = {
    bar: Bar,
    doughnut: Doughnut,
    line: Line
  }
  return components[props.type] || Bar
})

const chartData = computed(() => props.data)
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  ...props.options
}))
</script>