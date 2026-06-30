import re
from models.cliente_model import ClienteModel


class ClienteController:
    """
    Controlador de Clientes y Licencias.
    Valida la lógica de negocio y coordina Modelo-Vista.
    """

    def __init__(self):
        self.model = ClienteModel()

    def listar_clientes(self):
        try:
            data = self.model.listar_todos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def guardar_cliente(self, datos):
        # ── Validaciones ──
        if not datos.get("ci") or not datos["ci"].strip():
            return {"success": False, "message": "El C.I. es obligatorio."}
        if not datos.get("nombre_completo") or not datos["nombre_completo"].strip():
            return {"success": False, "message": "El nombre completo es obligatorio."}
        if not datos.get("telefono") or not datos["telefono"].strip():
            return {"success": False, "message": "El teléfono es obligatorio."}
        if not datos.get("email") or not datos["email"].strip():
            return {"success": False, "message": "El email es obligatorio."}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", datos["email"]):
            return {"success": False, "message": "El formato de email no es válido."}
        if not datos.get("nro_licencia") or not datos["nro_licencia"].strip():
            return {"success": False, "message": "El número de licencia es obligatorio."}
        if not datos.get("categoria_licencia") or not datos["categoria_licencia"].strip():
            return {"success": False, "message": "La categoría de licencia es obligatoria."}
        if not datos.get("fecha_vencimiento") or not datos["fecha_vencimiento"].strip():
            return {"success": False, "message": "La fecha de vencimiento de la licencia es obligatoria (YYYY-MM-DD)."}

        datos["ci"] = datos["ci"].strip()
        datos["nombre_completo"] = datos["nombre_completo"].strip()
        datos["telefono"] = datos["telefono"].strip()
        datos["direccion"] = datos.get("direccion", "").strip()
        datos["email"] = datos["email"].strip()
        datos["nro_licencia"] = datos["nro_licencia"].strip()
        datos["categoria_licencia"] = datos["categoria_licencia"].strip().upper()
        datos["fecha_vencimiento"] = datos["fecha_vencimiento"].strip()

        try:
            if datos.get("id_persona"):
                self.model.actualizar(datos["id_persona"], datos)
                return {"success": True, "message": "Cliente actualizado correctamente."}
            else:
                new_id = self.model.crear(datos)
                return {"success": True, "message": "Cliente registrado correctamente.", "id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error de base de datos: {e}"}

    def eliminar_cliente(self, id_persona):
        try:
            self.model.eliminar(id_persona)
            return {"success": True, "message": "Cliente eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": str(e)}
