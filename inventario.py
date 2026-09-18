import sqlite3
import hashlib
 
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
)
""")
 
conexion.commit()
conexion.close()
 
print("Base de datos y tablas creadas correctamente.")
 
 
def agregar_producto(nombre, precio, stock):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
 
    cursor.execute("""
        INSERT INTO productos (nombre, precio, stock)
        VALUES (?, ?, ?)
    """, (nombre, precio, stock))
 
    conexion.commit()
    conexion.close()
    print(f"Producto '{nombre}' agregado correctamente.")
 
 
def mostrar_productos():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
 
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
 
    conexion.close()
 
    if not productos:
        print("No hay productos registrados.")
        return
 
    print("\n--- Inventario ---")
    for producto in productos:
        id, nombre, precio, stock = producto
        print(f"ID: {id} | {nombre} | ${precio:.2f} | Stock: {stock}")
 
 
def actualizar_stock(id_producto, nuevo_stock):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
 
    cursor.execute("""
        UPDATE productos
        SET stock = ?
        WHERE id = ?
    """, (nuevo_stock, id_producto))
 
    conexion.commit()
 
    if cursor.rowcount == 0:
        print(f"No se encontró un producto con ID {id_producto}.")
    else:
        print(f"Stock del producto con ID {id_producto} actualizado a {nuevo_stock}.")
 
    conexion.close()
 
 
def eliminar_producto(id_producto):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
 
    cursor.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (id_producto,))
 
    conexion.commit()
 
    if cursor.rowcount == 0:
        print(f"No se encontró un producto con ID {id_producto}.")
    else:
        print(f"Producto con ID {id_producto} eliminado correctamente.")
 
    conexion.close()
 
 
def crear_usuario(usuario, contrasena):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
 
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
 
    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, contrasena)
            VALUES (?, ?)
        """, (usuario, contrasena_hash))
        conexion.commit()
        print(f"Usuario '{usuario}' creado correctamente.")
    except sqlite3.IntegrityError:
        print(f"El usuario '{usuario}' ya existe.")
 
    conexion.close()
 
 
def menu():
    while True:
        print("\n===== MENÚ INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Actualizar stock")
        print("4. Eliminar producto")
        print("5. Salir")
 
        opcion = input("Elige una opción: ")
 
        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            agregar_producto(nombre, precio, stock)
 
        elif opcion == "2":
            mostrar_productos()
 
        elif opcion == "3":
            id_producto = int(input("ID del producto a actualizar: "))
            nuevo_stock = int(input("Nuevo stock: "))
            actualizar_stock(id_producto, nuevo_stock)
 
        elif opcion == "4":
            id_producto = int(input("ID del producto a eliminar: "))
            eliminar_producto(id_producto)
 
        elif opcion == "5":
            print("¡Hasta luego!")
            break
 
        else:
            print("Opción no válida, intenta de nuevo.")
 
 
# Crea el usuario UNA sola vez, luego comenta esta línea
# crear_usuario("Imer", "1234")
 
menu()