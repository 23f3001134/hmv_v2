// One place for everything about the logged-in user, so views don't repeat it.

export const getToken = () => localStorage.getItem("access_token");
export const getRole = () => localStorage.getItem("role");

export const setSession = (token, role) => {
  localStorage.setItem("access_token", token);
  localStorage.setItem("role", role);
};

export const clearSession = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("token");
  localStorage.removeItem("role");
};

export const loginPathFor = (role) => {
  if (role === "patient") return "/patient/login";
  if (role === "doctor") return "/doctor/login";
  if (role === "admin") return "/admin/login";
  return "/";
};

export const dashboardPathFor = (role) => {
  if (role === "patient") return "/patient/dashboard";
  if (role === "doctor") return "/doctor/dashboard";
  if (role === "admin") return "/admin/dashboard";
  return "/";
};
