from Controller.Controllers import DatabaseController
from Controller.InputManager import InputManager


def inicializar() -> None:
    print("Sistema Inicializado")
    DatabaseController.conectar_database()


def menu_cliente():
    print("--- Bienvenido Cliente ---")
    InputManager.pausar()


def menu_vendedor():
    print("--- Bienvenido Vendedor ---")
    opciones: list[str] = [
        "Mostrar todos mis productos",
        "Actualizar Productos",
        "Gestionar Pedidos",
        "Cerrar sesion",
        "Apagar Sistema",
    ]
    seleccion: int = InputManager.leer_opcion_menu(opciones, "Menu")
    print(seleccion)
    InputManager.pausar()


def sistema() -> None:
    while True:
        print("\n  ---- Iniciar Sesion ----")
        email = InputManager.leer_texto_no_vacio("Ingrese  su email: ")
        password = InputManager.leer_texto_no_vacio("Ingrese su contraseña: ")
        tupla_result = DatabaseController.iniciar_sesion(email, password)
        if not tupla_result[0]:
            print("Error: Usuario no encontrado")
        else:
            break
    if tupla_result[1] == "cliente":
        menu_cliente()
    else:
        menu_vendedor()


if __name__ == "__main__":

    inicializar()
    sistema()
