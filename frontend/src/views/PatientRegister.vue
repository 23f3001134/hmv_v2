<template>
  <div class="auth-shell">
    <div class="auth-grid wide">
      <div class="auth-panel">
        <div class="panel-header">
          <p class="eyebrow">Patient Registration</p>
          <h2>Create Your Account</h2>
          <p class="subtitle">
            Join MediSys to book appointments and manage your care.
          </p>
        </div>

        <div v-if="message" class="alert" :class="success ? 'alert-success' : 'alert-danger'">
          {{ message }}
        </div>

        <form class="auth-form" @submit.prevent="register">
          <div class="field">
            <label class="form-label">Full Name</label>
            <input v-model="name" class="form-control" placeholder="Your name" required />
          </div>

          <div class="field">
            <label class="form-label">Email</label>
            <input type="email" v-model="email" class="form-control" placeholder="you@example.com" required />
          </div>

          <div class="field">
            <label class="form-label">Contact Number</label>
            <input v-model="contact" class="form-control" placeholder="Phone number" required />
          </div>

          <div class="field">
            <label class="form-label">Password</label>
            <input type="password" v-model="password" class="form-control" placeholder="Create a password" required />
          </div>

          <div class="field">
            <label class="form-label">Age</label>
            <input type="number" v-model="age" class="form-control" placeholder="Age" required />
          </div>

          <div class="field">
            <label class="form-label">Gender</label>
            <select v-model="gender" class="form-select" required>
              <option value="" disabled>Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <button class="btn btn-cta w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? "Registering..." : "Register" }}
          </button>
        </form>

        <div class="footer-note">
          Already have an account?
          <router-link to="/patient/login" class="link-strong">Login</router-link>
        </div>
      </div>

      <div class="side-panel">
        <div class="side-card">
          <div class="side-title">Why register?</div>
          <ul>
            <li>Access appointments quickly</li>
            <li>Store medical history securely</li>
            <li>Get reminders and updates</li>
            <li>Manage all visits in one place</li>
          </ul>
        </div>
        <div class="side-card accent">
          <div class="side-title">Privacy first</div>
          <p>Your data stays protected with role-based access controls.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

const router = useRouter()

const name = ref("")
const email = ref("")
const contact = ref("")
const password = ref("")
const age = ref("")
const gender = ref("")
const loading = ref(false)
const message = ref("")
const success = ref(false)

const register = async () => {
  loading.value = true
  message.value = ""
  success.value = false
  try {
    await api.post("/auth/patient/register", {
      name: name.value.trim(),
      email: email.value.trim().toLowerCase(),
      contact: contact.value.trim(),
      password: password.value,
      age: Number(age.value),
      gender: gender.value
    })

    message.value = "Registration successful. Please log in."
    success.value = true
    setTimeout(() => router.push("/patient/login"), 800)
  } catch (err) {
    message.value =
      err.response?.data?.message ||
      `Backend not reachable: ${err.message}. Ensure backend server is running on the correct port.`
    success.value = false
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 32px 16px;
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  background:
    radial-gradient(circle at 12% 10%, rgba(14, 165, 165, 0.14), transparent 40%),
    radial-gradient(circle at 88% 12%, rgba(56, 189, 248, 0.12), transparent 40%),
    linear-gradient(180deg, #f6f9fc 0%, #ffffff 70%);
}

.auth-grid {
  width: min(1100px, 100%);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 28px;
  align-items: stretch;
}

.auth-grid.wide {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.auth-panel {
  background: #ffffff;
  border-radius: 22px;
  padding: 32px;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.12);
}

.panel-header h2 {
  font-family: "DM Serif Display", "Georgia", serif;
  margin: 0 0 8px;
  font-size: 2rem;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 0.65rem;
  color: #0f766e;
  font-weight: 700;
  margin-bottom: 10px;
}

.subtitle {
  color: #475569;
  margin: 0 0 22px;
}

.auth-form {
  display: grid;
  gap: 16px;
}

.field {
  display: grid;
  gap: 6px;
}

.btn-cta {
  background: #0f766e;
  color: #fff;
  border: none;
  padding: 0.65rem 1rem;
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(15, 118, 110, 0.2);
}

.btn-cta:hover {
  background: #0d6b63;
  color: #fff;
}

.footer-note {
  margin-top: 18px;
  font-size: 0.9rem;
  color: #64748b;
}

.link-strong {
  font-weight: 700;
  text-decoration: none;
  color: #0f766e;
}

.side-panel {
  display: grid;
  gap: 18px;
}

.side-card {
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 18px 38px rgba(15, 23, 42, 0.2);
}

.side-card ul {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: grid;
  gap: 6px;
}

.side-card li::before {
  content: "* ";
  color: #38bdf8;
  font-weight: 700;
}

.side-card.accent {
  background: #ffffff;
  color: #0f172a;
  border: 1px solid rgba(148, 163, 184, 0.3);
}

.side-title {
  font-weight: 700;
  margin-bottom: 8px;
}

@media (max-width: 720px) {
  .auth-panel {
    padding: 24px;
  }
}
</style>
