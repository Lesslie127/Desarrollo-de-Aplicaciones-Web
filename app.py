from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os

app = Flask(__name__)

# Configuración de la base de datos SQLite con ruta absoluta
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'usuarios.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Modelo para la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Ruta para guardar datos en un archivo TXT
@app.route('/guardar_txt', methods=['POST'])
def guardar_txt():
    data = request.json
    if 'nombre' not in data or 'edad' not in data:
        return jsonify({"error": "Faltan datos: 'nombre' y 'edad' son requeridos."}), 400
    with open('datos/datos.txt', 'a') as f:
        f.write(f"{data['nombre']}, {data['edad']}\n")
    return jsonify({"mensaje": "Datos guardados en archivo TXT."})

# Ruta para leer datos desde el archivo TXT
@app.route('/leer_txt', methods=['GET'])
def leer_txt():
    try:
        with open('datos/datos.txt', 'r') as f:
            contenido = f.readlines()
        return jsonify({"datos": [line.strip() for line in contenido]})
    except FileNotFoundError:
        return jsonify({"error": "El archivo TXT no existe."})

# Ruta para guardar datos en un archivo JSON
@app.route('/guardar_json', methods=['POST'])
def guardar_json():
    data = request.json
    if not data.get('nombre') or not isinstance(data.get('edad'), int):
        return jsonify({"error": "Datos inválidos, asegúrate de enviar 'nombre' como cadena y 'edad' como entero."}), 400
    with open('datos/datos.json', 'a') as f:
        json.dump(data, f)
        f.write("\n")
    return jsonify({"mensaje": "Datos guardados en archivo JSON."})

# Ruta para leer datos desde el archivo JSON
@app.route('/leer_json', methods=['GET'])
def leer_json():
    try:
        with open('datos/datos.json', 'r') as f:
            contenido = [json.loads(line) for line in f]
        return jsonify({"datos": contenido})
    except FileNotFoundError:
        return jsonify({"error": "El archivo JSON no existe."})

# Ruta para guardar datos en un archivo CSV
@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    data = request.json
    if 'nombre' not in data or 'edad' not in data:
        return jsonify({"error": "Faltan datos: 'nombre' y 'edad' son requeridos."}), 400
    with open('datos/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['nombre'], data['edad']])
    return jsonify({"mensaje": "Datos guardados en archivo CSV."})

# Ruta para leer datos desde el archivo CSV
@app.route('/leer_csv', methods=['GET'])
def leer_csv():
    try:
        with open('datos/datos.csv', 'r') as f:
            reader = csv.reader(f)
            contenido = [row for row in reader]
        return jsonify({"datos": contenido})
    except FileNotFoundError:
        return jsonify({"error": "El archivo CSV no existe."})

# Ruta para guardar datos en SQLite
@app.route('/guardar_sqlite', methods=['POST'])
def guardar_sqlite():
    data = request.json
    if 'nombre' not in data or 'edad' not in data:
        return jsonify({"error": "Faltan datos: 'nombre' y 'edad' son requeridos."}), 400
    nuevo_usuario = Usuario(nombre=data['nombre'], edad=data['edad'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Datos guardados en base de datos SQLite."})

# Ruta para leer datos desde SQLite
@app.route('/leer_sqlite', methods=['GET'])
def leer_sqlite():
    usuarios = Usuario.query.all()
    return jsonify({"usuarios": [{"id": u.id, "nombre": u.nombre, "edad": u.edad} for u in usuarios]})

if __name__ == '__main__':
    app.run(debug=True)
