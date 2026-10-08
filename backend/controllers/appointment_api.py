from datetime import date, datetime

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource

from controllers.cache_utils import (
    delete_keys,
    key_patient_dashboard,
    key_doctor_dashboard,
    key_admin_dashboard
)
from controllers.models import db, Appointment, Doctor, DoctorAvailability
from controllers.validators import (
    ValidationError,
    handle_validation,
    get_json_body,
    require_fields,
)


class AppointmentAPI(Resource):

    @jwt_required()
    @handle_validation
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Only patients can book appointments"}, 403

        data = get_json_body()
        require_fields(data, "doctor_id", "appointment_date", "appointment_time")

        try:
            doctor_id = int(data["doctor_id"])
            date_obj = datetime.strptime(str(data["appointment_date"]), "%Y-%m-%d").date()
            time_obj = datetime.strptime(str(data["appointment_time"]), "%H:%M").time()
        except (ValueError, TypeError):
            raise ValidationError("Invalid doctor, date or time")

        if date_obj < date.today():
            raise ValidationError("You cannot book an appointment in the past")

        doctor = db.session.get(Doctor, doctor_id)
        if not doctor or doctor.is_blacklisted:
            return {"message": "This doctor is not available"}, 404

        has_availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id, date=date_obj
        ).first()
        if not has_availability:
            raise ValidationError("The doctor has no availability on this date")

        doctor_busy = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=date_obj,
            appointment_time=time_obj,
            status="Scheduled"
        ).first()
        if doctor_busy:
            return {"message": "This time is already booked. Please choose another time."}, 409

        patient_busy = Appointment.query.filter_by(
            patient_id=user_id,
            appointment_date=date_obj,
            appointment_time=time_obj,
            status="Scheduled"
        ).first()
        if patient_busy:
            return {"message": "You already have an appointment at this time."}, 409

        appointment = Appointment(
            patient_id=user_id,
            doctor_id=doctor_id,
            appointment_date=date_obj,
            appointment_time=time_obj
        )

        db.session.add(appointment)
        db.session.commit()
        delete_keys(
            key_patient_dashboard(user_id),
            key_doctor_dashboard(doctor_id),
            key_admin_dashboard("")
        )
        return {"message": "Appointment booked successfully"}, 201


class AppointmentStatusAPI(Resource):

    @jwt_required()
    @handle_validation
    def put(self, appointment_id):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "doctor":
            return {"message": "Only doctors can update status"}, 403

        data = get_json_body()
        status = str(data.get("status") or "").strip()
        if status not in {"Completed", "Cancelled"}:
            raise ValidationError("Invalid status")

        appointment = Appointment.query.get_or_404(appointment_id)
        if appointment.doctor_id != user_id:
            return {"message": "Unauthorized"}, 403

        if appointment.status != "Scheduled":
            raise ValidationError(f"This appointment is already {appointment.status}")

        appointment.status = status
        db.session.commit()
        delete_keys(
            key_doctor_dashboard(user_id),
            key_patient_dashboard(appointment.patient_id),
            key_admin_dashboard("")
        )
        return {"message": "Status updated"}, 200


class AppointmentCancelAPI(Resource):

    @jwt_required()
    @handle_validation
    def put(self, appointment_id):
        user_id = int(get_jwt_identity())
        role = get_jwt().get("role")

        if role != "patient":
            return {"message": "Only patients can cancel"}, 403

        appointment = Appointment.query.get_or_404(appointment_id)
        if appointment.patient_id != user_id:
            return {"message": "Unauthorized"}, 403

        if appointment.status != "Scheduled":
            raise ValidationError(f"This appointment is already {appointment.status}")

        appointment.status = "Cancelled"
        db.session.commit()
        delete_keys(
            key_patient_dashboard(user_id),
            key_doctor_dashboard(appointment.doctor_id),
            key_admin_dashboard("")
        )
        return {"message": "Appointment cancelled"}, 200
