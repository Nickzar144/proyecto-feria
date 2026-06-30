from models.automovil_model import AutomovilModel
from models.mantenimiento_model import MantenimientoModel


class FlotaController:
    """
    Controlador de la gestión de flota y taller.
    Contiene la lógica de negocio, validaciones y comunicación Modelo-Vista.
    """

    def __init__(self):
        self.automovil_model = AutomovilModel()
        self.mantenimiento_model = MantenimientoModel()

    # ─── Vehículos ───

    def listar_vehiculos(self):
        try:
            data = self.automovil_model.listar_todos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_categorias(self):
        try:
            data = self.automovil_model.listar_categorias()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def guardar_vehiculo(self, datos):
        if not datos.get("placa") or not datos["placa"].strip():
            return {"success": False, "message": "La placa es obligatoria."}
        if not datos.get("marca") or not datos["marca"].strip():
            return {"success": False, "message": "La marca es obligatoria."}
        if not datos.get("modelo") or not datos["modelo"].strip():
            return {"success": False, "message": "El modelo es obligatorio."}

        try:
            anio = int(datos.get("anio", 0))
            if anio < 1900 or anio > 2100:
                return {"success": False, "message": "El año debe estar entre 1900 y 2100."}
        except ValueError:
            return {"success": False, "message": "El año debe ser un número entero válido."}

        try:
            km = float(datos.get("kilometraje", 0))
            if km < 0:
                return {"success": False, "message": "El kilometraje no puede ser negativo."}
        except ValueError:
            return {"success": False, "message": "El kilometraje debe ser un número válido."}

        if datos.get("estado") not in ["DISPONIBLE", "ALQUILADO", "MANTENIMIENTO", "INACTIVO"]:
            return {"success": False, "message": "Estado no válido."}

        if not datos.get("id_categoria"):
            return {"success": False, "message": "Debe seleccionar una categoría."}

        datos["placa"] = datos["placa"].strip().upper()
        datos["marca"] = datos["marca"].strip()
        datos["modelo"] = datos["modelo"].strip()
        datos["color"] = datos.get("color", "").strip()
        datos["anio"] = anio
        datos["kilometraje"] = km

        try:
            if datos.get("id_vehiculo"):
                self.automovil_model.actualizar(datos["id_vehiculo"], datos)
                return {"success": True, "message": "Vehículo actualizado correctamente."}
            else:
                new_id = self.automovil_model.crear(datos)
                return {"success": True, "message": "Vehículo registrado correctamente.", "id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error de base de datos: {e}"}

    def eliminar_vehiculo(self, id_vehiculo):
        try:
            self.automovil_model.eliminar(id_vehiculo)
            return {"success": True, "message": "Vehículo eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # ─── Mantenimiento ───

    def listar_mantenimientos(self):
        try:
            data = self.mantenimiento_model.listar_todos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_mantenimientos_por_vehiculo(self, id_vehiculo):
        try:
            data = self.mantenimiento_model.listar_por_vehiculo(id_vehiculo)
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def guardar_mantenimiento(self, datos):
        if not datos.get("id_vehiculo"):
            return {"success": False, "message": "Debe seleccionar un vehículo."}
        if not datos.get("tipo") or not datos["tipo"].strip():
            return {"success": False, "message": "El tipo de mantenimiento es obligatorio."}

        try:
            costo = float(datos.get("costo", 0))
            if costo < 0:
                return {"success": False, "message": "El costo no puede ser negativo."}
        except ValueError:
            return {"success": False, "message": "El costo debe ser un número válido."}

        if not datos.get("fecha_inicio"):
            return {"success": False, "message": "La fecha de inicio es obligatoria (YYYY-MM-DD)."}

        if datos.get("fecha_fin") and datos["fecha_fin"] < datos["fecha_inicio"]:
            return {"success": False, "message": "La fecha de fin no puede ser anterior a la fecha de inicio."}

        datos["tipo"] = datos["tipo"].strip()
        datos["descripcion"] = datos.get("descripcion", "").strip()
        datos["costo"] = costo

        try:
            if datos.get("id_mantenimiento"):
                self.mantenimiento_model.actualizar(datos["id_mantenimiento"], datos)
                return {"success": True, "message": "Mantenimiento actualizado correctamente."}
            else:
                new_id = self.mantenimiento_model.crear(datos)
                return {"success": True, "message": "Mantenimiento registrado correctamente.", "id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error de base de datos: {e}"}

    def eliminar_mantenimiento(self, id_mantenimiento):
        try:
            self.mantenimiento_model.eliminar(id_mantenimiento)
            return {"success": True, "message": "Mantenimiento eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": str(e)}
