#!/usr/bin/env python3
"""
Check the database schema.
"""

import sqlite3
from pathlib import Path

db_path = Path('mantenimiento.db')

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Get Usuario table schema
cursor.execute("PRAGMA table_info(Usuario)")
columns = cursor.fetchall()

print("Usuario table columns:")
for col in columns:
    print(f"  {col}")

# Check admin user
cursor.execute("SELECT * FROM Usuario WHERE username = 'admin'")
admin = cursor.fetchone()
print("\nAdmin user data:", admin)

# Get column names
cursor.execute("SELECT * FROM Usuario WHERE username = 'admin'")
names = [description[0] for description in cursor.description]
print("\nColumn names:", names)

conn.close()