
import sqlite3
import hashlib
import hmac
import secrets

from modules.database import get_connection, initialize_database


def hash_password(password):
    """Securely hash a password using PBKDF2."""
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    """Check whether a password matches its stored hash."""
    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)

        candidate_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600_000,
        )

        return hmac.compare_digest(
            candidate_hash.hex(),
            hash_hex,
        )
    except (ValueError, TypeError):
        return False


def register_user(name, email, password, role="employee"):
    """Register an employee or HR admin."""
    initialize_database()

    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "Please fill in all required fields."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if role not in ("employee", "hr_admin"):
        return False, "Invalid user role."

    password_hash = hash_password(password)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, password_hash, role),
            )

        return True, "Registration successful."

    except sqlite3.IntegrityError:
        return False, "This email is already registered."


def login_user(email, password):
    """Authenticate a user and return basic profile details."""
    initialize_database()

    email = email.strip().lower()

    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = ? AND is_active = 1
            """,
            (email,),
        ).fetchone()

    if user is None:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }

def create_hr_admin(name, email, password):
    """Create an HR admin account safely without duplicating an email."""
    return register_user(
        name=name,
        email=email,
        password=password,
        role="hr_admin",
    )

def ensure_hr_admin(name, email, password):
    """Create the configured demo admin only if the email is unused."""
    initialize_database()
    email = email.strip().lower()

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT role FROM users WHERE email = ?",
            (email,),
        ).fetchone()

    if existing:
        if existing["role"] == "hr_admin":
            return True, "HR admin account already exists."
        return False, "That email belongs to a non-admin account."

    return create_hr_admin(name, email, password)
