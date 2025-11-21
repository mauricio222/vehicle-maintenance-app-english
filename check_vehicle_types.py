import sqlite3

conn = sqlite3.connect('mantenimiento.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check all maintenance types for vehicle-specific entries
cursor.execute("""
    SELECT DISTINCT
        t.id,
        t.nombre,
        t.miles_next_maintenance,
        t.meses_proximo_mantenimiento,
        t.categoria,
        v.alias as vehiculo_alias
    FROM Tipo_Mantenimiento t
    LEFT JOIN Tipo_Mantenimiento_Vehiculo tv ON t.id = tv.tipo_mantenimiento_id
    LEFT JOIN Vehiculo v ON tv.vehiculo_id = v.id
    WHERE t.nombre LIKE '%Battery%' OR t.nombre LIKE '%battery%'
    ORDER BY t.nombre, v.alias
""")

results = cursor.fetchall()
print("Battery maintenance types with vehicle associations:")
print("-" * 80)
for row in results:
    print(f"ID: {row['id']}, Name: {row['nombre']}, Miles: {row['miles_next_maintenance']}, "
          f"Months: {row['meses_proximo_mantenimiento']}, Category: {row['categoria']}, "
          f"Vehicle: {row['vehiculo_alias'] or 'Generic'}")

conn.close()