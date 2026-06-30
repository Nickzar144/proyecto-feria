from models.usuario_model import UsuarioModel


class AuthController:
    """
    Controlador de autenticación.
    Gestiona la lógica de negocio para el inicio de sesión,
    validaciones de entrada y comunicación con el modelo.
    """

    def __init__(self):
        self.model = UsuarioModel()

    def autenticar(self, username, password):
        """
        Valida credenciales contra la base de datos.
        Retorna un diccionario estandarizado con el resultado.
        """
        # Validaciones de negocio
        if not username or not username.strip():
            return {"success": False, "message": "El campo usuario es obligatorio."}

        if not password:
            return {"success": False, "message": "El campo contraseña es obligatorio."}

        usuario = self.model.obtener_por_username(username.strip())

        if usuario is None:
            return {"success": False, "message": "Credenciales inválidas."}

        estado = usuario.get("estado_usuario")
        if estado not in (1, "ACTIVO"):
            return {"success": False, "message": "El usuario se encuentra inactivo o bloqueado."}

        if self.model.verificar_contrasena(password, usuario["contrasena"]):
            # Registrar traza de auditoría
            self.model.registrar_auditoria(
                id_usuario=usuario["id_persona"],
                accion="LOGIN",
                tabla_afectada="usuario",
                id_registro=usuario["id_persona"]
            )

            return {
                "success": True,
                "message": "Autenticación exitosa.",
                "user": {
                    "id_persona": usuario["id_persona"],
                    "username": usuario["username"],
                    "id_rol": usuario["id_rol"],
                    "nombre_rol": usuario["nombre_rol"]
                }
            }
        else:
            return {"success": False, "message": "Credenciales inválidas."}
