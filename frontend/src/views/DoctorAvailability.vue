<template>
  <div class="availability-page min-vh-100 py-4">
    <div class="container">
      <div class="page-header mb-4">
        <div class="title-stack">
          <p class="eyebrow">Doctor Workspace</p>
          <h2 class="page-title">Availability Planner</h2>
          <p class="subtitle">
            Define clear time slots so patients can book without delays.
          </p>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div class="availability-shell">
        <DoctorAvailabilityCard
          :availability="availability"
          :saving="saving"
          @add-row="addRow"
          @remove-row="removeRow"
          @save="saveAvailability"
        />
        <div class="hint-panel">
          <div class="hint-title">Scheduling tips</div>
          <ul class="hint-list">
            <li>Keep morning and evening slots consistent.</li>
            <li>Add at least 5 days to cover the week.</li>
            <li>Use 24-hour time for clarity.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import api from "../services/api"
import DoctorAvailabilityCard from "../components/doctor/DoctorAvailabilityCard.vue"

const availability = ref([])
const saving = ref(false)
const error = ref("")

const loadAvailability = async () => {
  error.value = ""
  try {
    const res = await api.get("/doctor/availability")
    availability.value = res.data || []
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load availability"
  }
}

const addRow = () => {
  availability.value.push({
    date: "",
    morning_slot: "",
    evening_slot: ""
  })
}

const removeRow = (index) => {
  availability.value.splice(index, 1)
}

const saveAvailability = async () => {
  saving.value = true
  error.value = ""
  try {
    await api.put("/doctor/availability", availability.value)
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to save availability"
  } finally {
    saving.value = false
  }
}

onMounted(loadAvailability)
</script>

<style scoped>
.availability-page {
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  background:
    radial-gradient(circle at 10% 12%, rgba(14, 165, 165, 0.16), transparent 38%),
    radial-gradient(circle at 90% 10%, rgba(251, 146, 60, 0.18), transparent 32%),
    linear-gradient(180deg, #f6f9fc 0%, #ffffff 70%);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.title-stack {
  display: grid;
  gap: 6px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 0.65rem;
  font-weight: 700;
  color: #0f766e;
  margin: 0;
}

.page-title {
  font-family: "DM Serif Display", "Georgia", serif;
  font-size: 2.2rem;
  margin: 0;
  color: #0f172a;
}

.subtitle {
  color: #475569;
  margin: 0;
}

.header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.btn-cta {
  background: #0f766e;
  color: #fff;
  border: none;
  padding: 0.6rem 1.4rem;
  box-shadow: 0 12px 24px rgba(15, 118, 110, 0.2);
}

.btn-cta:hover {
  background: #0d6b63;
  color: #fff;
}

.availability-shell {
  display: grid;
  gap: 20px;
  animation: fade-up 0.45s ease both;
}

.availability-shell :deep(.card) {
  border-radius: 18px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.hint-panel {
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
}

.hint-title {
  font-weight: 700;
  margin-bottom: 8px;
}

.hint-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: grid;
  gap: 6px;
  color: #cbd5f5;
}

.hint-list li::before {
  content: "• ";
  color: #38bdf8;
  font-weight: 700;
}

@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 992px) {
  .availability-shell {
    grid-template-columns: 3fr 1fr;
    align-items: start;
  }
}

@media (min-width: 768px) {
  .page-header {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
