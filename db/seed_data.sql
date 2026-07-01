-- INSERTS DE LA BASE DE DATOS
USE movishare_db;

-- ============================================================
-- 1. ROLES
-- ============================================================
INSERT INTO rol (id_rol, nombre_rol, descripcion) VALUES
(1, 'ADMINISTRADOR', 'Acceso total al sistema: flota, clientes, reservas, pagos, reportes y auditoría.'),
(2, 'OPERADOR', 'Acceso a reservas, clientes y gestión diaria de alquileres.'),
(3, 'TÉCNICO', 'Acceso exclusivo al módulo de mantenimiento y flota.');

-- ============================================================
-- 2. CATEGORÍAS DE VEHÍCULOS
-- ============================================================
INSERT INTO categoria (id_categoria, nombre_categoria, tarifa_diaria, costo_seguro_dia) VALUES
(1, 'SEDÁN ECONÓMICO',    45.00, 5.00),
(2, 'SEDÁN PREMIUM',      85.00, 8.00),
(3, 'SUV ESTÁNDAR',      120.00, 10.00),
(4, 'SUV PREMIUM',       180.00, 12.00),
(5, 'CAMIONETA CARGA',   150.00, 15.00),
(6, 'MINIVAN / VAN',     200.00, 15.00),
(7, 'DEPORTIVO',         350.00, 20.00),
(8, 'LIMOUSINE',         500.00, 25.00);

-- ============================================================
-- 3. ÁMBITOS DE USO
-- ============================================================
INSERT INTO ambito_uso (id_ambito, descripcion, costo_adicional) VALUES
(1, 'URBANO (ciudad)',            0.00),
(2, 'INTERURBANO (carretera)',   25.00),
(3, 'TURÍSTICO (rutas largas)',   50.00),
(4, 'FRONTERIZO / INTERNACIONAL',100.00),
(5, 'EVENTO CORPORATIVO',        30.00);

-- ============================================================
-- 4. USUARIO ADMINISTRADOR
-- Credenciales: username=admin  |  contraseña=admin123
-- Hash bcrypt generado con bcrypt==4.1.3 (NIST compliant)
-- ============================================================
INSERT INTO persona (id_persona, ci, nombre_completo, telefono, direccion) VALUES
(1, '0000000', 'Administrador del Sistema', '00000000', 'Oficina Central');

INSERT INTO usuario (id_persona, username, contrasena, estado_usuario, id_rol) VALUES
(1, 'admin', '$2b$12$ug3l6wqJ9eWRV3kgAMGkS.e4k.uJntBGfWp/oCd6z9U3vWhav2ou2', 1, 1);

-- ============================================================
-- 5. CLIENTE DE DEMOSTRACIÓN
-- ============================================================
INSERT INTO persona (id_persona, ci, nombre_completo, telefono, direccion) VALUES
(2, '1234567', 'Juan Pérez García', '77712345', 'Av. América #123');

INSERT INTO cliente (id_persona, email) VALUES
(2, 'juan.perez@email.com');

INSERT INTO licencia (id_persona, nro_licencia, categoria, fecha_vencimiento) VALUES
(2, 'LIC-2024-001', 'B', '2027-06-30');

-- ============================================================
-- 6. VEHÍCULOS DE DEMOSTRACIÓN
-- ============================================================
INSERT INTO automovil (id_vehiculo, placa, marca, modelo, anio, color, kilometraje, estado, id_categoria) VALUES
(1, 'ABC1234', 'Toyota', 'Corolla', 2023, 'Blanco', 15000.00, 'DISPONIBLE', 1),
(2, 'XYZ5678', 'Honda', 'CR-V', 2022, 'Negro', 28000.00, 'DISPONIBLE', 3);
