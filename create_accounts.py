from database.auth_database import create_tables, create_user


create_tables()

print("===================================")
print(" SECURESHIELD ACCOUNT SETUP")
print("===================================")

# Create Admin account
admin_created = create_user(
    "admin",
    "admin@secureshield.local",
    "Admin@12345",
    "admin"
)

# Create normal User account
user_created = create_user(
    "user",
    "user@secureshield.local",
    "User@12345",
    "user"
)

if admin_created:
    print("Admin account created successfully.")
else:
    print("Admin account already exists.")

if user_created:
    print("User account created successfully.")
else:
    print("User account already exists.")

print("-----------------------------------")
print("Account setup completed.")