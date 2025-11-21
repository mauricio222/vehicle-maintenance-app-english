#!/usr/bin/env python3
"""
Clean the database but keep the admin user as a demo user.
This script removes all data except for the admin user account.
"""

import sqlite3
import os
from pathlib import Path

def clean_database_keep_admin():
    """Clean all database tables but keep the admin user."""

    # Database path
    db_path = Path('mantenimiento.db')

    if not db_path.exists():
        print(f"Database {db_path} not found!")
        return

    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        print("🔧 Starting database cleanup...")

        # First, check if admin user exists
        cursor.execute("SELECT id, username FROM Usuario WHERE username = 'admin'")
        admin_user = cursor.fetchone()

        if admin_user:
            admin_id = admin_user[0]
            print(f"✅ Found admin user (ID: {admin_id})")

            # Delete all maintenance records (not tied to admin since admin doesn't own vehicles)
            cursor.execute("DELETE FROM Mantenimiento")
            deleted_maintenance = cursor.rowcount
            print(f"   Deleted {deleted_maintenance} maintenance records")

            # Delete all vehicles (admin doesn't own vehicles)
            cursor.execute("DELETE FROM Vehiculo")
            deleted_vehicles = cursor.rowcount
            print(f"   Deleted {deleted_vehicles} vehicles")

            # Delete all mechanics
            cursor.execute("DELETE FROM Mecanico")
            deleted_mechanics = cursor.rowcount
            print(f"   Deleted {deleted_mechanics} mechanics")

            # Delete all maintenance types
            cursor.execute("DELETE FROM TipoMantenimiento")
            deleted_types = cursor.rowcount
            print(f"   Deleted {deleted_types} maintenance types")

            # Delete all users except admin
            cursor.execute("DELETE FROM Usuario WHERE id != ?", (admin_id,))
            deleted_users = cursor.rowcount
            print(f"   Deleted {deleted_users} other users")

            # Commit changes
            conn.commit()

            # Vacuum to optimize database
            cursor.execute("VACUUM")

            print("\n✨ Database cleanup complete!")
            print(f"📌 Admin user preserved: username='admin'")

            # Show final stats
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            user_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Vehiculo")
            vehicle_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Mantenimiento")
            maintenance_count = cursor.fetchone()[0]

            print("\n📊 Final database state:")
            print(f"   Users: {user_count}")
            print(f"   Vehicles: {vehicle_count}")
            print(f"   Maintenance records: {maintenance_count}")

        else:
            print("❌ Admin user not found in database!")
            print("   Creating admin user...")

            # Create admin user if it doesn't exist
            from werkzeug.security import generate_password_hash

            # First clean everything
            cursor.execute("DELETE FROM Mantenimiento")
            cursor.execute("DELETE FROM Vehiculo")
            cursor.execute("DELETE FROM Mecanico")
            cursor.execute("DELETE FROM TipoMantenimiento")
            cursor.execute("DELETE FROM Usuario")

            # Create admin user
            admin_password_hash = generate_password_hash('admin')
            cursor.execute("""
                INSERT INTO Usuario (username, password, email, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, ('admin', admin_password_hash, 'admin@example.com'))

            conn.commit()
            print("✅ Admin user created successfully!")
            print("   Username: admin")
            print("   Password: admin")

        conn.close()

        # Show database file size
        db_size = db_path.stat().st_size / 1024  # Size in KB
        print(f"\n💾 Database size: {db_size:.2f} KB")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE CLEANUP UTILITY")
    print("This will remove all data except the admin user")
    print("=" * 50)

    # Ask for confirmation
    response = input("\nAre you sure you want to clean the database? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        clean_database_keep_admin()
    else:
        print("❌ Operation cancelled")