from Controller.Controllers import SystemController
from Controller.InputManager import InputManager
import sys


def inicializar() -> None:
    print("=== SISTEMA INICIALIZADO CORRECTAMENTE ===")
    SystemController.conectar_database()


def comprar(id_usr, product_info: dict) -> bool:
    if not product_info:
        print(">>> ERROR: No se pudo obtener la información del producto")
        return False

    stock: int = product_info.get("stock", 0)
    id: str = product_info.get("id", "")
    if stock <= 0:
        print(">>> ERROR: El producto no está disponible en stock")
        return False

    cantidad: int = 0
    while cantidad <= 0 or cantidad > stock:
        cantidad = InputManager.leer_entero_positivo(
            "¿Cuántas unidades desea comprar? (Máximo disponible: {})".format(stock)
        )

        if cantidad > stock:
            print(
                f">>> ERROR: Solo hay {stock} unidades disponibles. Por favor, ingrese una cantidad válida."
            )

    tarjeta: str = ""

    while (not tarjeta.isdigit()) or len(tarjeta) != 10:
        tarjeta = InputManager.leer_texto_no_vacio(
            "Ingrese el número de su tarjeta de crédito (10 dígitos): "
        )
        if not tarjeta.isdigit() or len(tarjeta) != 10:
            print(">>> ERROR: El número de tarjeta debe ser un número de 10 dígitos")

    confirmacion = InputManager.leer_confirmacion(
        "¿Desea escribir una reseña del producto? (S/N): "
    )

    if confirmacion:
        escribir_resena(product_info["nombre"], id, id_usr)

    if SystemController.actualizar_stock(stock - cantidad, id):
        print(
            f">>> Compra de {cantidad} unidades del producto {product_info['nombre']} realizada con éxito"
        )
        SystemController.guardar_pedido(id_usr, id, cantidad)
        return True
    return False


def iniciar_carrito_compras(id_usr: str) -> None:
    print("\n=== CARRITO DE COMPRAS ===")

    # Crear un nuevo pedido (carrito)
    id_pedido = SystemController.crear_nuevo_pedido(id_usr)
    print(f">>> Carrito creado con ID: {id_pedido}")

    while True:
        opciones = [
            "Agregar producto al carrito",
            "Ver carrito actual",
            "Confirmar compra",
            "Cancelar compra",
        ]

        seleccion = InputManager.leer_opcion_menu(opciones, "OPCIONES DEL CARRITO")

        match seleccion:
            case 1:
                agregar_producto_al_carrito(id_pedido)
            case 2:
                mostrar_carrito(id_pedido, id_usr)
            case 3:
                if confirmar_compra_carrito(id_pedido, id_usr):
                    print(">>> ¡Compra confirmada exitosamente!")

                    return
            case 4:
                print(">>> Compra cancelada")
                return


def agregar_producto_al_carrito(id_pedido: str) -> None:
    print("\n--- Seleccionar Producto ---")

    # Mostrar todos los productos
    productos, ids = SystemController.mostrar_productos("", "")

    if not productos:
        print(">>> No hay productos disponibles")
        InputManager.pausar()
        return

    print("\n=== PRODUCTOS DISPONIBLES ===")
    for i, producto in enumerate(productos):
        print(f"  {i + 1}. {producto}")

    try:
        seleccion = InputManager.leer_entero(
            f"Seleccione un producto (1-{len(productos)}): "
        )
        if seleccion < 1 or seleccion > len(productos):
            print(">>> ERROR: Selección inválida")
            return

        producto_id = ids[seleccion - 1]
        producto_info = SystemController.mostrar_producto(producto_id)

        if not producto_info:
            print(">>> ERROR: No se pudo obtener información del producto")
            return

        stock = producto_info["stock"]
        print(f"Stock disponible: {stock}")

        cantidad = InputManager.leer_entero_positivo("Ingrese la cantidad deseada: ")

        if cantidad == 0:
            print(">>> ERROR: La cantidad debe ser mayor a 0")
            return

        if cantidad > stock:
            print(f">>> ERROR: Solo hay {stock} unidades disponibles")
            return

        # Agregar al carrito
        if SystemController.agregar_producto_a_pedido(id_pedido, producto_id, cantidad):
            print(
                f">>> Producto agregado al carrito: {cantidad} x {producto_info['nombre']}"
            )
        else:
            print(">>> ERROR: No se pudo agregar el producto al carrito")

    except Exception as e:
        print(f">>> ERROR: {e}")


def mostrar_carrito(id_pedido: str, id_usr: str) -> None:
    pedidos = SystemController.obtener_pedidos_usuario(id_usr)

    carrito = None
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            carrito = pedido
            break

    if not carrito or not carrito["productos"]:
        print(">>> El carrito está vacío")
        InputManager.pausar()
        return

    print(f"\n=== CARRITO {id_pedido} ===")
    total = 0

    for producto in carrito["productos"]:
        subtotal = producto["precio"] * producto["cantidad"]
        print(f"  - {producto['nombre']} x {producto['cantidad']} = ${subtotal:.2f}")
        total += subtotal

    print(f"\nTOTAL: ${total:.2f}")
    InputManager.pausar()


# Funcion para escribir reseñas
def escribir_resena(nombre: str, id_producto: str, id_usuario: str) -> None:
    calificacion = 10
    print(f"\n=== Reseña para el producto {nombre} ===")
    while calificacion > 5:
        calificacion = InputManager.leer_entero_positivo(
            "Ingrese la calificación (1-5): "
        )
        if calificacion > 5:
            print(">>> ERROR: La calificación debe ser entre 1 y 5")

    comentario = InputManager.leer_texto_no_vacio("Ingrese su comentario: ")

    if SystemController.crear_resena_producto(
        id_producto, id_usuario, calificacion, comentario
    ):
        print(">>> Reseña guardada exitosamente")
    else:
        print(">>> ERROR: No se pudo guardar la reseña")


# Función para mostrar reseñas de un producto
def mostrar_resenas_producto(producto_id: str, nombre_producto: str) -> None:
    """Muestra todas las reseñas de un producto específico"""
    resenas: list[dict] = SystemController.obtener_resenas_producto(producto_id)

    if not resenas:
        print(f"\n>>> No hay reseñas disponibles para '{nombre_producto}'")
        return

    print(f"\n=== RESEÑAS DE '{nombre_producto.upper()}' ===")

    # Calcular calificación promedio
    total_calificaciones: int = sum(resena["calificacion"] for resena in resenas)
    promedio: float = total_calificaciones / len(resenas)

    # Mostrar estadísticas
    print(f"📊 Total de reseñas: {len(resenas)}")
    print(f"⭐ Calificación promedio: {promedio:.1f}/5.0")
    print("-" * 60)

    # Mostrar cada reseña
    for i, resena in enumerate(resenas, 1):
        estrellas: str = "⭐" * resena["calificacion"] + "☆" * (
            5 - resena["calificacion"]
        )

        print(f"\n#{i} - {resena['cliente_nombre']}")
        print(f"   {estrellas} ({resena['calificacion']}/5)")
        print(f'   "{resena["comentario"]}"')

        if i < len(resenas):
            print("-" * 40)

    print("-" * 60)


def confirmar_compra_carrito(id_pedido: str, id_usr: str) -> bool:
    # Mostrar resumen final
    mostrar_carrito(id_pedido, id_usr)

    confirmacion = InputManager.leer_confirmacion("¿Confirmar la compra? (S/N): ")

    if not confirmacion:
        return False

    # Solicitar información de pago
    tarjeta = ""
    while not tarjeta.isdigit() or len(tarjeta) != 10:
        tarjeta = InputManager.leer_texto_no_vacio(
            "Ingrese el número de su tarjeta de crédito (10 dígitos): "
        )
        if not tarjeta.isdigit() or len(tarjeta) != 10:
            print(">>> ERROR: El número de tarjeta debe ser un número de 10 dígitos")

    # Actualizar stock de todos los productos y confirmar pedido
    pedidos = SystemController.obtener_pedidos_usuario(id_usr)
    carrito = None
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            carrito = pedido
            break

    if not carrito:
        print(">>> ERROR: No se encontró el carrito")
        return False

    confirmacion = InputManager.leer_confirmacion(
        "¿Desea escribir una reseña de cada producto? (S/N): "
    )

    # Actualizar stock de cada producto
    for producto in carrito["productos"]:
        producto_info = SystemController.mostrar_producto(producto["id"])

        if confirmacion:
            escribir_resena(producto_info["nombre"], producto["id"], id_usr)

        nuevo_stock = producto_info["stock"] - producto["cantidad"]

        if not SystemController.actualizar_stock(nuevo_stock, producto["id"]):
            print(f">>> ERROR: No se pudo actualizar el stock de {producto['nombre']}")
            return False

    # Confirmar el pedido
    if SystemController.confirmar_pedido(id_pedido):
        return True
    else:
        print(">>> ERROR: No se pudo confirmar el pedido")
        return False


def navegar(id_usr, productos: list[str], ids: list[str]) -> None:
    seleccion = InputManager.leer_opcion_menu(productos, "SELECCIONE UN PRODUCTO")
    product_info = SystemController.mostrar_producto(ids[seleccion - 1])

    # Mostrar opciones adicionales después de ver el producto
    while True:
        opciones_producto: list[str] = [
            "Ver reseñas del producto",
            "Realizar compra",
            "Volver al menú anterior",
        ]

        opcion: int = InputManager.leer_opcion_menu(
            opciones_producto, "OPCIONES DEL PRODUCTO"
        )

        match opcion:
            case 1:
                mostrar_resenas_producto(
                    ids[seleccion - 1], product_info.get("nombre", "Producto")
                )
                InputManager.pausar()
            case 2:
                compra_exitosa: bool = comprar(id_usr, product_info)
                if compra_exitosa:
                    return
                else:
                    print(">>> ERROR: No se pudo completar la compra")
                    InputManager.pausar()
            case 3:
                return


def gestionar_pedidos_cliente(id_usr: str):
    """Permite al cliente gestionar sus pedidos"""
    while True:
        opciones = [
            "Ver mis pedidos",
            "Ver carritos pendientes",
            "Crear nuevo carrito de compras",
            "Volver al menú principal",
        ]

        seleccion = InputManager.leer_opcion_menu(opciones, "GESTIÓN DE PEDIDOS")

        match seleccion:
            case 1:
                ver_pedidos_cliente(id_usr)
            case 2:
                gestionar_carritos_pendientes(id_usr)
            case 3:
                iniciar_carrito_compras(id_usr)
            case 4:
                return


def gestionar_carritos_pendientes(id_usr: str):
    """Permite al cliente continuar con carritos pendientes o crearlos nuevos"""
    pedidos = SystemController.obtener_pedidos_usuario(id_usr)

    # Filtrar solo los carritos (estado EN_CARRITO)
    carritos_pendientes = [p for p in pedidos if p["estado_envio"] == "EN_CARRITO"]

    if not carritos_pendientes:
        print(">>> No tiene carritos pendientes")
        InputManager.pausar()
        return

    print("\n=== CARRITOS PENDIENTES ===")
    for i, carrito in enumerate(carritos_pendientes):
        total_productos = len(carrito["productos"])
        total_precio = sum(p["precio"] * p["cantidad"] for p in carrito["productos"])

        print(
            f"  {i + 1}. Carrito {carrito['id']} - {total_productos} productos - Total: ${total_precio:.2f}"
        )
        if carrito["productos"]:
            print("     Productos:")
            for producto in carrito["productos"]:
                print(f"       - {producto['nombre']} x {producto['cantidad']}")
        print()

    print(f"  {len(carritos_pendientes) + 1}. Volver")

    try:
        seleccion = InputManager.leer_entero(
            f"Seleccione un carrito para continuar (1-{len(carritos_pendientes) + 1}): "
        )

        if seleccion == len(carritos_pendientes) + 1:
            return

        if seleccion < 1 or seleccion > len(carritos_pendientes):
            print(">>> ERROR: Selección inválida")
            return

        carrito_seleccionado = carritos_pendientes[seleccion - 1]
        continuar_carrito_existente(carrito_seleccionado["id"], id_usr)

    except Exception as e:
        print(f">>> ERROR: {e}")


def continuar_carrito_existente(id_pedido: str, id_usr: str):
    """Continúa con un carrito existente"""
    print(f"\n=== CONTINUANDO CARRITO {id_pedido} ===")

    while True:
        opciones = [
            "Agregar más productos",
            "Ver carrito actual",
            "Confirmar compra",
            "Cancelar y volver",
        ]

        seleccion = InputManager.leer_opcion_menu(opciones, "OPCIONES DEL CARRITO")

        match seleccion:
            case 1:
                agregar_producto_al_carrito(id_pedido)
            case 2:
                mostrar_carrito(id_pedido, id_usr)
            case 3:
                if confirmar_compra_carrito(id_pedido, id_usr):
                    print(">>> ¡Compra confirmada exitosamente!")
                    return
            case 4:
                return


def ver_pedidos_cliente(id_usr: str):
    """Muestra todos los pedidos del cliente"""
    pedidos = SystemController.obtener_pedidos_usuario(id_usr)

    if not pedidos:
        print(">>> No tiene pedidos registrados")
        InputManager.pausar()
        return

    # Separar carritos y pedidos procesados
    carritos = [p for p in pedidos if p["estado_envio"] == "EN_CARRITO"]
    pedidos_procesados = [p for p in pedidos if p["estado_envio"] != "EN_CARRITO"]

    print("\n=== HISTORIAL DE PEDIDOS ===")

    if carritos:
        print("\n--- CARRITOS PENDIENTES ---")
        for carrito in carritos:
            total_productos = len(carrito["productos"])
            total_precio = sum(
                p["precio"] * p["cantidad"] for p in carrito["productos"]
            )

            print(
                f"  🛒 Carrito {carrito['id']} - {total_productos} productos - Total: ${total_precio:.2f}"
            )
            if carrito["productos"]:
                print("     Productos:")
                for producto in carrito["productos"]:
                    print(f"       - {producto['nombre']} x {producto['cantidad']}")
            print()

    if pedidos_procesados:
        print("\n--- PEDIDOS CONFIRMADOS ---")
        for pedido in pedidos_procesados:
            estado = pedido["estado_envio"]
            fecha_compra = pedido["fecha_compra"]
            fecha_entrega = (
                pedido["fecha_entrega"] if pedido["fecha_entrega"] else "Pendiente"
            )
            total_productos = len(pedido["productos"])
            total_precio = sum(p["precio"] * p["cantidad"] for p in pedido["productos"])

            print(f"   Pedido {pedido['id']} - {estado}")
            print(f"     Fecha compra: {fecha_compra} | Fecha entrega: {fecha_entrega}")
            print(f"     {total_productos} productos - Total: ${total_precio:.2f}")

            if pedido["productos"]:
                print("     Productos:")
                for producto in pedido["productos"]:
                    print(f"       - {producto['nombre']} x {producto['cantidad']}")
            print()

    InputManager.pausar()


def buscar(id_usr: str = "") -> None:
    opciones: list[str] = [
        "ID del producto",
        "Nombre del producto",
        "Categoría",
        "ID del vendedor",
    ]
    seleccion: int = InputManager.leer_opcion_menu(opciones, "MÉTODO DE BÚSQUEDA")
    busqueda: str = ""
    productos: list[str] = []
    ids: list[str] = []
    mensaje_error: str = ""
    confirmacion: bool = False
    match seleccion:
        case 1:
            busqueda = InputManager.leer_texto_no_vacio("Ingrese el ID del producto:")
            productos, ids = SystemController.mostrar_productos("id", busqueda)
            mensaje_error = f">>> No existe un producto con el ID: {busqueda}"
        case 2:
            busqueda = InputManager.leer_texto_no_vacio(
                "Ingrese el nombre del producto:"
            )
            productos, ids = SystemController.mostrar_productos("nombre", busqueda)
            mensaje_error = f">>> No existe un producto con el nombre: {busqueda}"
        case 3:
            busqueda = InputManager.leer_texto_no_vacio(
                "Ingrese la categoría [juguetes, ropa, tecnología, hogar]:"
            )
            productos, ids = SystemController.mostrar_productos("categoria", busqueda)
            mensaje_error = f">>> No existe la categoría: {busqueda}"
        case 4:
            busqueda = InputManager.leer_texto_no_vacio("Ingrese el ID del vendedor:")
            productos, ids = SystemController.mostrar_productos("vendedor", busqueda)
            mensaje_error = f">>> No existe el vendedor con el ID: {busqueda}"
    if len(productos) == 0:
        print(mensaje_error)
    else:
        print("\n=== PRODUCTOS ENCONTRADOS ===")
        for i, producto in enumerate(productos):
            print(f"  {i + 1}. {producto}")

        confirmacion = InputManager.leer_confirmacion(
            "¿Desea ver los detalles de algún producto? (S/N)"
        )
    if confirmacion:
        navegar(id_usr, productos, ids)
    else:
        InputManager.pausar()


def menu_cliente(id: str) -> None:
    print("=== BIENVENIDO CLIENTE ===")
    opciones: list[str] = [
        "Ver todos los productos",
        "Buscar productos específicos",
        "Gestionar mis pedidos",
        "Cerrar sesión",
        "Salir del sistema",
    ]
    seleccion: int = InputManager.leer_opcion_menu(opciones, "MENÚ PRINCIPAL")

    productos: list[str] = []
    ids: list[str] = []
    match seleccion:
        case 1:
            confirmacion: bool = False
            # Mostrar todos los productos usando el método existente con parámetros vacíos
            productos, ids = SystemController.mostrar_productos("", "")
            if len(productos) == 0:
                print(">>> No hay productos disponibles en el sistema")
            else:
                print("\n=== TODOS LOS PRODUCTOS ===")
                for i, producto in enumerate(productos):
                    print(f"  {i + 1}. {producto}")
            confirmacion = InputManager.leer_confirmacion(
                "¿Desea ver los detalles de algún producto? (S/N)"
            )
            if confirmacion:
                navegar(id, productos, ids)
            else:
                InputManager.pausar()

        case 2:
            buscar(id)
        case 3:
            gestionar_pedidos_cliente(id)
        case 4:
            sistema()
        case 5:
            print("\n=== CERRANDO SISTEMA ===")
            sys.exit(0)
    menu_cliente(id)


def gestionar_productos(id_vendedor: str) -> None:
    """Permite al vendedor gestionar sus productos"""
    while True:
        opciones: list[str] = [
            "Agregar nuevo producto",
            "Ver mis productos",
            "Editar producto existente",
            "Eliminar producto",
            "Volver al menú principal",
        ]

        seleccion: int = InputManager.leer_opcion_menu(opciones, "GESTIÓN DE PRODUCTOS")

        match seleccion:
            case 1:
                agregar_producto_vendedor(id_vendedor)
            case 2:
                ver_productos_vendedor(id_vendedor)
            case 3:
                editar_producto_vendedor(id_vendedor)
            case 4:
                eliminar_producto_vendedor(id_vendedor)
            case 5:
                return


def agregar_producto_vendedor(id_vendedor: str) -> None:
    """Permite al vendedor agregar un nuevo producto"""
    print("\n=== AGREGAR NUEVO PRODUCTO ===")

    nombre: str = InputManager.leer_texto_no_vacio("Ingrese el nombre del producto: ")
    descripcion: str = InputManager.leer_texto_no_vacio(
        "Ingrese la descripción del producto: "
    )

    precio: float = 0.0
    while precio <= 0:
        precio = InputManager.leer_decimal_positivo("Ingrese el precio del producto: $")
        if precio <= 0:
            print(">>> ERROR: El precio debe ser mayor a 0")

    stock: int = 0
    while stock < 0:
        stock = InputManager.leer_entero("Ingrese la cantidad en stock: ")
        if stock < 0:
            print(">>> ERROR: El stock no puede ser negativo")

    print("\nCategorías disponibles:")
    categorias: list[str] = ["juguetes", "ropa", "tecnologia", "hogar"]
    for i, categoria in enumerate(categorias):
        print(f"  {i + 1}. {categoria.capitalize()}")

    categoria_seleccionada: str = ""
    while categoria_seleccionada not in categorias:
        try:
            opcion: int = InputManager.leer_entero_positivo(
                f"Seleccione una categoría (1-{len(categorias)}): "
            )
            if 1 <= opcion <= len(categorias):
                categoria_seleccionada = categorias[opcion - 1]
            else:
                print(">>> ERROR: Selección inválida")
        except Exception:
            print(">>> ERROR: Ingrese un número válido")

    # Confirmar creación
    print("\n=== CONFIRMACIÓN ===")
    print(f"Nombre: {nombre}")
    print(f"Descripción: {descripcion}")
    print(f"Precio: ${precio:.2f}")
    print(f"Stock: {stock}")
    print(f"Categoría: {categoria_seleccionada.capitalize()}")

    confirmacion: bool = InputManager.leer_confirmacion(
        "¿Confirma la creación del producto? (S/N): "
    )

    if confirmacion:
        resultado: bool = SystemController.crear_producto_vendedor(
            nombre, descripcion, precio, stock, categoria_seleccionada, id_vendedor
        )

        if resultado:
            print(">>> Producto creado exitosamente")
        else:
            print(">>> ERROR: No se pudo crear el producto")
    else:
        print(">>> Creación cancelada")

    InputManager.pausar()


def ver_productos_vendedor(id_vendedor: str) -> None:
    """Muestra todos los productos del vendedor"""
    productos: list[str] = []
    ids: list[str] = []
    productos, ids = SystemController.mostrar_productos_vendedor(id_vendedor)

    if len(productos) == 0:
        print(">>> No cuenta con ningún producto registrado")
    else:
        print("\n=== SUS PRODUCTOS ===")
        for i, producto in enumerate(productos):
            print(f"  {i + 1}. {producto}")

        # Mostrar detalles de un producto específico
        ver_detalles: bool = InputManager.leer_confirmacion(
            "¿Desea ver los detalles de algún producto? (S/N): "
        )

        if ver_detalles:
            try:
                seleccion: int = InputManager.leer_entero(
                    f"Seleccione un producto (1-{len(productos)}): "
                )
                if 1 <= seleccion <= len(productos):
                    producto_id: str = ids[seleccion - 1]
                    producto_info: dict = SystemController.mostrar_producto(producto_id)

                    # Ofrecer ver reseñas después de mostrar detalles
                    ver_resenas: bool = InputManager.leer_confirmacion(
                        "¿Desea ver las reseñas de este producto? (S/N): "
                    )

                    if ver_resenas:
                        mostrar_resenas_producto(
                            producto_id, producto_info.get("nombre", "Producto")
                        )
                else:
                    print(">>> ERROR: Selección inválida")
            except Exception:
                print(">>> ERROR: Selección inválida")

    InputManager.pausar()


def editar_producto_vendedor(id_vendedor: str) -> None:
    """Permite al vendedor editar un producto existente"""
    productos: list[str] = []
    ids: list[str] = []
    productos, ids = SystemController.mostrar_productos_vendedor(id_vendedor)

    if len(productos) == 0:
        print(">>> No cuenta con ningún producto registrado")
        InputManager.pausar()
        return

    print("\n=== EDITAR PRODUCTO ===")
    print("Seleccione el producto que desea editar:")
    for i, producto in enumerate(productos):
        print(f"  {i + 1}. {producto}")

    try:
        seleccion: int = InputManager.leer_entero(
            f"Seleccione un producto (1-{len(productos)}): "
        )
        if seleccion < 1 or seleccion > len(productos):
            print(">>> ERROR: Selección inválida")
            InputManager.pausar()
            return

        producto_id: str = ids[seleccion - 1]
        producto_actual: dict = SystemController.mostrar_producto(producto_id)

        if not producto_actual:
            print(">>> ERROR: No se pudo obtener la información del producto")
            InputManager.pausar()
            return

        print("\n=== DATOS ACTUALES ===")
        # Los detalles ya se muestran por mostrar_producto

        print("\n=== NUEVOS DATOS (presione Enter para mantener el valor actual) ===")

        nombre: str = InputManager.leer_texto_opcional(
            f"Nuevo nombre [{producto_actual['nombre']}]: "
        )
        if not nombre:
            nombre = producto_actual["nombre"]

        descripcion: str = InputManager.leer_texto_opcional(
            f"Nueva descripción [{producto_actual['descripcion']}]: "
        )
        if not descripcion:
            descripcion = producto_actual["descripcion"]

        precio_str: str = InputManager.leer_texto_opcional(
            f"Nuevo precio [{producto_actual['precio']}]: $"
        )
        precio: float = float(precio_str) if precio_str else producto_actual["precio"]

        stock_str: str = InputManager.leer_texto_opcional(
            f"Nuevo stock [{producto_actual['stock']}]: "
        )
        stock: int = int(stock_str) if stock_str else producto_actual["stock"]

        print(f"Categoría actual: {producto_actual['categoria']}")
        categorias: list[str] = ["juguetes", "ropa", "tecnologia", "hogar"]
        print("Categorías disponibles:")
        for i, cat in enumerate(categorias):
            print(f"  {i + 1}. {cat.capitalize()}")

        categoria_str: str = InputManager.leer_texto_opcional(
            "Nueva categoría (número o presione Enter para mantener): "
        )
        categoria: str = producto_actual["categoria"]
        if categoria_str:
            try:
                cat_index: int = int(categoria_str) - 1
                if 0 <= cat_index < len(categorias):
                    categoria = categorias[cat_index]
            except Exception:
                print(">>> Manteniendo categoría actual")  # Confirmar cambios
        confirmacion: bool = InputManager.leer_confirmacion(
            "¿Confirma los cambios? (S/N): "
        )

        if confirmacion:
            resultado: bool = SystemController.actualizar_producto_vendedor(
                producto_id, nombre, descripcion, precio, stock, categoria
            )

            if resultado:
                print(">>> Producto actualizado exitosamente")
            else:
                print(">>> ERROR: No se pudo actualizar el producto")
        else:
            print(">>> Actualización cancelada")

    except Exception as e:
        print(f">>> ERROR: {e}")

    InputManager.pausar()


def eliminar_producto_vendedor(id_vendedor: str) -> None:
    """Permite al vendedor eliminar un producto"""
    productos: list[str] = []
    ids: list[str] = []
    productos, ids = SystemController.mostrar_productos_vendedor(id_vendedor)

    if len(productos) == 0:
        print(">>> No cuenta con ningún producto registrado")
        InputManager.pausar()
        return

    print("\n=== ELIMINAR PRODUCTO ===")
    print("Seleccione el producto que desea eliminar:")
    for i, producto in enumerate(productos):
        print(f"  {i + 1}. {producto}")

    try:
        seleccion: int = InputManager.leer_entero(
            f"Seleccione un producto (1-{len(productos)}): "
        )
        if seleccion < 1 or seleccion > len(productos):
            print(">>> ERROR: Selección inválida")
            InputManager.pausar()
            return

        producto_id: str = ids[seleccion - 1]
        producto_info: dict = SystemController.mostrar_producto(producto_id)

        print("\n>>> ADVERTENCIA: Esta acción no se puede deshacer <<<")
        confirmacion: bool = InputManager.leer_confirmacion(
            f"¿Está seguro de que desea eliminar '{producto_info['nombre']}'? (S/N): "
        )

        if confirmacion:
            resultado: bool = SystemController.eliminar_producto_vendedor(producto_id)

            if resultado:
                print(">>> Producto eliminado exitosamente")
            else:
                print(">>> ERROR: No se pudo eliminar el producto")
        else:
            print(">>> Eliminación cancelada")

    except Exception as e:
        print(f">>> ERROR: {e}")

    InputManager.pausar()


def gestionar_pedidos_vendedor(id_vendedor: str) -> None:
    """Permite al vendedor gestionar sus pedidos"""
    while True:
        opciones: list[str] = [
            "Ver todos mis pedidos",
            "Actualizar estado de pedido",
            "Ver estadísticas de ventas",
            "Volver al menú principal",
        ]

        seleccion: int = InputManager.leer_opcion_menu(opciones, "GESTIÓN DE PEDIDOS")

        match seleccion:
            case 1:
                ver_pedidos_vendedor(id_vendedor)
            case 2:
                actualizar_estado_pedido_vendedor(id_vendedor)
            case 3:
                ver_estadisticas_vendedor(id_vendedor)
            case 4:
                return


def ver_pedidos_vendedor(id_vendedor: str) -> None:
    """Muestra todos los pedidos del vendedor"""
    pedidos: list[dict] = SystemController.obtener_pedidos_vendedor(id_vendedor)

    if not pedidos:
        print(">>> No tiene pedidos registrados")
        InputManager.pausar()
        return

    print("\n=== MIS PEDIDOS ===")
    for pedido in pedidos:
        estado: str = pedido["estado_envio"]
        fecha_compra: str = pedido["fecha_compra"]
        fecha_entrega: str = (
            pedido["fecha_entrega"] if pedido["fecha_entrega"] else "Pendiente"
        )
        cliente_nombre: str = pedido["cliente_nombre"]
        total: float = pedido["total_vendedor"]

        print(f"\nPedido {pedido['id']} - {estado}")
        print(f"   Cliente: {cliente_nombre}")
        print(f"   Fecha compra: {fecha_compra} | Fecha entrega: {fecha_entrega}")
        print(f"   Dirección: {pedido['direccion_entrega']}")
        print(f"   Total: ${total:.2f}")

        if pedido["productos"]:
            print("   Productos:")
            for producto in pedido["productos"]:
                subtotal: float = producto["precio"] * producto["cantidad"]
                print(
                    f"     - {producto['nombre']} x {producto['cantidad']} = ${subtotal:.2f}"
                )
        print("-" * 50)

    InputManager.pausar()


def actualizar_estado_pedido_vendedor(id_vendedor: str) -> None:
    """Permite al vendedor actualizar el estado de un pedido"""
    pedidos: list[dict] = SystemController.obtener_pedidos_vendedor(id_vendedor)

    if not pedidos:
        print(">>> No tiene pedidos registrados")
        InputManager.pausar()
        return

    # Filtrar pedidos que se pueden actualizar (no entregados)
    pedidos_actualizables: list[dict] = [
        p for p in pedidos if p["estado_envio"] != "ENTREGADO"
    ]

    if not pedidos_actualizables:
        print(">>> No tiene pedidos pendientes por actualizar")
        InputManager.pausar()
        return

    print("\n=== ACTUALIZAR ESTADO DE PEDIDO ===")
    print("Pedidos que puede actualizar:")

    for i, pedido in enumerate(pedidos_actualizables):
        print(
            f"  {i + 1}. Pedido {pedido['id']} - {pedido['estado_envio']} - Cliente: {pedido['cliente_nombre']}"
        )

    try:
        seleccion: int = InputManager.leer_entero(
            f"Seleccione un pedido (1-{len(pedidos_actualizables)}): "
        )
        if seleccion < 1 or seleccion > len(pedidos_actualizables):
            print(">>> ERROR: Selección inválida")
            InputManager.pausar()
            return

        pedido_seleccionado: dict = pedidos_actualizables[seleccion - 1]

        print(f"\nPedido seleccionado: {pedido_seleccionado['id']}")
        print(f"Estado actual: {pedido_seleccionado['estado_envio']}")

        estados_disponibles: list[str] = ["EN_PROCESO", "ENVIADO", "ENTREGADO"]
        print("\nEstados disponibles:")
        for i, estado in enumerate(estados_disponibles):
            print(f"  {i + 1}. {estado}")

        estado_seleccion: int = InputManager.leer_entero(
            f"Seleccione el nuevo estado (1-{len(estados_disponibles)}): "
        )

        if estado_seleccion < 1 or estado_seleccion > len(estados_disponibles):
            print(">>> ERROR: Estado inválido")
            InputManager.pausar()
            return

        nuevo_estado: str = estados_disponibles[estado_seleccion - 1]

        confirmacion: bool = InputManager.leer_confirmacion(
            f"¿Confirma cambiar el estado a '{nuevo_estado}'? (S/N): "
        )

        if confirmacion:
            resultado: bool = SystemController.actualizar_estado_pedido(
                pedido_seleccionado["id"], nuevo_estado
            )

            if resultado:
                print(">>> Estado del pedido actualizado exitosamente")
            else:
                print(">>> ERROR: No se pudo actualizar el estado del pedido")
        else:
            print(">>> Actualización cancelada")

    except Exception as e:
        print(f">>> ERROR: {e}")

    InputManager.pausar()


def ver_estadisticas_vendedor(id_vendedor: str) -> None:
    """Muestra las estadísticas de ventas del vendedor"""
    estadisticas: dict = SystemController.obtener_estadisticas_vendedor(id_vendedor)

    if not estadisticas:
        print(">>> No se pudieron obtener las estadísticas")
        InputManager.pausar()
        return

    print("\n=== ESTADÍSTICAS DE VENTAS ===")
    print(f"Total de productos: {estadisticas['total_productos']}")
    print(f"Productos sin stock: {estadisticas['productos_sin_stock']}")
    print(f"Total de pedidos: {estadisticas['total_pedidos']}")
    print(f"Pedidos en proceso: {estadisticas['pedidos_en_proceso']}")
    print(f"Pedidos entregados: {estadisticas['pedidos_entregados']}")
    print(f"Pedidos en carrito: {estadisticas['pedidos_en_carrito']}")
    print(f"Pedidos enviados: {estadisticas['pedidos_enviados']}")
    print(f"Ventas totales: ${estadisticas['ventas_totales']:.2f}")

    if estadisticas["productos_mas_vendidos"]:
        print("\nProductos más vendidos:")
        for i, producto in enumerate(estadisticas["productos_mas_vendidos"]):
            print(
                f"  {i + 1}. {producto['nombre']} - {producto['cantidad_vendida']} unidades"
            )
    else:
        print("\nNo hay datos de productos vendidos")

    InputManager.pausar()


def menu_vendedor(id: str) -> None:
    print("=== BIENVENIDO VENDEDOR ===")
    opciones: list[str] = [
        "Ver todos mis productos",
        "Gestionar productos",
        "Gestionar pedidos",
        "Cerrar sesión",
        "Salir del sistema",
    ]
    seleccion: int = InputManager.leer_opcion_menu(opciones, "MENÚ VENDEDOR")
    productos: list[str] = []
    ids: list[str] = []
    match seleccion:
        case 1:
            productos, ids = SystemController.mostrar_productos_vendedor(id)
            if len(productos) == 0:
                print(">>> No cuenta con ningún producto registrado")
            else:
                print("\n=== SUS PRODUCTOS ===")
                for i, producto in enumerate(productos):
                    print(f"  {i + 1}. {producto}")
            InputManager.pausar()
        case 2:
            gestionar_productos(id)
        case 3:
            gestionar_pedidos_vendedor(id)
        case 4:
            sistema()
        case 5:
            print("\n=== CERRANDO SISTEMA ===")
            sys.exit(0)
    menu_vendedor(id)


def sistema() -> None:
    while True:
        print("\n=== INICIAR SESIÓN ===")
        email = InputManager.leer_texto_no_vacio("Ingrese su email: ")
        password = InputManager.leer_texto_no_vacio("Ingrese su contraseña: ")
        tupla_result = SystemController.iniciar_sesion(email, password)
        if not tupla_result[0]:
            print(">>> ERROR: Usuario no encontrado o credenciales incorrectas")
        else:
            print(f">>> Sesión iniciada correctamente como {tupla_result[1].upper()}")
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
