
import pytest

from modules.auth import (
    hash_password,
    verify_password,
    register_user,
    login_user,
)


def test_password_hashing():
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_different_hashes_for_same_password():
    password = "TestPassword123!"

    hash_one = hash_password(password)
    hash_two = hash_password(password)

    assert hash_one != hash_two
    assert verify_password(password, hash_one)
    assert verify_password(password, hash_two)


def test_register_and_login_employee():
    import uuid

    email = f"employee_{uuid.uuid4().hex}@example.com"
    password = "TestPassword123!"

    success, message = register_user(
        name="Test Employee",
        email=email,
        password=password,
        role="employee",
    )

    assert success, message

    user = login_user(email, password)

    assert user is not None
    assert user["email"] == email
    assert user["role"] == "employee"


def test_login_with_wrong_password():
    import uuid

    email = f"employee_{uuid.uuid4().hex}@example.com"

    success, message = register_user(
        name="Test Employee",
        email=email,
        password="CorrectPassword123!",
    )

    assert success, message

    user = login_user(email, "WrongPassword123!")

    assert user is None


def test_registration_rejects_short_password():
    import uuid

    email = f"employee_{uuid.uuid4().hex}@example.com"

    success, message = register_user(
        name="Test Employee",
        email=email,
        password="short",
    )

    assert not success
    assert "8 characters" in message
