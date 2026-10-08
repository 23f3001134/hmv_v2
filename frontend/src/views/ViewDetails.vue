<template>
  <div class="details-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Department view</span>
      </div>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/doctor/login" class="nav-link">Doctor</RouterLink>
        <RouterLink to="/patient/login" class="nav-link">Patient</RouterLink>
        <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
      </div>
      <div class="nav-actions">
        <button class="nav-cta ghost" @click="goBackPage">Back</button>
        <button class="nav-cta" @click="logout">Logout</button>
      </div>
    </nav>

    <header class="hero-row">
      <div class="hero-copy">
        <p class="eyebrow">Department Overview</p>
        <h1>
          Department of
          <span class="accent">{{ department }}</span>.
        </h1>
        <p class="lead">
          Explore doctors, check availability, and book an appointment at a time
          that fits your schedule.
        </p>
        <div class="hero-actions">
          <button class="btn-ghost" @click="goToHistory">History</button>
          <button class="btn-primary" @click="goBack">Back to Dashboard</button>
        </div>
      </div>
      <div class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="panel-eyebrow">Doctors List</p>
              <h3>{{ doctors.length }} total</h3>
            </div>
            <span class="panel-tag">Live</span>
          </div>
          <div class="panel-body">
            <div class="panel-item">
              <div class="panel-icon">01</div>
              <div>
                <div class="panel-title">Availability</div>
                <p>Review slots before booking.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">02</div>
              <div>
                <div class="panel-title">Secure booking</div>
                <p>Appointments confirmed instantly.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="floating-card">
          <div class="floating-title">Booking tips</div>
          <ul>
            <li>Choose a morning slot for faster check-in</li>
            <li>Confirm date and time before booking</li>
            <li>Review availability notes</li>
          </ul>
        </div>
      </div>
    </header>

    <section class="dashboard-card">
      <div v-if="error" class="alert danger">
        {{ error }}
      </div>
      <div v-if="success" class="alert success">
        <div class="alert-title">Appointment confirmed.</div>
        <div class="muted-text">
          Doctor: Dr. {{ successDetails.doctor_name }}
          <span class="dot">*</span>
          Date: {{ successDetails.date }}
          <span class="dot">*</span>
          Time: {{ successDetails.time }}
        </div>
        <div class="muted-text">Redirecting to your dashboard...</div>
      </div>

      <div class="card-head">
        <h5>Doctors List</h5>
        <span class="pill-count">{{ doctors.length }} total</span>
      </div>

      <div class="card-body">
        <div v-if="loading" class="muted-text">Loading doctors...</div>
        <div v-else-if="doctors.length === 0" class="empty-state">
          No doctors found in this department.
        </div>
        <div v-else class="grid-cards">
          <article v-for="doc in doctors" :key="doc.id" class="doctor-card">
            <div class="doctor-head">
              <div>
                <div class="doctor-name"> {{ doc.name }}</div>
                <div class="muted-text">{{ doc.department }}</div>
                <div class="muted-text">{{ doc.experience }} yrs experience</div>
              </div>
              <button class="btn-ghost btn-sm" @click="toggleAvailability(doc.id)">
                {{ openDoctorId === doc.id ? "Hide Availability" : "Check Availability" }}
              </button>
            </div>

            <div v-if="openDoctorId === doc.id" class="availability-block">
              <div v-if="availabilityLoading" class="muted-text">Loading availability...</div>
              <div v-else>
                <div v-if="(availability[doc.id] || []).length === 0" class="muted-text">
                  No availability posted yet.
                </div>
                <div v-else class="availability-list">
                  <div v-for="slot in availability[doc.id]" :key="slot.date" class="availability-row">
                    <div>
                      <div class="row-title">{{ slot.date }}</div>
                      <div class="muted-text">
                        Morning: {{ slot.morning_slot }}
                        <span class="dot">*</span>
                        Evening: {{ slot.evening_slot }}
                      </div>
                    </div>
                    <div class="button-row">
                      <button class="btn-primary btn-sm" @click="prepareBooking(doc, slot, 'morning')">
                        Book Morning
                      </button>
                      <button class="btn-primary btn-sm" @click="prepareBooking(doc, slot, 'evening')">
                        Book Evening
                      </button>
                    </div>
                  </div>
                </div>

                <div v-if="booking.doctor" class="booking-box">
                  <div class="row-title">Book appointment with  {{ booking.doctor.name }}</div>
                  <div class="booking-grid">
                    <div class="field">
                      <label>Date</label>
                      <input v-model="booking.date" type="date" />
                    </div>
                    <div class="field">
                      <label>Time</label>
                      <input v-model="booking.time" type="time" />
                    </div>
                    <button class="btn-primary btn-sm" @click="bookAppointment">Book Appointment</button>
                  </div>
                  <div class="muted-text">You can book multiple appointments if needed.</div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../services/api"
import { clearSession } from "../utils/session"

const route = useRoute()
const router = useRouter()
const department = decodeURIComponent(route.params.department || "")

const doctors = ref([])
const availability = ref({})
const openDoctorId = ref(null)
const loading = ref(false)
const availabilityLoading = ref(false)
const error = ref("")
const success = ref(false)
const successDetails = ref({
  doctor_name: "",
  date: "",
  time: ""
})

const booking = ref({
  doctor: null,
  date: "",
  time: ""
})

const loadDoctors = async () => {
  loading.value = true
  error.value = ""
  try {
    const res = await api.get(`/patient/departments/${encodeURIComponent(department)}/doctors`)
    doctors.value = res.data || []
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to load doctors"
  } finally {
    loading.value = false
  }
}

const toggleAvailability = async (doctorId) => {
  success.value = false
  if (openDoctorId.value === doctorId) {
    openDoctorId.value = null
    return
  }
  openDoctorId.value = doctorId
  availabilityLoading.value = true
  try {
    const res = await api.get(`/patient/doctors/${doctorId}/availability`)
    availability.value = {
      ...availability.value,
      [doctorId]: res.data || []
    }
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to load availability"
  } finally {
    availabilityLoading.value = false
  }
}

const defaultTimeFromSlot = (slotText) => {
  if (!slotText) return "09:00"
  const parts = slotText.split("-")
  if (parts.length > 1) return parts[0].trim()
  return "09:00"
}

const prepareBooking = (doctor, slot, period) => {
  success.value = false
  booking.value = {
    doctor,
    date: slot.date,
    time: period === "morning"
      ? defaultTimeFromSlot(slot.morning_slot)
      : defaultTimeFromSlot(slot.evening_slot)
  }
}

const bookAppointment = async () => {
  if (!booking.value.doctor || !booking.value.date || !booking.value.time) return
  error.value = ""
  try {
    await api.post("/appointments", {
      doctor_id: booking.value.doctor.id,
      appointment_date: booking.value.date,
      appointment_time: booking.value.time
    })
    success.value = true
    successDetails.value = {
      doctor_name: booking.value.doctor.name,
      date: booking.value.date,
      time: booking.value.time
    }
    setTimeout(() => {
      router.push("/patient/dashboard")
    }, 1200)
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to book appointment"
  }
}

const goToHistory = () => {
  router.push("/patient/history")
}

const goBack = () => {
  router.push("/patient/dashboard")
}

const logout = () => {
  clearSession()
  router.push("/")
}

const goBackPage = () => {
  router.back()
}

onMounted(loadDoctors)
</script>

<style scoped>
.details-shell {
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

.nav-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-cta {
  border: none;
  background: #0f766e;
  color: #fff;
  padding: 0.6rem 1.2rem;
  border-radius: 999px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 12px 24px rgba(15, 118, 110, 0.25);
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

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.btn-primary,
.btn-ghost {
  text-decoration: none;
  padding: 0.75rem 1.6rem;
  border-radius: 999px;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #0f766e;
  color: #fff;
  box-shadow: 0 16px 28px rgba(15, 118, 110, 0.25);
}

.btn-ghost {
  border: 1px solid rgba(15, 23, 42, 0.2);
  color: #0f172a;
  background: rgba(255, 255, 255, 0.7);
}

.btn-primary:hover,
.btn-ghost:hover {
  transform: translateY(-2px);
}

.btn-sm {
  padding: 0.5rem 1.1rem;
  font-size: 0.85rem;
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

.floating-card {
  background: #0f172a;
  color: #e2e8f0;
  padding: 18px 20px;
  border-radius: 16px;
  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.18);
}

.floating-title {
  font-weight: 700;
  margin-bottom: 8px;
}

.floating-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
}

.floating-card li::before {
  content: "* ";
  color: #0ea5a5;
  font-weight: 700;
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

.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.doctor-card {
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  padding: 16px;
  background: #fdfefe;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
  display: grid;
  gap: 16px;
}

.doctor-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.doctor-name {
  font-weight: 700;
  margin-bottom: 4px;
}

.availability-block {
  display: grid;
  gap: 12px;
}

.availability-list {
  display: grid;
  gap: 10px;
}

.availability-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  border-radius: 12px;
  background: #f8fafc;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.booking-box {
  border: 1px dashed rgba(15, 118, 110, 0.35);
  border-radius: 12px;
  padding: 12px;
  background: rgba(15, 118, 110, 0.05);
  display: grid;
  gap: 12px;
}

.booking-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  align-items: end;
}

.field {
  display: grid;
  gap: 6px;
}

.field label {
  font-weight: 600;
  color: #0f172a;
}

.field input {
  border: none;
  background: rgba(255, 255, 255, 0.85);
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
  font-weight: 600;
  color: #0f172a;
}

.row-title {
  font-weight: 700;
}

.pill-count {
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.alert {
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-weight: 600;
  margin-bottom: 16px;
  display: grid;
  gap: 6px;
}

.alert.success {
  background: rgba(34, 197, 94, 0.12);
  color: #166534;
}

.alert.danger {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}

.alert-title {
  font-weight: 700;
}

.muted-text {
  color: #64748b;
}

.empty-state {
  text-align: center;
  color: #64748b;
  padding: 20px 0;
}

.dot {
  margin: 0 6px;
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

  .availability-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .doctor-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
