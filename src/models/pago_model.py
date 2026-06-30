from config.database import Database


class PagoModel:
    """
    Modelo de datos para Pagos.
    Gestiona exclusivamente consultas SQL parametrizadas.
    """

    @staticmethod
    def listar_todos():
        query = """
            SELECT 
                p.id_pago, p.nro_reserva, p.monto_pagado, p.fecha_pagado, p.metodo_pago,
                r.id_cliente, r.precio_total, r.estado
            FROM pago p
            INNER JOIN reserva r ON p.nro_reserva = r.nro_reserva
            ORDER BY p.fecha_pagado DESC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_por_reserva(nro_reserva):
        query = """
            SELECT 
                p.id_pago, p.nro_reserva, p.monto_pagado, p.fecha_pagado, p.metodo_pago,
                r.id_cliente, r.precio_total, r.estado
            FROM pago p
            INNER JOIN reserva r ON p.nro_reserva = r.nro_reserva
            WHERE p.nro_reserva = %s
            ORDER BY p.fecha_pagado DESC
        """
        return Database.execute_query(query, (nro_reserva,), fetch_all=True)

    @staticmethod
    def obtener_por_id(id_pago):
        query = """
            SELECT 
                p.id_pago, p.nro_reserva, p.monto_pagado, p.fecha_pagado, p.metodo_pago,
                r.id_cliente, r.precio_total, r.estado
            FROM pago p
            INNER JOIN reserva r ON p.nro_reserva = r.nro_reserva
            WHERE p.id_pago = %s
            LIMIT 1
        """
        return Database.execute_query(query, (id_pago,), fetch_one=True)

    @staticmethod
    def crear(datos):
        query = """
            INSERT INTO pago (nro_reserva, monto_pagado, fecha_pagado, metodo_pago)
            VALUES (%s, %s, %s, %s)
        """
        params = (datos['nro_reserva'], datos['monto_pagado'], datos['fecha_pagado'], datos['metodo_pago'])
        return Database.execute_query(query, params)

    @staticmethod
    def actualizar(id_pago, datos):
        query = """
            UPDATE pago 
            SET nro_reserva = %s, monto_pagado = %s, fecha_pagado = %s, metodo_pago = %s
            WHERE id_pago = %s
        """
        params = (datos['nro_reserva'], datos['monto_pagado'], datos['fecha_pagado'], datos['metodo_pago'], id_pago)
        Database.execute_query(query, params)

    @staticmethod
    def eliminar(id_pago):
        query = "DELETE FROM pago WHERE id_pago = %s"
        Database.execute_query(query, (id_pago,))
