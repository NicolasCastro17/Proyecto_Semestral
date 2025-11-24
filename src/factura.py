from datetime import datetime
import sqlite3
db = 'database/proyecto.db' 

TASA_IVA = 0.19
TASA_TOTAL = 1.19 # Para calcular el total bruto (1 + 0.19)

def calcular_iva(precio_neto):
    """Calcula el monto del 19% de IVA sobre un precio neto."""
    return round(precio_neto * TASA_IVA, 2)

def calcular_total_bruto(precio_neto):
    """Calcula el precio total (neto + IVA)."""
    return round(precio_neto * TASA_TOTAL, 2)

def conectar_db(db):
    return sqlite3.connect(db)

def emitir_factura(orden_id):
    """
    RF4: Selecciona una orden, calcula IVA y total,
    emite la factura y cambia el estado de la orden.
    """
    conn = conectar_db(db)
    cursor = conn.cursor()

    try:
        # 1. Verificar el estado actual de la orden
        cursor.execute("SELECT estado FROM ordenes_compra WHERE id = ?", (orden_id,))
        orden = cursor.fetchone()

        if not orden:
            print(f" Error: Orden de Compra N° {orden_id} no encontrada.")
            return False

        if orden[0] == 'Facturada':
            print(f" Advertencia: Orden de Compra N° {orden_id} ya ha sido facturada.")
            return False

        cursor.execute("SELECT monto_neto FROM ordenes_compra WHERE id = ?", (orden_id,))
        monto_neto_total = cursor.fetchone()[0] or 0.0
        
        # 3. Calcular IVA y Total a Pagar
        monto_iva = calcular_iva(monto_neto_total)
        monto_total = calcular_total_bruto(monto_neto_total)

        # 4. Registrar la nueva Factura
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO facturas (orden_id, fecha_emision, monto_neto, monto_iva, monto_total, estado_envio) VALUES (?, ?, ?, ?, ?, ?)",
            (orden_id, fecha_actual, monto_neto_total, monto_iva, monto_total, 'Pendiente')
        )
        
        factura_id = cursor.lastrowid # Obtener el ID de la factura recién creada

        # 5. Cambiar el estado de la Orden a "Facturada"
        cursor.execute(
            "UPDATE ordenes_compra SET estado = 'Facturada' WHERE id = ?",
            (orden_id,)
        )
        
        conn.commit()
        print(f" Factura N° {factura_id} emitida para Orden N° {orden_id}:")
        print(f"   Neto: ${monto_neto_total:,.2f}")
        print(f"   IVA (19%): ${monto_iva:,.2f}")
        print(f"   Total a Pagar: ${monto_total:,.2f}")
        return True

    except sqlite3.IntegrityError:
        print(f" Error de integridad: Ya existe una factura para la Orden N° {orden_id}.")
        return False
    except Exception as e:
        conn.rollback()
        print(f" Ocurrió un error al emitir la factura: {e}")
        return False
    finally:
        conn.close()