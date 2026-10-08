from datetime import date, timedelta


def _setup(h):
    day = (date.today() + timedelta(days=1)).isoformat()
    doctor_token, doctor_id = h.doctor_with_availability(day)
    patient = h.patient_token()
    h.c.post("/appointments", headers=h.auth(patient), json={
        "doctor_id": doctor_id, "appointment_date": day, "appointment_time": "09:00"
    })
    return doctor_token, patient, h.patient_id("pat@example.com")


def test_doctor_can_add_record_for_own_patient(h):
    doctor_token, patient_token, patient_id = _setup(h)
    res = h.c.post("/doctor/records", headers=h.auth(doctor_token), json={
        "patient_id": patient_id, "visit_type": "In-person",
        "diagnosis": "Flu", "prescription": "Rest", "medicine": "Paracetamol 500mg"
    })
    assert res.status_code == 201

    mine = h.c.get("/patient/records", headers=h.auth(patient_token)).get_json()
    assert len(mine) == 1
    assert mine[0]["diagnosis"] == "Flu"


def test_doctor_cannot_add_record_for_stranger(h):
    doctor_token, _, _ = _setup(h)
    h.register_patient(email="stranger@example.com", contact="9000011111")
    stranger_id = h.patient_id("stranger@example.com")
    res = h.c.post("/doctor/records", headers=h.auth(doctor_token), json={
        "patient_id": stranger_id, "diagnosis": "Anything"
    })
    assert res.status_code == 403


def test_record_without_diagnosis_is_400_not_500(h):
    doctor_token, _, patient_id = _setup(h)
    res = h.c.post("/doctor/records", headers=h.auth(doctor_token), json={"patient_id": patient_id})
    assert res.status_code == 400
