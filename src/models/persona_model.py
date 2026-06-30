from config.database import Database


class PersonaModel:
    """
    Modelo base para la entidad Persona.
    Provee operaciones atómicas sobre la tabla persona.
    """

    @staticmethod
    def insertar(datos):
        query = """
            INSERT INTO persona (ci, nombre_completo, telefono, direccion)
            VALUES (%s, %s, %s, %s)
        """
        params = (datos['ci'], datos['nombre_completo'], datos['telefono'], datos['direccion'])
        return Database.execute_query(query, params)

    @staticmethod
    def actualizar(id_persona, datos):
        query = """
            UPDATE persona
            SET ci = %s, nombre_completo = %s, telefono = %s, direccion = %s
            WHERE id_persona = %s
        """
        params = (datos['ci'], datos['nombre_completo'], datos['telefono'], datos['direccion'], id_persona)
        Database.execute_query(query, params)

    @staticmethod
    def eliminar(id_persona):
        query = "DELETE FROM persona WHERE id_persona = %s"
        Database.execute_query(query, (id_persona,))

    @staticmethod
    def obtener_por_ci(ci):
        query = "SELECT * FROM persona WHERE ci = %s LIMIT 1"
        return Database.execute_query(query, (ci,), fetch_one=True)

    @staticmethod
    def obtener_por_id(id_persona):
        query = "SELECT * FROM persona WHERE id_persona = %s LIMIT 1"
        return Database.execute_query(query, (id_persona,), fetch_one=True)
