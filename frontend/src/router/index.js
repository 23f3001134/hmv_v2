import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";
import PatientRegister from "../views/PatientRegister.vue";
import PatientLogin from "../views/PatientLogin.vue";
import DoctorLogin from "../views/DoctorLogin.vue";
import AdminLogin from "../views/AdminLogin.vue";

import PatientDashboard from "../views/PatientDashboard.vue";
import DoctorDashboard from "../views/DoctorDashboard.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import AddDoctor from "../views/AddDoctor.vue";
import PatientHistory from "../views/PatientHistory.vue";
import UpdatePatientHistory from "../views/UpdatePatientHistory.vue";
import DoctorAvailability from "../views/DoctorAvailability.vue";
import ViewDetails from "../views/ViewDetails.vue";

import { getToken, getRole, loginPathFor, dashboardPathFor } from "../utils/session";

// meta.roles = who may open the page. Pages without it are public.
const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/patient/register", name: "PatientRegister", component: PatientRegister },
  { path: "/patient/login", name: "PatientLogin", component: PatientLogin },
  { path: "/doctor/login", name: "DoctorLogin", component: DoctorLogin },
  { path: "/admin/login", name: "AdminLogin", component: AdminLogin },

  {
    path: "/patient/dashboard",
    name: "PatientDashboard",
    component: PatientDashboard,
    meta: { roles: ["patient"] }
  },
  {
    path: "/doctor/dashboard",
    name: "DoctorDashboard",
    component: DoctorDashboard,
    meta: { roles: ["doctor"] }
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { roles: ["admin"] }
  },
  {
    path: "/add_doctor",
    name: "AddDoctor",
    component: AddDoctor,
    meta: { roles: ["admin"] }
  },
  {
    // shared page: patients see their own history, doctors/admins see a patient's
    path: "/patient/history",
    name: "PatientHistory",
    component: PatientHistory,
    meta: { roles: ["patient", "doctor", "admin"] }
  },
  {
    path: "/patient/departments/:department",
    name: "ViewDetails",
    component: ViewDetails,
    props: true,
    meta: { roles: ["patient"] }
  },
  {
    path: "/patient/history/update",
    name: "UpdatePatientHistory",
    component: UpdatePatientHistory,
    meta: { roles: ["doctor"] }
  },
  {
    path: "/doctor/availability",
    name: "DoctorAvailability",
    component: DoctorAvailability,
    meta: { roles: ["doctor"] }
  },

  // anything unknown goes home instead of showing a blank page
  { path: "/:pathMatch(.*)*", redirect: "/" }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  const allowedRoles = to.meta.roles;
  if (!allowedRoles) return true;

  const token = getToken();
  const role = getRole();

  if (!token) return loginPathFor(allowedRoles[0]);
  if (!allowedRoles.includes(role)) return dashboardPathFor(role);
  return true;
});

export default router;
