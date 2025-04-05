from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Models.models import Usuario
from Models.modelsp import Producto
from flask import Flask, render_template, request, redirect, url_for, flash, session,  jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from Conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'  # Necesario para formularios con CSRF

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Definir la clase de formulario
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Enviar')

# Ruta principal (Página de inicio)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        session['nombre'] = form.nombre.data  # Guardar en sesión
        flash('Formulario enviado con éxito!', 'success')
        return redirect(url_for('resultado'))
    return render_template('formulario.html', form=form)

# Ruta para mostrar el resultado
@app.route('/resultado')
def resultado():
    nombre = session.get('nombre', None)  # Obtener de sesión

    if nombre is None:  # Evita errores si no se ha llenado el formulario
        flash('No hay datos en la sesión. Ingresa tu nombre en el formulario.', 'warning')
        return redirect(url_for('formulario'))

    return render_template('resultado.html', nombre=nombre)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test_db')
def test_db():
    conexion = obtener_conexion()
    if conexion:
        return "Conexión exitosa a MySQL"
    else:
        return "Error en la conexión a MySQL"

# Ruta para obtener todos los usuarios de la base de datos
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM usurios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(usuarios)  # Retornar los datos en formato JSON
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

# Ruta para mostrar los usuarios en una tabla HTML
@app.route('/usuarios_formulario', methods=['GET'])
def usuarios_tabla():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('usuarios_formulario.html', usuarios=usuarios)
    else:
        return "Error en la conexión a la base de datos", 500

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (nombre, email, password_hash))
        conexion.commit()
        flash('Usuario registrado correctamente')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.obtener_por_email(email)

        if usuario and usuario.verificar_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso')
            return redirect(url_for('productos'))  # Cambiado a la ruta de productos
        else:
            flash('Email o contraseña incorrectos')

    return render_template('login.html')

@app.route('/productos')
def productos():
    productos = Producto.obtener_todos()
    return render_template('productos.html', productos=productos)

@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        if nombre and precio and stock:
            Producto.insertar(nombre, float(precio), int(stock))
            flash('Producto creado exitosamente.')
            return redirect(url_for('listar_productos'))
        else:
            flash('Todos los campos son obligatorios.')
    return render_template('crear_producto.html')

@app.route('/productos')
def listar_productos():
    productos = Producto.obtener_todos()
    return render_template('productos.html', productos=productos)
@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    producto = Producto.obtener_por_id(id_producto)
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        Producto.actualizar(id_producto, nombre, float(precio), int(stock))
        flash('Producto actualizado correctamente.')
        return redirect(url_for('listar_productos'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id_producto>', methods=['GET', 'POST'])
def eliminar_producto(id_producto):
    if request.method == 'POST':
        Producto.eliminar(id_producto)
        flash('Producto eliminado correctamente.')
        return redirect(url_for('listar_productos'))
    producto = Producto.obtener_por_id(id_producto)
    return render_template('eliminar_producto.html.html', producto=producto)
def insertar(nombre, precio, stock):
    cursor = conexion.cursor()

    # Obtener el id_producto más alto
    cursor.execute("SELECT MAX(id_producto) FROM productos")
    max_id = cursor.fetchone()[0]

    # Si no hay registros, establecer id_producto en 1
    if max_id is None:
        nuevo_id = 1
    else:
        nuevo_id = max_id + 1

    # Insertar el nuevo producto con el id_producto manual
    cursor.execute(
        "INSERT INTO productos (id_producto, nombre, precio, stock) VALUES (%s, %s, %s, %s)",
        (nuevo_id, nombre, precio, stock)
    )
    conexion.commit()
    cursor.close()


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)