# app.py — Punto de entrada del programa
# Ejemplo en consola:  python src/app.py

# Librería estándar
# Sirve para trabajar con rutas de archivos de manera más clara.
# Ejemplo: construir la ruta hacia la base de datos.
from pathlib import Path

# Importamos funciones desde otros módulos creados por nosotros
# usuarioDefault crea usuario admin/admin123 si no existe.
# login muestra el inicio de sesión y valida credenciales.
from login import usuarioDefault, login

# menú principal del sistema.
from menu import Menu

# Librería estándar
# Se usa para conectarse a SQLite y ejecutar consultas en la base de datos.
import sqlite3


# Definimos la ruta hacia la base de datos
DB_PATH = Path(__file__).resolve().parents[1] / "database" / "proyecto.db"

def conectar_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def iniciarBD():
    # Crea las tablas de la base de datos si no existen
    with conectar_db() as conn:
        c = conn.cursor()

        # Tabla de usuarios: guarda nombre de usuario y hash de contraseña
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
         """
        )

        # Tabla de órdenes de compra: guarda datos de cliente y sus productos
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS ordenes_compra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                cliente TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                comuna TEXT NOT NULL,
                region TEXT NOT NULL,
                items_json TEXT NOT NULL,
                total REAL NOT NULL,
                estado TEXT NOT NULL DEFAULT 'OC_CREADA'
            );
            """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orden_id INTEGER NOT NULL UNIQUE,
                fecha_emision TEXT NOT NULL,
                monto_neto REAL NOT NULL,
                monto_iva REAL NOT NULL,
                monto_total REAL NOT NULL,
                estado_envio TEXT NOT NULL DEFAULT 'PENDIENTE',
                FOREIGN KEY (orden_id) REFERENCES ordenes_compra (id)
            );
            """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS envios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                fecha_envio TEXT NOT NULL,
                detalle_envio TEXT,
                estado TEXT NOT NULL DEFAULT 'DESPACHADO',
                FOREIGN KEY (factura_id) REFERENCES facturas (id)
            );
           """
        )
        conn.commit()


def main():
    usuarioDefault(DB_PATH)
    usuario = login(DB_PATH)
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo…")
        return
    # Paso 4: abre el menú principal del sistema
    Menu(usuario, DB_PATH)

if __name__ == "__main__":
    iniciarBD()
    main()