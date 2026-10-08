from conftest import ADMIN_PASSWORD


def test_patient_can_register_and_login(h):
    assert h.register_patient().status_code == 201
    res = h.c.post("/auth/patient/login", json={"email": "pat@example.com", "password": "Password1"})
    assert res.status_code == 200
    assert res.get_json()["role"] == "patient"


def test_register_rejects_bad_email(h):
    res = h.register_patient(email="not-an-email")
    assert res.status_code == 400


def test_register_rejects_short_password(h):
    res = h.register_patient(password="short")
    assert res.status_code == 400


def test_duplicate_email_and_contact_rejected(h):
    assert h.register_patient().status_code == 201
    assert h.register_patient().status_code == 400
    # different email but same phone number
    assert h.register_patient(email="other@example.com").status_code == 400


def test_login_with_missing_fields_is_400_not_500(client):
    assert client.post("/auth/patient/login", json={}).status_code == 400
    assert client.post("/auth/doctor/login", json={"email": "a@b.co"}).status_code == 400


def test_wrong_password_is_401(h):
    h.register_patient()
    res = h.c.post("/auth/patient/login", json={"email": "pat@example.com", "password": "WrongPass1"})
    assert res.status_code == 401


def test_old_admin_backdoor_is_gone(client):
    res = client.post("/auth/admin/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 401


def test_admin_can_login_with_real_password(client):
    res = client.post("/auth/admin/login", json={"username": "admin", "password": ADMIN_PASSWORD})
    assert res.status_code == 200
    assert res.get_json()["role"] == "admin"
