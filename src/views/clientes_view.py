import customtkinter as ctk
from tkinter import messagebox
from controllers.cliente_controller import ClienteController


class ClientesView(ctk.CTkFrame):
    """
    Vista transaccional para la gestión de Clientes y Licencias.
    Usa CustomTkinter exclusivamente. No contiene SQL.
    """

    def __init__(self, master):
        super().__init__(master)
        self.controller = ClienteController()

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Formulario (izquierda) ──
        self.frame_form = ctk.CTkFrame(self, width=420)
        self.frame_form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.frame_form.grid_propagate(False)
        self.frame_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_form,
            text="Registro de Cliente",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 25))

        # ID oculto
        self.c_id = ctk.CTkEntry(self.frame_form)
        self.c_id.grid(row=1, column=1, padx=10, pady=2)
        self.c_id.configure(state="disabled")

        campos_persona = [
            ("C.I.:", "c_ci"),
            ("Nombre Completo:", "c_nombre"),
            ("Teléfono:", "c_telefono"),
            ("Dirección:", "c_direccion"),
            ("Email:", "c_email"),
        ]
        row_offset = 2
        for i, (label, attr) in enumerate(campos_persona, start=row_offset):
            ctk.CTkLabel(self.frame_form, text=label).grid(
                row=i, column=0, padx=10, pady=5, sticky="e"
            )
            entry = ctk.CTkEntry(self.frame_form, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            setattr(self, attr, entry)

        # Separador Licencia
        ctk.CTkLabel(
            self.frame_form,
            text="— Datos de Licencia de Conducir —",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray"
        ).grid(row=row_offset + len(campos_persona), column=0, columnspan=2, pady=(15, 10))

        campos_licencia = [
            ("Nro. Licencia:", "c_nro_licencia"),
            ("Categoría:", "c_categoria_licencia"),
            ("Fecha Vencimiento:", "c_fecha_vencimiento"),
        ]
        lic_start = row_offset + len(campos_persona) + 1
        for i, (label, attr) in enumerate(campos_licencia, start=lic_start):
            ctk.CTkLabel(self.frame_form, text=label).grid(
                row=i, column=0, padx=10, pady=5, sticky="e"
            )
            entry = ctk.CTkEntry(self.frame_form, width=250)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            setattr(self, attr, entry)

        self.c_fecha_vencimiento.configure(placeholder_text="YYYY-MM-DD")

        # Botones
        btn_frame = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        btn_frame.grid(row=lic_start + len(campos_licencia), column=0, columnspan=2, pady=(25, 15))

        ctk.CTkButton(
            btn_frame, text="Nuevo", command=self.nuevo_cliente, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Guardar", command=self.guardar_cliente, width=90
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            btn_frame, text="Eliminar", command=self.eliminar_cliente,
            fg_color="#E74C3C", hover_color="#C0392B", width=90
        ).pack(side="left", padx=5)

        self.c_msg = ctk.CTkLabel(
            self.frame_form, text="", text_color="#E74C3C", wraplength=380
        )
        self.c_msg.grid(row=lic_start + len(campos_licencia) + 1, column=0, columnspan=2, pady=5)

        # ── Tabla (derecha) ──
        self.frame_table = ctk.CTkFrame(self)
        self.frame_table.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.frame_table.grid_columnconfigure(0, weight=1)
        self.frame_table.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_table,
            text="Listado de Clientes",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

        headers = ["ID", "C.I.", "Nombre", "Teléfono", "Email", "Licencia", "Vence", ""]
        widths = [40, 70, 130, 80, 130, 80, 85, 50]
        self.hdr = ctk.CTkFrame(self.frame_table, fg_color="transparent")
        self.hdr.grid(row=1, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                self.hdr, text=text, width=w, font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=col, padx=2, sticky="w")

        self.rows_container = ctk.CTkScrollableFrame(self.frame_table)
        self.rows_container.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.rows_container.grid_columnconfigure(0, weight=1)

        self.cargar_clientes()

    # ═══════════════════════════════════════════════════════════════
    #  CARGA DE DATOS
    # ═══════════════════════════════════════════════════════════════

    def cargar_clientes(self):
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        resultado = self.controller.listar_clientes()
        if not resultado["success"]:
            self.c_msg.configure(text=resultado.get("message", "Error al cargar clientes"))
            return

        data = resultado["data"]
        if not data:
            ctk.CTkLabel(
                self.rows_container, text="No hay clientes registrados.", text_color="gray"
            ).pack(pady=20)
            return

        widths = [40, 70, 130, 80, 130, 80, 85, 50]
        for item in data:
            row = ctk.CTkFrame(self.rows_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vals = [
                str(item["id_persona"]),
                item["ci"],
                item["nombre_completo"],
                item["telefono"],
                item["email"],
                item["nro_licencia"] if item["nro_licencia"] else "—",
                str(item["fecha_vencimiento"]) if item["fecha_vencimiento"] else "—",
            ]
            for col, (text, w) in enumerate(zip(vals, widths[:-1])):
                ctk.CTkLabel(row, text=text, width=w).grid(
                    row=0, column=col, padx=2, sticky="w"
                )
            ctk.CTkButton(
                row, text="Sel", width=45, font=ctk.CTkFont(size=11),
                command=lambda c=item: self.seleccionar_cliente(c)
            ).grid(row=0, column=len(vals), padx=2, sticky="w")

    def seleccionar_cliente(self, item):
        self._set_entry(self.c_id, str(item["id_persona"]), disabled=True)
        self._set_entry(self.c_ci, item["ci"])
        self._set_entry(self.c_nombre, item["nombre_completo"])
        self._set_entry(self.c_telefono, item["telefono"])
        self._set_entry(self.c_direccion, item["direccion"] if item["direccion"] else "")
        self._set_entry(self.c_email, item["email"])
        self._set_entry(self.c_nro_licencia, item["nro_licencia"] if item["nro_licencia"] else "")
        self._set_entry(self.c_categoria_licencia, item["categoria_licencia"] if item["categoria_licencia"] else "")
        self._set_entry(self.c_fecha_vencimiento, str(item["fecha_vencimiento"]) if item["fecha_vencimiento"] else "")
        self.c_msg.configure(text="")

    def nuevo_cliente(self):
        self._set_entry(self.c_id, "", disabled=True)
        self.c_ci.delete(0, "end")
        self.c_nombre.delete(0, "end")
        self.c_telefono.delete(0, "end")
        self.c_direccion.delete(0, "end")
        self.c_email.delete(0, "end")
        self.c_nro_licencia.delete(0, "end")
        self.c_categoria_licencia.delete(0, "end")
        self.c_fecha_vencimiento.delete(0, "end")
        self.c_msg.configure(text="")

    def guardar_cliente(self):
        datos = {
            "id_persona": self.c_id.get() if self.c_id.get() else None,
            "ci": self.c_ci.get(),
            "nombre_completo": self.c_nombre.get(),
            "telefono": self.c_telefono.get(),
            "direccion": self.c_direccion.get(),
            "email": self.c_email.get(),
            "nro_licencia": self.c_nro_licencia.get(),
            "categoria_licencia": self.c_categoria_licencia.get(),
            "fecha_vencimiento": self.c_fecha_vencimiento.get(),
        }
        resultado = self.controller.guardar_cliente(datos)
        if resultado["success"]:
            self.c_msg.configure(text=resultado["message"], text_color="#27AE60")
            self.nuevo_cliente()
            self.cargar_clientes()
        else:
            self.c_msg.configure(text=resultado["message"], text_color="#E74C3C")

    def eliminar_cliente(self):
        cid = self.c_id.get()
        if not cid:
            self.c_msg.configure(text="Seleccione un cliente para eliminar.", text_color="#E74C3C")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar el cliente seleccionado y sus datos asociados?"):
            resultado = self.controller.eliminar_cliente(cid)
            if resultado["success"]:
                self.c_msg.configure(text=resultado["message"], text_color="#27AE60")
                self.nuevo_cliente()
                self.cargar_clientes()
            else:
                self.c_msg.configure(text=resultado["message"], text_color="#E74C3C")

    @staticmethod
    def _set_entry(entry, value, disabled=False):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        if disabled:
            entry.configure(state="disabled")
