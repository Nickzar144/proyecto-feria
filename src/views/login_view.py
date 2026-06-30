import customtkinter as ctk
from controllers.auth_controller import AuthController


class LoginView(ctk.CTkFrame):
    """
    Vista de inicio de sesión.
    Renderiza el formulario de autenticación usando CustomTkinter.
    No contiene lógica SQL.
    """

    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.controller = AuthController()

        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Contenedor centrado del formulario
        self.frame_form = ctk.CTkFrame(self, width=420, height=480, corner_radius=12)
        self.frame_form.grid(row=0, column=0, padx=20, pady=20, sticky="")
        self.frame_form.grid_propagate(False)
        self.frame_form.grid_columnconfigure(0, weight=1)

        # Títulos
        self.lbl_title = ctk.CTkLabel(
            self.frame_form,
            text="MOVISHARE",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.lbl_title.grid(row=0, column=0, pady=(50, 5), padx=20)

        self.lbl_subtitle = ctk.CTkLabel(
            self.frame_form,
            text="Sistema de Gestión de Alquiler de Vehículos",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.lbl_subtitle.grid(row=1, column=0, pady=(0, 30), padx=20)

        # Entrada usuario
        self.entry_username = ctk.CTkEntry(
            self.frame_form,
            placeholder_text="Nombre de usuario",
            width=300,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.entry_username.grid(row=2, column=0, pady=10, padx=20)
        self.entry_username.focus()

        # Entrada contraseña
        self.entry_password = ctk.CTkEntry(
            self.frame_form,
            placeholder_text="Contraseña",
            show="*",
            width=300,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.entry_password.grid(row=3, column=0, pady=10, padx=20)

        # Botón login
        self.btn_login = ctk.CTkButton(
            self.frame_form,
            text="Ingresar al Sistema",
            command=self.login,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_login.grid(row=4, column=0, pady=(25, 10), padx=20)

        # Mensaje de error
        self.lbl_message = ctk.CTkLabel(
            self.frame_form,
            text="",
            text_color="#E74C3C",
            font=ctk.CTkFont(size=12),
            wraplength=300
        )
        self.lbl_message.grid(row=5, column=0, pady=(5, 10), padx=20)

        # Atajos de teclado
        self.entry_username.bind("<Return>", lambda event: self.login())
        self.entry_password.bind("<Return>", lambda event: self.login())

    def login(self):
        """Recoge datos de la vista y delega la autenticación al controlador."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        resultado = self.controller.autenticar(username, password)

        if resultado["success"]:
            self.lbl_message.configure(text="", text_color="#E74C3C")
            self.on_login_success(resultado["user"])
        else:
            self.lbl_message.configure(text=resultado["message"])
