from pathlib import Path
from orden_compra import listarOc, crearOc, detalleOc

def Menu(usuario: str, db: Path):
    while True:
        print("=== Menú Principal ===")
        print("1) Listar Órdenes de Compra")
        print("2) Crear Orden de Compra")
        print("3) Ver Detalle de una OC")
        print("4) Home")
        print("5) Cerrar sesión")
        op = input("Seleccione opción: ").strip()
        if op == "1":
            listarOc(db)
        elif op == "2":
            crearOc(db)
        elif op == "3":
            detalleOc(db)
        elif op == "4":
            print("\nVolviendo a Home...\n")
        elif op == "5":
            print(f"Hasta luego, {usuario}\n")
            break
        else:
            print("Opción inválida.\n")
#menu creado