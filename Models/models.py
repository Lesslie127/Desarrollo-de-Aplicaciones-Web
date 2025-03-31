from flask_login import UserMixin
from Conexion.conexion import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin):
    def __init__(self, idusuarios, nombre, email, password):
        self.id = idusuarios
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT idusuarios, nombre, email, password FROM usuarios WHERE email = %s", (email,))
        fila = cursor.fetchone()
        conexion.close()
        if fila:
            return Usuario(*fila)
        return None

    @staticmethod
    def obtener_por_id(idusuarios):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT idusuarios, nombre, email, password FROM usuarios WHERE idusuarios = %s", (idusuarios,))
        fila = cursor.fetchone()
        conexion.close()
        if fila:
            return Usuario(*fila)
        return None

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        password_hash = generate_password_hash(self.password)
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (self.nombre, self.email, password_hash))
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar_password(idusuarios, nueva_password):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        password_hash = generate_password_hash(nueva_password)
        cursor.execute("UPDATE usuarios SET password = %s WHERE idusuarios = %s", (password_hash, idusuarios))
        conexion.commit()
        conexion.close()
