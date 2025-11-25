from datetime import datetime
import sqlite3
from pathlib import Path


def conectar_db(db: Path):
    db.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db)


def registrar_envio(db: Path):
    factura_id = input("ID de la factura a despachar: ").strip()
    detalle = input("Detalle de envío (ej. courier o tracking): ").strip() or "Envio registrado"
    with conectar_db(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT orden_id, estado_envio FROM facturas WHERE id = ?",
            (factura_id,),
        )
        factura = cursor.fetchone()
        if not factura:
            print("Factura no encontrada.\n")
            return

        orden_id, estado_envio = factura
        if estado_envio == "DESPACHADO":
            print("La factura ya fue despachada.\n")
            return

        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO envios (factura_id, fecha_envio, detalle_envio, estado)
            VALUES (?, ?, ?, 'DESPACHADO')
            """,
            (factura_id, fecha_envio, detalle),
        )
        cursor.execute(
            "UPDATE facturas SET estado_envio = 'DESPACHADO' WHERE id = ?",
            (factura_id,),
        )
        cursor.execute(
            "UPDATE ordenes_compra SET estado = 'DESPACHADA' WHERE id = ?",
            (orden_id,),
        )
        conn.commit()

    print(f"Envío registrado para factura {factura_id}.\n")


def listar_envios(db: Path):
    with conectar_db(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.id, e.factura_id, e.fecha_envio, e.detalle_envio, f.orden_id
            FROM envios e
            JOIN facturas f ON e.factura_id = f.id
            ORDER BY e.id DESC
            """
        )
        envios = cursor.fetchall()

    if not envios:
        print("\n(No hay envíos registrados)\n")
        return

    print("\n=== Envíos ===")
    for envio_id, factura_id, fecha_envio, detalle_envio, orden_id in envios:
        print(
            f"Envío {envio_id} | Factura {factura_id} (OC {orden_id}) | Fecha: {fecha_envio} | Detalle: {detalle_envio}"
        )
    print("")