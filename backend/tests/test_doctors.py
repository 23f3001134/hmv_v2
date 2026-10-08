from datetime import date, timedelta


def test_admin_adds_doctor_and_doctor_can_login(h):
    admin = h.admin_token()
    res = h.add_doctor(admin)
    assert res.status_code == 201
    temp = res.get_json()["temporary_password"]
    assert temp and temp != "doctor123"

    res = h.c.post("/auth/doctor/login", json={"email": "doc@example.com", "password": temp})
    assert res.status_code == 200
    assert res.get_json()["role"] == "doctor"


def test_old_default_doctor_password_does_not_work(h):
    admin = h.admin_token()
    h.add_doctor(admin)
    res = h.c.post("/auth/doctor/login", json={"email": "doc@example.com", "password": "doctor123"})
    assert res.status_code == 401


def test_duplicate_doctor_email_rejected(h):
    admin = h.admin_token()
    assert h.add_doctor(admin).status_code == 201
    assert h.add_doctor(admin, contact="9000000001").status_code == 400


def test_doctor_with_appointments_cannot_be_deleted(h):
    day = (date.today() + timedelta(days=1)).isoformat()
    _, doctor_id = h.doctor_with_availability(day)
    patient = h.patient_token()
    book = h.c.post("/appointments", headers=h.auth(patient), json={
        "doctor_id": doctor_id, "appointment_date": day, "appointment_time": "09:00"
    })
    assert book.status_code == 201

    admin = h.admin_token()
    res = h.c.delete(f"/admin/doctors/{doctor_id}", headers=h.auth(admin))
    assert res.status_code == 409


def test_doctor_without_history_can_be_deleted(h):
    admin = h.admin_token()
    h.add_doctor(admin)
    doctor_id = h.doctor_id("doc@example.com")
    res = h.c.delete(f"/admin/doctors/{doctor_id}", headers=h.auth(admin))
    assert res.status_code == 200
