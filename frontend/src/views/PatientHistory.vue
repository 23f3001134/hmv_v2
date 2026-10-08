<template>
  <div class="history-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Patient history</span>
      </div>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/doctor/login" class="nav-link">Doctor</RouterLink>
        <RouterLink to="/patient/login" class="nav-link">Patient</RouterLink>
        <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
      </div>
      <div class="nav-actions">
        <button class="nav-cta ghost" @click="goBackPage">Back</button>
        <RouterLink class="nav-cta" to="/patient/dashboard">Back to Dashboard</RouterLink>
      </div>
    </nav>

    <header class="hero-row">
      <div class="hero-copy">
        <p class="eyebrow">Records Archive</p>
        <h1>
          Patient
          <span class="accent">history</span>.
        </h1>
        <p class="lead">Medical records and visit details in one secure timeline.</p>
      </div>
      <div class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="panel-eyebrow">Patient Details</p>
              <h3>{{ patient ? patient.name : "Loading..." }}</h3>
            </div>
            <span class="panel-tag">{{ records.length }} record(s)</span>
          </div>
          <div class="panel-body">
            <div class="panel-item">
              <div class="panel-icon">ID</div>
              <div>
                <div class="panel-title">{{ patient ? patient.email : "" }}</div>
                <p>Contact email on file.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">RX</div>
              <div>
                <div class="panel-title">History log</div>
                <p>Review prior visits, diagnoses, and prescriptions.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="dashboard-card">
      <div class="card-head">
        <h5>History Records</h5>
        <span v-if="loading" class="muted-text">Loading...</span>
      </div>
      <div class="card-body p-0">
        <div v-if="loading" class="empty-state">Loading history...</div>
        <div v-else class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Visit Type</th>
                <th>Diagnosis</th>
                <th>Prescription</th>
                <th>Medicine</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="records.length === 0">
                <td colspan="6" class="empty-cell">No records found.</td>
              </tr>
              <tr v-for="r in records" :key="r.id">
                <td>{{ r.id }}</td>
                <td>{{ r.visit_type }}</td>
                <td>{{ r.diagnosis }}</td>
                <td>{{ r.prescription }}</td>
                <td>{{ r.medicine }}</td>
                <td>{{ r.record_date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useRoute } from "vue-router"
import api from "../services/api"

const route = useRoute()
const patientId = computed(() => Number(route.query.patient_id || 0))
const role = localStorage.getItem("role")
const isDoctorView = computed(() => role === "doctor" && patientId.value > 0)
const isAdminView = computed(() => role === "admin" && patientId.value > 0)

const patient = ref(null)
const loading = ref(false)
const records = ref([])

async function fetchPatient() {
  if (isDoctorView.value) {
    const res = await api.get("/doctor/dashboard")
    const found = (res.data.assigned_patients || []).find(p => p.id === patientId.value)
    patient.value = found || null
    return
  }

  if (isAdminView.value) {
    const res = await api.get(`/admin/patients/${patientId.value}`)
    patient.value = res.data || null
    return
  }

  const res = await api.get("/patient/profile")
  patient.value = res.data || null
}

async function fetchHistory() {
  loading.value = true
  if (isDoctorView.value) {
    const res = await api.get("/doctor/records", {
      params: { patient_id: patientId.value }
    })
    records.value = res.data || []
  } else if (isAdminView.value) {
    const res = await api.get(`/admin/patients/${patientId.value}/records`)
    records.value = res.data || []
  } else {
    const res = await api.get("/patient/records")
    records.value = res.data || []
  }
  loading.value = false
}

onMounted(() => {
  fetchPatient()
  fetchHistory()
})

const goBackPage = () => {
  history.back()
}
</script>

<style scoped>
.history-shell {
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  min-height: 100vh;
  background:
    radial-gradient(circle at 10% 20%, rgba(14, 165, 165, 0.18), transparent 45%),
    radial-gradient(circle at 90% 12%, rgba(56, 189, 248, 0.16), transparent 40%),
    linear-gradient(180deg, #f6f9fc 0%, #ffffff 70%);
  color: #0f172a;
  padding: 28px clamp(16px, 4vw, 56px) 48px;
}

.top-nav {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 18px;
  padding: 14px 20px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(8px);
}

.brand {
  display: grid;
  gap: 2px;
}

.brand-mark {
  font-family: "DM Serif Display", "Georgia", serif;
  font-size: 1.6rem;
  color: #0f172a;
}

.brand-sub {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #64748b;
}

.nav-links {
  display: flex;
  gap: 18px;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #0f172a;
  font-weight: 600;
  font-size: 0.9rem;
}

.nav-link:hover {
  color: #0f766e;
}

.nav-cta {
  text-decoration: none;
  background: #0f766e;
  color: #fff;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  font-weight: 600;
  box-shadow: 0 12px 24px rgba(15, 118, 110, 0.25);
}

.nav-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-cta.ghost {
  background: rgba(15, 23, 42, 0.08);
  color: #0f172a;
  box-shadow: none;
}

.hero-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: center;
  margin-top: 36px;
}

.hero-copy h1 {
  font-family: "DM Serif Display", "Georgia", serif;
  font-size: clamp(2.2rem, 4vw, 3rem);
  line-height: 1.05;
  margin-bottom: 16px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.65rem;
  color: #0f766e;
  font-weight: 700;
  margin-bottom: 12px;
}

.accent {
  color: #0f766e;
}

.lead {
  font-size: 1.02rem;
  color: #475569;
  max-width: 560px;
}

.hero-panel {
  display: grid;
  gap: 18px;
}

.panel-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.panel-eyebrow {
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.18em;
  color: #0f766e;
  margin-bottom: 6px;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.35rem;
}

.panel-tag {
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  border-radius: 999px;
  padding: 0.35rem 0.8rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.panel-body {
  display: grid;
  gap: 18px;
  margin-top: 18px;
}

.panel-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  align-items: start;
}

.panel-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-weight: 700;
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
}

.panel-title {
  font-weight: 700;
  margin-bottom: 4px;
}

.panel-item p {
  margin: 0;
  color: #64748b;
}

.dashboard-card {
  margin-top: 36px;
  background: #ffffff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
}

.card-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.card-head h5 {
  margin: 0;
  font-size: 1.2rem;
}

.card-body {
  margin-top: 18px;
}

.table-wrap {
  overflow-x: auto;
  border-radius: 14px;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  text-align: left;
  background: rgba(15, 118, 110, 0.1);
  color: #0f172a;
  padding: 12px 16px;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

tbody td {
  padding: 14px 16px;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  color: #0f172a;
}

.muted-text {
  color: #64748b;
}

.empty-state {
  text-align: center;
  color: #64748b;
  padding: 24px 12px;
}

.empty-cell {
  text-align: center;
  color: #64748b;
  padding: 24px 12px;
}

@media (max-width: 960px) {
  .top-nav {
    grid-template-columns: 1fr;
    justify-items: start;
  }

  .nav-links {
    flex-wrap: wrap;
  }
}

@media (max-width: 720px) {
  .top-nav {
    gap: 12px;
  }

  .nav-cta {
    justify-self: start;
  }
}
</style>
