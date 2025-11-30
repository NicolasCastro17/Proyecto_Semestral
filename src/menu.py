from pathlib import Path
from orden_compra import listarOc, crearOc, detalleOc
from factura import emitir_factura, listar_facturas
from envio import registrar_envio, listar_envios

def Menu(usuario: str, db: Path):
    while True:
        print("=== Menú Principal ===")
        print("1) Listar Órdenes de Compra")
        print("2) Crear Orden de Compra")
        print("3) Ver Detalle de una OC")
        print("4) Emitir Factura")
        print("5) Listar Facturas")
        print("6) Registrar Envío")
        print("7) Listar Envíos")
        print("8) Cerrar sesión")
        op = input("Seleccione opción: ").strip()
        if op == "1":
            listarOc(db)
        elif op == "2":
            crearOc(db)
        elif op == "3":
            detalleOc(db)
        elif op == "4":
            emitir_factura(db)
        elif op == "5":
            listar_facturas(db)
        elif op == "6":
            registrar_envio(db)
        elif op == "7":
            listar_envios(db)
        elif op == "8":
            print(f"Hasta luego, {usuario}\n")
            break
        else:
            print("Opción inválida.\n")