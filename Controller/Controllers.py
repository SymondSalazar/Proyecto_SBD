from Model.database_mode import Database_model as Model


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

            # Mostrar información básica de reseñas
            resenas: list[dict] = Model.obtener_resenas_producto(id)
            if resenas:
                total_resenas: int = len(resenas)
                promedio: float = (
                    sum(r["calificacion"] for r in resenas) / total_resenas
                )
                print(f"Reseñas: {total_resenas} reseñas (⭐ {promedio:.1f}/5.0)")
            else:
                print("Reseñas: Sin reseñas disponibles")

            return producto
        else:
            print(f">>> No se encontró el producto con ID: {id}")
            return {}

    @staticmethod
    def obtener_resenas_producto(producto_id: str) -> list[dict]:
        resenas: list[dict] = Model.obtener_resenas_producto(producto_id)
        return resenas

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
    def crear_resena_producto(
        id_producto: str,
        id_usuario: str,
        calificacion: int,
        comentario: str,
    ) -> bool:
        exito = Model.crear_resena_producto(
            id_producto, id_usuario, calificacion, comentario
        )
        return exito

    # ============= MÉTODOS PARA VENDEDOR =============

    @staticmethod
    def crear_producto_vendedor(
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: str,
        vendedor_id: str,
    ) -> bool:
        resultado: bool = Model.crear_producto_vendedor(
            nombre, descripcion, precio, stock, categoria, vendedor_id
        )
        return resultado

    @staticmethod
    def actualizar_producto_vendedor(
        producto_id: str,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: str,
    ) -> bool:
        resultado: bool = Model.actualizar_producto_vendedor(
            producto_id, nombre, descripcion, precio, stock, categoria
        )
        return resultado

    @staticmethod
    def eliminar_producto_vendedor(producto_id: str) -> bool:
        resultado: bool = Model.eliminar_producto_vendedor(producto_id)
        return resultado

    @staticmethod
    def obtener_pedidos_vendedor(vendedor_id: str) -> list[dict]:
        pedidos: list[dict] = Model.obtener_pedidos_vendedor(vendedor_id)
        return pedidos

    @staticmethod
    def actualizar_estado_pedido(
        pedido_id: str, nuevo_estado: str, tipo_usuario: str
    ) -> bool:
        resultado: bool = Model.actualizar_estado_pedido(
            pedido_id, nuevo_estado, tipo_usuario
        )
        return resultado

    @staticmethod
    def obtener_estadisticas_vendedor(vendedor_id: str) -> dict:
        estadisticas: dict = Model.obtener_estadisticas_vendedor(vendedor_id)
        return estadisticas
