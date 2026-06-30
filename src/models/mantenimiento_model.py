from config.database import Database


class MantenimientoModel:
    """
    Modelo de datos para la entidad Mantenimiento.
    Gestiona exclusivamente consultas SQL parametrizadas.
    """

    @staticmethod
    def listar_todos():
        query = """
            SELECT 
                m.id_mantenimiento, m.id_vehiculo, m.tipo, m.descripcion,
                m.fecha_inicio, m.fecha_fin, m.costo,
                a.placa, a.marca, a.modelo
            FROM mantenimiento m
            INNER JOIN automovil a ON m.id_vehiculo = a.id_vehiculo
            ORDER BY m.fecha_inicio DESC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_por_vehiculo(id_vehiculo):
        query = """
            SELECT 
                m.id_mantenimiento, m.id_vehiculo, m.tipo, m.descripcion,
                m.fecha_inicio, m.fecha_fin, m.costo,
                a.placa, a.marca, a.modelo
            FROM mantenimiento m
            INNER JOIN automovil a ON m.id_vehiculo = a.id_vehiculo
            WHERE m.id_vehiculo = %s
            ORDER BY m.fecha_inicio DESC
        """
        return Database.execute_query(query, (id_vehiculo,), fetch_all=True)

    @staticmethod
    def obtener_por_id(id_mantenimiento):
        query = """
            SELECT 
                m.id_mantenimiento, m.id_vehiculo, m.tipo, m.descripcion,
                m.fecha_inicio, m.fecha_fin, m.costo,
                a.placa, a.marca, a.modelo
            FROM mantenimiento m
            INNER JOIN automovil a ON m.id_vehiculo = a.id_vehiculo
            WHERE m.id_mantenimiento = %s
            LIMIT 1
        """
        return Database.execute_query(query, (id_mantenimiento,), fetch_one=True)

    @staticmethod
    def crear(datos):
        query = """
            INSERT INTO mantenimiento 
                (id_vehiculo, tipo, descripcion, fecha_inicio, fecha_fin, costo)
            VALUES 
                (%s, %s, %s, %s, %s, %s)
        """
        params = (
            datos['id_vehiculo'], datos['tipo'], datos['descripcion'],
            datos['fecha_inicio'], datos['fecha_fin'], datos['costo']
        )
        return Database.execute_query(query, params)

    @staticmethod
    def actualizar(id_mantenimiento, datos):
        query = """
            UPDATE mantenimiento 
            SET id_vehiculo = %s, tipo = %s, descripcion = %s,
                fecha_inicio = %s, fecha_fin = %s, costo = %s
            WHERE id_mantenimiento = %s
        """
        params = (
            datos['id_vehiculo'], datos['tipo'], datos['descripcion'],
            datos['fecha_inicio'], datos['fecha_fin'], datos['costo'],
            id_mantenimiento
        )
        Database.execute_query(query, params)

    @staticmethod
    def eliminar(id_mantenimiento):
        query = "DELETE FROM mantenimiento WHERE id_mantenimiento = %s"
        Database.execute_query(query, (id_mantenimiento,))
