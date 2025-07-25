import Model.file_mode as Model
class DatabaseController:
    def __init__(self):
        pass

    @staticmethod
    def conectar_database():
        if Model.conectar():
            print("Conectado Correctamente")
        else:
            raise ConnectionError("No se pudo conectar")
    
