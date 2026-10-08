<template>
  <div class="admin-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Admin console</span>
      </div>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/doctor/login" class="nav-link">Doctor</RouterLink>
        <RouterLink to="/patient/login" class="nav-link">Patient</RouterLink>
        <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
      </div>
      <RouterLink class="nav-cta" to="/">Back to Home</RouterLink>
    </nav>

    <header class="hero-row">
      <div class="hero-copy">
        <p class="eyebrow">Hospital Control Center</p>
        <h1>
          Administrative
          <span class="accent">command</span>.
        </h1>
        <p class="lead">
          Monitor doctors, patients, and appointments in one dashboard with
          search, status control, and quick actions.
        </p>
        <div class="hero-actions">
          <div class="search-wrap">
            <input
              v-model="search"
              class="search-input"
              placeholder="Search doctor, patient, department..."
            />
          </div>
          <button class="btn-primary" @click="fetchAll">Search</button>
          <RouterLink class="btn-ghost" to="/add_doctor">Add Doctor</RouterLink>
        </div>
      </div>

      <div class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="panel-eyebrow">Live Overview</p>
              <h3>Daily operational snapshot</h3>
            </div>
            <span class="panel-tag">Active</span>
          </div>
          <div class="panel-body">
            <div class="panel-item">
              <div class="panel-icon">01</div>
              <div>
                <div class="panel-title">{{ doctors.length }} Doctors</div>
                <p>Manage staffing and department coverage.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">02</div>
              <div>
                <div class="panel-title">{{ patients.length }} Patients</div>
                <p>Track active profiles and eligibility.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">03</div>
              <div>
                <div class="panel-title">{{ appointments.length }} Appointments</div>
                <p>Stay ahead of upcoming schedules.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="floating-card">
          <div class="floating-title">Admin Focus</div>
          <ul>
            <li>Approve onboarding</li>
            <li>Monitor blacklist status</li>
            <li>Review appointment flow</li>
          </ul>
        </div>
      </div>
    </header>

    <main class="dashboard-body">
      <div v-if="actionError" class="alert alert-danger mb-4">
        {{ actionError }}
      </div>

      <section class="dashboard-card">
        <div class="card-head">
          <div>
            <h5>Registered Doctors</h5>
            <p>Manage doctors, departments, and account status.</p>
          </div>
          <div class="card-actions">
            <span class="pill-count">{{ doctors.length }} total</span>
            <RouterLink to="/add_doctor" class="btn-primary btn-sm">+ Create</RouterLink>
          </div>
        </div>

        <div class="card-body">
          <div v-if="doctors.length === 0" class="empty-state">
            <h6>No doctors registered yet</h6>
            <p>Start by adding a doctor to your system.</p>
            <RouterLink to="/add_doctor" class="btn-ghost btn-sm">Add First Doctor</RouterLink>
          </div>

          <div v-else class="grid-cards">
            <article v-for="doc in doctors" :key="doc.id" class="record-card">
              <div>
                <h6>{{ doc.name }}</h6>
                <p>{{ doc.department || "No department" }}</p>
                <span v-if="doc.is_blacklisted" class="badge danger">Blacklisted</span>
              </div>
              <div class="button-row">
                <button class="btn-warning btn-sm" @click="editDoctor(doc)">Edit</button>
                <button class="btn-danger btn-sm" @click="deleteDoctor(doc)">Delete</button>
                <button class="btn-muted btn-sm" @click="blacklistDoctor(doc)">
                  {{ doc.is_blacklisted ? "Unblacklist" : "Blacklist" }}
                </button>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="dashboard-card">
        <div class="card-head">
          <h5>Registered Patients</h5>
          <span class="pill-count">{{ patients.length }} total</span>
        </div>

        <div class="card-body">
          <div v-if="patients.length === 0" class="empty-state">No patients found</div>

          <div v-else class="stack-rows">
            <article v-for="p in patients" :key="p.id" class="patient-row">
              <div class="row-meta">
                <div class="avatar-chip">{{ (p.name || "?").slice(0, 1).toUpperCase() }}</div>
                <div>
                  <p class="row-title">{{ p.name }}</p>
                  <span v-if="p.is_blacklisted" class="badge danger">Blacklisted</span>
                </div>
              </div>
              <div class="button-row">
                <button class="btn-warning btn-sm" @click="editPatient(p)">Edit</button>
                <button class="btn-danger btn-sm" @click="deletePatient(p)">Delete</button>
                <button class="btn-muted btn-sm" @click="blacklistPatient(p)">
                  {{ p.is_blacklisted ? "Unblacklist" : "Blacklist" }}
                </button>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="dashboard-card">
        <div class="card-head">
          <h5>Upcoming Appointments</h5>
          <span class="pill-count">{{ appointments.length }} scheduled</span>
        </div>

        <div class="card-body p-0">
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Patient</th>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>History</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="appointments.length === 0">
                  <td colspan="5" class="empty-cell">No appointments found</td>
                </tr>
                <tr v-for="a in appointments" :key="a.id">
                  <td>{{ a.id }}</td>
                  <td>{{ a.patient_name }}</td>
                  <td>{{ a.doctor_name }}</td>
                  <td>{{ a.department }}</td>
                  <td>
                    <button class="btn-ghost btn-sm" @click="viewHistory(a.patient_id)">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const doctors = ref([])
const patients = ref([])
const appointments = ref([])
const search = ref("")
const actionError = ref("")


const fetchAll = async () => {
  try {
    const res = await api.get("/admin/dashboard", {
      params: { q: search.value }
    })

    doctors.value = res.data.doctors
    patients.value = res.data.patients
    appointments.value = res.data.appointments
  } catch (err) {
    console.error("Dashboard fetch failed", err)
  }
}

const editDoctor = async doc => {
  actionError.value = ""
  const doctor_name = prompt("Doctor name", doc.name)
  if (doctor_name === null) return
  const department = prompt("Department", doc.department || "")
  if (department === null) return
  const experience = prompt("Experience (years)", String(doc.experience ?? ""))
  if (experience === null) return
  const email = prompt("Email", doc.email || "")
  if (email === null) return
  const contact = prompt("Contact", doc.contact || "")
  if (contact === null) return

  try {
    await api.put(`/admin/doctors/${doc.id}`, {
      doctor_name,
      department,
      experience: Number(experience),
      email,
      contact
    })
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update doctor"
  }
}

const deleteDoctor = async doc => {
  actionError.value = ""
  if (!confirm(`Delete ${doc.name}? This will remove related data.`)) return
  try {
    await api.delete(`/admin/doctors/${doc.id}`)
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to delete doctor"
  }
}

const blacklistDoctor = async doc => {
  actionError.value = ""
  try {
    await api.put(`/admin/doctors/${doc.id}/blacklist`, {
      is_blacklisted: !doc.is_blacklisted
    })
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update blacklist"
  }
}

const editPatient = async patient => {
  actionError.value = ""
  const name = prompt("Patient name", patient.name)
  if (name === null) return
  const email = prompt("Email", patient.email || "")
  if (email === null) return
  const contact = prompt("Contact", patient.contact || "")
  if (contact === null) return
  const age = prompt("Age", String(patient.age ?? ""))
  if (age === null) return
  const gender = prompt("Gender", patient.gender || "")
  if (gender === null) return

  try {
    await api.put(`/admin/patients/${patient.id}`, {
      name,
      email,
      contact,
      age: age === "" ? null : Number(age),
      gender
    })
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update patient"
  }
}

const deletePatient = async patient => {
  actionError.value = ""
  if (!confirm(`Delete ${patient.name}? This will remove related data.`)) return
  try {
    await api.delete(`/admin/patients/${patient.id}`)
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to delete patient"
  }
}

const blacklistPatient = async patient => {
  actionError.value = ""
  try {
    await api.put(`/admin/patients/${patient.id}/blacklist`, {
      is_blacklisted: !patient.is_blacklisted
    })
    await fetchAll()
  } catch (err) {
    actionError.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update blacklist"
  }
}
const viewHistory = id => {
  router.push({ path: "/patient/history", query: { patient_id: id } })
}

// LOAD
onMounted(fetchAll)
</script>

<style scoped>
.admin-shell {
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
  margin: 22px 0 0;
}

.search-wrap {
  flex: 1 1 260px;
}

.search-input {
  width: 100%;
  border: none;
  background: rgba(255, 255, 255, 0.8);
  padding: 0.85rem 1.1rem;
  border-radius: 999px;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
  font-weight: 600;
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

.dashboard-body {
  margin-top: 42px;
  display: grid;
  gap: 28px;
}

.dashboard-card {
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
  margin: 0 0 6px;
  font-size: 1.2rem;
}

.card-head p {
  margin: 0;
  color: #64748b;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pill-count {
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.card-body {
  margin-top: 20px;
}

.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.record-card {
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  padding: 16px;
  background: #fdfefe;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
  display: grid;
  gap: 16px;
}

.record-card h6 {
  margin: 0 0 6px;
  font-size: 1rem;
}

.record-card p {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge.danger {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.btn-warning,
.btn-danger,
.btn-muted {
  border: none;
  border-radius: 999px;
  padding: 0.45rem 0.9rem;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
}

.btn-warning {
  background: rgba(245, 158, 11, 0.18);
  color: #92400e;
}

.btn-danger {
  background: rgba(239, 68, 68, 0.16);
  color: #b91c1c;
}

.btn-muted {
  background: rgba(15, 23, 42, 0.08);
  color: #0f172a;
}

.stack-rows {
  display: grid;
  gap: 12px;
}

.patient-row {
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  padding: 14px 16px;
  background: #ffffff;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.row-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-title {
  margin: 0;
  font-weight: 700;
}

.avatar-chip {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  display: grid;
  place-items: center;
  font-weight: 700;
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

.empty-state {
  text-align: center;
  color: #64748b;
  display: grid;
  gap: 8px;
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

  .patient-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
