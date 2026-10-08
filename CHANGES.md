# What was fixed

## Security
- Secrets moved out of the code into environment variables (the app refuses to start without them).
- Removed the hidden `admin` / `admin123` login backdoor. Admin is now created with `flask --app app seed-admin`.
- Removed the default doctor password `doctor123`. Admin now receives a random temporary password once.
- Blacklisted or deleted users are rejected immediately, even with an old token (JWT revocation check).
- Missing or expired tokens return a proper 401 (`PROPAGATE_EXCEPTIONS`) and the frontend logs the user out.
- CORS origins configurable; HTML in monthly reports escaped; CSV export protected from formula injection; server file path no longer emailed.

## Bugs and business logic
- Deleting a doctor no longer silently deletes patients' medical records (blocked with a clear message).
- Booking checks: doctor exists and is active, date is available, not in the past, no double-booking.
- Appointment status changes only from `Scheduled`.
- A doctor can only add records for their own patients.
- Availability update validates everything first, so a bad row can't wipe existing data.
- Admin search results no longer show stale cached data; moving a doctor between departments refreshes both lists.
- Patients no longer see past dates or blacklisted doctors' availability.
- Bad or missing input now returns a clear 400 instead of crashing with a 500 (new `validators.py`).
- Duplicate phone numbers and mixed-case emails handled.
- Export button no longer crashes when Redis isn't running.
- Removed dead code (`PatientHistoryAPI` was never registered).

## Frontend
- Role-based route guards, so pages can't be opened without logging in.
- Central session helper and axios 401 handler; logout code no longer copy-pasted.
- Renamed `DoctorAvailiabilty.vue` and `Patienthistory.vue` (typos); removed an empty store file.
- API URL defaults to the local backend; `.env.development` included.
- Add Doctor page shows the temporary password.

## Project hygiene
- Removed `venv`, `__pycache__`, the committed database and junk files.
- New README, `.gitignore`, `.env.example`, one-click Windows run scripts.
- pytest suite and GitHub Actions CI (tests + frontend build).
