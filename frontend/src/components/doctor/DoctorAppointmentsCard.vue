<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Upcoming Appointments</h5>
      <span class="badge text-bg-primary">Today</span>
    </div>
    <div class="card-body p-0">
      <div class="table-responsive">
        <table class="table mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="appointments.length === 0">
              <td colspan="6" class="text-center text-muted py-4">
                No appointments found.
              </td>
            </tr>
            <tr v-for="a in appointments" :key="a.id">
              <td>{{ a.id }}</td>
              <td>{{ a.patient_name }}</td>
              <td>{{ a.date }}</td>
              <td>{{ a.time }}</td>
              <td>
                <span :class="statusClass(a.status)">
                  {{ a.status }}
                </span>
              </td>
              <td class="text-end">
                <div v-if="isFinal(a.status)" class="text-muted small">
                  No action required
                </div>
                <div v-else class="d-inline-flex gap-2 justify-content-end">
                  <button class="btn btn-sm btn-outline-primary" @click="$emit('update-history', a)">
                    Update
                  </button>
                  <button class="btn btn-sm btn-success" @click="$emit('mark-completed', a)">
                    Mark done
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="$emit('cancel-appointment', a)">
                    Cancel
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  appointments: { type: Array, default: () => [] }
})

defineEmits(["mark-completed", "cancel", "cancel-appointment", "update-history"])

const statusClass = status => {
  const base = "badge"
  if (!status) return `${base} text-bg-secondary`
  const value = status.toLowerCase()
  if (value.includes("confirm")) return `${base} text-bg-success`
  if (value.includes("cancel")) return `${base} text-bg-danger`
  if (value.includes("complete")) return `${base} text-bg-primary`
  return `${base} text-bg-warning`
}

const isFinal = status => {
  if (!status) return false
  const value = status.toLowerCase()
  return value.includes("complete") || value.includes("cancel")
}
</script>
