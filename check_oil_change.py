import sqlite3
import json

conn = sqlite3.connect('mantenimiento.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check oil change maintenance type
cursor.execute("""
    SELECT id, nombre, miles_next_maintenance, meses_proximo_mantenimiento, categoria
    FROM Tipo_Mantenimiento
    WHERE nombre LIKE '%Oil%' OR nombre LIKE '%oil%'
""")

results = cursor.fetchall()
print("Oil change maintenance types in database:")
print("-" * 60)
for row in results:
    print(f"ID: {row['id']}")
    print(f"Name: {row['nombre']}")
    print(f"Miles: {row['miles_next_maintenance']}")
    print(f"Months: {row['meses_proximo_mantenimiento']}")
    print(f"Category: {row['categoria']}")
    print("-" * 60)

    # Test the API response format
    print(f"\nAPI response would be:")
    tipo_dict = dict(row)
    print(json.dumps(tipo_dict, indent=2))

conn.close()