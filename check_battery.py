import sqlite3

conn = sqlite3.connect('mantenimiento.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check battery maintenance type
cursor.execute("""
    SELECT id, nombre, miles_next_maintenance, meses_proximo_mantenimiento, categoria
    FROM Tipo_Mantenimiento
    WHERE nombre LIKE '%Battery%' OR nombre LIKE '%battery%'
""")

results = cursor.fetchall()
print("Battery maintenance types in database:")
print("-" * 60)
for row in results:
    print(f"ID: {row['id']}")
    print(f"Name: {row['nombre']}")
    print(f"Miles: {row['miles_next_maintenance']}")
    print(f"Months: {row['meses_proximo_mantenimiento']}")
    print(f"Category: {row['categoria']}")
    print("-" * 60)

conn.close()