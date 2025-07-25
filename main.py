from Controller.Controllers import DatabaseController
from Controller.InputManager import InputManager



def inicializar()  -> None:
    print("Sistema Inicializado")
    DatabaseController.conectar_database()

if __name__ == "__main__":
    
    inicializar()