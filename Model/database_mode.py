import sqlite3
from datetime import datetime, timedelta
import os


class DB_model:
    DB_PATH = "datos_bd/ecommerce.db"

    def __init__(self):
        raise TypeError("Esta clase no debe ser instanciada")

    @staticmethod
    def conectar() -> bool:
        return os.path.exists(DB_model.DB_PATH)

    @staticmethod
    def guardar_pedido(id_usr: str, id_producto: str, cantidad: int) -> None:
        print(">>> Guardando pedido en la base de datos...")

    @staticmethod
    def validar_usuario(email: str, password: str) -> tuple[bool, str, str]:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()

                # Verificar en la tabla cuentas
                cursor.execute(
                    """
                    SELECT id FROM cuentas 
                    WHERE email = ? AND contrasena = ?
                """,
                    (email, password),
                )
                cuenta = cursor.fetchone()

                if not cuenta:
                    return (False, "Ninguno", "Ninguno")

                cuenta_id = cuenta[0]

                # Verificar si es cliente
                cursor.execute(
                    """
                    SELECT cuenta_id FROM clientes 
                    WHERE cuenta_id = ?
                """,
                    (cuenta_id,),
                )
                if cursor.fetchone():
                    return (True, "cliente", cuenta_id)

                # Verificar si es vendedor
                cursor.execute(
                    """
                    SELECT cuenta_id FROM vendedores 
                    WHERE cuenta_id = ?
                """,
                    (cuenta_id,),
                )
                if cursor.fetchone():
                    return (True, "vendedor", cuenta_id)

                return (False, "Ninguno", "Ninguno")

        except sqlite3.Error:
            return (False, "Ninguno", "Ninguno")

    @staticmethod
    def filtrar_productos(metodo: str, busqueda: str) -> tuple[list[str], list[str]]:
        productos = []
        ids = []
        metodos_validos = ["id", "nombre", "descripcion", "categoria", "vendedor"]

        if metodo not in metodos_validos:
            return (productos, ids)

        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()
                query = "SELECT id, nombre FROM productos"
                params = ()

                if metodo and busqueda:
                    if metodo == "vendedor":
                        query += " WHERE vendedor_id = ?"
                    else:
                        query += f" WHERE {metodo} LIKE ?"
                    params = (busqueda.lower() if metodo != "vendedor" else busqueda,)

                cursor.execute(query, params)
                resultados = cursor.fetchall()

                productos = [res[1] for res in resultados]
                ids = [res[0] for res in resultados]

        except sqlite3.Error:
            pass

        return (productos, ids)

    @staticmethod
    def obtener_producto(id: str) -> dict:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM productos 
                    WHERE id = ?
                """,
                    (id,),
                )
                producto = cursor.fetchone()

                if producto:
                    column_names = [desc[0] for desc in cursor.description]
                    return dict(zip(column_names, producto))
        except sqlite3.Error:
            pass
        return {}

    @staticmethod
    def actualizar_stock(cantidad: int, id: str) -> bool:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE productos 
                    SET stock = ? 
                    WHERE id = ?
                """,
                    (cantidad, id),
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @staticmethod
    def crear_nuevo_pedido(id_usr: str) -> str:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()

                # Obtener dirección del cliente
                cursor.execute(
                    """
                    SELECT direccion_envio FROM clientes 
                    WHERE cuenta_id = ?
                """,
                    (id_usr,),
                )
                direccion = cursor.fetchone()[0]

                # Generar nuevo ID de pedido
                cursor.execute("SELECT MAX(id) FROM pedidos")
                ultimo_id = cursor.fetchone()[0] or "PD000"
                num = int(ultimo_id[2:]) + 1
                nuevo_id = f"PD{num:03d}"

                # Insertar nuevo pedido
                fecha_compra = datetime.now().strftime("%d-%m-%Y")
                cursor.execute(
                    """
                    INSERT INTO pedidos (
                        id, cliente_id, direccion_entrega, 
                        fecha_entrega, fecha_compra, estado_envio
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (nuevo_id, id_usr, direccion, "", fecha_compra, "EN_PROCESO"),
                )
                conn.commit()
                return nuevo_id

        except sqlite3.Error:
            return ""

    @staticmethod
    def agregar_producto_a_pedido(
        id_pedido: str, id_producto: str, cantidad: int
    ) -> bool:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO pedidos_productos (
                        pedido_id, producto_id, cantidad
                    ) VALUES (?, ?, ?)
                """,
                    (id_pedido, id_producto, cantidad),
                )
                conn.commit()
                return True
        except sqlite3.Error:
            return False

    @staticmethod
    def obtener_pedidos_usuario(id_usr: str) -> list[dict]:
        pedidos = []
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()

                # Obtener pedidos del usuario
                cursor.execute(
                    """
                    SELECT * FROM pedidos 
                    WHERE cliente_id = ?
                """,
                    (id_usr,),
                )
                column_names = [desc[0] for desc in cursor.description]
                pedidos_raw = cursor.fetchall()

                for pedido in pedidos_raw:
                    pedido_dict = dict(zip(column_names, pedido))
                    pedido_id = pedido_dict["id"]

                    # Obtener productos del pedido
                    cursor.execute(
                        """
                        SELECT pp.producto_id, pp.cantidad, p.nombre, p.precio
                        FROM pedidos_productos pp
                        JOIN productos p ON pp.producto_id = p.id
                        WHERE pp.pedido_id = ?
                    """,
                        (pedido_id,),
                    )
                    productos = []
                    for prod in cursor.fetchall():
                        productos.append(
                            {
                                "id": prod[0],
                                "nombre": prod[2],
                                "precio": prod[3],
                                "cantidad": prod[1],
                            }
                        )

                    pedido_dict["productos"] = productos
                    pedidos.append(pedido_dict)

        except sqlite3.Error:
            pass

        return pedidos

    @staticmethod
    def confirmar_pedido(id_pedido: str) -> bool:
        try:
            with sqlite3.connect(DB_model.DB_PATH) as conn:
                cursor = conn.cursor()
                fecha_entrega = (datetime.now() + timedelta(days=5)).strftime(
                    "%d-%m-%Y"
                )

                cursor.execute(
                    """
                    UPDATE pedidos 
                    SET estado_envio = 'EN_PROCESO', 
                        fecha_entrega = ?
                    WHERE id = ?
                """,
                    (fecha_entrega, id_pedido),
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
