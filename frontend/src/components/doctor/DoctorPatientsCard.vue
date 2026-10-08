<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Assigned Patients</h5>
      <span class="badge text-bg-success">Active</span>
    </div>
    <div class="card-body">
      <div v-if="patients.length === 0" class="text-muted text-center py-3">
        No assigned patients.
      </div>
      <div
        v-for="p in patients"
        :key="p.id"
        class="d-flex align-items-center justify-content-between border rounded-3 p-3 mb-2"
      >
        <div>
          <div class="fw-semibold">{{ p.name }}</div>
          <div class="text-muted small">{{ p.email }}</div>
        </div>
        <button class="btn btn-sm btn-outline-primary" @click="$emit('view-history', p)">
          View
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  patients: { type: Array, default: () => [] }
})

defineEmits(["view-history"])
</script>
