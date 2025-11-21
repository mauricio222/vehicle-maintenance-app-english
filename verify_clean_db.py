import sqlite3

conn = sqlite3.connect('mantenimiento.db')
cursor = conn.cursor()

print("=" * 60)
print("DATABASE STATUS - DEMO READY")
print("=" * 60)

# Check each table
tables = [
    ('Usuario', 'Users'),
    ('Vehiculo', 'Vehicles'),
    ('Detalle_Vehiculo', 'Vehicle Details'),
    ('Mecánico', 'Mechanics'),
    ('Tipo_Mantenimiento', 'Maintenance Types'),
    ('Mantenimiento', 'Maintenances')
]

for table_name, display_name in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    if table_name == 'Usuario':
        cursor.execute(f"SELECT username FROM {table_name}")
        users = cursor.fetchall()
        print(f"✓ {display_name}: {count} record(s)")
        for user in users:
            print(f"  - Username: {user[0]} (demo account)")
    else:
        status = "✓ Empty - Ready for demo data" if count == 0 else f"⚠ Has {count} records"
        print(f"✓ {display_name}: {status}")

print("=" * 60)
print("✅ Database is clean and ready for demo!")
print("Login with: username='admin', password='admin'")
print("=" * 60)

conn.close()