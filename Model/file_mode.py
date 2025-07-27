import pandas as pd


class File_model:
    clientes = None
    cuentas = None
    pedidos_productos = None
    pedidos = None
    productos_imagenes = None
    productos_resenas = None
    productos = None
    vendedores = None

    def __init__(self):
        raise TypeError("Esta clase no debe ser instanciada")

    @staticmethod
    def conectar() -> bool:
        try:
            pedidos_path = "datos_bd/pedidos_productos.csv"
            resena_path = "datos_bd/productos_reseñas.csv"
            File_model.clientes = pd.read_csv("datos_bd/clientes.csv")
            File_model.cuentas = pd.read_csv("datos_bd/cuentas.csv")
            File_model.pedidos_productos = pd.read_csv(pedidos_path)
            File_model.pedidos = pd.read_csv("datos_bd/pedidos.csv")
            File_model.productos_imagenes = pd.read_csv(
                "datos_bd/productos_categorias.csv"
            )
            File_model.productos_resenas = pd.read_csv(resena_path)
            File_model.productos = pd.read_csv("datos_bd/productos.csv")
            File_model.vendedores = pd.read_csv("datos_bd/vendedores.csv")
            return True

        except FileNotFoundError:
            print("No se ha encontrado el archivo")
            return False

        except Exception:
            print("Hubo un error al leer el archivo")

    @staticmethod
    def validar_usuario(email: str, password: str) -> tuple[bool, str]:
        filas = File_model.cuentas[
            (File_model.cuentas["email"] == email)
            & (File_model.cuentas["contrasena"] == password)
        ]
        if filas.empty:
            return (False, "Ninguno", "Niguno")

        id_ = filas.iloc[0]["id"]

        get_rol = File_model.clientes[File_model.clientes["cuenta_id"] == id_]
        rol = "cliente"
        if get_rol.empty:
            rol = "vendedor"
            return (True, rol, id_)

        return (True, rol, id_)

    @staticmethod
    def filtrar_productos(metodo: str, busqueda: str) -> list[str]:
        productos: list[str] = []

        metodos = ["id", "nombre", "descripcion", "categoria", "vendedor"]
        categorias = ["juguetes", "ropa", "tecnologia", "hogar"]

        if metodo == "categoria" and busqueda not in categorias:
            return productos
        if metodo not in metodos:
            return productos

        filas = pd.DataFrame()
        match metodo:
            case "id":
                filas = File_model.productos[File_model.productos["id"] == busqueda]
            case "nombre":
                filas = File_model.productos[File_model.productos["nombre"] == busqueda]
            case "descripcion":
                filas = File_model.productos[
                    File_model.productos["descripcion"] == busqueda
                ]
            case "categoria":
                filas = File_model.productos[
                    File_model.productos["categoria"] == busqueda
                ]
            case "vendedor":
                filas = File_model.productos[
                    File_model.productos["vendedor_id"] == busqueda
                ]

        if filas.empty:
            return productos

        for nombre in filas["nombre"]:
            productos.append(nombre)
        return productos
