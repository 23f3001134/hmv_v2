# Hospital Management System V2

A full-stack hospital management web app with **three roles** (Admin, Doctor, Patient), built with **Flask + Vue 3**.
Patients book appointments, doctors manage availability and treatment records, and admins manage the whole system.

> **Live demo:** _add your Vercel link here_ (the free backend may take ~30 seconds to wake up on the first request)
> **Screenshots:** _add 3-4 images to a `docs/` folder and link them here_

## Features

| Role | What they can do |
|---|---|
| **Admin** | Add / edit / blacklist doctors, edit / blacklist / delete patients, search, view all appointments and any patient's history |
| **Doctor** | See upcoming appointments and assigned patients, publish availability, mark appointments completed or cancelled, add treatment records |
| **Patient** | Register, browse departments and doctors, see availability, book and cancel appointments, view treatment history, edit profile, request a CSV export of their history |

**Business rules enforced by the API**
- A booking needs a real, non-blacklisted doctor who has published availability on that date.
- No past dates. No double-booking of the same doctor or the same patient at the same time.
- A doctor can only write records for patients they have an appointment with.
- Only `Scheduled` appointments can be completed or cancelled.
- A doctor with appointments or medical records cannot be deleted (blacklist instead), so patient records are never lost.
- A blacklisted or deleted account stops working **immediately**, even with an old token.

## Tech stack
- **Backend:** Python, Flask, Flask-RESTful, SQLAlchemy (SQLite by default, PostgreSQL via `DATABASE_URL`), Flask-JWT-Extended, Flask-Caching, Flask-CORS
- **Background jobs:** Celery + Redis (daily appointment reminders, monthly doctor reports, CSV export)
- **Frontend:** Vue 3, Vue Router, Axios, Bootstrap 5, Vite
- **Quality:** pytest test-suite, GitHub Actions CI

## Project structure
```
backend/
  app.py              app setup, JWT behaviour, routes, CLI commands
  config.py           settings read from environment variables
  controllers/        auth, doctor/patient/admin APIs, models, validators, Celery tasks
  tests/              pytest suite
frontend/
  src/views/          pages          src/router/   routes + role guards
  src/components/     reusable UI    src/utils/    session helpers
```

## Run it on your laptop

### Easiest (Windows)
1. Double-click **`run_backend.bat`** and wait until it says the backend is starting.
   The first run creates the virtual environment, installs packages, and prints your **admin password**.
2. Double-click **`run_frontend.bat`**.
3. Open **http://localhost:5173** and log in as admin (`admin` + the password printed in step 1, also saved in `backend/.env`).

### Manual (any OS)
```bash
# backend
cd backend
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python make_env.py               # creates .env with random secrets and prints the admin password
flask --app app init-db
flask --app app seed-admin
python app.py                    # http://127.0.0.1:5000

# frontend (second terminal)
cd frontend
npm install
npm run dev                      # http://localhost:5173
```
You do **not** need Redis locally: `make_env.py` sets `CELERY_ALWAYS_EAGER=true`, so background jobs run inside the request.

### Using your old local data
Copy your old `hospital.db` into `backend/instance/` before the first start. Note that `seed-admin` resets the admin password to the one in `.env`.

## Run the tests
```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

## Environment variables (backend)
| Variable | Required | Purpose |
|---|---|---|
| `SECRET_KEY`, `JWT_SECRET_KEY` | yes | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_USERNAME`, `ADMIN_PASSWORD` | for `seed-admin` | Admin account (password at least 8 characters) |
| `CORS_ORIGINS` | in production | Frontend URL(s), comma separated |
| `DATABASE_URL` | no | Default is SQLite. Use PostgreSQL in production |
| `CACHE_TYPE`, `CACHE_REDIS_URL` | no | `RedisCache` to share the cache between workers |
| `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | for real background jobs | Redis URLs |
| `CELERY_ALWAYS_EAGER` | local only | `true` runs jobs inline, no Redis needed |
| `SMTP_*`, `DEFAULT_GCHAT_WEBHOOK_URL` | no | Where reminders and reports are sent |

See `backend/.env.example`.

## Deployment notes
- **Frontend (Vercel):** set `VITE_API_BASE_URL` to the backend URL.
- **Backend (Render):** set the variables above, then run `flask --app app init-db` and `flask --app app seed-admin` once in the shell. Start command: `gunicorn app:app`.
- **Database:** SQLite files are wiped on Render's free tier when it redeploys. Use a free PostgreSQL instance for real data.
- **Scheduled jobs** need a Celery worker **and** beat process plus Redis. Without them the API works, but reminders and reports will not run.

## API overview
`/auth/{patient|doctor|admin}/login`, `/auth/patient/register`, `/admin/dashboard`, `/admin/doctors[/<id>]`, `/admin/patients/<id>[/records|/blacklist]`, `/doctor/dashboard`, `/doctor/availability`, `/doctor/records`, `/patient/dashboard`, `/patient/profile`, `/patient/records[/export]`, `/patient/departments/<name>/doctors`, `/patient/doctors/<id>/availability`, `/appointments[/<id>/status|/cancel]`

## Known limitations / ideas
- The admin dashboard loads all records at once (add pagination).
- Availability slots are free text such as `09:00-12:00`; replace with time pickers and enforce time ranges.
- Two simultaneous bookings of one slot are blocked by a check, not a database constraint.
- Doctors cannot change their own password yet.
- The JWT is kept in `localStorage`; a hardened version would use httpOnly cookies.
