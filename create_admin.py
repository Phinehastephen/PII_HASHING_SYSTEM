from modules.auth import register_user

register_user(
    "admin",
    "admin123",
    "administrator"
)

print("Admin user created")