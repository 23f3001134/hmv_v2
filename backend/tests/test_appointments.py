from datetime import date, timedelta


def _day(offset=1):
    return (date.today() + timedelta(days=offset)).isoformat()


def _book(h, token, doctor_id, day, time="09:00"):
    return h.c.post("/appointments", headers=h.auth(token), json={
        "doctor_id": doctor_id, "appointment_date": day, "appointment_time": time
    })


def test_patient_can_book_available_day(h):
    day = _day()
    _, doctor_id = h.doctor_with_availability(day)
    patient = h.patient_token()
    assert _book(h, patient, doctor_id, day).status_code == 201


def test_same_slot_cannot_be_booked_twice(h):
    day = _day()
    _, doctor_id = h.doctor_with_availability(day)
    first = h.patient_token()
    second = h.patient_token(email="two@example.com", contact="9876500000")
    assert _book(h, first, doctor_id, day).status_code == 201
    assert _book(h, second, doctor_id, day).status_code == 409


def test_cannot_book_in_the_past(h):
    day = _day(-1)
    _, doctor_id = h.doctor_with_availability(_day())
    patient = h.patient_token()
    assert _book(h, patient, doctor_id, day).status_code == 400


def test_cannot_book_day_without_availability(h):
    _, doctor_id = h.doctor_with_availability(_day(1))
    patient = h.patient_token()
    assert _book(h, patient, doctor_id, _day(5)).status_code == 400


def test_cannot_book_unknown_doctor(h):
    patient = h.patient_token()
    assert _book(h, patient, 9999, _day()).status_code == 404


def test_bad_date_format_is_400_not_500(h):
    _, doctor_id = h.doctor_with_availability(_day())
    patient = h.patient_token()
    assert _book(h, patient, doctor_id, "tomorrow").status_code == 400


def test_cancelled_appointment_cannot_be_cancelled_again(h):
    day = _day()
    _, doctor_id = h.doctor_with_availability(day)
    patient = h.patient_token()
    _book(h, patient, doctor_id, day)
    with_id = h.c.get("/patient/dashboard", headers=h.auth(patient)).get_json()
    appointment_id = with_id["appointments"][0]["id"]

    assert h.c.put(f"/appointments/{appointment_id}/cancel", headers=h.auth(patient)).status_code == 200
    assert h.c.put(f"/appointments/{appointment_id}/cancel", headers=h.auth(patient)).status_code == 400


def test_doctor_can_complete_but_not_reopen(h):
    day = _day()
    doctor_token, doctor_id = h.doctor_with_availability(day)
    patient = h.patient_token()
    _book(h, patient, doctor_id, day)
    dash = h.c.get("/doctor/dashboard", headers=h.auth(doctor_token)).get_json()
    appointment_id = dash["upcoming_appointments"][0]["id"]

    done = h.c.put(f"/appointments/{appointment_id}/status", headers=h.auth(doctor_token),
                   json={"status": "Completed"})
    assert done.status_code == 200
    again = h.c.put(f"/appointments/{appointment_id}/status", headers=h.auth(doctor_token),
                    json={"status": "Cancelled"})
    assert again.status_code == 400


def test_bad_availability_does_not_wipe_old_data(h):
    day = _day()
    doctor_token, _ = h.doctor_with_availability(day)
    bad = h.c.put("/doctor/availability", headers=h.auth(doctor_token), json=[
        {"date": "not-a-date", "morning_slot": "09:00-12:00", "evening_slot": "15:00-17:00"}
    ])
    assert bad.status_code == 400
    kept = h.c.get("/doctor/availability", headers=h.auth(doctor_token)).get_json()
    assert len(kept) == 1
