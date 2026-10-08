<template>
  <div class="auth-shell">
    <div class="auth-grid">
      <div class="auth-panel">
        <div class="panel-header">
          <p class="eyebrow">Doctor Access</p>
          <h2>Doctor Login</h2>
          <p class="subtitle">
            Access patient schedules, histories, and daily workflow.
          </p>
        </div>

        <form class="auth-form" @submit.prevent="login">
          <div class="field">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              placeholder="doctor@hospital.com"
              v-model="email"
              required
            />
          </div>

          <div class="field">
            <label class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              placeholder="Enter your password"
              v-model="password"
              required
            />
          </div>

          <div v-if="error" class="alert alert-danger py-2">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-cta w-100" :disabled="loading">
            <span v-if="loading">Logging in...</span>
            <span v-else>Login</span>
          </button>
        </form>

        <div class="footer-note">
          Only authorized doctors are allowed to access this panel.
        </div>
      </div>

      <div class="side-panel">
        <div class="side-card">
          <div class="side-title">Daily workflow</div>
          <ul>
            <li>Review scheduled visits</li>
            <li>Update patient records</li>
            <li>Set availability slots</li>
            <li>Complete appointments quickly</li>
          </ul>
        </div>
        <div class="side-card accent">
          <div class="side-title">Need help?</div>
          <p>Contact hospital IT to reset your access credentials.</p>
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

const email = ref("")
const password = ref("")
const loading = ref(false)
const error = ref("")

const login = async () => {
  error.value = ""
  loading.value = true

  try {
    const res = await api.post("/auth/doctor/login", {
      email: email.value,
      password: password.value
    })

    localStorage.setItem("access_token", res.data.access_token)
    localStorage.setItem("role", "doctor")

    router.push("/doctor/dashboard")
  } catch (err) {
    error.value = err.response?.data?.message || "Invalid email or password"
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
