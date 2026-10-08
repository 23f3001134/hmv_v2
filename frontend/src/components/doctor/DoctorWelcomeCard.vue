<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
        <div>
          <p class="text-uppercase text-muted small mb-1">Doctor Portal</p>
          <h4 class="mb-2">Welcome, {{ doctor?.name || "Doctor" }}</h4>
          <p class="text-muted mb-2">
            Department:
            <span class="fw-semibold">{{ doctor?.department || "N/A" }}</span>
          </p>
          <p class="text-muted mb-3">
            Manage appointments, update patient records, and keep your
            availability up to date from one modern workspace.
          </p>
          <div class="d-flex flex-wrap gap-2">
            <span class="badge bg-primary-subtle text-primary">Smart schedule</span>
            <span class="badge bg-success-subtle text-success">Quick notes</span>
            <span class="badge bg-warning-subtle text-warning">Auto reminders</span>
          </div>
        </div>
        <div class="d-flex gap-3">
          <div class="text-center border rounded-3 px-3 py-2">
            <div class="text-muted small">Appointments</div>
            <div class="fs-4 fw-bold">{{ appointmentCount }}</div>
          </div>
          <div class="text-center border rounded-3 px-3 py-2">
            <div class="text-muted small">Patients</div>
            <div class="fs-4 fw-bold">{{ patientCount }}</div>
          </div>
        </div>
      </div>
      <div class="mt-4 d-flex justify-content-end">
        <button class="btn btn-outline-secondary btn-sm" @click="$emit('logout')">
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  doctor: { type: Object, default: null },
  appointmentCount: { type: Number, default: 0 },
  patientCount: { type: Number, default: 0 }
})

defineEmits(["logout"])
</script>
