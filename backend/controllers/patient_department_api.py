from datetime import date

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt

from controllers.models import db, Doctor, DoctorAvailability
from controllers.cache_utils import (
    get_or_set,
    key_patient_department_doctors,
    key_patient_doctor_availability
)


class PatientDepartmentDoctorsAPI(Resource):

    @jwt_required()
    def get(self, department):
        role = get_jwt().get("role")
        if role != "patient":
            return {"message": "Patient only"}, 403

        cache_key = key_patient_department_doctors(department)

        def build():
            doctors = (
                db.session.query(Doctor)
                .filter(
                    Doctor.department == department,
                    Doctor.is_blacklisted.is_(False)
                )
                .order_by(Doctor.doctor_name)
                .all()
            )

            return [
                {
                    "id": d.id,
                    "name": d.doctor_name,
                    "department": d.department,
                    "experience": d.experience,
                    "email": d.email,
                    "contact": d.contact
                }
                for d in doctors
            ], 200

        return get_or_set(cache_key, build)


class PatientDoctorAvailabilityAPI(Resource):

    @jwt_required()
    def get(self, doctor_id):
        role = get_jwt().get("role")
        if role != "patient":
            return {"message": "Patient only"}, 403

        doctor = db.session.get(Doctor, doctor_id)
        if not doctor or doctor.is_blacklisted:
            return {"message": "Doctor not found"}, 404

        cache_key = key_patient_doctor_availability(doctor_id)

        def build():
            availability = (
                DoctorAvailability.query
                .filter(
                    DoctorAvailability.doctor_id == doctor_id,
                    DoctorAvailability.date >= date.today()
                )
                .order_by(DoctorAvailability.date)
                .all()
            )

            return [
                {
                    "date": a.date.strftime("%Y-%m-%d"),
                    "morning_slot": a.morning_slot,
                    "evening_slot": a.evening_slot
                }
                for a in availability
            ], 200

        return get_or_set(cache_key, build)
