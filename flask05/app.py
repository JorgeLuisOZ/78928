from flask import Flask, render_template, request, Response, redirect, url_for
import sqlite3
from producto import Producto 

app = Flask(__name__)

# productos = [Producto("Computadora", 22499), Producto("Impresora", 2999)]

@app.route('/')
def index():
    con = conexion()
    productos = con.execute('SELECT * FROM productos').fetchall()
    print(productos)
    con.close()
    return render_template('productos.html', productos=productos)

@app.route('/crear', methods=['POST'])
def crear():
    nombre = request.form['nombre']
    precio = request.form['precio']
    
    con = conexion()
    con.execute('INSERT INTO productos (nombre, precio) values (?,?)', (nombre,precio))
    con.commit()
    con.close()
    # return Response("creado", headers={'Location':'/'}, status=302)
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    con = conexion()
    p = con.execute('SELECT * FROM productos WHERE id = ?', (id)).fetchone()
    con.close()
    # se crea la plantilla para editar el producto deseado
    return render_template('editar.html', producto=p)

@app.route('/guardar', methods=['POST'])
def guardar():
    n=request.form.get('nombre')
    p=request.form.get('precio')
    id=request.form.get('id')
    print(f"{n} {p} {id}")
    
    con = conexion()
    con.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (n,p,id))
    con.commit()
    con.close()
    return Response("guardado", headers={'Location': '/'}, status=302)

@app.route('/eliminar/<id>')
def eliminar(id):
    con = conexion()
    con.execute('DELETE FROM productos WHERE id=?', (id))
    con.commit()
    con.close()
    return Response("eliminado", headers={'Location': '/'}, status=302)

def conexion():
    con = sqlite3.connect('basedatos.db')
    # row_factory
    # hace que las consultas se vuelvan diccionarios pudiendo 
    # seleccionar valores mediante ['nombre_columna']
    con.row_factory = sqlite3.Row
    return con

def iniciar_db():
    con = conexion()
    # se crea la tabla en caso de que no exista

    con.execute('''
        CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
        )
    ''')

    con.commit()
    # salva los datos depues de la ejecucion 
    con.close()

if __name__ == '__main__':
    iniciar_db()
    app.run(host='0.0.0.0', debug=True)
