<template>
  <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-sm transition-shadow">
    <p class="text-xs text-gray-500 mb-1">{{ title }}</p>
    <p :class="`text-3xl font-bold ${color} mb-1`">{{ value }}</p>
    <p class="text-xs text-gray-400">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  subtitle: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: 'text-blue-600'
  }
})
</script>