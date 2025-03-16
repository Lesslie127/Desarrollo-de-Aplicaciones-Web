from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from Conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'  # Necesario para formularios con CSRF

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

# Ruta "About"
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para probar la conexión a la base de datos
@app.route('/test_db')
def test_db():
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            conexion.close()
            return "Conexión exitosa a MySQL"
        else:
            return "Error en la conexión a MySQL"
    except Exception as e:
        return f"Error al conectar a la base de datos: {str(e)}"

# Ruta para obtener todos los usuarios de la base de datos en formato JSON
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)  # Resultados en formato de diccionario
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
            return jsonify(usuarios)  # Retornar los datos en formato JSON
        else:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuarios: {str(e)}"}), 500

# Ruta para mostrar los usuarios en una tabla HTML
@app.route('/usuarios_formulario', methods=['GET'])
def usuarios_tabla():
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)  # Resultados en formato de diccionario
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
            return render_template('usuarios_formulario.html', usuarios=usuarios)
        else:
            return "Error en la conexión a la base de datos", 500
    except Exception as e:
        return f"Error al cargar usuarios: {str(e)}", 500

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
