<template>
  <div class="details-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Doctor records</span>
      </div>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/doctor/login" class="nav-link">Doctor</RouterLink>
        <RouterLink to="/patient/login" class="nav-link">Patient</RouterLink>
        <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
      </div>
      <div class="nav-actions">
        <button class="nav-cta ghost" type="button" @click="goBackPage">Back</button>
        <RouterLink class="nav-cta" to="/doctor/dashboard">Dashboard</RouterLink>
      </div>
    </nav>

    <header class="hero-row">
      <div class="hero-copy">
        <p class="eyebrow">Medical Record</p>
        <h1>
          Update patient
          <span class="accent">history</span>.
        </h1>
        <p class="lead">
          Record visit details, diagnosis, and prescriptions so the timeline stays
          complete and accurate.
        </p>
      </div>
      <div class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="panel-eyebrow">Patient Profile</p>
              <h3>{{ patient?.name || "Loading..." }}</h3>
            </div>
            <span class="panel-tag">ID {{ patientId || "-" }}</span>
          </div>
          <div class="panel-body">
            <div class="panel-item">
              <div class="panel-icon">@</div>
              <div>
                <div class="panel-title">{{ patient?.email || "-" }}</div>
                <p>Contact email on file.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">RX</div>
              <div>
                <div class="panel-title">Doctor note</div>
                <p>History updates are visible in patient records immediately.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="floating-card">
          <div class="floating-title">Checklist</div>
          <ul>
            <li>Confirm visit type before saving</li>
            <li>Add dosage with each medicine</li>
            <li>Include clear diagnosis notes</li>
          </ul>
        </div>
      </div>
    </header>

    <section class="dashboard-card">
      <div v-if="error" class="alert danger">{{ error }}</div>
      <div v-if="success" class="alert success">History updated successfully.</div>

      <div class="card-head">
        <h5>Visit Entry Form</h5>
        <span class="pill-count">{{ form.medicines.length }} medicine item(s)</span>
      </div>

      <form class="form-grid" @submit.prevent="saveHistory">
        <div class="field">
          <label for="visitType">Visit Type</label>
          <input
            id="visitType"
            v-model.trim="form.visitType"
            type="text"
            placeholder="First Visit / Follow-up"
            required
          />
        </div>

        <div class="field">
          <label for="testDone">Test Done</label>
          <input
            id="testDone"
            v-model.trim="form.testDone"
            type="text"
            placeholder="ECG, Blood Test, X-Ray"
          />
        </div>

        <div class="field full">
          <label for="diagnosis">Diagnosis</label>
          <input
            id="diagnosis"
            v-model.trim="form.diagnosis"
            type="text"
            placeholder="Enter diagnosis"
            required
          />
        </div>

        <div class="field full">
          <label for="prescription">Prescription</label>
          <textarea
            id="prescription"
            v-model.trim="form.prescription"
            rows="4"
            placeholder="Prescription notes"
            required
          ></textarea>
        </div>

        <div class="field full">
          <div class="medicine-head">
            <label>Medicines</label>
            <button class="btn-ghost btn-sm" type="button" @click="addMedicine">
              + Add Medicine
            </button>
          </div>

          <div class="medicine-list">
            <div
              v-for="(med, index) in form.medicines"
              :key="index"
              class="medicine-row"
            >
              <input
                v-model.trim="med.name"
                type="text"
                placeholder="Medicine name"
              />
              <input
                v-model.trim="med.dosage"
                type="text"
                placeholder="1-0-1"
              />
              <button
                class="btn-danger btn-sm"
                type="button"
                @click="removeMedicine(index)"
              >
                Remove
              </button>
            </div>
          </div>
        </div>

        <div class="form-actions full">
          <button class="btn-ghost" type="button" @click="goBackPage">Cancel</button>
          <button class="btn-primary" type="submit" :disabled="saving || !canSave">
            {{ saving ? "Saving..." : "Save History" }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "../services/api"

const route = useRoute()
const router = useRouter()
const patientId = Number(route.query.patient_id || 0)

const patient = ref(null)
const saving = ref(false)
const error = ref("")
const success = ref(false)

const form = reactive({
  visitType: "",
  testDone: "",
  diagnosis: "",
  prescription: "",
  medicines: [{ name: "", dosage: "" }]
})

const canSave = computed(() => {
  return form.visitType && form.diagnosis && form.prescription
})

function addMedicine() {
  form.medicines.push({ name: "", dosage: "" })
}

function removeMedicine(index) {
  form.medicines.splice(index, 1)
  if (form.medicines.length === 0) {
    form.medicines.push({ name: "", dosage: "" })
  }
}

const getMedicinePayload = () => {
  return form.medicines
    .map(med => `${med.name} ${med.dosage}`.trim())
    .filter(Boolean)
    .join(", ")
}

async function fetchPatient() {
  if (!patientId) {
    error.value = "Invalid patient ID."
    return
  }

  try {
    const res = await api.get("/doctor/dashboard")
    const found = (res.data.assigned_patients || []).find(p => p.id === patientId)
    patient.value = found || null

    if (!found) {
      error.value = "Patient not found in your assigned list."
    }
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to load patient details"
  }
}

async function saveHistory() {
  if (!patientId || !canSave.value || saving.value) return

  saving.value = true
  error.value = ""
  success.value = false

  try {
    await api.post("/doctor/records", {
      patient_id: patientId,
      visit_type: form.visitType,
      test_done: form.testDone,
      diagnosis: form.diagnosis,
      prescription: form.prescription,
      medicine: getMedicinePayload()
    })

    success.value = true
    setTimeout(() => {
      router.push({ path: "/patient/history", query: { patient_id: patientId } })
    }, 700)
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to save patient history"
  } finally {
    saving.value = false
  }
}

const goBackPage = () => {
  router.back()
}

onMounted(fetchPatient)
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
  text-decoration: none;
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

.pill-count {
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.form-grid {
  margin-top: 18px;
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.field {
  display: grid;
  gap: 6px;
}

.field.full {
  grid-column: 1 / -1;
}

.field label {
  font-weight: 700;
  color: #0f172a;
}

.field input,
.field textarea {
  border: none;
  background: rgba(255, 255, 255, 0.85);
  padding: 0.75rem 0.9rem;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
  font-weight: 600;
  color: #0f172a;
}

.field textarea {
  resize: vertical;
}

.medicine-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.medicine-list {
  display: grid;
  gap: 10px;
}

.medicine-row {
  display: grid;
  gap: 10px;
  grid-template-columns: 1fr 160px auto;
  align-items: center;
}

.btn-primary,
.btn-ghost,
.btn-danger {
  text-decoration: none;
  padding: 0.75rem 1.3rem;
  border-radius: 999px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: #0f766e;
  color: #fff;
  box-shadow: 0 16px 28px rgba(15, 118, 110, 0.25);
}

.btn-primary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-ghost {
  border: 1px solid rgba(15, 23, 42, 0.2);
  color: #0f172a;
  background: rgba(255, 255, 255, 0.7);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 6px;
}

.alert {
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-weight: 600;
  margin-bottom: 16px;
}

.alert.success {
  background: rgba(34, 197, 94, 0.12);
  color: #166534;
}

.alert.danger {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}

@media (max-width: 960px) {
  .top-nav {
    grid-template-columns: 1fr;
    justify-items: start;
  }

  .nav-links {
    flex-wrap: wrap;
  }

  .medicine-row {
    grid-template-columns: 1fr;
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
