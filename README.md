# Proyecto Semestral: Sistema de Órdenes de Compra, Facturación y Envíos

## Descripción del Proyecto

Sistema en consola desarrollado en Python que simula la gestión empresarial de órdenes de compra, facturación y envíos. Utiliza SQLite para el almacenamiento de datos y GitHub Actions para automatización de pruebas.

### Funcionalidades Implementadas

- **RF1**: Registro de órdenes de compra  
- **RF2**: Autenticación de usuarios  
- **RF3**: Menú principal del sistema  
- **RF4**: Emisión de facturas  
- **RF5**: Registro de envío de productos  

---

## Integrantes del Grupo

- Richard Moreano  
- Nicolás Castro  

---

## Estructura del Proyecto

```text
Proyecto_Semestral/
├── README.md
├── .gitignore
├── ci/
│   └── pipeline.yml        # Automatización con GitHub Actions
├── database/
│   └── proyecto.db         # Base de datos SQLite
├── evidencias/             # Capturas de pantalla
├── src/
│   ├── app.py              # Punto de entrada principal
│   ├── login.py            # Autenticación (RF2)
│   ├── menu.py             # Menú principal (RF3)
│   ├── orden_compra.py     # Órdenes de compra (RF1)
│   ├── factura.py          # Emisión de facturas (RF4)
│   └── envio.py            # Registro de envíos (RF5)
└── tests/
    └── test_rf4.py         # Pruebas automatizadas
```

---

## Funcionalidades del Sistema

### RF1 – Órdenes de Compra
- Crear nuevas órdenes de compra
- Registrar datos del cliente (nombre, dirección, teléfono, comuna, región)
- Agregar productos con sus precios
- Calcular el total automáticamente
- Estados: `OC_CREADA` → `FACTURADA` → `DESPACHADA`

### RF2 – Autenticación
- Sistema de login con usuario y contraseña
- Contraseña hasheada con SHA-256
- Máximo 3 intentos de acceso
- **Credenciales por defecto**: Usuario `admin` / Contraseña `admin123`

### RF3 – Menú Principal
Opciones disponibles:
- Listar todas las órdenes de compra
- Crear nueva orden
- Ver detalle de orden específica
- Emitir factura
- Listar facturas
- Registrar envío
- Listar envíos
- Cerrar sesión

### RF4 – Emisión de Facturas
- Seleccionar orden en estado `OC_CREADA`
- Cálculo automático: Neto + IVA (19%) = Total
- Actualización de estado a `FACTURADA`
- Estado inicial de envío: `NO_DESPACHADO`

### RF5 – Registro de Envío
- Seleccionar factura existente
- Crear registro en tabla `envios`
- Actualizar estado a `DESPACHADO`
- Flujo completo: OC → Factura → Envío

---

## Tecnologías Utilizadas

- **Lenguaje**: Python 3
- **Base de datos**: SQLite
- **Librerías**:
  - `sqlite3`: Gestión de base de datos
  - `hashlib`: Hash de contraseñas
  - `getpass`: Ocultamiento de contraseñas
  - `json`: Serialización de productos
  - `pathlib`: Manejo de rutas

---

## Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/NicolasCastro17/Proyecto_Semestral.git
cd Proyecto_Semestral
```

### 2. Ejecutar el programa
```bash
python src/app.py
```

**Alternativa:**
```bash
python -m src.app
```

---

## Pruebas Automatizadas

Ejecutar pruebas con pytest:
```bash
pytest
```

El archivo `tests/test_rf4.py` verifica:
- Creación correcta de registros en tabla `facturas`
- Cambio de estado de orden a `FACTURADA`
- Cálculo correcto del IVA (19%)

### Automatización con GitHub Actions

El archivo `ci/pipeline.yml` ejecuta automáticamente las pruebas al hacer push, verificando:
- Instalación de dependencias
- Ejecución de tests
- Integridad del código

---

## Ejemplo de Uso

### Crear una orden de compra
```
=== Nueva Orden de Compra ===
Número de OC: OC-001
Cliente: Empresa ABC
Dirección: Av. Providencia 123
Teléfono: +56912345678
Comuna: Providencia
Región: Metropolitana
Producto (ENTER para terminar): Laptop
Precio: 800000
Producto (ENTER para terminar): Mouse
Precio: 25000
Producto (ENTER para terminar): [ENTER]
✅ Orden registrada correctamente.
```

---

## Notas Técnicas

- La base de datos se crea automáticamente en la primera ejecución
- Las contraseñas se almacenan hasheadas (SHA-256), nunca en texto plano
- Sistema con validaciones y manejo de errores básico
- Uso de rutas relativas para portabilidad

---

