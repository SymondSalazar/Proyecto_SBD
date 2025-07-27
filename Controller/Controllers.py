from Model.file_mode import File_model as Model


class SystemController:
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
        valido, tipo_usuario, id_ = Model.validar_usuario(email, password)
        return valido, tipo_usuario, id_

    @staticmethod
    def mostrar_productos(metodo: str, busqueda: str) -> list[str]:
        productos: list[str] = Model.filtrar_productos(metodo, busqueda)
        return productos

    @staticmethod
    def mostrar_productos_vendedor(id: str) -> list[str]:
        productos: list[str] = SystemController.mostrar_productos("vendedor", id)
        return productos
