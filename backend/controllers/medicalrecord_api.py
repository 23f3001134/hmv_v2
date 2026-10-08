from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource

from controllers.cache_utils import delete_keys, key_doctor_dashboard, key_patient_records
from controllers.models import db, MedicalRecord, Patient, Appointment
from controllers.validators import (
    handle_validation,
    get_json_body,
    require_fields,
    clean_text,
    clean_int,
    optional_text,
)


class MedicalRecordAPI(Resource):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "doctor":
            return {"message": "Only doctors can view records"}, 403
        patient_id = request.args.get("patient_id", type=int)

        query = (
            db.session.query(MedicalRecord, Patient)
            .join(Patient, MedicalRecord.patient_id == Patient.id)
            .filter(MedicalRecord.doctor_id == user_id)
            .order_by(MedicalRecord.record_date.desc())
        )

        if patient_id:
            query = query.filter(MedicalRecord.patient_id == patient_id)

        records = query.all()

        return [
            {
                "id": r.id,
                "patient_id": p.id,
                "patient_name": p.name,
                "visit_type": r.visit_type,
                "diagnosis": r.diagnosis,
                "prescription": r.prescription,
                "medicine": r.medicine,
                "record_date": r.record_date.strftime("%Y-%m-%d")
            }
            for r, p in records
        ], 200

    @jwt_required()
    @handle_validation
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "doctor":
            return {"message": "Only doctors can add records"}, 403

        data = get_json_body()
        require_fields(data, "patient_id", "diagnosis")
        patient_id = clean_int(data, "patient_id", 1, 2_000_000_000)

        patient = db.session.get(Patient, patient_id)
        if not patient:
            return {"message": "Patient not found"}, 404

        # A doctor may only write records for patients they have an appointment with.
        is_their_patient = Appointment.query.filter_by(
            doctor_id=user_id, patient_id=patient_id
        ).first()
        if not is_their_patient:
            return {"message": "You can only add records for your own patients"}, 403

        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=user_id,
            visit_type=optional_text(data, "visit_type", 50, "In-person"),
            diagnosis=clean_text(data, "diagnosis", 250),
            prescription=optional_text(data, "prescription", 250),
            medicine=optional_text(data, "medicine", 250)
        )

        db.session.add(record)
        db.session.commit()
        delete_keys(
            key_doctor_dashboard(user_id),
            key_patient_records(patient_id)
        )
        return {"message": "Medical record added"}, 201
