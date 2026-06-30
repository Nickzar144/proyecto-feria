import sys
import os

# Asegurar que el directorio src/ esté en sys.path para importaciones absolutas planas
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import customtkinter as ctk
from config.database import Database
from views.login_view import LoginView

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """
    Punto de entrada unificado de la aplicación MOVISHARE.
    Gestiona el ciclo de vida de la ventana principal y la navegación inicial.
    """

    def __init__(self):
        super().__init__()
        self.title("MOVISHARE - Sistema de Alquiler de Vehículos")
        self.geometry("1280x800")
        self.minsize(1100, 700)

        self.current_user = None
        self.current_frame = None

        # Inicializar pool de conexiones MySQL
        try:
            Database.initialize_pool()
        except Exception as e:
            self.mostrar_error_db(f"No se pudo conectar a la base de datos.\n\nDetalle: {e}")
            return

        self.show_login()

    def mostrar_error_db(self, mensaje):
        """Muestra un mensaje crítico si la base de datos no está disponible."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both")
        lbl = ctk.CTkLabel(
            frame,
            text=mensaje,
            text_color="#E74C3C",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        lbl.pack(expand=True)
        self.current_frame = frame

    def show_login(self):
        """Renderiza la pantalla de inicio de sesión."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_user = None
        self.current_frame = LoginView(self, self.on_login_success)
        self.current_frame.pack(expand=True, fill="both")

    def on_login_success(self, user):
        """
        Callback invocado por LoginView cuando las credenciales son válidas.
        Instancia la ventana principal con menú lateral.
        """
        from views.main_window import MainWindow
        self.current_user = user
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = MainWindow(self, user, self.show_login)
        self.current_frame.pack(expand=True, fill="both")

    def on_closing(self):
        """Libera recursos al cerrar la aplicación."""
        Database.close_pool()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
