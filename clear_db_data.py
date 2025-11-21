#!/usr/bin/env python3
"""
Script to clear all data from the database while keeping the table structure intact.
"""

import sqlite3
import os
from pathlib import Path

# Database path
DB_PATH = Path('mantenimiento.db')

def clear_all_data():
    """Clear all data from the database tables."""

    if not DB_PATH.exists():
        print(f"Database {DB_PATH} not found!")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    try:
        # List of tables to clear (in correct order to respect foreign key constraints)
        tables_to_clear = [
            'Mantenimiento',
            'Kilometraje',
            'Tipo_Mantenimiento',
            'Vehiculo',
            'Detalle_Vehiculo',
            'Mecánico',
            'Usuario'
        ]

        # Disable foreign key constraints temporarily
        cursor.execute('PRAGMA foreign_keys = OFF')

        for table in tables_to_clear:
            try:
                cursor.execute(f'DELETE FROM {table}')
                count = cursor.rowcount
                print(f"✓ Cleared {count} records from {table}")

                # Reset the autoincrement counter
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

            except sqlite3.Error as e:
                print(f"✗ Error clearing {table}: {e}")

        # Re-enable foreign key constraints
        cursor.execute('PRAGMA foreign_keys = ON')

        # Commit all changes
        conn.commit()
        print("\n✅ All data has been cleared successfully!")
        print("The database structure remains intact.")

        # Show current database size
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        print(f"\nDatabase contains {table_count} tables (structure preserved)")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE DATA CLEARING TOOL")
    print("=" * 50)
    print(f"Database: {DB_PATH}")
    print("\nThis will DELETE ALL DATA from all tables!")
    print("The table structure will remain intact.\n")

    response = input("Are you sure you want to proceed? (yes/no): ")

    if response.lower() == 'yes':
        clear_all_data()
    else:
        print("Operation cancelled.")