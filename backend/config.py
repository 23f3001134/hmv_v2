import os
from datetime import timedelta

from dotenv import load_dotenv

# Reads backend/.env when running locally. On Render/Vercel the values
# come from the dashboard's Environment Variables, so no .env file is needed.
load_dotenv()


def _required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "For local development copy backend/.env.example to backend/.env "
            "and fill in the values."
        )
    return value


def _database_url():
    url = os.getenv("DATABASE_URL", "sqlite:///hospital.db")
    # Render/Heroku give "postgres://", SQLAlchemy needs "postgresql://"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    # --- Secrets: NEVER hardcode these. They must come from the environment. ---
    SECRET_KEY = _required("SECRET_KEY")
    JWT_SECRET_KEY = _required("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Lets Flask-JWT-Extended's 401 errors (missing/expired token) work properly
    # with Flask-RESTful instead of turning into a 500.
    PROPAGATE_EXCEPTIONS = True

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "120"))
    )

    CORS_ORIGINS = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if o.strip()
    ]

    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "60"))
    CACHE_KEY_PREFIX = os.getenv("CACHE_KEY_PREFIX", "mad2:")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/1")

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")

    DAILY_REMINDER_HOUR = int(os.getenv("DAILY_REMINDER_HOUR", "8"))
    DAILY_REMINDER_MINUTE = int(os.getenv("DAILY_REMINDER_MINUTE", "0"))
    MONTHLY_REPORT_HOUR = int(os.getenv("MONTHLY_REPORT_HOUR", "9"))
    MONTHLY_REPORT_MINUTE = int(os.getenv("MONTHLY_REPORT_MINUTE", "0"))

    DEFAULT_GCHAT_WEBHOOK_URL = os.getenv("DEFAULT_GCHAT_WEBHOOK_URL", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "no-reply@mad2.local")

    EXPORT_DIR = os.getenv("EXPORT_DIR", "instance/exports")
