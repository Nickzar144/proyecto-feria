import customtkinter as ctk
from tkinter import messagebox
from controllers.reserva_controller import ReservaController


class ReservasView(ctk.CTkFrame):
    """
    Vista transaccional para Reservas y Control de Pagos.
    Usa CustomTkinter exclusivamente. No contiene SQL.
    """

    def __init__(self, master):
        super().__init__(master)
        self.controller = ReservaController()

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ── Pestaña Reservas ──
        self.tab_reservas = self.tabview.add("Reservas de Alquiler")
        self.tab_reservas.grid_columnconfigure(1, weight=1)
        self.tab_reservas.grid_rowconfigure(0, weight=1)

        self._build_reserva_form()
        self._build_reserva_table()

        # ── Pestaña Pagos ──
        self.tab_pagos = self.tabview.add("Control de Pagos")
        self.tab_pagos.grid_columnconfigure(1, weight=1)
        self.tab_pagos.grid_rowconfigure(0, weight=1)

        self._build_pago_form()
        self._build_pago_table()

        self.cargar_listas_iniciales()
        self.cargar_reservas()
        self.cargar_pagos()

    # ═══════════════════════════════════════════════════════════════
    #  RESERVAS — FORMULARIO
    # ═══════════════════════════════════════════════════════════════

    def _build_reserva_form(self):
        self.frame_r_form = ctk.CTkFrame(self.tab_reservas, width=400)
        self.frame_r_form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.frame_r_form.grid_propagate(False)
        self.frame_r_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_r_form,
            text="Contrato de Alquiler",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 20))

        self.r_nro = ctk.CTkEntry(self.frame_r_form)
        self.r_nro.grid(row=1, column=1, padx=10, pady=2)
        self.r_nro.configure(state="disabled")

        # Cliente
        ctk.CTkLabel(self.frame_r_form, text="Cliente:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.r_cliente = ctk.CTkOptionMenu(self.frame_r_form, values=["Cargando..."], width=240)
        self.r_cliente.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Usuario
        ctk.CTkLabel(self.frame_r_form, text="Usuario:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.r_usuario = ctk.CTkOptionMenu(self.frame_r_form, values=["Cargando..."], width=240)
        self.r_usuario.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Ámbito
        ctk.CTkLabel(self.frame_r_form, text="Ámbito:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.r_ambito = ctk.CTkOptionMenu(self.frame_r_form, values=["Cargando..."], width=240)
        self.r_ambito.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        campos = [
            ("Fecha Inicio:", "r_fecha_inicio", "YYYY-MM-DD"),
            ("Fecha Final:", "r_fecha_final", "YYYY-MM-DD"),
            ("Precio Total (Bs):", "r_precio_total", "Calcule o ingrese"),
            ("Litros Gas. Salida:", "r_litros_salida", ""),
            ("Km Salida:", "r_km_salida", ""),
            ("Litros Gas. Retorno:", "r_litros_retorno", ""),
            ("Km Retorno:", "r_km_retorno", ""),
        ]
        for i, (label, attr, placeholder) in enumerate(campos, start=5):
            ctk.CTkLabel(self.frame_r_form, text=label).grid(row=i, column=0, padx=10, pady=4, sticky="e")
            entry = ctk.CTkEntry(self.frame_r_form, width=240)
            entry.grid(row=i, column=1, padx=10, pady=4, sticky="w")
            if placeholder:
                entry.configure(placeholder_text=placeholder)
            setattr(self, attr, entry)

        # Estado
        ctk.CTkLabel(self.frame_r_form, text="Estado:").grid(row=12, column=0, padx=10, pady=5, sticky="e")
        self.r_estado = ctk.CTkOptionMenu(
            self.frame_r_form,
            values=["PENDIENTE", "ACTIVA", "COMPLETADA", "CANCELADA"],
            width=240
        )
        self.r_estado.grid(row=12, column=1, padx=10, pady=5, sticky="w")
        self.r_estado.set("PENDIENTE")

        # Vehículo
        ctk.CTkLabel(self.frame_r_form, text="Vehículo:").grid(row=13, column=0, padx=10, pady=5, sticky="e")
        self.r_vehiculo = ctk.CTkOptionMenu(self.frame_r_form, values=["Cargando..."], width=240)
        self.r_vehiculo.grid(row=13, column=1, padx=10, pady=5, sticky="w")

        # Botones
        btn_frame = ctk.CTkFrame(self.frame_r_form, fg_color="transparent")
        btn_frame.grid(row=14, column=0, columnspan=2, pady=(15, 10))

        ctk.CTkButton(btn_frame, text="Nuevo", command=self.nueva_reserva, width=80).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="Calcular", command=self.calcular_precio_ui, width=80).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="Guardar", command=self.guardar_reserva, width=80).pack(side="left", padx=4)
        ctk.CTkButton(
            btn_frame, text="Eliminar", command=self.eliminar_reserva,
            fg_color="#E74C3C", hover_color="#C0392B", width=80
        ).pack(side="left", padx=4)

        self.r_msg = ctk.CTkLabel(self.frame_r_form, text="", text_color="#E74C3C", wraplength=360)
        self.r_msg.grid(row=15, column=0, columnspan=2, pady=5)

    def _build_reserva_table(self):
        self.frame_r_table = ctk.CTkFrame(self.tab_reservas)
        self.frame_r_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.frame_r_table.grid_columnconfigure(0, weight=1)
        self.frame_r_table.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_r_table, text="Listado de Reservas",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        headers = ["Nro", "Cliente", "Usuario", "Inicio", "Final", "Precio", "Estado", ""]
        widths = [45, 100, 90, 85, 85, 75, 80, 50]
        hdr = ctk.CTkFrame(self.frame_r_table, fg_color="transparent")
        hdr.grid(row=1, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(hdr, text=text, width=w, font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=2, sticky="w")

        self.rows_r_container = ctk.CTkScrollableFrame(self.frame_r_table)
        self.rows_r_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.rows_r_container.grid_columnconfigure(0, weight=1)

    # ═══════════════════════════════════════════════════════════════
    #  PAGOS — FORMULARIO
    # ═══════════════════════════════════════════════════════════════

    def _build_pago_form(self):
        self.frame_p_form = ctk.CTkFrame(self.tab_pagos, width=400)
        self.frame_p_form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.frame_p_form.grid_propagate(False)
        self.frame_p_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_p_form,
            text="Registro de Pago",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 20))

        self.p_id = ctk.CTkEntry(self.frame_p_form)
        self.p_id.grid(row=1, column=1, padx=10, pady=2)
        self.p_id.configure(state="disabled")

        # Reserva
        ctk.CTkLabel(self.frame_p_form, text="Reserva Nro:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.p_reserva = ctk.CTkOptionMenu(self.frame_p_form, values=["Cargando..."], width=240)
        self.p_reserva.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        campos = [
            ("Monto Pagado (Bs):", "p_monto", ""),
            ("Fecha Pago:", "p_fecha", "YYYY-MM-DD"),
        ]
        for i, (label, attr, placeholder) in enumerate(campos, start=3):
            ctk.CTkLabel(self.frame_p_form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.frame_p_form, width=240)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            if placeholder:
                entry.configure(placeholder_text=placeholder)
            setattr(self, attr, entry)

        # Método
        ctk.CTkLabel(self.frame_p_form, text="Método:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.p_metodo = ctk.CTkOptionMenu(
            self.frame_p_form,
            values=["EFECTIVO", "TRANSFERENCIA", "TARJETA_DEBITO", "TARJETA_CREDITO", "OTRO"],
            width=240
        )
        self.p_metodo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.p_metodo.set("EFECTIVO")

        btn_frame = ctk.CTkFrame(self.frame_p_form, fg_color="transparent")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(20, 15))

        ctk.CTkButton(btn_frame, text="Nuevo", command=self.nuevo_pago, width=90).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Guardar", command=self.guardar_pago, width=90).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Eliminar", command=self.eliminar_pago,
            fg_color="#E74C3C", hover_color="#C0392B", width=90
        ).pack(side="left", padx=5)

        self.p_msg = ctk.CTkLabel(self.frame_p_form, text="", text_color="#E74C3C", wraplength=360)
        self.p_msg.grid(row=7, column=0, columnspan=2, pady=5)

    def _build_pago_table(self):
        self.frame_p_table = ctk.CTkFrame(self.tab_pagos)
        self.frame_p_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.frame_p_table.grid_columnconfigure(0, weight=1)
        self.frame_p_table.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_p_table, text="Historial de Pagos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        headers = ["ID", "Reserva", "Monto", "Fecha", "Método", ""]
        widths = [45, 70, 80, 90, 100, 50]
        hdr = ctk.CTkFrame(self.frame_p_table, fg_color="transparent")
        hdr.grid(row=1, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(hdr, text=text, width=w, font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=2, sticky="w")

        self.rows_p_container = ctk.CTkScrollableFrame(self.frame_p_table)
        self.rows_p_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.rows_p_container.grid_columnconfigure(0, weight=1)

    # ═══════════════════════════════════════════════════════════════
    #  CARGA DE DATOS Y ACCIONES — RESERVAS
    # ═══════════════════════════════════════════════════════════════

    def cargar_reservas(self):
        for widget in self.rows_r_container.winfo_children():
            widget.destroy()

        resultado = self.controller.listar_reservas()
        if not resultado["success"]:
            self.r_msg.configure(text=resultado.get("message", "Error al cargar reservas"))
            return

        data = resultado["data"]
        if not data:
            ctk.CTkLabel(self.rows_r_container, text="No hay reservas registradas.", text_color="gray").pack(pady=20)
            return

        self.reservas_list = []
        self.reservas_map = {}
        widths = [45, 100, 90, 85, 85, 75, 80, 50]
        for item in data:
            row = ctk.CTkFrame(self.rows_r_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vals = [
                str(item["nro_reserva"]),
                item["cliente_nombre"],
                item["usuario_nombre"],
                str(item["fecha_inicio"]),
                str(item["fecha_final"]),
                f"{item['precio_total']:.2f}",
                item["estado"],
            ]
            for col, (text, w) in enumerate(zip(vals, widths[:-1])):
                ctk.CTkLabel(row, text=text, width=w).grid(row=0, column=col, padx=2, sticky="w")
            ctk.CTkButton(
                row, text="Sel", width=45, font=ctk.CTkFont(size=11),
                command=lambda r=item: self.seleccionar_reserva(r)
            ).grid(row=0, column=len(vals), padx=2, sticky="w")

            # Guardar mapeo para dropdown de pagos
            display = f"#{item['nro_reserva']} — {item['cliente_nombre']}"
            self.reservas_list.append(display)
            self.reservas_map[display] = item["nro_reserva"]

        # Actualizar dropdown de pagos
        if self.reservas_list:
            self.p_reserva.configure(values=self.reservas_list)
            self.p_reserva.set(self.reservas_list[0])
        else:
            self.p_reserva.configure(values=["Sin reservas"])

    def seleccionar_reserva(self, item):
        self._set_entry(self.r_nro, str(item["nro_reserva"]), disabled=True)
        # Cliente
        cliente_disp = f"{item['id_cliente']} - {item['cliente_nombre']}"
        if cliente_disp in self.clientes_map:
            self.r_cliente.set(cliente_disp)
        # Usuario
        usuario_disp = f"{item['id_usuario']} - {item['usuario_nombre']}"
        if usuario_disp in self.usuarios_map:
            self.r_usuario.set(usuario_disp)
        # Ámbito
        ambito_disp = f"{item['id_ambito']} - {item['ambito_descripcion']}"
        if ambito_disp in self.ambitos_map:
            self.r_ambito.set(ambito_disp)
        # Vehículo (recargar incluyendo el actual)
        self.cargar_vehiculos(excluir_id=item["id_vehiculo"])
        veh_disp = f"{item['id_vehiculo']} - {item['placa']}"
        if veh_disp in self.vehiculos_map:
            self.r_vehiculo.set(veh_disp)

        self._set_entry(self.r_fecha_inicio, str(item["fecha_inicio"]))
        self._set_entry(self.r_fecha_final, str(item["fecha_final"]))
        self._set_entry(self.r_precio_total, str(item["precio_total"]))
        self.r_estado.set(item["estado"])
        self._set_entry(self.r_litros_salida, str(item["litros_gasolina_salida"] if item["litros_gasolina_salida"] else 0))
        self._set_entry(self.r_km_salida, str(item["kilometraje_salida"] if item["kilometraje_salida"] else 0))
        self._set_entry(self.r_litros_retorno, str(item["litros_gasolina_retorno"] if item["litros_gasolina_retorno"] else 0))
        self._set_entry(self.r_km_retorno, str(item["kilometraje_retorno"] if item["kilometraje_retorno"] else 0))
        self.r_msg.configure(text="")

    def nueva_reserva(self):
        self._set_entry(self.r_nro, "", disabled=True)
        if self.clientes_list:
            self.r_cliente.set(self.clientes_list[0])
        if self.usuarios_list:
            self.r_usuario.set(self.usuarios_list[0])
        if self.ambitos_list:
            self.r_ambito.set(self.ambitos_list[0])
        self.r_fecha_inicio.delete(0, "end")
        self.r_fecha_final.delete(0, "end")
        self._set_entry(self.r_precio_total, "")
        self.r_estado.set("PENDIENTE")
        self.cargar_vehiculos()
        self.r_litros_salida.delete(0, "end")
        self.r_km_salida.delete(0, "end")
        self.r_litros_retorno.delete(0, "end")
        self.r_km_retorno.delete(0, "end")
        self.r_msg.configure(text="")

    def calcular_precio_ui(self):
        datos = self._gather_reserva_data()
        if not datos["fecha_inicio"] or not datos["fecha_final"]:
            self.r_msg.configure(text="Ingrese fechas de inicio y final.", text_color="#E74C3C")
            return
        if not datos["id_vehiculo"]:
            self.r_msg.configure(text="Seleccione un vehículo.", text_color="#E74C3C")
            return
        if not datos["id_ambito"]:
            self.r_msg.configure(text="Seleccione un ámbito.", text_color="#E74C3C")
            return
        resultado = self.controller.calcular_precio(datos["fecha_inicio"], datos["fecha_final"], datos["id_vehiculo"], datos["id_ambito"])
        if resultado["success"]:
            self._set_entry(self.r_precio_total, str(resultado["precio_total"]))
            det = resultado["detalle"]
            msg = (f"Precio calculado: {resultado['precio_total']} Bs  |  "
                   f"{resultado['dias']} días  |  Tarifa: {det['tarifa_diaria']} + Seguro: {det['costo_seguro_dia']}  |  "
                   f"Ámbito: +{det['costo_adicional_ambito']}")
            self.r_msg.configure(text=msg, text_color="#27AE60")
        else:
            self.r_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def guardar_reserva(self):
        datos = self._gather_reserva_data()
        resultado = self.controller.guardar_reserva(datos)
        if resultado["success"]:
            self.r_msg.configure(text=resultado["message"], text_color="#27AE60")
            self.nueva_reserva()
            self.cargar_reservas()
            self.cargar_pagos()
        else:
            self.r_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def eliminar_reserva(self):
        nro = self.r_nro.get()
        if not nro:
            self.r_msg.configure(text="Seleccione una reserva para eliminar.", text_color="#E74C3C")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar la reserva seleccionada? Se liberará el vehículo y se borrarán los pagos asociados."):
            resultado = self.controller.eliminar_reserva(nro)
            if resultado["success"]:
                self.r_msg.configure(text=resultado["message"], text_color="#27AE60")
                self.nueva_reserva()
                self.cargar_reservas()
                self.cargar_pagos()
            else:
                self.r_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def _gather_reserva_data(self):
        return {
            "nro_reserva": self.r_nro.get() if self.r_nro.get() else None,
            "id_cliente": self.clientes_map.get(self.r_cliente.get()),
            "id_usuario": self.usuarios_map.get(self.r_usuario.get()),
            "id_ambito": self.ambitos_map.get(self.r_ambito.get()),
            "fecha_inicio": self.r_fecha_inicio.get(),
            "fecha_final": self.r_fecha_final.get(),
            "precio_total": self.r_precio_total.get(),
            "estado": self.r_estado.get(),
            "id_vehiculo": self.vehiculos_map.get(self.r_vehiculo.get()),
            "litros_gasolina_salida": self.r_litros_salida.get(),
            "litros_gasolina_retorno": self.r_litros_retorno.get(),
            "kilometraje_salida": self.r_km_salida.get(),
            "kilometraje_retorno": self.r_km_retorno.get(),
        }

    # ═══════════════════════════════════════════════════════════════
    #  CARGA DE DATOS Y ACCIONES — PAGOS
    # ═══════════════════════════════════════════════════════════════

    def cargar_pagos(self):
        for widget in self.rows_p_container.winfo_children():
            widget.destroy()

        resultado = self.controller.listar_pagos()
        if not resultado["success"]:
            self.p_msg.configure(text=resultado.get("message", "Error al cargar pagos"))
            return

        data = resultado["data"]
        if not data:
            ctk.CTkLabel(self.rows_p_container, text="No hay pagos registrados.", text_color="gray").pack(pady=20)
            return

        widths = [45, 70, 80, 90, 100, 50]
        for item in data:
            row = ctk.CTkFrame(self.rows_p_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vals = [
                str(item["id_pago"]),
                str(item["nro_reserva"]),
                f"{item['monto_pagado']:.2f}",
                str(item["fecha_pagado"]),
                item["metodo_pago"],
            ]
            for col, (text, w) in enumerate(zip(vals, widths[:-1])):
                ctk.CTkLabel(row, text=text, width=w).grid(row=0, column=col, padx=2, sticky="w")
            ctk.CTkButton(
                row, text="Sel", width=45, font=ctk.CTkFont(size=11),
                command=lambda p=item: self.seleccionar_pago(p)
            ).grid(row=0, column=len(vals), padx=2, sticky="w")

    def seleccionar_pago(self, item):
        self._set_entry(self.p_id, str(item["id_pago"]), disabled=True)
        display = f"#{item['nro_reserva']} — {item.get('cliente_nombre', 'Reserva')}"
        # Buscar en mapa actual
        for disp, nro in self.reservas_map.items():
            if nro == item["nro_reserva"]:
                self.p_reserva.set(disp)
                break
        self._set_entry(self.p_monto, str(item["monto_pagado"]))
        self._set_entry(self.p_fecha, str(item["fecha_pagado"]))
        self.p_metodo.set(item["metodo_pago"])
        self.p_msg.configure(text="")

    def nuevo_pago(self):
        self._set_entry(self.p_id, "", disabled=True)
        if self.reservas_list:
            self.p_reserva.set(self.reservas_list[0])
        self.p_monto.delete(0, "end")
        self.p_fecha.delete(0, "end")
        self.p_metodo.set("EFECTIVO")
        self.p_msg.configure(text="")

    def guardar_pago(self):
        datos = {
            "id_pago": self.p_id.get() if self.p_id.get() else None,
            "nro_reserva": self.reservas_map.get(self.p_reserva.get()),
            "monto_pagado": self.p_monto.get(),
            "fecha_pagado": self.p_fecha.get(),
            "metodo_pago": self.p_metodo.get(),
        }
        resultado = self.controller.guardar_pago(datos)
        if resultado["success"]:
            self.p_msg.configure(text=resultado["message"], text_color="#27AE60")
            self.nuevo_pago()
            self.cargar_pagos()
        else:
            self.p_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def eliminar_pago(self):
        pid = self.p_id.get()
        if not pid:
            self.p_msg.configure(text="Seleccione un pago para eliminar.", text_color="#E74C3C")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el pago seleccionado?"):
            resultado = self.controller.eliminar_pago(pid)
            if resultado["success"]:
                self.p_msg.configure(text=resultado["message"], text_color="#27AE60")
                self.nuevo_pago()
                self.cargar_pagos()
            else:
                self.p_msg.configure(text=resultado["message"], text_color="#E74C3C")

    # ═══════════════════════════════════════════════════════════════
    #  UTILIDADES Y CARGA INICIAL
    # ═══════════════════════════════════════════════════════════════

    def cargar_listas_iniciales(self):
        # Clientes
        self.clientes_map = {}
        self.clientes_list = []
        res = self.controller.listar_clientes()
        if res["success"] and res["data"]:
            for c in res["data"]:
                disp = f"{c['id_persona']} - {c['nombre_completo']}"
                self.clientes_list.append(disp)
                self.clientes_map[disp] = c["id_persona"]
            self.r_cliente.configure(values=self.clientes_list)
            self.r_cliente.set(self.clientes_list[0])
        else:
            self.r_cliente.configure(values=["Sin clientes"])

        # Usuarios
        self.usuarios_map = {}
        self.usuarios_list = []
        res = self.controller.listar_usuarios()
        if res["success"] and res["data"]:
            for u in res["data"]:
                disp = f"{u['id_persona']} - {u['nombre_completo']}"
                self.usuarios_list.append(disp)
                self.usuarios_map[disp] = u["id_persona"]
            self.r_usuario.configure(values=self.usuarios_list)
            self.r_usuario.set(self.usuarios_list[0])
        else:
            self.r_usuario.configure(values=["Sin usuarios"])

        # Ámbitos
        self.ambitos_map = {}
        self.ambitos_list = []
        res = self.controller.listar_ambitos()
        if res["success"] and res["data"]:
            for a in res["data"]:
                disp = f"{a['id_ambito']} - {a['descripcion']}"
                self.ambitos_list.append(disp)
                self.ambitos_map[disp] = a["id_ambito"]
            self.r_ambito.configure(values=self.ambitos_list)
            self.r_ambito.set(self.ambitos_list[0])
        else:
            self.r_ambito.configure(values=["Sin ámbitos"])

        self.cargar_vehiculos()

    def cargar_vehiculos(self, excluir_id=None):
        self.vehiculos_map = {}
        self.vehiculos_list = []
        res = self.controller.listar_vehiculos_disponibles(excluir_id=excluir_id)
        if res["success"] and res["data"]:
            for v in res["data"]:
                disp = f"{v['id_vehiculo']} - {v['placa']}"
                self.vehiculos_list.append(disp)
                self.vehiculos_map[disp] = v["id_vehiculo"]
            self.r_vehiculo.configure(values=self.vehiculos_list)
            self.r_vehiculo.set(self.vehiculos_list[0])
        else:
            self.r_vehiculo.configure(values=["Sin vehículos"])

    @staticmethod
    def _set_entry(entry, value, disabled=False):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        if disabled:
            entry.configure(state="disabled")
