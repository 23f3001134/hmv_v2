from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.database import db
from controllers.models import Admin, Patient, Doctor
from controllers.validators import (
    ValidationError,
    get_json_body,
    require_fields,
    clean_text,
    clean_email,
    clean_phone,
    clean_password,
    clean_age,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"message": err.message}), err.status


def _token_response(user_id, role):
    token = create_access_token(
        identity=str(user_id),
        additional_claims={"role": role}
    )
    return jsonify({"access_token": token, "role": role})


@auth_bp.route("/patient/register", methods=["POST"])
def patient_register():
    data = get_json_body()
    require_fields(data, "name", "email", "contact", "password")

    name = clean_text(data, "name")
    email = clean_email(data)
    contact = clean_phone(data)
    password = clean_password(data)
    age = clean_age(data)
    gender = str(data.get("gender") or "Unknown").strip()[:10]

    if Patient.query.filter(func.lower(Patient.email) == email).first():
        return jsonify({"message": "Email already exists"}), 400
    if Patient.query.filter_by(contact=contact).first():
        return jsonify({"message": "Contact number already exists"}), 400

    patient = Patient(
        name=name,
        email=email,
        contact=contact,
        password=generate_password_hash(password),
        age=age,
        gender=gender
    )

    try:
        db.session.add(patient)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email or contact already exists"}), 400

    return jsonify({"message": "Patient registered successfully"}), 201


@auth_bp.route("/patient/login", methods=["POST"])
def patient_login():
    data = get_json_body()
    require_fields(data, "email", "password")
    email = str(data["email"]).strip().lower()

    patient = Patient.query.filter(func.lower(Patient.email) == email).first()

    if not patient or not check_password_hash(patient.password, str(data["password"])):
        return jsonify({"message": "Invalid credentials"}), 401

    if patient.is_blacklisted:
        return jsonify({"message": "Patient is blacklisted"}), 403

    return _token_response(patient.id, "patient")


@auth_bp.route("/doctor/login", methods=["POST"])
def doctor_login():
    data = get_json_body()
    require_fields(data, "email", "password")
    email = str(data["email"]).strip().lower()

    doctor = Doctor.query.filter(func.lower(Doctor.email) == email).first()

    if not doctor or not check_password_hash(doctor.password, str(data["password"])):
        return jsonify({"message": "Invalid credentials"}), 401

    if doctor.is_blacklisted:
        return jsonify({"message": "Doctor is blacklisted"}), 403

    return _token_response(doctor.id, "doctor")


@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = get_json_body()
    require_fields(data, "username", "password")
    username = str(data["username"]).strip()

    admin = Admin.query.filter_by(username=username).first()

    # No auto-creation and no hardcoded fallback password here.
    # The admin account is created with:  flask --app app seed-admin
    if not admin or not check_password_hash(admin.password, str(data["password"])):
        return jsonify({"message": "Invalid admin credentials"}), 401

    return _token_response(admin.id, "admin")
