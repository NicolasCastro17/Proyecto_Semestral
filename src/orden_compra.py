import json
import sqlite3
from pathlib import Path

def _get_conn(db: Path):
    db.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db)

def crearOc(db: Path):
    print("\n=== Nueva Orden de Compra ===")
    numero = input("Número de OC: ").strip()
    cliente = input("Cliente: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    comuna = input("Comuna: ").strip()
    region = input("Región: ").strip()

    items = []
    while True:
        prod = input("Producto (ENTER para terminar): ").strip()
        if not prod:
            break
        precio = int(input("Precio: "))
        items.append({"producto": prod, "precio": precio})

    total = sum(i["precio"] for i in items)

    with _get_conn(db) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO ordenes_compra
              (numero, cliente, direccion, telefono, comuna, region, items_json, total, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'OC_CREADA')
        """, (numero, cliente, direccion, telefono, comuna, region, json.dumps(items), total))
        conn.commit()

    print("✅ Orden registrada correctamente.\n")

def listarOc(db: Path):
    with _get_conn(db) as conn:
        c = conn.cursor()
        c.execute("SELECT id, numero, cliente, total, estado FROM ordenes_compra ORDER BY id DESC")
        rows = c.fetchall()

    if not rows:
        print("\n(No hay órdenes cargadas)\n")
        return

    print("\n=== Órdenes de Compra ===")
    for r in rows:
        print(f"[{r[0]}] N° {r[1]} | Cliente: {r[2]} | Total: ${r[3]} | Estado: {r[4]}")
    print("")

def detalleOc(db: Path):
    oc_id = input("ID de la OC: ").strip()
    with _get_conn(db) as conn:
        c = conn.cursor()
        c.execute("""
          SELECT numero, cliente, direccion, telefono, comuna, region, items_json, total, estado
          FROM ordenes_compra WHERE id=?
        """, (oc_id,))
        row = c.fetchone()

    if not row:
        print("OC no encontrada.\n")
        return

    numero, cliente, direccion, telefono, comuna, region, items_json, total, estado = row
    print("\n=== Detalle OC ===")
    print(f"N°: {numero}")
    print(f"Cliente: {cliente}")
    print(f"Dirección: {direccion}, {comuna}, {region}. Tel: {telefono}")
    items = json.loads(items_json)
    for i, it in enumerate(items, 1):
        print(f"  {i}. {it['producto']} - ${it['precio']}")
    print(f"TOTAL: ${total} | Estado: {estado}\n")