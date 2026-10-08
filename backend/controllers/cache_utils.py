from flask import current_app
from extensions import cache


def get_or_set(key, builder, timeout=None):
    cached = cache.get(key)
    if cached is not None:
        return cached
    value = builder()
    cache_timeout = timeout or current_app.config.get("CACHE_DEFAULT_TIMEOUT", 60)
    cache.set(key, value, timeout=cache_timeout)
    return value


def delete_keys(*keys):
    for key in keys:
        if key:
            cache.delete(key)


def key_admin_dashboard(search):
    return f"admin_dashboard:{search or 'all'}"


def key_patient_dashboard(user_id):
    return f"patient_dashboard:{user_id}"


def key_patient_records(user_id):
    return f"patient_records:{user_id}"


def key_doctor_dashboard(user_id):
    return f"doctor_dashboard:{user_id}"


def key_doctor_availability(user_id):
    return f"doctor_availability:{user_id}"


def key_patient_department_doctors(department):
    return f"patient_department_doctors:{department}"


def key_patient_doctor_availability(doctor_id):
    return f"patient_doctor_availability:{doctor_id}"
