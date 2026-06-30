from config.database import Database


class AutomovilModel:
    """
    Modelo de datos para la entidad Automovil.
    Gestiona exclusivamente consultas SQL parametrizadas.
    """

    @staticmethod
    def listar_todos():
        query = """
            SELECT 
                a.id_vehiculo, a.placa, a.marca, a.modelo, a.anio,
                a.color, a.kilometraje, a.estado, a.id_categoria,
                c.nombre_categoria
            FROM automovil a
            INNER JOIN categoria c ON a.id_categoria = c.id_categoria
            ORDER BY a.id_vehiculo DESC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def obtener_por_id(id_vehiculo):
        query = """
            SELECT 
                a.id_vehiculo, a.placa, a.marca, a.modelo, a.anio,
                a.color, a.kilometraje, a.estado, a.id_categoria,
                c.nombre_categoria
            FROM automovil a
            INNER JOIN categoria c ON a.id_categoria = c.id_categoria
            WHERE a.id_vehiculo = %s
            LIMIT 1
        """
        return Database.execute_query(query, (id_vehiculo,), fetch_one=True)

    @staticmethod
    def crear(datos):
        query = """
            INSERT INTO automovil 
                (placa, marca, modelo, anio, color, kilometraje, estado, id_categoria)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            datos['placa'], datos['marca'], datos['modelo'],
            datos['anio'], datos['color'], datos['kilometraje'],
            datos['estado'], datos['id_categoria']
        )
        return Database.execute_query(query, params)

    @staticmethod
    def actualizar(id_vehiculo, datos):
        query = """
            UPDATE automovil 
            SET placa = %s, marca = %s, modelo = %s, anio = %s,
                color = %s, kilometraje = %s, estado = %s, id_categoria = %s
            WHERE id_vehiculo = %s
        """
        params = (
            datos['placa'], datos['marca'], datos['modelo'],
            datos['anio'], datos['color'], datos['kilometraje'],
            datos['estado'], datos['id_categoria'], id_vehiculo
        )
        Database.execute_query(query, params)

    @staticmethod
    def eliminar(id_vehiculo):
        query = "DELETE FROM automovil WHERE id_vehiculo = %s"
        Database.execute_query(query, (id_vehiculo,))

    @staticmethod
    def listar_categorias():
        query = """
            SELECT id_categoria, nombre_categoria 
            FROM categoria 
            ORDER BY nombre_categoria ASC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_por_estado(estado):
        query = """
            SELECT 
                a.id_vehiculo, a.placa, a.marca, a.modelo, a.anio,
                a.color, a.kilometraje, a.estado, a.id_categoria,
                c.nombre_categoria
            FROM automovil a
            INNER JOIN categoria c ON a.id_categoria = c.id_categoria
            WHERE a.estado = %s
            ORDER BY a.id_vehiculo DESC
        """
        return Database.execute_query(query, (estado,), fetch_all=True)
