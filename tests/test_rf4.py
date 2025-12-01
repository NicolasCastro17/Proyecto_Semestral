import sqlite3
from pathlib import Path
import pytest

from src.factura import emitir_factura

@pytest.fixture
def db_con_orden(tmp_path):
    """
    Crea una base de datos SQLite en un archivo temporal
    con una orden lista para facturar (estado OC_CREADA).
    """
    db_path = tmp_path / "test_proyecto.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabla ordenes_compra (simplificada pero compatible)
    cursor.execute("""
        CREATE TABLE ordenes_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            cliente TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT NOT NULL,
            comuna TEXT NOT NULL,
            region TEXT NOT NULL,
            items_json TEXT NOT NULL,
            total REAL NOT NULL,
            estado TEXT NOT NULL
        );
    """)

    # Tabla facturas (como usa tu función)
    cursor.execute("""
        CREATE TABLE facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER NOT NULL UNIQUE,
            fecha_emision TEXT NOT NULL,
            monto_neto REAL NOT NULL,
            monto_iva REAL NOT NULL,
            monto_total REAL NOT NULL,
            estado_envio TEXT NOT NULL
        );
    """)

    # Insertar una OC con total 100 y estado OC_CREADA
    cursor.execute("""
        INSERT INTO ordenes_compra
            (numero, cliente, direccion, telefono, comuna, region,
             items_json, total, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "ORD-001",
        "Cliente Test",
        "Calle Falsa 123",
        "+56900000000",
        "Comuna X",
        "Region Y",
        "[]",
        100.00,
        "OC_CREADA"
    ))
    orden_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return db_path, orden_id


def test_emision_factura_exitosa(db_con_orden, monkeypatch):
    """
    Verifica que emitir_factura:
    - Registre la factura asociada a la orden
    - Cambie el estado de la orden a 'FACTURADA'
    - Calcule el total como neto + 19% de IVA (RF4)
    """
    db_path, orden_id = db_con_orden

    # Simular entrada de usuario con el id de la orden
    monkeypatch.setattr("builtins.input", lambda _: str(orden_id))

    # Ejecutar la función usando la ruta de la DB (Path)
    emitir_factura(db_path)

    # Verificar resultados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # A. Estado de la orden
    cursor.execute("SELECT estado FROM ordenes_compra WHERE id = ?", (orden_id,))
    estado_final = cursor.fetchone()[0]
    assert estado_final == "FACTURADA"

    # B. Factura creada con monto total = 119.00
    cursor.execute("SELECT monto_total FROM facturas WHERE orden_id = ?", (orden_id,))
    factura = cursor.fetchone()

    assert factura is not None, "Error: No se encontró la factura en la base de datos."
    assert factura[0] == pytest.approx(119.00)  # 100 neto + 19 IVA

    conn.close()
