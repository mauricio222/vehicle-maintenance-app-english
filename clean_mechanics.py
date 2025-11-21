#!/usr/bin/env python3
"""
Clean the Mecánico (Mechanics) table.
"""

import sqlite3
from pathlib import Path

def clean_mechanics_table():
    """Clean the mechanics table."""

    # Database path
    db_path = Path('mantenimiento.db')

    if not db_path.exists():
        print(f"Database {db_path} not found!")
        return

    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        print("🔧 Cleaning Mechanics table...")

        # Check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%ec%nico%'")
        tables = cursor.fetchall()
        print(f"Found related tables: {[t[0] for t in tables]}")

        # Try different possible table names
        mechanics_deleted = 0

        # Try Mecánico (with accent)
        try:
            cursor.execute("DELETE FROM Mecánico")
            mechanics_deleted = cursor.rowcount
            print(f"✅ Deleted {mechanics_deleted} mechanics from 'Mecánico' table")
        except sqlite3.OperationalError:
            # Try Mecanico (without accent)
            try:
                cursor.execute("DELETE FROM Mecanico")
                mechanics_deleted = cursor.rowcount
                print(f"✅ Deleted {mechanics_deleted} mechanics from 'Mecanico' table")
            except sqlite3.OperationalError:
                print("❌ No Mechanics table found")

        # Also clean Tipo_Mantenimiento if exists
        try:
            cursor.execute("DELETE FROM Tipo_Mantenimiento")
            types_deleted = cursor.rowcount
            print(f"✅ Deleted {types_deleted} maintenance types from 'Tipo_Mantenimiento' table")
        except sqlite3.OperationalError:
            pass

        # Commit changes
        conn.commit()

        # Vacuum to optimize database
        cursor.execute("VACUUM")

        print("\n✨ Cleanup complete!")

        # Show final stats for all tables
        print("\n📊 Final database state:")

        cursor.execute("SELECT COUNT(*) FROM Usuario")
        user_count = cursor.fetchone()[0]
        print(f"   Users: {user_count}")

        cursor.execute("SELECT COUNT(*) FROM Vehiculo")
        vehicle_count = cursor.fetchone()[0]
        print(f"   Vehicles: {vehicle_count}")

        cursor.execute("SELECT COUNT(*) FROM Mantenimiento")
        maintenance_count = cursor.fetchone()[0]
        print(f"   Maintenance records: {maintenance_count}")

        try:
            cursor.execute("SELECT COUNT(*) FROM Mecánico")
            mechanic_count = cursor.fetchone()[0]
            print(f"   Mechanics: {mechanic_count}")
        except:
            try:
                cursor.execute("SELECT COUNT(*) FROM Mecanico")
                mechanic_count = cursor.fetchone()[0]
                print(f"   Mechanics: {mechanic_count}")
            except:
                print(f"   Mechanics: N/A")

        try:
            cursor.execute("SELECT COUNT(*) FROM Tipo_Mantenimiento")
            type_count = cursor.fetchone()[0]
            print(f"   Maintenance types: {type_count}")
        except:
            print(f"   Maintenance types: N/A")

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
    print("MECHANICS TABLE CLEANUP")
    print("=" * 50)
    clean_mechanics_table()