import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Optional, Tuple, Any
from Controller.InputManager import InputManager


class Database_model:
    connection: Optional[mysql.connector.MySQLConnection] = None

    # Configuración de la base de datos
    DB_CONFIG = {
        "host": "localhost",
        "port": 3306,
        "database": "Proyecto_SBD",
        "user": "root",
        "password": "",
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "autocommit": True,
    }

    def __init__(self):
        raise TypeError("Esta clase no debe ser instanciada")

    @staticmethod
    def conectar() -> bool:
        """Establece conexión con la base de datos MySQL"""
        try:
            Database_model.connection = mysql.connector.connect(
                **Database_model.DB_CONFIG
            )

            if Database_model.connection and Database_model.connection.is_connected():
                db_info = Database_model.connection.get_server_info()
                print(f">>> Conectado a MySQL Server versión {db_info}")
                return True
            return False

        except Error as e:
            print(f">>> ERROR: No se pudo conectar a MySQL: {e}")
            return False
        except Exception as e:
            print(f">>> ERROR: Error inesperado al conectar: {e}")
            return False

    @staticmethod
    def _ejecutar_query(
        query: str, params: Optional[Tuple] = None, fetch_type: str = "none"
    ) -> Any:
        """Método auxiliar para ejecutar queries de forma segura"""
        try:
            if (
                not Database_model.connection
                or not Database_model.connection.is_connected()
            ):
                if not Database_model.conectar():
                    return None

            if Database_model.connection is None:
                return None

            cursor = Database_model.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch_type == "one":
                result = cursor.fetchone()
            elif fetch_type == "all":
                result = cursor.fetchall()
            else:
                result = cursor.rowcount

            cursor.close()
            return result

        except Error as e:
            print(f">>> ERROR en query: {e}")
            return None
        except Exception as e:
            print(f">>> ERROR inesperado: {e}")
            return None

    @staticmethod
    def validar_usuario(email: str, password: str) -> tuple[bool, str, str]:
        #  Valida las credenciales del usuario
        query = """
            SELECT c.id, c.email, c.nombre, cl.cuenta_id as cliente_id, v.cuenta_id as vendedor_id
            FROM cuentas c
            LEFT JOIN clientes cl ON c.id = cl.cuenta_id
            LEFT JOIN vendedores v ON c.id = v.cuenta_id
            WHERE c.email = %s AND c.contrasena = %s
        """

        resultado = Database_model._ejecutar_query(query, (email, password), "one")

        if not resultado:
            return (False, "Ninguno", "Ninguno")

        id_usuario = str(resultado["id"])
        seleccion: int = 0
        if resultado["cliente_id"] and resultado["vendedor_id"]:
            opciones: list[str] = ["Ingresar como Cliente", "Ingresar como Vendedor"]
            seleccion = InputManager.leer_opcion_menu(
                opciones, "Seleccione el modo de entrada"
            )
            match seleccion:
                case 1:
                    return (True, "cliente", id_usuario)
                case 2:
                    return (True, "vendedor", id_usuario)
        # Determinar el tipo de usuario
        if resultado["cliente_id"]:
            return (True, "cliente", id_usuario)
        elif resultado["vendedor_id"]:
            return (True, "vendedor", id_usuario)
        else:
            return (False, "Ninguno", "Ninguno")

    @staticmethod
    def filtrar_productos(metodo: str, busqueda: str) -> tuple[list[str], list[str]]:
        # Filtra productos según el método y búsqueda especificados
        productos: list[str] = []
        ids: list[str] = []

        # Construir query base
        query_base = (
            "SELECT id, nombre, descripcion, precio, stock, categoria FROM productos"
        )
        params = ()

        # Agregar condiciones según el método
        if metodo == "" and busqueda == "":
            query = query_base + " ORDER BY nombre"
        elif metodo == "id":
            query = query_base + " WHERE LOWER(id) = LOWER(%s)"
            params = (busqueda,)
        elif metodo == "nombre":
            query = query_base + " WHERE LOWER(nombre) LIKE LOWER(%s)"
            params = (f"%{busqueda}%",)
        elif metodo == "descripcion":
            query = query_base + " WHERE LOWER(descripcion) LIKE LOWER(%s)"
            params = (f"%{busqueda}%",)
        elif metodo == "categoria":
            categorias_validas = ["juguetes", "ropa", "tecnologia", "hogar"]
            if busqueda.lower() not in categorias_validas:
                return productos, ids
            query = query_base + " WHERE LOWER(categoria) = LOWER(%s)"
            params = (busqueda,)
        elif metodo == "vendedor":
            query = query_base + " WHERE LOWER(vendedor_id) = LOWER(%s)"
            params = (busqueda,)
        else:
            return productos, ids

        resultados = Database_model._ejecutar_query(query, params, "all")

        if resultados and isinstance(resultados, list):
            for producto in resultados:
                if isinstance(producto, dict):
                    nombre_formato = f"{producto['nombre']} - ${producto['precio']:.2f} (Stock: {producto['stock']})"
                    productos.append(nombre_formato)
                    ids.append(str(producto["id"]))

        return productos, ids

    @staticmethod
    def obtener_producto(id: str) -> dict:
        """Obtiene la información completa de un producto"""
        query = """
            SELECT id, nombre, descripcion, calificacion, stock, precio, categoria, vendedor_id
            FROM productos 
            WHERE id = %s
        """

        resultado = Database_model._ejecutar_query(query, (id,), "one")

        if resultado and isinstance(resultado, dict):
            return resultado
        return {}

    @staticmethod
    def obtener_resenas_producto(producto_id: str) -> list[dict]:
        """Obtiene todas las reseñas de un producto específico"""
        query = """
            SELECT 
                pr.id,
                pr.calificacion,
                pr.comentario,
                pr.fecha_resena,
                c.nombre as cliente_nombre
            FROM productos_resenas pr
            JOIN clientes cl ON pr.cliente_id = cl.cuenta_id
            JOIN cuentas c ON cl.cuenta_id = c.id
            WHERE pr.producto_id = %s
            ORDER BY pr.fecha_resena DESC
        """

        resultados = Database_model._ejecutar_query(query, (producto_id,), "all")

        resenas_lista = []
        if resultados and isinstance(resultados, list):
            for resena in resultados:
                if isinstance(resena, dict):
                    resena_data = {
                        "id": str(resena["id"]),
                        "cliente_nombre": str(resena["cliente_nombre"]).strip(),
                        "calificacion": int(resena["calificacion"]),
                        "comentario": str(resena["comentario"] or ""),
                    }
                    resenas_lista.append(resena_data)

        return resenas_lista

    @staticmethod
    def actualizar_stock(cantidad: int, id: str) -> bool:
        """Actualiza el stock de un producto"""
        query = "UPDATE productos SET stock = %s WHERE id = %s"
        resultado = Database_model._ejecutar_query(query, (cantidad, id))
        return isinstance(resultado, int) and resultado > 0

    @staticmethod
    def guardar_pedido(id_usr: str, id_producto: str, cantidad: int) -> None:
        """Guarda un pedido individual (método legacy)"""
        # Legacy wrapper: delega a la API moderna sin imprimir mensajes.
        try:
            pedido_id = Database_model.crear_nuevo_pedido(id_usr)
            if not pedido_id:
                return

            # Intentar agregar producto; no imprimimos ni lanzamos errores hacia fuera
            Database_model.agregar_producto_a_pedido(pedido_id, id_producto, cantidad)
            return
        except Exception:
            # Silencioso: en caso de error, simplemente no hacer nada (compatibilidad backward)
            return

    @staticmethod
    def crear_nuevo_pedido(id_usr: str) -> str:
        """Crea un nuevo pedido en estado carrito"""
        try:
            # Obtener información del cliente
            query_cliente = """
                SELECT direccion_envio 
                FROM clientes 
                WHERE cuenta_id = %s
            """
            cliente_info = Database_model._ejecutar_query(
                query_cliente, (id_usr,), "one"
            )

            if not cliente_info or not isinstance(cliente_info, dict):
                raise Exception("Cliente no encontrado")

            # Generar ID del pedido
            query_ultimo_id = "SELECT id FROM pedidos ORDER BY id DESC LIMIT 1"
            ultimo_pedido = Database_model._ejecutar_query(query_ultimo_id, (), "one")

            if ultimo_pedido and isinstance(ultimo_pedido, dict):
                numero = int(ultimo_pedido["id"][3:]) + 1
                id_pedido = f"PED{str(numero).zfill(3)}"
            else:
                id_pedido = "PD001"

            # Crear pedido en estado carrito
            fecha_compra = datetime.now().strftime("%Y-%m-%d")

            query_pedido = """
                INSERT INTO pedidos (id, cliente_id, direccion_entrega, fecha_compra, estado_envio)
                VALUES (%s, %s, %s, %s, 'EN_CARRITO')
            """

            Database_model._ejecutar_query(
                query_pedido,
                (id_pedido, id_usr, cliente_info["direccion_envio"], fecha_compra),
            )

            return id_pedido

        except Exception as e:
            print(f">>> ERROR: No se pudo crear el pedido. {e}")
            return ""

    @staticmethod
    def agregar_producto_a_pedido(
        id_pedido: str, id_producto: str, cantidad: int
    ) -> bool:
        """Agrega un producto a un pedido existente"""
        try:
            # Verificar si el producto ya está en el pedido
            query_verificar = """
                SELECT cantidad FROM pedidos_productos 
                WHERE pedido_id = %s AND producto_id = %s
            """
            producto_existente = Database_model._ejecutar_query(
                query_verificar, (id_pedido, id_producto), "one"
            )

            if producto_existente and isinstance(producto_existente, dict):
                # Actualizar cantidad existente
                nueva_cantidad = int(producto_existente["cantidad"]) + cantidad

                query_actualizar = """
                    UPDATE pedidos_productos 
                    SET cantidad = %s
                    WHERE pedido_id = %s AND producto_id = %s
                """
                resultado = Database_model._ejecutar_query(
                    query_actualizar,
                    (nueva_cantidad, id_pedido, id_producto),
                )
            else:
                # Insertar nuevo producto
                query_insertar = """
                    INSERT INTO pedidos_productos (pedido_id, producto_id, cantidad)
                    VALUES (%s, %s, %s)
                """
                resultado = Database_model._ejecutar_query(
                    query_insertar,
                    (id_pedido, id_producto, cantidad),
                )

            return isinstance(resultado, int) and resultado > 0

        except Exception:
            return False

    @staticmethod
    def obtener_pedidos_usuario(id_usr: str) -> list[dict]:
        """Obtiene todos los pedidos de un usuario"""
        query_pedidos = """
            SELECT id, cliente_id, direccion_entrega, fecha_entrega, fecha_compra, estado_envio
            FROM pedidos 
            WHERE cliente_id = %s
            ORDER BY fecha_compra DESC
        """

        pedidos = Database_model._ejecutar_query(query_pedidos, (id_usr,), "all")

        if not pedidos or not isinstance(pedidos, list):
            return []

        pedidos_usuario = []

        for pedido in pedidos:
            if not isinstance(pedido, dict):
                continue

            # Obtener productos del pedido
            query_productos = """
                SELECT 
                    pp.producto_id as id,
                    p.nombre,
                    p.precio as precio,
                    pp.cantidad
                FROM pedidos_productos pp
                JOIN productos p ON pp.producto_id = p.id
                WHERE pp.pedido_id = %s
            """

            productos = Database_model._ejecutar_query(
                query_productos, (pedido["id"],), "all"
            )

            productos_lista = []
            if productos and isinstance(productos, list):
                for producto in productos:
                    if isinstance(producto, dict):
                        productos_lista.append(
                            {
                                "id": str(producto["id"]),
                                "nombre": str(producto["nombre"]),
                                "precio": float(producto["precio"]),
                                "cantidad": int(producto["cantidad"]),
                            }
                        )

            pedido_info = {
                "id": str(pedido["id"]),
                "cliente_id": str(pedido["cliente_id"]),
                "direccion_entrega": str(pedido["direccion_entrega"]),
                "fecha_entrega": pedido["fecha_entrega"].strftime("%d-%m-%Y")
                if pedido["fecha_entrega"]
                else "",
                "fecha_compra": pedido["fecha_compra"].strftime("%d-%m-%Y")
                if pedido["fecha_compra"]
                else "",
                "estado_envio": str(pedido["estado_envio"]),
                "productos": productos_lista,
            }

            pedidos_usuario.append(pedido_info)

        return pedidos_usuario

    @staticmethod
    def confirmar_pedido(id_pedido: str) -> bool:
        """Confirma un pedido usando el procedimiento almacenado como cliente"""
        try:
            query = "CALL sp_modificar_pedido(%s, %s, %s)"
            resultado = Database_model._ejecutar_query(
                query, (id_pedido, "EN_PROCESO", "cliente")
            )
            return resultado is not None
        except Exception as e:
            print(f">>> ERROR al confirmar pedido: {e}")
            return False

        except Exception:
            return False

    @staticmethod
    def crear_resena_producto(
        id_producto: str, id_usuario: str, calificacion: int, comentario: str
    ) -> bool:
        """Crea una nueva reseña para un producto"""
        try:
            print(">>> Creando reseña del producto...")

            # Generar ID de reseña
            query_ultimo_id = (
                "SELECT id FROM productos_resenas ORDER BY id DESC LIMIT 1"
            )
            ultima_resena = Database_model._ejecutar_query(query_ultimo_id, (), "one")

            if ultima_resena and isinstance(ultima_resena, dict):
                numero = int(ultima_resena["id"][3:]) + 1
                id_resena = f"REV{str(numero).zfill(3)}"
            else:
                id_resena = "REV001"

            # Insertar reseña
            query = """
                INSERT INTO productos_resenas (id, cliente_id, producto_id, calificacion, comentario)
                VALUES (%s, %s, %s, %s, %s)
            """

            resultado = Database_model._ejecutar_query(
                query, (id_resena, id_usuario, id_producto, calificacion, comentario)
            )

            return isinstance(resultado, int) and resultado > 0

        except Exception:
            return False

    @staticmethod
    def crear_producto_vendedor(
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: str,
        vendedor_id: str,
    ) -> bool:
        """Crea un nuevo producto para el vendedor"""
        try:
            # Generar ID del producto
            query_ultimo_id = "SELECT id FROM productos ORDER BY id DESC LIMIT 1"
            ultimo_producto = Database_model._ejecutar_query(query_ultimo_id, (), "one")

            if ultimo_producto and isinstance(ultimo_producto, dict):
                numero = int(ultimo_producto["id"][4:]) + 1
                nuevo_id = f"PROD{str(numero).zfill(3)}"
            else:
                nuevo_id = "PROD001"

            # Insertar producto
            query = """
                INSERT INTO productos (id, nombre, descripcion, stock, precio, categoria, vendedor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            resultado = Database_model._ejecutar_query(
                query,
                (nuevo_id, nombre, descripcion, stock, precio, categoria, vendedor_id),
            )

            return isinstance(resultado, int) and resultado > 0

        except Exception:
            return False

    @staticmethod
    def actualizar_producto_vendedor(
        producto_id: str,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: str,
    ) -> bool:
        """Actualiza un producto existente del vendedor"""
        try:
            query = """
                UPDATE productos 
                SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria = %s
                WHERE id = %s
            """

            resultado = Database_model._ejecutar_query(
                query, (nombre, descripcion, precio, stock, categoria, producto_id)
            )

            return isinstance(resultado, int) and resultado > 0

        except Exception:
            return False

    @staticmethod
    def eliminar_producto_vendedor(producto_id: str) -> bool:
        """Elimina un producto del vendedor"""
        try:
            # Verificar si el producto está en algún pedido
            query_check_pedidos = (
                "SELECT COUNT(*) as cnt FROM pedidos_productos WHERE producto_id = %s"
            )
            resultado_check = Database_model._ejecutar_query(
                query_check_pedidos, (producto_id,), "one"
            )
            if (
                resultado_check
                and isinstance(resultado_check, dict)
                and int(resultado_check.get("cnt", 0)) > 0
            ):
                # No se puede eliminar porque tiene pedidos asociados
                print(
                    f">>> No se puede eliminar el producto {producto_id}: existen pedidos asociados"
                )
                return False

            # Eliminar reseñas asociadas (si las hay)
            query_delete_resenas = (
                "DELETE FROM productos_resenas WHERE producto_id = %s"
            )
            Database_model._ejecutar_query(query_delete_resenas, (producto_id,))

            # Eliminar el producto
            query = "DELETE FROM productos WHERE id = %s"
            resultado = Database_model._ejecutar_query(query, (producto_id,))
            return isinstance(resultado, int) and resultado > 0

        except Exception:
            return False

    @staticmethod
    def obtener_pedidos_vendedor(vendedor_id: str) -> list[dict]:
        """Obtiene todos los pedidos que contienen productos del vendedor"""
        # Obtener pedidos con el total correspondiente sólo a los productos de este vendedor
        query = """
            SELECT p.id, p.cliente_id, p.direccion_entrega, p.fecha_entrega,
                   p.fecha_compra, p.estado_envio, c.nombre AS cliente_nombre,
                   SUM(pp.cantidad * pr.precio) AS total_vendedor
            FROM pedidos p
            JOIN pedidos_productos pp ON p.id = pp.pedido_id
            JOIN productos pr ON pp.producto_id = pr.id
            JOIN clientes cl ON p.cliente_id = cl.cuenta_id
            JOIN cuentas c ON cl.cuenta_id = c.id
            WHERE pr.vendedor_id = %s
            GROUP BY p.id, p.cliente_id, p.direccion_entrega, p.fecha_entrega, p.fecha_compra, p.estado_envio, c.nombre
            ORDER BY p.fecha_compra DESC
        """

        pedidos = Database_model._ejecutar_query(query, (vendedor_id,), "all")

        if not pedidos or not isinstance(pedidos, list):
            return []

        pedidos_vendedor = []
        for pedido in pedidos:
            if not isinstance(pedido, dict):
                continue

            # Obtener productos del pedido que pertenecen al vendedor
            query_productos = """
                SELECT 
                    pp.producto_id as id,
                    p.nombre,
                    p.precio as precio,
                    pp.cantidad
                FROM pedidos_productos pp
                JOIN productos p ON pp.producto_id = p.id
                WHERE pp.pedido_id = %s AND p.vendedor_id = %s
            """

            productos = Database_model._ejecutar_query(
                query_productos, (pedido["id"], vendedor_id), "all"
            )

            productos_lista = []
            if productos and isinstance(productos, list):
                for producto in productos:
                    if isinstance(producto, dict):
                        productos_lista.append(
                            {
                                "id": str(producto["id"]),
                                "nombre": str(producto["nombre"]),
                                "precio": float(producto["precio"]),
                                "cantidad": int(producto["cantidad"]),
                            }
                        )

            pedido_info = {
                "id": str(pedido["id"]),
                "cliente_id": str(pedido["cliente_id"]),
                "cliente_nombre": str(pedido.get("cliente_nombre") or ""),
                "direccion_entrega": str(pedido["direccion_entrega"]),
                "fecha_entrega": pedido["fecha_entrega"].strftime("%d-%m-%Y")
                if pedido["fecha_entrega"]
                else "",
                "fecha_compra": pedido["fecha_compra"].strftime("%d-%m-%Y")
                if pedido["fecha_compra"]
                else "",
                "estado_envio": str(pedido["estado_envio"]),
                "productos": productos_lista,
                "total_vendedor": float(pedido.get("total_vendedor") or 0.0),
            }

            pedidos_vendedor.append(pedido_info)

        return pedidos_vendedor

    @staticmethod
    def actualizar_estado_pedido(
        pedido_id: str, nuevo_estado: str, tipo_usuario: str
    ) -> bool:
        """Ahora usa el store procedure"""
        try:
            query = "CALL sp_modificar_pedido(%s, %s, %s)"
            resultado = Database_model._ejecutar_query(
                query, (pedido_id, nuevo_estado, tipo_usuario)
            )
            return resultado is not None
        except Exception as e:
            print(f">>> ERROR al actualizar estado del pedido: {e}")
            return False

    @staticmethod
    def obtener_estadisticas_vendedor(vendedor_id: str) -> dict:
        """Obtiene estadísticas básicas del vendedor optimizadas"""
        try:
            # Consulta consolidada para productos y pedidos
            query_consolidada = """
                SELECT 
                    -- Productos
                    (SELECT COUNT(*) FROM productos WHERE vendedor_id = %s) AS total_productos,
                    (SELECT COUNT(*) FROM productos WHERE vendedor_id = %s AND stock = 0) AS productos_sin_stock,
                    
                    -- Pedidos
                    COUNT(DISTINCT pp.pedido_id) AS total_pedidos,
                    COUNT(DISTINCT CASE WHEN p.estado_envio = 'EN_PROCESO' THEN p.id END) AS en_proceso,
                    COUNT(DISTINCT CASE WHEN p.estado_envio = 'ENVIADO' THEN p.id END) AS enviados,
                    COUNT(DISTINCT CASE WHEN p.estado_envio = 'EN_CARRITO' THEN p.id END) AS en_carrito,
                    COUNT(DISTINCT CASE WHEN p.estado_envio = 'ENTREGADO' THEN p.id END) AS entregados,
                    
                    -- Ventas
                    COALESCE(SUM(CASE WHEN p.estado_envio IN ('ENTREGADO', 'EN_PROCESO','ENVIADO') THEN pp.cantidad * pr.precio END), 0) AS ventas_totales
                FROM pedidos_productos pp
                JOIN productos pr ON pp.producto_id = pr.id
                JOIN pedidos p ON pp.pedido_id = p.id
                WHERE pr.vendedor_id = %s
            """

            # Top productos en consulta separada por eficiencia
            query_top_productos = """
                SELECT 
                    pr.id, 
                    pr.nombre, 
                    SUM(pp.cantidad) AS cantidad_vendida,
                    SUM(pp.cantidad * pr.precio) AS total_recaudado
                FROM pedidos_productos pp
                JOIN productos pr ON pp.producto_id = pr.id
                WHERE pr.vendedor_id = %s
                GROUP BY pr.id, pr.nombre
                ORDER BY cantidad_vendida DESC
                LIMIT 5
            """

            # Ejecutar consulta consolidada
            res_consolidado = Database_model._ejecutar_query(
                query_consolidada, (vendedor_id, vendedor_id, vendedor_id), "one"
            )

            # Procesar resultados consolidados
            stats = {
                "total_productos": res_consolidado.get("total_productos", 0),
                "productos_sin_stock": res_consolidado.get("productos_sin_stock", 0),
                "total_pedidos": res_consolidado.get("total_pedidos", 0),
                "pedidos_en_proceso": res_consolidado.get("en_proceso", 0),
                "pedidos_en_carrito": res_consolidado.get("en_carrito", 0),
                "pedidos_enviados": res_consolidado.get("enviados", 0),
                "pedidos_entregados": res_consolidado.get("entregados", 0),
                "ventas_totales": round(
                    float(res_consolidado.get("ventas_totales", 0.0)), 2
                ),
            }

            # Obtener top productos
            top_productos = Database_model._ejecutar_query(
                query_top_productos, (vendedor_id,), "all"
            )
            stats["productos_mas_vendidos"] = (
                [
                    {
                        "id": row["id"],
                        "nombre": row["nombre"],
                        "cantidad_vendida": row["cantidad_vendida"],
                        "total_recaudado": round(row["total_recaudado"], 2),
                    }
                    for row in top_productos
                ]
                if top_productos
                else []
            )

            return stats

        except Exception:
            return {}

    @staticmethod
    def cerrar_conexion() -> None:
        """Cierra la conexión a la base de datos"""
        try:
            if Database_model.connection and Database_model.connection.is_connected():
                Database_model.connection.close()
                print(">>> Conexión a MySQL cerrada")
        except Exception as e:
            print(f">>> ERROR al cerrar conexión: {e}")
