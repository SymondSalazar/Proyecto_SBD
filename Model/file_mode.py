import pandas as pd


class File_model:
    clientes = pd.DataFrame()
    cuentas = pd.DataFrame()
    pedidos_productos = pd.DataFrame()
    pedidos = pd.DataFrame()
    productos_imagenes = pd.DataFrame()
    productos_resenas = pd.DataFrame()
    productos = pd.DataFrame()
    vendedores = pd.DataFrame()

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
            File_model.pedidos["fecha_entrega"] = pd.to_datetime(
                File_model.pedidos["fecha_entrega"], errors="coerce", format="%d-%m-%Y"
            )
            File_model.pedidos["fecha_compra"] = pd.to_datetime(
                File_model.pedidos["fecha_compra"], errors="coerce", format="%d-%m-%Y"
            )
            return True

        except FileNotFoundError:
            print(">>> ERROR: No se encontraron los archivos de la base de datos")
            return False

        except Exception:
            print(">>> ERROR: Hubo un problema al leer los archivos de datos")
            return False

    @staticmethod
    def validar_usuario(email: str, password: str) -> tuple[bool, str, str]:
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
    def filtrar_productos(metodo: str, busqueda: str) -> tuple[list[str], list[str]]:
        productos: list[str] = []
        ids: list[str] = []

        metodos = ["id", "nombre", "descripcion", "categoria", "vendedor"]
        categorias = ["juguetes", "ropa", "tecnologia", "hogar"]
        if metodo == "" and busqueda == "":
            productos = File_model.productos["nombre"].tolist()
            ids = File_model.productos["id"].tolist()
            return productos, ids
        if metodo == "categoria" and busqueda not in categorias:
            return productos, ids
        if metodo not in metodos:
            return productos, ids

        filas = pd.DataFrame()
        match metodo:
            case "id":
                filas = File_model.productos[
                    File_model.productos["id"].str.lower() == busqueda.lower()
                ]
            case "nombre":
                filas = File_model.productos[
                    File_model.productos["nombre"].str.lower() == busqueda.lower()
                ]
            case "descripcion":
                filas = File_model.productos[
                    File_model.productos["descripcion"].str.lower() == busqueda.lower()
                ]
            case "categoria":
                filas = File_model.productos[
                    File_model.productos["categoria"].str.lower() == busqueda.lower()
                ]
            case "vendedor":
                filas = File_model.productos[
                    File_model.productos["vendedor_id"].str.lower() == busqueda.lower()
                ]

        if filas.empty:
            return productos, ids

        # Versión más robusta para extraer los nombres
        nombres_series = filas["nombre"]
        if not isinstance(nombres_series, pd.Series):
            return productos, ids
        if not isinstance(filas["id"], pd.Series):
            return productos, ids

        # Convertir a lista de strings
        productos = [str(nombre) for nombre in nombres_series if pd.notna(nombre)]
        ids = filas["id"].tolist()
        return productos, ids

    @staticmethod
    def obtener_producto(id: str) -> dict:
        filas = File_model.productos[File_model.productos["id"] == id]
        if filas.empty:
            return {}

        producto = filas.iloc[0].to_dict()

        return producto

    @staticmethod
    def actualizar_stock(cantidad: int, id: str) -> bool:
        filas = File_model.productos[File_model.productos["id"] == id]
        if filas.empty:
            return False

        File_model.productos.loc[File_model.productos["id"] == id, "stock"] = cantidad
        File_model.productos.to_csv("datos_bd/productos.csv", index=False)
        return True

    @staticmethod
    def guardar_pedido(id_usr: str, id_producto: str, cantidad: int) -> None:
        id_pedido = "PD" + str(int(File_model.pedidos["id"].iloc[-1][2:]) + 1).zfill(3)
        cliente_id = id_usr
        direccion_entrega = File_model.clientes.loc[
            File_model.clientes["cuenta_id"] == cliente_id, "direccion_envio"
        ].iloc[0]

        fecha_compra = pd.Timestamp.now().strftime("%Y-%m-%d")

        fecha_entrega = pd.Timestamp.now() + pd.Timedelta(days=5)

        if isinstance(fecha_entrega, pd.Timestamp):
            fecha_entrega = fecha_entrega.strftime("%Y-%m-%d")

        estado_envio = "En_Proceso"

        nuevo_pedido_producto = pd.DataFrame(
            {
                "pedido_id": [id_pedido],
                "producto_id": [id_producto],
                "cantidad": [cantidad],
            }
        )
        nuevo_pedido_producto.to_csv(
            "datos_bd/pedidos_productos.csv", mode="a", header=False, index=False
        )

        nuevo_pedido = pd.DataFrame(
            {
                "id": [id_pedido],
                "cliente_id": [cliente_id],
                "direccion_entrega": [direccion_entrega],
                "fecha_entrega": [fecha_entrega],
                "fecha_compra": [fecha_compra],
                "estado_envio": [estado_envio],
            }
        )

        nuevo_pedido.to_csv("datos_bd/pedidos.csv", mode="a", header=False, index=False)

    @staticmethod
    def crear_nuevo_pedido(id_usr: str) -> str:
        # Recargar DataFrames para tener datos actualizados
        File_model.pedidos = pd.read_csv("datos_bd/pedidos.csv")

        # Generar nuevo ID de pedido
        if File_model.pedidos.empty:
            id_pedido = "PD001"
        else:
            id_pedido = "PD" + str(
                int(File_model.pedidos["id"].iloc[-1][2:]) + 1
            ).zfill(3)

        cliente_id = id_usr
        direccion_entrega = File_model.clientes.loc[
            File_model.clientes["cuenta_id"] == cliente_id, "direccion_envio"
        ].iloc[0]

        fecha_compra = pd.Timestamp.now().strftime("%d-%m-%Y")
        fecha_entrega = ""
        estado_envio = "EN_PROCESO"  # Estado inicial

        nuevo_pedido = pd.DataFrame(
            {
                "id": [id_pedido],
                "cliente_id": [cliente_id],
                "direccion_entrega": [direccion_entrega],
                "fecha_entrega": [fecha_entrega],
                "fecha_compra": [fecha_compra],
                "estado_envio": [estado_envio],
            }
        )

        File_model.pedidos = pd.concat(
            [File_model.pedidos, nuevo_pedido], ignore_index=True
        )

        nuevo_pedido.to_csv("datos_bd/pedidos.csv", mode="a", header=False, index=False)

        return id_pedido

    @staticmethod
    def agregar_producto_a_pedido(
        id_pedido: str, id_producto: str, cantidad: int
    ) -> bool:
        try:
            # Recargar DataFrame para tener datos actualizados
            File_model.pedidos_productos = pd.read_csv("datos_bd/pedidos_productos.csv")

            nuevo_pedido_producto = pd.DataFrame(
                {
                    "pedido_id": [id_pedido],
                    "producto_id": [id_producto],
                    "cantidad": [cantidad],
                }
            )

            # Agregar al DataFrame en memoria
            File_model.pedidos_productos = pd.concat(
                [File_model.pedidos_productos, nuevo_pedido_producto], ignore_index=True
            )

            # Guardar en archivo
            nuevo_pedido_producto.to_csv(
                "datos_bd/pedidos_productos.csv", mode="a", header=False, index=False
            )
            return True
        except Exception:
            return False

    @staticmethod
    def obtener_pedidos_usuario(id_usr: str) -> list[dict]:
        # Por ahora lo recargo los datos porque son pocos, cuando tengamos la base de datos no sera necesario
        # Ya que la base de datos estara actualizada y solo se necesitara una query
        File_model.pedidos = pd.read_csv("datos_bd/pedidos.csv")
        File_model.pedidos_productos = pd.read_csv("datos_bd/pedidos_productos.csv")
        File_model.productos = pd.read_csv("datos_bd/productos.csv")

        pedidos_usuario = []

        # Obtener pedidos del usuario
        pedidos_cliente = File_model.pedidos[File_model.pedidos["cliente_id"] == id_usr]

        for _, pedido in pedidos_cliente.iterrows():
            pedido_info = {
                "id": pedido["id"],
                "cliente_id": pedido["cliente_id"],
                "direccion_entrega": pedido["direccion_entrega"],
                "fecha_entrega": pedido["fecha_entrega"],
                "fecha_compra": pedido["fecha_compra"],
                "estado_envio": pedido["estado_envio"],
                "productos": [],
            }

            # Obtener productos del pedido
            productos_pedido = File_model.pedidos_productos[
                File_model.pedidos_productos["pedido_id"] == pedido["id"]
            ]

            productos_lista = []
            for _, producto_pedido in productos_pedido.iterrows():
                # Obtener información del producto
                producto_info = File_model.productos[
                    File_model.productos["id"] == producto_pedido["producto_id"]
                ]

                if not producto_info.empty:
                    producto_data = {
                        "id": producto_info.iloc[0]["id"],
                        "nombre": producto_info.iloc[0]["nombre"],
                        "precio": producto_info.iloc[0]["precio"],
                        "cantidad": producto_pedido["cantidad"],
                    }
                    productos_lista.append(producto_data)

            pedido_info["productos"] = productos_lista
            pedidos_usuario.append(pedido_info)

        return pedidos_usuario

    @staticmethod
    def confirmar_pedido(id_pedido: str) -> bool:
        try:
            # Recargar DataFrame para tener datos actualizados
            File_model.pedidos = pd.read_csv("datos_bd/pedidos.csv")

            # Actualizar estado del pedido
            File_model.pedidos.loc[
                File_model.pedidos["id"] == id_pedido, "estado_envio"
            ] = "EN_PROCESO"

            # Calcular fecha de entrega (5 días después)
            import datetime

            fecha_entrega = datetime.datetime.now() + datetime.timedelta(days=5)
            fecha_entrega_str = fecha_entrega.strftime("%d-%m-%Y")
            File_model.pedidos.loc[
                File_model.pedidos["id"] == id_pedido, "fecha_entrega"
            ] = fecha_entrega_str

            # Guardar cambios
            File_model.pedidos.to_csv("datos_bd/pedidos.csv", index=False)

            return True
        except Exception:
            return False
