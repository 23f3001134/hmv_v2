# Hospital Management System V2: Frontend

Vue 3 + Vite + Bootstrap single-page app. It talks to the Flask API in `../backend`.

## Run
```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # production build in dist/
```

## Configuration
The API address comes from `VITE_API_BASE_URL`.
- Local: `.env.development` already points to `http://127.0.0.1:5000`.
- Production (Vercel): set `VITE_API_BASE_URL` in the project's Environment Variables.

## Structure
- `src/views/`: one file per page (login pages, dashboards, history, availability)
- `src/components/`: reusable cards and layout (Navbar, Footer, doctor dashboard cards)
- `src/router/index.js`: routes plus **role-based route guards** (`meta.roles`)
- `src/services/api.js`: axios instance that adds the JWT and logs the user out on a 401
- `src/utils/session.js`: token and role helpers used everywhere
