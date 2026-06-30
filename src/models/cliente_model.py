from config.database import Database


class ClienteModel:
    """
    Modelo de datos para Cliente y Licencia.
    Gestiona la herencia con persona mediante transacciones atómicas.
    """

    @staticmethod
    def listar_todos():
        query = """
            SELECT 
                p.id_persona, p.ci, p.nombre_completo, p.telefono, p.direccion,
                c.email,
                l.id_licencia, l.nro_licencia, l.categoria AS categoria_licencia, l.fecha_vencimiento
            FROM persona p
            INNER JOIN cliente c ON p.id_persona = c.id_persona
            LEFT JOIN licencia l ON p.id_persona = l.id_persona
            ORDER BY p.id_persona DESC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def obtener_por_id(id_persona):
        query = """
            SELECT 
                p.id_persona, p.ci, p.nombre_completo, p.telefono, p.direccion,
                c.email,
                l.id_licencia, l.nro_licencia, l.categoria AS categoria_licencia, l.fecha_vencimiento
            FROM persona p
            INNER JOIN cliente c ON p.id_persona = c.id_persona
            LEFT JOIN licencia l ON p.id_persona = l.id_persona
            WHERE p.id_persona = %s
            LIMIT 1
        """
        return Database.execute_query(query, (id_persona,), fetch_one=True)

    @staticmethod
    def crear(datos):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Insertar persona
            cursor.execute("""
                INSERT INTO persona (ci, nombre_completo, telefono, direccion)
                VALUES (%s, %s, %s, %s)
            """, (datos['ci'], datos['nombre_completo'], datos['telefono'], datos['direccion']))
            id_persona = cursor.lastrowid

            # 2. Insertar cliente
            cursor.execute("""
                INSERT INTO cliente (id_persona, email)
                VALUES (%s, %s)
            """, (id_persona, datos['email']))

            # 3. Insertar licencia
            cursor.execute("""
                INSERT INTO licencia (id_persona, nro_licencia, categoria, fecha_vencimiento)
                VALUES (%s, %s, %s, %s)
            """, (id_persona, datos['nro_licencia'], datos['categoria_licencia'], datos['fecha_vencimiento']))

            conn.commit()
            return id_persona
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar(id_persona, datos):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            # 1. Actualizar persona
            cursor.execute("""
                UPDATE persona
                SET ci = %s, nombre_completo = %s, telefono = %s, direccion = %s
                WHERE id_persona = %s
            """, (datos['ci'], datos['nombre_completo'], datos['telefono'], datos['direccion'], id_persona))

            # 2. Actualizar cliente
            cursor.execute("""
                UPDATE cliente
                SET email = %s
                WHERE id_persona = %s
            """, (datos['email'], id_persona))

            # 3. Upsert licencia (si existe fila, actualizar; sino insertar)
            cursor.execute("""
                SELECT id_licencia FROM licencia WHERE id_persona = %s LIMIT 1
            """, (id_persona,))
            row = cursor.fetchone()
            if row:
                cursor.execute("""
                    UPDATE licencia
                    SET nro_licencia = %s, categoria = %s, fecha_vencimiento = %s
                    WHERE id_persona = %s
                """, (datos['nro_licencia'], datos['categoria_licencia'], datos['fecha_vencimiento'], id_persona))
            else:
                cursor.execute("""
                    INSERT INTO licencia (id_persona, nro_licencia, categoria, fecha_vencimiento)
                    VALUES (%s, %s, %s, %s)
                """, (id_persona, datos['nro_licencia'], datos['categoria_licencia'], datos['fecha_vencimiento']))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar(id_persona):
        # Por ON DELETE CASCADE o manualidad, borramos en orden inverso
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM licencia WHERE id_persona = %s", (id_persona,))
            cursor.execute("DELETE FROM cliente WHERE id_persona = %s", (id_persona,))
            cursor.execute("DELETE FROM persona WHERE id_persona = %s", (id_persona,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
