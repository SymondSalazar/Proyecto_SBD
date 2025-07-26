from Model.file_mode import File_model as Model


class DatabaseController:
    def __init__(self):
        raise TypeError("Esta clase no puede ser instanciada")

    @staticmethod
    def conectar_database() -> None:
        if Model.conectar():
            print("Conexion a la base de datos establecida con exito")
        else:
            raise ConnectionError("No se pudo conectar")

    @staticmethod
    def iniciar_sesion(email: str, password: str):
        valido, tipo_usuario = Model.validar_usuario(email, password)
        return valido, tipo_usuario
