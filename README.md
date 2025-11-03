
# Proyecto Semestral: Sistema de Órdenes de Compra y Facturación (Entrega 1)

## Descripción del Proyecto

Este proyecto implementa la Base Funcional de un sistema de gestión para una empresa que administra órdenes de compra, facturación y envío.

Esta Entrega 1 (Sprint 1) se centra en la persistencia de datos y el control de acceso, cumpliendo con los siguientes módulos principales:

- **Módulo de Login (RF2)**: Control de acceso seguro al sistema.
- **Módulo de Órdenes de Compra (RF1)**: Registro y almacenamiento de nuevas órdenes.
- **Menú Principal (RF3)**: Navegación entre las secciones del sistema.

## Integrantes del Grupo

- Richard Moreano
- Nicolás Castro

## Estructura del Proyecto

```
Proyecto_Semestral/
├── README.md
├── .gitignore
├── database/
│   └── proyecto.db          # Base de datos SQLite (se crea automáticamente)
├── evidencias/              # Capturas de pantalla del proceso de desarrollo
│   ├── branches.jpeg
│   ├── commits 1.png
│   ├── commit 2.jpeg
│   ├── feature dev2.jpeg
│   ├── issues.png
│   ├── kanban.png
│   ├── kanban done.jpeg
│   ├── pr dev.jpeg
│   ├── pr qa.jpeg
│   └── prs abiertos.png
└── src/                     # Código fuente del proyecto
    ├── app.py              # Punto de entrada principal
    ├── login.py            # Módulo de autenticación
    ├── menu.py             # Menú principal del sistema
    └── orden_compra.py     # Gestión de órdenes de compra
```

## Funcionalidades Implementadas

### 1. Sistema de Autenticación
- Login seguro con usuario y contraseña
- Contraseñas encriptadas usando SHA-256
- Usuario por defecto: `admin` / `admin123`
- Máximo 3 intentos de login
- Entrada de contraseña oculta en terminal

### 2. Gestión de Órdenes de Compra
- **Crear nueva orden**: Registro completo con datos del cliente y productos
- **Listar órdenes**: Vista de todas las órdenes con información resumida
- **Ver detalle**: Información completa de una orden específica
- Estados de orden: `OC_CREADA`, `FACTURADA`, `DESPACHADA`

### 3. Base de Datos
- SQLite con creación automática de tablas
- Tabla `usuarios`: Gestión de credenciales
- Tabla `ordenes_compra`: Almacenamiento de órdenes con productos en formato JSON

## Requisitos Técnicos

### Lenguaje y Base de Datos
- **Lenguaje**: Python 3.6+
- **Base de Datos**: SQLite (incluido en Python estándar)

### Librerías Utilizadas (Python estándar)
- `sqlite3`: Conexión y manipulación de la base de datos
- `hashlib`: Encriptación segura de contraseñas (SHA-256)
- `getpass`: Entrada de contraseña sin mostrarla en terminal
- `json`: Serialización de productos en la base de datos
- `pathlib`: Manejo robusto de rutas de archivos

## Instalación y Ejecución

### Prerrequisitos
- Python 3.6 o superior instalado en el sistema
- Terminal/CMD/PowerShell

### Pasos para ejecutar

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/NicolasCastro17/Proyecto_Semestral.git
   cd Proyecto_Semestral
   ```

2. **Ejecutar el programa**
   ```bash
   python src/app.py
   ```
   
   **Alternativa desde la raíz del proyecto:**
   ```bash
   python -m src.app
   ```

### Credenciales por defecto
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## Uso del Sistema

1. **Inicio de sesión**: Ingresa las credenciales por defecto
2. **Menú principal**: Selecciona entre las opciones disponibles:
   - `1`: Listar todas las órdenes de compra
   - `2`: Crear una nueva orden de compra
   - `3`: Ver detalle de una orden específica
   - `4`: Volver al menú principal
   - `5`: Cerrar sesión

### Ejemplo de uso - Crear orden de compra:
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

## Notas Técnicas

- La base de datos se crea automáticamente en la primera ejecución
- Los archivos se organizan usando rutas relativas robustas
- Las contraseñas se almacenan hasheadas, nunca en texto plano
- El sistema maneja errores de entrada y validaciones básicas
