from controllers.database import db
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, default=0)
    gender = db.Column(db.String(10), default="Unknown")
    is_blacklisted = db.Column(db.Boolean, default=False)

    medical_records = db.relationship(
        'MedicalRecord', backref='patient',
        cascade="all, delete-orphan"
    )

    appointments = db.relationship(
        'Appointment', backref='patient',
        cascade="all, delete-orphan"
    )


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    appointments = db.relationship(
        'Appointment', backref='doctor',
        cascade="all, delete-orphan"
    )

    medical_records = db.relationship(
        'MedicalRecord', backref='doctor',
        cascade="all, delete-orphan"
    )

    availability = db.relationship(
        'DoctorAvailability', backref='doctor',
        cascade="all, delete-orphan"
    )


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='Scheduled')


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    visit_type = db.Column(db.String(50))
    diagnosis = db.Column(db.String(250), nullable=False)
    prescription = db.Column(db.String(250))
    medicine = db.Column(db.String(250))
    record_date = db.Column(db.DateTime, default=datetime.utcnow)


class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_slot = db.Column(db.String(50), nullable=False)
    evening_slot = db.Column(db.String(50), nullable=False)
