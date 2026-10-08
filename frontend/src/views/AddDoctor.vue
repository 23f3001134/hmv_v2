<template>
  <div class="add-shell">
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
      <RouterLink class="nav-cta" to="/admin/dashboard">Back to Dashboard</RouterLink>
    </nav>

    <main class="form-grid">
      <section class="form-copy">
        <p class="eyebrow">New Staff Entry</p>
        <h1>
          Add a doctor to
          <span class="accent">MediSys</span>.
        </h1>
        <p class="lead">
          Register core details to enable scheduling, department visibility, and
          patient assignment across the system.
        </p>
        <div class="focus-card">
          <div class="focus-title">Admin checklist</div>
          <ul>
            <li>Verify credentials</li>
            <li>Assign department</li>
            <li>Confirm contact info</li>
          </ul>
        </div>
      </section>

      <section class="form-card">
        <h4>Add New Doctor</h4>
        <p class="helper-text">
          Register a new doctor and make them available for appointments in the system.
        </p>

        <div class="field">
          <label>Doctor Name</label>
          <input v-model="form.doctor_name" placeholder="Dr. Amit" />
        </div>

        <div class="field">
          <label>Department</label>
          <input v-model="form.department" placeholder="Cardiology" />
        </div>

        <div class="field">
          <label>Experience (years)</label>
          <input v-model.number="form.experience" type="number" placeholder="3" />
        </div>

        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="amit@gmail.com" />
        </div>

        <div class="field">
          <label>Contact</label>
          <input v-model="form.contact" placeholder="9876543211" />
        </div>

        <button class="btn-primary" @click="createDoctor" :disabled="loading">
          <span v-if="loading">Creating...</span>
          <span v-else>Create</span>
        </button>

        <div v-if="success" class="alert success">
          <p class="mb-1">Doctor added successfully.</p>
          <p class="mb-1">
            Temporary password: <strong>{{ tempPassword }}</strong>
          </p>
          <p class="mb-2">
            Copy it now and share it with the doctor. It will not be shown again.
          </p>
          <button class="btn-primary" @click="router.push('/admin/dashboard')">
            Back to dashboard
          </button>
        </div>

        <div v-if="error" class="alert danger">
          {{ error }}
        </div>
      </section>
    </main>
  </div>
</template>


<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()
const loading = ref(false)
const error = ref("")
const success = ref(false)
const tempPassword = ref("")

const form = reactive({
  doctor_name: "",
  department: "",
  experience: "",
  email: "",
  contact: ""
})



const createDoctor = async () => {
  error.value = ""
  success.value = false
  loading.value = true

  try {
    const payload = {
      doctor_name: form.doctor_name,
      department: form.department,
      experience: Number(form.experience),
      email: form.email,
      contact: form.contact
    }

    const res = await api.post("/admin/doctors", payload)

    tempPassword.value = res.data.temporary_password
    success.value = true

  } catch (err) {
    console.error(err.response?.data || err)
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      err.message ||
      "Server error"
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.add-shell {
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: center;
  margin-top: 40px;
}

.form-copy h1 {
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
  max-width: 520px;
}

.focus-card {
  margin-top: 24px;
  background: #0f172a;
  color: #e2e8f0;
  padding: 18px 20px;
  border-radius: 16px;
  box-shadow: 0 16px 32px rgba(15, 23, 42, 0.18);
}

.focus-title {
  font-weight: 700;
  margin-bottom: 8px;
}

.focus-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
}

.focus-card li::before {
  content: "* ";
  color: #0ea5a5;
  font-weight: 700;
}

.form-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 26px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 16px;
}

.form-card h4 {
  margin: 0;
  font-size: 1.4rem;
}

.helper-text {
  margin: 0;
  color: #64748b;
}

.field {
  display: grid;
  gap: 8px;
}

.field label {
  font-weight: 600;
  color: #0f172a;
}

.field input {
  border: none;
  background: rgba(255, 255, 255, 0.85);
  padding: 0.85rem 1rem;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
  font-weight: 600;
  color: #0f172a;
}

.btn-primary {
  text-decoration: none;
  padding: 0.75rem 1.6rem;
  border-radius: 999px;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: none;
  cursor: pointer;
  background: #0f766e;
  color: #fff;
  box-shadow: 0 16px 28px rgba(15, 118, 110, 0.25);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.alert {
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-weight: 600;
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
