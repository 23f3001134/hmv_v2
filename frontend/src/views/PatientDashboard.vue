<template>
  <div class="patient-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Patient portal</span>
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

    <div v-if="loading" class="loading-card">
      <div class="spinner"></div>
      <p>Loading your dashboard...</p>
    </div>

    <div v-else>
      <header class="hero-row">
        <div class="hero-copy">
          <p class="eyebrow">Welcome Back</p>
          <h1>
            Hello, {{ patient.name || "Patient" }}
            <span class="accent">dashboard</span>.
          </h1>
          <p class="lead">
            Manage appointments, explore departments, and update your profile without
            leaving MediSys.
          </p>
          <div class="hero-actions">
            <button class="btn-primary" @click="toggleEdit">
              {{ editMode ? "Cancel Edit" : "Edit Profile" }}
            </button>
            <button class="btn-ghost" @click="goToHistory">History</button>
          </div>
        </div>

        <div class="hero-panel">
          <div class="panel-card">
            <div class="panel-header">
              <div>
                <p class="panel-eyebrow">Health Snapshot</p>
                <h3>Upcoming focus</h3>
              </div>
              <span class="panel-tag">Active</span>
            </div>
            <div class="panel-body">
              <div class="panel-item">
                <div class="panel-icon">01</div>
                <div>
                  <div class="panel-title">{{ appointments.length }} Appointments</div>
                  <p>Plan your schedule and arrive early.</p>
                </div>
              </div>
              <div class="panel-item">
                <div class="panel-icon">02</div>
                <div>
                  <div class="panel-title">{{ departments.length }} Departments</div>
                  <p>Browse specialty care and availability.</p>
                </div>
              </div>
              <div class="panel-item">
                <div class="panel-icon">03</div>
                <div>
                  <div class="panel-title">Secure Profile</div>
                  <p>Keep contact details current.</p>
                </div>
              </div>
            </div>
          </div>
          <div class="floating-card">
            <div class="floating-title">Patient tips</div>
            <ul>
              <li>Confirm upcoming slots</li>
              <li>Update contact info</li>
              <li>Check department details</li>
            </ul>
          </div>
        </div>
      </header>

      <div class="dashboard-grid">
        <section class="dashboard-card">
          <div class="card-head">
            <div>
              <h5>Your Profile</h5>
              <p>Review and update your personal details.</p>
            </div>
          </div>
          <div v-if="error" class="alert danger">
            {{ error }}
          </div>
          <div class="card-body">
            <div v-if="editMode" class="form-grid">
              <div class="field">
                <label>Name</label>
                <input v-model="form.name" />
              </div>
              <div class="field">
                <label>Contact</label>
                <input v-model="form.contact" />
              </div>
              <div class="field">
                <label>Age</label>
                <input v-model.number="form.age" type="number" />
              </div>
              <div class="field">
                <label>Gender</label>
                <input v-model="form.gender" />
              </div>
              <div class="muted-text">Email: {{ patient.email }}</div>
              <button class="btn-primary btn-sm" @click="updateProfile" :disabled="saving">
                {{ saving ? "Updating..." : "Update Profile" }}
              </button>
            </div>
            <div v-else class="profile-summary">
              <p>Name: {{ patient.name }}</p>
              <p>Email: {{ patient.email }}</p>
              <p>Contact: {{ patient.contact }}</p>
              <p>Age: {{ patient.age }}</p>
              <p>Gender: {{ patient.gender }}</p>
              <button class="btn-primary btn-sm" @click="toggleEdit">Update Profile</button>
            </div>
          </div>
        </section>

        <section class="dashboard-card">
          <div class="card-head">
            <h5>Departments</h5>
            <span class="pill-count">{{ departments.length }} available</span>
          </div>
          <div class="card-body">
            <div v-if="departments.length === 0" class="empty-state">
              No departments available.
            </div>
            <div v-else class="stack-rows">
              <div v-for="dept in departments" :key="dept" class="dept-row">
                <span>{{ dept }}</span>
                <button class="btn-ghost btn-sm" @click="goToDepartment(dept)">View Details</button>
              </div>
            </div>
          </div>
        </section>

        <section class="dashboard-card">
          <div class="card-head">
            <h5>Upcoming Appointments</h5>
            <span class="pill-count">{{ appointments.length }} upcoming</span>
          </div>
          <div class="card-body p-0">
            <div class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody v-if="appointments.length > 0">
                  <tr v-for="(a, index) in appointments" :key="a.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ a.doctor_name }}</td>
                    <td>{{ a.department }}</td>
                    <td>{{ a.date }}</td>
                    <td>{{ a.time }}</td>
                    <td>
                      <button class="btn-danger btn-sm" @click="cancelAppointment(a.id)">
                        Cancel
                      </button>
                    </td>
                  </tr>
                </tbody>
                <tbody v-else>
                  <tr>
                    <td colspan="6" class="empty-cell">No upcoming appointments</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p v-if="cancelNotice" class="alert success">{{ cancelNotice }}</p>
            <p class="muted-note">
              Please arrive at least 15 minutes early. You can cancel appointments from here.
            </p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { clearSession } from "../utils/session"

const router = useRouter();

const loading = ref(true);
const patient = ref({
  name: "",
  email: "",
  contact: "",
  age: "",
  gender: ""
});
const appointments = ref([]);
const departments = ref([]);
const editMode = ref(false);
const saving = ref(false);
const error = ref("");
const cancelNotice = ref("");
const form = ref({
  name: "",
  contact: "",
  age: "",
  gender: ""
});

const syncForm = () => {
  form.value = {
    name: patient.value.name || "",
    contact: patient.value.contact || "",
    age: patient.value.age ?? "",
    gender: patient.value.gender || ""
  };
};

const loadDashboard = async () => {
  try {
    const res = await api.get("/patient/dashboard");
    patient.value = res.data.patient;
    appointments.value = res.data.appointments || [];
    departments.value = res.data.departments || [];
    syncForm();
  } catch (err) {
    console.error("Failed to load dashboard", err);
    error.value = "Failed to load dashboard";
  } finally {
    loading.value = false;
  }
};

onMounted(loadDashboard);

const cancelAppointment = async (id) => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  cancelNotice.value = "";
  try {
    await api.put(`/appointments/${id}/cancel`);
    appointments.value = appointments.value.filter((item) => item.id !== id);
    cancelNotice.value = "Appointment canceled.";
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to cancel appointment";
  }
};

const toggleEdit = () => {
  editMode.value = !editMode.value;
  if (editMode.value) {
    syncForm();
  }
};

const updateProfile = async () => {
  saving.value = true;
  error.value = "";
  try {
    await api.put("/patient/profile", {
      name: form.value.name,
      contact: form.value.contact,
      age: form.value.age,
      gender: form.value.gender
    });
    await loadDashboard();
    editMode.value = false;
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      err.response?.data?.msg ||
      "Failed to update profile";
  } finally {
    saving.value = false;
  }
};

const goToHistory = () => {
  router.push("/patient/history");
};

const goToDepartment = (dept) => {
  router.push({ path: `/patient/departments/${encodeURIComponent(dept)}` });
};

const logout = () => {
  clearSession()
  router.push("/");
};

const goBackPage = () => {
  router.back();
};
</script>

<style scoped>
.patient-shell {
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

.loading-card {
  margin-top: 40px;
  background: #ffffff;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
  display: grid;
  justify-items: center;
  gap: 12px;
  color: #475569;
}

.spinner {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 3px solid rgba(15, 118, 110, 0.2);
  border-top-color: #0f766e;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.hero-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: center;
  margin-top: 40px;
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

.btn-danger {
  border: none;
  border-radius: 999px;
  padding: 0.45rem 0.9rem;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  background: rgba(239, 68, 68, 0.16);
  color: #b91c1c;
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

.dashboard-grid {
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

.card-body {
  margin-top: 18px;
}

.form-grid {
  display: grid;
  gap: 12px;
  max-width: 420px;
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
  padding: 0.75rem 1rem;
  border-radius: 12px;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
  font-weight: 600;
  color: #0f172a;
}

.profile-summary {
  display: grid;
  gap: 6px;
  color: #475569;
}

.muted-text {
  font-size: 0.85rem;
  color: #64748b;
}

.pill-count {
  background: rgba(15, 118, 110, 0.12);
  color: #0f766e;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.stack-rows {
  display: grid;
  gap: 12px;
}

.dept-row {
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  padding: 14px 16px;
  background: #ffffff;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
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

.muted-note {
  margin: 16px 0 0;
  color: #64748b;
}

.alert {
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-weight: 600;
  margin-top: 12px;
}

.alert.success {
  background: rgba(34, 197, 94, 0.12);
  color: #166534;
}

.alert.danger {
  background: rgba(239, 68, 68, 0.12);
  color: #b91c1c;
}

.empty-state {
  text-align: center;
  color: #64748b;
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

  .dept-row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
