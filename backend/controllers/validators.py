"""Small input-validation helpers so bad requests return a clear 400
instead of crashing with a KeyError / 500."""
import functools
import re

from flask import request

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?\d{10,14}$")


class ValidationError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def handle_validation(fn):
    """Use on Flask-RESTful methods: turns ValidationError into a JSON 400.
    Put it BELOW @jwt_required():
        @jwt_required()
        @handle_validation
        def post(self): ...
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValidationError as err:
            return {"message": err.message}, err.status
    return wrapper


def get_json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    return data


def require_fields(data, *fields):
    missing = [f for f in fields if data.get(f) in (None, "")]
    if missing:
        raise ValidationError("Missing required field(s): " + ", ".join(missing))


def clean_text(data, field, max_len=150):
    value = str(data.get(field, "")).strip()
    if not value:
        raise ValidationError(f"{field} cannot be empty")
    if len(value) > max_len:
        raise ValidationError(f"{field} must be at most {max_len} characters")
    return value


def optional_text(data, field, max_len=250, default=""):
    value = data.get(field)
    if value is None:
        return default
    value = str(value).strip()
    if not value:
        return default
    if len(value) > max_len:
        raise ValidationError(f"{field} must be at most {max_len} characters")
    return value


def clean_email(data, field="email"):
    value = clean_text(data, field).lower()
    if not EMAIL_RE.match(value):
        raise ValidationError("Enter a valid email address")
    return value


def clean_phone(data, field="contact"):
    value = clean_text(data, field, max_len=15).replace(" ", "").replace("-", "")
    if not PHONE_RE.match(value):
        raise ValidationError("Contact must be 10 to 14 digits")
    return value


def clean_password(data, field="password"):
    value = str(data.get(field, ""))
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if len(value) > 128:
        raise ValidationError("Password is too long")
    return value


def clean_int(data, field, min_value, max_value):
    try:
        number = int(data.get(field))
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a number")
    if not min_value <= number <= max_value:
        raise ValidationError(f"{field} must be between {min_value} and {max_value}")
    return number


def clean_age(data, field="age"):
    raw = data.get(field, 0)
    if raw in (None, ""):
        return 0
    return clean_int({field: raw}, field, 0, 120)
