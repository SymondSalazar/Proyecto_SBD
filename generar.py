from pathlib import Path
from datetime import date, timedelta
import random
import csv

# Crear carpeta para guardar los archivos
output_dir = Path("C:/Users/INTEL/Desktop/Proyecto_BD/datos_bd")
output_dir.mkdir(exist_ok=True)

# Generadores auxiliares
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def write_csv(filename, header, rows):
    with open(output_dir / filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

# Datos base
cuentas = [
    ("cuenta{:03d}".format(i), f"user{i}@email.com", f"Nombre{i}", random_date(date(2023, 1, 1), date(2024, 12, 31)))
    for i in range(1, 11)
]

clientes = [("cuenta{:03d}".format(i), f"Calle {i*10} y Av. Ejemplo") for i in range(1, 6)]
vendedores = [("cuenta{:03d}".format(i), f"Vendedor {i}", random.choice(["ALTO", "MEDIO", "BAJO"])) for i in range(6, 11)]

categorias = ["Electrónica", "Ropa", "Hogar", "Juguetes", "Libros", "Deportes", "Oficina", "Mascotas", "Salud", "Belleza"]

productos = []
imagenes = []
for i in range(1, 11):
    pid = f"prod{i:03d}"
    productos.append((
        pid,
        f"Producto{i}",
        f"Descripción del producto {i}",
        random.randint(1, 5),
        random.randint(5, 50),
        round(random.uniform(10.0, 200.0), 2),
        random.choice(categorias),
        random.choice(vendedores)[0]
    ))
    imagenes.append((f"https://img.com/producto{i}.jpg", pid))

pedidos = []
pedidos_productos = []
for i in range(1, 11):
    pid = f"ped{i:03d}"
    cliente_id = random.choice(clientes)[0]
    pedidos.append((
        pid,
        cliente_id,
        random.choice(["PENDIENTE", "ENVIADO", "ENTREGADO"]),
        f"Dirección {i*7} de entrega",
        random_date(date(2025, 7, 25), date(2025, 8, 30)),
        random_date(date(2025, 6, 1), date(2025, 7, 25))
    ))
    for _ in range(random.randint(1, 3)):
        pedidos_productos.append((
            pid,
            random.choice(productos)[0],
            random.randint(1, 5)
        ))

reseñas = []
for i in range(1, 11):
    reseñas.append((
        f"res{i:03d}",
        random.choice(clientes)[0],
        random.choice(productos)[0],
        random.randint(1, 5),
        f"Comentario {i}"
    ))

# Escribir archivos
write_csv("cuentas.txt", ["id", "email", "nombre", "fecha_creacion"], cuentas)
write_csv("clientes.txt", ["cuenta_id", "direccion_envio"], clientes)
write_csv("vendedores.txt", ["cuenta_id", "descripcion", "valoracion"], vendedores)
write_csv("productos_categorias.txt", ["nombre"], [[c] for c in categorias])
write_csv("productos.txt", ["id", "nombre", "descripcion", "calificacion", "stock", "precio", "categoria", "vendedor_id"], productos)
write_csv("productos_imagenes.txt", ["url", "product_id"], imagenes)
write_csv("pedidos.txt", ["id", "cliente_id", "estado_envio", "direccion_entrega", "fecha_entrega", "fecha_creacion"], pedidos)
write_csv("pedidos_productos.txt", ["pedido_id", "producto_id", "cantidad"], pedidos_productos)
write_csv("productos_reseñas.txt", ["id", "cliente_id", "producto_id", "calificacion", "comentario"], reseñas)

print(output_dir)