import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers.reporte_controller import ReporteController


class ReportesView(ctk.CTkFrame):
    """
    Vista de Dashboard de Reportes y Auditoría.
    Embebe gráficos matplotlib dentro de CustomTkinter.
    """

    def __init__(self, master):
        super().__init__(master)
        self.controller = ReporteController()

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # ── Dashboard Financiero ──
        self.tab_dash = self.tabview.add("Dashboard Financiero")
        self.tab_dash.grid_columnconfigure(0, weight=1)
        self.tab_dash.grid_rowconfigure(1, weight=1)

        self._build_dashboard(self.tab_dash)

        # ── Logs de Auditoría ──
        self.tab_audit = self.tabview.add("Logs de Auditoría")
        self.tab_audit.grid_columnconfigure(0, weight=1)
        self.tab_audit.grid_rowconfigure(1, weight=1)

        self._build_auditoria(self.tab_audit)

        self.cargar_dashboard()
        self.cargar_auditoria()

    # ═══════════════════════════════════════════════════════════════
    #  DASHBOARD
    # ═══════════════════════════════════════════════════════════════

    def _build_dashboard(self, parent):
        # KPIs
        self.kpi_frame = ctk.CTkFrame(parent, height=100)
        self.kpi_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.kpi_frame.grid_propagate(False)
        for i in range(4):
            self.kpi_frame.grid_columnconfigure(i, weight=1)

        self.kpi_ingresos = self._create_kpi_card(self.kpi_frame, "Ingresos Totales (Bs)", "0.00", 0)
        self.kpi_reservas = self._create_kpi_card(self.kpi_frame, "Total Reservas", "0", 1)
        self.kpi_vehiculos = self._create_kpi_card(self.kpi_frame, "Vehículos Activos", "0", 2)
        self.kpi_mantenimiento = self._create_kpi_card(self.kpi_frame, "Costo Mantenimiento (Bs)", "0.00", 3)

        # Charts
        self.charts_frame = ctk.CTkFrame(parent)
        self.charts_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        self.charts_frame.grid_rowconfigure(0, weight=1)

        # Chart 1: Ingresos por mes
        self.fig1 = Figure(figsize=(5.5, 3.8), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.charts_frame)
        self.canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Chart 2: Reservas por estado (pie)
        self.fig2 = Figure(figsize=(5.5, 3.8), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.charts_frame)
        self.canvas2.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def _create_kpi_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, corner_radius=8)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(10, 0))
        lbl = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"))
        lbl.pack(pady=(0, 10))
        return lbl

    def cargar_dashboard(self):
        # KPIs
        kpis = self.controller.get_kpis()
        self.kpi_ingresos.configure(text=f"{kpis['ingresos']:,.2f}")
        self.kpi_reservas.configure(text=str(kpis['reservas']))
        self.kpi_vehiculos.configure(text=str(kpis['vehiculos_activos']))
        self.kpi_mantenimiento.configure(text=f"{kpis['costo_mantenimiento']:,.2f}")

        # Chart 1: Ingresos mensuales
        data_ingresos = self.controller.get_ingresos_por_mes()
        self.ax1.clear()
        if data_ingresos:
            meses = [self._mes_nombre(int(d['mes'])) for d in data_ingresos]
            valores = [float(d['total']) for d in data_ingresos]
            bars = self.ax1.bar(meses, valores, color='#3498DB', edgecolor='white')
            self.ax1.set_title("Ingresos por Mes (Bs)", fontsize=12, fontweight='bold', color='#2C3E50')
            self.ax1.set_ylabel("Monto (Bs)", fontsize=10)
            self.ax1.tick_params(axis='x', rotation=30, labelsize=9)
            self.ax1.tick_params(axis='y', labelsize=9)
            self.ax1.set_axisbelow(True)
            self.ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    self.ax1.text(bar.get_x() + bar.get_width()/2., height,
                                  f"{height:,.0f}", ha='center', va='bottom', fontsize=8)
        else:
            self.ax1.text(0.5, 0.5, "Sin datos de ingresos", ha='center', va='center',
                          transform=self.ax1.transAxes, fontsize=11, color='gray')
            self.ax1.set_xticks([])
            self.ax1.set_yticks([])
        self.fig1.tight_layout()
        self.canvas1.draw()

        # Chart 2: Distribución de reservas
        data_estados = self.controller.get_reservas_por_estado()
        self.ax2.clear()
        if data_estados:
            labels = [d['estado'] for d in data_estados]
            sizes = [int(d['total']) for d in data_estados]
            colores = ['#2ECC71', '#3498DB', '#F1C40F', '#E74C3C', '#9B59B6']
            wedges, texts, autotexts = self.ax2.pie(
                sizes, labels=labels, autopct='%1.1f%%', startangle=140,
                colors=colores[:len(labels)], textprops={'fontsize': 9}
            )
            self.ax2.set_title("Distribución de Reservas por Estado", fontsize=12, fontweight='bold', color='#2C3E50')
        else:
            self.ax2.text(0.5, 0.5, "Sin datos de reservas", ha='center', va='center',
                          transform=self.ax2.transAxes, fontsize=11, color='gray')
        self.fig2.tight_layout()
        self.canvas2.draw()

    @staticmethod
    def _mes_nombre(num):
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        return meses[num - 1] if 1 <= num <= 12 else str(num)

    # ═══════════════════════════════════════════════════════════════
    #  AUDITORÍA
    # ═══════════════════════════════════════════════════════════════

    def _build_auditoria(self, parent):
        self.audit_filter_frame = ctk.CTkFrame(parent, height=60)
        self.audit_filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.audit_filter_frame.grid_propagate(False)

        ctk.CTkLabel(self.audit_filter_frame, text="Usuario:").pack(side="left", padx=(10, 2))
        self.audit_user = ctk.CTkOptionMenu(self.audit_filter_frame, values=["Todos"], width=150)
        self.audit_user.pack(side="left", padx=5)

        ctk.CTkLabel(self.audit_filter_frame, text="Acción:").pack(side="left", padx=(15, 2))
        self.audit_action = ctk.CTkOptionMenu(self.audit_filter_frame, values=["Todas"], width=140)
        self.audit_action.pack(side="left", padx=5)

        ctk.CTkLabel(self.audit_filter_frame, text="Desde:").pack(side="left", padx=(15, 2))
        self.audit_desde = ctk.CTkEntry(self.audit_filter_frame, width=110, placeholder_text="YYYY-MM-DD")
        self.audit_desde.pack(side="left", padx=5)

        ctk.CTkLabel(self.audit_filter_frame, text="Hasta:").pack(side="left", padx=(10, 2))
        self.audit_hasta = ctk.CTkEntry(self.audit_filter_frame, width=110, placeholder_text="YYYY-MM-DD")
        self.audit_hasta.pack(side="left", padx=5)

        ctk.CTkButton(
            self.audit_filter_frame, text="Filtrar", command=self.aplicar_filtro_auditoria,
            width=80, font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=15)
        ctk.CTkButton(
            self.audit_filter_frame, text="Limpiar", command=self.limpiar_filtro_auditoria,
            width=80
        ).pack(side="left", padx=5)

        # Table
        self.audit_table_frame = ctk.CTkFrame(parent)
        self.audit_table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.audit_table_frame.grid_columnconfigure(0, weight=1)
        self.audit_table_frame.grid_rowconfigure(1, weight=1)

        headers = ["ID", "Usuario", "Acción", "Tabla", "Registro", "Fecha / Hora"]
        widths = [50, 110, 90, 110, 70, 160]
        hdr = ctk.CTkFrame(self.audit_table_frame, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=5)
        for col, (text, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(hdr, text=text, width=w, font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=col, padx=2, sticky="w"
            )

        self.audit_rows = ctk.CTkScrollableFrame(self.audit_table_frame)
        self.audit_rows.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.audit_rows.grid_columnconfigure(0, weight=1)

    def cargar_auditoria(self):
        # Cargar usuarios en filtro
        self.audit_users_map = {"Todos": None}
        res_users = self.controller.listar_usuarios_auditoria()
        if res_users["success"] and res_users["data"]:
            users = ["Todos"]
            for u in res_users["data"]:
                name = u["username"] if u["username"] else f"ID:{u['id_usuario']}"
                users.append(name)
                self.audit_users_map[name] = u["id_usuario"]
            self.audit_user.configure(values=users)
            self.audit_user.set("Todos")
        else:
            self.audit_user.configure(values=["Todos"])

        # Cargar acciones en filtro
        res_actions = self.controller.listar_acciones_auditoria()
        if res_actions["success"] and res_actions["data"]:
            actions = ["Todas"] + [a["accion"] for a in res_actions["data"]]
            self.audit_action.configure(values=actions)
            self.audit_action.set("Todas")
        else:
            self.audit_action.configure(values=["Todas"])

        self.aplicar_filtro_auditoria()

    def aplicar_filtro_auditoria(self):
        filtros = {}
        user_sel = self.audit_user.get()
        if user_sel != "Todos" and hasattr(self, 'audit_users_map'):
            uid = self.audit_users_map.get(user_sel)
            if uid is not None:
                filtros['id_usuario'] = uid

        action_sel = self.audit_action.get()
        if action_sel != "Todas":
            filtros['accion'] = action_sel

        desde = self.audit_desde.get().strip()
        if desde:
            filtros['fecha_desde'] = desde

        hasta = self.audit_hasta.get().strip()
        if hasta:
            filtros['fecha_hasta'] = hasta

        resultado = self.controller.listar_auditoria(filtros)
        self._render_auditoria_rows(resultado["data"] if resultado["success"] else [])
        if not resultado["success"]:
            for widget in self.audit_rows.winfo_children():
                widget.destroy()
            ctk.CTkLabel(self.audit_rows, text=resultado.get("message", "Error"), text_color="#E74C3C").pack(pady=20)

    def limpiar_filtro_auditoria(self):
        self.audit_user.set("Todos")
        self.audit_action.set("Todas")
        self.audit_desde.delete(0, "end")
        self.audit_hasta.delete(0, "end")
        self.aplicar_filtro_auditoria()

    def _render_auditoria_rows(self, data):
        for widget in self.audit_rows.winfo_children():
            widget.destroy()

        if not data:
            ctk.CTkLabel(
                self.audit_rows, text="No se encontraron registros de auditoría.", text_color="gray"
            ).pack(pady=20)
            return

        widths = [50, 110, 90, 110, 70, 160]
        for item in data:
            row = ctk.CTkFrame(self.audit_rows, fg_color="transparent")
            row.pack(fill="x", pady=1)
            vals = [
                str(item["id_auditoria"]),
                item["username"] if item["username"] else f"ID:{item['id_usuario']}",
                item["accion"],
                item["tabla_afectada"] if item["tabla_afectada"] else "—",
                str(item["id_registro"]) if item["id_registro"] is not None else "—",
                str(item["fecha_hora"]),
            ]
            for col, (text, w) in enumerate(zip(vals, widths)):
                ctk.CTkLabel(row, text=text, width=w, wraplength=w+10 if col == 1 else 0).grid(
                    row=0, column=col, padx=2, sticky="w"
                )
