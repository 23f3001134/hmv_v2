import axios from "axios";
import { getToken, getRole, clearSession, loginPathFor } from "../utils/session";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000",
  headers: {
    "Content-Type": "application/json"
  }
});

api.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If the server says "not logged in" (expired token, blacklisted account...),
// clear the stale session and send the user to the right login page.
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status;
    const url = error.config?.url || "";
    const isLoginCall = url.startsWith("/auth/");

    if (status === 401 && !isLoginCall && getToken()) {
      const loginPath = loginPathFor(getRole());
      clearSession();
      window.location.assign(loginPath);
    }
    return Promise.reject(error);
  }
);

export default api;
