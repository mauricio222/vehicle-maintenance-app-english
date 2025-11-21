#!/usr/bin/env python3
import sqlite3
from werkzeug.security import generate_password_hash
import sys

# Connect to database
conn = sqlite3.connect('mantenimiento.db')
cursor = conn.cursor()

# Check if there are any existing users
cursor.execute("SELECT username FROM Usuario")
existing_users = cursor.fetchall()

print("=" * 50)
print("VEHICLE MAINTENANCE APP - TEST CREDENTIALS")
print("=" * 50)

if existing_users:
    print("\nExisting users in database:")
    for user in existing_users:
        print(f"  - Username: {user[0]}")
    print("\n(Note: Passwords are encrypted and cannot be retrieved)")
    print("If you forgot your password, create a new test user below.\n")
else:
    print("\nNo users found in database.\n")

# Create test users
test_users = [
    ('admin', 'admin123', 'Administrator'),
    ('testuser', 'test123', 'Test User'),
    ('demo', 'demo123', 'Demo User')
]

print("Creating/Updating test users...")
print("-" * 50)

for username, password, description in test_users:
    # Check if user already exists
    cursor.execute("SELECT id FROM Usuario WHERE username = ?", (username,))
    existing = cursor.fetchone()

    if existing:
        # Update password for existing user
        hashed_password = generate_password_hash(password)
        cursor.execute("UPDATE Usuario SET password_hash = ? WHERE username = ?",
                      (hashed_password, username))
        print(f"✓ Updated: {username} ({description})")
    else:
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO Usuario (username, password_hash) VALUES (?, ?)",
                      (username, hashed_password))
        print(f"✓ Created: {username} ({description})")

conn.commit()
conn.close()

print("\n" + "=" * 50)
print("TEST LOGIN CREDENTIALS")
print("=" * 50)
print("\nYou can now login at http://localhost:5000/login with:")
print("\nOption 1 - Admin Account:")
print("  Username: admin")
print("  Password: admin123")
print("\nOption 2 - Test User Account:")
print("  Username: testuser")
print("  Password: test123")
print("\nOption 3 - Demo Account:")
print("  Username: demo")
print("  Password: demo123")
print("\n" + "=" * 50)
print("\n✅ Test users ready! You can now login to the application.")