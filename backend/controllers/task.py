import csv
import io
import os
from datetime import date, datetime, timedelta
from html import escape

from flask import current_app

from app import celery
from controllers.models import db, Appointment, Patient, Doctor, MedicalRecord
from notifications import notify_user


def _csv_safe(value):
    """Stop cells like '=cmd()' from running as formulas when opened in Excel."""
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def _month_range(target_date):
    first_day = target_date.replace(day=1)
    next_month = (first_day + timedelta(days=32)).replace(day=1)
    last_day = next_month - timedelta(days=1)
    return first_day, last_day


@celery.task
def send_daily_reminders():
    today = date.today()

    appointments = (
        db.session.query(Appointment, Patient, Doctor)
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(
            Appointment.appointment_date == today,
            Appointment.status == "Scheduled"
        )
        .order_by(Appointment.appointment_time)
        .all()
    )

    for appointment, patient, doctor in appointments:
        time_str = appointment.appointment_time.strftime("%H:%M")
        message = (
            f"Reminder: You have an appointment today at {time_str} with "
            f"Dr. {doctor.doctor_name} ({doctor.department})."
        )
        notify_user(
            patient.email,
            subject="Appointment Reminder",
            message=message
        )


@celery.task
def send_monthly_activity_reports():
    today = date.today()
    month_start, month_end = _month_range(today - timedelta(days=1))

    doctors = Doctor.query.order_by(Doctor.doctor_name).all()

    for doctor in doctors:
        appointments = (
            db.session.query(Appointment, Patient)
            .join(Patient, Appointment.patient_id == Patient.id)
            .filter(
                Appointment.doctor_id == doctor.id,
                Appointment.appointment_date >= month_start,
                Appointment.appointment_date <= month_end
            )
            .order_by(Appointment.appointment_date, Appointment.appointment_time)
            .all()
        )

        records = (
            db.session.query(MedicalRecord, Patient)
            .join(Patient, MedicalRecord.patient_id == Patient.id)
            .filter(
                MedicalRecord.doctor_id == doctor.id,
                MedicalRecord.record_date >= datetime.combine(month_start, datetime.min.time()),
                MedicalRecord.record_date <= datetime.combine(month_end, datetime.max.time())
            )
            .order_by(MedicalRecord.record_date)
            .all()
        )

        html = _render_monthly_report_html(doctor, appointments, records, month_start, month_end)
        subject = f"Monthly Activity Report ({month_start:%b %Y})"
        message = f"Monthly activity report for {month_start:%B %Y}."
        notify_user(doctor.email, subject=subject, message=message, html_body=html)


@celery.task
def export_patient_treatments_csv(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return {"status": "not_found"}

    records = (
        db.session.query(MedicalRecord, Doctor)
        .join(Doctor, MedicalRecord.doctor_id == Doctor.id)
        .filter(MedicalRecord.patient_id == patient_id)
        .order_by(MedicalRecord.record_date.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "user_id",
        "username",
        "consulting_doctor",
        "appointment_date",
        "diagnosis",
        "prescription",
        "medicine",
        "next_visit_suggested"
    ])

    for record, doctor in records:
        writer.writerow([
            patient.id,
            _csv_safe(patient.name),
            _csv_safe(doctor.doctor_name),
            record.record_date.strftime("%Y-%m-%d"),
            _csv_safe(record.diagnosis),
            _csv_safe(record.prescription),
            _csv_safe(record.medicine),
            ""
        ])

    csv_content = output.getvalue().encode("utf-8")
    filename = f"treatment_export_patient_{patient.id}_{date.today():%Y%m%d}.csv"
    export_dir = os.path.join(current_app.root_path, current_app.config["EXPORT_DIR"])
    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, filename)

    with open(file_path, "wb") as f:
        f.write(csv_content)

    notify_user(
        patient.email,
        subject="Your Treatment Export Is Ready",
        message="Your treatment history export is ready. The CSV is attached.",
        html_body="<p>Your treatment history export is ready. The CSV is attached.</p>",
        attachments=[{"filename": filename, "content": csv_content}]
    )

    return {"status": "sent", "records": len(records), "file_path": file_path}


def _render_monthly_report_html(doctor, appointments, records, month_start, month_end):
    appointment_rows = "".join(
        f"<tr><td>{a.appointment_date:%Y-%m-%d}</td>"
        f"<td>{a.appointment_time:%H:%M}</td>"
        f"<td>{escape(p.name)}</td>"
        f"<td>{escape(a.status)}</td></tr>"
        for a, p in appointments
    ) or "<tr><td colspan='4'>No appointments</td></tr>"

    record_rows = "".join(
        f"<tr><td>{r.record_date:%Y-%m-%d}</td>"
        f"<td>{escape(p.name)}</td>"
        f"<td>{escape(r.diagnosis)}</td>"
        f"<td>{escape(r.prescription or '')}</td>"
        f"<td>{escape(r.medicine or '')}</td></tr>"
        for r, p in records
    ) or "<tr><td colspan='5'>No medical records</td></tr>"

    return f"""
    <html>
      <body>
        <h2>Monthly Activity Report</h2>
        <p>Doctor: {escape(doctor.doctor_name)}</p>
        <p>Department: {escape(doctor.department)}</p>
        <p>Period: {month_start:%Y-%m-%d} to {month_end:%Y-%m-%d}</p>
        <h3>Appointments</h3>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr>
            <th>Date</th>
            <th>Time</th>
            <th>Patient</th>
            <th>Status</th>
          </tr>
          {appointment_rows}
        </table>
        <h3>Medical Records</h3>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Diagnosis</th>
            <th>Prescription</th>
            <th>Medicine</th>
          </tr>
          {record_rows}
        </table>
      </body>
    </html>
    """
