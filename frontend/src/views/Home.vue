<template>
  <div class="home-shell">
    <nav class="top-nav">
      <div class="brand">
        <span class="brand-mark">MediSys</span>
        <span class="brand-sub">Smart hospital suite</span>
      </div>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/doctor/login" class="nav-link">Doctor</RouterLink>
        <RouterLink to="/patient/login" class="nav-link">Patient</RouterLink>
        <RouterLink to="/admin/login" class="nav-link">Admin</RouterLink>
      </div>
      <RouterLink class="nav-cta" to="/patient/login">Get Started</RouterLink>
    </nav>

    <main class="hero-grid">
      <section class="hero-content">
        <p class="eyebrow">Hospital Management</p>
        <h1>
          An operating system for
          <span class="accent">modern care</span>.
        </h1>
        <p class="lead">
          MediSys connects doctors, patients, and admins with live scheduling,
          secure records, and clear communication in one place.
        </p>
        <div class="hero-actions">
          <RouterLink class="btn-primary" to="/patient/login">Start as Patient</RouterLink>
          <RouterLink class="btn-ghost" to="/doctor/login">Doctor Portal</RouterLink>
        </div>

        <div class="stats-row">
          <div class="stat-chip">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Access</div>
          </div>
          <div class="stat-chip">
            <div class="stat-value">1 View</div>
            <div class="stat-label">Unified records</div>
          </div>
          <div class="stat-chip">
            <div class="stat-value">3 Roles</div>
            <div class="stat-label">Doctor, Patient, Admin</div>
          </div>
        </div>
      </section>

      <section class="hero-panel">
        <div class="panel-card">
          <div class="panel-header">
            <div>
              <p class="panel-eyebrow">Why MediSys</p>
              <h3>Designed for speed and clarity</h3>
            </div>
            <span class="panel-tag">Secure</span>
          </div>
          <div class="panel-body">
            <div class="panel-item">
              <div class="panel-icon">01</div>
              <div>
                <div class="panel-title">Live appointments</div>
                <p>Keep schedules synced across doctors and patients.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">02</div>
              <div>
                <div class="panel-title">Medical history at hand</div>
                <p>View diagnoses, prescriptions, and notes instantly.</p>
              </div>
            </div>
            <div class="panel-item">
              <div class="panel-icon">03</div>
              <div>
                <div class="panel-title">Streamlined admin flow</div>
                <p>Manage doctors, patients, and departments quickly.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="floating-card">
          <div class="floating-title">Daily Focus</div>
          <ul>
            <li>Morning check-ins</li>
            <li>Appointments tracked</li>
            <li>Follow-up reminders</li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home-shell {
  font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
  min-height: 100vh;
  background:
    radial-gradient(circle at 10% 20%, rgba(14, 165, 165, 0.18), transparent 45%),
    radial-gradient(circle at 90% 12%, rgba(56, 189, 248, 0.16), transparent 40%),
    linear-gradient(180deg, #f6f9fc 0%, #ffffff 70%);
  color: #0f172a;
  padding: 28px clamp(16px, 4vw, 56px) 40px;
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

.hero-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: center;
  margin-top: 40px;
}

.hero-content {
  color: #0f172a;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.65rem;
  color: #0f766e;
  font-weight: 700;
  margin-bottom: 12px;
}

h1 {
  font-family: "DM Serif Display", "Georgia", serif;
  font-size: clamp(2.4rem, 4vw, 3.4rem);
  line-height: 1.05;
  margin-bottom: 16px;
}

.accent {
  color: #0f766e;
}

.lead {
  font-size: 1.05rem;
  color: #475569;
  max-width: 540px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 24px 0;
}

.btn-primary,
.btn-ghost {
  text-decoration: none;
  padding: 0.75rem 1.6rem;
  border-radius: 999px;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
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

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.stat-chip {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
}

.hero-panel {
  display: grid;
  gap: 18px;
  position: relative;
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
  font-size: 1.4rem;
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
