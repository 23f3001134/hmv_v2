from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from controllers.models import db, Patient, Doctor, Appointment, MedicalRecord
from controllers.cache_utils import (
    get_or_set,
    key_patient_dashboard,
    key_patient_records
)


class PatientDashboardAPI(Resource):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Patient only"}, 403

        cache_key = key_patient_dashboard(user_id)

        def build():
            patient = Patient.query.get_or_404(user_id)

            appointments = (
                db.session.query(Appointment, Doctor)
                .join(Doctor, Appointment.doctor_id == Doctor.id)
                .filter(Appointment.patient_id == user_id)
                .order_by(Appointment.appointment_date, Appointment.appointment_time)
                .all()
            )

            appointments_data = [
                {
                    "id": a.id,
                    "doctor_name": d.doctor_name,
                    "department": d.department,
                    "date": a.appointment_date.strftime("%Y-%m-%d"),
                    "time": a.appointment_time.strftime("%H:%M"),
                    "status": a.status
                }
                for a, d in appointments
            ]

            departments = [
                row[0]
                for row in (
                    db.session.query(Doctor.department)
                    .filter(Doctor.is_blacklisted.is_(False))
                    .distinct()
                    .order_by(Doctor.department)
                    .all()
                )
            ]

            return {
                "patient": {
                    "id": patient.id,
                    "name": patient.name,
                    "email": patient.email,
                    "contact": patient.contact,
                    "age": patient.age,
                    "gender": patient.gender
                },
                "appointments": appointments_data,
                "departments": departments
            }, 200

        return get_or_set(cache_key, build)


class PatientRecordsAPI(Resource):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Patient only"}, 403

        cache_key = key_patient_records(user_id)

        def build():
            records = (
                db.session.query(MedicalRecord, Doctor)
                .join(Doctor, MedicalRecord.doctor_id == Doctor.id)
                .filter(MedicalRecord.patient_id == user_id)
                .order_by(MedicalRecord.record_date.desc())
                .all()
            )

            return [
                {
                    "id": r.id,
                    "doctor_name": d.doctor_name,
                    "visit_type": r.visit_type,
                    "diagnosis": r.diagnosis,
                    "prescription": r.prescription,
                    "medicine": r.medicine,
                    "record_date": r.record_date.strftime("%Y-%m-%d")
                }
                for r, d in records
            ], 200

        return get_or_set(cache_key, build)


class PatientExportAPI(Resource):

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Patient only"}, 403

        from controllers.task import export_patient_treatments_csv
        try:
            task = export_patient_treatments_csv.delay(user_id)
        except Exception:
            current_app.logger.exception("Could not queue export job (is Redis/Celery running?)")
            return {"message": "Export service is unavailable right now. Please try again later."}, 503

        return {
            "message": "Export started. You will receive a notification when it is ready.",
            "task_id": task.id
        }, 202
