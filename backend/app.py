import os

import click
from celery import Celery
from celery.schedules import crontab
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash

from config import Config
from controllers.models import db, Admin, Patient, Doctor
from extensions import cache
from controllers.auth import auth_bp
from controllers.crud_api import (
    DoctorCRUDAPI,
    DoctorPasswordResetAPI,
    DoctorDetailAPI,
    DoctorBlacklistAPI,
    PatientProfileAPI
)
from controllers.admin_dashboard_api import AdminDashboardAPI
from controllers.patient_dashboard_api import (
    PatientDashboardAPI,
    PatientRecordsAPI,
    PatientExportAPI
)
from controllers.patient_department_api import (
    PatientDepartmentDoctorsAPI,
    PatientDoctorAvailabilityAPI
)
from controllers.admin_patient_api import (
    AdminPatientDetailAPI,
    AdminPatientRecordsAPI,
    AdminPatientBlacklistAPI
)
from controllers.doctor_dashboard_api import DoctorDashboardAPI, DoctorAvailabilityAPI
from controllers.medicalrecord_api import MedicalRecordAPI
from controllers.appointment_api import AppointmentAPI, AppointmentStatusAPI, AppointmentCancelAPI

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=True)

db.init_app(app)
cache.init_app(app)
jwt = JWTManager(app)

api = Api(app)

export_dir = os.path.join(app.root_path, app.config["EXPORT_DIR"])
os.makedirs(export_dir, exist_ok=True)


# ---------------------------------------------------------------------------
# JWT behaviour
# ---------------------------------------------------------------------------
@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    """Reject tokens of users who were blacklisted or deleted AFTER logging in.
    Without this, a blacklisted user keeps working until the token expires."""
    role = jwt_payload.get("role")
    try:
        user_id = int(jwt_payload.get("sub"))
    except (TypeError, ValueError):
        return True

    if role == "patient":
        user = db.session.get(Patient, user_id)
        return user is None or user.is_blacklisted
    if role == "doctor":
        user = db.session.get(Doctor, user_id)
        return user is None or user.is_blacklisted
    if role == "admin":
        return db.session.get(Admin, user_id) is None
    return True


@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({"message": "This account is disabled or no longer exists."}), 401


@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({"message": "Session expired. Please log in again."}), 401


@jwt.unauthorized_loader
def missing_token_response(reason):
    return jsonify({"message": "Please log in first."}), 401


@jwt.invalid_token_loader
def invalid_token_response(reason):
    return jsonify({"message": "Invalid session. Please log in again."}), 401


@app.errorhandler(Exception)
def handle_unexpected_error(err):
    """Return JSON (not an HTML page) for anything we did not expect."""
    if isinstance(err, HTTPException):
        return err
    app.logger.exception("Unhandled error")
    return jsonify({"message": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# Celery (background jobs). Needs Redis for real use.
# For local development without Redis set CELERY_ALWAYS_EAGER=true in .env
# and tasks run immediately inside the request instead.
# ---------------------------------------------------------------------------
def make_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config["CELERY_BROKER_URL"],
        backend=flask_app.config["CELERY_RESULT_BACKEND"]
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)
celery.conf.task_always_eager = os.getenv("CELERY_ALWAYS_EAGER", "false").lower() == "true"
celery.conf.beat_schedule = {
    "daily-reminders": {
        "task": "controllers.task.send_daily_reminders",
        "schedule": crontab(
            hour=app.config["DAILY_REMINDER_HOUR"],
            minute=app.config["DAILY_REMINDER_MINUTE"]
        )
    },
    "monthly-reports": {
        "task": "controllers.task.send_monthly_activity_reports",
        "schedule": crontab(
            day_of_month=1,
            hour=app.config["MONTHLY_REPORT_HOUR"],
            minute=app.config["MONTHLY_REPORT_MINUTE"]
        )
    }
}


@app.route('/')
def home():
    return "Welcome to the API"


app.register_blueprint(auth_bp)

api.add_resource(DoctorCRUDAPI, "/admin/doctors")
api.add_resource(DoctorPasswordResetAPI, "/admin/doctors/<int:doctor_id>/reset-password")
api.add_resource(DoctorDetailAPI, "/admin/doctors/<int:doctor_id>")
api.add_resource(DoctorBlacklistAPI, "/admin/doctors/<int:doctor_id>/blacklist")
api.add_resource(AdminDashboardAPI, "/admin/dashboard")
api.add_resource(DoctorDashboardAPI, "/doctor/dashboard")
api.add_resource(DoctorAvailabilityAPI, "/doctor/availability")
api.add_resource(MedicalRecordAPI, "/doctor/records")
api.add_resource(AppointmentAPI, "/appointments")
api.add_resource(AppointmentStatusAPI, "/appointments/<int:appointment_id>/status")
api.add_resource(AppointmentCancelAPI, "/appointments/<int:appointment_id>/cancel")
api.add_resource(PatientProfileAPI, "/patient/profile")
api.add_resource(PatientDashboardAPI, "/patient/dashboard")
api.add_resource(PatientRecordsAPI, "/patient/records")
api.add_resource(PatientExportAPI, "/patient/records/export")
api.add_resource(PatientDepartmentDoctorsAPI, "/patient/departments/<string:department>/doctors")
api.add_resource(PatientDoctorAvailabilityAPI, "/patient/doctors/<int:doctor_id>/availability")
api.add_resource(AdminPatientDetailAPI, "/admin/patients/<int:patient_id>")
api.add_resource(AdminPatientRecordsAPI, "/admin/patients/<int:patient_id>/records")
api.add_resource(AdminPatientBlacklistAPI, "/admin/patients/<int:patient_id>/blacklist")


# Imported last: task.py does "from app import celery", so celery must exist first.
import controllers.task  # noqa: E402,F401


# ---------------------------------------------------------------------------
# Command-line helpers (replace the old hardcoded admin / admin123)
# ---------------------------------------------------------------------------
@app.cli.command("init-db")
def init_db_command():
    """Create all database tables:  flask --app app init-db"""
    db.create_all()
    click.echo("Database tables created.")


@app.cli.command("seed-admin")
def seed_admin_command():
    """Create (or reset) the admin account from environment variables.

    Needs ADMIN_PASSWORD (min 8 chars). ADMIN_USERNAME is optional (default: admin).
    Run:  flask --app app seed-admin
    """
    username = os.getenv("ADMIN_USERNAME", "admin").strip()
    password = os.getenv("ADMIN_PASSWORD", "")

    if len(password) < 8:
        raise click.ClickException("Set ADMIN_PASSWORD (at least 8 characters) first.")

    db.create_all()
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        admin.password = generate_password_hash(password)
        click.echo(f"Admin '{username}' already existed, password updated.")
    else:
        db.session.add(Admin(username=username, password=generate_password_hash(password)))
        click.echo(f"Admin '{username}' created.")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
