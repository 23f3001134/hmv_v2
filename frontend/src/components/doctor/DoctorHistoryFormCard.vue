<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Update Patient History</h5>
      <span class="badge text-bg-warning">Quick Notes</span>
    </div>
    <div class="card-body">
      <form class="row g-3" @submit.prevent="$emit('save')">
        <div class="col-md-6">
          <label class="form-label">Patient</label>
          <select v-model="form.patient_id" class="form-select" required>
            <option disabled value="">Select patient</option>
            <option v-for="p in patients" :key="p.id" :value="p.id">
              {{ p.name }}
            </option>
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label">Visit Type</label>
          <select v-model="form.visit_type" class="form-select" required>
            <option>In-person</option>
            <option>Video</option>
            <option>Follow-up</option>
          </select>
        </div>
        <div class="col-12">
          <label class="form-label">Diagnosis</label>
          <input v-model="form.diagnosis" class="form-control" type="text" required />
        </div>
        <div class="col-md-6">
          <label class="form-label">Prescription</label>
          <input v-model="form.prescription" class="form-control" type="text" />
        </div>
        <div class="col-md-6">
          <label class="form-label">Medicine</label>
          <input v-model="form.medicine" class="form-control" type="text" />
        </div>
        <div class="col-12 d-flex justify-content-between align-items-center">
          <p class="text-muted small mb-0">
            Keep records updated so the care team can coordinate follow-ups.
          </p>
          <button class="btn btn-primary" type="submit" :disabled="saving">
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
defineProps({
  patients: { type: Array, default: () => [] },
  form: { type: Object, required: true },
  saving: { type: Boolean, default: false }
})

defineEmits(["save"])
</script>
