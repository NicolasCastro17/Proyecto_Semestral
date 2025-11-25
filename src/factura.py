from datetime import datetime
import sqlite3
from pathlib import Path

TASA_IVA = 0.19
TASA_TOTAL = 1.19 # Para calcular el total bruto (1 + 0.19)

def conectar_db(db: Path):
    db.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db)


def calcular_iva(precio_neto: float) -> float:
    """Calcula el monto del 19% de IVA sobre un precio neto."""
    return round(precio_neto * TASA_IVA, 2)

def calcular_total_bruto(precio_neto: float) -> float:
    return round(precio_neto * TASA_TOTAL, 2)

def emitir_factura(db: Path):
    orden_id = input("ID de la orden a facturar: ").strip()
    with conectar_db(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT total, estado FROM ordenes_compra WHERE id = ?", (orden_id,))
        orden = cursor.fetchone()

        if not orden:
            print("Orden no encontrada.\n")
            return
        monto_neto_total, estado = orden
        if estado != "OC_CREADA":
            print("La orden ya fue facturada o despachada.\n")
            return

        cursor.execute("SELECT id FROM facturas WHERE orden_id = ?", (orden_id,))
        if cursor.fetchone():
            print("La orden ya tiene una factura emitida.\n")
            return
        
        # 3. Calcular IVA y Total a Pagar
        monto_iva = calcular_iva(monto_neto_total)
        monto_total = calcular_total_bruto(monto_neto_total)

        # 4. Registrar la nueva Factura
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
             """
            INSERT INTO facturas (orden_id, fecha_emision, monto_neto, monto_iva, monto_total, estado_envio)
            VALUES (?, ?, ?, ?, ?, 'PENDIENTE')
            """,
            (orden_id, fecha_actual, monto_neto_total, monto_iva, monto_total),
        )
        
        cursor.execute("UPDATE ordenes_compra SET estado = 'FACTURADA' WHERE id = ?", (orden_id,))
        conn.commit()

    print(" Factura emitida correctamente. Resumen:")
    print(f"   Orden: {orden_id}")
    print(f"   Neto: ${monto_neto_total:,.2f}")
    print(f"   IVA (19%): ${monto_iva:,.2f}")
    print(f"   Total: ${monto_total:,.2f}\n")
        
def listar_facturas(db: Path):
    with conectar_db(db) as conn:
        cursor = conn.cursor()
        cursor.execute(
        """
            SELECT f.id, f.orden_id, f.fecha_emision, f.monto_total, f.estado_envio
            FROM facturas f
            ORDER BY f.id DESC
            """
        )
        facturas = cursor.fetchall()

    if not facturas:
        print("\n(No hay facturas emitidas)\n")
        return

    print("\n=== Facturas ===")
    for f_id, orden_id, fecha, total, estado_envio in facturas:
        print(f"Factura {f_id} | OC {orden_id} | Fecha: {fecha} | Total: ${total:,.2f} | Envío: {estado_envio}")
    print("")