import sqlite3
import pandas as pd
import os


def migrar_datos():
    # Conectar a la base de datos
    conn = sqlite3.connect("datos_bd/ecommerce.db")

    # Lista de archivos CSV
    archivos_csv = [
        "clientes.csv",
        "cuentas.csv",
        "pedidos.csv",
        "pedidos_productos.csv",
        "productos.csv",
        "productos_categorias.csv",
        "productos_imagenes.csv",
        "productos_reseñas.csv",
        "vendedores.csv",
    ]

    for archivo in archivos_csv:
        ruta = f"datos_bd/{archivo}"
        if os.path.exists(ruta):
            # Leer CSV
            df = pd.read_csv(ruta)

            # Obtener nombre de tabla (quitar .csv)
            tabla = archivo.replace(".csv", "")

            # Insertar datos en la tabla
            df.to_sql(tabla, conn, if_exists="replace", index=False)
            print(f"Migrados datos de {archivo} a tabla {tabla}")

    conn.close()
    print("Migración completada")


if __name__ == "__main__":
    migrar_datos()
