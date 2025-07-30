from Model.file_mode import File_model as Model


class SystemController:
    def __init__(self):
        raise TypeError("Esta clase no puede ser instanciada")

    @staticmethod
    def conectar_database() -> None:
        if Model.conectar():
            print(">>> Conexión a la base de datos establecida con éxito")
        else:
            raise ConnectionError(">>> ERROR: No se pudo conectar a la base de datos")

    @staticmethod
    def iniciar_sesion(email: str, password: str):
        valido, tipo_usuario, id_ = Model.validar_usuario(email, password)
        return valido, tipo_usuario, id_

    @staticmethod
    def mostrar_productos(metodo: str, busqueda: str) -> tuple[list[str], list[str]]:
        ids: list[str] = []
        productos: list[str] = []
        productos, ids = Model.filtrar_productos(metodo, busqueda)
        return productos, ids

    @staticmethod
    def mostrar_productos_vendedor(id: str) -> tuple[list[str], list[str]]:
        productos, ids = SystemController.mostrar_productos("vendedor", id)
        return productos, ids

    @staticmethod
    def mostrar_producto(id: str) -> dict:
        producto = Model.obtener_producto(id)
        if producto:
            print("\n=== DETALLES DEL PRODUCTO ===")
            for key, value in producto.items():
                if key == "id" or key == "vendedor_id":
                    continue

                print(f"{key.capitalize()}: {value}")
            return producto
        else:
            print(f">>> No se encontró el producto con ID: {id}")
            return {}

    @staticmethod
    def actualizar_stock(cantidad: int, id: str) -> bool:
        actualizacion_exitosa = Model.actualizar_stock(cantidad, id)
        return actualizacion_exitosa

    @staticmethod
    def guardar_pedido(id_usr: str, id_producto: str, cantidad: int) -> None:
        try:
            Model.guardar_pedido(id_usr, id_producto, cantidad)
            print(">>> Pedido guardado exitosamente")
        except Exception as e:
            print(f">>> ERROR: No se pudo guardar el pedido. {e}")

    @staticmethod
    def crear_nuevo_pedido(id_usr: str) -> str:
        id_pedido = Model.crear_nuevo_pedido(id_usr)
        return id_pedido

    @staticmethod
    def agregar_producto_a_pedido(
        id_pedido: str, id_producto: str, cantidad: int
    ) -> bool:
        agregado_exitoso: bool = Model.agregar_producto_a_pedido(
            id_pedido, id_producto, cantidad
        )
        return agregado_exitoso

    @staticmethod
    def obtener_pedidos_usuario(id_usr: str) -> list[dict]:
        pedidos_usuario = Model.obtener_pedidos_usuario(id_usr)
        return pedidos_usuario

    @staticmethod
    def confirmar_pedido(id_pedido: str) -> bool:
        confirmacion_exitosa: bool = Model.confirmar_pedido(id_pedido)
        return confirmacion_exitosa

    @staticmethod
    def crear_resena_producto(cliente_id: str, producto_id: str, calificacion: int, comentario: str) -> bool:
        return Model.crear_resena(cliente_id, producto_id, calificacion, comentario)

    @staticmethod
    def obtener_resenas_producto(producto_id: str) -> list[dict]:
        return Model.obtener_resenas_producto(producto_id)

    @staticmethod
    def puede_cliente_resenar(cliente_id: str, producto_id: str) -> bool:
        return Model.verificar_puede_resenar(cliente_id, producto_id)

    @staticmethod
    def obtener_producto_info(producto_id: str) -> dict:
        productos = Model.productos
        producto = productos[productos["id"] == producto_id]
        if not producto.empty:
            producto_data = producto.iloc[0]
            return {
                "id": producto_data["id"],
                "nombre": producto_data["nombre"],
                "precio": producto_data["precio"],
                "stock": producto_data["stock"],
                "calificacion": producto_data["calificacion"],
                "descripcion": producto_data["descripcion"]
            }
        return {}

    @staticmethod
    def obtener_productos_pedido(pedido_id: str) -> list[dict]:
        pedidos_productos = Model.pedidos_productos
        productos_pedido = pedidos_productos[pedidos_productos["pedido_id"] == pedido_id]
        
        productos_lista = []
        for _, producto in productos_pedido.iterrows():
            productos_lista.append({
                "producto_id": producto["producto_id"],
                "cantidad": producto["cantidad"]
            })
        
        return productos_lista
