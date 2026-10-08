"""Shared test setup. Environment variables are set BEFORE the app is imported,
because config.py refuses to start without secrets."""
import os
import sys
import tempfile

import pytest

_tmp = tempfile.mkdtemp()
ADMIN_PASSWORD = "AdminPass123"

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key"
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp, "test.db").replace("\\", "/")
os.environ["EXPORT_DIR"] = os.path.join(_tmp, "exports")
os.environ["CELERY_ALWAYS_EAGER"] = "true"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash  # noqa: E402

from app import app as flask_app  # noqa: E402
from controllers.models import db, Admin, Doctor, Patient  # noqa: E402
from extensions import cache  # noqa: E402


class Helper:
    """Small wrapper so each test reads like a story."""

    def __init__(self, client):
        self.c = client

    @staticmethod
    def auth(token):
        return {"Authorization": f"Bearer {token}"}

    def admin_token(self):
        res = self.c.post("/auth/admin/login", json={"username": "admin", "password": ADMIN_PASSWORD})
        return res.get_json()["access_token"]

    def register_patient(self, email="pat@example.com", contact="9876543210",
                         password="Password1", name="Pat"):
        return self.c.post("/auth/patient/register", json={
            "name": name, "email": email, "contact": contact,
            "password": password, "age": 30, "gender": "Female"
        })

    def patient_token(self, email="pat@example.com", contact="9876543210", password="Password1"):
        self.register_patient(email=email, contact=contact, password=password)
        res = self.c.post("/auth/patient/login", json={"email": email, "password": password})
        return res.get_json()["access_token"]

    def add_doctor(self, admin_token, email="doc@example.com", contact="9123456780",
                   department="Cardiology"):
        res = self.c.post("/admin/doctors", headers=self.auth(admin_token), json={
            "doctor_name": "Dr Test", "department": department, "experience": 5,
            "email": email, "contact": contact
        })
        return res

    def doctor_token(self, email, password):
        res = self.c.post("/auth/doctor/login", json={"email": email, "password": password})
        return res.get_json()["access_token"]

    @staticmethod
    def doctor_id(email):
        with flask_app.app_context():
            return Doctor.query.filter_by(email=email).first().id

    @staticmethod
    def patient_id(email):
        with flask_app.app_context():
            return Patient.query.filter_by(email=email).first().id

    def doctor_with_availability(self, day, email="doc@example.com", contact="9123456780"):
        """Admin creates a doctor, doctor logs in and publishes one available day."""
        admin = self.admin_token()
        temp = self.add_doctor(admin, email=email, contact=contact).get_json()["temporary_password"]
        token = self.doctor_token(email, temp)
        res = self.c.put("/doctor/availability", headers=self.auth(token), json=[
            {"date": day, "morning_slot": "09:00-12:00", "evening_slot": "15:00-17:00"}
        ])
        assert res.status_code == 200, res.get_json()
        return token, self.doctor_id(email)


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Admin(username="admin", password=generate_password_hash(ADMIN_PASSWORD)))
        db.session.commit()
        cache.clear()
    yield flask_app.test_client()
    with flask_app.app_context():
        db.session.remove()


@pytest.fixture()
def h(client):
    return Helper(client)
