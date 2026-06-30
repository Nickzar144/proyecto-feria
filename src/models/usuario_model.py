import bcrypt
from config.database import Database


class UsuarioModel:
    """
    Modelo de datos para la entidad Usuario.
    Maneja únicamente consultas SQL parametrizadas y retorna datos puros.
    """

    @staticmethod
    def obtener_por_username(username):
        """
        Busca un usuario activo/inactivo por su nombre de usuario,
        incluyendo el nombre del rol asociado.
        """
        query = """
            SELECT 
                u.id_persona,
                u.username,
                u.contrasena,
                u.estado_usuario,
                u.id_rol,
                r.nombre_rol
            FROM usuario u
            INNER JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.username = %s
            LIMIT 1
        """
        return Database.execute_query(query, (username,), fetch_one=True)

    @staticmethod
    def verificar_contrasena(contrasena_plana, contrasena_hash):
        """
        Compara una contraseña en texto plano contra un hash almacenado
        usando bcrypt (NIST compliance).
        """
        if isinstance(contrasena_plana, str):
            contrasena_plana = contrasena_plana.encode('utf-8')
        if isinstance(contrasena_hash, str):
            contrasena_hash = contrasena_hash.encode('utf-8')
        return bcrypt.checkpw(contrasena_plana, contrasena_hash)

    @staticmethod
    def registrar_auditoria(id_usuario, accion, tabla_afectada, id_registro):
        """
        Inserta un registro en la tabla de auditoría para trazabilidad.
        """
        query = """
            INSERT INTO auditoria 
                (id_usuario, accion, tabla_afectada, id_registro, fecha_hora)
            VALUES 
                (%s, %s, %s, %s, NOW())
        """
        return Database.execute_query(
            query,
            (id_usuario, accion, tabla_afectada, id_registro)
        )
