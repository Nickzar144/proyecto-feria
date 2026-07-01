import customtkinter as ctk
from tkinter import messagebox
from controllers.flota_controller import FlotaController


class FlotaView(ctk.CTkFrame):
    """
    Vista transaccional para la gestión de vehículos y mantenimiento.
    Utiliza CustomTkinter exclusivamente. No contiene SQL.
    """

    def __init__(self, master):
        super().__init__(master)
        self.controller = FlotaController()

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ── Pestaña Vehículos ──
        self.tab_vehiculos = self.tabview.add("Gestión de Vehículos")
        self.tab_vehiculos.grid_columnconfigure(1, weight=1)
        self.tab_vehiculos.grid_rowconfigure(0, weight=1)

        self._build_vehiculos_form()
        self._build_vehiculos_table()

        # ── Pestaña Mantenimiento ──
        self.tab_mantenimiento = self.tabview.add("Control de Taller")
        self.tab_mantenimiento.grid_columnconfigure(1, weight=1)
        self.tab_mantenimiento.grid_rowconfigure(0, weight=1)

        self._build_mantenimiento_form()
        self._build_mantenimiento_table()

        self.cargar_listas_iniciales()
        self.cargar_vehiculos()
        self.cargar_mantenimientos()

    # ═══════════════════════════════════════════════════════════════
    #  VEHÍCULOS
    # ═══════════════════════════════════════════════════════════════

    def _build_vehiculos_form(self):
        self.frame_v_form = ctk.CTkFrame(self.tab_vehiculos, width=380)
        self.frame_v_form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.frame_v_form.grid_propagate(False)
        self.frame_v_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_v_form,
            text="Datos del Vehículo",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 20))

        # ID oculto
        self.v_id = ctk.CTkEntry(self.frame_v_form)
        self.v_id.grid(row=1, column=1, padx=10, pady=2)
        self.v_id.configure(state="disabled")

        campos = [
            ("Placa:", "v_placa"),
            ("Marca:", "v_marca"),
            ("Modelo:", "v_modelo"),
            ("Año:", "v_anio"),
            ("Color:", "v_color"),
            ("Kilometraje:", "v_kilometraje"),
        ]
        for i, (label, attr) in enumerate(campos, start=2):
            ctk.CTkLabel(self.frame_v_form, text=label).grid(
                row=i, column=0, padx=10, pady=5, sticky="e"
            )
            entry = ctk.CTkEntry(self.frame_v_form, width=220)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            setattr(self, attr, entry)

        # Estado
        ctk.CTkLabel(self.frame_v_form, text="Estado:").grid(
            row=8, column=0, padx=10, pady=5, sticky="e"
        )
        self.v_estado = ctk.CTkOptionMenu(
            self.frame_v_form,
            values=["DISPONIBLE", "ALQUILADO", "MANTENIMIENTO", "INACTIVO"],
            width=220
        )
        self.v_estado.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.v_estado.set("DISPONIBLE")

        # Categoría
        ctk.CTkLabel(self.frame_v_form, text="Categoría:").grid(
            row=9, column=0, padx=10, pady=5, sticky="e"
        )
        self.v_categoria = ctk.CTkOptionMenu(
            self.frame_v_form,
            values=["Cargando..."],
            width=220
        )
        self.v_categoria.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # Botones
        btn_frame = ctk.CTkFrame(self.frame_v_form, fg_color="transparent")
        btn_frame.grid(row=10, column=0, columnspan=2, pady=(25, 15))

        ctk.CTkButton(
            btn_frame, text="Nuevo", command=self.nuevo_vehiculo, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Guardar", command=self.guardar_vehiculo, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Eliminar", command=self.eliminar_vehiculo,
            fg_color="#E74C3C", hover_color="#C0392B", width=90
        ).pack(side="left", padx=5)

        self.v_msg = ctk.CTkLabel(
            self.frame_v_form, text="", text_color="#E74C3C", wraplength=340
        )
        self.v_msg.grid(row=11, column=0, columnspan=2, pady=5)

    def _build_vehiculos_table(self):
        self.frame_v_table = ctk.CTkFrame(self.tab_vehiculos)
        self.frame_v_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.frame_v_table.grid_columnconfigure(0, weight=1)
        self.frame_v_table.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.frame_v_table,
            text="Listado de Vehículos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        # Encabezados
        headers = ["ID", "Placa", "Marca", "Modelo", "Año", "Estado", "Categoría", ""]
        widths = [50, 80, 90, 90, 55, 90, 100, 60]
        self.hdr_v = ctk.CTkFrame(self.frame_v_table, fg_color="transparent")
        self.hdr_v.grid(row=1, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                self.hdr_v, text=text, width=w, font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=2, sticky="w")

        # Área scrollable de filas
        self.rows_v_container = ctk.CTkScrollableFrame(self.frame_v_table)
        self.rows_v_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.rows_v_container.grid_columnconfigure(0, weight=1)

    def cargar_vehiculos(self):
        for widget in self.rows_v_container.winfo_children():
            widget.destroy()

        resultado = self.controller.listar_vehiculos()
        if not resultado["success"]:
            self.v_msg.configure(text=resultado.get("message", "Error al cargar vehículos"))
            return

        data = resultado["data"]
        if not data:
            ctk.CTkLabel(
                self.rows_v_container, text="No hay vehículos registrados.", text_color="gray"
            ).pack(pady=20)
            return

        widths = [50, 80, 90, 90, 55, 90, 100, 60]
        for item in data:
            row = ctk.CTkFrame(self.rows_v_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vals = [
                str(item["id_vehiculo"]),
                item["placa"],
                item["marca"],
                item["modelo"],
                str(item["anio"]),
                item["estado"],
                item["nombre_categoria"],
            ]
            for col, (text, w) in enumerate(zip(vals, widths[:-1])):
                ctk.CTkLabel(row, text=text, width=w).grid(
                    row=0, column=col, padx=2, sticky="w"
                )
            ctk.CTkButton(
                row, text="Sel", width=50, font=ctk.CTkFont(size=11),
                command=lambda v=item: self.seleccionar_vehiculo(v)
            ).grid(row=0, column=len(vals), padx=2, sticky="w")

    def seleccionar_vehiculo(self, item):
        self._set_entry(self.v_id, str(item["id_vehiculo"]), disabled=True)
        self._set_entry(self.v_placa, item["placa"])
        self._set_entry(self.v_marca, item["marca"])
        self._set_entry(self.v_modelo, item["modelo"])
        self._set_entry(self.v_anio, str(item["anio"]))
        self._set_entry(self.v_color, item["color"] if item["color"] else "")
        self._set_entry(self.v_kilometraje, str(item["kilometraje"]))
        self.v_estado.set(item["estado"])
        self.v_categoria.set(item["nombre_categoria"])
        self.v_msg.configure(text="")

    def nuevo_vehiculo(self):
        self._set_entry(self.v_id, "", disabled=True)
        self.v_placa.delete(0, "end")
        self.v_marca.delete(0, "end")
        self.v_modelo.delete(0, "end")
        self.v_anio.delete(0, "end")
        self.v_color.delete(0, "end")
        self.v_kilometraje.delete(0, "end")
        self.v_estado.set("DISPONIBLE")
        if self.categorias_list:
            self.v_categoria.set(self.categorias_list[0])
        self.v_msg.configure(text="")

    def guardar_vehiculo(self):
        datos = {
            "id_vehiculo": self.v_id.get() if self.v_id.get() else None,
            "placa": self.v_placa.get(),
            "marca": self.v_marca.get(),
            "modelo": self.v_modelo.get(),
            "anio": self.v_anio.get(),
            "color": self.v_color.get(),
            "kilometraje": self.v_kilometraje.get(),
            "estado": self.v_estado.get(),
            "id_categoria": self.categorias_map.get(self.v_categoria.get()),
        }
        resultado = self.controller.guardar_vehiculo(datos)
        if resultado["success"]:
            self.v_msg.configure(text=resultado["message"], text_color="#27AE60")
            self.nuevo_vehiculo()
            self.cargar_vehiculos()
            self.cargar_vehiculos_en_mantenimiento()
        else:
            self.v_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def eliminar_vehiculo(self):
        vid = self.v_id.get()
        if not vid:
            self.v_msg.configure(text="Seleccione un vehículo para eliminar.", text_color="#E74C3C")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el vehículo seleccionado?"):
            resultado = self.controller.eliminar_vehiculo(vid)
            if resultado["success"]:
                self.v_msg.configure(text=resultado["message"], text_color="#27AE60")
                self.nuevo_vehiculo()
                self.cargar_vehiculos()
                self.cargar_vehiculos_en_mantenimiento()
            else:
                self.v_msg.configure(text=resultado["message"], text_color="#E74C3C")

    # ═══════════════════════════════════════════════════════════════
    #  MANTENIMIENTO
    # ═══════════════════════════════════════════════════════════════

    def _build_mantenimiento_form(self):
        self.frame_m_form = ctk.CTkFrame(self.tab_mantenimiento, width=380)
        self.frame_m_form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.frame_m_form.grid_propagate(False)
        self.frame_m_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_m_form,
            text="Registro de Mantenimiento",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(15, 20))

        self.m_id = ctk.CTkEntry(self.frame_m_form)
        self.m_id.grid(row=1, column=1, padx=10, pady=2)
        self.m_id.configure(state="disabled")

        # Vehículo
        ctk.CTkLabel(self.frame_m_form, text="Vehículo:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.m_vehiculo = ctk.CTkOptionMenu(
            self.frame_m_form, values=["Cargando..."], width=220
        )
        self.m_vehiculo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        campos = [
            ("Tipo:", "m_tipo"),
            ("Descripción:", "m_descripcion"),
            ("Fecha Inicio:", "m_fecha_inicio"),
            ("Fecha Fin:", "m_fecha_fin"),
            ("Costo (Bs):", "m_costo"),
        ]
        for i, (label, attr) in enumerate(campos, start=3):
            ctk.CTkLabel(self.frame_m_form, text=label).grid(
                row=i, column=0, padx=10, pady=5, sticky="e"
            )
            entry = ctk.CTkEntry(self.frame_m_form, width=220)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            setattr(self, attr, entry)

        self.m_fecha_inicio.configure(placeholder_text="YYYY-MM-DD")
        self.m_fecha_fin.configure(placeholder_text="YYYY-MM-DD (opcional)")

        btn_frame = ctk.CTkFrame(self.frame_m_form, fg_color="transparent")
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(25, 15))

        ctk.CTkButton(
            btn_frame, text="Nuevo", command=self.nuevo_mantenimiento, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Guardar", command=self.guardar_mantenimiento, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Eliminar", command=self.eliminar_mantenimiento,
            fg_color="#E74C3C", hover_color="#C0392B", width=90
        ).pack(side="left", padx=5)

        self.m_msg = ctk.CTkLabel(
            self.frame_m_form, text="", text_color="#E74C3C", wraplength=340
        )
        self.m_msg.grid(row=9, column=0, columnspan=2, pady=5)

    def _build_mantenimiento_table(self):
        self.frame_m_table = ctk.CTkFrame(self.tab_mantenimiento)
        self.frame_m_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.frame_m_table.grid_columnconfigure(0, weight=1)
        self.frame_m_table.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.frame_m_table,
            text="Historial de Mantenimiento",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        headers = ["ID", "Vehículo", "Tipo", "Inicio", "Fin", "Costo", ""]
        widths = [45, 110, 90, 85, 85, 70, 55]
        self.hdr_m = ctk.CTkFrame(self.frame_m_table, fg_color="transparent")
        self.hdr_m.grid(row=1, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                self.hdr_m, text=text, width=w, font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=2, sticky="w")

        self.rows_m_container = ctk.CTkScrollableFrame(self.frame_m_table)
        self.rows_m_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.rows_m_container.grid_columnconfigure(0, weight=1)

    def cargar_mantenimientos(self):
        for widget in self.rows_m_container.winfo_children():
            widget.destroy()

        resultado = self.controller.listar_mantenimientos()
        if not resultado["success"]:
            self.m_msg.configure(text=resultado.get("message", "Error al cargar mantenimientos"))
            return

        data = resultado["data"]
        if not data:
            ctk.CTkLabel(
                self.rows_m_container, text="No hay registros de mantenimiento.", text_color="gray"
            ).pack(pady=20)
            return

        widths = [45, 110, 90, 85, 85, 70, 55]
        for item in data:
            row = ctk.CTkFrame(self.rows_m_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vehiculo_str = f"{item['placa']}"
            vals = [
                str(item["id_mantenimiento"]),
                vehiculo_str,
                item["tipo"],
                str(item["fecha_inicio"]),
                str(item["fecha_fin"]) if item["fecha_fin"] else "—",
                f"{item['costo']:.2f}",
            ]
            for col, (text, w) in enumerate(zip(vals, widths[:-1])):
                ctk.CTkLabel(row, text=text, width=w).grid(
                    row=0, column=col, padx=2, sticky="w"
                )
            ctk.CTkButton(
                row, text="Sel", width=45, font=ctk.CTkFont(size=11),
                command=lambda m=item: self.seleccionar_mantenimiento(m)
            ).grid(row=0, column=len(vals), padx=2, sticky="w")

    def seleccionar_mantenimiento(self, item):
        self._set_entry(self.m_id, str(item["id_mantenimiento"]), disabled=True)
        display = f"{item['placa']} - {item['marca']} {item['modelo']}"
        if display in self.vehiculos_map:
            self.m_vehiculo.set(display)
        self._set_entry(self.m_tipo, item["tipo"])
        self._set_entry(self.m_descripcion, item["descripcion"] if item["descripcion"] else "")
        self._set_entry(self.m_fecha_inicio, str(item["fecha_inicio"]))
        self._set_entry(self.m_fecha_fin, str(item["fecha_fin"]) if item["fecha_fin"] else "")
        self._set_entry(self.m_costo, str(item["costo"]))
        self.m_msg.configure(text="")

    def nuevo_mantenimiento(self):
        self._set_entry(self.m_id, "", disabled=True)
        if self.vehiculos_list:
            self.m_vehiculo.set(self.vehiculos_list[0])
        self.m_tipo.delete(0, "end")
        self.m_descripcion.delete(0, "end")
        self.m_fecha_inicio.delete(0, "end")
        self.m_fecha_fin.delete(0, "end")
        self.m_costo.delete(0, "end")
        self.m_msg.configure(text="")

    def guardar_mantenimiento(self):
        display = self.m_vehiculo.get()
        datos = {
            "id_mantenimiento": self.m_id.get() if self.m_id.get() else None,
            "id_vehiculo": self.vehiculos_map.get(display),
            "tipo": self.m_tipo.get(),
            "descripcion": self.m_descripcion.get(),
            "fecha_inicio": self.m_fecha_inicio.get() or None,
            "fecha_fin": self.m_fecha_fin.get() or None,
            "costo": self.m_costo.get(),
        }
        resultado = self.controller.guardar_mantenimiento(datos)
        if resultado["success"]:
            self.m_msg.configure(text=resultado["message"], text_color="#27AE60")
            self.nuevo_mantenimiento()
            self.cargar_mantenimientos()
        else:
            self.m_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def eliminar_mantenimiento(self):
        mid = self.m_id.get()
        if not mid:
            self.m_msg.configure(text="Seleccione un mantenimiento para eliminar.", text_color="#E74C3C")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el registro de mantenimiento seleccionado?"):
            resultado = self.controller.eliminar_mantenimiento(mid)
            if resultado["success"]:
                self.m_msg.configure(text=resultado["message"], text_color="#27AE60")
                self.nuevo_mantenimiento()
                self.cargar_mantenimientos()
            else:
                self.m_msg.configure(text=resultado["message"], text_color="#E74C3C")

    # ═══════════════════════════════════════════════════════════════
    #  UTILIDADES Y CARGA INICIAL
    # ═══════════════════════════════════════════════════════════════

    def cargar_listas_iniciales(self):
        # Categorías
        self.categorias_map = {}
        self.categorias_list = []
        res = self.controller.listar_categorias()
        if res["success"] and res["data"]:
            for cat in res["data"]:
                self.categorias_list.append(cat["nombre_categoria"])
                self.categorias_map[cat["nombre_categoria"]] = cat["id_categoria"]
            self.v_categoria.configure(values=self.categorias_list)
            self.v_categoria.set(self.categorias_list[0])
        else:
            self.v_categoria.configure(values=["Sin categorías"])

        # Vehículos para mantenimiento
        self.cargar_vehiculos_en_mantenimiento()

    def cargar_vehiculos_en_mantenimiento(self):
        self.vehiculos_map = {}
        self.vehiculos_list = []
        res = self.controller.listar_vehiculos()
        if res["success"] and res["data"]:
            for v in res["data"]:
                display = f"{v['placa']} - {v['marca']} {v['modelo']}"
                self.vehiculos_list.append(display)
                self.vehiculos_map[display] = v["id_vehiculo"]
            self.m_vehiculo.configure(values=self.vehiculos_list)
            self.m_vehiculo.set(self.vehiculos_list[0])
        else:
            self.m_vehiculo.configure(values=["Sin vehículos"])

    @staticmethod
    def _set_entry(entry, value, disabled=False):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        if disabled:
            entry.configure(state="disabled")
