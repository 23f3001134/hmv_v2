<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Patient History</h5>
      <span class="badge text-bg-info">Records</span>
    </div>
    <div class="card-body p-0">
      <div class="table-responsive">
        <table class="table mb-0 align-middle">
          <thead class="table-light">
            <tr>
              <th>#</th>
              <th>Patient</th>
              <th>Visit Type</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Medicine</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="records.length === 0">
              <td colspan="6" class="text-center text-muted py-4">
                No records available.
              </td>
            </tr>
            <tr v-for="r in records" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.patient_name }}</td>
              <td>{{ r.visit_type }}</td>
              <td>{{ r.diagnosis }}</td>
              <td>{{ r.prescription }}</td>
              <td>{{ r.medicine }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  records: { type: Array, default: () => [] }
})
</script>
