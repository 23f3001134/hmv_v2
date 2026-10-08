from flask_restful import Resource
from flask import request
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.security import generate_password_hash

from controllers.models import db, Patient, MedicalRecord, Doctor
from controllers.validators import (
    handle_validation, get_json_body, clean_text, clean_email, clean_phone, clean_password, clean_age
)
from controllers.cache_utils import (
    delete_keys,
    key_admin_dashboard,
    key_patient_dashboard,
    key_patient_records
)


class AdminPatientDetailAPI(Resource):

    @jwt_required()
    def get(self, patient_id):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        patient = Patient.query.get_or_404(patient_id)
        return {
            "id": patient.id,
            "name": patient.name,
            "email": patient.email,
            "contact": patient.contact,
            "age": patient.age,
            "gender": patient.gender,
            "is_blacklisted": patient.is_blacklisted
        }, 200

    @jwt_required()
    @handle_validation
    def put(self, patient_id):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        patient = Patient.query.get_or_404(patient_id)
        data = get_json_body()

        if "email" in data:
            email = clean_email(data)
            clash = Patient.query.filter(
                func.lower(Patient.email) == email, Patient.id != patient_id
            ).first()
            if clash:
                return {"message": "Email already exists"}, 400
            patient.email = email

        if "contact" in data:
            contact = clean_phone(data)
            clash = Patient.query.filter(
                Patient.contact == contact, Patient.id != patient_id
            ).first()
            if clash:
                return {"message": "Contact already exists"}, 400
            patient.contact = contact

        if "name" in data:
            patient.name = clean_text(data, "name")
        if data.get("age") not in (None, ""):
            patient.age = clean_age(data)
        if data.get("gender"):
            patient.gender = str(data["gender"]).strip()[:10]

        if data.get("password"):
            patient.password = generate_password_hash(clean_password(data))

        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_patient_dashboard(patient_id),
            key_patient_records(patient_id)
        )
        return {"message": "Patient updated successfully"}, 200

    @jwt_required()
    def delete(self, patient_id):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_patient_dashboard(patient_id),
            key_patient_records(patient_id)
        )
        return {"message": "Patient deleted successfully"}, 200


class AdminPatientRecordsAPI(Resource):

    @jwt_required()
    def get(self, patient_id):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        records = (
            db.session.query(MedicalRecord, Doctor)
            .join(Doctor, MedicalRecord.doctor_id == Doctor.id)
            .filter(MedicalRecord.patient_id == patient_id)
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


class AdminPatientBlacklistAPI(Resource):

    @jwt_required()
    def put(self, patient_id):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Admin only"}, 403

        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json() or {}
        if "is_blacklisted" in data:
            patient.is_blacklisted = bool(data["is_blacklisted"])
        else:
            patient.is_blacklisted = not patient.is_blacklisted

        db.session.commit()
        delete_keys(
            key_admin_dashboard(""),
            key_patient_dashboard(patient_id),
            key_patient_records(patient_id)
        )
        return {
            "message": "Patient blacklist updated",
            "is_blacklisted": patient.is_blacklisted
        }, 200
