from datetime import datetime
import hashlib
from flask_menu import Menu, register_menu
from flask import Flask, request, render_template, Response, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #flash 
usuario_actual = ''
Menu(app = app) 

from Clases import db
from Clases import Usuario, Receta, Ingrediente

@app.route('/') #ruta raiz
def index ():
    #global usuario_actual
    # return 'hola mundo'
    #usuario_actual = -1 #luego tengo que redefinir la seguridad de las demas paginas
    return render_template('index.html')

@app.route('/login/', methods = [ 'GET', 'POST' ])
def login ():
    global usuario_actual
    if request.method == 'POST':
        if not request.form[ 'email' ] or not request.form[ 'password' ]:
            return render_template('error.html', mensaje = 'Los datos no son correctos')
        else:
            usuario_actual = Usuario.query.filter_by(correo = request.form['email']).first()
            if usuario_actual is None:
                return render_template('error.html', error = 'El correo no esta registrado')
            else:
                verificacion = hashlib.md5(bytes(request.form['password'], encoding = 'utf-8'))
                if (usuario_actual.clave == verificacion.hexdigest()):
                    return render_template('index.html', usuarioActual = usuario_actual.id)
                else:
                    return render_template('error.html', error = 'La contraseña no es valida')
    else:
        return render_template('login.html')

@app.route('/receta/', methods = [ 'GET', 'POST' ])
def receta ():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['tiempo'] or not request.form['descripcion']:
            return render_template('error.html', error='Contenido no ingresado')
        else:
            nueva_receta = Receta(nombre = request.form['nombre'], tiempo = request.form['tiempo'], fecha = datetime.today(), elaboracion = request.form['descripcion'], cantidadmegusta = 0, usuarioid = request.form['usuario_id'])
            db.session.add( nueva_receta )
            db.session.commit()
            flash('Receta agregada exitosamente')
            cantidad = request.form['cantidad'] #obtengo la cantidad de ingredientes que se ingreso en el form
            #receta_actual = Receta.query.filter_by(nombre = request.form['nombreReceta']).first()
            return render_template('ingrediente.html', recetaActual = nueva_receta.id, cantidadIngredientes = cantidad) #le envio al html para usar el for
    else:
        return render_template('receta.html')

@app.route('/ingrediente/', methods = [ 'GET', 'POST' ])
def ingrediente ():
    i = 0
    if request.method == 'POST':
        if not request.form['nombreIngrediente'] or not request.form['cantidad'] or not request.form['unidad']:
            return render_template('error.html', error='Contenido no ingresado')
        else:
            while i < 10:
                if request.form['nombreIngrediente'] is not None and request.form['cantidad'] is not None and request.form['unidad'] is not None:
                    nuevo_ingrediente = Ingrediente(nombre = request.form['nombreIngrediente'+str(i)], cantidad = request.form['cantidad'+str(i)], unidad = request.form['unidad'+str(i)], recetaid = request.form['receta_id'])
                    db.session.add( nuevo_ingrediente )
                    db.session.commit()
                    i += 1
                else:
                    i = 10
    return render_template('ingrediente.html') 


if __name__ == '__main__':
    app.run(debug = True)
    