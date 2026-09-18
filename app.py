from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "cambia_esto_por_algo_secreto_123"


@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect("/inventario")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE usuario = ? AND contrasena = ?
    """, (usuario, contrasena_hash))

    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        session["usuario"] = usuario
        return redirect("/inventario")
    else:
        return render_template("login.html", error="Usuario o contraseña incorrectos.")


@app.route("/inventario")
def inventario():
    if "usuario" not in session:
        return redirect("/")

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    return render_template("inventario.html", productos=productos, usuario=session["usuario"])

@app.route("/agregar_producto", methods=["POST"])
def agregar_producto_web():
    if "usuario" not in session:
        return redirect("/")

    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    stock = int(request.form["stock"])

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, precio, stock)
        VALUES (?, ?, ?)
    """, (nombre, precio, stock))
    conexion.commit()
    conexion.close()
    return redirect("/inventario")

@app.route("/editar_producto/<int:id_producto>")
def mostrar_editar_producto(id_producto):
    if "usuario" not in session:
        return redirect("/")

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    conexion.close()

    return render_template("editar_producto.html", producto=producto)


@app.route("/editar_producto/<int:id_producto>", methods=["POST"])
def guardar_edicion(id_producto):
    if "usuario" not in session:
        return redirect("/")

    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    stock = int(request.form["stock"])

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre = ?, precio = ?, stock = ?
        WHERE id = ?
    """, (nombre, precio, stock, id_producto))
    conexion.commit()
    conexion.close()

    return redirect("/inventario")


@app.route("/eliminar_producto/<int:id_producto>", methods=["POST"])
def eliminar_producto_web(id_producto):
    if "usuario" not in session:
        return redirect("/")

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()

    return redirect("/inventario")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/registro", methods=["POST"])
def crear_cuenta():
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]
    contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, contrasena)
            VALUES (?, ?)
        """, (usuario, contrasena_hash))
        conexion.commit()
        conexion.close()
        return redirect("/")
    except sqlite3.IntegrityError:
        conexion.close()
        return render_template("registro.html", error="Ese usuario ya existe.")
    
if __name__ == "__main__":
    app.run(debug=True)