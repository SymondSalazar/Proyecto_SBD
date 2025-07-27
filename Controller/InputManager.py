class InputManager:
    def __init__(self):
        raise TypeError("No se puede instanciar esta clase.")

    @staticmethod
    def leer_texto(mensaje: str) -> str:
        print(mensaje)
        return input().strip()

    @staticmethod
    def leer_texto_no_vacio(mensaje: str) -> str:
        valor: str
        while True:
            valor = InputManager.leer_texto(mensaje)
            if valor.strip() != "":
                return valor
            else:
                print("Error: Debe ingresar un texto no vacio")

    @staticmethod
    def leer_entero(mensaje: str) -> int:
        while True:
            try:
                print(mensaje)
                valor: int = int(input().strip())
                return valor
            except ValueError:
                print("Error: Debes Ingresar un numero entero.")

    @staticmethod
    def leer_entero_positivo(mensaje: str) -> int:
        valor: int = -1
        while valor <= 0:
            valor = InputManager.leer_entero(mensaje)
            if valor < 0:
                print("Error: El valor debe ser mayor a 0.")
        return valor

    @staticmethod
    def leer_decimal(mensaje: str) -> float:
        while True:
            try:
                print(mensaje)
                valor = float(input().strip())
                return valor
            except ValueError:
                print("Error debes ingresar un numero valido.")

    @staticmethod
    def leer_confirmacion(mensaje: str) -> bool:
        respuesta: str = ""
        while respuesta.lower() not in ["s", "n"]:
            respuesta = InputManager.leer_texto()
            if respuesta.lower() not in ["s", "n"]:
                print("Error: Debes  responder S o N.")
        return respuesta.lower() == "s"

    @staticmethod
    def leer_opcion_menu(opciones: list[str], titulo: str) -> int:
        print(f"\n---- {titulo} ----")
        for i, opcion in enumerate(opciones):
            print(f"{i + 1}.- {opcion}")

        eleccion: int = -1

        while eleccion < 1 or eleccion > len(opciones):
            eleccion = InputManager.leer_entero(
                f"Seleccione una opcion (1-{len(opciones)}): "
            )
            if eleccion < 1 or eleccion > len(opciones):
                print("Error : opcion invalidad. Intente nuevamente.")
        return eleccion

    @staticmethod
    def pausar() -> None:
        print("\nPresione enter para continuar.")
        input()
