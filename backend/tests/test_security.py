def test_protected_route_needs_login(client):
    assert client.get("/admin/dashboard").status_code == 401


def test_patient_cannot_open_admin_dashboard(h):
    token = h.patient_token()
    res = h.c.get("/admin/dashboard", headers=h.auth(token))
    assert res.status_code == 403


def test_garbage_token_is_401(client):
    res = client.get("/patient/dashboard", headers={"Authorization": "Bearer not.a.token"})
    assert res.status_code == 401


def test_blacklisted_patient_loses_access_immediately(h):
    token = h.patient_token()
    assert h.c.get("/patient/dashboard", headers=h.auth(token)).status_code == 200

    admin = h.admin_token()
    pid = h.patient_id("pat@example.com")
    res = h.c.put(f"/admin/patients/{pid}/blacklist", headers=h.auth(admin),
                  json={"is_blacklisted": True})
    assert res.status_code == 200

    # the OLD token must stop working right away, not after it expires
    assert h.c.get("/patient/dashboard", headers=h.auth(token)).status_code == 401
