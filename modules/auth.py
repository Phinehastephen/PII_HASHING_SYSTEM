from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user_model import User


def register_user(
    username,
    password,
    role="admin"
):

    hashed_password = generate_password_hash(password)

    User.create_user(
        username,
        hashed_password,
        role
    )


def authenticate_user(
    username,
    password
):

    user = User.find_by_username(username)

    if not user:
        return None

    if check_password_hash(
        user["password"],
        password
    ):
        return user

    return None