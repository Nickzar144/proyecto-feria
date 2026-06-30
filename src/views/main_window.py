import customtkinter as ctk
from views.flota_view import FlotaView
from views.clientes_view import ClientesView
from views.reservas_view import ReservasView
from views.reportes_view import ReportesView


class MainWindow(ctk.CTkFrame):
    """
    Contenedor principal de la aplicación con menú de navegación lateral.
    Gestiona el área de contenido dinámico y el cierre de sesión.
    """

    def __init__(self, master, user, on_logout):
        super().__init__(master)
        self.master = master
        self.user = user
        self.on_logout = on_logout
        self.current_view = None

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ──
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar,
            text="MOVISHARE",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_logo.grid(row=0, column=0, pady=(35, 5), padx=20)

        self.lbl_user = ctk.CTkLabel(
            self.sidebar,
            text=f"Usuario: {user['username']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_user.grid(row=1, column=0, pady=(0, 2), padx=20)

        self.lbl_role = ctk.CTkLabel(
            self.sidebar,
            text=f"Rol: {user['nombre_rol']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_role.grid(row=2, column=0, pady=(0, 30), padx=20)

        # ── Botones de navegación ──
        self.btn_flota = ctk.CTkButton(
            self.sidebar,
            text="Gestión de Flota",
            command=self.show_flota,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.btn_flota.grid(row=3, column=0, pady=5, padx=15, sticky="ew")

        self.btn_clientes = ctk.CTkButton(
            self.sidebar,
            text="Gestión de Clientes",
            command=self.show_clientes,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.btn_clientes.grid(row=4, column=0, pady=5, padx=15, sticky="ew")

        self.btn_reservas = ctk.CTkButton(
            self.sidebar,
            text="Reservas y Pagos",
            command=self.show_reservas,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.btn_reservas.grid(row=5, column=0, pady=5, padx=15, sticky="ew")

        self.btn_reportes = ctk.CTkButton(
            self.sidebar,
            text="Reportes y Auditoría",
            command=self.show_reportes,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.btn_reportes.grid(row=6, column=0, pady=5, padx=15, sticky="ew")

        # ── Logout ──
        self.btn_logout = ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            command=self.logout,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_logout.grid(row=7, column=0, pady=(10, 30), padx=15, sticky="ew")

        # ── Área de contenido ──
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        # Vista por defecto
        self.show_flota()

    def clear_content(self):
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def show_flota(self):
        self.clear_content()
        self.current_view = FlotaView(self.content)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_clientes(self):
        self.clear_content()
        self.current_view = ClientesView(self.content)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_reservas(self):
        self.clear_content()
        self.current_view = ReservasView(self.content)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_reportes(self):
        self.clear_content()
        self.current_view = ReportesView(self.content)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def _show_placeholder(self, texto):
        self.clear_content()
        frame = ctk.CTkFrame(self.content)
        frame.grid(row=0, column=0, sticky="nsew")
        lbl = ctk.CTkLabel(
            frame,
            text=texto,
            font=ctk.CTkFont(size=18),
            text_color="gray",
            justify="center"
        )
        lbl.pack(expand=True)
        self.current_view = frame

    def logout(self):
        self.on_logout()
