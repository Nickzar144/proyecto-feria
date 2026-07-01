# MOVISHARE - Sistema de Gestión de Alquiler de Vehículos

## Descripción

Sistema de escritorio para la gestión integral de alquiler de vehículos, desarrollado bajo la arquitectura **Modelo-Vista-Controlador (MVC)**. Permite administrar flotas de vehículos, clientes, reservas, pagos, mantenimiento y generar reportes estadísticos con trazabilidad completa de auditoría.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| **Lenguaje** | Python 3.10+ |
| **Interfaz Gráfica (GUI)** | CustomTkinter 5.2.2 (ventanas modernas, soporte oscuro/claro) |
| **Base de Datos** | MySQL Server 8.0+ |
| **Conector MySQL** | mysql-connector-python 9.7.0 |
| **Seguridad** | bcrypt 4.1.3 (hashing NIST compliant) |
| **Reportes / Dashboard** | matplotlib 3.9.4 (gráficos embebidos en CustomTkinter) |
| **Variables de Entorno** | python-dotenv 1.2.2 |

---

## Estructura del Proyecto

```
movishare/
├── .env                    # Variables de entorno (credenciales MySQL) - NO subir a GitHub
├── .gitignore              # Exclusiones de Git (venv, .env, caches)
├── requirements.txt        # Dependencias de Python
├── README.md               # Este archivo
├── db/
│   ├── schema.sql          # Script DDL: creación de la base de datos y tablas
│   ├── seed_data.sql       # Datos base: roles, categorías, admin, config
│   └── test_data.sql       # Datos de prueba: usuarios, clientes, vehículos, reservas, pagos
└── src/
    ├── main.py              # Punto de entrada de la aplicación
    ├── config/
    │   └── database.py      # Pool de conexiones MySQL
    ├── controllers/
    │   ├── auth_controller.py     # Lógica de autenticación
    │   ├── cliente_controller.py  # Gestión de clientes y licencias
    │   ├── flota_controller.py   # Gestión de vehículos y mantenimiento
    │   ├── reporte_controller.py # KPIs, gráficos y auditoría
    │   └── reserva_controller.py # Reservas, cálculo de precios y pagos
    ├── models/
    │   ├── auditoria_model.py      # Logs de auditoría
    │   ├── automovil_model.py      # CRUD de vehículos
    │   ├── cliente_model.py        # CRUD de clientes (transaccional)
    │   ├── mantenimiento_model.py  # CRUD de mantenimientos
    │   ├── pago_model.py           # CRUD de pagos
    │   ├── persona_model.py        # CRUD base de personas
    │   ├── reserva_model.py        # CRUD de reservas (transaccional)
    │   └── usuario_model.py        # Autenticación y auditoría
    └── views/
        ├── login_view.py       # Pantalla de inicio de sesión
        ├── main_window.py      # Ventana principal con menú lateral
        ├── clientes_view.py    # CRUD de clientes y licencias
        ├── flota_view.py       # CRUD de vehículos y taller
        ├── reservas_view.py    # Reservas y control de pagos
        └── reportes_view.py    # Dashboard financiero y logs de auditoría
```

---

## Instalación y Configuración

### 1. Requisitos Previos

- **Python 3.10 o superior** instalado
- **MySQL Server 8.0+** instalado y ejecutándose en `localhost:3306`
- Acceso al usuario `root` de MySQL (o crear un usuario dedicado)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/Nickzar144/proyecto-feria.git
cd proyecto-feria
```

### 3. Crear el Archivo `.env`

En la raíz del proyecto, crea un archivo llamado `.env` con las credenciales de tu MySQL local:

```env
# MOVISHARE - Variables de Entorno
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=movishare_db
```

> ⚠️ **IMPORTANTE:** Este archivo ya está en `.gitignore` y no se sube a GitHub por seguridad.

### 4. Crear la Base de Datos y Datos

Ejecuta los tres scripts SQL en orden en tu cliente MySQL (MySQL Workbench, phpMyAdmin, o terminal):

```sql
-- 1. Crear la base de datos, tablas, índices y datos base
SOURCE /ruta/al/proyecto/db/schema.sql;

-- 2. Insertar datos de configuración (roles, categorías, admin)
SOURCE /ruta/al/proyecto/db/seed_data.sql;

-- 3. Insertar datos de prueba (usuarios, clientes, vehículos, reservas, pagos)
SOURCE /ruta/al/proyecto/db/test_data.sql;
```

**Desde la terminal de Windows (PowerShell):**

```powershell
mysql -u root -ptu_contraseña < "C:\ruta\al\proyecto\db\schema.sql"
mysql -u root -ptu_contraseña < "C:\ruta\al\proyecto\db\seed_data.sql"
mysql -u root -ptu_contraseña < "C:\ruta\al\proyecto\db\test_data.sql"
```

### 5. Instalar Dependencias de Python

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 6. Ejecutar la Aplicación

```bash
python src/main.py
```

---

## Credenciales de Prueba

### Usuario Administrador

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `admin123` |
| Rol | ADMINISTRADOR (acceso total) |

### Usuarios Adicionales (prueba de roles)

| Usuario | Contraseña | Rol |
|---|---|---|
| `mgonzalez` | `admin123` | OPERADOR (reservas, clientes) |
| `crodriguez` | `admin123` | TÉCNICO (flota, mantenimiento) |

---

## Funcionalidades del Sistema

### Módulo 1 - Login y Auditoría
- Autenticación con hashing seguro (bcrypt)
- Registro automático de LOGS de auditoría por cada acción del usuario

### Módulo 2 - Gestión de Flota
- CRUD completo de vehículos (placa, marca, modelo, categoría, estado)
- Control de taller: mantenimientos preventivos y correctivos con costos
- Estados de vehículos: `DISPONIBLE`, `ALQUILADO`, `MANTENIMIENTO`, `INACTIVO`

### Módulo 3 - Gestión de Clientes
- CRUD de clientes con datos personales
- Gestión de licencias de conducir (número, categoría, fecha de vencimiento)

### Módulo 4 - Reservas y Pagos
- Creación de contratos de alquiler con cálculo automático de precio
- Fórmula: `precio_total = (tarifa_diaria + seguro_día) × días + costo_adicional_ámbito`
- Control de gasolina y kilometraje (salida/retorno)
- Estados: `PENDIENTE`, `ACTIVA`, `COMPLETADA`, `CANCELADA`
- Registro de pagos asociados a cada reserva (métodos: Efectivo, Transferencia, Tarjeta)
- Transacciones atómicas: reserva + vehículo + pago con rollback automático

### Módulo 5 - Dashboard de Reportes
- **KPIs en tiempo real:** ingresos totales, total de reservas, vehículos activos, costos de mantenimiento
- **Gráficos matplotlib embebidos:**
  - Barras: Ingresos por mes
  - Pastel: Distribución de reservas por estado
- **Logs de Auditoría filtrables:** por usuario, acción y rango de fechas

---

## Arquitectura MVC

| Capa | Responsabilidad | Restricción |
|---|---|---|
| **Model** | Consultas SQL parametrizadas (`%s`), transacciones atómicas, retorno de datos puros | No importa tkinter/customtkinter |
| **View** | Renderizado de widgets CustomTkinter, eventos de usuario, tablas scrollables | No contiene SQL |
| **Controller** | Lógica de negocio, validaciones (fechas, números, campos obligatorios), encriptación bcrypt | Puente entre Model y View |

---

## Notas para Revisión

- El sistema fue probado en **Windows 11** con **Python 3.13** y **MySQL 8.0**.
- Todas las transacciones de inserción en cascada (cliente→licencia, reserva→vehículo→pago) usan `BEGIN / COMMIT / ROLLBACK` manual para garantizar integridad referencial.
- El pool de conexiones MySQL se inicializa una sola vez en `main.py` y se libera al cerrar la aplicación.

---

## Autor

Desarrollado como proyecto académico para el sistema **MOVISHARE** de gestión de alquiler de vehículos.
