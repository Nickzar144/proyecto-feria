from datetime import datetime
from models.reserva_model import ReservaModel
from models.pago_model import PagoModel


class ReservaController:
    """
    Controlador de Reservas y Pagos.
    Contiene la lógica de negocio, validaciones y cálculo automático de precios.
    """

    def __init__(self):
        self.reserva_model = ReservaModel()
        self.pago_model = PagoModel()

    # ─── Listados auxiliares ───

    def listar_reservas(self):
        try:
            data = self.reserva_model.listar_todos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_clientes(self):
        try:
            data = self.reserva_model.listar_clientes()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_usuarios(self):
        try:
            data = self.reserva_model.listar_usuarios()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_ambitos(self):
        try:
            data = self.reserva_model.listar_ambitos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_vehiculos_disponibles(self, excluir_id=None):
        try:
            data = self.reserva_model.listar_vehiculos_disponibles(excluir_id)
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_pagos(self):
        try:
            data = self.pago_model.listar_todos()
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def listar_pagos_por_reserva(self, nro_reserva):
        try:
            data = self.pago_model.listar_por_reserva(nro_reserva)
            return {"success": True, "data": data or []}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # ─── Cálculo de precio ───

    def calcular_precio(self, fecha_inicio, fecha_final, id_vehiculo, id_ambito):
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            ff = datetime.strptime(fecha_final, "%Y-%m-%d")
        except ValueError:
            return {"success": False, "message": "Las fechas deben tener formato YYYY-MM-DD."}

        if ff < fi:
            return {"success": False, "message": "La fecha final no puede ser anterior a la fecha de inicio."}

        dias = (ff - fi).days + 1
        if dias <= 0:
            dias = 1

        # Obtener categoría del vehículo
        vehiculos = self.reserva_model.listar_vehiculos_disponibles(excluir_id=id_vehiculo)
        categoria = None
        for v in vehiculos:
            if v['id_vehiculo'] == id_vehiculo:
                categoria = v['id_categoria']
                break
        # Si no está en disponibles, buscar directamente
        if categoria is None:
            from config.database import Database
            row = Database.execute_query(
                "SELECT id_categoria FROM automovil WHERE id_vehiculo = %s LIMIT 1",
                (id_vehiculo,), fetch_one=True
            )
            if row:
                categoria = row['id_categoria']

        if not categoria:
            return {"success": False, "message": "No se pudo determinar la categoría del vehículo."}

        tarifa = self.reserva_model.obtener_tarifa_categoria(categoria)
        if not tarifa:
            return {"success": False, "message": "No se encontró tarifa para la categoría del vehículo."}

        ambito = self.reserva_model.obtener_costo_ambito(id_ambito)
        if not ambito:
            return {"success": False, "message": "No se encontró información del ámbito de uso."}

        base = (float(tarifa['tarifa_diaria']) + float(tarifa['costo_seguro_dia'])) * dias
        adicional = float(ambito['costo_adicional'])
        total = round(base + adicional, 2)

        return {
            "success": True,
            "precio_total": total,
            "dias": dias,
            "detalle": {
                "tarifa_diaria": float(tarifa['tarifa_diaria']),
                "costo_seguro_dia": float(tarifa['costo_seguro_dia']),
                "dias": dias,
                "costo_adicional_ambito": adicional
            }
        }

    # ─── Reservas ───

    def guardar_reserva(self, datos):
        if not datos.get("id_cliente"):
            return {"success": False, "message": "Debe seleccionar un cliente."}
        if not datos.get("id_usuario"):
            return {"success": False, "message": "Debe seleccionar un usuario responsable."}
        if not datos.get("id_ambito"):
            return {"success": False, "message": "Debe seleccionar un ámbito de uso."}
        if not datos.get("id_vehiculo"):
            return {"success": False, "message": "Debe seleccionar un vehículo."}
        if not datos.get("fecha_inicio") or not datos.get("fecha_final"):
            return {"success": False, "message": "Las fechas de inicio y final son obligatorias (YYYY-MM-DD)."}
        if datos.get("estado") not in ("PENDIENTE", "ACTIVA", "COMPLETADA", "CANCELADA"):
            return {"success": False, "message": "Estado de reserva no válido."}

        try:
            litros_salida = float(datos.get("litros_gasolina_salida", 0))
            litros_retorno = float(datos.get("litros_gasolina_retorno", 0))
            km_salida = float(datos.get("kilometraje_salida", 0))
            km_retorno = float(datos.get("kilometraje_retorno", 0))
            if litros_salida < 0 or litros_retorno < 0 or km_salida < 0 or km_retorno < 0:
                return {"success": False, "message": "Los valores de gasolina y kilometraje no pueden ser negativos."}
        except ValueError:
            return {"success": False, "message": "Los valores de gasolina y kilometraje deben ser numéricos."}

        # Calcular precio si no viene explícito
        if not datos.get("precio_total"):
            calc = self.calcular_precio(datos['fecha_inicio'], datos['fecha_final'], datos['id_vehiculo'], datos['id_ambito'])
            if not calc["success"]:
                return calc
            datos["precio_total"] = calc["precio_total"]
        else:
            try:
                datos["precio_total"] = float(datos["precio_total"])
                if datos["precio_total"] < 0:
                    return {"success": False, "message": "El precio total no puede ser negativo."}
            except ValueError:
                return {"success": False, "message": "El precio total debe ser un valor numérico."}

        datos["litros_gasolina_salida"] = litros_salida
        datos["litros_gasolina_retorno"] = litros_retorno
        datos["kilometraje_salida"] = km_salida
        datos["kilometraje_retorno"] = km_retorno

        try:
            if datos.get("nro_reserva"):
                self.reserva_model.actualizar(datos["nro_reserva"], datos)
                return {"success": True, "message": "Reserva actualizada correctamente."}
            else:
                new_id = self.reserva_model.crear(datos)
                return {"success": True, "message": "Reserva registrada correctamente.", "id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error de base de datos: {e}"}

    def eliminar_reserva(self, nro_reserva):
        try:
            self.reserva_model.eliminar(nro_reserva)
            return {"success": True, "message": "Reserva eliminada correctamente."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # ─── Pagos ───

    def guardar_pago(self, datos):
        if not datos.get("nro_reserva"):
            return {"success": False, "message": "Debe asociar el pago a una reserva."}
        if not datos.get("monto_pagado"):
            return {"success": False, "message": "El monto pagado es obligatorio."}
        if not datos.get("fecha_pagado"):
            return {"success": False, "message": "La fecha de pago es obligatoria (YYYY-MM-DD)."}
        if not datos.get("metodo_pago") or not datos["metodo_pago"].strip():
            return {"success": False, "message": "El método de pago es obligatorio."}

        try:
            monto = float(datos["monto_pagado"])
            if monto <= 0:
                return {"success": False, "message": "El monto pagado debe ser mayor a cero."}
        except ValueError:
            return {"success": False, "message": "El monto pagado debe ser numérico."}

        datos["monto_pagado"] = monto
        datos["metodo_pago"] = datos["metodo_pago"].strip().upper()

        try:
            if datos.get("id_pago"):
                self.pago_model.actualizar(datos["id_pago"], datos)
                return {"success": True, "message": "Pago actualizado correctamente."}
            else:
                new_id = self.pago_model.crear(datos)
                return {"success": True, "message": "Pago registrado correctamente.", "id": new_id}
        except Exception as e:
            return {"success": False, "message": f"Error de base de datos: {e}"}

    def eliminar_pago(self, id_pago):
        try:
            self.pago_model.eliminar(id_pago)
            return {"success": True, "message": "Pago eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": str(e)}
