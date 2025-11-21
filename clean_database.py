import sqlite3

# Connect to the database
conn = sqlite3.connect('mantenimiento.db')
cursor = conn.cursor()

# Begin transaction
cursor.execute("BEGIN TRANSACTION")

try:
    # Delete all data except admin user from all tables

    # Delete all maintenances
    cursor.execute("DELETE FROM Mantenimiento")
    print("✓ Deleted all maintenances")

    # Delete all maintenance types
    cursor.execute("DELETE FROM Tipo_Mantenimiento")
    print("✓ Deleted all maintenance types")

    # Delete all mechanics
    cursor.execute("DELETE FROM Mecánico")
    print("✓ Deleted all mechanics")

    # Delete all vehicles
    cursor.execute("DELETE FROM Vehiculo")
    print("✓ Deleted all vehicles")

    # Delete all vehicle details
    cursor.execute("DELETE FROM Detalle_Vehiculo")
    print("✓ Deleted all vehicle details")

    # Delete all users except admin
    cursor.execute("DELETE FROM Usuario WHERE username != 'admin'")
    print("✓ Deleted all users except admin")

    # Verify admin user still exists
    admin = cursor.execute("SELECT * FROM Usuario WHERE username = 'admin'").fetchone()
    if admin:
        print(f"✓ Admin user preserved: {admin}")
    else:
        print("⚠ Warning: Admin user not found!")

    # Commit the transaction
    conn.commit()
    print("\n✅ Database cleaned successfully! Only admin user remains.")

except Exception as e:
    # Rollback on error
    conn.rollback()
    print(f"❌ Error: {e}")

finally:
    conn.close()