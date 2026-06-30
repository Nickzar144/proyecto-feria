from models.auditoria_model import AuditoriaModel
from config.database import Database


class ReporteController:
    """
    Controlador de Reportes y Auditoría.
    Procesa métricas financieras y trazabilidad para el dashboard.
    """

    def __init__(self):
        self.auditoria_model = AuditoriaModel()

    # ─── KPIs ───

    def get_kpis(self):
        q1 = "SELECT COALESCE(SUM(monto_pagado), 0) AS total FROM pago"
        q2 = "SELECT COUNT(*) AS total FROM reserva"
        q3 = "SELECT COUNT(*) AS total FROM automovil WHERE estado != 'INACTIVO'"
        q4 = "SELECT COALESCE(SUM(costo), 0) AS total FROM mantenimiento"

        r1 = Database.execute_query(q1, fetch_one=True)
        r2 = Database.execute_query(q2, fetch_one=True)
        r3 = Database.execute_query(q3, fetch_one=True)
        r4 = Database.execute_query(q4, fetch_one=True)

        return {
            "ingresos": float(r1['total']) if r1 else 0,
            "reservas": int(r2['total']) if r2 else 0,
            "vehiculos_activos": int(r3['total']) if r3 else 0,
            "costo_mantenimiento": float(r4['total']) if r4 else 0,
        }

    # ─── Gráficos ───

    def get_ingresos_por_mes(self, anio=None):
        if anio:
            query = """
                SELECT MONTH(fecha_pagado) AS mes, SUM(monto_pagado) AS total
                FROM pago
                WHERE YEAR(fecha_pagado) = %s
                GROUP BY MONTH(fecha_pagado)
                ORDER BY mes ASC
            """
            return Database.execute_query(query, (anio,), fetch_all=True)
        else:
            query = """
                SELECT MONTH(fecha_pagado) AS mes, SUM(monto_pagado) AS total
                FROM pago
                GROUP BY MONTH(fecha_pagado)
                ORDER BY mes ASC
            """
            return Database.execute_query(query, fetch_all=True)

    def get_reservas_por_estado(self):
        query = """
            SELECT estado, COUNT(*) AS total
            FROM reserva
            GROUP BY estado
            ORDER BY total DESC
        """
        return Database.execute_query(query, fetch_all=True)

    def get_mantenimientos_por_tipo(self):
        query = """
            SELECT tipo, COUNT(*) AS total, SUM(costo) AS costo_total
            FROM mantenimiento
            GROUP BY tipo
            ORDER BY total DESC
        """
        return Database.execute_query(query, fetch_all=True)

    # ─── Auditoría ───

    def listar_auditoria(self, filtros=None):
        try:
            data = self.auditoria_model.listar_todos(filtros)
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_usuarios_auditoria(self):
        try:
            data = self.auditoria_model.listar_usuarios_distintos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_acciones_auditoria(self):
        try:
            data = self.auditoria_model.listar_acciones_distintas()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}
