# login.py — Registro y autenticación
# Librería estándar de Python
# Se usa para aplicar funciones de hash (ej: SHA-256) a las contraseñas.
# Esto permite guardar solo un "código" irrevertible en la base de datos,
# en vez de guardar la contraseña real en texto plano.
import hashlib

# Se usa para conectarse y trabajar con bases de datos SQLite.
# Permite ejecutar consultas (SELECT, INSERT, etc.) en archivos .db.
import sqlite3

# Librería estándar
# Se usa para pedir la contraseña al usuario sin mostrarla en pantalla.
# Ejemplo: cuando escribes la clave en la terminal y aparecen solo asteriscos o nada.
from getpass import getpass

# Librería estándar
# Se usa para manejar rutas de archivos de manera más segura que con strings.
# Ejemplo: Path("database/proyecto.db") representa la ruta a la base de datos.
from pathlib import Path

def conectar_db(db: Path):
    # db es un objeto Path que apunta al archivo de base de datos
    # database/proyecto.db
    # db.parent se refiere a la carpeta que contiene ese archivo (database/).
    # mkdir(parents=True, exist_ok=True) asegura que esa carpeta exista.
    db.parent.mkdir(parents=True, exist_ok=True)
    # db.parent se refiere a la carpeta que contiene ese archivo (database/).
    # mkdir(parents=True, exist_ok=True) asegura que esa carpeta exista.
    return sqlite3.connect(db)
    # Abre la conexión con la base de datos SQLite que está en esa ruta.
    # Si el archivo no existe, SQLite lo crea vacío automáticamente.
    # Devuelve el objeto Connection para poder ejecutar consultas (SELECT, INSERT, etc.).

def encriptarPassword(pwd: str) -> str:
    # Recibe la contraseña en texto plano (ejemplo: "admin123")
    # encode("utf-8") → convierte el texto a bytes, porque hashlib trabaja con bytes.
    # hashlib.sha256(...).hexdigest() → devuelve el hash como un string hexadecimal.
    # Ejemplo: "admin123" se convierte en "240be518fabd2724ddb6f04eeb1da596..."
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()


def usuarioExistente(db: Path, username: str) -> bool:
    # Verifica si un usuario ya está registrado en la base de datos.
    with conectar_db(db) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM usuarios WHERE username=?", (username,))
        # fetchone() devuelve una fila si encontró algo, o None si no hay coincidencia.
        return c.fetchone() is not None


def usuarioDefault(db: Path):
    """Crea un usuario por defecto admin/admin123 si no existe."""
    if not usuarioExistente(db, "admin"):
        with conectar_db(db) as conn:
            c = conn.cursor()
            # Se inserta "admin" con la contraseña encriptada.
            c.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
                ("admin", encriptarPassword("admin123"))
            )
            conn.commit()


def autenticarUsuario(db: Path, username: str, password: str) -> bool:
    # Verifica si la combinación usuario/contraseña es correcta.
    with conectar_db(db) as conn:
        c = conn.cursor()
        c.execute("SELECT password_hash FROM usuarios WHERE username=?", (username,))
        row = c.fetchone()
    # row[0] contiene el hash guardado en la BD.
    # Se compara con el hash de la contraseña ingresada.
    return bool(row and row[0] == encriptarPassword(password))


def login(db: Path):
    print("=== Inicio de Sesión ===")
    for _ in range(3):  # El usuario tiene 3 intentos
        user = input("Usuario: ").strip()
        pwd = getpass("Contraseña: ")
        if autenticarUsuario(db, user, pwd):
            print(f"Bienvenido, {user}\n")
            return user
        print("Credenciales incorrectas. Intenta nuevamente.\n")
    # Si falla los 3 intentos devuelve None
    return None