from config.database import Database


class AuditoriaModel:
    """
    Modelo de datos para Auditoría.
    Gestiona consultas de trazabilidad con filtros dinámicos.
    """

    @staticmethod
    def listar_todos(filtros=None):
        where_clauses = []
        params = []
        if filtros:
            if filtros.get('id_usuario'):
                where_clauses.append("a.id_usuario = %s")
                params.append(filtros['id_usuario'])
            if filtros.get('accion'):
                where_clauses.append("a.accion = %s")
                params.append(filtros['accion'])
            if filtros.get('fecha_desde'):
                where_clauses.append("DATE(a.fecha_hora) >= %s")
                params.append(filtros['fecha_desde'])
            if filtros.get('fecha_hasta'):
                where_clauses.append("DATE(a.fecha_hora) <= %s")
                params.append(filtros['fecha_hasta'])

        where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        query = f"""
            SELECT 
                a.id_auditoria, a.id_usuario, a.accion, a.tabla_afectada,
                a.id_registro, a.fecha_hora,
                u.username
            FROM auditoria a
            LEFT JOIN usuario u ON a.id_usuario = u.id_persona
            {where_str}
            ORDER BY a.fecha_hora DESC
            LIMIT 500
        """
        return Database.execute_query(query, tuple(params) if params else None, fetch_all=True)

    @staticmethod
    def listar_usuarios_distintos():
        query = """
            SELECT DISTINCT a.id_usuario, u.username 
            FROM auditoria a
            LEFT JOIN usuario u ON a.id_usuario = u.id_persona
            WHERE a.id_usuario IS NOT NULL
            ORDER BY u.username ASC
        """
        return Database.execute_query(query, fetch_all=True)

    @staticmethod
    def listar_acciones_distintas():
        query = "SELECT DISTINCT accion FROM auditoria ORDER BY accion ASC"
        return Database.execute_query(query, fetch_all=True)
