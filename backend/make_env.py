"""Creates backend/.env for LOCAL development with fresh random secrets.
Run automatically by run_backend.bat. Safe to run again: it never overwrites."""
import os
import secrets

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

if os.path.exists(path):
    print(".env already exists - leaving it unchanged.")
    raise SystemExit(0)

admin_password = secrets.token_urlsafe(9)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(f"""# Local development settings (generated). Never commit this file.
SECRET_KEY={secrets.token_hex(32)}
JWT_SECRET_KEY={secrets.token_hex(32)}

ADMIN_USERNAME=admin
ADMIN_PASSWORD={admin_password}

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Run background jobs inside the request, so you do not need Redis on your laptop.
CELERY_ALWAYS_EAGER=true
""")

print("=" * 60)
print("Created backend/.env")
print("Your local ADMIN LOGIN  ->  username: admin")
print(f"                            password: {admin_password}")
print("(it is also saved inside backend/.env)")
print("=" * 60)
