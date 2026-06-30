from config.database import Database
from datetime import datetime


class ReservaModel:
    """
    Modelo de datos para Reserva y Reserva_Automovil.
    Gestiona transacciones SQL atómicas.
    """

    @staticmethod
    def listar_todos():
        query = """
            SELECT 
                r.nro_reserva, r.id_cliente, r.id_usuario, r.id_ambito,
                r.fecha_inicio, r.fecha_final, r.precio_total, r.estado,
                p.nombre_completo AS cliente_nombre,
                u.username AS usuario_nombre,
                a.descripcion AS ambito_descripcion,
                ra.id_vehiculo, ra.litros_gasolina_salida, ra.litros_gasolina_retorno,
                ra.kilometraje_salida, ra.kilometraje_retorno,
                au.placa, au.marca, au.modelo
            FROM reserva r
            INNER JOIN persona p ON r.id_cliente = p.id_persona
            INNER JOIN usuario u ON r.id_usuario = u.id_persona
            INNER JOIN ambito_uso a ON r.id_ambito = a.id_ambito
            LEFT JOIN reserva_automovil ra ON r.nro_reserva = ra.nro_reserva
            LEFT JOIN automovil au ON ra.id_vehiculo = au.id_vehiculo
            ORDER BY r.nro_reserva DESC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def obtener_por_id(nro_reserva):
        query = """
            SELECT 
                r.nro_reserva, r.id_cliente, r.id_usuario, r.id_ambito,
                r.fecha_inicio, r.fecha_final, r.precio_total, r.estado,
                p.nombre_completo AS cliente_nombre,
                u.username AS usuario_nombre,
                a.descripcion AS ambito_descripcion,
                ra.id_vehiculo, ra.litros_gasolina_salida, ra.litros_gasolina_retorno,
                ra.kilometraje_salida, ra.kilometraje_retorno,
                au.placa, au.marca, au.modelo
            FROM reserva r
            INNER JOIN persona p ON r.id_cliente = p.id_persona
            INNER JOIN usuario u ON r.id_usuario = u.id_persona
            INNER JOIN ambito_uso a ON r.id_ambito = a.id_ambito
            LEFT JOIN reserva_automovil ra ON r.nro_reserva = ra.nro_reserva
            LEFT JOIN automovil au ON ra.id_vehiculo = au.id_vehiculo
            WHERE r.nro_reserva = %s
            LIMIT 1
        """
        return Database.execute_query(query, (nro_reserva,), fetch_one=True)

    @staticmethod
    def crear(datos):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar reserva
            cursor.execute("""
                INSERT INTO reserva 
                    (id_cliente, id_usuario, id_ambito, fecha_inicio, fecha_final, precio_total, estado)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s)
            """, (
                datos['id_cliente'], datos['id_usuario'], datos['id_ambito'],
                datos['fecha_inicio'], datos['fecha_final'], datos['precio_total'], datos['estado']
            ))
            nro_reserva = cursor.lastrowid

            # 2. Insertar reserva_automovil
            cursor.execute("""
                INSERT INTO reserva_automovil 
                    (nro_reserva, id_vehiculo, litros_gasolina_salida, litros_gasolina_retorno, kilometraje_salida, kilometraje_retorno)
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
            """, (
                nro_reserva, datos['id_vehiculo'],
                datos.get('litros_gasolina_salida', 0), datos.get('litros_gasolina_retorno', 0),
                datos.get('kilometraje_salida', 0), datos.get('kilometraje_retorno', 0)
            ))

            # 3. Marcar vehículo como ALQUILADO si estado es ACTIVA o PENDIENTE
            if datos['estado'] in ('ACTIVA', 'PENDIENTE'):
                cursor.execute("""
                    UPDATE automovil SET estado = 'ALQUILADO' WHERE id_vehiculo = %s
                """, (datos['id_vehiculo'],))

            conn.commit()
            return nro_reserva
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar(nro_reserva, datos):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Obtener vehículo anterior para posible liberación
            cursor.execute("""
                SELECT id_vehiculo FROM reserva_automovil WHERE nro_reserva = %s
            """, (nro_reserva,))
            row = cursor.fetchone()
            old_vehiculo = row[0] if row else None

            # 2. Actualizar reserva
            cursor.execute("""
                UPDATE reserva 
                SET id_cliente = %s, id_usuario = %s, id_ambito = %s,
                    fecha_inicio = %s, fecha_final = %s, precio_total = %s, estado = %s
                WHERE nro_reserva = %s
            """, (
                datos['id_cliente'], datos['id_usuario'], datos['id_ambito'],
                datos['fecha_inicio'], datos['fecha_final'], datos['precio_total'],
                datos['estado'], nro_reserva
            ))

            # 3. Actualizar reserva_automovil
            cursor.execute("""
                UPDATE reserva_automovil 
                SET id_vehiculo = %s, litros_gasolina_salida = %s, litros_gasolina_retorno = %s,
                    kilometraje_salida = %s, kilometraje_retorno = %s
                WHERE nro_reserva = %s
            """, (
                datos['id_vehiculo'], datos.get('litros_gasolina_salida', 0),
                datos.get('litros_gasolina_retorno', 0), datos.get('kilometraje_salida', 0),
                datos.get('kilometraje_retorno', 0), nro_reserva
            ))

            # 4. Ajustar estado de vehículos
            if old_vehiculo and old_vehiculo != datos['id_vehiculo']:
                cursor.execute("UPDATE automovil SET estado = 'DISPONIBLE' WHERE id_vehiculo = %s", (old_vehiculo,))

            if datos['estado'] in ('ACTIVA', 'PENDIENTE'):
                cursor.execute("UPDATE automovil SET estado = 'ALQUILADO' WHERE id_vehiculo = %s", (datos['id_vehiculo'],))
            elif datos['estado'] in ('COMPLETADA', 'CANCELADA'):
                cursor.execute("UPDATE automovil SET estado = 'DISPONIBLE' WHERE id_vehiculo = %s", (datos['id_vehiculo'],))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar(nro_reserva):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            # Liberar vehículo antes de borrar relación
            cursor.execute("""
                SELECT id_vehiculo FROM reserva_automovil WHERE nro_reserva = %s
            """, (nro_reserva,))
            row = cursor.fetchone()
            id_vehiculo = row[0] if row else None

            cursor.execute("DELETE FROM pago WHERE nro_reserva = %s", (nro_reserva,))
            cursor.execute("DELETE FROM reserva_automovil WHERE nro_reserva = %s", (nro_reserva,))
            cursor.execute("DELETE FROM reserva WHERE nro_reserva = %s", (nro_reserva,))

            if id_vehiculo:
                cursor.execute("UPDATE automovil SET estado = 'DISPONIBLE' WHERE id_vehiculo = %s", (id_vehiculo,))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def listar_clientes():
        query = """
            SELECT p.id_persona, p.ci, p.nombre_completo
            FROM persona p
            INNER JOIN cliente c ON p.id_persona = c.id_persona
            ORDER BY p.nombre_completo ASC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_usuarios():
        query = """
            SELECT p.id_persona, p.nombre_completo, u.username
            FROM persona p
            INNER JOIN usuario u ON p.id_persona = u.id_persona
            WHERE u.estado_usuario = 'ACTIVO'
            ORDER BY p.nombre_completo ASC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_ambitos():
        query = """
            SELECT id_ambito, descripcion, costo_adicional 
            FROM ambito_uso 
            ORDER BY descripcion ASC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_vehiculos_disponibles(excluir_id=None):
        query = """
            SELECT id_vehiculo, placa, marca, modelo, id_categoria
            FROM automovil
            WHERE estado = 'DISPONIBLE'
            ORDER BY placa ASC
        """
        params = ()
        if excluir_id:
            query = """
                SELECT id_vehiculo, placa, marca, modelo, id_categoria
                FROM automovil
                WHERE estado = 'DISPONIBLE' OR id_vehiculo = %s
                ORDER BY placa ASC
            """
            params = (excluir_id,)
        return Database.execute_query(query, params, fetch_all=True)

    @staticmethod
    def obtener_tarifa_categoria(id_categoria):
        query = """
            SELECT tarifa_diaria, costo_seguro_dia 
            FROM categoria 
            WHERE id_categoria = %s 
            LIMIT 1
        """
        return Database.execute_query(query, (id_categoria,), fetch_one=True)

    @staticmethod
    def obtener_costo_ambito(id_ambito):
        query = """
            SELECT costo_adicional 
            FROM ambito_uso 
            WHERE id_ambito = %s 
            LIMIT 1
        """
        return Database.execute_query(query, (id_ambito,), fetch_one=True)
