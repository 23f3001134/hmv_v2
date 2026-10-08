import secrets

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from controllers.cache_utils import (
    delete_keys,
    key_admin_dashboard,
    key_patient_dashboard,
    key_patient_records,
    key_doctor_dashboard,
    key_patient_department_doctors,
    key_patient_doctor_availability
)
from controllers.models import db, Patient, Doctor, Appointment, MedicalRecord
from controllers.validators import (
    ValidationError,
    handle_validation,
    get_json_body,
    require_fields,
    clean_text,
    clean_email,
    clean_phone,
    clean_password,
    clean_int,
    clean_age,
)


def _is_admin():
    return get_jwt().get("role") == "admin"


class PatientProfileAPI(Resource):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Unauthorized"}, 403

        patient = Patient.query.get_or_404(user_id)

        return {
            "id": patient.id,
            "name": patient.name,
            "email": patient.email,
            "contact": patient.contact,
            "age": patient.age,
            "gender": patient.gender
        }, 200

    @jwt_required()
    @handle_validation
    def put(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Unauthorized"}, 403

        patient = Patient.query.get_or_404(user_id)
        data = get_json_body()

        if data.get("name"):
            patient.name = clean_text(data, "name")

        if data.get("contact"):
            contact = clean_phone(data)
            clash = Patient.query.filter(
                Patient.contact == contact, Patient.id != user_id
            ).first()
            if clash:
                raise ValidationError("Contact number already exists")
            patient.contact = contact

        if data.get("age") not in (None, ""):
            patient.age = clean_age(data)

        if data.get("gender"):
            patient.gender = str(data["gender"]).strip()[:10]

        if data.get("password"):
            patient.password = generate_password_hash(clean_password(data))

        db.session.commit()
        delete_keys(
            key_patient_dashboard(user_id),
            key_patient_records(user_id),
            key_admin_dashboard("")
        )
        return {"message": "Profile updated successfully"}, 200


class DoctorCRUDAPI(Resource):

    @jwt_required()
    def get(self):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        doctors = Doctor.query.all()
        return [
            {
                "id": d.id,
                "doctor_name": d.doctor_name,
                "department": d.department,
                "experience": d.experience,
                "email": d.email,
                "contact": d.contact
            }
            for d in doctors
        ], 200

    @jwt_required()
    @handle_validation
    def post(self):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        data = get_json_body()
        require_fields(data, "doctor_name", "department", "experience", "email", "contact")

        name = clean_text(data, "doctor_name")
        department = clean_text(data, "department", 100)
        experience = clean_int(data, "experience", 0, 70)
        email = clean_email(data)
        contact = clean_phone(data)

        if Doctor.query.filter(func.lower(Doctor.email) == email).first():
            return {"message": "Email already exists"}, 400
        if Doctor.query.filter_by(contact=contact).first():
            return {"message": "Contact already exists"}, 400

        temp_password = secrets.token_urlsafe(9)

        doctor = Doctor(
            doctor_name=name,
            department=department,
            experience=experience,
            email=email,
            contact=contact,
            password=generate_password_hash(temp_password)
        )

        db.session.add(doctor)
        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_patient_department_doctors(doctor.department)
        )
        # Shown to the admin ONCE so they can pass it to the doctor.
        return {
            "message": "Doctor added successfully",
            "temporary_password": temp_password
        }, 201


class DoctorPasswordResetAPI(Resource):

    @jwt_required()
    def post(self, doctor_id):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        doctor = Doctor.query.get_or_404(doctor_id)
        temp_password = secrets.token_urlsafe(9)
        doctor.password = generate_password_hash(temp_password)
        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_doctor_dashboard(doctor_id)
        )
        return {
            "message": "Doctor password reset",
            "temporary_password": temp_password
        }, 200


class DoctorDetailAPI(Resource):

    @jwt_required()
    @handle_validation
    def put(self, doctor_id):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        doctor = Doctor.query.get_or_404(doctor_id)
        data = get_json_body()
        old_department = doctor.department

        if "doctor_name" in data:
            doctor.doctor_name = clean_text(data, "doctor_name")

        if "department" in data:
            doctor.department = clean_text(data, "department", 100)

        if "experience" in data:
            doctor.experience = clean_int(data, "experience", 0, 70)

        if "email" in data:
            email = clean_email(data)
            clash = Doctor.query.filter(
                func.lower(Doctor.email) == email, Doctor.id != doctor_id
            ).first()
            if clash:
                return {"message": "Email already exists"}, 400
            doctor.email = email

        if "contact" in data:
            contact = clean_phone(data)
            clash = Doctor.query.filter(
                Doctor.contact == contact, Doctor.id != doctor_id
            ).first()
            if clash:
                return {"message": "Contact already exists"}, 400
            doctor.contact = contact

        if data.get("password"):
            doctor.password = generate_password_hash(clean_password(data))

        db.session.commit()
        # Clear BOTH departments so a doctor who moved does not linger in the old list.
        delete_keys(
            key_admin_dashboard(""),
            key_doctor_dashboard(doctor_id),
            key_patient_department_doctors(old_department),
            key_patient_department_doctors(doctor.department)
        )
        return {"message": "Doctor updated successfully"}, 200

    @jwt_required()
    def delete(self, doctor_id):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        doctor = Doctor.query.get_or_404(doctor_id)

        # Deleting a doctor would also delete their appointments and, worse,
        # every patient's medical records written by them. Block that.
        has_records = MedicalRecord.query.filter_by(doctor_id=doctor_id).first() is not None
        has_appointments = Appointment.query.filter_by(doctor_id=doctor_id).first() is not None
        if has_records or has_appointments:
            return {
                "message": (
                    "This doctor has appointments or medical records and cannot be "
                    "deleted. Blacklist the doctor instead."
                )
            }, 409

        department = doctor.department
        db.session.delete(doctor)
        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_doctor_dashboard(doctor_id),
            key_patient_department_doctors(department),
            key_patient_doctor_availability(doctor_id)
        )
        return {"message": "Doctor deleted successfully"}, 200


class DoctorBlacklistAPI(Resource):

    @jwt_required()
    def put(self, doctor_id):
        if not _is_admin():
            return {"message": "Admin only"}, 403

        doctor = Doctor.query.get_or_404(doctor_id)
        data = request.get_json(silent=True) or {}
        if "is_blacklisted" in data:
            doctor.is_blacklisted = bool(data["is_blacklisted"])
        else:
            doctor.is_blacklisted = not doctor.is_blacklisted

        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_doctor_dashboard(doctor_id),
            key_patient_department_doctors(doctor.department),
            key_patient_doctor_availability(doctor_id)
        )
        return {
            "message": "Doctor blacklist updated",
            "is_blacklisted": doctor.is_blacklisted
        }, 200
