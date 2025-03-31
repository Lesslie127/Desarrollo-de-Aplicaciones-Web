from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from Conexion.conexion import obtener_conexion
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Models.models import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'  # Necesario para formularios con CSRF

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Definir la clase de formulario
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Definir el formulario para el nombre (el formulario de inicio)
class NombreForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
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
        return redirect(url_for('about'))  # Redirigir a la página "Acerca de"
    return render_template('index.html', form=form)

# Ruta para la página "Acerca de" (Bienvenida)
@app.route('/about')
def about():
    nombre = session.get('nombre')  # Obtener el nombre desde la sesión
    if not nombre:
        flash('Por favor, ingresa tu nombre primero.', 'warning')
        return redirect(url_for('formulario'))
    return render_template('about.html', nombre=nombre)

# Ruta para registrar usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (nombre, email, password))
        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Usuario registrado correctamente')
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        usuario = Usuario.obtener_por_email(email)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash('Inicio de sesión exitoso')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos')

    return render_template('login.html', form=form)

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada')
    return redirect(url_for('index'))

# Ruta protegida (solo accesible si estás logueado)
@app.route('/protegido')
@login_required
def protegido():
    return f'Bienvenido, {current_user.nombre}. Esta es una página protegida.'

# Función de Flask-Login para cargar un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
