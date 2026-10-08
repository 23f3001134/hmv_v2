<template>
  <div class="dashboard-shell">
    <div class="container py-4">
      <div class="page-header mb-4">
        <div class="title-stack">
          <p class="eyebrow">Doctor Workspace</p>
          <h2 class="page-title">Dashboard Overview</h2>
          <p class="subtitle">Track appointments, patients, and daily momentum.</p>
        </div>
        <div class="header-actions">
          <button class="btn btn-outline-dark" @click="goToAvailability">
            Availability
          </button>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <div class="hero-shell mb-4">
        <DoctorWelcomeCard
          :doctor="doctor"
          :appointment-count="appointments.length"
          :patient-count="patients.length"
          @logout="logout"
        />
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="stat card border-0 shadow-sm stat-accent">
            <div class="card-body">
              <div class="stat-label">Upcoming Appointments</div>
              <div class="stat-value">{{ appointments.length }}</div>
              <div class="text-muted small">Today and future schedules</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat card border-0 shadow-sm">
            <div class="card-body">
              <div class="stat-label">Assigned Patients</div>
              <div class="stat-value">{{ patients.length }}</div>
              <div class="text-muted small">Active patients under care</div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat card border-0 shadow-sm">
            <div class="card-body">
              <div class="stat-label">Profile</div>
              <div class="stat-value">
                {{ doctor?.email || "doctor@hospital.com" }}
              </div>
              <div class="text-muted small">Primary contact</div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-lg-8">
          <div class="section-card">
        <DoctorAppointmentsCard
          :appointments="appointments"
          @mark-completed="markCompleteFromCard"
          @cancel-appointment="cancelFromCard"
          @update-history="updateHistoryFromCard"
        />
          </div>
        </div>
        <div class="col-lg-4">
          <div class="section-card">
            <DoctorPatientsCard
              :patients="patients"
              @view-history="viewPatientFromCard"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"
import { clearSession } from "../utils/session"
import DoctorWelcomeCard from "../components/doctor/DoctorWelcomeCard.vue"
import DoctorAppointmentsCard from "../components/doctor/DoctorAppointmentsCard.vue"
import DoctorPatientsCard from "../components/doctor/DoctorPatientsCard.vue"

const router = useRouter()

const doctor = ref(null)
const appointments = ref([])
const patients = ref([])
const error = ref("")

const loadDashboard = async () => {
  error.value = ""
  try {
    const res = await api.get("/doctor/dashboard")
    doctor.value = res.data.doctor
    appointments.value = res.data.upcoming_appointments || []
    patients.value = res.data.assigned_patients || []
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Welcome, Doctor!"
  }
}

const viewPatient = patientId => {
  router.push({ path: "/patient/history", query: { patient_id: patientId } })
}

const updateHistory = patientId => {
  router.push({ path: "/patient/history/update", query: { patient_id: patientId } })
}

const goToAvailability = () => {
  router.push("/doctor/availability")
}

const markComplete = async appointmentId => {
  error.value = ""
  try {
    await api.put(`/appointments/${appointmentId}/status`, {
      status: "Completed"
    })
    await loadDashboard()
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update appointment"
  }
}

const cancelAppointment = async appointmentId => {
  error.value = ""
  try {
    await api.put(`/appointments/${appointmentId}/status`, {
      status: "Cancelled"
    })
    await loadDashboard()
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update appointment"
  }
}

const logout = () => {
  clearSession()
  router.push("/")
}

onMounted(loadDashboard)

const markCompleteFromCard = appointment => {
  if (!appointment?.id) return
  markComplete(appointment.id)
}

const cancelFromCard = appointment => {
  if (!appointment?.id) return
  if (!confirm("Are you sure you want to cancel this appointment?")) return
  cancelAppointment(appointment.id)
}

const viewPatientFromCard = patient => {
  if (!patient?.id) return
  viewPatient(patient.id)
}

const updateHistoryFromCard = appointment => {
  if (!appointment?.patient_id) return
  updateHistory(appointment.patient_id)
}
</script>

<style scoped>
.dashboard-shell {
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  background:
    radial-gradient(circle at 12% 10%, rgba(14, 165, 165, 0.18), transparent 38%),
    radial-gradient(circle at 88% 12%, rgba(249, 115, 22, 0.18), transparent 36%),
    linear-gradient(180deg, #f6f9fc 0%, #ffffff 60%);
  min-height: 100vh;
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
  gap: 12px;
}

.hero-shell {
  position: relative;
  animation: lift-in 0.45s ease both;
}

.hero-shell::before {
  content: "";
  position: absolute;
  inset: -12px;
  border-radius: 24px;
  background: linear-gradient(120deg, rgba(14, 165, 165, 0.18), rgba(15, 118, 110, 0.05));
  z-index: 0;
}

.hero-shell :deep(.card) {
  position: relative;
  z-index: 1;
  border-radius: 20px;
  overflow: hidden;
}

.stat {
  border-radius: 16px;
  background: #ffffff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 30px rgba(15, 23, 42, 0.12);
}

.stat-accent {
  background: linear-gradient(130deg, rgba(14, 165, 165, 0.14), rgba(255, 255, 255, 0.9));
}

.stat-label {
  font-size: 0.8rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #0f172a;
  word-break: break-word;
}

.section-card {
  animation: fade-up 0.55s ease both;
}

.section-card :deep(.card) {
  border-radius: 18px;
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

@keyframes lift-in {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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
