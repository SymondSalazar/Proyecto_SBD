from Controller.Controllers import SystemController
from Controller.InputManager import InputManager
import sys


def inicializar() -> None:
    print("Sistema Inicializado")
    SystemController.conectar_database()


def menu_cliente(id: str) -> None:
    print("--- Bienvenido Cliente ---")
    InputManager.pausar()


def menu_vendedor(id: str) -> None:
    print("--- Bienvenido Vendedor ---")
    opciones: list[str] = [
        "Mostrar todos mis productos",
        "Actualizar Productos",
        "Gestionar Pedidos",
        "Cerrar sesion",
        "Apagar Sistema",
    ]
    seleccion: int = InputManager.leer_opcion_menu(opciones, "Menu")
    match seleccion:
        case 1:
            productos: list[str] = SystemController.mostrar_productos_vendedor(id)
            if len(productos) == 0:
                print("No cuenta con nigun producto")
                pass

            print("\n ---- Estos son sus productos ----")
            for i, producto in enumerate(productos):
                print(f"{i + 1}.- {producto}")
        case 2:
            pass
        case 3:
            pass
        case 4:
            sistema()
        case 5:
            sys.exit(0)


def sistema() -> None:
    while True:
        print("\n  ---- Iniciar Sesion ----")
        email = InputManager.leer_texto_no_vacio("Ingrese  su email: ")
        password = InputManager.leer_texto_no_vacio("Ingrese su contraseña: ")
        tupla_result = SystemController.iniciar_sesion(email, password)
        if not tupla_result[0]:
            print("Error: Usuario no encontrado")
        else:
            break
    if tupla_result[1] == "cliente":
        menu_cliente(tupla_result[2])
    else:
        menu_vendedor(tupla_result[2])


i = 0
while True:
    if __name__ == "__main__":
        if i == 0:
            inicializar()
            i += 1
        sistema()
