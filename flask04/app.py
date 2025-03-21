from flask import Flask, render_template, request, Response, redirect, url_for
from producto import Producto 

app = Flask(__name__)

productos = [Producto("Computadora", 22499), Producto("Impresora", 2999)]

@app.route('/')
def index():
    # productos = [Producto("Computadora", 22499), Producto("Impresora", 2999)]
    return render_template('productos.html', productos=productos)

@app.route('/crear', methods=['POST'])
def crear():
    nombre = request.form['nombre']
    precio = request.form['precio']
    productos.append(Producto(nombre, precio))
    
    # return Response("creado", headers={'Location':'/'}, status=302)
    return redirect(url_for('index'))

@app.route('/editar/<producto>/<precio>')
def editar(producto, precio):
    # recuperar el producto
    print(producto, precio)
    return render_template('editar.html', producto=producto, precio=precio)

@app.route('/guardar', methods=['POST'])
def guardar():
    n=request.form['nombre']
    p=request.form['precio']
    print(n, p)
    i = 0 
    for e in productos:
        if e.nombre == n:
            productos[i] = Producto(n, p)
            print(f"{e.nombre} {e.precio}")
        i+=1
    return Response("guardado", headers={'Location': '/'}, status=302)

@app.route('/eliminar/<nombre>')
def eliminar(nombre):
    i=0
    for e in productos:
        if e.nombre == nombre:
            productos.pop(i)
        i+=1
    return Response("eliminado", headers={'Location': '/'}, status=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
