DROP DATABASE IF EXISTS movishare_db;
CREATE DATABASE movishare_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE movishare_db;

-- ============================================================
-- 1. TABLAS DE CONFIGURACIÓN BASE
-- ============================================================

CREATE TABLE rol (
    id_rol          INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol      VARCHAR(50) NOT NULL UNIQUE,
    descripcion     VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE categoria (
    id_categoria        INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria    VARCHAR(50) NOT NULL UNIQUE,
    tarifa_diaria       DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    costo_seguro_dia    DECIMAL(12,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB;

CREATE TABLE ambito_uso (
    id_ambito           INT AUTO_INCREMENT PRIMARY KEY,
    descripcion         VARCHAR(100) NOT NULL,
    costo_adicional     DECIMAL(12,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB;

-- ============================================================
-- 2. ENTIDADES PRINCIPALES (PERSONA, USUARIO, CLIENTE)
-- ============================================================

CREATE TABLE persona (
    id_persona      INT AUTO_INCREMENT PRIMARY KEY,
    ci              VARCHAR(20) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    telefono        VARCHAR(20),
    direccion       VARCHAR(150)
) ENGINE=InnoDB;

CREATE TABLE usuario (
    id_persona      INT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    contrasena      VARCHAR(255) NOT NULL,
    estado_usuario  ENUM('ACTIVO','INACTIVO','BLOQUEADO') NOT NULL DEFAULT 'ACTIVO',
    id_rol          INT NOT NULL,
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
) ENGINE=InnoDB;

CREATE TABLE cliente (
    id_persona      INT PRIMARY KEY,
    email           VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE licencia (
    id_licencia         INT AUTO_INCREMENT PRIMARY KEY,
    id_persona          INT NOT NULL,
    nro_licencia        VARCHAR(50) NOT NULL,
    categoria           VARCHAR(10) NOT NULL,
    fecha_vencimiento   DATE NOT NULL,
    FOREIGN KEY (id_persona) REFERENCES cliente(id_persona) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- 3. FLOTA Y MANTENIMIENTO
-- ============================================================

CREATE TABLE automovil (
    id_vehiculo     INT AUTO_INCREMENT PRIMARY KEY,
    placa           VARCHAR(15) NOT NULL UNIQUE,
    marca           VARCHAR(50) NOT NULL,
    modelo          VARCHAR(50) NOT NULL,
    anio            INT NOT NULL,
    color           VARCHAR(30),
    kilometraje     DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    estado          ENUM('DISPONIBLE','ALQUILADO','MANTENIMIENTO','INACTIVO') NOT NULL DEFAULT 'DISPONIBLE',
    id_categoria    INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
) ENGINE=InnoDB;

CREATE TABLE mantenimiento (
    id_mantenimiento    INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo         INT NOT NULL,
    tipo                VARCHAR(50) NOT NULL,
    descripcion         VARCHAR(255),
    fecha_inicio        DATE NOT NULL,
    fecha_fin           DATE,
    costo               DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (id_vehiculo) REFERENCES automovil(id_vehiculo) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- 4. RESERVAS Y PAGOS (NÚCLEO TRANSACCIONAL)
-- ============================================================

CREATE TABLE reserva (
    nro_reserva     INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente      INT NOT NULL,
    id_usuario      INT NOT NULL,
    id_ambito       INT NOT NULL,
    fecha_inicio    DATE NOT NULL,
    fecha_final     DATE NOT NULL,
    precio_total    DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    estado          ENUM('PENDIENTE','ACTIVA','COMPLETADA','CANCELADA') NOT NULL DEFAULT 'PENDIENTE',
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_persona),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_persona),
    FOREIGN KEY (id_ambito) REFERENCES ambito_uso(id_ambito)
) ENGINE=InnoDB;

CREATE TABLE reserva_automovil (
    nro_reserva                 INT PRIMARY KEY,
    id_vehiculo                 INT NOT NULL,
    litros_gasolina_salida      DECIMAL(8,2) DEFAULT 0.00,
    litros_gasolina_retorno     DECIMAL(8,2) DEFAULT 0.00,
    kilometraje_salida          DECIMAL(12,2) DEFAULT 0.00,
    kilometraje_retorno         DECIMAL(12,2) DEFAULT 0.00,
    FOREIGN KEY (nro_reserva) REFERENCES reserva(nro_reserva) ON DELETE CASCADE,
    FOREIGN KEY (id_vehiculo) REFERENCES automovil(id_vehiculo)
) ENGINE=InnoDB;

CREATE TABLE pago (
    id_pago         INT AUTO_INCREMENT PRIMARY KEY,
    nro_reserva     INT NOT NULL,
    monto_pagado    DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    fecha_pagado    DATE NOT NULL,
    metodo_pago     VARCHAR(30) NOT NULL,
    FOREIGN KEY (nro_reserva) REFERENCES reserva(nro_reserva) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- 5. AUDITORÍA Y TRAZABILIDAD
-- ============================================================

CREATE TABLE auditoria (
    id_auditoria    INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario      INT,
    accion          VARCHAR(50) NOT NULL,
    tabla_afectada  VARCHAR(50),
    id_registro     INT,
    fecha_hora      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- 6. ÍNDICES ESTRATÉGICOS
-- ============================================================

CREATE INDEX idx_usuario_login         ON usuario(username, estado_usuario);
CREATE INDEX idx_persona_nombre        ON persona(nombre_completo);
CREATE INDEX idx_automovil_estado      ON automovil(estado);
CREATE INDEX idx_mantenimiento_fechas  ON mantenimiento(fecha_inicio, fecha_fin);
CREATE INDEX idx_reserva_fechas        ON reserva(fecha_inicio, fecha_final);
CREATE INDEX idx_reserva_estado        ON reserva(estado);
CREATE INDEX idx_pago_fecha            ON pago(fecha_pagado);
CREATE INDEX idx_auditoria_registro    ON auditoria(id_usuario, fecha_hora);

-- ============================================================
-- 7. DATOS DE CONFIGURACIÓN BASE
-- ============================================================

INSERT INTO rol (nombre_rol, descripcion) VALUES
('ADMINISTRADOR', 'Acceso total al sistema: flota, clientes, reservas, pagos, reportes y auditoría.'),
('OPERADOR',      'Acceso a reservas, clientes y gestión diaria de alquileres.'),
('TÉCNICO',       'Acceso exclusivo al módulo de mantenimiento y flota.');

INSERT INTO categoria (nombre_categoria, tarifa_diaria, costo_seguro_dia) VALUES
('SEDÁN ECONÓMICO',    45.00, 5.00),
('SEDÁN PREMIUM',      85.00, 8.00),
('SUV ESTÁNDAR',      120.00, 10.00),
('SUV PREMIUM',       180.00, 12.00),
('CAMIONETA CARGA',   150.00, 15.00),
('MINIVAN / VAN',     200.00, 15.00),
('DEPORTIVO',         350.00, 20.00),
('LIMOUSINE',         500.00, 25.00);

INSERT INTO ambito_uso (descripcion, costo_adicional) VALUES
('URBANO (ciudad)',           0.00),
('INTERURBANO (carretera)',  25.00),
('TURÍSTICO (rutas largas)', 50.00),
('FRONTERIZO / INTERNACIONAL', 100.00),
('EVENTO CORPORATIVO',       30.00);

-- ============================================================
-- 8. USUARIO ADMINISTRADOR DE PRUEBA
-- Credenciales: username = admin  |  contraseña = admin123
-- ============================================================

INSERT INTO persona (ci, nombre_completo, telefono, direccion)
VALUES ('0000000', 'Administrador del Sistema', '00000000', 'Oficina Central');

INSERT INTO usuario (id_persona, username, contrasena, estado_usuario, id_rol)
VALUES (1, 'admin', '$2b$12$ug3l6wqJ9eWRV3kgAMGkS.e4k.uJntBGfWp/oCd6z9U3vWhav2ou2', 'ACTIVO', 1);

-- ============================================================
-- 9. DATOS DE DEMOSTRACIÓN OPCIONALES

-- ============================================================

-- Cliente de prueba
INSERT INTO persona (ci, nombre_completo, telefono, direccion)
VALUES ('1234567', 'Juan Pérez García', '77712345', 'Av. América #123');

INSERT INTO cliente (id_persona, email)
VALUES (2, 'juan.perez@email.com');

INSERT INTO licencia (id_persona, nro_licencia, categoria, fecha_vencimiento)
VALUES (2, 'LIC-2024-001', 'B', '2027-06-30');

-- Vehículo de prueba
INSERT INTO automovil (placa, marca, modelo, anio, color, kilometraje, estado, id_categoria)
VALUES ('ABC1234', 'Toyota', 'Corolla', 2023, 'Blanco', 15000.00, 'DISPONIBLE', 1);

INSERT INTO automovil (placa, marca, modelo, anio, color, kilometraje, estado, id_categoria)
VALUES ('XYZ5678', 'Honda', 'CR-V', 2022, 'Negro', 28000.00, 'DISPONIBLE', 3);
