-- ============================================================
-- MOVISHARE - Datos completos de prueba para todas las funcionalidades
-- Este script cubre: usuarios, clientes, vehículos, mantenimiento,
-- reservas y pagos.
-- ============================================================

USE movishare_db;

-- ============================================================
-- 1. USUARIOS ADICIONALES (Operador y Técnico)
-- ============================================================

INSERT INTO persona (id_persona, ci, nombre_completo, telefono, direccion) VALUES
(3, '9876543', 'María González López', '77798765', 'Calle Bolívar #456'),
(4, '4567890', 'Carlos Rodríguez Silva', '77745678', 'Av. Panamericana #789');

INSERT INTO usuario (id_persona, username, contrasena, estado_usuario, id_rol) VALUES
(3, 'mgonzalez', '$2b$12$ug3l6wqJ9eWRV3kgAMGkS.e4k.uJntBGfWp/oCd6z9U3vWhav2ou2', 1, 2),
(4, 'crodriguez', '$2b$12$ug3l6wqJ9eWRV3kgAMGkS.e4k.uJntBGfWp/oCd6z9U3vWhav2ou2', 1, 3);

-- ============================================================
-- 2. CLIENTES ADICIONALES
-- ============================================================

INSERT INTO persona (id_persona, ci, nombre_completo, telefono, direccion) VALUES
(5, '7890123', 'Ana Martínez Ruiz', '77778901', 'Calle Sucre #321'),
(6, '3456789', 'Luis Fernández Castro', '77734567', 'Av. América #654'),
(7, '5678901', 'Diana Torres Paredes', '77756789', 'Calle Lanza #987');

INSERT INTO cliente (id_persona, email) VALUES
(5, 'ana.martinez@email.com'),
(6, 'luis.fernandez@email.com'),
(7, 'diana.torres@email.com');

INSERT INTO licencia (id_persona, nro_licencia, categoria, fecha_vencimiento) VALUES
(5, 'LIC-2023-045', 'B', '2026-12-15'),
(6, 'LIC-2022-112', 'C', '2027-03-20'),
(7, 'LIC-2024-078', 'B', '2028-08-10');

-- ============================================================
-- 3. VEHÍCULOS ADICIONALES (diversos estados)
-- ============================================================

INSERT INTO automovil (id_vehiculo, placa, marca, modelo, anio, color, kilometraje, estado, id_categoria) VALUES
(3, 'DEF9012', 'Ford', 'Focus', 2021, 'Gris', 32000.00, 'DISPONIBLE', 1),
(4, 'GHI3456', 'BMW', 'Serie 3', 2023, 'Azul', 8000.00, 'DISPONIBLE', 2),
(5, 'JKL7890', 'Toyota', 'RAV4', 2022, 'Plateado', 25000.00, 'DISPONIBLE', 3),
(6, 'MNO1234', 'Mercedes', 'GLE', 2023, 'Negro', 12000.00, 'DISPONIBLE', 4),
(7, 'PQR5678', 'Ford', 'Ranger', 2021, 'Rojo', 45000.00, 'MANTENIMIENTO', 5),
(8, 'STU9012', 'Hyundai', 'H1', 2020, 'Blanco', 60000.00, 'DISPONIBLE', 6),
(9, 'VWX3456', 'Porsche', '911', 2023, 'Amarillo', 5000.00, 'ALQUILADO', 7),
(10, 'YZA7890', 'Lincoln', 'Navigator', 2022, 'Negro', 18000.00, 'DISPONIBLE', 8);

-- ============================================================
-- 4. MANTENIMIENTOS (taller)
-- ============================================================

INSERT INTO mantenimiento (id_mantenimiento, id_vehiculo, tipo, descripcion, fecha_inicio, fecha_fin, costo) VALUES
(1, 7, 'PREVENTIVO', 'Cambio de aceite y filtros', '2025-01-10', '2025-01-10', 350.00),
(2, 7, 'CORRECTIVO', 'Reparación de sistema de frenos', '2025-02-15', '2025-02-18', 1200.00),
(3, 3, 'PREVENTIVO', 'Revisión general y alineación', '2025-03-05', '2025-03-05', 280.00),
(4, 5, 'CORRECTIVO', 'Cambio de batería y alternador', '2025-04-12', '2025-04-13', 850.00),
(5, 10, 'PREVENTIVO', 'Inspección de lujo pre-alquiler', '2025-05-20', '2025-05-20', 500.00);

-- ============================================================
-- 5. RESERVAS (diversos estados)
-- ============================================================

-- Reserva 1: COMPLETADA (pagada)
INSERT INTO reserva (nro_reserva, id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado) VALUES
(1, 2, 1, 2, '2025-01-15', '2025-01-18', 430.00, 'COMPLETADA');
INSERT INTO reserva_automovil (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno) VALUES
(1, 1, 45.00, 12.00, 15000.00, 15350.00);

-- Reserva 2: ACTIVA (pagada parcialmente)
INSERT INTO reserva (nro_reserva, id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado) VALUES
(2, 5, 3, 3, '2025-06-20', '2025-06-25', 810.00, 'ACTIVA');
INSERT INTO reserva_automovil (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno) VALUES
(2, 9, 60.00, 0.00, 5000.00, 0.00);

-- Reserva 3: PENDIENTE (sin pagar)
INSERT INTO reserva (nro_reserva, id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado) VALUES
(3, 6, 1, 1, '2025-07-01', '2025-07-03', 150.00, 'PENDIENTE');
INSERT INTO reserva_automovil (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno) VALUES
(3, 4, 55.00, 0.00, 8000.00, 0.00);

-- Reserva 4: CANCELADA
INSERT INTO reserva (nro_reserva, id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado) VALUES
(4, 7, 3, 4, '2025-02-10', '2025-02-15', 950.00, 'CANCELADA');
INSERT INTO reserva_automovil (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno) VALUES
(4, 6, 70.00, 0.00, 12000.00, 0.00);

-- Reserva 5: COMPLETADA
INSERT INTO reserva (nro_reserva, id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado) VALUES
(5, 2, 1, 5, '2025-03-08', '2025-03-10', 540.00, 'COMPLETADA');
INSERT INTO reserva_automovil (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno) VALUES
(5, 3, 40.00, 8.00, 32000.00, 32450.00);

-- ============================================================
-- 6. PAGOS
-- ============================================================

INSERT INTO pago (id_pago, nro_reserva, monto_pagado, fecha_pagado, metodo_pago) VALUES
(1, 1, 430.00, '2025-01-15', 'EFECTIVO'),
(2, 2, 400.00, '2025-06-18', 'TRANSFERENCIA'),
(3, 5, 540.00, '2025-03-08', 'TARJETA_CREDITO');

-- ============================================================
-- 7. AUDITORÍA (logs de prueba adicionales)
-- ============================================================

INSERT INTO auditoria (id_usuario, accion, tabla_afectada, id_registro, fecha_hora) VALUES
(1, 'LOGIN', 'usuario', 1, '2025-01-15 08:30:00'),
(1, 'INSERT', 'automovil', 3, '2025-01-16 09:15:00'),
(3, 'LOGIN', 'usuario', 3, '2025-02-20 10:00:00'),
(1, 'INSERT', 'reserva', 1, '2025-01-15 14:20:00'),
(1, 'UPDATE', 'reserva', 2, '2025-06-18 16:45:00'),
(4, 'LOGIN', 'usuario', 4, '2025-03-10 11:30:00'),
(1, 'DELETE', 'cliente', 7, '2025-04-05 09:00:00'),
(3, 'INSERT', 'pago', 2, '2025-06-18 17:00:00');
