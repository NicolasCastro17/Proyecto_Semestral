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


# Definimos la ruta hacia la base de datos:
# /database/proyecto.db
# __file__ ruta del archivo actual (src/app.py).
# .parents[1] sube un nivel (raíz del proyecto).
# "database/proyecto.db" subcarpeta database con el archivo de la BD.
db = (Path(__file__).resolve().parents[1] / "database" / "proyecto.db")


def conectar_db():
    # Asegura que la carpeta "database/" exista
    db.parent.mkdir(parents=True, exist_ok=True)
    # Devuelve una conexión a SQLite usando esa ruta
    return sqlite3.connect(db)


def iniciarBD():
    # Crea las tablas de la base de datos si no existen
    with conectar_db() as conn:
        c = conn.cursor()

        # Tabla de usuarios: guarda nombre de usuario y hash de contraseña
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)

        # Tabla de órdenes de compra: guarda datos de cliente y sus productos
        c.execute("""
            CREATE TABLE IF NOT EXISTS ordenes_compra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL,
                cliente TEXT NOT NULL,
                direccion TEXT NOT NULL,
                telefono TEXT NOT NULL,
                comuna TEXT NOT NULL,
                region TEXT NOT NULL,
                items_json TEXT NOT NULL,   -- JSON: [{producto, precio}]
                total REAL NOT NULL,
                estado TEXT NOT NULL DEFAULT 'OC_CREADA'  -- OC_CREADA | FACTURADA | DESPACHADA
            );
        """)
        conn.commit()


def main():
    # Paso 1: inicializa la base de datos y tablas
    iniciarBD()
    # Paso 2: asegura que exista usuario admin/admin123
    usuarioDefault(db)
    # Paso 3: pide login al usuario
    usuario = login(db)
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo…")
        return
    # Paso 4: abre el menú principal del sistema
    Menu(usuario, db)


# Esto se ejecuta solo si corremos este archivo directamente
if __name__ == "__main__":
    main()
