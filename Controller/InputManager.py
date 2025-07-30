class InputManager:
    def __init__(self):
        raise TypeError("No se puede instanciar esta clase.")

    @staticmethod
    def leer_texto(mensaje: str) -> str:
        print(mensaje)
        return input().strip()

    @staticmethod
    def leer_texto_no_vacio(mensaje: str) -> str:
        valor: str = ""
        while True:
            valor = InputManager.leer_texto(mensaje)
            if valor.strip() != "":
                return valor
            else:
                print(">>> ERROR: Debe ingresar un texto no vacío")
        return valor

    @staticmethod
    def leer_entero(mensaje: str) -> int:
        valor: int = 0
        while True:
            try:
                print(mensaje)
                valor = int(input().strip())
                return valor
            except ValueError:
                print(">>> ERROR: Debe ingresar un número entero válido")
        return valor

    @staticmethod
    def leer_entero_positivo(mensaje: str) -> int:
        valor: int = -1
        while valor <= 0:
            valor = InputManager.leer_entero(mensaje)
            if valor < 0:
                print(">>> ERROR: El valor debe ser mayor a 0")
        return valor

    @staticmethod
    def leer_decimal(mensaje: str) -> float:
        valor: float = 0.0
        while True:
            try:
                print(mensaje)
                valor = float(input().strip())
                return valor
            except ValueError:
                print(">>> ERROR: Debe ingresar un número decimal válido")
        return valor

    @staticmethod
    def leer_confirmacion(mensaje: str) -> bool:
        respuesta: str = ""
        while respuesta.lower() not in ["s", "n"]:
            respuesta = InputManager.leer_texto(mensaje)
            if respuesta.lower() not in ["s", "n"]:
                print(">>> ERROR: Debe responder S o N")
        return respuesta.lower() == "s"

    @staticmethod
    def leer_opcion_menu(opciones: list[str], titulo: str) -> int:
        print(f"\n=== {titulo} ===")
        for i, opcion in enumerate(opciones):
            print(f"  {i + 1}. {opcion}")

        eleccion: int = -1

        while eleccion < 1 or eleccion > len(opciones):
            eleccion = InputManager.leer_entero(
                f"Seleccione una opción (1-{len(opciones)}): "
            )
            if eleccion < 1 or eleccion > len(opciones):
                print(">>> ERROR: Opción inválida. Intente nuevamente")
        return eleccion

    @staticmethod
    def pausar() -> None:
        print("\n>>> Presione Enter para continuar...")
        input()
