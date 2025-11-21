#!/usr/bin/env python3
"""
Verify that the admin user exists and can log in.
"""

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash

def verify_admin_user():
    """Verify the admin user exists with correct credentials."""

    db_path = Path('mantenimiento.db')

    if not db_path.exists():
        print("❌ Database not found!")
        return False

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check for admin user
        cursor.execute("SELECT id, username, password FROM Usuario WHERE username = 'admin'")
        admin = cursor.fetchone()

        if admin:
            admin_id, username, password_hash = admin
            print("✅ Admin user found!")
            print(f"   ID: {admin_id}")
            print(f"   Username: {username}")

            # Verify password
            if check_password_hash(password_hash, 'admin'):
                print("   Password: 'admin' (verified ✓)")
            else:
                print("   Password: Unable to verify")

            # Check if admin has any vehicles
            cursor.execute("SELECT COUNT(*) FROM Vehiculo WHERE usuario_id = ?", (admin_id,))
            vehicle_count = cursor.fetchone()[0]
            print(f"   Vehicles owned: {vehicle_count}")

            # Check total database state
            print("\n📊 Database Statistics:")
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            total_users = cursor.fetchone()[0]
            print(f"   Total users: {total_users}")

            cursor.execute("SELECT COUNT(*) FROM Vehiculo")
            total_vehicles = cursor.fetchone()[0]
            print(f"   Total vehicles: {total_vehicles}")

            cursor.execute("SELECT COUNT(*) FROM Mantenimiento")
            total_maintenance = cursor.fetchone()[0]
            print(f"   Total maintenance records: {total_maintenance}")

            conn.close()

            print("\n🎯 Demo Login Credentials:")
            print("   URL: http://localhost:5000")
            print("   Username: admin")
            print("   Password: admin")

            return True
        else:
            print("❌ Admin user not found!")
            conn.close()
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ADMIN USER VERIFICATION")
    print("=" * 50)
    verify_admin_user()