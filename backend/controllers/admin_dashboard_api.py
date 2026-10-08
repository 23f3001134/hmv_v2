from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt

from controllers.models import Doctor, Patient, Appointment
from controllers.database import db
from controllers.cache_utils import get_or_set, key_admin_dashboard


class AdminDashboardAPI(Resource):

    @jwt_required()
    def get(self):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        search = request.args.get("q", "").strip()

        cache_key = key_admin_dashboard(search)

        def build():
            doctors_query = Doctor.query
            if search:
                doctors_query = doctors_query.filter(
                    Doctor.doctor_name.ilike(f"%{search}%")
                )

            doctors = doctors_query.order_by(Doctor.doctor_name).all()

            doctors_data = [
                {
                    "id": d.id,
                    "name": d.doctor_name,
                    "department": d.department,
                    "experience": d.experience,
                    "email": d.email,
                    "contact": d.contact,
                    "is_blacklisted": d.is_blacklisted
                }
                for d in doctors
            ]

            patients_query = Patient.query
            if search:
                patients_query = patients_query.filter(
                    Patient.name.ilike(f"%{search}%")
                )

            patients = patients_query.order_by(Patient.name).all()

            patients_data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "email": p.email,
                    "contact": p.contact,
                    "age": p.age,
                    "gender": p.gender,
                    "is_blacklisted": p.is_blacklisted
                }
                for p in patients
            ]

            appointments = (
                db.session.query(Appointment, Patient, Doctor)
                .join(Patient, Appointment.patient_id == Patient.id)
                .join(Doctor, Appointment.doctor_id == Doctor.id)
                .order_by(Appointment.appointment_date, Appointment.appointment_time)
                .all()
            )

            appointments_data = [
                {
                    "id": a.id,
                    "patient_id": p.id,
                    "patient_name": p.name,
                    "doctor_name": d.doctor_name,
                    "department": d.department,
                    "date": a.appointment_date.strftime("%Y-%m-%d"),
                    "time": a.appointment_time.strftime("%H:%M"),
                    "status": a.status
                }
                for a, p, d in appointments
            ]

            return {
                "doctors": doctors_data,
                "patients": patients_data,
                "appointments": appointments_data
            }, 200

        # Only the unfiltered dashboard is cached. Search results use other keys that
        # nothing ever cleared, so they showed stale data.
        if search:
            return build()
        return get_or_set(cache_key, build)
