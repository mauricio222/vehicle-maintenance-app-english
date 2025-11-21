#!/usr/bin/env python3
"""
Script to convert database from kilometers to miles
"""

import sqlite3
from pathlib import Path

DB_PATH = Path('mantenimiento.db')

def convert_to_miles():
    """Convert database schema and data from kilometers to miles."""

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    try:
        # Start transaction
        cursor.execute('BEGIN TRANSACTION')

        print("Converting database to use miles instead of kilometers...")

        # 1. Rename columns in Kilometraje table to use Miles
        print("1. Updating Kilometraje table to Mileage...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Mileage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                mileage INTEGER NOT NULL,
                FOREIGN KEY (vehiculo_id) REFERENCES Vehiculo(id),
                UNIQUE(vehiculo_id, fecha, mileage)
            )
        ''')

        # Copy data from Kilometraje to Mileage (converting km to miles)
        cursor.execute('''
            INSERT OR IGNORE INTO Mileage (id, vehiculo_id, fecha, mileage)
            SELECT id, vehiculo_id, fecha, CAST(kilometraje * 0.621371 AS INTEGER)
            FROM Kilometraje
        ''')

        # 2. Update Tipo_Mantenimiento table
        print("2. Updating Tipo_Mantenimiento table...")
        cursor.execute('''
            ALTER TABLE Tipo_Mantenimiento
            RENAME COLUMN kilometros_proximo_mantenimiento TO miles_next_maintenance
        ''')

        # Convert existing kilometer values to miles
        cursor.execute('''
            UPDATE Tipo_Mantenimiento
            SET miles_next_maintenance = CAST(miles_next_maintenance * 0.621371 AS INTEGER)
            WHERE miles_next_maintenance IS NOT NULL
        ''')

        # 3. Update Mantenimiento table to reference new Mileage table
        print("3. Updating Mantenimiento table...")
        cursor.execute('''
            ALTER TABLE Mantenimiento
            RENAME COLUMN kilometraje_id TO mileage_id
        ''')

        # 4. Drop the old Kilometraje table
        print("4. Dropping old Kilometraje table...")
        cursor.execute('DROP TABLE IF EXISTS Kilometraje')

        # Commit transaction
        cursor.execute('COMMIT')
        print("\n✅ Database successfully converted to use miles!")

        # Show summary
        cursor.execute('SELECT COUNT(*) FROM Mileage')
        mileage_count = cursor.fetchone()[0]
        print(f"   - Mileage records: {mileage_count}")

        cursor.execute('SELECT COUNT(*) FROM Tipo_Mantenimiento WHERE miles_next_maintenance IS NOT NULL')
        maintenance_types = cursor.fetchone()[0]
        print(f"   - Maintenance types with mile intervals: {maintenance_types}")

    except sqlite3.Error as e:
        cursor.execute('ROLLBACK')
        print(f"❌ Error converting database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    convert_to_miles()